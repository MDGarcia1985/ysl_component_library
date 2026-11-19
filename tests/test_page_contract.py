# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/test_page_contract.py
Purpose: Execute AC-401 through AC-405 and the AC-501 denial against the frozen page contract.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Fact literals live in page_checks.py. The renderer is loaded by path, not imported for expectations.
Related decision: DEV-2026-11-19-009.
"""

from pathlib import Path
import hashlib
import runpy
import shutil
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKS = runpy.run_path(str(ROOT / 'tests/page_checks.py'))
DEFINITIONS = (
    'hardware/controllers/arduino/uno_r3/definition.yml',
    'hardware/controllers/arduino/ventuno_q/definition.yml',
    'hardware/controllers/microchip/attiny_x5/definition.yml',
    'hardware/drivers/ti/l293_family/definition.yml',
    'hardware/sensors/generic/hc_sr04/definition.yml',
)
PAYLOAD = 'Board <script>alert(1)</script> | [click](javascript:alert(1))'
FACT_PAYLOAD = '<img src=x onerror=alert(1)> | [click](javascript:alert(1))'


def renderer():
    """Purpose: Load the generator without using its helpers as the oracle.
    Design: run_path keeps the test on the script contract. Workflow: Page cases.
    Data Handoff: The loaded module namespace.
    """
    return runpy.run_path(str(ROOT / 'src/ysl_components/reference_pages.py'))


def copy_definitions(destination):
    """Purpose: Give generation a clean catalog. Design: Copy the five definition files only.
    Workflow: AC-403. Data Handoff: The destination root.
    """
    for relative in DEFINITIONS:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return destination


class PageContractTests(unittest.TestCase):
    """Purpose: Hold the P4 cases. Design: One method per acceptance contract.
    Workflow: unittest discovery. Data Handoff: Assertions.
    """

    @classmethod
    def setUpClass(cls):
        """Purpose: Generate the repository pages once. Design: Later mutations copy the strings.
        Workflow: Class setup. Data Handoff: The in-memory page mapping.
        """
        cls.pages = renderer()['build_pages'](ROOT)

    def test_ac401_catalog_and_pages_match_the_fact_oracle(self):
        """Purpose: Require the five entries and the literal hardware facts.
        Design: The oracle does not read renderer snapshots. Workflow: AC-401.
        Data Handoff: Assertion failure text lists every missed fact.
        """
        self.assertEqual(set(self.pages), set(CHECKS['GENERATED_PAGES']))
        errors = CHECKS['check_fact_oracle'](self.pages)
        self.assertEqual(errors, [], '\n'.join(errors))
        link_errors = CHECKS['check_local_links'](ROOT, self.pages)
        self.assertEqual(link_errors, [], '\n'.join(link_errors))
        self.assertEqual(CHECKS['missing_generated_images'](ROOT, self.pages), [])
        guidance = (ROOT / 'hardware/controllers/arduino/ventuno_q/sources/README.md').read_text(encoding='utf-8')
        self.assertFalse(guidance.startswith('<!-- Generated'))
        self.assertIn('source limitations', guidance)

    def test_ac402_faults_in_generated_output_are_detected(self):
        """Purpose: Show that link, image, and fact checks notice planted faults.
        Design: Mutate copies. Leave the repository pages untouched. Workflow: AC-402.
        Data Handoff: Each planted fault produces at least one error, and the clean pages do not.
        """
        self.assertEqual(CHECKS['check_fact_oracle'](self.pages), [])
        self.assertEqual(CHECKS['check_local_links'](ROOT, self.pages), [])
        ventuno = 'hardware/controllers/arduino/ventuno_q/README.md'
        removed = dict(self.pages)
        removed[ventuno] = removed[ventuno].replace('](definition.yml)', '](missing.yml)', 1)
        self.assertTrue(CHECKS['check_local_links'](ROOT, removed))
        broken = dict(self.pages)
        broken[ventuno] = broken[ventuno].replace('user_manual.md#', 'user_manual.md#not-a-real-heading-', 1)
        self.assertTrue(any('missing fragment' in item for item in CHECKS['check_local_links'](ROOT, broken)))
        image = dict(self.pages)
        image[ventuno] += '\n![missing diagram](assets/not-a-real-page-asset.png)\n'
        self.assertTrue(CHECKS['missing_generated_images'](ROOT, image))
        wrong = dict(self.pages)
        wrong[ventuno] = wrong[ventuno].replace('PB5', 'PD5')
        fact_errors = CHECKS['check_fact_oracle'](wrong)
        self.assertTrue(any('VENTUNO D5' in item for item in fact_errors))

    def test_ac402_manual_images_stay_source_limitations(self):
        """Purpose: Keep absent manual art out of the generated-asset count.
        Design: Inventory the manual separately from generated pages. Workflow: AC-402.
        Data Handoff: The thumbnail is missing, and generated pages have no missing images.
        """
        inventory = CHECKS['inventory_manual_images'](ROOT)
        self.assertIn(
            str(ROOT / 'hardware/controllers/arduino/ventuno_q/sources/assets/thumbnail.png'),
            inventory['missing'],
        )
        self.assertGreaterEqual(len(inventory['missing']), 40)
        self.assertEqual(inventory['present'], [])
        self.assertEqual(CHECKS['missing_generated_images'](ROOT, self.pages), [])

    def test_ac403_clean_directories_match(self):
        """Purpose: Require deterministic generation. Design: Two fresh directory trees, then two repository calls.
        Workflow: AC-403. Data Handoff: Equal SHA-256 digests.
        """
        build = renderer()['build_pages']
        with tempfile.TemporaryDirectory() as first_name, tempfile.TemporaryDirectory() as second_name:
            first_pages = build(copy_definitions(Path(first_name)))
            second_pages = build(copy_definitions(Path(second_name)))
        self.assertEqual(set(first_pages), set(second_pages))
        for relative, content in first_pages.items():
            self.assertEqual(hashlib.sha256(content.encode('utf-8')).hexdigest(), hashlib.sha256(second_pages[relative].encode('utf-8')).hexdigest(), relative)
        repeat = build(ROOT)
        self.assertEqual(self.pages, repeat)

    def test_ac404_markup_in_labels_stays_data(self):
        """Purpose: Keep hostile labels from becoming markup. Design: A reviewer-shaped temporary definition.
        Workflow: AC-404. Data Handoff: Escaped text and an intact catalog table.
        """
        document = """\
