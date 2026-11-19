# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/collect_migration_evidence.py
Purpose: Capture P2 tests, preservation results, corruption observations, and navigation.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Local self-evaluation only; no human G2 approval or packaging authority.
Related decision: DEV-2026-11-19-005.
"""
from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import hashlib
import importlib.metadata
import json
import os
import platform
import runpy
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'docs/evidence/migration-2026-11-19'


def main():
    """Purpose: Record actual execution. Design: Reuse runner events, not converter expectations. Workflow: Script. Data Handoff: Reports and exit status."""
    if sys.flags.optimize:
        raise SystemExit('Refusing optimized evidence collection')
    os.chdir(ROOT)
    result_class = runpy.run_path(str(ROOT / 'tests/collect_schema_review_evidence.py'))['ReviewResult']
    suite = unittest.defaultTestLoader.discover('tests')
    collected = suite.countTestCases()
    stdout, stderr = StringIO(), StringIO()
    with redirect_stdout(stdout):
        result = unittest.TextTestRunner(stream=stderr, verbosity=2, resultclass=result_class).run(suite)
    (FOLDER / 'after.stdout.txt').write_text(stdout.getvalue(), encoding='utf-8')
    (FOLDER / 'after.stderr.txt').write_text(stderr.getvalue(), encoding='utf-8')
    for filename in ('checks.json', 'manifest.json'):
        (FOLDER / filename).write_text(json.dumps({'status': 'pending_finalization', 'exit_code': 1}) + '\n', encoding='utf-8')
    (FOLDER / 'after.exit-code.txt').write_text('1\n', encoding='utf-8')
    navigation = runpy.run_path(str(ROOT / 'tests/collect_preparation_evidence.py'))['check_navigation']()
    migration_passed = [name for name in result.passed if '.MigrationTests.' in name]
    mutations = [item for item in result.subcases if 'test_required_deliberate_corruptions_are_detected' in item['test']]
    maps = json.loads((FOLDER / 'field-map.json').read_text(encoding='utf-8'))
    summary = {identity: {'original_fields': len(mapping['fields']), 'generated_fields': len(mapping['generated_fields'])} for identity, mapping in maps.items()}
    # Read actual per-ID pin counts, independent of registry iteration order.
    import yaml
    baseline = json.loads((FOLDER / 'baseline.json').read_text(encoding='utf-8'))
    for identity, item in baseline['definitions'].items():
        summary[identity]['pin_records'] = len(yaml.safe_load((ROOT / item['path']).read_text(encoding='utf-8'))['pins'])
    success = result.wasSuccessful() and collected >= 22 and len(migration_passed) == 7 and len(mutations) == 6 and all(item['success'] for item in mutations) and not result.skipped and not navigation['errors']
    report = {'status': 'self_evaluated_P2_candidate_G2_review_pending', 'utc_time': datetime.now(timezone.utc).isoformat(), 'command': 'python -B tests/collect_migration_evidence.py', 'platform': platform.platform(), 'python': sys.version, 'dependencies': {name: importlib.metadata.version(name) for name in ('PyYAML', 'jsonschema', 'referencing')}, 'collected': collected, 'executed': result.testsRun, 'passed': result.passed, 'migration_methods_passed': migration_passed, 'subcases': result.subcases, 'mutation_cases': mutations, 'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped), 'components': summary, 'original_fields': sum(item['original_fields'] for item in summary.values()), 'pin_records': sum(item['pin_records'] for item in summary.values()), 'navigation': navigation, 'exit_code': 0 if success else 1}
    (FOLDER / 'checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (FOLDER / 'after.exit-code.txt').write_text(str(report['exit_code']) + '\n', encoding='utf-8')
    files = {}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in {'.git', '.venv', '__pycache__'} for part in path.relative_to(ROOT).parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in ('DEVNOTES.md', 'TEST_LOG.md', 'docs/evidence/migration-2026-11-19/manifest.json'):
            continue
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    (FOLDER / 'manifest.json').write_text(json.dumps({'status': 'local_file_inventory_not_an_approval_or_signature', 'files': files, 'exclusions': ['DEVNOTES.md', 'TEST_LOG.md', 'this manifest', '.git/', '.venv/', '__pycache__/']}, indent=2) + '\n', encoding='utf-8')
    print(f'{result.testsRun}/{collected} methods; {len(migration_passed)} migration methods; {len(mutations)}/6 corruptions detected; {len(result.skipped)} skipped.')
    print(f'{report["original_fields"]} original fields accounted for; {report["pin_records"]} pin records; {len(summary)} schema-valid components.')
    print(f'Failures: {len(result.failures)}; errors: {len(result.errors)}; navigation errors: {len(navigation["errors"])}.')
    for error in navigation['errors']:
        print(error)
    print('P2 self-evaluation only; G2 review and CLI/packaging work remain separate.')
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
