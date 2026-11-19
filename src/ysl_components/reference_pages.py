# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/reference_pages.py
Purpose: Generate Markdown reference pages directly from hardware YAML.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Source-only documentation utility; no query CLI or packaging entry point.
Related decision: DEV-2026-11-19-003.
"""
from collections import defaultdict
from pathlib import Path
import hashlib
import html
import os
import re
from urllib.parse import quote
import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Purpose: Prevent lost fields. Design: Safe YAML plus unique keys. Workflow: Rendering. Data Handoff: Mappings."""


def unique_mapping(loader, node, deep=False):
    """Purpose: Reject duplicate keys. Design: Inspect source nodes. Workflow: YAML load. Data Handoff: Mapping or ValueError."""
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate key {key!r} at line {key_node.start_mark.line + 1}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def describe(value):
    """Purpose: Explain structured values. Design: Human labels, no raw JSON. Workflow: Table cells. Data Handoff: Plain text."""
    if isinstance(value, dict):
        return '; '.join(f'{key.replace("_", " ")}: {describe(child)}' for key, child in value.items() if key != 'source_refs')
    if isinstance(value, list):
        return ', '.join(describe(child) for child in value)
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    return str(value) if value is not None else 'Not specified'


def cell(value):
    """Purpose: Escape data. Design: No executable markup in cells. Workflow: Tables. Data Handoff: Markdown-safe text."""
    text = html.escape(describe(value), quote=False)
    for old, new in [('|', '&#124;'), ('`', '&#96;'), ('[', '&#91;'), (']', '&#93;'), ('*', '&#42;')]:
        text = text.replace(old, new)
    return text.replace('\n', '<br>')


def slug(heading):
    """Purpose: Link source headings. Design: GFM-style punctuation removal. Workflow: Citations. Data Handoff: Fragment."""
    return re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-')


def local_link(target, page):
    """Purpose: Link relocated files. Design: Relative portable paths. Workflow: Page generation. Data Handoff: URL path."""
    return quote(os.path.relpath(target, page.parent).replace(os.sep, '/'), safe='/._-')


def table(headers, rows):
    """Purpose: Format comparisons. Design: Escape every data cell. Workflow: Render sections. Data Handoff: Markdown lines."""
    result = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |']
    result.extend('| ' + ' | '.join(cell(value) for value in row) + ' |' for row in rows)
    return result + ['']


def citations(board, refs, root, page):
    """Purpose: Attach exact provenance. Design: Local section links. Workflow: Reference tables. Data Handoff: Markdown links."""
    output = []
    for reference in refs:
        record = board.get('source', {}).get('references', {})[reference]
        target = local_link(root / record['path'], page)
        output.append(f'[{cell(record["heading"])}]({target}#{slug(record["heading"])})')
    return '; '.join(output) or 'No section citation'


def sourced_table(headers, records, board, root, page):
    """Purpose: Preserve live citations. Design: Escape data before adding links. Workflow: Sourced rows. Data Handoff: Markdown lines."""
    output = table(headers + ['Sources'], [])[:-1]
    for values, refs in records:
        output.append('| ' + ' | '.join(cell(value) for value in values) + ' | ' + citations(board, refs, root, page) + ' |')
    return output + ['']


def details(title, node, level=3):
    """Purpose: Expose nested hardware facts. Design: Recursive readable lists. Workflow: Supplemental sections. Data Handoff: Lines."""
    output = ['#' * min(level, 6) + ' ' + cell(title), '']
    if isinstance(node, dict):
        children = []
        for key, value in node.items():
            if key == 'source_refs':
                continue
            if isinstance(value, dict):
                children.append((key, value))
            else:
                output.append(f'- **{cell(key)}:** {cell(value)}')
        output.append('')
        for key, value in children:
            output.extend(details(key, value, level + 1))
    else:
        output.extend([cell(node), ''])
    return output


