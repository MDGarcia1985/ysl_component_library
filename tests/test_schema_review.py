"""File: tests/test_schema_review.py
Purpose: Define schema-review expectations before writing the draft schemas.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Synthetic fixtures and local evaluation; no catalog migration or package implementation.
Related decision: DEV-2026-11-19-004.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import runpy
import unittest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/schema_review'


def fixture(name='board'):
    """Purpose: Read independent inputs. Design: Fixed authored JSON. Workflow: Tests. Data Handoff: Fresh fixture mapping."""
    return json.loads((FIXTURES / f'{name}.json').read_text(encoding='utf-8'))


def validator(filename='component.schema.json'):
    """Purpose: Exercise actual schema files. Design: Offline registry. Workflow: Tests. Data Handoff: JSON Schema validator."""
    registry = Registry()
    for path in sorted((ROOT / 'schemas').glob('*.schema.json')):
        schema = json.loads(path.read_text(encoding='utf-8'))
        if '$id' in schema:
            registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
    return Draft202012Validator(json.loads((ROOT / 'schemas' / filename).read_text(encoding='utf-8')), registry=registry, format_checker=FormatChecker())


class SchemaReviewTests(unittest.TestCase):
    """Purpose: Review draft contracts. Design: Positive and adversarial cases. Workflow: unittest. Data Handoff: Observable failures."""

    def test_schema_documents_and_positive_kinds(self):
        """Purpose: AC-101. Design: Three authored shapes. Workflow: Review run. Data Handoff: Assertions."""
        paths = list((ROOT / 'schemas').glob('*.schema.json'))
        self.assertGreaterEqual(len(paths), 6)
        for path in paths:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding='utf-8')))
        for name in ('board', 'family', 'module'):
            with self.subTest(kind=name):
                self.assertEqual(list(validator().iter_errors(fixture(name))), [])

    def test_identity_types_and_closed_fields(self):
        """Purpose: AC-102. Design: Fixed invalid edits. Workflow: Review run. Data Handoff: Required rejections."""
        cases = []
        for field in ('id', 'name', 'manufacturer', 'schema_version', 'pins'):
            value = fixture()
            del value[field]
            cases.append((f'missing_{field}', value))
        for field, invalid in [('id', 'Arduino/Bad ID'), ('schema_version', '99.0.0'), ('kind', 'firmware'), ('category', 'software')]:
            value = fixture()
            value[field] = invalid
            cases.append((field, value))
        value = fixture(); value['pin_map'] = value['pins']; cases.append(('misspelled_root', value))
        value = fixture(); value['pins']['TX']['capabilties'] = []; cases.append(('misspelled_pin', value))
        value = fixture(); value['connectors']['J1']['positions'] = True; cases.append(('boolean_position_count', value))
        value = fixture(); value['board']['processors']['mcu']['attributes'] = {'anything': 1}; cases.append(('untyped_blob', value))
        value = fixture(); value['module'] = {'module_type': 'sensor'}; cases.append(('wrong_kind_details', value))
        value = fixture(); value['id'] += '\n'; cases.append(('whitespace_id', value))
        value = fixture(); value['sources']['manual']['path'] = '../outside.md'; cases.append(('source_traversal', value))
        value = fixture(); value['sources']['manual']['path'] = '/absolute.md'; cases.append(('absolute_source_path', value))
        value = fixture(); value['pins']['TX']['location']['position'] = 'A1\n'; cases.append(('whitespace_position', value))
        for label, value in cases:
            with self.subTest(case=label):
                self.assertTrue(list(validator().iter_errors(value)), label)

    def test_quantity_units_and_uncertainty(self):
        """Purpose: AC-102 uncertainty. Design: Conflicting facts cannot pick a winner. Workflow: Review run. Data Handoff: Rejections."""
        cases = []
        value = fixture(); value['facts']['logic_voltage']['value']['unit'] = 'mA'; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['value']['nominal'] = '3.3'; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['value']['nominal'] = True; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['value']['unit'] = 'volts'; cases.append(value)
        value = fixture(); value['facts']['radio_version']['value'] = '5.3'; cases.append(value)
        value = fixture(); value['facts']['radio_version']['claims'] = value['facts']['radio_version']['claims'][:1]; cases.append(value)
        value = fixture('module'); value['facts']['per_pin_current']['value'] = False; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['source_refs'] = []; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['status'] = 'derived'; cases.append(value)
        value = fixture(); value['verification']['status'] = 'bench_tested'; cases.append(value)
        value = fixture(); value['sources']['manual']['snapshot_date'] = '2026-02-30'; cases.append(value)
        value = fixture(); value['facts']['logic_voltage']['value'] = 3.3; cases.append(value)
        for index, value in enumerate(cases):
            with self.subTest(case=index):
                self.assertTrue(list(validator().iter_errors(value)))
        value = fixture(); value['facts']['logic_voltage']['status'] = 'derived'; value['facts']['logic_voltage']['derivation'] = 'Synthetic derivation, not a measurement.'
        self.assertEqual(list(validator().iter_errors(value)), [])

    def test_registry_and_proposed_ids(self):
        """Purpose: AC-104 shape. Design: Fixed registry expectations. Workflow: Review run. Data Handoff: Assertions."""
        registry = json.loads((ROOT / 'schemas/identity-registry.json').read_text(encoding='utf-8'))
        self.assertEqual(list(validator('identity-registry.schema.json').iter_errors(registry)), [])
        expected = {'arduino/uno-r3', 'arduino/ventuno-q', 'microchip/attiny-x5', 'ti/l293-family', 'generic/hc-sr04'}
        self.assertEqual({entry['id'] for entry in registry['entries']}, expected)
        self.assertEqual(registry['status'], 'proposed')
        review = runpy.run_path(str(ROOT / 'tests/schema_review_support.py'))
        self.assertEqual(review['registry_errors'](registry), [])
        repeated = deepcopy(registry); repeated['entries'].append(deepcopy(registry['entries'][0]))
        self.assertIn('ID_COLLISION', {item['code'] for item in review['registry_errors'](repeated)})
        collision = deepcopy(registry); collision['entries'][1]['legacy_aliases'] = ['ARDUINO_UNO_R3']
        self.assertIn('ALIAS_COLLISION', {item['code'] for item in review['registry_errors'](collision)})
        import yaml
        for entry in registry['entries']:
            legacy = yaml.safe_load((ROOT / entry['definition_path']).read_text(encoding='utf-8-sig'))
            self.assertEqual(legacy['id'], entry['id'])
            self.assertTrue(set(entry['legacy_aliases']).issubset(legacy['aliases']))
            data = legacy
            self.assertEqual(entry['variant_selectors'], list(data.get('variants', {})))
            self.assertEqual(entry['profile_selectors'], list(data.get('profiles', {})))

    def test_semantic_references_positions_and_cycles(self):
        """Purpose: AC-104/105. Design: Typed cross-field faults. Workflow: Review harness. Data Handoff: Stable diagnostic codes."""
        review = runpy.run_path(str(ROOT / 'tests/schema_review_support.py'))
        check = review['semantic_errors']
        self.assertEqual(check([fixture(), fixture('family'), fixture('module')]), [])
        reserved = fixture()
        reserved['facts']['processor'] = {'status': 'legacy_uncited', 'value': 'Historical descriptive label, not an entity reference'}
        reserved['sources']['connector'] = deepcopy(reserved['sources']['manual'])
        self.assertEqual(list(validator().iter_errors(reserved)), [])
        self.assertEqual(check([reserved]), [])
        cases = []
        value = fixture(); value['interfaces']['UART0']['signals']['TX'] = 'MISSING'; cases.append((value, 'REF_NOT_FOUND'))
        value = fixture(); value['pins']['TX']['location']['connector'] = 'MISSING'; cases.append((value, 'REF_NOT_FOUND'))
        value = fixture(); value['pins']['AUX']['location']['connector'] = 'J1'; cases.append((value, 'POSITION_COLLISION'))
        value = fixture(); value['pins']['AUX']['location'] = {'connector': 'J1', 'position': 1.0}; cases.append((value, 'POSITION_COLLISION'))
        value = fixture(); value['pins']['RX']['location']['position'] = 3; cases.append((value, 'POSITION_OUT_OF_RANGE'))
        value = fixture(); value['facts']['logic_voltage']['source_refs'] = ['MISSING']; cases.append((value, 'REF_NOT_FOUND'))
        value = fixture(); value['facts']['logic_voltage']['value'].update(min=5, max=3); cases.append((value, 'QUANTITY_ORDER'))
        value = fixture('family'); value['variants']['BASE']['inherits'] = 'variant:PROTECTED'; cases.append((value, 'INHERITANCE_CYCLE'))
        value = fixture('family'); value['profiles']['LOW_VOLTAGE']['inherits'] = 'variant:MISSING'; cases.append((value, 'REF_NOT_FOUND'))
        value = fixture(); value['power_domains']['logic']['input_dependencies'] = ['logic']; cases.append((value, 'POWER_CYCLE'))
        value = fixture(); value['connections']['uart_header']['to'] = 'connector:MISSING'; cases.append((value, 'REF_NOT_FOUND'))
        value = fixture(); value['facts']['radio_version']['claims'][1]['value'] = '5.1'; cases.append((value, 'CONFLICT_NOT_DISTINCT'))
        value = fixture(); value['verification'] = {'status': 'bench_tested', 'records': {'failed_bench': {'kind': 'bench_test', 'result': 'fail', 'reviewer': 'Synthetic reviewer', 'date': '2026-11-19', 'scope': 'Synthetic test only', 'procedure': 'No hardware used', 'observations': 'Synthetic failure', 'artifact_path': 'tests/fixtures/synthetic_result.txt'}}}; cases.append((value, 'VERIFICATION_EVIDENCE_MISSING'))
        for value, expected in cases:
            with self.subTest(code=expected):
                errors = check([value])
                self.assertIn(expected, {item['code'] for item in errors})
                self.assertTrue(all(item['path'].startswith('/') for item in errors))
        self.assertIn('ID_COLLISION', {e['code'] for e in check([fixture(), fixture()])})
        other = fixture('module'); other['aliases'] = ['REVIEW_BOARD']
        self.assertIn('ALIAS_COLLISION', {e['code'] for e in check([fixture(), other])})
        quantity = fixture(); quantity['facts']['logic_voltage']['value']['nominal'] = 0.0033; quantity['facts']['logic_voltage']['value']['unit'] = 'kV'
        self.assertTrue(list(validator().iter_errors(quantity)))

    def test_strict_yaml_input_boundary(self):
        """Purpose: AC-103. Design: Fixed hostile/ambiguous YAML. Workflow: Review harness. Data Handoff: Explicit rejections."""
        review = runpy.run_path(str(ROOT / 'tests/schema_review_support.py'))
        load = review['load_review_yaml']
        for text in ('pin: first\npin: second\n', 'x: &x {pin: a}\ny: *x\n', 'x: &x {pin: a}\ny: {<<: *x}\n', '---\npin: a\n---\npin: b\n', 'x: !!python/object:builtins.object {}\n', '2026-11-19: pin\n', 'pin: 2026-11-19\n', 'pin: .nan\n'):
            with self.subTest(yaml=text):
                with self.assertRaises(ValueError):
                    load(text)
        self.assertEqual(load('pins: {"ON": {maps_to: "OFF"}}\n'), {'pins': {'ON': {'maps_to': 'OFF'}}})

    def test_hardware_and_packaging_are_unchanged(self):
        """Purpose: Preserve approved inputs. Design: Archived bytes and current schema adoption. Workflow: Review run. Data Handoff: Assertions."""
        baseline = json.loads((ROOT / 'docs/evidence/schema-review-2026-11-19/before.json').read_text(encoding='utf-8'))
        migration = json.loads((ROOT / 'docs/evidence/migration-2026-11-19/baseline.json').read_text(encoding='utf-8'))
        snapshots = {item['path']: item['snapshot'] for item in migration['definitions'].values()}
        for name, digest in baseline['preserved_files'].items():
            if name.endswith('/README.md') and '/sources/' not in name:
                definition = ROOT / name.replace('/README.md', '/definition.yml')
                self.assertIn(hashlib.sha256(definition.read_bytes()).hexdigest(), (ROOT / name).read_text(encoding='utf-8'))
            else:
                self.assertEqual(hashlib.sha256((ROOT / snapshots.get(name, name)).read_bytes()).hexdigest(), digest, name)
        import yaml
        for path in (ROOT / 'hardware').rglob('definition.yml'):
            self.assertTrue(validator().is_valid(yaml.safe_load(path.read_text(encoding='utf-8-sig'))), str(path))
        for name, record in baseline['journal_prefixes'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()[:record['byte_length']]).hexdigest(), record['sha256'])
        for path in ('src/ysl_components/__init__.py', 'src/ysl_components/__main__.py', 'dist', 'build'):
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == '__main__':
    unittest.main()
