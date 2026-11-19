# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tools/migrate_catalog.py
Purpose: Reproduce the authorized P2 migration from preserved original snapshots.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: One-off source utility; no query CLI, package implementation, or source-spec correction.
Related decision: DEV-2026-11-19-005.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
import yaml

VERSION = '1.0.0-draft.1'
FOLDER = 'docs/evidence/migration-2026-11-19'
UNITS = {'V': 'voltage', 'mA': 'current', 'A': 'current', 'Hz': 'frequency', 'MB': 'storage', 'GB': 'storage', 'byte': 'storage', 'mm': 'length', 'm': 'length', 'ms': 'time', 'us': 'time', 's': 'time', 'deg': 'angle', 'W': 'power', 'bit': 'resolution', 'bit/s': 'data_rate', 'Mbit/s': 'data_rate', 'GHz': 'frequency', 'TOPS': 'compute_rate', 'm/s': 'speed', 'count': 'count', '1': 'ratio'}
SUFFIXES = [('_m_per_s', 'm/s'), ('_bytes', 'byte'), ('_bits', 'bit'), ('_mbps', 'Mbit/s'), ('_bps', 'bit/s'), ('_ghz', 'GHz'), ('_hz', 'Hz'), ('_tops', 'TOPS'), ('_gb', 'GB'), ('_mm', 'mm'), ('_ms', 'ms'), ('_us', 'us'), ('_deg', 'deg'), ('_v', 'V'), ('_a', 'A'), ('_w', 'W'), ('_s', 's')]
COUNTS = {'cpu_cores', 'onboard_antennas', 'onboard_ports', 'additional_ports_via_header', 'tmds_data_pairs', 'tmds_clock_pairs', 'data_lanes', 'control_gpio_physical_pin', 'rows', 'columns', 'count', 'mounting_standoffs', 'standard_available', 'conditional_available', 'transmitted_cycles_per_measurement', 'positions'}


def pointer(parts):
    """Purpose: Name mapping locations. Design: JSON Pointer escaping. Workflow: Migration trace. Data Handoff: String."""
    return '/' + '/'.join(str(value).replace('~', '~0').replace('/', '~1') for value in parts)


def leaf_paths(node, path=()):
    """Purpose: Inventory trace coverage. Design: Preserve empty containers too. Workflow: Finalization. Data Handoff: Leaf pointers."""
    if isinstance(node, dict) and node:
        return {p: value for key, child in node.items() for p, value in leaf_paths(child, path + (key,)).items()}
    if isinstance(node, list) and node:
        return {p: value for key, child in enumerate(node) for p, value in leaf_paths(child, path + (key,)).items()}
    return {pointer(path): node}


