# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/query.py
Purpose: Project catalog documents into the frozen list, show, pin, and export results.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Read-only except export, which writes only an explicit path outside the catalog.
No connection is reported as safe. Uncertainty is copied, not resolved.
Related decision: DEV-2026-11-19-006.
"""

from pathlib import Path
import hashlib
import json
import yaml

from ysl_components.loader import diagnostic


KINDS = {'board', 'ic_family', 'module'}
CATEGORIES = {'controllers', 'drivers', 'sensors', 'actuators', 'interfaces', 'power', 'connectors'}
FACT_STATUSES = {'documented', 'derived', 'legacy_uncited', 'unknown', 'conflicting'}
UNCERTAIN = {'unknown', 'conflicting', 'legacy_uncited'}


class QueryFailure(Exception):
    """Purpose: Return a classified query miss. Design: Exit code plus one diagnostic.
    Workflow: Resolution. Data Handoff: CLI envelope result.
    """

    def __init__(self, exit_code, code, message, result):
        super().__init__(message)
        self.exit_code = exit_code
        self.code = code
        self.message = message
        self.result = result


def selection_block(component=None, variant=None, profile=None, resolved_by=None):
    """Purpose: Fill the envelope selection. Design: Nulls stay explicit.
    Workflow: Every response. Data Handoff: Selection object.
    """
    return {'component': component, 'profile': profile, 'resolved_by': resolved_by, 'variant': variant}


def member_key(variant, profile):
    """Purpose: Name the requested member. Design: The caller already rejected both flags.
    Workflow: show, pin, pins, and interface. Data Handoff: variant: or profile: key, or None.
    """
    if variant:
        return f'variant:{variant}', 'variant'
    if profile:
        return f'profile:{profile}', 'profile'
    return None, None


def members(document):
    """Purpose: Index variants and profiles. Design: Prefixed keys match inheritance references.
    Workflow: Scope overlay. Data Handoff: Member map.
    """
    found = {f'variant:{key}': value for key, value in document.get('variants', {}).items()}
    found.update({f'profile:{key}': value for key, value in document.get('profiles', {}).items()})
    return found


def overlay(document, variant, profile):
    """Purpose: Apply explicit member overrides. Design: Complete entity replacement along inherits.
    Workflow: Pin and interface scope. Data Handoff: Pins, interfaces, and the member's own facts.
    """
    key, kind = member_key(variant, profile)
    pins = dict(document['pins'])
    interfaces = dict(document['interfaces'])
    if key is None:
        return pins, interfaces, None, None
    table = members(document)
    if key not in table:
        code = 'VARIANT_NOT_FOUND' if kind == 'variant' else 'PROFILE_NOT_FOUND'
        raise QueryFailure(3, code, key, {'code': code, 'query': variant or profile, 'status': 'not_found'})
    chain = []
    visited = set()
    current = key
    while current in table and current not in visited:
        visited.add(current)
        chain.append(table[current])
        current = table[current].get('inherits')
    for item in reversed(chain):
        pins.update(item.get('pins', {}))
        interfaces.update(item.get('interfaces', {}))
    return pins, interfaces, table[key].get('facts', {}), key


def resolve_component(catalog, selector):
    """Purpose: Find one component by id or alias. Design: casefold, without choosing among collisions.
    Workflow: show, pin, pins, interface, and export. Data Handoff: Loaded file and resolved_by, or a failure.
    """
    folded = selector.casefold()
    matches = []
    for item in catalog.files:
        document = item.document
        if not item.schema_ok or document is None:
            continue
        names = [document['id'], *document.get('aliases', [])]
        if any(isinstance(name, str) and name.casefold() == folded for name in names):
            how = 'id' if document['id'].casefold() == folded else 'alias'
            matches.append((item, how))
    if not matches:
        raise QueryFailure(3, 'COMPONENT_NOT_FOUND', selector, {'code': 'COMPONENT_NOT_FOUND', 'query': selector, 'status': 'not_found'})
    if len(matches) > 1:
        raise QueryFailure(2, 'ALIAS_COLLISION', selector, {
            'code': 'ALIAS_COLLISION',
            'diagnostic_count': len(matches),
            'status': 'invalid',
        })
    return matches[0]


def resolve_pin(pins, selector):
    """Purpose: Find one pin. Design: Exact key wins; exact aliases must be unique.
    Workflow: pin operation. Data Handoff: Pin key and resolved_by, or a failure.
    """
    if selector in pins:
        return selector, 'key'
    matches = sorted(key for key, pin in pins.items() if selector in pin.get('aliases', []))
    if len(matches) == 1:
        return matches[0], 'alias'
    if len(matches) > 1:
        raise QueryFailure(4, 'AMBIGUOUS_PIN', selector, {'candidates': matches, 'code': 'AMBIGUOUS_PIN', 'status': 'ambiguous'})
    raise QueryFailure(3, 'PIN_NOT_FOUND', selector, {'code': 'PIN_NOT_FOUND', 'query': selector, 'status': 'not_found'})


def summary(document):
    """Purpose: Describe one component in a list. Design: Identity and verification only.
    Workflow: list and search. Data Handoff: Summary object.
    """
    return {
        'aliases': list(document.get('aliases', [])),
        'category': document['category'],
        'id': document['id'],
        'kind': document['kind'],
        'manufacturer': document['manufacturer'],
        'name': document['name'],
        'verification_status': document['verification']['status'],
    }


def manufacturer_matches(document, wanted):
    """Purpose: Apply the manufacturer filter. Design: Exact casefold, with unknown as a status.
    Workflow: list and search. Data Handoff: Boolean.
    """
    manufacturer = document.get('manufacturer', {})
    if wanted.casefold() == 'unknown':
        return manufacturer.get('status') == 'unknown'
    return manufacturer.get('status') == 'known' and manufacturer.get('name', '').casefold() == wanted.casefold()


def fact_statuses(node):
    """Purpose: Collect fact states for search. Design: Only values inside a facts map.
    Workflow: --fact-status. Data Handoff: Set of status strings.
    """
    found = set()
    if isinstance(node, dict):
        facts = node.get('facts')
        if isinstance(facts, dict):
            for fact in facts.values():
                if isinstance(fact, dict) and isinstance(fact.get('status'), str):
                    found.add(fact['status'])
        for key, value in node.items():
            if key != 'facts':
                found.update(fact_statuses(value))
    elif isinstance(node, list):
        for value in node:
            found.update(fact_statuses(value))
    return found


def matches_filters(document, kind, category, manufacturer, text, capability, interface_type, fact_status):
    """Purpose: AND the frozen filters. Design: Capability and interface type use the base document.
    Workflow: list and search. Data Handoff: Boolean.
    """
    if kind and document.get('kind') != kind:
        return False
    if category and document.get('category') != category:
        return False
    if manufacturer and not manufacturer_matches(document, manufacturer):
        return False
    if text:
        folded = text.casefold()
        haystack = [document.get('id', ''), document.get('name', ''), *document.get('aliases', [])]
        if not any(isinstance(value, str) and folded in value.casefold() for value in haystack):
            return False
    if capability:
        pins = document.get('pins', {})
        if not any(capability in pin.get('capabilities', []) for pin in pins.values() if isinstance(pin, dict)):
            return False
    if interface_type:
        interfaces = document.get('interfaces', {})
        if not any(interface.get('type') == interface_type for interface in interfaces.values() if isinstance(interface, dict)):
            return False
    if fact_status and fact_status not in fact_statuses(document):
        return False
    return True


def list_components(catalog, **filters):
    """Purpose: List matching components. Design: Empty input is success.
    Workflow: list and search. Data Handoff: Result object.
    """
    documents = [item.document for item in catalog.files if item.schema_ok]
    chosen = [summary(document) for document in documents if matches_filters(document, **filters)]
    chosen.sort(key=lambda item: item['id'])
    return {'components': chosen, 'status': 'ok'}


def pin_summary(key, pin):
    """Purpose: Show a pin mapping without its full fact payload.
    Design: Preserve absent fields as null. Workflow: show and pins. Data Handoff: Summary object.
    """
    location = pin.get('location') if isinstance(pin.get('location'), dict) else None
    return {
        'aliases': list(pin.get('aliases', [])),
        'capabilities': list(pin.get('capabilities', [])),
        'connector': None if location is None else location.get('connector'),
        'direction': pin.get('direction'),
        'maps_to': pin.get('maps_to'),
        'pin': key,
        'position': None if location is None else location.get('position'),
    }


def uncertainty(document):
    """Purpose: Keep unknown, conflicting, and uncited facts visible.
    Design: Conflicting and unknown facts do not receive a selected value.
    Workflow: show. Data Handoff: Uncertainty object.
    """
    facts = []

    def walk(node, prefix):
        """Purpose: Visit facts maps. Design: Skip the facts node after recording its entries.
        Workflow: Uncertainty collection. Data Handoff: Appends fact records.
        """
        if isinstance(node, dict):
            entries = node.get('facts')
            if isinstance(entries, dict):
                for key, fact in entries.items():
                    if not isinstance(fact, dict) or fact.get('status') not in UNCERTAIN:
                        continue
                    path = f'{prefix}.facts.{key}' if prefix else f'facts.{key}'
                    record = {'path': path, 'status': fact['status']}
                    if fact['status'] == 'conflicting':
                        record['claims'] = fact.get('claims', [])
                        record['selected_value'] = None
                    elif fact['status'] == 'unknown':
                        record['selected_value'] = None
                        if 'explanation' in fact:
                            record['explanation'] = fact['explanation']
                        if 'notes' in fact:
                            record['notes'] = fact['notes']
                    else:
                        if 'source_refs' in fact:
                            record['source_refs'] = fact['source_refs']
                        if 'value' in fact:
                            record['value'] = fact['value']
                    facts.append(record)
            for key, value in node.items():
                if key == 'facts':
                    continue
                next_prefix = f'{prefix}.{key}' if prefix else str(key)
                if isinstance(value, dict):
                    walk(value, next_prefix)
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, dict):
                            walk(item, f'{next_prefix}.{index}')
        elif isinstance(node, list):
            for index, item in enumerate(node):
                if isinstance(item, dict):
                    walk(item, f'{prefix}.{index}' if prefix else str(index))

    walk(document, '')
    facts.sort(key=lambda item: item['path'])
    connections = []
    for key, connection in document.get('connections', {}).items():
        if isinstance(connection, dict) and connection.get('routing_status') in {'conflicting', 'unknown'}:
            connections.append({
                'id': key,
                'notes': connection.get('notes'),
                'routing_status': connection['routing_status'],
            })
    connections.sort(key=lambda item: item['id'])
    return {
        'connections': connections,
        'facts': facts,
        'verification_status': document['verification']['status'],
    }


def show_component(catalog, selector, variant=None, profile=None):
    """Purpose: Return one component projection. Design: Stored constraints stay intact.
    Workflow: show. Data Handoff: Result and selection.
    """
    item, how = resolve_component(catalog, selector)
    document = item.document
    pins, _interfaces, facts, _key = overlay(document, variant, profile)
    result = {
        'aliases': list(document.get('aliases', [])),
        'category': document['category'],
        'connector_ids': sorted(document.get('connectors', {})),
        'constraints': document.get('constraints', {}),
        'id': document['id'],
        'interface_ids': sorted(document.get('interfaces', {})),
        'kind': document['kind'],
        'manufacturer': document['manufacturer'],
        'name': document['name'],
        'pin_count': len(pins),
        'pins': [pin_summary(key, pin) for key, pin in sorted(pins.items())],
        'profile_selectors': sorted(document.get('profiles', {})),
        'provenance_status': document['provenance']['status'],
        'resource_conflicts': document.get('resource_conflicts', {}),
        'schema_version': document['schema_version'],
        'selected_facts': facts,
        'selected_profile': profile,
        'selected_variant': variant,
        'source_ids': sorted(document.get('sources', {})),
        'status': 'ok',
        'uncertainty': uncertainty(document),
        'variant_selectors': sorted(document.get('variants', {})),
        'verification_status': document['verification']['status'],
    }
    return result, selection_block(document['id'], variant, profile, how)


def contains_token(node, tokens):
    """Purpose: See whether a record mentions a pin or interface.
    Design: Compare stored strings only. Workflow: Related constraints. Data Handoff: Boolean.
    """
    if isinstance(node, str):
        return node in tokens
    if isinstance(node, list):
        return any(contains_token(value, tokens) for value in node)
    if isinstance(node, dict):
        return any(contains_token(value, tokens) for value in node.values())
    return False


def related_records(document, tokens):
    """Purpose: Attach constraints that mention the requested pin or interface.
    Design: Summaries do not add a safety conclusion. Workflow: pin and interface.
    Data Handoff: Sorted records.
    """
    records = []
    for section in ('constraints', 'resource_conflicts'):
        for key, value in document.get(section, {}).items():
            if not isinstance(value, dict) or not contains_token(value, tokens):
                continue
            targets = value.get('targets', value.get('participants', []))
            records.append({
                'affected_pins': list(value.get('affected_pins', [])),
                'id': key,
                'kind': value.get('kind'),
                'notes': value.get('notes'),
                'rule': value.get('rule'),
                'section': section,
                'targets': list(targets) if isinstance(targets, list) else [],
            })
    records.sort(key=lambda item: (item['section'], item['id']))
    return records


def pin_result(catalog, selector, pin_selector, variant=None, profile=None):
    """Purpose: Return one pin. Design: Do not invent a target for an ambiguous alias.
    Workflow: pin. Data Handoff: Result and selection.
    """
    item, how = resolve_component(catalog, selector)
    document = item.document
    pins, _interfaces, _facts, _key = overlay(document, variant, profile)
    key, pin_how = resolve_pin(pins, pin_selector)
    pin = pins[key]
    location = pin.get('location') if isinstance(pin.get('location'), dict) else None
    result = {
        'aliases': list(pin.get('aliases', [])),
        'capabilities': list(pin.get('capabilities', [])),
        'component_id': document['id'],
        'constraints': related_records(document, {key, f'pin:{key}'}),
        'direction': pin.get('direction'),
        'facts': pin.get('facts', {}),
        'location': location,
        'maps_to': pin.get('maps_to'),
        'pin': key,
        'provenance': pin.get('provenance', {}),
        'resolved_by': pin_how,
        'selected_profile': profile,
        'selected_variant': variant,
        'shared_with': pin.get('shared_with'),
        'status': 'ok',
        'verification_status': document['verification']['status'],
    }
    return result, selection_block(document['id'], variant, profile, how)


def pins_result(catalog, selector, connector=None, capability=None, variant=None, profile=None):
    """Purpose: List pins in a selected scope. Design: Optional connector and capability filters.
    Workflow: pins. Data Handoff: Result and selection.
    """
    item, how = resolve_component(catalog, selector)
    document = item.document
    pins, _interfaces, _facts, _key = overlay(document, variant, profile)
    chosen = []
    for key, pin in sorted(pins.items()):
        summary_pin = pin_summary(key, pin)
        if connector and summary_pin['connector'] != connector:
            continue
        if capability and capability not in summary_pin['capabilities']:
            continue
        chosen.append(summary_pin)
    result = {
        'component_id': document['id'],
        'pins': chosen,
        'selected_profile': profile,
        'selected_variant': variant,
        'status': 'ok',
    }
    return result, selection_block(document['id'], variant, profile, how)


def interface_result(catalog, selector, interface_id, variant=None, profile=None):
    """Purpose: Return one interface. Design: Signal values stay pin references.
    Workflow: interface. Data Handoff: Result and selection.
    """
    item, how = resolve_component(catalog, selector)
    document = item.document
    _pins, interfaces, _facts, _key = overlay(document, variant, profile)
    if interface_id not in interfaces:
        raise QueryFailure(3, 'INTERFACE_NOT_FOUND', interface_id, {'code': 'INTERFACE_NOT_FOUND', 'query': interface_id, 'status': 'not_found'})
    interface = interfaces[interface_id]
    result = {
        'component_id': document['id'],
        'constraints': related_records(document, {interface_id, f'interface:{interface_id}'}),
        'facts': interface.get('facts', {}),
        'interface': interface_id,
        'provenance_status': interface.get('provenance', {}).get('status'),
        'selected_profile': profile,
        'selected_variant': variant,
        'signals': interface.get('signals', {}),
        'status': 'ok',
        'type': interface.get('type'),
    }
    return result, selection_block(document['id'], variant, profile, how)


def export_text(document, export_format):
    """Purpose: Serialize a stored component. Design: Canonical JSON or sorted YAML.
    Workflow: export. Data Handoff: UTF-8 text.
    """
    if export_format == 'json':
        return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + '\n'
    text = yaml.safe_dump(document, sort_keys=True, allow_unicode=True)
    if not text.endswith('\n'):
        text += '\n'
    return text


def export_component(catalog, selector, export_format, output, force):
    """Purpose: Write one component outside the catalog. Design: Refuse overwrite and in-catalog paths.
    Workflow: export. Data Handoff: Envelope result. Side effect: one output file when authorized.
    """
    item, how = resolve_component(catalog, selector)
    destination = Path(output)
    if not destination.is_absolute():
        destination = Path.cwd() / destination
    destination = destination.resolve()
    try:
        destination.relative_to(catalog.root)
        inside = True
    except ValueError:
        inside = False
    if inside:
        raise QueryFailure(2, 'OUTPUT_PROTECTED', str(destination), {'code': 'OUTPUT_PROTECTED', 'status': 'invalid'})
    if destination.exists() and destination.is_dir():
        raise QueryFailure(2, 'USAGE', 'output path is a directory', {'code': 'USAGE', 'status': 'invalid_usage'})
    if not destination.parent.is_dir():
        raise QueryFailure(2, 'USAGE', 'output directory does not exist', {'code': 'USAGE', 'status': 'invalid_usage'})
    if destination.exists() and not force:
        raise QueryFailure(2, 'OUTPUT_EXISTS', str(destination), {'code': 'OUTPUT_EXISTS', 'status': 'invalid'})
    text = export_text(item.document, export_format)
    temporary = destination.with_name(destination.name + '.ysl-tmp')
    temporary.write_text(text, encoding='utf-8', newline='\n')
    temporary.replace(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    result = {
        'bytes': destination.stat().st_size,
        'component_id': item.document['id'],
        'format': export_format,
        'output': destination.as_posix(),
        'sha256': digest,
        'status': 'ok',
    }
    return result, selection_block(item.document['id'], resolved_by=how)


def file_inventory(catalog):
    """Purpose: Report every in-scope file. Design: Failures stay visible in the list.
    Workflow: validate. Data Handoff: Validate result.
    """
    files = []
    for item in catalog.files:
        identity = None
        if isinstance(item.document, dict) and isinstance(item.document.get('id'), str):
            identity = item.document['id']
        files.append({
            'diagnostics': len(item.diagnostics),
            'id': identity,
            'path': item.relative,
            'schema_version': item.schema_version,
            'sha256': item.sha256,
        })
    return {
        'diagnostic_count': len(catalog.diagnostics),
        'files': files,
        'index': catalog.index_state,
        'status': 'valid' if catalog.exit_code() == 0 else 'invalid',
    }


def invalid_result(catalog):
    """Purpose: Withhold component entries when the catalog is not valid.
    Design: Count diagnostics without echoing a successful list. Workflow: Queries on bad catalogs.
    Data Handoff: Invalid result.
    """
    return {'diagnostic_count': len(catalog.diagnostics), 'status': 'invalid'}


def query_diagnostic(failure, file_name):
    """Purpose: Place a query miss on stderr. Design: Same shape as loader diagnostics.
    Workflow: Exit 2, 3, or 4 from an operation. Data Handoff: One diagnostic.
    """
    return diagnostic(failure.code, file_name, '', failure.message)
