# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/loader.py
Purpose: Load a local catalog and report schema, reference, and index diagnostics.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Read-only. Installed schemas come from package data. A source checkout uses schemas/ beside src.
No network retrieval.
Related decision: DEV-2026-11-19-006, DEV-2026-11-19-012.
"""

from pathlib import Path
import hashlib
import json
import re
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
import yaml
from yaml.tokens import AliasToken, AnchorToken, TagToken

from ysl_components import SUPPORTED_SCHEMA_VERSION


INDEX_NAME = 'catalog-index.json'
INDEX_ALGORITHM = 'sha256-definition-bytes-v1'


class ParseFailure(Exception):
    """Purpose: Keep a loader rejection distinct from a crash.
    Design: Carry a frozen diagnostic code. Workflow: YAML construction.
    Data Handoff: Code and message for stderr.
    """

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class ReviewLoader(yaml.SafeLoader):
    """Purpose: Bound catalog YAML. Design: JSON booleans and unique string keys.
    Workflow: One definition document. Data Handoff: JSON-compatible data.
    """


ReviewLoader.yaml_implicit_resolvers = {
    key: [(tag, regex) for tag, regex in rules if tag != 'tag:yaml.org,2002:bool']
    for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
ReviewLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$'), list('tf'))


def unique_mapping(loader, node, deep=False):
    """Purpose: Reject lost or non-string keys. Design: Inspect source nodes before construction.
    Workflow: YAML load. Data Handoff: Mapping or ParseFailure.
    """
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ParseFailure('YAML_KEY_TYPE', f'line {key_node.start_mark.line + 1}')
        if key in result:
            raise ParseFailure('YAML_DUPLICATE_KEY', f'{key} at line {key_node.start_mark.line + 1}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


ReviewLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def pointer(parts):
    """Purpose: Give diagnostics a stable location. Design: JSON Pointer escaping.
    Workflow: Schema and semantic checks. Data Handoff: Pointer string.
    """
    return '/' + '/'.join(str(part).replace('~', '~0').replace('/', '~1') for part in parts)


def diagnostic(code, file, path, message):
    """Purpose: Build one stderr record. Design: Four frozen fields.
    Workflow: Every rejection. Data Handoff: JSON-ready mapping.
    """
    return {'code': code, 'file': file, 'message': message, 'path': path}


def load_yaml_text(text):
    """Purpose: Read one component document. Design: Forbid aliases, tags, and non-JSON values.
    Workflow: Each definition.yml. Data Handoff: Data or ParseFailure.
    """
    try:
        if any(isinstance(token, (AliasToken, AnchorToken, TagToken)) for token in yaml.scan(text)):
            raise ParseFailure('YAML_CONSTRUCT_FORBIDDEN', 'anchors, aliases, and explicit tags are unsupported')
        data = yaml.load(text, Loader=ReviewLoader)
        if data is None:
            raise ParseFailure('YAML_SYNTAX', 'document is empty')
        json.dumps(data, allow_nan=False)
        return data
    except ParseFailure:
        raise
    except yaml.YAMLError as error:
        raise ParseFailure('YAML_SYNTAX', str(error).splitlines()[0]) from error
    except (TypeError, ValueError, OverflowError) as error:
        raise ParseFailure('YAML_NON_JSON_VALUE', str(error)) from error


def schema_directory():
    """Purpose: Find the approved schemas. Design: Prefer files shipped inside the installed package.
    A source checkout has no data directory, so it keeps the repository schemas directory.
    Workflow: Validator construction. Data Handoff: Directory path.
    """
    packaged = Path(__file__).resolve().parent / 'data' / 'schemas'
    if (packaged / 'component.schema.json').is_file():
        return packaged
    return Path(__file__).resolve().parents[2] / 'schemas'


def packaged_catalog_directory():
    """Purpose: Find the catalog shipped with the installed command.
    Design: Absent in a source checkout, so development invocation cannot grow a silent default.
    Workflow: ysl-components when --catalog is omitted. Data Handoff: Directory or None.
    """
    path = Path(__file__).resolve().parent / 'data' / 'catalog'
    if path.is_dir():
        return path
    return None


def component_validator():
    """Purpose: Validate the current component schema offline.
    Design: Register local URN resources and enable format checks. No retriever is attached.
    Workflow: Once per process. Data Handoff: Draft 2020-12 validator.
    """
    registry = Registry()
    directory = schema_directory()
    for path in sorted(directory.glob('*.schema.json')):
        schema = json.loads(path.read_text(encoding='utf-8'))
        if '$id' in schema:
            registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
    component = json.loads((directory / 'component.schema.json').read_text(encoding='utf-8'))
    return Draft202012Validator(component, registry=registry, format_checker=FormatChecker())


def semantic_errors(document):
    """Purpose: Check references, quantities, inheritance, and positions.
    Design: Same rules as the schema-review harness, applied to one schema-valid document.
    Workflow: After JSON Schema succeeds. Data Handoff: Diagnostic field records without a file name.
    """
    errors = []

    def error(code, path, message):
        """Purpose: Collect one semantic failure. Design: Stable pointer.
        Workflow: Nested checks. Data Handoff: Appends a record.
        """
        errors.append({'code': code, 'path': pointer(path), 'message': message})

    variants = {f'variant:{key}': value for key, value in document.get('variants', {}).items()}
    variants.update({f'profile:{key}': value for key, value in document.get('profiles', {}).items()})
    local_names = set()
    for name in [document.get('id', ''), *document.get('aliases', [])]:
        folded = name.casefold() if isinstance(name, str) else ''
        if folded in local_names:
            error('ALIAS_COLLISION', ['aliases'], str(name))
        local_names.add(folded)

    def check_cycles(nodes, targets, code, base_path):
        """Purpose: Reject cyclic inheritance and power dependencies.
        Design: Depth-first coloring. Workflow: One document. Data Handoff: Diagnostics.
        """
        active = set()
        done = set()

        def visit(key):
            """Purpose: Walk one dependency chain. Design: Track the active set.
            Workflow: Cycle check. Data Handoff: Diagnostics and visited state.
            """
            if key in active:
                error(code, base_path + [key], key)
                return
            if key in done or key not in nodes:
                return
            active.add(key)
            for target in targets(nodes[key]):
                visit(target)
            active.remove(key)
            done.add(key)

        for key in nodes:
            visit(key)

    check_cycles(variants, lambda item: [item['inherits']] if 'inherits' in item else [], 'INHERITANCE_CYCLE', ['variants'])
    check_cycles(document.get('power_domains', {}), lambda item: item.get('input_dependencies', []), 'POWER_CYCLE', ['power_domains'])

    def context(member=None):
        """Purpose: Build one member's visible entities. Design: Base tables plus ancestor overrides.
        Workflow: Reference and position checks. Data Handoff: Entity maps.
        """
        tables = {
            'pin': dict(document['pins']),
            'connector': document['connectors'],
            'interface': dict(document['interfaces']),
            'processor': document.get('board', {}).get('processors', {}),
            'component': document.get('onboard_components', {}),
            'feature': document.get('features', {}),
            'power_domain': document.get('power_domains', {}),
        }
        chain = []
        visited = set()
        while member in variants and member not in visited:
            visited.add(member)
            chain.append(variants[member])
            member = variants[member].get('inherits')
        for item in reversed(chain):
            tables['pin'].update(item.get('pins', {}))
            tables['interface'].update(item.get('interfaces', {}))
        return tables

    def resolve(namespace, key, path, tables):
        """Purpose: Reject a dangling typed name. Design: Local tables only.
        Workflow: Each reference. Data Handoff: Diagnostic or nothing.
        """
        if key not in tables.get(namespace, {}):
            error('REF_NOT_FOUND', path, f'{namespace}:{key}')

    def walk(node, path, tables):
        """Purpose: Find semantic references without treating fact names as fields.
        Design: Explicit reference keys. Map entry names stay identities.
        Workflow: Nested entities. Data Handoff: Diagnostics.
        """
        if isinstance(node, list):
            for offset, value in enumerate(node):
                walk(value, path + [offset], tables)
            return
        if not isinstance(node, dict):
            return
        if 'dimension' in node and 'unit' in node:
            if 'min' in node and 'max' in node and node['min'] > node['max']:
                error('QUANTITY_ORDER', path, 'min exceeds max')
            for field in ('value', 'nominal', 'typical'):
                if field in node and (('min' in node and node[field] < node['min']) or ('max' in node and node[field] > node['max'])):
                    error('QUANTITY_OUT_OF_RANGE', path + [field], field)
        if node.get('status') == 'conflicting' and 'claims' in node:
            values = {json.dumps(claim.get('value'), sort_keys=True) for claim in node['claims']}
            if len(values) < 2:
                error('CONFLICT_NOT_DISTINCT', path + ['claims'], 'conflict needs distinct values')
        for key, value in node.items():
            location = path + [key]
            if key in ('facts', 'sources', 'records', 'pins', 'connectors', 'interfaces', 'onboard_components', 'processors', 'features', 'connections', 'resource_conflicts', 'power_domains', 'constraints'):
                for name, details in value.items():
                    walk(details, location + [name], tables)
                continue
            if key in ('source_refs', 'evidence_refs'):
                known = document['sources'] if key == 'source_refs' else document['verification']['records']
                for offset, target in enumerate(value):
                    if target not in known:
                        error('REF_NOT_FOUND', location + [offset], target)
            elif key in ('from', 'to', 'target') and isinstance(value, str) and ':' in value:
                namespace, target = value.split(':', 1)
                resolve(namespace, target, location, tables)
            elif key in ('via', 'participants', 'targets', 'feeds', 'protection_refs'):
                for offset, reference in enumerate(value):
                    if isinstance(reference, str) and ':' in reference:
                        namespace, target = reference.split(':', 1)
                        resolve(namespace, target, location + [offset], tables)
            elif key in ('affected_pins', 'pin_refs', 'connector_refs', 'input_dependencies'):
                namespace = {'affected_pins': 'pin', 'pin_refs': 'pin', 'connector_refs': 'connector', 'input_dependencies': 'power_domain'}[key]
                for offset, target in enumerate(value):
                    resolve(namespace, target, location + [offset], tables)
            elif key in ('processor', 'connector', 'shared_with') and isinstance(value, str):
                resolve({'processor': 'processor', 'connector': 'connector', 'shared_with': 'pin'}[key], value, location, tables)
            elif key == 'signals' and isinstance(value, dict):
                for role, targets in value.items():
                    for target in targets if isinstance(targets, list) else [targets]:
                        if isinstance(target, str):
                            resolve('pin', target, location + [role], tables)
                continue
            elif key == 'inherits' and value not in variants:
                error('REF_NOT_FOUND', location, str(value))
            if key in ('variants', 'profiles'):
                label = 'variant' if key == 'variants' else 'profile'
                for member, details in value.items():
                    walk(details, location + [member], context(f'{label}:{member}'))
            else:
                walk(value, location, tables)

    def positions(tables, path):
        """Purpose: Keep connector coordinates unique. Design: Normalize numeric positions.
        Workflow: Base and member scopes. Data Handoff: Diagnostics.
        """
        occupied = {}
        for key, pin in tables['pin'].items():
            if 'location' not in pin:
                continue
            location = pin['location']
            position = location['position']
            numeric = isinstance(position, (int, float)) and not isinstance(position, bool)
            normalized = str(int(position)) if numeric or (isinstance(position, str) and position.isdigit()) else str(position)
            coordinate = (location['connector'], normalized)
            if coordinate in occupied:
                error('POSITION_COLLISION', path + ['pins', key, 'location'], str(coordinate))
            occupied[coordinate] = key
            connector = tables['connector'].get(location['connector'], {})
            if normalized.isdigit() and 'positions' in connector and not 1 <= int(normalized) <= connector['positions']:
                error('POSITION_OUT_OF_RANGE', path + ['pins', key, 'location', 'position'], normalized)
        check_cycles(tables['pin'], lambda item: [item['shared_with']] if 'shared_with' in item else [], 'SHARED_PIN_CYCLE', path + ['pins'])

    tables = context()
    walk(document, [], tables)
    positions(tables, [])
    for member in variants:
        positions(context(member), [member])
    status = document['verification']['status']
    if status != 'not_verified':
        kind = 'bench_test' if status == 'bench_tested' else 'document_review'
        records = document['verification'].get('records', {})
        if not any(record.get('kind') == kind and record.get('result') == 'pass' for record in records.values()):
            error('VERIFICATION_EVIDENCE_MISSING', ['verification'], kind)
    return errors


class LoadedFile:
    """Purpose: Retain one in-scope definition. Design: Raw bytes stay the hash input.
    Workflow: Catalog load. Data Handoff: Document, digest, and file-local diagnostics.
    """

    def __init__(self, relative, raw):
        self.relative = relative
        self.raw = raw
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self.document = None
        self.schema_version = None
        self.schema_ok = False
        self.diagnostics = []


class Catalog:
    """Purpose: Hold a loaded directory. Design: Definitions are the answer source.
    Workflow: Passed to query operations. Data Handoff: Files, diagnostics, digest, index state.
    """

    def __init__(self, root, files, diagnostics, index_state, digest):
        self.root = root
        self.files = files
        self.diagnostics = diagnostics
        self.index_state = index_state
        self.digest = digest

    def exit_code(self):
        """Purpose: Apply the frozen precedence. Design: Unsupported schema outranks other data errors.
        Workflow: Before a query result is returned. Data Handoff: Process exit code 0, 2, or 5.
        """
        codes = {item['code'] for item in self.diagnostics}
        if 'SCHEMA_UNSUPPORTED' in codes:
            return 5
        if self.diagnostics:
            return 2
        return 0


def catalog_digest(files):
    """Purpose: Identify definition bytes. Design: Sorted relative paths, independent of the index.
    Workflow: Envelope construction. Data Handoff: Hex digest.
    """
    payload = ''.join(f'{item.relative}\0{item.sha256}\n' for item in files)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def check_index(root, files):
    """Purpose: Reject a derived index that does not match the files.
    Design: Absence is allowed. Mismatch is never used as an answer. No rewrite.
    Workflow: After definition bytes are hashed. Data Handoff: Index state and diagnostics.
    """
    path = root / INDEX_NAME
    if not path.is_file():
        return 'absent', []
    relative = INDEX_NAME
    try:
        index = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return 'invalid', [diagnostic('INDEX_INVALID', relative, '', str(error).splitlines()[0])]
    definitions = index.get('definitions') if isinstance(index, dict) else None
    shape_ok = (
        isinstance(index, dict)
        and index.get('schema_version') == SUPPORTED_SCHEMA_VERSION
        and index.get('algorithm') == INDEX_ALGORITHM
        and isinstance(definitions, list)
    )
    if not shape_ok:
        return 'invalid', [diagnostic('INDEX_INVALID', relative, '', 'index shape is not the frozen object')]
    recorded = []
    for entry in definitions:
        if not isinstance(entry, dict) or not isinstance(entry.get('path'), str) or not isinstance(entry.get('sha256'), str):
            return 'invalid', [diagnostic('INDEX_INVALID', relative, '/definitions', 'each entry needs path and sha256')]
        recorded.append((entry['path'], entry['sha256']))
    actual = [(item.relative, item.sha256) for item in files]
    if sorted(recorded) != actual:
        return 'stale', [diagnostic('INDEX_STALE', relative, '', 'index does not match definition bytes')]
    return 'fresh', []


def load_catalog(root):
    """Purpose: Read every in-scope definition and its optional index.
    Design: Enumerate files even when some fail. Do not skip invalid data.
    Workflow: validate and every query. Data Handoff: Catalog object.
    """
    root = root.resolve()
    paths = []
    for path in root.rglob('definition.yml'):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative.startswith('../') or '/../' in relative:
            continue
        paths.append(path)
    paths.sort(key=lambda item: item.relative_to(root).as_posix())
    validator = component_validator()
    files = []
    diagnostics = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        loaded = LoadedFile(relative, raw)
        try:
            text = raw.decode('utf-8')
            document = load_yaml_text(text)
        except UnicodeError as error:
            loaded.diagnostics.append(diagnostic('YAML_SYNTAX', relative, '', f'file is not valid UTF-8: {error}'))
        except ParseFailure as error:
            loaded.diagnostics.append(diagnostic(error.code, relative, '', error.message))
        else:
            loaded.document = document if isinstance(document, dict) else None
            version = document.get('schema_version') if isinstance(document, dict) else None
            loaded.schema_version = version if isinstance(version, str) else None
            if not isinstance(document, dict):
                loaded.diagnostics.append(diagnostic('SCHEMA_INVALID', relative, '', 'document is not an object'))
            elif isinstance(version, str) and version != SUPPORTED_SCHEMA_VERSION:
                loaded.diagnostics.append(diagnostic('SCHEMA_UNSUPPORTED', relative, '/schema_version', version))
            else:
                schema_errors = sorted(validator.iter_errors(document), key=lambda item: (pointer(item.absolute_path), item.message))
                for item in schema_errors:
                    loaded.diagnostics.append(diagnostic('SCHEMA_INVALID', relative, pointer(item.absolute_path), item.message))
                if not schema_errors:
                    loaded.schema_ok = True
                    for item in semantic_errors(document):
                        loaded.diagnostics.append(diagnostic(item['code'], relative, item['path'], item['message']))
        diagnostics.extend(loaded.diagnostics)
        files.append(loaded)
    seen = {}
    names = {}
    for item in files:
        document = item.document
        if not item.schema_ok or not isinstance(document, dict) or not isinstance(document.get('id'), str):
            continue
        identity = document['id']
        if identity in seen:
            diagnostics.append(diagnostic('ID_COLLISION', item.relative, '/id', identity))
        seen[identity] = item.relative
        for name in [identity, *document.get('aliases', [])]:
            if not isinstance(name, str):
                continue
            folded = name.casefold()
            if folded in names and names[folded] != item.relative:
                diagnostics.append(diagnostic('ALIAS_COLLISION', item.relative, '/aliases', name))
            names[folded] = item.relative
    index_state, index_diagnostics = check_index(root, files)
    diagnostics.extend(index_diagnostics)
    diagnostics.sort(key=lambda item: (item['file'], item['path'], item['code'], item['message']))
    return Catalog(root, files, diagnostics, index_state, catalog_digest(files))