class Migration:
    """Purpose: Normalize one definition. Design: Every source leaf traced. Workflow: Catalog utility. Data Handoff: Component and field map."""

    def __init__(self, entry, original, snapshot):
        """Purpose: Set explicit identity/context. Design: Approved registry and original bytes. Workflow: Conversion. Data Handoff: Mutable trace state."""
        self.entry, self.original, self.snapshot = entry, original, snapshot
        self.legacy, self.old = next(iter(original.items()))
        self.fields = {}
        self.default_refs = ['manual'] if entry['id'] == 'arduino/ventuno-q' else (['datasheet'] if entry['id'] == 'generic/hc-sr04' else ['legacy_snapshot'])
        self.default_status = 'documented' if self.default_refs != ['legacy_snapshot'] else 'legacy_uncited'
        self.out = {'schema_version': VERSION, 'id': entry['id'], 'name': {'arduino/uno-r3': 'Arduino Uno R3', 'arduino/ventuno-q': 'Arduino VENTUNO Q', 'microchip/attiny-x5': 'ATtiny25 / ATtiny45 / ATtiny85', 'ti/l293-family': 'L293 / L293D', 'generic/hc-sr04': 'HC-SR04'}[entry['id']], 'category': entry['definition_path'].split('/')[1], 'kind': entry['kind'], 'manufacturer': {'status': 'known', 'name': self.old['manufacturer']} if 'manufacturer' in self.old else {'status': 'unknown', 'reason': 'Manufacturer not specified in the original definition.'}, 'aliases': [self.legacy], 'provenance': self.provenance(), 'sources': {}, 'verification': {'status': 'not_verified', 'records': {}, 'notes': 'Schema/source migration and static checks do not establish bench verification.'}, 'facts': {}, 'pins': {}, 'connectors': {}, 'interfaces': {}, 'constraints': {}}
        if 'manufacturer' in self.old:
            self.track(('manufacturer',), ('manufacturer', 'name'))

    def provenance(self, refs=None, status=None):
        """Purpose: Preserve citation strength. Design: Uncited stays uncited. Workflow: Entity/fact creation. Data Handoff: Provenance object."""
        return {'status': status or self.default_status, 'source_refs': list(self.default_refs if refs is None else refs)}

    def put(self, path, value):
        """Purpose: Write normalized destinations. Design: Only declared object structures. Workflow: Conversion. Data Handoff: Output mutation."""
        node = self.out
        for key in path[:-1]:
            node = node.setdefault(key, {})
        node[path[-1]] = deepcopy(value)

    def track(self, old_path, new_path):
        """Purpose: Preserve original values. Design: Trace every original leaf. Workflow: After copying data. Data Handoff: Mapping entries."""
        value = self.old
        for key in old_path:
            value = value[key]
        for suffix in leaf_paths(value):
            parts = [] if suffix == '/' else [part.replace('~1', '/').replace('~0', '~') for part in suffix[1:].split('/')]
            source = pointer((self.legacy,) + old_path + tuple(parts))
            destination = pointer(new_path + tuple(parts))
            self.fields.setdefault(source, [])
            if destination not in self.fields[source]:
                self.fields[source].append(destination)

    def copy(self, old_path, new_path):
        """Purpose: Copy meaningful fields. Design: No implicit value transforms. Workflow: Entity conversion. Data Handoff: Value and trace."""
        value = self.old
        for key in old_path:
            value = value[key]
        self.put(new_path, value)
        self.track(old_path, new_path)

    def entity(self, node, old_path, new_path, **extra):
        """Purpose: Create typed entity metadata. Design: Explicit source inheritance. Workflow: Section conversion. Data Handoff: Output entity."""
        refs = node.get('source_refs', self.default_refs)
        self.put(new_path, {'facts': {}, 'provenance': self.provenance(refs), **extra})
        if 'source_refs' in node:
            self.track(old_path + ('source_refs',), new_path + ('provenance', 'source_refs'))

    def unit(self, path, hint=None):
        """Purpose: Assign explicit dimensions. Design: Source suffix/units whitelist; no numeric guessing. Workflow: Facts. Data Handoff: Unit or error."""
        for part in reversed(path):
            label = str(part).lower()
            for suffix, unit in SUFFIXES:
                if label.endswith(suffix):
                    return unit
        if hint:
            return hint[0]
        if any(str(part).lower() in ('voltage', 'logic_voltage') for part in path):
            return 'V'
        if str(path[-1]) == 'factory_clock_divider':
            return '1'
        if any(str(part) in COUNTS for part in path):
            return 'count'
        raise ValueError('Numeric source requires an explicit unit decision: ' + '/'.join(map(str, path)))

    def facts(self, node, old_path, destination, prefix=(), refs=None, hint=None, status=None):
        """Purpose: Normalize supplemental facts. Design: Typed leaves, never opaque blobs. Workflow: Entity leftovers. Data Handoff: Facts and exact trace."""
        refs = self.default_refs if refs is None else refs
        if isinstance(node, dict):
            local_refs = node.get('source_refs', refs)
            local_hint = (node['units'], old_path + ('units',)) if 'units' in node else hint
            stats = {key: value for key, value in node.items() if key in ('value', 'min', 'max', 'nominal', 'typical') and isinstance(value, (int, float)) and not isinstance(value, bool)}
            skipped = {'source_refs', 'units'}
            if stats:
                unit = local_hint[0] if local_hint else self.unit(old_path, local_hint)
                quantity = {'dimension': UNITS[unit], 'unit': unit, 'rating_kind': 'operating' if 'voltage' in old_path or 'electrical' in old_path else 'unspecified', **stats}
                name = '__'.join(map(str, prefix)) or 'rating'
                target = destination + (name,)
                self.put(target, {'status': status or self.default_status, 'value': quantity, 'source_refs': list(local_refs)})
                for key in stats:
                    self.track(old_path + (key,), target + ('value', key))
                if local_hint:
                    self.track(local_hint[1], target + ('value', 'unit'))
                if 'source_refs' in node:
                    self.track(old_path + ('source_refs',), target + ('source_refs',))
                skipped.update(stats)
            for key, value in node.items():
                if key not in skipped:
                    self.facts(value, old_path + (key,), destination, prefix + (key,), local_refs, local_hint, status)
            if 'source_refs' in node and pointer((self.legacy,) + old_path + ('source_refs', '0')) not in self.fields:
                # A source-only context still gets a typed provenance-bearing note.
                name = '__'.join(map(str, prefix + ('source_context',)))
                target = destination + (name,)
                self.put(target, {'status': status or self.default_status, 'value': 'Source context for this section', 'source_refs': list(local_refs)})
                self.track(old_path + ('source_refs',), target + ('source_refs',))
            return
        if isinstance(node, list):
            for index, value in enumerate(node):
                self.facts(value, old_path + (index,), destination, prefix + (str(index),), refs, hint, status)
            return
        name = '__'.join(map(str, prefix)) or str(old_path[-1])
        target = destination + (name,)
        container = self.out
        for key in destination:
            container = container.setdefault(key, {})
        if name in container:
            raise ValueError(f'Fact key collision: {target}')
        value = node
        statistic = 'value'
        if isinstance(node, (int, float)) and not isinstance(node, bool):
            unit = self.unit(old_path, hint)
            label = str(old_path[-1])
            statistic = next((part for part in ('min', 'max', 'nominal', 'typical') if part in label.split('_')), 'value')
            rating = 'continuous' if 'continuous' in label else ('peak' if 'peak' in label else ('resolution' if 'resolution' in label else 'unspecified'))
            value = {'dimension': UNITS[unit], 'unit': unit, 'rating_kind': rating, statistic: node}
        self.put(target, {'status': status or self.default_status, 'value': value, 'source_refs': list(refs)})
        self.track(old_path, target + (('value', statistic) if isinstance(value, dict) else ('value',)))
        if isinstance(value, dict) and hint and value['unit'] == hint[0]:
            self.track(hint[1], target + ('value', 'unit'))

    def leftovers(self, node, old_path, destination, excluded):
        """Purpose: Account for nonstructural data. Design: Explicit exclusions plus typed facts. Workflow: Entities. Data Handoff: Trace coverage."""
        self.facts({key: value for key, value in node.items() if key not in excluded}, old_path, destination, refs=node.get('source_refs', self.default_refs))

    def sources(self):
        """Purpose: Retain original attribution. Design: Copy locators without claiming new verification. Workflow: Before entities. Data Handoff: Source map."""
        self.out['sources']['legacy_snapshot'] = {'title': 'Pre-migration repository definition', 'kind': 'legacy_note', 'path': self.snapshot, 'notes': 'Original bytes and comments preserved; this locator does not establish manufacturer verification.'}
        source = self.old.get('source', {})
        if self.legacy == 'arduino_ventuno_q':
            self.out['sources']['manual'] = {'title': source['document'], 'kind': 'manual', 'path': source['path'], 'snapshot_date': source['snapshot_pulled_date'], 'author': source['author']}
            for old, new in [('document', 'title'), ('path', 'path'), ('snapshot_pulled_date', 'snapshot_date'), ('author', 'author')]:
                self.track(('source', old), ('sources', 'manual', new))
            for key, record in source['references'].items():
                self.out['sources'][key] = {'title': record['heading'], 'kind': 'manual', 'path': record['path'], 'section': record['heading'], 'snapshot_date': record['snapshot_pulled_date'], 'notes': record['evidence_type']}
                for old, new in [('path', 'path'), ('heading', 'section'), ('snapshot_pulled_date', 'snapshot_date'), ('evidence_type', 'notes')]:
                    self.track(('source', 'references', key, old), ('sources', key, new))
            for key, url in source['related_documents'].items():
                self.out['sources']['linked_' + key] = {'title': key.replace('_', ' ').title(), 'kind': {'full_pinout': 'pinout', 'schematics': 'schematic', 'datasheet': 'datasheet'}[key], 'url': url, 'notes': 'Linked by the copied manual; not fetched to resolve source discrepancies.'}
                self.track(('source', 'related_documents', key), ('sources', 'linked_' + key, 'url'))
            for record in source['discrepancies']:
                index = source['discrepancies'].index(record)
                target = ('constraints', 'source_conflict__' + record['topic'])
                self.entity(record, ('source', 'discrepancies', index), target, kind='source_conflict', rule=record['disposition'])
                self.track(('source', 'discrepancies', index, 'disposition'), target + ('rule',))
                self.leftovers(record, ('source', 'discrepancies', index), target + ('facts',), {'source_refs', 'disposition'})
            self.leftovers(source, ('source',), ('facts',), {'document', 'path', 'snapshot_pulled_date', 'author', 'references', 'related_documents', 'discrepancies'})
        elif source:
            self.out['sources']['datasheet'] = {'title': source['document'], 'kind': 'datasheet', 'url': source['url']}
            self.track(('source', 'document'), ('sources', 'datasheet', 'title'))
            self.track(('source', 'url'), ('sources', 'datasheet', 'url'))
            self.leftovers(source, ('source',), ('facts',), {'document', 'url'})

    def connectors(self):
        """Purpose: Preserve connector identity. Design: No guessed positions. Workflow: Before pin locations. Data Handoff: Connector maps."""
        for key, node in self.old.get('connectors', {}).items():
            target = ('connectors', key)
            self.entity(node, ('connectors', key), target, type=node.get('type', 'documented_header'))
            for field in ('type', 'positions', 'processor'):
                if field in node:
                    self.copy(('connectors', key, field), target + (field,))
            self.leftovers(node, ('connectors', key), target + ('facts',), {'type', 'positions', 'processor', 'source_refs'})
        if self.entry['kind'] == 'ic_family':
            self.out['connectors']['PACKAGE'] = {'type': 'ic_package', 'facts': {}, 'provenance': self.provenance()}
        if self.entry['id'] == 'generic/hc-sr04':
            header = self.old['physical']['header']
            self.out['connectors']['HEADER'] = {'type': 'module_header', 'positions': header['positions'], 'facts': {}, 'provenance': self.provenance()}
            self.track(('physical', 'header', 'positions'), ('connectors', 'HEADER', 'positions'))

    def pins(self):
        """Purpose: Preserve all 345 named pin records. Design: Keep shared aliases explicitly. Workflow: Conversion. Data Handoff: Canonical pin map."""
        for section in ('pin_map', 'power_pins', 'special_pins'):
            for key, node in self.old.get(section, {}).items():
                old_path, target = (section, key), ('pins', key)
                self.entity(node, old_path, target)
                copied = {'source_refs'}
                for field in ('maps_to', 'capabilities', 'aliases', 'shared_with'):
                    if field in node:
                        self.copy(old_path + (field,), target + (field,)); copied.add(field)
                if 'direction' in node and node['direction'] != 'power':
                    self.copy(old_path + ('direction',), target + ('direction',)); copied.add('direction')
                connector = node.get('connector') or ('PACKAGE' if self.entry['kind'] == 'ic_family' else ('HEADER' if self.entry['id'] == 'generic/hc-sr04' else None))
                if 'physical_pin' in node:
                    if connector is None:
                        raise ValueError('Physical position has no source-supported connector context')
                    self.put(target + ('location',), {'connector': connector, 'position': node['physical_pin']})
                    self.track(old_path + ('physical_pin',), target + ('location', 'position')); copied.add('physical_pin')
                    if 'connector' in node:
                        self.track(old_path + ('connector',), target + ('location', 'connector')); copied.add('connector')
                self.leftovers(node, old_path, target + ('facts',), copied)

    def interfaces(self):
        """Purpose: Normalize real signal references. Design: Preserve alternate lists and implementation labels. Workflow: Conversion. Data Handoff: Interfaces."""
        types = {'full_h_bridge': 'h_bridge', 'operational_amplifier': 'opamp', 'can_fd': 'can_bus', 'can_controller_signals': 'can_controller', 'ultrasonic_time_of_flight': 'ultrasonic_time_of_flight'}
        for key, node in self.old.get('interfaces', {}).items():
            old_path, target = ('interfaces', key), ('interfaces', key)
            inferred = {'ICSP': 'programming', 'ISP': 'programming', 'USI_SPI': 'spi', 'USI_I2C': 'i2c', 'ADC': 'adc', 'PWM': 'pwm', 'ANALOG_COMPARATOR': 'analog_comparator', 'power': 'power'}.get(key, 'custom')
            kind = types.get(node.get('type'), node.get('type', inferred))
            self.entity(node, old_path, target, type=kind, signals={})
            if kind == 'custom': self.put(target + ('description',), 'Legacy interface ' + key)
            def visit(value, path, roles):
                """Purpose: Distinguish signals from metadata. Design: Resolve declared pins only. Workflow: Interface traversal. Data Handoff: Signals/facts."""
                name = '__'.join(map(str, roles))
                if isinstance(value, str) and value in self.out['pins']:
                    self.copy(path, target + ('signals', name))
                elif isinstance(value, list) and value and all(isinstance(item, str) and item in self.out['pins'] for item in value):
                    self.copy(path, target + ('signals', name))
                elif isinstance(value, dict):
                    for child, item in value.items(): visit(item, path + (child,), roles + (child,))
                else:
                    self.facts(value, path, target + ('facts',), roles, refs=node.get('source_refs', self.default_refs))
            for field, value in node.items():
                if field == 'source_refs': continue
                if field in ('processor', 'implementation'):
                    self.copy(old_path + (field,), target + (field,))
                elif field == 'connector':
                    self.put(target + ('connector_refs',), [value]); self.track(old_path + (field,), target + ('connector_refs', 0))
                elif field == 'type' and value == kind:
                    self.copy(old_path + (field,), target + ('type',))
                else:
                    visit(value, old_path + (field,), (field,))

    def parts_and_members(self):
        """Purpose: Preserve processor, component and family distinctions. Design: Explicit members, no expansion guesses. Workflow: Conversion. Data Handoff: Typed entities."""
        if self.entry['kind'] == 'board':
            self.out['board'] = {'processors': {}}
            processors = self.old.get('processors', {'mcu': {}})
            for key, node in processors.items():
                target = ('board', 'processors', key)
                self.entity(node, ('processors', key), target, role='Processor ' + key)
                model = self.old.get(key)
                if model:
                    self.copy((key,), target + ('model',))
                if 'architecture' in node:
                    self.copy(('processors', key, 'architecture'), target + ('architecture',))
                if node:
                    self.leftovers(node, ('processors', key), target + ('facts',), {'architecture', 'source_refs'})
        elif self.entry['kind'] == 'ic_family':
            self.out['ic_family'] = {'family': self.old.get('family', self.out['name'])}
            for field in ('family', 'architecture', 'package'):
                if field in self.old: self.copy((field,), ('ic_family', field))
        else:
            self.out['module'] = {'module_type': self.old.get('device_type', 'hardware_module')}
            if 'device_type' in self.old: self.track(('device_type',), ('module', 'module_type'))
        for key, node in self.old.get('onboard_components', {}).items():
            target = ('onboard_components', key)
            self.entity(node, ('onboard_components', key), target, role=node['role'])
            self.track(('onboard_components', key, 'role'), target + ('role',))
            if 'part_number' in node: self.copy(('onboard_components', key, 'part_number'), target + ('model',))
            self.leftovers(node, ('onboard_components', key), target + ('facts',), {'part_number', 'role', 'source_refs'})
        for section in ('variants', 'profiles'):
            for key, node in self.old.get(section, {}).items():
                target = (section, key)
                self.entity(node, (section, key), target)
                if 'inherits' in node:
                    self.put(target + ('inherits',), 'variant:' + node['inherits'])
                    # Keep the original selector too, so the trace requires exact equality.
                self.leftovers(node, (section, key), target + ('facts',), {'source_refs'})

    def relationships(self):
        """Purpose: Preserve graph/conflict semantics. Design: Approved enum plus original details. Workflow: Conversion. Data Handoff: Graph and conditions."""
        for key, node in self.old.get('connections', {}).items():
            target = ('connections', key)
            self.put(target, {'from': node['from'], 'to': node['to'], 'relationship': node['relationship'], 'routing_status': 'conflicting' if 'unresolved' in node.get('routing_status', '') else 'documented', 'provenance': self.provenance(node['source_refs'])})
            for field in ('from', 'to', 'relationship', 'via'):
                if field in node: self.copy(('connections', key, field), target + (field,))
            if 'routing_status' in node: self.copy(('connections', key, 'routing_status'), target + ('notes',))
            self.track(('connections', key, 'source_refs'), target + ('provenance', 'source_refs'))
        for key, node in self.old.get('resource_conflicts', {}).items():
            target = ('resource_conflicts', key)
            policy = {'unavailable_to_external_header_while_bluetooth_active': 'unavailable_when', 'at_most_one_active': 'at_most_one_active', 'not_simultaneous_as_stated_by_manual': 'not_simultaneous', 'gpio_and_alternate_function_not_simultaneous_on_same_pin': 'per_pin_exclusion'}[node['policy']]
            self.put(target, {'policy': policy, 'notes': node['policy'], 'provenance': self.provenance(node['source_refs'])})
            self.track(('resource_conflicts', key, 'policy'), target + ('notes',))
            for field in ('affected_pins', 'participants'):
                if field in node: self.copy(('resource_conflicts', key, field), target + (field,))
            if policy == 'unavailable_when': self.put(target + ('when',), {'target': 'component:nfa725b', 'state': 'bluetooth_active'})
            self.track(('resource_conflicts', key, 'source_refs'), target + ('provenance', 'source_refs'))
            leftovers = {field: value for field, value in node.items() if field not in {'policy', 'affected_pins', 'participants', 'source_refs'}}
            if leftovers:
                context = ('constraints', 'resource_context__' + key)
                self.entity(node, ('resource_conflicts', key), context, kind='condition', rule='Additional source context for resource conflict ' + key)
                self.facts(leftovers, ('resource_conflicts', key), context + ('facts',))

    def other_sections(self):
        """Purpose: Preserve non-pin facts and power relationships. Design: Typed facts and scoped constraints. Workflow: Conversion. Data Handoff: Remaining sections."""
        for key, node in self.old.get('constraints', {}).items():
            target = ('constraints', key)
            self.entity(node if isinstance(node, dict) else {}, ('constraints', key), target, kind='requirement', rule='Preserve source constraint group: ' + key)
            self.facts(node, ('constraints', key), target + ('facts',))
        if 'logic' in self.old:
            target = ('constraints', 'logic_truth_table')
            self.entity({}, (), target, kind='condition', rule='Source H-bridge logic states; no executable safety inference.')
            self.facts(self.old['logic'], ('logic',), target + ('facts',))
        for key, node in self.old.get('voltage', {}).items():
            if key == 'units': continue
            target = ('power_domains', key)
            role = 'input' if key.endswith('_input') else ('reference' if key.endswith('_logic') else 'rail')
            self.entity(node if isinstance(node, dict) else {}, ('voltage', key), target, role=role)
            hint = (self.old['voltage']['units'], ('voltage', 'units')) if 'units' in self.old['voltage'] else None
            self.facts(node, ('voltage', key), target + ('facts',), hint=hint)
        for key, node in self.old.get('power_distribution', {}).items():
            if not isinstance(node, dict):
                if key != 'source_refs': self.facts(node, ('power_distribution', key), ('facts',), ('power_distribution', key))
                continue
            target = ('power_domains', key)
            self.entity(node, ('power_distribution', key), target, role='output', limit_scope='unknown')
            self.facts(node, ('power_distribution', key), target + ('facts',))
            if 'connectors' in node: self.put(target + ('feeds',), ['connector:' + name for name in node['connectors']])
            if 'input_ref' in node: self.put(target + ('input_dependencies',), [node['input_ref']])
        if 'source_refs' in self.old.get('power_distribution', {}):
            self.facts({'source_refs': self.old['power_distribution']['source_refs']}, ('power_distribution',), ('facts',), ('power_distribution',))
        for section in ('onboard', 'wireless'):
            values = self.old.get(section, {})
            feature_items = values.items() if section == 'onboard' else ([('wireless', values)] if values else [])
            for key, node in feature_items:
                old_path = (section, key) if section == 'onboard' else (section,)
                target = ('features', key)
                self.entity(node, old_path, target, type=key)
                excluded = {'source_refs'}
                for field in ('processor', 'connected_processor'):
                    if field in node: self.copy(old_path + (field,), target + ('processor',)); excluded.add(field)
                if key == 'wireless':
                    versions = node['bluetooth']['versions_stated']
                    self.put(target + ('facts', 'bluetooth_version'), {'status': 'conflicting', 'claims': [{'value': value, 'source_refs': ['architecture'] if value == '5.3' else ['wireless']} for value in versions], 'notes': 'Manual sections disagree; no version selected.'})
                    for index in range(len(versions)): self.track(old_path + ('bluetooth', 'versions_stated', index), target + ('facts', 'bluetooth_version', 'claims', index, 'value'))
                    remaining = deepcopy(node); del remaining['bluetooth']['versions_stated']
                    self.leftovers(remaining, old_path, target + ('facts',), excluded)
                else:
                    self.leftovers(node, old_path, target + ('facts',), excluded)
        excluded = {'manufacturer', 'source', 'pin_map', 'power_pins', 'special_pins', 'interfaces', 'connectors', 'variants', 'profiles', 'constraints', 'logic', 'voltage', 'onboard', 'wireless', 'processors', 'onboard_components', 'connections', 'resource_conflicts', 'power_distribution'}
        excluded.update({'mcu', 'mpu'} if self.entry['kind'] == 'board' else {'family', 'architecture', 'package'})
        if self.entry['kind'] == 'module': excluded.add('device_type')
        self.leftovers(self.old, (), ('facts',), excluded)

    def finish(self):
        """Purpose: Enforce complete accounting. Design: Fail on any unexplained source field. Workflow: Finalization. Data Handoff: Component/map."""
        self.sources(); self.connectors(); self.pins(); self.interfaces(); self.parts_and_members(); self.relationships(); self.other_sections()
        original = leaf_paths(self.original)
        missing = sorted(set(original) - set(self.fields))
        if missing:
            raise ValueError(f'{self.entry["id"]} unmapped source leaves: {missing[:12]}')
        covered = {p for targets in self.fields.values() for p in targets}
        generated = {p: {'value': value, 'reason': 'Structural normalization, source-supported classification, explicit unit interpretation, schema metadata, or uncertainty; not a new electrical observation.'} for p, value in leaf_paths(self.out).items() if p not in covered}
        return self.out, {'source_snapshot': self.snapshot, 'fields': dict(sorted(self.fields.items())), 'generated_fields': generated}