def pin_references(node, pins):
    """Purpose: Summarize interfaces. Design: Match declared pin identities only. Workflow: Interface table. Data Handoff: Sorted IDs."""
    found = set()
    if isinstance(node, str) and node in pins:
        found.add(node)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key not in ('source_refs', 'note', 'type', 'processor'):
                found.update(pin_references(value, pins))
    elif isinstance(node, list):
        for value in node:
            found.update(pin_references(value, pins))
    return sorted(found)


def render_component(root, definition, identity, board):
    """Purpose: Build one reference. Design: YAML is authoritative. Workflow: build_pages. Data Handoff: Deterministic Markdown."""
    page = definition.parent / 'README.md'
    digest = hashlib.sha256(definition.read_bytes()).hexdigest()
    title = board.get('model') or board.get('family', '').replace('_', '/') or identity.replace('_', ' ').title()
    output = [f'<!-- Generated from definition.yml; SHA-256: {digest}. Do not edit manually. -->',
              f'# {cell(title)}', '',
              f'[Catalog]({local_link(root / "docs/catalog.md", page)}) · [Hardware YAML](definition.yml)', '',
              'This page is generated from the hardware definition. Source statements and static checks do not establish bench verification.', '',
              '## Identity and capabilities', '']
    summary = [('Legacy definition key', identity), ('Manufacturer', board.get('manufacturer', 'Not specified')), ('Device type', board.get('device_type', 'Controller board or family'))]
    for key in ('mcu', 'mpu', 'architecture', 'logic_voltage', 'clock_hz', 'package'):
        if key in board:
            summary.append((key, board[key]))
    pins = {}
    for section in ('pin_map', 'power_pins', 'special_pins'):
        for key, record in board.get(section, {}).items():
            if key in pins:
                raise ValueError(f'Duplicate pin identity across sections: {key}')
            pins[key] = record
    summary += [('Named pin records', len(pins)), ('Interfaces', len(board.get('interfaces', {})))]
    output += table(['Property', 'Value'], summary)
    capabilities = sorted({value for pin in pins.values() for value in pin.get('capabilities', [])})
    output += ['**Declared capabilities:** ' + ', '.join(cell(value) for value in capabilities), '']
    for section in ('variants', 'profiles', 'processors', 'memory'):
        if section in board:
            output += ['## ' + section.title(), '']
            records = [([key, value], value.get('source_refs', [])) for key, value in board[section].items()]
            output += sourced_table(['Name', 'Documented properties'], records, board, root, page)
    if 'onboard_components' in board:
        output += ['## Onboard component inventory', '']
        records = [([key, item.get('part_number', 'Part number unspecified'), item['role']], item['source_refs']) for key, item in board['onboard_components'].items()]
        output += sourced_table(['ID', 'Part', 'Board role'], records, board, root, page)
    if 'connections' in board:
        output += ['## Connection relationships', '', 'References use the typed namespaces documented in the YAML source record. A documented connection does not assert undisclosed internal routing.', '']
        records = [([key, edge['from'], edge['to'], edge['relationship'], ', '.join(edge.get('via', [])), edge.get('routing_status', '')], edge['source_refs']) for key, edge in board['connections'].items()]
        output += sourced_table(['ID', 'From', 'To', 'Relationship', 'Via', 'Routing status'], records, board, root, page)
    if 'resource_conflicts' in board:
        output += ['## Resource conflicts', '']
        records = [([key, ', '.join(item.get('affected_pins', [])), ', '.join(item.get('participants', [])), item['policy'], item.get('scope', item.get('note', ''))], item['source_refs']) for key, item in board['resource_conflicts'].items()]
        output += sourced_table(['Conflict ID', 'Pins', 'Participants', 'Policy', 'Scope'], records, board, root, page)
    output += ['## Power and electrical summary', '']
    voltage = board.get('voltage', board.get('electrical', {}))
    records = [([key, value], value.get('source_refs', []) if isinstance(value, dict) else []) for key, value in voltage.items()]
    output += sourced_table(['Domain or property', 'Documented values'], records, board, root, page)
    if 'power_distribution' in board:
        output += ['### Distribution and input dependencies', '']
        output += ['Carrier outputs outside the limited nets do not have unlimited current. The manual leaves the independent-versus-combined scope of the 2.8 A rail limit unresolved.', '']
        records = []
        for key, item in board['power_distribution'].items():
            if key == 'source_refs':
                continue
            refs = item.get('source_refs', []) if isinstance(item, dict) else board['power_distribution'].get('source_refs', [])
            values = {field: value for field, value in item.items() if field != 'source_refs'} if isinstance(item, dict) else item
            records.append(([key, values], refs))
        output += sourced_table(['Group or rule', 'Documented relationships and limits'], records, board, root, page)
    output += ['## Interfaces', '']
    records = []
    for key, interface in board.get('interfaces', {}).items():
        records.append(([key, interface.get('type', 'Not specified'), interface.get('processor', 'Not specified'), ', '.join(pin_references(interface, pins)), interface.get('note', '')], interface.get('source_refs', [])))
    output += sourced_table(['Interface', 'Type', 'Processor', 'Pins', 'Notes'], records, board, root, page)
    if 'connectors' in board:
        output += ['## Connector summary', '']
        records = []
        for key, connector in board['connectors'].items():
            info = {field: value for field, value in connector.items() if field != 'source_refs'}
            records.append(([key, info], connector.get('source_refs', [])))
        output += sourced_table(['Connector', 'Specification'], records, board, root, page)
    output += ['## Pin tables', '']
    groups = defaultdict(list)
    for key, record in pins.items():
        groups[record.get('connector', 'Other pins')].append((key, record))
    for group in sorted(groups):
        output += ['### ' + cell(group), '']
        records = [([key, record.get('physical_pin', 'Not specified'), record.get('maps_to', 'Not specified'), record.get('source_function', record.get('mcu_pin', '')), ', '.join(record.get('capabilities', [])), ', '.join(record.get('aliases', [])), record.get('note', '')], record.get('source_refs', [])) for key, record in groups[group]]
        output += sourced_table(['Pin ID', 'Position', 'Signal', 'Function or MCU port', 'Capabilities', 'Aliases', 'Notes'], records, board, root, page)
    for section in ('constraints', 'physical', 'onboard', 'wireless', 'ranging', 'logic'):
        if section in board:
            output += ['## ' + section.title(), '']
            for key, value in board[section].items():
                if key != 'source_refs':
                    output += details(key, value)
    source = board.get('source', {})
    output += ['## Known issues and source coverage', '']
    if source.get('discrepancies'):
        records = [([item['topic'], item['claims'], item['disposition']], item.get('source_refs', [])) for item in source['discrepancies']]
        output += sourced_table(['Issue', 'Conflicting source claims', 'Disposition'], records, board, root, page)
    else:
        output += ['No structured source-discrepancy inventory is recorded for this definition. This is not a claim that no discrepancies exist.', '']
    for gap in source.get('coverage_gaps', []):
        output.append('- ' + cell(gap))
    if 'coverage_gaps' in source:
        output.append('')
    output += ['## Sources', '']
    if 'path' in source:
        output += [f'[Local manual]({local_link(root / source["path"], page)}) — snapshot {cell(source.get("snapshot_pulled_date", "not specified"))}.', '']
    if source.get('url'):
        output += [f'[Source document]({source["url"]})', '']
    if source.get('references'):
        for key, record in source['references'].items():
            output.append(f'- {cell(key)}: {citations(board, [key], root, page)}; snapshot {cell(record["snapshot_pulled_date"])}.')
        output += ['', 'The copied manual retains its original site-relative links and missing local image references. See [source limitations](sources/README.md).', '']
    elif not source:
        output += ['Source citations remain incomplete in this legacy definition. Check comments in the YAML for any document identifiers; no new source facts were inferred by this generator.', '']
    return '\n'.join(output).rstrip() + '\n'


