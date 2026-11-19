# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/collect_page_evidence.py
Purpose: Capture the P4 page run, fact and link checks, views, and packaging denial.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Local self-evaluation only. Does not approve G4 or invoke a package builder.
Related decision: DEV-2026-11-19-009.
"""

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import html
import importlib.metadata
import json
import os
import platform
import re
import runpy
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'docs/evidence/pages-2026-11-19'
VIEWS = FOLDER / 'views'


def load(relative):
    """Purpose: Load a local tool by path. Design: Avoid package installation.
    Workflow: Collection. Data Handoff: Module namespace.
    """
    return runpy.run_path(str(ROOT / relative))


def write_json(path, payload):
    """Purpose: Store one report. Design: Stable indentation. Workflow: Evidence files.
    Data Handoff: The written path.
    """
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    return path


def excerpt(text, start, end, start_after=None, limit=None):
    """Purpose: Copy one generated region. Design: Headings are exact lines. start_after skips an earlier copy of the same heading.
    Workflow: Review views. Data Handoff: Markdown excerpt.
    """
    lines = text.splitlines()
    origin = 0
    if start_after:
        origin = next(index for index, line in enumerate(lines) if line == start_after) + 1
    begin = next(index for index, line in enumerate(lines) if index >= origin and line == start)
    finish = next(index for index, line in enumerate(lines) if index > begin and line == end)
    chosen = lines[begin:finish]
    if limit is not None:
        chosen = chosen[:limit]
    return '\n'.join(chosen) + '\n'


def inline(text):
    """Purpose: Show Markdown emphasis as text. Design: Drop link targets before escaping.
    Workflow: HTML views. Data Handoff: Safe HTML.
    """
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    return html.escape(text)


def markdown_html(title, markdown):
    """Purpose: Render a review view. Design: Headings, paragraphs, and tables only.
    Workflow: Screenshots. Data Handoff: An HTML document.
    """
    lines = markdown.splitlines()
    parts = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('|'):
            rows = []
            while index < len(lines) and lines[index].startswith('|'):
                rows.append([cell.strip() for cell in lines[index].strip('|').split('|')])
                index += 1
            body_rows = [row for row in rows if not all(set(cell) <= set('-: ') and cell for cell in row)]
            if not body_rows:
                continue
            header, *rest = body_rows
            rendered = ['<table><thead><tr>']
            rendered.extend(f'<th>{inline(cell)}</th>' for cell in header)
            rendered.append('</tr></thead><tbody>')
            for row in rest:
                rendered.append('<tr>' + ''.join(f'<td>{inline(cell)}</td>' for cell in row) + '</tr>')
            rendered.append('</tbody></table>')
            parts.append(''.join(rendered))
            continue
        if line.startswith('#'):
            level = min(len(line) - len(line.lstrip('#')), 6)
            parts.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
        elif line.startswith('<!--'):
            parts.append(f'<p class="marker">{inline(line)}</p>')
        elif line.strip():
            parts.append(f'<p>{inline(line)}</p>')
        index += 1
    style = (
        'body{font:16px/1.45 Georgia,serif;margin:24px;color:#1c1c1c;background:#fff}'
        'table{border-collapse:collapse;width:100%;margin:12px 0}'
        'th,td{border:1px solid #bbb;padding:4px 6px;vertical-align:top;font:13px/1.35 ui-sans-serif,sans-serif}'
        'th{background:#f3f1ea;text-align:left}.marker{color:#555;font:12px ui-sans-serif,sans-serif}'
    )
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<title>{html.escape(title)}</title><style>{style}</style></head><body>'
        f'<h1>{html.escape(title)}</h1>{"".join(parts)}</body></html>'
    )


def screenshot(html_path, png_path, width, height):
    """Purpose: Capture one rendered view. Design: Kill Chrome after the PNG exists.
    Headless Chrome in this environment does not exit on its own. Workflow: View capture.
    Data Handoff: PNG bytes, or an error string.
    """
    command = [
        'google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
        '--hide-scrollbars', f'--window-size={width},{height}', f'--screenshot={png_path}', html_path.as_uri(),
    ]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    error = 'screenshot was not written'
    try:
        for _ in range(100):
            if png_path.is_file() and png_path.stat().st_size > 1000 and png_path.read_bytes().startswith(b'\x89PNG'):
                error = ''
                break
            if process.poll() is not None:
                error = f'chrome exited {process.returncode} before writing a PNG'
                break
            subprocess.run(['sleep', '0.1'], check=False)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
    return error


def packaging_cases():
    """Purpose: Exercise every denial reason. Design: A builder that would write a file must not be called.
    Workflow: AC-501. Data Handoff: The observed reasons.
    """
    packaging = load('src/ysl_components/packaging.py')
    digest = 'candidate-under-review'
    called = []

    def builder(path):
        called.append(path)
        Path(path).write_text('wheel', encoding='utf-8')

    requests = [
        (None, 'approval_absent'),
        ({'approved': True}, 'local_approval_is_not_authorization'),
        ({'approved': True, 'gate': 'G4', 'candidate': digest, 'channel': 'repository'}, 'local_approval_is_not_authorization'),
        ({'approved': True, 'gate': 'G3', 'candidate': digest, 'channel': 'external'}, 'wrong_gate'),
        ({'approved': True, 'gate': 'G4', 'candidate': 'other-candidate', 'channel': 'external'}, 'candidate_mismatch'),
        ({'approved': True, 'gate': 'G4', 'candidate': digest, 'channel': 'external'}, 'candidate_not_approved'),
    ]
    observed = []
    for approval, expected in requests:
        result = packaging['request_package_build'](approval, digest, builder=builder)
        observed.append({'expected_reason': expected, 'result': result})
    return {'builder_called': called, 'cases': observed, 'dist_exists': (ROOT / 'dist').exists()}


def tamper_demo():
    """Purpose: Show the manifest verifier on a disposable copy. Design: Do not alter the real bundle.
    Workflow: AC-405. Data Handoff: Missing and changed observations.
    """
    checks = load('tests/page_checks.py')
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        (root / 'report.txt').write_text('page evidence\n', encoding='utf-8')
        manifest = checks['build_manifest'](root, ['report.txt'])
        clean = checks['verify_manifest'](root, manifest)
        (root / 'report.txt').unlink()
        missing = checks['verify_manifest'](root, manifest)
        (root / 'report.txt').write_text('altered\n', encoding='utf-8')
        changed = checks['verify_manifest'](root, manifest)
    return {'clean': clean, 'missing': missing, 'changed': changed}


def navigation():
    """Purpose: Reuse the repository link scan. Design: The manual snapshot stays excluded.
    Workflow: Evidence. Data Handoff: Navigation counts and errors.
    """
    return load('tests/collect_preparation_evidence.py')['check_navigation']()


def main():
    """Purpose: Write the P4 evidence bundle. Design: Tests run as a subprocess. Manifest is last.
    Workflow: python -B tests/collect_page_evidence.py. Data Handoff: Process exit code.
    """
    if sys.flags.optimize:
        raise SystemExit('Refusing optimized evidence collection')
    FOLDER.mkdir(parents=True, exist_ok=True)
    VIEWS.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    (FOLDER / 'after.stdout.txt').write_text(completed.stdout, encoding='utf-8')
    (FOLDER / 'after.stderr.txt').write_text(completed.stderr, encoding='utf-8')
    (FOLDER / 'after.exit-code.txt').write_text(str(completed.returncode) + '\n', encoding='utf-8')

    checks = load('tests/page_checks.py')
    renderer = load('src/ysl_components/reference_pages.py')
    pages = {relative: (ROOT / relative).read_text(encoding='utf-8') for relative in checks['GENERATED_PAGES']}
    generated = renderer['build_pages'](ROOT)
    generated_again = renderer['build_pages'](ROOT)
    fact_errors = checks['check_fact_oracle'](pages)
    link_errors = checks['check_local_links'](ROOT, pages)
    image_errors = checks['missing_generated_images'](ROOT, pages)
    limitations = checks['inventory_manual_images'](ROOT)
    denial = packaging_cases()
    tamper = tamper_demo()
    page_digests = {relative: hashlib.sha256(content.encode('utf-8')).hexdigest() for relative, content in generated.items()}
    determinism = {
        'repository_generations_match': generated == generated_again,
        'repository_files_match_generator': pages == generated,
        'page_sha256': page_digests,
    }
    write_json(FOLDER / 'fact-report.json', {'errors': fact_errors})
    write_json(FOLDER / 'source-limitations.json', limitations)
    write_json(FOLDER / 'packaging-denial.json', denial)
    write_json(FOLDER / 'tamper-demo.json', tamper)
    write_json(FOLDER / 'determinism.json', determinism)

    catalog = pages['docs/catalog.md']
    ventuno = pages['hardware/controllers/arduino/ventuno_q/README.md']
    attiny = pages['hardware/controllers/microchip/attiny_x5/README.md']
    pin_view = excerpt(ventuno, '### JDIGITAL', '### JHAT', start_after='## Pin tables', limit=36)
    conflict_view = (
        excerpt(ventuno, '## Resource conflicts', '## Power and electrical summary')
        + '\n'
        + excerpt(ventuno, '## Constraints and known issues', '### resource_context__jhat_bluetooth_uart')
    )
    attiny_view = excerpt(attiny, '## Variants', '## Power and electrical summary')
    view_sources = {
        'catalog': catalog,
        'ventuno-d5-pins': pin_view,
        'ventuno-conflicts': conflict_view,
        'attiny-family': attiny_view,
    }
    screenshot_errors = {}
    heights = {'catalog': 1100, 'ventuno-d5-pins': 1400, 'ventuno-conflicts': 2200, 'attiny-family': 1800}
    for name, content in view_sources.items():
        (VIEWS / f'{name}.md').write_text(
            f'Excerpt of generated Markdown for review. The generated page is authoritative.\n\n```markdown\n{content}```\n',
            encoding='utf-8',
        )
        html_path = VIEWS / f'{name}.html'
        png_path = VIEWS / f'{name}.png'
        html_path.write_text(markdown_html(name, content), encoding='utf-8')
        screenshot_errors[name] = screenshot(html_path, png_path, 1200, heights[name])

    write_json(FOLDER / 'link-report.json', {'status': 'pending_navigation'})
    write_json(FOLDER / 'checks.json', {'status': 'pending_navigation'})
    write_json(FOLDER / 'manifest.json', {'status': 'pending_finalization'})
    nav = navigation()
    write_json(FOLDER / 'link-report.json', {
        'generated_page_errors': link_errors,
        'generated_image_errors': image_errors,
        'repository_navigation': nav,
    })
    denial_ok = (
        denial['builder_called'] == []
        and not denial['dist_exists']
        and all(item['result']['reason'] == item['expected_reason'] and item['result']['built'] is False for item in denial['cases'])
    )
    tamper_ok = tamper['clean'] == [] and tamper['missing'][0]['problem'] == 'missing' and tamper['changed'][0]['problem'] == 'changed'
    screenshots_ok = not any(screenshot_errors.values())
    success = (
        completed.returncode == 0
        and not fact_errors
        and not link_errors
        and not image_errors
        and not nav['errors']
        and determinism['repository_generations_match']
        and determinism['repository_files_match_generator']
        and denial_ok
        and tamper_ok
        and screenshots_ok
        and limitations['missing']
        and not limitations['present']
    )
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
    report = {
        'status': 'self_evaluated_P4_candidate_G4_not_approved',
        'utc_time': datetime.now(timezone.utc).isoformat(),
        'command': 'python -B tests/collect_page_evidence.py',
        'candidate_head': head,
        'candidate_status_porcelain': status,
        'platform': platform.platform(),
        'python': sys.version,
        'dependencies': {name: importlib.metadata.version(name) for name in ('PyYAML', 'jsonschema', 'referencing')},
        'unittest_exit_code': completed.returncode,
        'fact_errors': fact_errors,
        'generated_link_errors': link_errors,
        'generated_image_errors': image_errors,
        'navigation_errors': nav['errors'],
        'navigation_counts': {'documents': nav['documents'], 'local_links_and_fragments': nav['local_links_and_fragments']},
        'manual_images_missing': len(limitations['missing']),
        'manual_images_present': len(limitations['present']),
        'determinism_match': determinism['repository_generations_match'] and determinism['repository_files_match_generator'],
        'packaging_denial_ok': denial_ok,
        'tamper_demo_ok': tamper_ok,
        'screenshot_errors': screenshot_errors,
        'limitations': [
            'Linux only. Windows was not executed.',
            'No independent reviewer reproduced this run.',
            'Six VENTUNO discrepancies remain unresolved.',
            'Physical verification remains not_verified.',
            'Manual images listed in source-limitations.json are absent.',
            'Packaging was denied and no distribution was produced.',
            'G4 is not approved.',
        ],
        'exit_code': 0 if success else 1,
    }
    write_json(FOLDER / 'checks.json', report)
    files = {}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in {'.git', '.venv', '__pycache__'} for part in path.relative_to(ROOT).parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in {'DEVNOTES.md', 'TEST_LOG.md', 'docs/evidence/pages-2026-11-19/manifest.json'}:
            continue
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(FOLDER / 'manifest.json', {
        'status': 'local_file_inventory_not_an_approval_or_signature',
        'candidate_head': head,
        'files': files,
        'exclusions': ['DEVNOTES.md', 'TEST_LOG.md', 'this manifest', '.git/', '.venv/', '__pycache__/'],
    })
    manifest = json.loads((FOLDER / 'manifest.json').read_text(encoding='utf-8'))
    problems = checks['verify_manifest'](ROOT, manifest)
    print(f'unittest exit {completed.returncode}; fact errors {len(fact_errors)}; link errors {len(link_errors)}; navigation errors {len(nav["errors"])}.')
    print(f'manual images missing {len(limitations["missing"])}; packaging denial ok {denial_ok}; tamper ok {tamper_ok}.')
    print(f'screenshot errors {screenshot_errors}; manifest problems {len(problems)}; collector exit {report["exit_code"]}.')
    if problems:
        print(problems[:5])
        return 1
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
