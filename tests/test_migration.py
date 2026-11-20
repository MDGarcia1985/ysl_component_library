# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/test_migration.py
Purpose: Define P2 preservation, schema, source-oracle, and corruption tests first.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Local self-evaluation only; no independent/human G2 approval implied.
Related decision: DEV-2026-11-19-005.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import runpy
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'docs/evidence/migration-2026-11-19'
BASELINE = json.loads((FOLDER / 'baseline.json').read_text(encoding='utf-8'))
COMPARE = runpy.run_path(str(ROOT / 'tests/migration_checks.py'))
STRICT_LOAD = runpy.run_path(str(ROOT / 'tests/schema_review_support.py'))['load_review_yaml']


def matches_recorded_digest(path, digest):
    """Purpose: Compare a preserved file with its recorded digest.
    Design: LF git blobs match a Windows CRLF baseline when that is the only difference.
    A changed character matches neither digest. See DEV-2026-11-19-007.
    Workflow: AC-206. Data Handoff: Boolean.
    """
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() == digest:
        return True
    if b'\r' not in data:
        return hashlib.sha256(data.replace(b'\n', b'\r\n')).hexdigest() == digest
    return False


def migrated():
    """Purpose: Read candidate definitions. Design: Baseline IDs/paths. Workflow: Tests. Data Handoff: ID-to-document mapping."""
    return {identity: STRICT_LOAD((ROOT / item['path']).read_text(encoding='utf-8')) for identity, item in BASELINE['definitions'].items()}