def build_pages(root):
    """Purpose: Render the catalog. Design: Pure in-memory outputs. Workflow: Generator/tests. Data Handoff: Path-to-Markdown mapping."""
    root = Path(root).resolve()
    outputs = {}
    catalog = ['<!-- Generated from hardware/**/definition.yml. Do not edit manually. -->', '# Hardware catalog', '',
               '[Repository overview](../README.md) · [Implementation plan](planning/CLI_IMPLEMENTATION_PLAN.md)', '',
               'Browse reference pages by category and namespace. The catalog uses the user-approved schema and stable IDs. CLI queries and packaging remain separate gated work.', '']
    rows = []
    for definition in sorted((root / 'hardware').rglob('definition.yml')):
        document = yaml.load(definition.read_text(encoding='utf-8-sig'), Loader=UniqueKeyLoader)
        if isinstance(document, dict) and 'schema_version' in document:
            board = document
            identity = board['id']
            page = definition.parent / 'README.md'
            outputs[page.relative_to(root).as_posix()] = render_normalized(root, definition, board)
            parts = definition.relative_to(root / 'hardware').parts
            reference = f'[{cell(board["name"])}]({local_link(page, root / "docs/catalog.md")})'
            issues = sum(item['kind'] == 'source_conflict' for item in board.get('constraints', {}).values())
            rows.append('| ' + ' | '.join([cell(parts[0]), cell(parts[1]), reference, f'[YAML]({local_link(definition, root / "docs/catalog.md")})', str(issues)]) + ' |')
            continue
        if not isinstance(document, dict) or len(document) != 1:
            raise ValueError(f'Expected one hardware root: {definition}')
        identity, board = next(iter(document.items()))
        relative = definition.relative_to(root).as_posix()
        page = definition.parent / 'README.md'
        outputs[page.relative_to(root).as_posix()] = render_component(root, definition, identity, board)
        parts = definition.relative_to(root / 'hardware').parts
        name = board.get('model') or board.get('family', '').replace('_', '/') or identity.replace('_', ' ').title()
        reference = f'[{cell(name)}]({local_link(page, root / "docs/catalog.md")})'
        rows.append('| ' + ' | '.join([cell(parts[0]), cell(parts[1]), reference, f'[YAML]({local_link(definition, root / "docs/catalog.md")})', str(len(board.get('source', {}).get('discrepancies', [])))]) + ' |')
    catalog += table(['Category', 'Namespace', 'Reference page', 'Definition', 'Recorded source issues'], [])[:-1] + rows + ['']
    catalog += ['## Migration status', '', 'The user approved the schema/ID candidate and authorized P2 migration. All five definitions now use that contract. [Migration evidence](evidence/migration-2026-11-19/README.md) preserves original bytes and a complete source-field map. G2 review, query CLI implementation, and G4 packaging approval remain separate; packaging is disabled.', '']
    outputs['docs/catalog.md'] = '\n'.join(catalog).rstrip() + '\n'
    return outputs


