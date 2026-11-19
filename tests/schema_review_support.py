# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/schema_review_support.py
Purpose: Exercise parsing and semantic rules that JSON Schema cannot express.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Review harness only, not a production package, query CLI, or safety checker.
Related decision: DEV-2026-11-19-004.
"""
import json
import re
import yaml
from yaml.tokens import AliasToken, AnchorToken, TagToken


class ReviewLoader(yaml.SafeLoader):
    """Purpose: Bound review input. Design: Safe YAML and JSON booleans. Workflow: Fixture load. Data Handoff: JSON-compatible data."""


ReviewLoader.yaml_implicit_resolvers = {key: [(tag, regex) for tag, regex in rules if tag != 'tag:yaml.org,2002:bool'] for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()}
ReviewLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$'), list('tf'))


def unique_mapping(loader, node, deep=False):
    """Purpose: Detect lost keys. Design: Reject non-string/duplicate keys. Workflow: Parser constructor. Data Handoff: Mapping or error."""
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError(f'YAML_KEY_TYPE at line {key_node.start_mark.line + 1}')
        if key in result:
            raise ValueError(f'YAML_DUPLICATE_KEY at line {key_node.start_mark.line + 1}: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


ReviewLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_review_yaml(text):
    """Purpose: Test serialization boundaries. Design: No aliases/tags/non-JSON values. Workflow: Review tests. Data Handoff: Data or ValueError."""
    try:
        if any(isinstance(token, (AliasToken, AnchorToken, TagToken)) for token in yaml.scan(text)):
            raise ValueError('YAML_CONSTRUCT_FORBIDDEN: anchors, aliases, and explicit tags are unsupported')
        data = yaml.load(text, Loader=ReviewLoader)
        try:
            json.dumps(data, allow_nan=False)
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError(f'YAML_NON_JSON_VALUE: {error}') from error
        return data
    except yaml.YAMLError as error:
        raise ValueError(f'YAML_SYNTAX: {error}') from error
    except (TypeError, OverflowError, ValueError) as error:
        raise ValueError(str(error)) from error


def pointer(parts):
    """Purpose: Locate diagnostics. Design: JSON Pointer escaping. Workflow: Semantic checks. Data Handoff: Stable location string."""
    return '/' + '/'.join(str(part).replace('~', '~0').replace('/', '~1') for part in parts)


def semantic_errors(documents):
    """Purpose: Review cross-field contracts. Design: Inspect schema-valid documents only. Workflow: Tests. Data Handoff: Sorted code/path records."""
    errors = []
    identities = {}
    names = {}

    def error(code, path, message):
        """Purpose: Collect observations. Design: No exception-as-success. Workflow: Checks. Data Handoff: Diagnostic appended."""
        errors.append({'code': code, 'path': pointer(path), 'message': message})

    for index, document in enumerate(documents):
        identity = document['id']
        if identity in identities:
            error('ID_COLLISION', [index, 'id'], identity)
        identities[identity] = index
        local_names = set()
        for name in [identity, *document['aliases']]:
            folded = name.casefold()
            if folded in local_names or (folded in names and names[folded] != index):
                error('ALIAS_COLLISION', [index, 'aliases'], name)
            local_names.add(folded)
            names[folded] = index
        variants = {f'variant:{key}': value for key, value in document.get('variants', {}).items()}
        variants.update({f'profile:{key}': value for key, value in document.get('profiles', {}).items()})

        def check_cycles(nodes, targets, code, base_path):
            """Purpose: Detect impossible inheritance/dependencies. Design: DFS coloring. Workflow: One document. Data Handoff: Diagnostics."""
            active = set()
            done = set()
            def visit(key):
                """Purpose: Walk dependency chains. Design: Track active nodes. Workflow: Cycle check. Data Handoff: Diagnostics/state."""
                if key in active:
                    error(code, base_path + [key], key)
                    return
                if key in done:
                    return
                active.add(key)
                for target in targets(nodes[key]):
                    if target in nodes:
                        visit(target)
                active.remove(key)
                done.add(key)
            for key in nodes:
                visit(key)

        check_cycles(variants, lambda item: [item['inherits']] if 'inherits' in item else [], 'INHERITANCE_CYCLE', [index, 'variants'])
        check_cycles(document.get('power_domains', {}), lambda item: item.get('input_dependencies', []), 'POWER_CYCLE', [index, 'power_domains'])

        def context(member=None):
            """Purpose: Resolve member scope. Design: Root plus ancestor overrides. Workflow: Semantic walk. Data Handoff: Entity maps."""
            tables = {'pin': dict(document['pins']), 'connector': document['connectors'], 'interface': dict(document['interfaces']), 'processor': document.get('board', {}).get('processors', {}), 'component': document.get('onboard_components', {}), 'feature': document.get('features', {}), 'power_domain': document.get('power_domains', {})}
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
            """Purpose: Reject dangling names. Design: Typed local tables. Workflow: Each reference. Data Handoff: Diagnostics."""
            if key not in tables.get(namespace, {}):
                error('REF_NOT_FOUND', path, f'{namespace}:{key}')

        def walk(node, path, tables):
            """Purpose: Check semantic references. Design: Explicit reference fields. Workflow: Nested entities. Data Handoff: Diagnostics."""
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
                values = {json.dumps(claim['value'], sort_keys=True) for claim in node['claims']}
                if len(values) < 2:
                    error('CONFLICT_NOT_DISTINCT', path + ['claims'], 'conflict needs distinct values')
            for key, value in node.items():
                location = path + [key]
                if key in ('facts', 'sources', 'records', 'pins', 'connectors', 'interfaces', 'onboard_components', 'processors', 'features', 'connections', 'resource_conflicts', 'power_domains', 'constraints'):
                    # Map entry names are user-defined identities, not reference
                    # field names. Inspect each typed value without reinterpreting
                    # a fact/source called "processor" or "connector".
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
                        namespace, target = reference.split(':', 1)
                        resolve(namespace, target, location + [offset], tables)
                elif key in ('affected_pins', 'pin_refs', 'connector_refs', 'input_dependencies'):
                    namespace = {'affected_pins': 'pin', 'pin_refs': 'pin', 'connector_refs': 'connector', 'input_dependencies': 'power_domain'}[key]
                    for offset, target in enumerate(value):
                        resolve(namespace, target, location + [offset], tables)
                elif key in ('processor', 'connector', 'shared_with'):
                    resolve({'processor': 'processor', 'connector': 'connector', 'shared_with': 'pin'}[key], value, location, tables)
                elif key == 'signals':
                    for role, targets in value.items():
                        for target in targets if isinstance(targets, list) else [targets]:
                            resolve('pin', target, location + [role], tables)
                    continue
                elif key == 'inherits' and value not in variants:
                    error('REF_NOT_FOUND', location, value)
                if key in ('variants', 'profiles'):
                    for member, details in value.items():
                        walk(details, location + [member], context(f'{"variant" if key == "variants" else "profile"}:{member}'))
                else:
                    walk(value, location, tables)

        def positions(tables, path):
            """Purpose: Check connector coordinates. Design: Connector-scoped uniqueness. Workflow: Root/member scopes. Data Handoff: Diagnostics."""
            occupied = {}
            for key, pin in tables['pin'].items():
                if 'location' not in pin:
                    continue
                location = pin['location']
                position = location['position']
                numeric = isinstance(position, (int, float)) and not isinstance(position, bool)
                normalized = str(int(position)) if numeric or str(position).isdigit() else str(position)
                coordinate = (location['connector'], normalized)
                if coordinate in occupied:
                    error('POSITION_COLLISION', path + ['pins', key, 'location'], str(coordinate))
                occupied[coordinate] = key
                connector = tables['connector'].get(location['connector'], {})
                if normalized.isdigit() and 'positions' in connector and not 1 <= int(normalized) <= connector['positions']:
                    error('POSITION_OUT_OF_RANGE', path + ['pins', key, 'location', 'position'], normalized)
            check_cycles(tables['pin'], lambda item: [item['shared_with']] if 'shared_with' in item else [], 'SHARED_PIN_CYCLE', path + ['pins'])

        tables = context()
        walk(document, [index], tables)
        positions(tables, [index])
        for member in variants:
            positions(context(member), [index, member])
        status = document['verification']['status']
        if status != 'not_verified':
            kind = 'bench_test' if status == 'bench_tested' else 'document_review'
            if not any(record['kind'] == kind and record['result'] == 'pass' for record in document['verification']['records'].values()):
                error('VERIFICATION_EVIDENCE_MISSING', [index, 'verification'], kind)
    return sorted(errors, key=lambda item: (item['path'], item['code'], item['message']))


def registry_errors(registry):
    """Purpose: Review proposed registry identities. Design: Case-folded collisions. Workflow: Tests. Data Handoff: Code/path diagnostics."""
    errors = []
    identities = set()
    names = {}
    for index, entry in enumerate(registry['entries']):
        if entry['id'] in identities:
            errors.append({'code': 'ID_COLLISION', 'path': pointer(['entries', index, 'id']), 'message': entry['id']})
        identities.add(entry['id'])
        local = set()
        for alias in [entry['id'], *entry['legacy_aliases']]:
            name = alias.casefold()
            if name in local or (name in names and names[name] != index):
                errors.append({'code': 'ALIAS_COLLISION', 'path': pointer(['entries', index, 'legacy_aliases']), 'message': alias})
            names[name] = index
            local.add(name)
    return sorted(errors, key=lambda item: (item['path'], item['code']))
