# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/collect_schema_review_evidence.py
Purpose: Record schema-review outcomes without overwriting earlier phase evidence.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Local self-evaluation only; no package, catalog migration, or gate approval.
Related decision: DEV-2026-11-19-004.
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
FOLDER = ROOT / 'docs/evidence/schema-review-2026-11-19'


class ReviewResult(unittest.TextTestResult):
    """Purpose: Preserve actual observations. Design: Record unittest events. Workflow: Review collection. Data Handoff: Case/subcase records."""

    def __init__(self, *args, **kwargs):
        """Purpose: Start observation lists. Design: Retain standard runner. Workflow: Runner creation. Data Handoff: Result instance."""
        super().__init__(*args, **kwargs)
        self.passed = []
        self.subcases = []

    def addSuccess(self, test):
        """Purpose: Record executed success. Design: Use unittest callback. Workflow: Completed case. Data Handoff: ID and runner state."""
        self.passed.append(test.id())
        super().addSuccess(test)

    def addSubTest(self, test, subtest, error):
        """Purpose: Keep adversarial-case observations. Design: Capture subtest outcome. Workflow: Case execution. Data Handoff: ID/params/result."""
        self.subcases.append({'test': test.id(), 'case': str(subtest), 'success': error is None})
        super().addSubTest(test, subtest, error)


def main():
    """Purpose: Collect a reproducible review run. Design: Nonempty inventory plus raw results. Workflow: Script. Data Handoff: Evidence files/status."""
    if sys.flags.optimize:
        raise SystemExit('Refusing optimized evaluation')
    os.chdir(ROOT)
    suite = unittest.defaultTestLoader.discover('tests')
    collected = suite.countTestCases()
    raw = StringIO()
    stdout = StringIO()
    with redirect_stdout(stdout):
        result = unittest.TextTestRunner(stream=raw, verbosity=2, resultclass=ReviewResult).run(suite)
    FOLDER.mkdir(parents=True, exist_ok=True)
    (FOLDER / 'after.stdout.txt').write_text(stdout.getvalue(), encoding='utf-8')
    (FOLDER / 'after.stderr.txt').write_text(raw.getvalue(), encoding='utf-8')
    # Publish explicit pending states before checking navigation to this run's own
    # report files. A partial collector run must never leave a success claim.
    (FOLDER / 'checks.json').write_text(json.dumps({'status': 'pending_evidence_finalization', 'exit_code': 1}) + '\n', encoding='utf-8')
    (FOLDER / 'after.exit-code.txt').write_text('1\n', encoding='utf-8')
    (FOLDER / 'manifest.json').write_text(json.dumps({'status': 'pending_evidence_finalization'}) + '\n', encoding='utf-8')
    navigation = runpy.run_path(str(ROOT / 'tests/collect_preparation_evidence.py'))['check_navigation']()
    schema_passed = [name for name in result.passed if '.SchemaReviewTests.' in name]
    versions = {name: importlib.metadata.version(name) for name in ('PyYAML', 'jsonschema', 'referencing')}
    success = result.wasSuccessful() and collected >= 15 and len(schema_passed) == 7 and len(result.subcases) >= 54 and not result.skipped and not navigation['errors']
    report = {'status': 'self_evaluated_review_draft_no_gate_approval', 'utc_time': datetime.now(timezone.utc).isoformat(), 'command': 'python -B tests/collect_schema_review_evidence.py', 'python': sys.version, 'platform': platform.platform(), 'dependencies': versions, 'collected': collected, 'executed': result.testsRun, 'passed': result.passed, 'schema_review_methods_passed': schema_passed, 'subcases': result.subcases, 'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped), 'navigation': navigation, 'exit_code': 0 if success else 1}
    (FOLDER / 'checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (FOLDER / 'after.exit-code.txt').write_text(str(report['exit_code']) + '\n', encoding='utf-8')
    files = {}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in {'.git', '.venv', '__pycache__'} for part in path.relative_to(ROOT).parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in ('DEVNOTES.md', 'TEST_LOG.md', 'docs/evidence/schema-review-2026-11-19/manifest.json'):
            continue
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    (FOLDER / 'manifest.json').write_text(json.dumps({'status': 'local_digest_inventory_not_signed_or_approved', 'files': files, 'exclusions': ['DEVNOTES.md', 'TEST_LOG.md', 'this manifest', '.git/', '.venv/', '__pycache__/']}, indent=2) + '\n', encoding='utf-8')
    print(f'{result.testsRun}/{collected} methods executed; {len(schema_passed)} schema-review methods passed; {len(result.subcases)} subcases recorded; {len(result.skipped)} skipped.')
    print(f'Failures: {len(result.failures)}; errors: {len(result.errors)}; navigation errors: {len(navigation["errors"])}.')
    for error in navigation['errors']:
        print(error)
    print('Hardware/pyproject/journal-prefix preservation checked by the executed tests; no packaging or migration performed.')
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