def migrate_catalog(root):
    """Purpose: Reproduce P2 from original bytes. Design: Pure conversion, no writes. Workflow: Tests/source utility. Data Handoff: Documents/maps."""
    root = Path(root)
    baseline = json.loads((root / FOLDER / 'baseline.json').read_text(encoding='utf-8'))
    entries = json.loads((root / 'schemas/identity-registry.json').read_text(encoding='utf-8'))['entries']
    documents, maps = {}, {}
    for entry in entries:
        snapshot = baseline['definitions'][entry['id']]['snapshot']
        original = yaml.safe_load((root / snapshot).read_text(encoding='utf-8-sig'))
        documents[entry['id']], maps[entry['id']] = Migration(entry, original, snapshot).finish()
    return documents, maps


class Dumper(yaml.SafeDumper):
    """Purpose: Readable deterministic YAML. Design: Indented lists, no aliases. Workflow: Writing. Data Handoff: YAML text."""
    def increase_indent(self, flow=False, indentless=False):
        """Purpose: Keep lists readable. Design: Consistent two-space levels. Workflow: Dumper. Data Handoff: Parent indent state."""
        return super().increase_indent(flow, False)
    def ignore_aliases(self, data):
        """Purpose: Emit independent values. Design: Approved YAML subset forbids aliases. Workflow: Dumper. Data Handoff: Always true."""
        return True


def main():
    """Purpose: Write authorized migration outputs. Design: Fixed registry destinations. Workflow: Direct source script. Data Handoff: YAML and trace report."""
    root = Path(__file__).resolve().parents[1]
    documents, maps = migrate_catalog(root)
    # Validate all converted documents before replacing any destination. The
    # independent conservation/reference tests remain outside this converter.
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    registry = Registry()
    for schema_path in sorted((root / 'schemas').glob('*.schema.json')):
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
        registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
    schema = json.loads((root / 'schemas/component.schema.json').read_text(encoding='utf-8'))
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    for document in documents.values():
        validator.validate(document)
    baseline = json.loads((root / FOLDER / 'baseline.json').read_text(encoding='utf-8'))
    for identity, document in documents.items():
        destination = root / baseline['definitions'][identity]['path']
        destination.write_text('# Schema/ID migration; original source bytes are retained in docs/evidence/migration-2026-11-19/before/.\n# Related decision: DEV-2026-11-19-005. No bench verification is implied.\n\n' + yaml.dump(document, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')
        print(identity, len(document['pins']), 'pins', len(maps[identity]['fields']), 'source leaves')
    (root / FOLDER / 'field-map.json').write_text(json.dumps(maps, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