def normalized_citations(board, refs, root, page):
    """Purpose: Link normalized evidence. Design: Source IDs resolve locally. Workflow: Migrated pages. Data Handoff: Source links."""
    output = []
    for key in refs:
        record = board['sources'][key]
        target = local_link(root / record['path'], page) if 'path' in record else record.get('url')
        if target and 'section' in record:
            target += '#' + slug(record['section'])
        output.append(f'[{cell(record["title"])}]({target})' if target else cell(record['title']))
    return '; '.join(output) or 'No source citation'


def normalized_table(headers, records, board, root, page):
    """Purpose: Render approved data shapes. Design: Escape cells, preserve source links. Workflow: Migrated sections. Data Handoff: Markdown lines."""
    output = table(headers + ['Sources'], [])[:-1]
    for values, refs in records:
        output.append('| ' + ' | '.join(cell(value) for value in values) + ' | ' + normalized_citations(board, refs, root, page) + ' |')
    return output + ['']


def normalized_facts(facts, board, root, page):
    """Purpose: Expose typed facts and uncertainty. Design: Never select a conflicting claim. Workflow: Entity sections. Data Handoff: Tables."""
    records = []
    for key, fact in facts.items():
        value = fact.get('value', fact.get('notes', 'Unknown'))
        refs = list(fact.get('source_refs', []))
        if fact['status'] == 'conflicting':
            value = 'Conflicting claims: ' + '; '.join(describe(claim['value']) for claim in fact['claims'])
            refs = sorted({source for claim in fact['claims'] for source in claim['source_refs']})
        records.append(([key, fact['status'], value], refs))
    return normalized_table(['Fact', 'Evidence state', 'Value / documented limits'], records, board, root, page)