class MigrationTests(unittest.TestCase):
    """Purpose: Test P2 independently. Design: Snapshots plus direct manual oracles. Workflow: unittest. Data Handoff: Evidence/failures."""

    def test_all_five_schema_and_semantic_contracts(self):
        """Purpose: AC-201. Design: Approved schema and semantic checks. Workflow: Test run. Data Handoff: Assertions."""
        checker = runpy.run_path(str(ROOT / 'tests/test_schema_review.py'))['validator']()
        documents = migrated()
        self.assertEqual(set(documents), set(BASELINE['definitions']))
        for identity, document in documents.items():
            self.assertEqual(document.get('id'), identity)
            self.assertEqual(list(checker.iter_errors(document)), [], identity)
            self.assertIn(BASELINE['definitions'][identity]['legacy_root'], document['aliases'])
        semantic = runpy.run_path(str(ROOT / 'tests/schema_review_support.py'))['semantic_errors']
        self.assertEqual(semantic(list(documents.values())), [])

    def test_complete_source_and_destination_field_maps(self):
        """Purpose: AC-201. Design: No migrator imports. Workflow: Every original leaf. Data Handoff: Exact conservation assertions."""
        maps = json.loads((FOLDER / 'field-map.json').read_text(encoding='utf-8'))
        for identity, document in migrated().items():
            original = yaml.safe_load((ROOT / BASELINE['definitions'][identity]['snapshot']).read_text(encoding='utf-8-sig'))
            self.assertEqual(COMPARE['conservation_errors'](original, document, maps[identity]), [], identity)
        self.assertEqual(sum(len(doc['pins']) for doc in migrated().values()), 345)

    def test_manual_pin_tables_and_independent_board_facts(self):
        """Purpose: AC-202/203. Design: Compare actual source tables directly. Workflow: Test run. Data Handoff: Assertions."""
        documents = migrated()
        board = documents['arduino/ventuno-q']
        self.assertEqual(board['pins']['D5']['maps_to'], 'PB5')
        self.assertEqual(documents['arduino/uno-r3']['pins']['D5']['maps_to'], 'PD5')
        manual = (ROOT / 'hardware/controllers/arduino/ventuno_q/sources/user_manual.md').read_text(encoding='utf-8')
        uno_rows = re.search(r'(?m)^\| MCU Pin.*(?:\n\|.*)+', manual).group().splitlines()[2:]
        self.assertEqual(len(uno_rows), 22)
        for row in uno_rows:
            port, labels, _ = [cell.strip() for cell in row.strip('|').split('|')]
            labels = [label.strip() for label in labels.split('/')]
            number = int(labels[0][1:])
            key = f'A{number - 14}' if 14 <= number <= 19 else labels[0]
            self.assertEqual(board['pins'][key]['maps_to'], port)
            self.assertTrue(set(labels).issubset({key, *board['pins'][key].get('aliases', [])}))
        for connector, heading, count in [('JHAT', '### RPi 40-Pin Header', 40), ('JMEDIA', '#### JMEDIA', 60), ('JMISC', '#### JMISC', 60), ('JOMEGA', '### JOMEGA Expansion Header', 100)]:
            section = manual.split(heading + '\n', 1)[1]
            block = re.search(r'(?m)^\|.*(?:\n\|.*)+', section).group()
            rows = [[cell.strip() for cell in row.strip('|').split('|')] for row in block.splitlines()[2:]]
            self.assertEqual(len(rows), count)
            for position, signal, function in rows:
                number = int(position.replace('Pin', '').strip())
                pin = board['pins'][f'{connector}_{number}']
                self.assertEqual(pin['maps_to'], function if signal == '-' else signal)
                self.assertEqual(pin['location'], {'connector': connector, 'position': number})
                if signal != '-' and function:
                    self.assertEqual(pin['facts']['source_function']['value'], function)
        self.assertEqual(set(board['interfaces']['UNO_PWM']['signals']['pins']), {'D3', 'D5', 'D6', 'D9', 'D10', 'D11'})
        self.assertEqual(board['resource_conflicts']['jhat_bluetooth_uart']['affected_pins'], ['JHAT_8', 'JHAT_10', 'JHAT_11', 'JHAT_36'])

    def test_variant_safety_and_source_conflicts_survive(self):
        """Purpose: AC-204. Design: Fixed discriminating source facts. Workflow: Test run. Data Handoff: Assertions."""
        documents = migrated()
        attiny = documents['microchip/attiny-x5']
        self.assertEqual(set(attiny['variants']), {'ATtiny25', 'ATtiny45', 'ATtiny85'})
        self.assertEqual(set(attiny['profiles']), {'ATtiny25V', 'ATtiny45V', 'ATtiny85V'})
        self.assertEqual(attiny['pins']['PB5']['maps_to'], 'PB5')
        self.assertTrue(attiny['constraints']['reset']['facts']['gpio_requires_fuse_change']['value'])
        self.assertEqual(attiny['interfaces']['USI_I2C']['implementation'], 'usi_software')
        driver = documents['ti/l293-family']
        self.assertEqual(driver['variants']['L293']['facts']['continuous_output_current_a']['value']['value'], 1.0)
        self.assertEqual(driver['variants']['L293D']['facts']['continuous_output_current_a']['value']['value'], 0.6)
        for variant in ('L293', 'L293D'):
            quantity = driver['variants'][variant]['facts']['continuous_output_current_a']['value']
            self.assertEqual((quantity['dimension'], quantity['unit'], quantity['rating_kind']), ('current', 'A', 'continuous'))
        self.assertFalse(driver['variants']['L293']['facts']['integrated_clamp_diodes']['value'])
        self.assertTrue(driver['variants']['L293D']['facts']['integrated_clamp_diodes']['value'])
        self.assertTrue(documents['generic/hc-sr04']['constraints']['interface']['facts']['echo_level_shift_required_for_3v3_only_host']['value'])
        vent = documents['arduino/ventuno-q']
        self.assertEqual(len([key for key in vent['constraints'] if key.startswith('source_conflict__')]), 6)
        self.assertEqual(vent['features']['wireless']['facts']['bluetooth_version']['status'], 'conflicting')
        self.assertTrue(all(doc['verification']['status'] == 'not_verified' for doc in documents.values()))

    def test_required_deliberate_corruptions_are_detected(self):
        """Purpose: AC-205. Design: Mutate data independently of mapping code. Workflow: Comparison. Data Handoff: Rejection observations."""
        documents = migrated()
        maps = json.loads((FOLDER / 'field-map.json').read_text(encoding='utf-8'))
        variants = []
        item = deepcopy(documents['arduino/ventuno-q']); del item['pins']['JOMEGA_100']; variants.append(('arduino/ventuno-q', item))
        item = deepcopy(documents['arduino/ventuno-q']); item['pins']['D5']['maps_to'] = 'PD5'; variants.append(('arduino/ventuno-q', item))
        item = deepcopy(documents['ti/l293-family']); fields = item['variants']['L293']['facts']; fields['continuous_output_current_a'], fields['peak_output_current_a'] = fields['peak_output_current_a'], fields['continuous_output_current_a']; variants.append(('ti/l293-family', item))
        item = deepcopy(documents['microchip/attiny-x5']); del item['variants']['ATtiny45']; variants.append(('microchip/attiny-x5', item))
        item = deepcopy(documents['arduino/ventuno-q']); item['features']['wireless']['facts']['bluetooth_version'] = {'status': 'documented', 'value': '5.3', 'source_refs': ['architecture']}; variants.append(('arduino/ventuno-q', item))
        item = deepcopy(documents['ti/l293-family']); item['variants']['L293']['facts']['continuous_output_current_a']['value'].update(dimension='voltage', unit='V'); variants.append(('ti/l293-family', item))
        for mutation, (identity, item) in enumerate(variants):
            with self.subTest(component=identity, mutation=mutation):
                original = yaml.safe_load((ROOT / BASELINE['definitions'][identity]['snapshot']).read_text(encoding='utf-8-sig'))
                self.assertTrue(COMPARE['conservation_errors'](original, item, maps[identity]))

    def test_sources_schema_bytes_and_history_are_preserved(self):
        """Purpose: AC-206. Design: Pre-change byte hashes. Workflow: Test run. Data Handoff: Assertions."""
        for path, digest in BASELINE['preserved_files'].items():
            if path == 'pyproject.toml':
                import tomllib
                project = tomllib.loads((ROOT / path).read_text(encoding='utf-8'))
                self.assertTrue(project['tool']['ysl_component_library']['packaging_enabled'])
                self.assertNotEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)
                continue
            self.assertTrue(matches_recorded_digest(ROOT / path, digest), path)
        for identity, item in BASELINE['definitions'].items():
            self.assertTrue(matches_recorded_digest(ROOT / item['snapshot'], item['sha256']), identity)
        for name, record in BASELINE['journals'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()[:record['byte_length']]).hexdigest(), record['sha256'])
        self.assertTrue((ROOT / 'src/ysl_components/__main__.py').exists())
        self.assertFalse((ROOT / 'dist').exists())

    def test_migration_is_deterministic_from_snapshots(self):
        """Purpose: AC-206. Design: Pure repeated conversion. Workflow: Source utility. Data Handoff: Equal results/maps."""
        migrate = runpy.run_path(str(ROOT / 'tools/migrate_catalog.py'))['migrate_catalog']
        first, maps = migrate(ROOT)
        second, again = migrate(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(maps, again)
        self.assertEqual(first, migrated())


if __name__ == '__main__':
    unittest.main()
