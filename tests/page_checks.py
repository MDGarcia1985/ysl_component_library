# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/page_checks.py
Purpose: Check generated pages against the frozen fact oracle and evidence manifest.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Literals only. This module does not import the page renderer.
Related decision: DEV-2026-11-19-009.
"""

from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANUAL = 'hardware/controllers/arduino/ventuno_q/sources/user_manual.md'
GENERATED_PAGES = (
    'docs/catalog.md',
    'hardware/controllers/arduino/uno_r3/README.md',
    'hardware/controllers/arduino/ventuno_q/README.md',
    'hardware/controllers/microchip/attiny_x5/README.md',
    'hardware/drivers/ti/l293_family/README.md',
    'hardware/sensors/generic/hc_sr04/README.md',
)
CATALOG_IDS = (
    'arduino/uno-r3',
    'arduino/ventuno-q',
    'microchip/attiny-x5',
    'ti/l293-family',
    'generic/hc-sr04',
)
CONFLICT_TOPICS = (
    'qwiic_controller',
    'can_pd0_pd1',
    'bluetooth_version',
    'isp_model',
    'wifi_band_description',
    'pwm_example_range',
)
FAMILY_SELECTORS = ('ATtiny25', 'ATtiny45', 'ATtiny85', 'ATtiny25V', 'ATtiny45V', 'ATtiny85V')


def digest_bytes(data):
    """Purpose: Name evidence bytes. Design: SHA-256 only. Workflow: Manifests. Data Handoff: Hex digest."""
    return hashlib.sha256(data).hexdigest()


def pin_row(text, pin_id):
    """Purpose: Find one pin table row. Design: Match the escaped pin id at the row start.
    Workflow: Fact oracle. Data Handoff: The row, or an empty string.
    """
    prefix = f'| {pin_id} |'
    for line in text.splitlines():
        if line.startswith(prefix):
            return line
    return ''


def heading_section(text, heading):
    """Purpose: Isolate one heading and its body. Design: Stop at the next same-or-higher heading.
    Workflow: Family and variant comparisons. Data Handoff: Section text, or an empty string.
    """
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if line == heading), None)
    if start is None:
        return ''
    level = len(heading) - len(heading.lstrip('#'))
    body = [lines[start]]
    for line in lines[start + 1:]:
        if line.startswith('#'):
            marks = len(line) - len(line.lstrip('#'))
            if marks <= level and line[marks:marks + 1] == ' ':
                break
        body.append(line)
    return '\n'.join(body)


def capability_line(text):
    """Purpose: Read the capability summary. Design: One generated line. Workflow: AC-401. Data Handoff: Line text."""
    for line in text.splitlines():
        if line.startswith('**Declared pin capabilities:**'):
            return line
    return ''


def check_fact_oracle(pages):
    """Purpose: Compare pages with the frozen literals. Design: Do not ask the renderer what it meant to write.
    Workflow: AC-401 and the wrong-fact mutation. Data Handoff: A list of observation strings. Empty means the oracle held.
    """
    errors = []

    def require(page, needle):
        if needle not in pages.get(page, ''):
            errors.append(f'{page} does not contain {needle!r}')

    catalog = pages.get('docs/catalog.md', '')
    for identity in CATALOG_IDS:
        require('docs/catalog.md', identity)
    for needle in (
        'python src/ysl_components/reference_pages.py',
        'Packaging is disabled',
        'g3-approval-2026-11-19.md',
        'authored separately',
    ):
        require('docs/catalog.md', needle)
    if '<!-- Generated from hardware/**/definition.yml. Do not edit manually. -->' not in catalog:
        errors.append('catalog is missing its generated-file marker')

    uno = 'hardware/controllers/arduino/uno_r3/README.md'
    ventuno = 'hardware/controllers/arduino/ventuno_q/README.md'
    attiny = 'hardware/controllers/microchip/attiny_x5/README.md'
    l293 = 'hardware/drivers/ti/l293_family/README.md'
    sensor = 'hardware/sensors/generic/hc_sr04/README.md'
    for page in (uno, ventuno, attiny, l293, sensor):
        text = pages.get(page, '')
        if not text.startswith('<!-- Generated from definition.yml; SHA-256:'):
            errors.append(f'{page} is missing its generated-file marker')
        if 'Do not edit manually.' not in text.splitlines()[0] if text else True:
            errors.append(f'{page} marker does not say to leave the file alone')
        require(page, 'not_verified')
        require(page, '**Verification limits:** status not_verified.')
        if not capability_line(text):
            errors.append(f'{page} has no declared pin capability line')
    uno_d5 = pin_row(pages.get(uno, ''), 'D5')
    if 'PD5' not in uno_d5:
        errors.append('Uno D5 row does not map to PD5')
    if 'PB5' in uno_d5:
        errors.append('Uno D5 row contains the VENTUNO signal PB5')
    ventuno_d5 = pin_row(pages.get(ventuno, ''), 'D5')
    if 'PB5' not in ventuno_d5:
        errors.append('VENTUNO D5 row does not map to PB5')
    if 'PD5' in ventuno_d5:
        errors.append('VENTUNO D5 row contains the Uno signal PD5')
    require(uno, 'i2c_sda')
    require(uno, 'pwm')
    require(ventuno, 'I2C3_SDA')
    require(ventuno, '2.8')
    require(ventuno, 'user_manual.md')
    for topic in CONFLICT_TOPICS:
        require(ventuno, topic)
    require(attiny, '**Family selectors:**')
    for name in FAMILY_SELECTORS:
        require(attiny, name)
    if 'pwm' not in capability_line(pages.get(uno, '')):
        errors.append('Uno capability summary does not list pwm')
    require(l293, '**Family selectors:**')
    l293_body = heading_section(pages.get(l293, ''), '### L293')
    l293d_body = heading_section(pages.get(l293, ''), '### L293D')
    if 'integrated_clamp_diodes' not in l293_body or '| no |' not in l293_body or '1.0' not in l293_body:
        errors.append('L293 section does not show continuous current 1.0 and clamp diodes no')
    if 'integrated_clamp_diodes' not in l293d_body or '| yes |' not in l293d_body or '0.6' not in l293d_body:
        errors.append('L293D section does not show continuous current 0.6 and clamp diodes yes')
    require(sensor, 'host_must_measure_echo_pulse_width')
    require(sensor, 'echo_level_shift_required_for_3v3_only_host')
    require(sensor, 'Unknown: Manufacturer not specified in the original definition.')
    return errors


def _headings(text):
    """Purpose: Collect heading fragments. Design: Same slug rule as the generator.
    Workflow: Fragment checks. Data Handoff: A set of fragments.
    """
    found = set()
    for heading in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        found.add(re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-'))
    return found


def _visible_text(text):
    """Purpose: Ignore fenced examples. Design: Drop fenced blocks before link scanning.
    Workflow: Link checks. Data Handoff: Markdown with fences removed.
    """
    return re.sub(r'```.*?```', '', text, flags=re.S)


def check_local_links(root, pages):
    """Purpose: Resolve generated links and fragments. Design: Prefer in-memory generated text over stale files.
    Workflow: AC-401 and AC-402. Data Handoff: Error strings.
    """
    root = Path(root)
    errors = []
    for relative, text in sorted(pages.items()):
        page = root / relative
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', _visible_text(text)):
            if link.startswith(('https://', 'http://', 'mailto:')):
                continue
            target_text, _, anchor = unquote(link).partition('#')
            if target_text:
                target = (page.parent / target_text).resolve()
                try:
                    target_relative = target.relative_to(root.resolve()).as_posix()
                except ValueError:
                    errors.append(f'{relative} -> {link}')
                    continue
                if target_relative in pages:
                    body = pages[target_relative]
                elif target.is_file():
                    body = target.read_text(encoding='utf-8')
                else:
                    errors.append(f'{relative} -> {link}')
                    continue
            else:
                body = text
                target_relative = relative
            if anchor and anchor not in _headings(body):
                errors.append(f'{relative} -> missing fragment {link}')
    return errors


def missing_generated_images(root, pages):
    """Purpose: Find image links in generated pages. Design: Manual images are not in this set.
    Workflow: AC-402. Data Handoff: Missing image references.
    """
    root = Path(root)
    missing = []
    for relative, text in sorted(pages.items()):
        page = root / relative
        for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https://', 'http://')):
                continue
            target = (page.parent / unquote(link).split('#', 1)[0]).resolve()
            if not target.is_file():
                missing.append(f'{relative} -> {link}')
    return missing


def inventory_manual_images(root):
    """Purpose: List manual images the repository does not contain. Design: Read the manual, not generated pages.
    Workflow: Source-limitation inventory. Data Handoff: Present and missing asset paths.
    """
    root = Path(root)
    manual = root / MANUAL
    text = manual.read_text(encoding='utf-8')
    present = []
    missing = []
    for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if link.startswith(('https://', 'http://')):
            continue
        relative = unquote(link).split('#', 1)[0]
        target = (manual.parent / relative).resolve()
        record = (manual.parent / relative).as_posix()
        if target.is_file():
            present.append(record)
        else:
            missing.append(record)
    return {'manual': MANUAL, 'present': present, 'missing': missing}


def build_manifest(root, paths):
    """Purpose: Bind evidence bytes. Design: Sorted relative paths and SHA-256. Workflow: AC-405.
    Data Handoff: A manifest mapping. The manifest file itself is not an entry.
    """
    root = Path(root)
    files = {}
    for relative in sorted(paths):
        files[relative] = digest_bytes((root / relative).read_bytes())
    return {
        'status': 'local_file_inventory_not_an_approval_or_signature',
        'files': files,
    }


def verify_manifest(root, manifest):
    """Purpose: Detect a missing or changed evidence file. Design: Re-hash every listed path.
    Workflow: AC-405. Data Handoff: Problem records. Empty means the listed files match.
    """
    root = Path(root)
    problems = []
    for relative, expected in manifest['files'].items():
        path = root / relative
        if not path.is_file():
            problems.append({'path': relative, 'problem': 'missing'})
            continue
        actual = digest_bytes(path.read_bytes())
        if actual != expected:
            problems.append({'path': relative, 'problem': 'changed', 'expected': expected, 'actual': actual})
    return problems


def write_manifest(path, manifest):
    """Purpose: Store a manifest. Design: Stable JSON. Workflow: Evidence bundle. Data Handoff: The written file."""
    Path(path).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