def render_normalized(root, definition, board):
    """Purpose: Keep browsing usable after migration. Design: Render canonical fields directly. Workflow: build_pages. Data Handoff: Deterministic Markdown."""
    page = definition.parent / 'README.md'
    digest = hashlib.sha256(definition.read_bytes()).hexdigest()
    output = [f'<!-- Generated from definition.yml; SHA-256: {digest}. Do not edit manually. -->',
              '# ' + cell(board['name']), '', f'[Catalog]({local_link(root / "docs/catalog.md", page)}) · [Hardware YAML](definition.yml)', '',
              'This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.', '',
              '## Identity and capabilities', '']
    output += table(['Property', 'Value'], [('ID', board['id']), ('Schema version', board['schema_version']), ('Kind', board['kind']), ('Manufacturer', board['manufacturer'].get('name', 'Unknown: ' + board['manufacturer'].get('reason', 'Not specified'))), ('Legacy aliases', board['aliases']), ('Named pin records', len(board['pins'])), ('Interfaces', len(board['interfaces'])), ('Verification', board['verification']['status'])])
    output += ['## Component facts', ''] + normalized_facts(board['facts'], board, root, page)
    if 'board' in board:
        output += ['## Processors', '']
        for key, part in board['board']['processors'].items():
            output += ['### ' + cell(key), '', '**Model:** ' + cell(part.get('model', 'Not specified')), '']
            output += normalized_facts(part['facts'], board, root, page)
    for section in ('variants', 'profiles'):
        if section in board:
            output += ['## ' + section.title(), '']
            for key, member in board[section].items():
                output += ['### ' + cell(key), '', '**Inherits:** ' + cell(member.get('inherits', 'Base component')), '']
                output += normalized_facts(member['facts'], board, root, page)
    if 'onboard_components' in board:
        output += ['## Onboard component inventory', '']
        records = [([key, item.get('model', 'Part number unspecified'), item['role']], item['provenance'].get('source_refs', [])) for key, item in board['onboard_components'].items()]
        output += normalized_table(['ID', 'Part', 'Role'], records, board, root, page)
        for key, item in board['onboard_components'].items():
            if item['facts']:
                output += ['### ' + cell(key), ''] + normalized_facts(item['facts'], board, root, page)
    if 'connections' in board:
        output += ['## Connection relationships', '']
        records = [([key, item['from'], item['to'], item['relationship'], item.get('via', []), item['routing_status'], item.get('notes', '')], item['provenance'].get('source_refs', [])) for key, item in board['connections'].items()]
        output += normalized_table(['ID', 'From', 'To', 'Relationship', 'Via', 'Routing state', 'Notes'], records, board, root, page)
    if 'resource_conflicts' in board:
        output += ['## Resource conflicts', '']
        records = [([key, item.get('affected_pins', []), item.get('participants', []), item['policy'], item.get('when', {}), item['notes']], item['provenance'].get('source_refs', [])) for key, item in board['resource_conflicts'].items()]
        output += normalized_table(['ID', 'Pins', 'Participants', 'Policy', 'Condition', 'Source rule'], records, board, root, page)
    output += ['## Power and electrical summary', '']
    for key, domain in board.get('power_domains', {}).items():
        output += ['### ' + cell(key), '', '**Role:** ' + cell(domain['role']) + '; **Limit scope:** ' + cell(domain.get('limit_scope', 'Not independently classified')), '']
        if 'feeds' in domain:
            output += ['**Feeds:** ' + cell(domain['feeds']), '']
        if 'input_dependencies' in domain:
            output += ['**Possible input dependencies:** ' + cell(domain['input_dependencies']), '']
        output += normalized_facts(domain['facts'], board, root, page)
    output += ['## Interfaces', '']
    records = [([key, item['type'], item.get('processor', 'Not specified'), item['signals']], item['provenance'].get('source_refs', [])) for key, item in board['interfaces'].items()]
    output += normalized_table(['ID', 'Type', 'Processor', 'Signal roles / pins'], records, board, root, page)
    for key, item in board['interfaces'].items():
        if item['facts']:
            output += ['### ' + cell(key), ''] + normalized_facts(item['facts'], board, root, page)
    output += ['## Connector summary', '']
    records = [([key, item['type'], item.get('positions', 'Not specified'), item.get('processor', 'Not specified')], item['provenance'].get('source_refs', [])) for key, item in board['connectors'].items()]
    output += normalized_table(['ID', 'Type', 'Positions', 'Processor'], records, board, root, page)
    for key, item in board['connectors'].items():
        if item['facts']:
            output += ['### ' + cell(key), ''] + normalized_facts(item['facts'], board, root, page)
    output += ['## Pin tables', '']
    groups = defaultdict(list)
    for key, pin in board['pins'].items():
        groups[pin.get('location', {}).get('connector', pin['facts'].get('connector', {}).get('value', 'Unnumbered or logical board connections'))].append((key, pin))
    for connector, items in sorted(groups.items()):
        output += ['### ' + cell(connector), '']
        records = [([key, pin.get('location', {}).get('position', 'Not specified'), pin.get('maps_to', 'Not specified'), pin['facts'].get('source_function', {}).get('value', ''), pin.get('capabilities', []), pin.get('aliases', []), pin.get('shared_with', '')], pin['provenance'].get('source_refs', [])) for key, pin in items]
        output += normalized_table(['Pin', 'Position', 'Signal', 'Source function', 'Capabilities', 'Aliases', 'Shared with'], records, board, root, page)
        for key, pin in items:
            if pin['facts']:
                output += ['#### ' + cell(key), ''] + normalized_facts(pin['facts'], board, root, page)
    output += ['## Constraints and known issues', '']
    for key, item in board.get('constraints', {}).items():
        output += ['### ' + cell(key), '', '**' + cell(item['kind']) + ':** ' + cell(item['rule']), '']
        output += normalized_facts(item['facts'], board, root, page)
    if 'features' in board:
        output += ['## Onboard and wireless features', '']
        for key, item in board['features'].items():
            output += ['### ' + cell(key), ''] + normalized_facts(item['facts'], board, root, page)
    output += ['## Sources', '']
    for key, record in board['sources'].items():
        output += ['- ' + cell(key) + ': ' + normalized_citations(board, [key], root, page) + ('; snapshot ' + cell(record['snapshot_date']) if 'snapshot_date' in record else '')]
    output += ['', 'Original source snapshots and the [migration field map](' + local_link(root / 'docs/evidence/migration-2026-11-19/field-map.json', page) + ') preserve historical context. No unresolved source claim was silently corrected.', '']
    if (definition.parent / 'sources/README.md').is_file():
        output += ['See [source limitations](sources/README.md) for inherited missing images/site-relative links.', '']
    return '\n'.join(output).rstrip() + '\n'


def main():
    """Purpose: Write generated pages. Design: Fixed repository outputs. Workflow: Run this source file. Data Handoff: Markdown files/stdout."""
    root = Path(__file__).resolve().parents[2]
    outputs = build_pages(root)
    for relative, content in outputs.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        print(relative)


if __name__ == '__main__':
    main()