schema_version: 1.0.0-draft.1
id: generic/markup-probe
name: "{name}"
category: sensors
kind: module
manufacturer:
  status: unknown
  reason: Probe only
aliases: []
verification:
  status: not_verified
facts:
  label:
    status: legacy_uncited
    value: "{fact}"
    source_refs: [src]
sources:
  src:
    title: "Source <script>alert(1)</script>"
pins: {{}}
interfaces: {{}}
connectors: {{}}
""".format(name=PAYLOAD, fact=FACT_PAYLOAD)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            definition = root / 'hardware/sensors/generic/markup_probe/definition.yml'
            definition.parent.mkdir(parents=True)
            definition.write_text(document, encoding='utf-8')
            pages = renderer()['build_pages'](root)
        combined = '\n'.join(pages.values())
        self.assertNotIn('<script>', combined)
        self.assertNotIn('<img', combined)
        self.assertNotIn('](javascript:', combined)
        self.assertIn('alert(1)', combined)
        self.assertIn('onerror=alert(1)', combined)
        self.assertIn('&#124;', combined)
        self.assertIn('&#91;', combined)
        catalog = pages['docs/catalog.md']
        table_lines = [line for line in catalog.splitlines() if line.startswith('|')]
        self.assertTrue(table_lines)
        width = table_lines[0].count('|')
        self.assertTrue(all(line.count('|') == width for line in table_lines))

    def test_ac405_manifest_detects_missing_and_changed_evidence(self):
        """Purpose: Show that the evidence manifest notices tampering.
        Design: A temporary bundle stands in for a reviewer copy. Workflow: AC-405.
        Data Handoff: A clean manifest matches, and both mutations are named.
        """
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'report.txt').write_text('candidate efbe756\nplatform linux\nresult self-evaluated\n', encoding='utf-8')
            (root / 'limits.txt').write_text('windows not executed\nno independent reviewer\nG4 not approved\n', encoding='utf-8')
            manifest = CHECKS['build_manifest'](root, ['report.txt', 'limits.txt'])
            self.assertEqual(CHECKS['verify_manifest'](root, manifest), [])
            (root / 'limits.txt').unlink()
            missing = CHECKS['verify_manifest'](root, manifest)
            self.assertEqual([item['problem'] for item in missing], ['missing'])
            (root / 'limits.txt').write_text('changed\n', encoding='utf-8')
            changed = CHECKS['verify_manifest'](root, manifest)
            self.assertEqual([item['problem'] for item in changed], ['changed'])

    def test_ac501_packaging_requests_are_denied(self):
        """Purpose: Keep packaging closed. Design: Every request shape returns a denial and the builder is not called.
        Workflow: AC-501. Data Handoff: Reason codes and an absent distribution.
        """
        packaging = runpy.run_path(str(ROOT / 'src/ysl_components/packaging.py'))
        digest = 'efbe756a74911bf1e9d468756b29c0ca8ba806ec'
        called = []

        def builder(path):
            called.append(path)
            Path(path).write_text('wheel', encoding='utf-8')

        cases = [
            (None, 'approval_absent'),
            ({'approved': True}, 'local_approval_is_not_authorization'),
            ({'approved': True, 'gate': 'G4', 'candidate': digest, 'channel': 'repository'}, 'local_approval_is_not_authorization'),
            ({'approved': True, 'gate': 'G3', 'candidate': digest, 'channel': 'external'}, 'wrong_gate'),
            ({'approved': True, 'gate': 'G4', 'candidate': 'other-candidate', 'channel': 'external'}, 'candidate_mismatch'),
            ({'approved': True, 'gate': 'G4', 'candidate': digest, 'channel': 'external'}, 'packaging_closed_until_external_g4'),
        ]
        for approval, reason in cases:
            result = packaging['request_package_build'](approval, digest, builder=builder)
            self.assertFalse(result['authorized'])
            self.assertFalse(result['built'])
            self.assertFalse(result['distribution_written'])
            self.assertEqual(result['reason'], reason)
        self.assertEqual(called, [])
        project = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))
        self.assertNotIn('build-system', project)
        self.assertNotIn('project', project)
        self.assertFalse(project['tool']['ysl_component_library']['packaging_enabled'])
        self.assertFalse((ROOT / 'dist').exists())


if __name__ == '__main__':
    unittest.main()
