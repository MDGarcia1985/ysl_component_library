# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/test_query_contract.py
Purpose: Execute AC-301 through AC-308 against the frozen query contract.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Subprocess only. Expected values come from fixtures and literals, not query helpers.
Related decision: DEV-2026-11-19-006.
"""

from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
BOARD = json.loads((ROOT / 'tests/fixtures/schema_review/board.json').read_text(encoding='utf-8'))
MODULE = json.loads((ROOT / 'tests/fixtures/schema_review/module.json').read_text(encoding='utf-8'))
CATALOG_IDS = [
    'arduino/uno-r3',
    'arduino/ventuno-q',
    'generic/hc-sr04',
    'microchip/attiny-x5',
    'ti/l293-family',
]


def run_cli(args, catalog=None, cwd=None, fault=False, block_network=False):
    """Purpose: Run the candidate as a subprocess. Design: No import of query helpers.
    Workflow: Every AC case. Data Handoff: Completed process.
    """
    env = os.environ.copy()
    python_path = [str(ROOT / 'src')]
    if block_network:
        python_path.append(str(ROOT / 'tests/fixtures/query_contract'))
    env['PYTHONPATH'] = os.pathsep.join(python_path)
    env.pop('YSL_COMPONENTS_FAULT', None)
    if fault:
        env['YSL_COMPONENTS_FAULT'] = 'unexpected'
    command = [sys.executable, '-B', '-m', 'ysl_components']
    if catalog is not None:
        command.extend(['--catalog', str(catalog)])
    command.extend(args)
    return subprocess.run(command, cwd=cwd or ROOT, env=env, capture_output=True, text=True)


def parsed(result):
    """Purpose: Require a JSON document and JSON diagnostics. Design: Reject mixed stdout.
    Workflow: Assertions. Data Handoff: Envelope and diagnostic list.
    """
    document = json.loads(result.stdout)
    diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
    return document, diagnostics


def write_yaml(directory, relative, document):
    """Purpose: Place a fixed fixture in a catalog. Design: Test-side dump, not the CLI exporter.
    Workflow: Synthetic catalogs. Data Handoff: Written path.
    """
    path = directory / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False), encoding='utf-8')
    return path


def tree_hashes(directory):
    """Purpose: Prove queries do not modify a catalog. Design: Hash regular files only.
    Workflow: Before and after. Data Handoff: Path-to-digest map.
    """
    found = {}
    for path in sorted(item for item in directory.rglob('*') if item.is_file() and not item.is_symlink()):
        found[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


def index_document(directory):
    """Purpose: Build the frozen index independently. Design: Raw definition bytes.
    Workflow: AC-308. Data Handoff: Index object.
    """
    definitions = []
    for path in sorted(item for item in directory.rglob('definition.yml') if item.is_file()):
        definitions.append({
            'path': path.relative_to(directory).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return {
        'algorithm': 'sha256-definition-bytes-v1',
        'definitions': definitions,
        'schema_version': '1.0.0-draft.1',
    }


class QueryContractTests(unittest.TestCase):
    """Purpose: Cover the frozen P3 cases. Design: Black-box process results.
    Workflow: unittest. Data Handoff: Failures naming the AC id.
    """

    def assert_envelope(self, document, operation):
        """Purpose: Check the frozen wrapper. Design: Safety flags stay false.
        Workflow: Successful and failed responses. Data Handoff: Assertion.
        """
        self.assertEqual(document['envelope'], {
            'contract': 'ysl-components-query',
            'revision': '1',
            'schema_version': '1.0.0-draft.1',
        })
        self.assertEqual(document['operation'], operation)
        self.assertFalse(document['safety']['connection_asserted_safe'])
        self.assertFalse(document['safety']['bench_verification_inferred'])
        self.assertNotIn('"connection_asserted_safe": true', json.dumps(document))

    def test_ac301_validation_enumerates_valid_and_invalid_files(self):
        """Purpose: AC-301. Design: One malformed file among schema and reference failures.
        Workflow: validate. Data Handoff: Exit 2 and every file.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_yaml(root, 'valid/definition.yml', BOARD)
            (root / 'broken').mkdir()
            (root / 'broken/definition.yml').write_text('id: one\nid: two\n', encoding='utf-8')
            shaped = json.loads(json.dumps(BOARD))
            shaped['id'] = 'review/shaped'
            shaped['aliases'] = ['shaped_board']
            shaped['pin_map'] = {}
            write_yaml(root, 'shaped/definition.yml', shaped)
            dangling = json.loads(json.dumps(BOARD))
            dangling['id'] = 'review/dangling'
            dangling['aliases'] = ['dangling_board']
            dangling['pins']['TX']['processor'] = 'missing'
            write_yaml(root, 'dangling/definition.yml', dangling)
            result = run_cli(['validate'], root)
            document, diagnostics = parsed(result)
            self.assertEqual(result.returncode, 2)
            self.assert_envelope(document, 'validate')
            self.assertEqual(document['result']['status'], 'invalid')
            self.assertEqual(
                [item['path'] for item in document['result']['files']],
                ['broken/definition.yml', 'dangling/definition.yml', 'shaped/definition.yml', 'valid/definition.yml'],
            )
            self.assertIsNone(document['result']['files'][0]['id'])
            self.assertEqual(document['result']['files'][3]['id'], 'review/synthetic-board')
            codes = {item['code'] for item in diagnostics}
            self.assertIn('YAML_DUPLICATE_KEY', codes)
            self.assertIn('SCHEMA_INVALID', codes)
            self.assertIn('REF_NOT_FOUND', codes)
            self.assertGreaterEqual(document['result']['diagnostic_count'], 3)
            clean = run_cli(['validate'], root)
            # The mixed catalog is the case above. A separate valid tree must exit 0.
            with tempfile.TemporaryDirectory() as valid_dir:
                valid_root = Path(valid_dir)
                write_yaml(valid_root, 'alpha/definition.yml', BOARD)
                clean = run_cli(['validate'], valid_root)
            document, diagnostics = parsed(clean)
            self.assertEqual(clean.returncode, 0, clean.stderr)
            self.assertEqual(diagnostics, [])
            self.assertEqual(document['result']['status'], 'valid')
            self.assertEqual(document['result']['files'][0]['id'], 'review/synthetic-board')

    def test_ac302_list_and_search_are_catalog_specific(self):
        """Purpose: AC-302. Design: Fixed ids, filters, and an empty search.
        Workflow: list and search on the real catalog and a synthetic one. Data Handoff: Assertions.
        """
        listed = run_cli(['list'], ROOT)
        document, diagnostics = parsed(listed)
        self.assertEqual(listed.returncode, 0)
        self.assertEqual(diagnostics, [])
        self.assertEqual([item['id'] for item in document['result']['components']], CATALOG_IDS)
        by_id = {item['id']: item for item in document['result']['components']}
        self.assertEqual(by_id['arduino/uno-r3']['manufacturer']['status'], 'unknown')
        self.assertEqual(by_id['arduino/ventuno-q']['manufacturer'], {'name': 'Arduino', 'status': 'known'})
        self.assertEqual(by_id['generic/hc-sr04']['kind'], 'module')
        self.assertEqual(by_id['ti/l293-family']['category'], 'drivers')
        self.assertTrue(all(item['verification_status'] == 'not_verified' for item in document['result']['components']))
        families = run_cli(['list', '--kind', 'ic_family'], ROOT)
        self.assertEqual(
            [item['id'] for item in parsed(families)[0]['result']['components']],
            ['microchip/attiny-x5', 'ti/l293-family'],
        )
        sensors = run_cli(['list', '--category', 'sensors'], ROOT)
        self.assertEqual([item['id'] for item in parsed(sensors)[0]['result']['components']], ['generic/hc-sr04'])
        arduino = run_cli(['list', '--manufacturer', 'Arduino'], ROOT)
        self.assertEqual([item['id'] for item in parsed(arduino)[0]['result']['components']], ['arduino/ventuno-q'])
        unknown = run_cli(['search', '--manufacturer', 'unknown'], ROOT)
        self.assertEqual(
            [item['id'] for item in parsed(unknown)[0]['result']['components']],
            ['arduino/uno-r3', 'generic/hc-sr04'],
        )
        empty = run_cli(['search', '--text', 'zzz-no-component'], ROOT)
        empty_document, empty_diagnostics = parsed(empty)
        self.assertEqual(empty.returncode, 0)
        self.assertEqual(empty_diagnostics, [])
        self.assertEqual(empty_document['result'], {'components': [], 'status': 'ok'})
        pwm = run_cli(['search', '--capability', 'pwm'], ROOT)
        self.assertEqual(
            [item['id'] for item in parsed(pwm)[0]['result']['components']],
            ['arduino/uno-r3', 'arduino/ventuno-q', 'microchip/attiny-x5'],
        )
        echo = run_cli(['search', '--interface-type', 'ultrasonic_time_of_flight'], ROOT)
        self.assertEqual([item['id'] for item in parsed(echo)[0]['result']['components']], ['generic/hc-sr04'])
        conflicts = run_cli(['search', '--fact-status', 'conflicting'], ROOT)
        self.assertEqual([item['id'] for item in parsed(conflicts)[0]['result']['components']], ['arduino/ventuno-q'])
        with tempfile.TemporaryDirectory() as temporary:
            other = Path(temporary)
            write_yaml(other, 'widget/definition.yml', MODULE)
            other_list = run_cli(['list'], other)
            self.assertEqual([item['id'] for item in parsed(other_list)[0]['result']['components']], ['generic/synthetic-sensor'])
            self.assertNotIn('arduino/uno-r3', other_list.stdout)

    def test_ac303_show_pin_alias_interface_and_variant(self):
        """Purpose: AC-303. Design: Literals taken from the migrated definitions and the synthetic board.
        Workflow: show, pin, pins, and interface. Data Handoff: Assertions.
        """
        uno = parsed(run_cli(['pin', 'arduino/uno-r3', 'D5'], ROOT))[0]['result']
        self.assertEqual(uno['pin'], 'D5')
        self.assertEqual(uno['maps_to'], 'PD5')
        self.assertEqual(uno['resolved_by'], 'key')
        self.assertIn('pwm', uno['capabilities'])
        self.assertEqual(uno['verification_status'], 'not_verified')
        ventuno = parsed(run_cli(['pin', 'arduino_ventuno_q', 'D5'], ROOT))[0]
        self.assertEqual(ventuno['selection'], {
            'component': 'arduino/ventuno-q',
            'profile': None,
            'resolved_by': 'alias',
            'variant': None,
        })
        self.assertEqual(ventuno['result']['maps_to'], 'PB5')
        self.assertEqual(ventuno['result']['aliases'], ['FDCAN2_RX'])
        ambiguous = run_cli(['pin', 'arduino/uno-r3', 'D18'], ROOT)
        ambiguous_document, ambiguous_diagnostics = parsed(ambiguous)
        self.assertEqual(ambiguous.returncode, 4)
        self.assertEqual(ambiguous_document['result'], {
            'candidates': ['A4', 'SDA'],
            'code': 'AMBIGUOUS_PIN',
            'status': 'ambiguous',
        })
        self.assertEqual(ambiguous_diagnostics[0]['code'], 'AMBIGUOUS_PIN')
        self.assertIsNone(ambiguous_document['selection']['component'])
        sda = parsed(run_cli(['pin', 'arduino/uno-r3', 'SDA'], ROOT))[0]['result']
        self.assertEqual(sda['maps_to'], 'PC4')
        self.assertEqual(sda['shared_with'], 'A4')
        analog = parsed(run_cli(['pin', 'arduino/ventuno-q', 'A4'], ROOT))[0]['result']
        self.assertEqual(analog['maps_to'], 'PE14')
        self.assertNotIn('i2c_sda', analog['capabilities'])
        qwiic = parsed(run_cli(['pin', 'arduino/ventuno-q', 'QWIIC_SDA'], ROOT))[0]['result']
        self.assertEqual(qwiic['maps_to'], 'PC9')
        self.assertIn('i2c_sda', qwiic['capabilities'])
        missing = run_cli(['pin', 'arduino/uno-r3', 'D99'], ROOT)
        self.assertEqual(missing.returncode, 3)
        self.assertEqual(parsed(missing)[0]['result']['code'], 'PIN_NOT_FOUND')
        unknown = run_cli(['show', 'missing/board'], ROOT)
        self.assertEqual(unknown.returncode, 3)
        self.assertEqual(parsed(unknown)[0]['result']['code'], 'COMPONENT_NOT_FOUND')
        bad_variant = run_cli(['show', 'ti/l293-family', '--variant', 'L293X'], ROOT)
        self.assertEqual(bad_variant.returncode, 3)
        self.assertEqual(parsed(bad_variant)[0]['result']['code'], 'VARIANT_NOT_FOUND')
        diodes = parsed(run_cli(['show', 'ti/l293-family', '--variant', 'L293D'], ROOT))[0]['result']
        self.assertEqual(diodes['selected_variant'], 'L293D')
        self.assertIs(diodes['selected_facts']['integrated_clamp_diodes']['value'], True)
        self.assertEqual(diodes['selected_facts']['continuous_output_current_a']['value']['value'], 0.6)
        self.assertEqual(diodes['selected_facts']['continuous_output_current_a']['value']['rating_kind'], 'continuous')
        self.assertEqual(diodes['selected_facts']['peak_output_current_a']['value']['value'], 1.2)
        plain = parsed(run_cli(['show', 'ti/l293-family', '--variant', 'L293'], ROOT))[0]['result']
        self.assertIs(plain['selected_facts']['integrated_clamp_diodes']['value'], False)
        self.assertEqual(plain['selected_facts']['continuous_output_current_a']['value']['value'], 1.0)
        profile = parsed(run_cli(['show', 'microchip/attiny-x5', '--profile', 'ATtiny85V'], ROOT))[0]['result']
        self.assertEqual(profile['selected_facts']['voltage_profile']['status'], 'legacy_uncited')
        self.assertEqual(profile['selected_facts']['voltage_profile']['value'], 'v_variant')
        self.assertEqual(profile['selected_facts']['max_clock_hz']['value']['max'], 10000000)
        self.assertEqual(profile['verification_status'], 'not_verified')
        pwm = parsed(run_cli(['pins', 'arduino/ventuno-q', '--capability', 'pwm'], ROOT))[0]['result']['pins']
        self.assertEqual(sorted(item['pin'] for item in pwm), ['D10', 'D11', 'D3', 'D5', 'D6', 'D9'])
        self.assertEqual({item['pin']: item['maps_to'] for item in pwm}['D5'], 'PB5')
        header = parsed(run_cli(['pins', 'generic/hc-sr04', '--connector', 'HEADER'], ROOT))[0]['result']['pins']
        self.assertEqual([item['pin'] for item in header], ['ECHO', 'GND', 'TRIG', 'VCC'])
        interface = parsed(run_cli(['interface', 'generic/hc-sr04', 'range_measurement'], ROOT))[0]['result']
        self.assertEqual(interface['type'], 'ultrasonic_time_of_flight')
        self.assertEqual(interface['signals'], {'ground': 'GND', 'power': 'VCC', 'response': 'ECHO', 'trigger': 'TRIG'})
        missing_interface = run_cli(['interface', 'generic/hc-sr04', 'UART0'], ROOT)
        self.assertEqual(missing_interface.returncode, 3)
        self.assertEqual(parsed(missing_interface)[0]['result']['code'], 'INTERFACE_NOT_FOUND')

    def test_ac304_conflicts_and_types_stay_stable(self):
        """Purpose: AC-304. Design: Repeat the same command and compare parsed types.
        Workflow: show twice. Data Handoff: Identical stdout and unselected conflicts.
        """
        first = run_cli(['show', 'arduino/ventuno-q'], ROOT)
        second = run_cli(['show', 'arduino/ventuno-q'], ROOT)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        document = json.loads(first.stdout)
        bluetooth = next(item for item in document['result']['uncertainty']['facts'] if item['path'] == 'features.wireless.facts.bluetooth_version')
        self.assertEqual(bluetooth['status'], 'conflicting')
        self.assertIsNone(bluetooth['selected_value'])
        self.assertEqual(bluetooth['claims'], [
            {'source_refs': ['architecture'], 'value': '5.3'},
            {'source_refs': ['wireless'], 'value': '5.1'},
        ])
        self.assertIsInstance(bluetooth['claims'][0]['value'], str)
        connection = document['result']['uncertainty']['connections']
        self.assertEqual(connection, [{
            'id': 'can_bus_path',
            'notes': 'PD0_PD1_TX_RX_assignment_unresolved',
            'routing_status': 'conflicting',
        }])
        self.assertEqual(document['result']['verification_status'], 'not_verified')
        sensor = parsed(run_cli(['show', 'generic/hc-sr04'], ROOT))[0]['result']
        self.assertEqual(sensor['manufacturer']['status'], 'unknown')
        echo = sensor['constraints']['interface']['facts']['echo_level_shift_required_for_3v3_only_host']
        self.assertIs(echo['value'], True)
        self.assertEqual(echo['status'], 'documented')
        legacy = parsed(run_cli(['show', 'arduino/uno-r3'], ROOT))[0]['result']
        clock = next(item for item in legacy['uncertainty']['facts'] if item['path'] == 'facts.clock_hz')
        self.assertEqual(clock['status'], 'legacy_uncited')
        self.assertEqual(clock['value']['value'], 16000000)
        self.assertNotEqual(clock['status'], 'documented')

    def test_ac305_stdout_stderr_and_exit_codes(self):
        """Purpose: AC-305. Design: One subprocess per exit category.
        Workflow: Fault seam, usage, data, lookup, ambiguity, and schema version.
        Data Handoff: Exit codes and channel split.
        """
        cases = []
        success = run_cli(['validate'], ROOT)
        cases.append((0, success, None))
        fault = run_cli(['validate'], ROOT, fault=True)
        cases.append((1, fault, 'UNEXPECTED'))
        usage = run_cli(['list'])
        cases.append((2, usage, 'USAGE'))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'broken').mkdir()
            (root / 'broken/definition.yml').write_text('{', encoding='utf-8')
            invalid = run_cli(['list'], root)
            cases.append((2, invalid, 'YAML_SYNTAX'))
            write_yaml(root, 'future/definition.yml', {**BOARD, 'schema_version': '9.9.9', 'id': 'review/future', 'aliases': ['future_board']})
            unsupported = run_cli(['list'], root)
            cases.append((5, unsupported, 'SCHEMA_UNSUPPORTED'))
        missing = run_cli(['show', 'missing/part'], ROOT)
        cases.append((3, missing, 'COMPONENT_NOT_FOUND'))
        ambiguous = run_cli(['pin', 'arduino/uno-r3', 'D18'], ROOT)
        cases.append((4, ambiguous, 'AMBIGUOUS_PIN'))
        absent = run_cli(['list'], ROOT / 'missing-catalog-directory')
        cases.append((3, absent, 'CATALOG_NOT_FOUND'))
        for code, result, diagnostic_code in cases:
            with self.subTest(code=code, diagnostic=diagnostic_code):
                self.assertEqual(result.returncode, code)
                document, diagnostics = parsed(result)
                self.assertTrue(result.stdout.endswith('\n'))
                self.assertNotIn('\n{', result.stdout)
                if code == 0:
                    self.assertEqual(diagnostics, [])
                else:
                    self.assertIn(diagnostic_code, [item['code'] for item in diagnostics])
                self.assertFalse(document['safety']['connection_asserted_safe'])
        both = run_cli(['show', 'ti/l293-family', '--variant', 'L293', '--profile', 'ATtiny85V'], ROOT)
        self.assertEqual(both.returncode, 2)
        self.assertEqual(parsed(both)[1][0]['code'], 'SELECTION_CONFLICT')
        helped = run_cli(['--help'])
        self.assertEqual(helped.returncode, 2)
        self.assertEqual(parsed(helped)[0]['result']['status'], 'invalid_usage')

    def test_ac306_export_round_trip_and_overwrite(self):
        """Purpose: AC-306. Design: Reload exported bytes with an independent parser.
        Workflow: JSON and YAML export. Data Handoff: Semantic equality and protected files.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            catalog = root / 'catalog'
            outside = root / 'outside'
            outside.mkdir()
            write_yaml(catalog, 'alpha/definition.yml', BOARD)
            before = tree_hashes(catalog)
            json_path = outside / 'board.json'
            exported = run_cli(['export', 'review/synthetic-board', '--format', 'json', '--output', str(json_path)], catalog)
            self.assertEqual(exported.returncode, 0, exported.stderr)
            self.assertEqual(tree_hashes(catalog), before)
            loaded = json.loads(json_path.read_text(encoding='utf-8'))
            self.assertEqual(loaded, BOARD)
            self.assertEqual(loaded['facts']['radio_version']['status'], 'conflicting')
            self.assertNotIn('value', loaded['facts']['radio_version'])
            self.assertIsInstance(loaded['facts']['logic_voltage']['value']['nominal'], float)
            yaml_path = outside / 'board.yaml'
            yaml_export = run_cli(['export', 'review_board', '--format', 'yaml', '--output', str(yaml_path)], catalog)
            self.assertEqual(yaml_export.returncode, 0, yaml_export.stderr)
            self.assertEqual(yaml.safe_load(yaml_path.read_text(encoding='utf-8')), BOARD)
            blocked = run_cli(['export', 'review/synthetic-board', '--format', 'json', '--output', str(json_path)], catalog)
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(parsed(blocked)[1][0]['code'], 'OUTPUT_EXISTS')
            self.assertEqual(json.loads(json_path.read_text(encoding='utf-8')), BOARD)
            json_path.write_text('placeholder\n', encoding='utf-8')
            forced = run_cli(['export', 'review/synthetic-board', '--format', 'json', '--output', str(json_path), '--force'], catalog)
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertEqual(json.loads(json_path.read_text(encoding='utf-8')), BOARD)
            protected = catalog / 'alpha/definition.yml'
            digest = hashlib.sha256(protected.read_bytes()).hexdigest()
            refused = run_cli(['export', 'review/synthetic-board', '--format', 'json', '--output', str(protected), '--force'], catalog)
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(parsed(refused)[1][0]['code'], 'OUTPUT_PROTECTED')
            self.assertEqual(hashlib.sha256(protected.read_bytes()).hexdigest(), digest)

    def test_ac307_readonly_paths_and_no_network(self):
        """Purpose: AC-307. Design: Absolute path with spaces, another working directory, blocked sockets.
        Workflow: Linux only. Data Handoff: Unchanged hashes. Windows is not claimed.
        """
        self.assertNotEqual(sys.platform, 'win32')
        self.assertIn('Linux', platform.platform())
        before = tree_hashes(ROOT / 'hardware')
        with tempfile.TemporaryDirectory() as temporary:
            spaced = Path(temporary) / 'my catalog'
            spaced.mkdir()
            write_yaml(spaced, 'widget/definition.yml', MODULE)
            elsewhere = Path(temporary) / 'elsewhere'
            elsewhere.mkdir()
            result = run_cli(['show', 'generic/synthetic-sensor'], spaced, cwd=elsewhere, block_network=True)
            document, diagnostics = parsed(result)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(diagnostics, [])
            self.assertEqual(document['result']['id'], 'generic/synthetic-sensor')
            self.assertEqual(document['catalog']['path'], spaced.resolve().as_posix())
            self.assertNotIn('arduino/uno-r3', result.stdout)
            self.assertEqual(document['result']['uncertainty']['facts'][0]['status'], 'legacy_uncited')
            unknown = next(item for item in document['result']['uncertainty']['facts'] if item['status'] == 'unknown')
            self.assertIsNone(unknown['selected_value'])
        listed = run_cli(['list'], ROOT, cwd=Path(tempfile.gettempdir()), block_network=True)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual([item['id'] for item in parsed(listed)[0]['result']['components']], CATALOG_IDS)
        self.assertEqual(tree_hashes(ROOT / 'hardware'), before)

    def test_ac308_stale_index_is_rejected(self):
        """Purpose: AC-308. Design: Corrupt the index, then change a definition without refreshing it.
        Workflow: validate and list. Data Handoff: INDEX_STALE and no component list.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = write_yaml(root, 'alpha/definition.yml', BOARD)
            fresh = index_document(root)
            (root / 'catalog-index.json').write_text(json.dumps(fresh, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            valid = run_cli(['validate'], root)
            document, diagnostics = parsed(valid)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertEqual(diagnostics, [])
            self.assertEqual(document['result']['index'], 'fresh')
            listed = parsed(run_cli(['list'], root))[0]['result']['components']
            self.assertEqual([item['id'] for item in listed], ['review/synthetic-board'])
            stale = json.loads(json.dumps(fresh))
            stale['definitions'][0]['sha256'] = '0' * 64
            (root / 'catalog-index.json').write_text(json.dumps(stale), encoding='utf-8')
            rejected = run_cli(['list'], root)
            rejected_document, rejected_diagnostics = parsed(rejected)
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(rejected_diagnostics[0]['code'], 'INDEX_STALE')
            self.assertEqual(rejected_document['result'], {'diagnostic_count': 1, 'status': 'invalid'})
            self.assertNotIn('components', rejected_document['result'])
            (root / 'catalog-index.json').write_text(json.dumps(fresh), encoding='utf-8')
            target.write_text(target.read_text(encoding='utf-8') + '\n', encoding='utf-8')
            changed = run_cli(['show', 'review/synthetic-board'], root)
            self.assertEqual(changed.returncode, 2)
            self.assertEqual(parsed(changed)[1][0]['code'], 'INDEX_STALE')
            self.assertNotIn('review/synthetic-board', parsed(changed)[0]['result'].get('components', []))
            broken = root / 'catalog-index.json'
            broken.write_text('{', encoding='utf-8')
            invalid = run_cli(['validate'], root)
            self.assertEqual(invalid.returncode, 2)
            self.assertEqual(parsed(invalid)[1][0]['code'], 'INDEX_INVALID')


if __name__ == '__main__':
    unittest.main()
