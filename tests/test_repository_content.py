# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/test_repository_content.py
Purpose: Check the requested layout, hardware enrichment, and generated references.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Local self-evaluation, not the independent CLI acceptance suite.
Related decision: DEV-2026-11-19-003.
"""
from pathlib import Path
import hashlib
import json
import re
import runpy
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = json.loads((ROOT / 'docs/evidence/migration-2026-11-19/baseline.json').read_text(encoding='utf-8'))
SNAPSHOTS = {item['path']: item['snapshot'] for item in MIGRATION['definitions'].values()}
BASELINE = json.loads((ROOT / 'docs/evidence/reorganization-2026-11-19/baseline.json').read_text(encoding='utf-8'))
VENTUNO = ROOT / 'hardware/controllers/arduino/ventuno_q/definition.yml'
MANUAL = 'hardware/controllers/arduino/ventuno_q/sources/user_manual.md'


def matches_recorded_digest(path, digest):
    """Purpose: Compare relocated bytes with the preparation digest.
    Design: Accept the recorded LF digest or its CRLF translation. See DEV-2026-11-19-007.
    Workflow: Layout preservation. Data Handoff: Boolean.
    """
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() == digest:
        return True
    if b'\r' not in data:
        return hashlib.sha256(data.replace(b'\n', b'\r\n')).hexdigest() == digest
    return False


def read_board():
    """Purpose: Load the candidate. Design: Read YAML only. Workflow: Tests. Data Handoff: Board mapping."""
    return yaml.safe_load(VENTUNO.read_text(encoding='utf-8'))


def assert_preserved(case, original, current, location=''):
    """Purpose: Detect loss. Design: Compare old leaves independently. Workflow: Migration test. Data Handoff: Assertions."""
    if isinstance(original, dict):
        for key, value in original.items():
            case.assertIn(key, current, location)
            assert_preserved(case, value, current[key], f'{location}/{key}')
    elif isinstance(original, list):
        case.assertEqual(len(original), len(current), location)
        for index, value in enumerate(original):
            assert_preserved(case, value, current[index], f'{location}/{index}')
    else:
        if original == 'controllers/arduino/md/arduino_ventuno_q.md':
            original = MANUAL
        case.assertEqual(original, current, location)


class RepositoryContentTests(unittest.TestCase):
    """Purpose: Verify preparation work. Design: Source-based oracles. Workflow: unittest. Data Handoff: Failures/evidence."""

    def test_layout_and_legacy_preservation(self):
        """Purpose: Detect missing moves/loss. Design: Frozen baseline. Workflow: Test run. Data Handoff: Assertions."""
        self.assertEqual(len(list((ROOT / 'hardware').rglob('definition.yml'))), 5)
        for record in BASELINE['files']:
            new = ROOT / record['new_path']
            self.assertTrue(new.is_file(), str(new))
            self.assertFalse((ROOT / record['old_path']).exists(), record['old_path'])
            if record['old_path'].endswith('_STANDARDS.md') or record['new_path'].endswith('user_manual.md') or (record['old_path'].endswith('.yml') and 'ventuno' not in record['old_path']):
                self.assertTrue(matches_recorded_digest(ROOT / SNAPSHOTS.get(record['new_path'], record['new_path']), record['sha256']))
        for path, original in BASELINE['definitions'].items():
            assert_preserved(self, original, yaml.safe_load((ROOT / SNAPSHOTS[path]).read_text(encoding='utf-8-sig')))

    def test_journal_history_is_unchanged(self):
        """Purpose: Preserve history. Design: Prefix hashes. Workflow: After append. Data Handoff: Assertions."""
        for name, record in BASELINE['journals'].items():
            prefix = (ROOT / name).read_bytes()[:record['byte_length']]
            self.assertEqual(hashlib.sha256(prefix).hexdigest(), record['sha256'])

    def test_inventory_comes_from_manual(self):
        """Purpose: Check component claims. Design: Exact source tokens. Workflow: Enrichment test. Data Handoff: Assertions."""
        board = read_board()
        manual = (ROOT / MANUAL).read_text(encoding='utf-8')
        required = {'ATA6563', 'MAX98091', 'TUSB7340', 'QCA-8081', 'NFA725B', 'TRJT9010A98NL', 'RCLAMP0524TCT', 'DF2B7ASL,L3F'}
        parts = {item.get('model') for item in board['onboard_components'].values()}
        self.assertTrue(required.issubset(parts))
        for part in required:
            self.assertIn(part, manual)
        translator = board['onboard_components']['jhat_level_translation']
        self.assertNotIn('model', translator)
        self.assertEqual(translator['facts']['identification']['value'], 'unspecified_in_manual')

    def test_source_sections_and_conflicts(self):
        """Purpose: Check provenance. Design: Resolve all local citations. Workflow: Enrichment test. Data Handoff: Assertions."""
        board = read_board()
        refs = board['sources']
        headings = set(re.findall(r'^#{1,6} (.+)$', (ROOT / MANUAL).read_text(encoding='utf-8'), re.M))
        for record in refs.values():
            if 'section' in record:
                self.assertEqual(record['path'], MANUAL)
                self.assertEqual(record['snapshot_date'], '2026-11-19')
                self.assertIn(record['section'], headings)
        def walk(node):
            """Purpose: Find citations. Design: Recursive data traversal. Workflow: Provenance test. Data Handoff: Assertions."""
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == 'source_refs':
                        self.assertTrue(value)
                        self.assertTrue(set(value).issubset(refs), value)
                    else:
                        walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)
        walk(board)
        self.assertTrue(all(pin['provenance'].get('source_refs') for pin in board['pins'].values()))
        self.assertEqual(len([item for item in board['constraints'].values() if item['kind'] == 'source_conflict']), 6)
        self.assertEqual(board['features']['wireless']['facts']['bluetooth_version']['status'], 'conflicting')

    def test_relationships_resolve(self):
        """Purpose: Catch dangling graph edges. Design: Typed reference namespaces. Workflow: Enrichment test. Data Handoff: Assertions."""
        board = read_board()
        entities = {'processor': board['board']['processors'], 'component': board['onboard_components'], 'connector': board['connectors'], 'interface': board['interfaces'], 'pin': board['pins']}
        for edge in board['connections'].values():
            for reference in [edge['from'], edge['to'], *edge.get('via', [])]:
                namespace, key = reference.split(':', 1)
                self.assertIn(key, entities[namespace], reference)
        can = board['connections']['can_bus_path']
        self.assertEqual(can['from'], 'processor:mcu')
        self.assertEqual(can['to'], 'connector:CAN_SCREW_TERMINAL')
        self.assertEqual(can['via'], ['component:ata6563'])
        self.assertEqual(can['routing_status'], 'conflicting')
        self.assertIn('unresolved', can['notes'])
        self.assertEqual(board['connections']['jhat_path']['via'], ['component:jhat_level_translation'])

    def test_resource_and_power_constraints(self):
        """Purpose: Preserve critical restrictions. Design: Manual-specific expected facts. Workflow: Enrichment test. Data Handoff: Assertions."""
        board = read_board()
        bluetooth = board['resource_conflicts']['jhat_bluetooth_uart']
        self.assertEqual(bluetooth['affected_pins'], ['JHAT_8', 'JHAT_10', 'JHAT_11', 'JHAT_36'])
        self.assertEqual(bluetooth['policy'], 'unavailable_when')
        self.assertEqual(board['resource_conflicts']['display_output_mux']['participants'], ['connector:HDMI', 'interface:JMEDIA_MIPI_DSI'])
        power = board['power_domains']
        self.assertEqual(power['limited_outputs']['facts']['stated_current_limit_a']['value']['value'], 2.8)
        self.assertEqual(set(power['carrier_outputs_outside_limited_nets']['feeds']), {'connector:JMEDIA', 'connector:JMISC', 'connector:JOMEGA'})
        self.assertNotIn('max_current_a', power['carrier_outputs_outside_limited_nets'])
        for input_id in ('usb_c_pd_input', 'barrel_jack_input', 'screw_terminal_input', 'uno_vin_input'):
            self.assertIn(input_id, power)
        self.assertEqual(power['uno_vin_input']['facts']['ptc_fuse_rating_a']['value']['value'], 1.1)
        self.assertEqual(power['rtc_backup']['facts']['max_voltage_v']['value']['max'], 3.3)

    def test_deterministic_generated_pages(self):
        """Purpose: Detect stale references. Design: Rebuild in memory. Workflow: After generation. Data Handoff: Assertions."""
        renderer = runpy.run_path(str(ROOT / 'src/ysl_components/reference_pages.py'))
        first = renderer['build_pages'](ROOT)
        self.assertEqual(first, renderer['build_pages'](ROOT))
        self.assertEqual(len(first), 6)
        for relative, content in first.items():
            self.assertEqual((ROOT / relative).read_text(encoding='utf-8'), content, relative)
        page = first['hardware/controllers/arduino/ventuno_q/README.md']
        for fact in ('ATA6563', 'JOMEGA_100', 'PB5', '2.8', 'jhat_bluetooth_uart', 'display_output_mux', 'Bluetooth', 'can_pd0_pd1'):
            self.assertIn(fact, page)

    def test_packaging_metadata_matches_the_catalog_approval(self):
        """Purpose: Keep the package declaration on the widened G4 scope.
        Design: Metadata may exist. Schema bytes and publication stay closed.
        Workflow: Test run. Data Handoff: Assertions.
        """
        import tomllib
        project = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))
        self.assertEqual(project['project']['name'], 'ysl-components')
        self.assertEqual(project['project']['version'], '1.0.0a1')
        self.assertEqual(project['project']['scripts']['ysl-components'], 'ysl_components.cli:installed_main')
        tool = project['tool']['ysl_component_library']
        self.assertTrue(tool['packaging_enabled'])
        self.assertFalse(tool['publish_authorized'])
        self.assertEqual(tool['approved_candidate'], 'bbf013354b3ac7d4fdc9be8b44090634b431b118')
        schema = json.loads((ROOT / 'schemas/component.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(schema['x-ysl-review-status'], 'draft-not-approved')
        self.assertEqual(schema['properties']['schema_version']['const'], '1.0.0-draft.1')
        self.assertFalse((ROOT / 'dist').exists())


if __name__ == '__main__':
    unittest.main()
