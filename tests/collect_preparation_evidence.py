# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/collect_preparation_evidence.py
Purpose: Capture reproducible local evidence for layout and source enrichment.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Self-evaluation only; does not approve a CLI gate or freeze an oracle.
Related decision: DEV-2026-11-19-003.
"""
from copy import deepcopy
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import hashlib
import json
import os
import platform
import re
import runpy
import subprocess
import sys
import unittest
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidence/reorganization-2026-11-19'


def check_navigation():
    """Purpose: Verify browsing links. Design: Exclude fenced code and copied manual. Workflow: Collection. Data Handoff: Counts/errors."""
    checked = 0
    documents = 0
    errors = []
    manual = ROOT / 'hardware/controllers/arduino/ventuno_q/sources/user_manual.md'
    for page in sorted(ROOT.rglob('*.md')):
        if page == manual:
            continue
        documents += 1
        text = re.sub(r'```.*?```', '', page.read_text(encoding='utf-8'), flags=re.S)
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if link.startswith(('https://', 'http://', 'mailto:')):
                continue
            relative, _, anchor = unquote(link).partition('#')
            target = (page.parent / relative).resolve() if relative else page
            checked += 1
            if not target.is_file() or not target.is_relative_to(ROOT):
                errors.append(f'{page.relative_to(ROOT)} -> {link}')
            elif anchor:
                body = target.read_text(encoding='utf-8')
                headings = re.findall(r'^#{1,6}\s+(.+)$', body, re.M)
                slugs = {re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-') for heading in headings}
                if anchor not in slugs:
                    errors.append(f'{page.relative_to(ROOT)} -> missing fragment {link}')
    return {'documents': documents, 'local_links_and_fragments': checked, 'errors': errors, 'excluded_source_snapshot': str(manual.relative_to(ROOT))}


def corruption_checks():
    """Purpose: Demonstrate useful failures. Design: In-memory fault injection, no file edits. Workflow: Collection. Data Handoff: Observations."""
    namespace = runpy.run_path(str(ROOT / 'tests/test_repository_content.py'))
    test_class = namespace['RepositoryContentTests']
    original = namespace['read_board']()
    cases = []
    variants = []
    broken = deepcopy(original)
    del broken['onboard_components']['ata6563']
    variants.append(('missing_can_transceiver', 'test_inventory_comes_from_manual', broken))
    broken = deepcopy(original)
    broken['connections']['can_bus_path']['via'] = ['component:qca8081']
    variants.append(('wrong_can_intermediary', 'test_relationships_resolve', broken))
    broken = deepcopy(original)
    broken['resource_conflicts']['jhat_bluetooth_uart']['affected_pins'].pop()
    variants.append(('missing_bluetooth_conflict_pin', 'test_resource_and_power_constraints', broken))
    broken = deepcopy(original)
    broken['pin_map']['D0']['source_refs'] = ['nonexistent_section']
    variants.append(('dangling_section_reference', 'test_source_sections_and_conflicts', broken))
    for name, method, data in variants:
        stream = StringIO()
        globals_map = getattr(test_class, method).__globals__
        with patch.dict(globals_map, {'read_board': lambda: data}):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.TestSuite([test_class(method)]))
        cases.append({'case': name, 'detected': len(result.failures) == 1 and not result.errors, 'mechanism': 'in_memory_fault_injection_into_test_input', 'raw_report': stream.getvalue()})
    changed = deepcopy(original)
    changed['pin_map']['JOMEGA_100']['source_function'] = 'PF6'
    expected = namespace['BASELINE']['definitions']['hardware/controllers/arduino/ventuno_q/definition.yml']
    try:
        namespace['assert_preserved'](unittest.TestCase(), expected, {'arduino_ventuno_q': changed})
    except AssertionError as error:
        cases.append({'case': 'wrong_expansion_pin_function_with_same_pin_count', 'detected': True, 'mechanism': 'independent_original_field_tree_comparison', 'raw_report': str(error)})
    else:
        cases.append({'case': 'wrong_expansion_pin_function_with_same_pin_count', 'detected': False})
    return cases


def renderer_checks():
    """Purpose: Check rendering boundaries. Design: Deliberately invalid data. Workflow: Collection. Data Handoff: Static test observations."""
    renderer = runpy.run_path(str(ROOT / 'src/ysl_components/reference_pages.py'))
    escaped = renderer['cell']('<script>alert(1)</script>|[label]`')
    escaping = '<script>' not in escaped and '|' not in escaped and '[' not in escaped and '`' not in escaped
    rejected = False
    try:
        yaml.load('pin: first\npin: second\n', Loader=renderer['UniqueKeyLoader'])
    except ValueError:
        rejected = True
    return {'markup_escaped': escaping, 'duplicate_yaml_key_rejected': rejected}


def main():
    """Purpose: Collect local evidence. Design: Capture subprocess truth and hashes. Workflow: Direct script. Data Handoff: Files/status."""
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, env=environment)
    (EVIDENCE / 'after.stdout.txt').write_bytes(result.stdout)
    (EVIDENCE / 'after.stderr.txt').write_bytes(result.stderr)
    (EVIDENCE / 'after.exit-code.txt').write_text(str(result.returncode) + '\n', encoding='utf-8')
    navigation = check_navigation()
    corruptions = corruption_checks()
    rendering = renderer_checks()
    report = {'evaluation': 'local_self_evaluation_not_independent_gate_approval', 'utc_time': datetime.now(timezone.utc).isoformat(), 'command': command, 'working_directory': str(ROOT), 'platform': platform.platform(), 'python': sys.version, 'pyyaml': yaml.__version__, 'unittest_exit_code': result.returncode, 'navigation': navigation, 'corruption_checks': corruptions, 'renderer_checks': rendering, 'hardware_verification': 'not_bench_tested'}
    (EVIDENCE / 'checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    files = {}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in {'.git', '.venv', '__pycache__'} for part in path.relative_to(ROOT).parts):
            continue
        if path.name == 'manifest.json' or path == ROOT / 'DEVNOTES.md' or path == ROOT / 'TEST_LOG.md':
            continue
        files[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = {'status': 'self_evaluated_not_a_signature_or_human_approval', 'files': files, 'exclusions': ['manifest.json', 'DEVNOTES.md', 'TEST_LOG.md', '.git/', '.venv/', '__pycache__/']}
    (EVIDENCE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    success = result.returncode == 0 and not navigation['errors'] and all(case['detected'] for case in corruptions) and all(rendering.values())
    print(f'Unit test exit code: {result.returncode}')
    print(f'Navigation: {navigation["local_links_and_fragments"]} local links/fragments, {len(navigation["errors"])} errors')
    for error in navigation['errors']:
        print(error)
    print(f'Deliberate corruptions detected: {sum(case["detected"] for case in corruptions)}/{len(corruptions)}')
    print(f'Renderer checks: {rendering}')
    print(f'Manifest: {len(files)} file digests; local self-evaluation only')
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
