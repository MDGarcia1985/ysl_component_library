# Verification Record

### TEST-2026-11-19-001 — VENTUNO Q source transcription validation

**Date:** 2026-11-19  
**Time:** 05:52 America/New_York  
**Tester:** Codex  
**Level:** T0  
**Result:** STATIC_ONLY

#### Scope

Static validation of the new VENTUNO Q hardware definition against the local manual.

#### Files Under Validation

- `controllers/arduino/yaml/arduino_ventuno_q.yml`
- Existing `.yml` definitions, for duplicate-key-aware parsing only.

#### Objective

Verify that the YAML parses without duplicate keys, reproduces the complete source
pin tables, and resolves its interface pin references.

#### Preconditions

Repository root as the working directory; Python and PyYAML 6.0.2 available.
Local source: `controllers/arduino/md/arduino_ventuno_q.md`.

#### Procedure

Run the following in PowerShell from the repository root. The command is retained
here so the static checks can be repeated without adding runtime tooling.

```powershell
@'
from pathlib import Path
import re
import yaml

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        assert key not in result, f'Duplicate key {key!r}, line {key_node.start_mark.line + 1}'
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
paths = sorted(Path('.').rglob('*.yml'))
loaded = {p: yaml.load(p.read_text(encoding='utf-8-sig'), Loader=UniqueKeyLoader) for p in paths}
board = loaded[Path('controllers/arduino/yaml/arduino_ventuno_q.yml')]['arduino_ventuno_q']
pins = board['pin_map']
manual = Path(board['source']['path']).read_text(encoding='utf-8-sig')
tables = [('JHAT', '### RPi 40-Pin Header', 40), ('JMEDIA', '#### JMEDIA', 60), ('JMISC', '#### JMISC', 60), ('JOMEGA', '### JOMEGA Expansion Header', 100)]
for connector, heading, count in tables:
    section = manual.split(heading + '\n', 1)[1]
    block = re.search(r'(?m)^\|.*(?:\n\|.*)+', section).group()
    rows = [[cell.strip() for cell in line.strip('|').split('|')] for line in block.splitlines()[2:]]
    actual = {v['physical_pin']: v for v in pins.values() if v.get('connector') == connector}
    assert len(rows) == len(actual) == count
    assert set(actual) == set(range(1, count + 1))
    for label, signal, function in rows:
        pin = actual[int(label.replace('Pin', '').strip())]
        assert pin['maps_to'] == (function if signal == '-' else signal)
        if signal != '-' and function:
            assert pin['source_function'] == function
    print(f'{connector}: {count} positions match manual signal/function columns')
uno = re.search(r'(?m)^\| MCU Pin.*(?:\n\|.*)+', manual).group().splitlines()[2:]
for row in uno:
    port, labels, function = [cell.strip() for cell in row.strip('|').split('|')]
    labels = [label.strip() for label in labels.split('/')]
    number = int(labels[0][1:])
    key = f'A{number - 14}' if 14 <= number <= 19 else labels[0]
    assert pins[key]['maps_to'] == port
    assert set(labels).issubset({key, *pins[key].get('aliases', [])})
assert len(uno) == 22 and len(pins) == 288
pwm_section = manual.split('### PWM Pins\n', 1)[1].split('## Connectors & Expansion Ports', 1)[0]
pwm = set(re.findall(r'^\|\s+PB\d+\s+\|\s+(D\d+)\s+\|', pwm_section, re.M))
assert pwm == set(board['interfaces']['UNO_PWM']['pins'])
assert pwm == {key for key, pin in pins.items() if 'pwm' in pin.get('capabilities', [])}
roles = {'RX', 'TX', 'SS', 'MOSI', 'MISO', 'SCK', 'CS', 'SDA', 'SCL', 'RFR', 'CTS', 'WS', 'DATA0', 'DATA1', 'positive_input', 'negative_input', 'output', 'high', 'low'}
references = []
for interface in board['interfaces'].values():
    references.extend(value for key, value in interface.items() if key in roles)
    references.extend(interface.get('pins', []))
    references.extend(interface.get('chip_selects', []))
    references.extend(interface.get('channels', {}).values())
    if 'external_reference' in interface:
        references.append(interface['external_reference']['pin'])
assert all(ref in pins for ref in references)
assert all(pin['connector'] in board['connectors'] or pin['connector'] in {'JANALOG', 'JDIGITAL'} for pin in pins.values() if 'connector' in pin)
assert board['constraints']['multiplexing']['jhat_unavailable_while_bluetooth_active'] == ['JHAT_8', 'JHAT_10', 'JHAT_11', 'JHAT_36']
assert len(board['source']['discrepancies']) == 6
assert isinstance(board['source']['snapshot_pulled_date'], str)
assert board['connectors']['M2']['supported_form_factors'] == ['2230']
print(f'UNO: {len(uno)} pins and all 6 PWM pins match manual tables')
print(f'{len(paths)} YAML files parse with unique keys; {len(references)} interface pin references resolve')
print('Static transcription checks complete; no bench or linked-PDF verification performed')
'@ | python -
```

Manually review the processor, power, connector, analog, wireless, and constraint
sections against the corresponding local manual sections. Check that conflicting
claims remain identified and unsupported electrical limits are omitted.

#### Expected Result

All five YAML definitions parse with unique keys. The new definition contains all
22 UNO signals, all 260 numbered expansion positions, six documented PWM pins,
and valid interface pin references. Source discrepancies remain explicit.

#### Actual Result

Parsing and table comparisons completed without assertion failures. All 76
interface pin references resolved. Manual review retained the six discrepancy
notes and identified incomplete pinouts without inventing positions or limits.

#### Evidence

Executed command: PowerShell here-string piped to `python -`, as reproduced above.
Output:

```text
JHAT: 40 positions match manual signal/function columns
JMEDIA: 60 positions match manual signal/function columns
JMISC: 60 positions match manual signal/function columns
JOMEGA: 100 positions match manual signal/function columns
UNO: 22 pins and all 6 PWM pins match manual tables
5 YAML files parse with unique keys; 76 interface pin references resolve
Static transcription checks complete; no bench or linked-PDF verification performed
```

#### Failures / Observations

No static check failures. The manual contains six inconsistencies recorded in the
definition. Its local text does not provide every connector pinout or per-pin
electrical limits. No linked PDF verification or bench measurement was performed.

#### Related DEVNOTES

DEV-2026-11-19-001.

#### Related Tests

None.

#### Disposition

Static transcription validation is complete. The definition may be included in
the hardware library under DEV-2026-11-19-001. Resolve disputed or unspecified
hardware details against primary documentation before relying on those details
for connections; this record does not establish hardware operation.

---

---

### TEST-2026-11-19-002 — Catalog and CLI planning document validation

**Date:** 2026-11-19  
**Time:** 06:34 America/New_York  
**Tester:** Codex  
**Level:** T0  
**Result:** STATIC_ONLY

#### Scope

Documentation integrity and current-inventory consistency for the proposed
catalog/CLI plan. This is not execution of the proposed product acceptance suite.

#### Files Under Validation

- `README.md`
- `CONTRIBUTING.md`
- `repo_docs/CLI_IMPLEMENTATION_PLAN.md`
- `repo_docs/CLI_ACCEPTANCE_TESTS.md`
- `repo_docs/CLI_GATE_REVIEW_TEMPLATE.md`

#### Objective

Check local references, balanced code fences, unique and complete planned AC IDs,
phase/gate status, and consistency of the documented source inventory.

#### Preconditions

Repository root as working directory; Python and PyYAML available. The five
hardware definitions are read-only inputs to these documentation checks.

#### Procedure

Execute a PowerShell Python here-string using `python -` to:

1. Read the five listed documents as UTF-8 and assert balanced triple-backtick fences.
2. Extract Markdown links and assert every local target exists; for fragment links,
   check the corresponding heading slug.
3. Extract table-row AC IDs using `^\| (AC-\d{3}) \|` and require exactly the
   ranges AC-001..004, AC-101..105, AC-201..206, AC-301..308, AC-401..405,
   and AC-501..505, with no duplicates.
4. Require six P0-P5 phase headings, corresponding AC range references, the
   mandatory G4/P5 boundary, and the explicit statement that all gates are pending.
5. Parse the five current `.yml` definitions and sum entries under `pin_map`,
   `power_pins`, and `special_pins`; require 345 source pin records, matching
   the planning baseline. These include shared connections and aliases.
6. Check the new decision record states that no review gate is approved.

#### Expected Result

All documentation checks complete without assertion failures. Product acceptance
tests remain defined but unimplemented and unexecuted.

#### Actual Result

All five documents passed the stated static checks: 34 local links, 33 unique
planned acceptance contracts, six phases, five hardware definitions, and 345
source pin records. No gate approval or product test result was produced.

#### Evidence

Executed command: PowerShell here-string piped to `python -` from the repository
root. Output:

```text
Documentation checks: 5 files; 34 local links; balanced code fences.
Acceptance contracts: 33 unique planned AC IDs covering six phases; all gates pending.
Planning inventory: 5 definitions; 345 source pin records.
Product acceptance tests were not implemented or executed.
```

#### Failures / Observations

No documentation check failures. The proposed trusted evaluator, frozen source
baseline, held-out fixtures, executable acceptance harness, and human approvals
have not been established. These are future P0 deliverables, not implied by this
record or by the checked acceptance-contract prose.

#### Related DEVNOTES

DEV-2026-11-19-002.

#### Related Tests

None; TEST-2026-11-19-001 covers earlier VENTUNO transcription checks, not this plan.

#### Disposition

Planning documents are ready for review. The user requested plan and test contracts
only, so no implementation phases or packaging were performed. All proposed gates
remain pending; later implementation begins with P0 and G0.


---

---

### TEST-2026-11-19-003 ? Preparation tests before layout and enrichment

**Date:** 2026-11-19  
**Time:** 06:45 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** FAIL

#### Scope

Expected red baseline of the preparation requirements before their implementation.

#### Files Under Validation

- tests/test_repository_content.py
- Current pre-move definitions and journal prefixes captured in baseline.json

#### Objective

Confirm tests do not report success while the requested layout, enrichment,
reference generator, and inactive scaffold files are absent.

#### Preconditions

Five existing definitions; source/manual/journal baseline captured before edits.
Preparation test cases written first; Python 3.13.5 and PyYAML 6.0.2 available.

#### Procedure

Run python -m unittest discover -s tests -v in a subprocess from the repository
root. Capture unedited stdout, stderr, and exit code before moving or enriching files.

#### Expected Result

A nonzero result because the newly requested artifacts do not exist yet; keep the
case collection and errors instead of claiming the missing functionality passed.

#### Actual Result

Eight cases collected: one passed, one failed, and six errored. Process exit code
was 1. The journal-prefix check passed; required layout/content/generator/scaffolds
were missing. The suite was deliberately red before corrective implementation.

#### Evidence

- docs/evidence/reorganization-2026-11-19/before.stdout.txt
- docs/evidence/reorganization-2026-11-19/before.stderr.txt
- docs/evidence/reorganization-2026-11-19/before.exit-code.txt
- docs/evidence/reorganization-2026-11-19/baseline.json

#### Failures / Observations

This is an expected pre-implementation failure, not a passing acceptance run.
The preparation tests and baseline remain agent-writable and self-evaluated.

#### Related DEVNOTES

DEV-2026-11-19-003.

#### Related Tests

Retested by TEST-2026-11-19-004 after implementing the requested preparation.

#### Disposition

Proceed only with correcting the missing layout/content/generator/scaffolds and
retest. No CLI gate, source truth, or packaging approval is established.


---

---

### TEST-2026-11-19-004 ? Prepared catalog reference generation and conservation checks

**Date:** 2026-11-19  
**Time:** 06:59 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** PASS

#### Scope

Execute the source-only reference generator and local preparation checks after
reorganization/enrichment. This is not the protected CLI acceptance suite or
physical hardware verification.

#### Files Under Validation

- hardware/**/definition.yml and generated README.md files
- hardware/controllers/arduino/ventuno_q/sources/user_manual.md
- src/ysl_components/reference_pages.py
- tests/test_repository_content.py
- tests/collect_preparation_evidence.py
- docs/catalog.md, current documentation links, and inactive scaffolds

#### Objective

Verify that generated reference pages reproduce the current YAML, original data
and source/history are conserved, structured additions resolve, and targeted
faults are detected by the local checks.

#### Preconditions

Windows, Python 3.13.5, and PyYAML 6.0.2. The original baseline was captured before
moves or enrichment; its contents and tests remain agent-writable self-evaluation.
No package build/installation or human gate approval has occurred.

#### Procedure

1. Run python src/ysl_components/reference_pages.py from the repository root.
2. Run python -m unittest discover -s tests -v. Tests compare original fields,
   unchanged file bytes, journal-prefix hashes, manual citations, relationships,
   conflicts/power facts, deterministic generated pages, and inactive scaffolds.
3. Run python -B tests/collect_preparation_evidence.py. This repeats the eight
   cases in a subprocess and captures raw stdout/stderr/exit status. It also checks
   authored/generated Markdown navigation and source fragments, preserving the
   manual's disclosed inherited missing-asset limitations.
4. Inspect five explicit in-memory corruptions: removed CAN inventory entry,
   wrong CAN intermediary, removed Bluetooth-conflict pin, dangling source section,
   and an altered JOMEGA pin function with the same pin count. Require each
   specified check to fail; no production files are mutated.
5. Check markup escaping and duplicate YAML-key rejection. Record environment,
   commands, raw observations, and a local SHA-256 file manifest.

#### Expected Result

Six reproducible generated pages; eight local tests successful; valid current
navigation and source-heading references; all five specified corruptions detected;
unsafe markup escaped and duplicate YAML keys rejected. Original source/history
must remain intact, with no CLI packaging activated.

#### Actual Result

All eight cases passed and the subprocess returned 0. All six generated pages
matched deterministic in-memory regeneration. The 631 local links/fragments had
zero errors. All five specified corruptions were detected; markup escaping and
unique-key checks succeeded. The local manifest contains 40 file digests.

The four other hardware definitions, manual, and standards retain original bytes;
all previous VENTUNO fields are preserved except the intentionally relocated source
path. All historical journal prefixes match their pre-change hashes. The schema
is deliberately rejecting and project packaging metadata/entry points are absent.

#### Evidence

- docs/evidence/reorganization-2026-11-19/README.md
- docs/evidence/reorganization-2026-11-19/baseline.json
- docs/evidence/reorganization-2026-11-19/after.stdout.txt
- docs/evidence/reorganization-2026-11-19/after.stderr.txt
- docs/evidence/reorganization-2026-11-19/after.exit-code.txt
- docs/evidence/reorganization-2026-11-19/checks.json
- docs/evidence/reorganization-2026-11-19/manifest.json

Collector output:

```text
Unit test exit code: 0
Navigation: 631 local links/fragments, 0 errors
Deliberate corruptions detected: 5/5
Renderer checks: {'markup_escaped': True, 'duplicate_yaml_key_rejected': True}
Manifest: 40 file digests; local self-evaluation only
```

#### Failures / Observations

No failures in the final local preparation checks. Preserve the earlier red
baseline. The corruption demonstrations use in-memory substitution/direct field
comparison, not a held-out black-box CLI evaluator. No browser visual review,
Linux run, bench test, primary-PDF discrepancy resolution, independent acceptance,
package build/installation, or publication was performed. The copied manual's
missing local images and site-relative links remain disclosed source limitations.

The manifest intentionally excludes itself, root journals, caches, and Git metadata;
original journal-prefix integrity is checked separately. It is not a signature,
human approval, or the later CLI plan's complete approved candidate identity.

#### Related DEVNOTES

DEV-2026-11-19-003; earlier scope and source context in DEV-2026-11-19-001 and
DEV-2026-11-19-002.

#### Related Tests

Retest of TEST-2026-11-19-003 after implementing the requested preparation.

#### Disposition

The separately requested repository layout, source additions, and generated
references are ready for human browsing. This PASS covers the observed local
preparation behavior only. All G0-G5 gates remain pending; future CLI-plan
execution begins with its independently reviewed P0 baseline. Packaging remains
closed until explicit G4 human validation.


---

---

### TEST-2026-11-19-005 - Schema test-first baseline before draft implementation

**Date:** 2026-11-19  
**Time:** 07:18 America/New_York  
**Tester:** Codex  
**Level:** T0  
**Result:** FAIL

#### Scope

Schema review expectations against the old rejecting placeholder.

#### Files Under Validation

- tests/test_schema_review.py
- tests/fixtures/schema_review/board.json, family.json, module.json
- schemas/component.schema.json before replacement

#### Objective

Confirm missing draft resources and review helpers do not pass the new positive
and semantic acceptance expectations.

#### Preconditions

Fixtures/tests authored first; hardware/pyproject/journal-prefix baseline captured.
Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2 available.

#### Procedure

Run python -B -m unittest discover -s tests -p test_schema_review.py -v in a
subprocess and retain raw stdout/stderr and exit status before implementing schemas.

#### Expected Result

Nonzero result because the six resources, registry, and semantic/parsing harness
are absent and the placeholder rejects otherwise valid examples.

#### Actual Result

Seven methods ran: two failed, three errored, two passed. Exit status 1. This is
the expected red baseline, not a passing schema acceptance result.

#### Evidence

- docs/evidence/schema-review-2026-11-19/before.stdout.txt
- docs/evidence/schema-review-2026-11-19/before.stderr.txt
- docs/evidence/schema-review-2026-11-19/before.exit-code.txt
- docs/evidence/schema-review-2026-11-19/before.json

#### Failures / Observations

Missing implementation and rejecting placeholder; corrective schema/harness work
is required. Tests and fixtures are agent-writable, not an independently frozen oracle.

#### Related DEVNOTES

DEV-2026-11-19-004.

#### Related Tests

Retested by TEST-2026-11-19-007.

#### Disposition

Proceed only with implementing/correcting the requested review draft and tests.
No production migration or packaging is authorized by this failure.

---

---

### TEST-2026-11-19-006 - First schema evidence collector attempt

**Date:** 2026-11-19  
**Time:** 07:29 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** FAIL

#### Scope

First execution of the schema-review evidence collector and navigation checks.

#### Files Under Validation

- tests/collect_schema_review_evidence.py
- docs/evidence/schema-review-2026-11-19/README.md and report outputs

#### Objective

Produce complete reports with working evidence navigation and successful test outcomes.

#### Preconditions

Draft schemas/helpers implemented; all preparation and schema tests available.

#### Procedure

Run python -B tests/collect_schema_review_evidence.py and capture the resulting
structured observations, raw test reports, exit code, and artifact inventory.

#### Expected Result

All test methods/subcases execute and evidence links resolve after output creation.

#### Actual Result

All 15 methods and 54 subcases succeeded with zero skips, but navigation ran before
checks.json, after.exit-code.txt, and manifest.json were created. Three missing-target
errors correctly caused exit status 1.

#### Evidence

- docs/evidence/schema-review-2026-11-19/first-collector-attempt/checks.json
- docs/evidence/schema-review-2026-11-19/first-collector-attempt/after.stderr.txt
- docs/evidence/schema-review-2026-11-19/first-collector-attempt/after.exit-code.txt

#### Failures / Observations

Collector output-ordering defect; test success alone did not establish complete
evidence. Preserve the failed attempt. Correct the collector to write explicit
pending/non-success report states before checking its own output links, then
finalize actual results and hashes. Interrupted collection cannot claim success.

#### Related DEVNOTES

DEV-2026-11-19-004.

#### Related Tests

Retested by TEST-2026-11-19-007.

#### Disposition

Correct the collector ordering and rerun. No acceptance gate is approved.

---

---

### TEST-2026-11-19-007 - Schema review harness, regression, and preservation checks

**Date:** 2026-11-19  
**Time:** 07:30 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** PASS

#### Scope

Local validation of the schema review draft, synthetic fixtures, review parser/
semantic behavior, preparation regression, and evidence navigation.

#### Files Under Validation

- Six schemas and proposed identity registry under schemas/
- tests/test_schema_review.py and tests/schema_review_support.py
- Three authored synthetic JSON fixtures
- Preparation tests, documentation, hardware/pyproject baseline and journal prefixes

#### Objective

Execute the defined review cases with positive and explicit negative observations,
while preserving catalog bytes and stopping before package implementation.

#### Preconditions

Windows with Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2.
Local schema registry and FormatChecker configured. No dependencies installed;
no project/package/build entry point created.

#### Procedure

1. Run python -B -m unittest discover -s tests -p test_schema_review.py -v.
2. Run python -B -m unittest discover -s tests -v.
3. Run python -B tests/collect_schema_review_evidence.py. Require all seven schema
   methods among at least 15 total methods, at least 54 recorded subcases, no skips,
   no optimized execution, no failures/errors, and valid current Markdown navigation.
4. Inspect the initial failed run and failed collector attempt separately from the
   final run. Compare every hardware file and pyproject.toml with before-byte hashes;
   compare pre-change journal prefixes and ensure legacy definitions remain unmigrated.

#### Expected Result

Six valid metaschemas, three valid synthetic kinds, five proposed IDs matching
legacy aliases/selectors, correct negative rejections, and no changed hardware or
packaging bytes. All review checks execute without skips; all current links resolve.

#### Actual Result

All 15 methods passed, including all seven schema-review methods. All 54 recorded
subcases succeeded; zero skips, failures, errors, or navigation errors. Final exit
status 0. Hardware/pyproject bytes and pre-existing journal prefixes match baseline.
No Python package initializer/main, CLI, build/distribution artifacts, or migration
was created. All five existing wrapped definitions are intentionally rejected by
this normalized draft until a later migration is approved.

#### Evidence

- docs/evidence/schema-review-2026-11-19/README.md
- docs/evidence/schema-review-2026-11-19/after.stdout.txt
- docs/evidence/schema-review-2026-11-19/after.stderr.txt
- docs/evidence/schema-review-2026-11-19/after.exit-code.txt
- docs/evidence/schema-review-2026-11-19/checks.json
- docs/evidence/schema-review-2026-11-19/manifest.json (67 file digests)

Collector output:

```text
15/15 methods executed; 7 schema-review methods passed; 54 subcases recorded; 0 skipped.
Failures: 0; errors: 0; navigation errors: 0.
Hardware/pyproject/journal-prefix preservation checked by the executed tests; no packaging or migration performed.
```

#### Failures / Observations

No final local failures. Preserve TEST-2026-11-19-005 and TEST-2026-11-19-006.
Results are self-evaluated; no protected runner, human-approved oracle, independent
reproduction, real query behavior, full field-by-field migration, Linux run, hardware
bench test, or package build/installation is claimed. Schema documents check shape;
semantic checks remain a test-only prototype, not an implemented production API.

#### Related DEVNOTES

DEV-2026-11-19-004.

#### Related Tests

Retest of TEST-2026-11-19-005 and TEST-2026-11-19-006. Retains the preparation
regression expectations from TEST-2026-11-19-004 with the explicitly authorized
transition from rejecting scaffold to unapproved schema draft.

#### Disposition

The schemas, proposed IDs, fixtures, and local evidence are ready for human review.
No review gate is approved and no further implementation is performed. Await review
before adoption/migration; packaging still requires separate explicit G4 approval.


---

---

### TEST-2026-11-19-008 - P2 test-first migration baseline

**Date:** 2026-11-19  
**Time:** 10:33 America/New_York  
**Tester:** Codex  
**Level:** T0  
**Result:** FAIL

#### Scope

P2 requirements before writing the converter or normalized definitions.

#### Files Under Validation

- tests/test_migration.py
- Original definitions and migration baseline

#### Objective

Demonstrate that missing migration cannot pass the new preservation/schema tests.

#### Preconditions

Windows, Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2.
Original definitions preserved before migration; approved schema/registry snapshot
available locally. No package installation or independent runner is claimed.

#### Procedure

Run python -B -m unittest discover -s tests -p test_migration.py -v in a subprocess; retain stdout/stderr/exit status before implementing migration.

#### Expected Result

Nonzero result for missing flat instances, field map and converter.

#### Actual Result

Seven methods ran: one failure, five errors, one preservation-only pass; exit 1.

#### Evidence

- docs/evidence/migration-2026-11-19/before.stdout.txt
- docs/evidence/migration-2026-11-19/before.stderr.txt
- docs/evidence/migration-2026-11-19/before.exit-code.txt
- docs/evidence/migration-2026-11-19/baseline.json

#### Failures / Observations

Expected red baseline; it is not a passing acceptance result.

#### Related DEVNOTES

DEV-2026-11-19-005.

#### Related Tests

Retested by TEST-2026-11-19-011.

#### Disposition

Continue only to implement/correct the requested migration and retest.


---

---

### TEST-2026-11-19-009 - First P2 schema validation

**Date:** 2026-11-19  
**Time:** 10:38 America/New_York  
**Tester:** Codex  
**Level:** T0  
**Result:** FAIL

#### Scope

First converted instances under the approved schemas.

#### Files Under Validation

- Migrated definitions
- tools/migrate_catalog.py

#### Objective

Validate output against the immutable approved contract.

#### Preconditions

Windows, Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2.
Original definitions preserved before migration; approved schema/registry snapshot
available locally. No package installation or independent runner is claimed.

#### Procedure

Run P2 tests, then enumerate actual JSON Schema errors for all five converted documents.

#### Expected Result

All five instances validate without schema changes.

#### Actual Result

VENTUNO generated source metadata used kind schematics; the approved enum requires schematic. Other preservation/manual/determinism/corruption/source checks completed successfully.

#### Evidence

- docs/evidence/migration-2026-11-19/first-validation-failure.json

#### Failures / Observations

Correct the converter classification; do not broaden the approved enum to hide the defect.

#### Related DEVNOTES

DEV-2026-11-19-005.

#### Related Tests

Retested after correction; semantic walker failure recorded separately in TEST-2026-11-19-010.

#### Disposition

Correct source-kind generation, regenerate from snapshots, and rerun.


---

---

### TEST-2026-11-19-010 - P2 semantic checker traversal defect

**Date:** 2026-11-19  
**Time:** 10:39 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** FAIL

#### Scope

Typed semantic checking after schema-shape correction.

#### Files Under Validation

- tests/schema_review_support.py
- Real migrated definitions

#### Objective

Resolve references without interpreting arbitrary fact/source names as reference fields.

#### Preconditions

Windows, Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2.
Original definitions preserved before migration; approved schema/registry snapshot
available locally. No package installation or independent runner is claimed.

#### Procedure

Run the P2 suite and preserve the traceback from semantic_errors on the converted catalog.

#### Expected Result

Schema-valid fact maps can contain a fact named processor without a reference lookup.

#### Actual Result

The walker treated a fact-value dictionary under key processor as a reference target and raised TypeError: unhashable type: dict. The other six P2 methods passed.

#### Evidence

- docs/evidence/migration-2026-11-19/semantic-walker-failure.txt

#### Failures / Observations

Walk values inside typed inventory maps without reinterpreting map entry names; add a regression using reserved fact/source names. Approved JSON Schema bytes remain unchanged.

#### Related DEVNOTES

DEV-2026-11-19-005.

#### Related Tests

Retested by TEST-2026-11-19-011.

#### Disposition

Correct traversal and retain all existing reference/collision negative tests before proceeding.


---

---

### TEST-2026-11-19-011 - P2 migration conservation and regression evidence

**Date:** 2026-11-19  
**Time:** 10:52 America/New_York  
**Tester:** Codex  
**Level:** T1  
**Result:** PASS

#### Scope

Completed P2 migration, independent source comparison, normalized reference generation and local evidence.

#### Files Under Validation

- Five migrated hardware definitions and six generated pages
- tools/migrate_catalog.py
- tests/test_migration.py, migration_checks.py and schema/preparation regressions
- Approved schemas, original snapshots, source/config/journal baselines

#### Objective

Execute P2 behavior and preservation checks while stopping before query CLI and packaging.

#### Preconditions

Windows, Python 3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, referencing 0.30.2.
Original definitions preserved before migration; approved schema/registry snapshot
available locally. No package installation or independent runner is claimed.

#### Procedure

Run the source migration utility and documentation generator. Run python -B tests/collect_migration_evidence.py. The collector executes all tests, captures raw events, refuses optimization, requires seven migration methods and six corruption subcases, and checks current links/fragments. Inspect original and generated leaf accounting independently of converter helpers.

#### Expected Result

Five schema-valid instances; all 3403 original leaves and 345 pin records accounted for; original bytes retained; all corruption/semantic/reference/regression checks pass with no skipped cases.

#### Actual Result

22/22 methods passed, including seven migration methods; 60 subcases recorded and all six deliberate corruptions rejected. All 3403 original leaves map to exact-type/exact-value destinations, and additional metadata is bound to recorded generated values/reasons. All 345 pin records survive. Zero failures/errors/skips; 1447 current links/fragments have zero errors. Approved schema/registry bytes, original source/standards bytes, pyproject bytes and journal prefixes match baseline. Final exit code 0.

#### Evidence

- docs/evidence/migration-2026-11-19/README.md
- docs/evidence/migration-2026-11-19/field-map.json
- docs/evidence/migration-2026-11-19/after.stdout.txt
- docs/evidence/migration-2026-11-19/after.stderr.txt
- docs/evidence/migration-2026-11-19/after.exit-code.txt
- docs/evidence/migration-2026-11-19/checks.json
- docs/evidence/migration-2026-11-19/manifest.json (90 file digests)

#### Failures / Observations

Local self-evaluation only. The comparison checker does not import conversion code; the separate deterministic-conversion test intentionally invokes it. Original snapshots/mappings/tests are still agent-writable, so independent reproduction and human G2 review remain necessary. No source discrepancy was silently resolved, no physical verification promoted, and no query CLI, package backend, installation, Linux run, or publication was performed. Historical prior-phase evidence is not rewritten.

#### Related DEVNOTES

DEV-2026-11-19-005.

#### Related Tests

Retest of TEST-2026-11-19-008, TEST-2026-11-19-009 and TEST-2026-11-19-010. Retains earlier schema/preparation regressions with explicit adoption-aware expectations.

#### Disposition

P2 is ready for G2 review. Do not infer G2 acceptance or G4 packaging approval from this local PASS; stop before P3 query/CLI implementation.

---

---

### TEST-2026-11-19-012 — P3 module compilation

**Date:** 2026-11-19  
**Time:** 14:46 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T0  
**Result:** PASS

#### Scope

Static compilation of the new development package modules.

#### Files Under Validation

- src/ysl_components/__init__.py
- src/ysl_components/__main__.py
- src/ysl_components/loader.py
- src/ysl_components/query.py
- src/ysl_components/cli.py

#### Objective

Verify that the new modules compile under the local interpreter.

#### Preconditions

Linux, Python 3.12.3. No package installation.

#### Procedure

Run `python3 -B -m py_compile` on the five modules listed above.

#### Expected Result

The compiler exits 0 and reports no syntax error.

#### Actual Result

Compilation completed with exit 0. Bytecode created during the compile was deleted and is not part of the change.

#### Evidence

- `python3 -B -m py_compile src/ysl_components/__init__.py src/ysl_components/__main__.py src/ysl_components/loader.py src/ysl_components/query.py src/ysl_components/cli.py`

#### Failures / Observations

Compilation does not exercise query behavior.

#### Related DEVNOTES

DEV-2026-11-19-006.

#### Related Tests

Runtime coverage is TEST-2026-11-19-013 and TEST-2026-11-19-014.

#### Disposition

Static compilation is complete. Runtime results are recorded separately.

---

---

### TEST-2026-11-19-013 — P3 query contract cases AC-301 through AC-308

**Date:** 2026-11-19  
**Time:** 14:48 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T2  
**Result:** PASS

#### Scope

Subprocess behavior of `python -m ysl_components` for validation, list, search, show, pin, pins, interface, and export.

#### Files Under Validation

- src/ysl_components/cli.py
- src/ysl_components/loader.py
- src/ysl_components/query.py
- tests/test_query_contract.py
- The five migrated hardware definitions
- tests/fixtures/schema_review/board.json
- tests/fixtures/schema_review/module.json

#### Objective

Observe the frozen exit codes, JSON envelope, diagnostic codes, and read-only query results for AC-301 through AC-308 on Linux.

#### Preconditions

Linux 6.12.113+, Python 3.12.3, PyYAML 6.0.1, jsonschema 4.23.0, referencing 0.30.2. `PYTHONPATH=src` is supplied by the test. No wheel, editable install, or installed command. Windows was not available. Results are self-evaluated.

#### Procedure

Run `python3 -B -m unittest tests.test_query_contract -v`, and then the same eight methods as part of `python3 -B -m unittest discover -s tests -v`. The cases call the module as a subprocess. They do not import query helpers. Networked sockets are blocked for the AC-307 subprocess. Catalog file hashes are compared before and after read-only commands.

#### Expected Result

Eight methods pass. Valid catalogs exit 0. Invalid data exits 2 and still lists every definition file. Unsupported schema version exits 5. Missing selectors exit 3. Uno pin alias D18 exits 4 with candidates A4 and SDA and no selected pin. Stdout parses as one JSON document. Success writes no stderr. Export round-trips the synthetic board, refuses an existing file without `--force`, and refuses a path inside the catalog. A stale or invalid `catalog-index.json` exits 2 and does not return component entries. VENTUNO D5 maps to PB5, Uno D5 maps to PD5, Bluetooth claims stay 5.3 and 5.1 with no selected value, and verification stays `not_verified`.

#### Actual Result

All eight methods passed inside the final 30-test run. The behaviors listed above were observed, including identical repeated VENTUNO show output, L293D continuous current 0.6 with integrated clamp diodes true, and L293 continuous current 1.0 with integrated clamp diodes false. An earlier local expectation that L293 pins used the exact capability token `pwm` was corrected to the stored tokens `pwm_input` and `pwm_output_conditional` before this pass; the product filter stayed exact.

#### Evidence

- `python3 -B -m unittest discover -s tests -v` — 30 tests, OK, about 44 seconds
- Command shape: `PYTHONPATH=src python3 -B -m ysl_components --catalog <path> <operation>`

#### Failures / Observations

Linux only. Windows AC-307 was not executed; see TEST-2026-11-19-015. No independent reviewer ran these cases. The fault seam `YSL_COMPONENTS_FAULT=unexpected` is what produced exit 1. JSON Schema library sentences are not asserted. No definition or source file was modified by the queries.

#### Related DEVNOTES

DEV-2026-11-19-006.

#### Related Tests

TEST-2026-11-19-012, TEST-2026-11-19-014, TEST-2026-11-19-015.

#### Disposition

Linux query behavior matches the frozen contract in this self-evaluated run. G3 is not accepted by this record. Packaging remains unauthorized.

---

---

### TEST-2026-11-19-014 — P3 regression of the existing local suite

**Date:** 2026-11-19  
**Time:** 14:48 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T3  
**Result:** PASS

#### Scope

Milestone regression after the query module and the Linux newline comparison for preserved bytes.

#### Files Under Validation

- tests/test_query_contract.py
- tests/test_migration.py
- tests/test_schema_review.py
- tests/test_repository_content.py
- src/ysl_components/
- pyproject.toml remained without a build backend

#### Objective

Run the existing unittest suite together with the new query cases and confirm packaging is still disabled.

#### Preconditions

Same Linux interpreter and libraries as TEST-2026-11-19-013. Journal prefixes and schema bytes were not rewritten. DEV-2026-11-19-007 allows a pure LF-to-CRLF digest match for the Windows baseline.

#### Procedure

Run `python3 -B -m unittest discover -s tests -v` from the repository root after the query modules and preservation comparison were in place.

#### Expected Result

30 tests, no failures, no errors, and no skips. `pyproject.toml` still has no project or build-system table.

#### Actual Result

Ran 30 tests in 44.051 seconds. OK. No failures, errors, or skips. The packaging guard still saw `packaging_enabled` false and no `dist` directory.

#### Evidence

- `python3 -B -m unittest discover -s tests -v`
- Output ended with `Ran 30 tests in 44.051s` and `OK`

#### Failures / Observations

Self-evaluated on Linux. The preservation checks accept the recorded CRLF digest when the LF git blob differs only by newline translation, as decided in DEV-2026-11-19-007. That is not a new Windows execution. Generated pages were not regenerated.

#### Related DEVNOTES

DEV-2026-11-19-006, DEV-2026-11-19-007.

#### Related Tests

TEST-2026-11-19-011, TEST-2026-11-19-013, TEST-2026-11-19-015.

#### Disposition

The local Linux regression may be used as P3 evidence for G3. It does not close G3, authorize packaging, or establish bench verification.

---

---

### TEST-2026-11-19-015 — Windows execution of AC-307

**Date:** 2026-11-19  
**Time:** 14:48 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T2  
**Result:** NOT_EXECUTED

#### Scope

AC-307 on Windows: catalog paths, working directory, read-only hashes, and no network.

#### Files Under Validation

- src/ysl_components/cli.py

#### Objective

Record that the Windows half of AC-307 was not run.

#### Preconditions

This session had a Linux checkout only. No Windows runner was available.

#### Procedure

No Windows command was run.

#### Expected Result

The same query observations as the Linux AC-307 case, on Windows.

#### Actual Result

The procedure was not started. Linux coverage is TEST-2026-11-19-013. Windows is unverified.

#### Evidence

- `platform.platform()` during the Linux run: `Linux-6.12.113+-x86_64-with-glibc2.39`

#### Failures / Observations

Missing platform coverage is not a Linux pass.

#### Related DEVNOTES

DEV-2026-11-19-006.

#### Related Tests

TEST-2026-11-19-013.

#### Disposition

Leave Windows unverified for G3. Do not mark AC-307 fully covered.

---

---

### TEST-2026-11-19-016 — P4 page contract before the generator adaptation

**Date:** 2026-11-19  
**Time:** 16:31 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T1  
**Result:** FAIL

#### Scope

AC-401 through AC-405 and the AC-501 denial, against the generator as it stood after G3 and before the P4 adaptation.

#### Files Under Validation

- src/ysl_components/reference_pages.py
- tests/test_page_contract.py
- tests/page_checks.py

#### Objective

Observe whether the existing generator already satisfies the frozen page contract.

#### Preconditions

Linux 6.12.113+, Python 3.12.3, PyYAML 6.0.1. The page contract and tests existed. `src/ysl_components/packaging.py` did not. Generated pages were the P2 output.

#### Procedure

Run `python3 -B -m unittest tests.test_page_contract -v` from the repository root.

#### Expected Result

Seven methods pass: fact oracle, planted link/image/fact faults, manual-image inventory, two clean generations, escaped labels, manifest tamper detection, and six packaging denials with no distribution.

#### Actual Result

Ran 7 tests in 1.425 seconds. FAILED: 2 failures, 1 error. AC-402 manual images, AC-403 determinism, AC-404 escaping, and AC-405 manifest tamper passed. AC-401 and the clean half of AC-402 failed. The catalog did not contain the five stable IDs, the regeneration command, `Packaging is disabled`, the G3 record name, or `authored separately`. Component pages had no `**Verification limits:**` line and no `**Declared pin capabilities:**` line. The ATtiny and L293 pages had no `**Family selectors:**` line. The discriminating hardware literals already on the pages, including Uno `PD5`, VENTUNO `PB5`, the six conflict topics, L293/L293D currents and clamp diodes, and the HC-SR04 echo facts, were not in the failure list. AC-501 raised `FileNotFoundError` for `src/ysl_components/packaging.py`.

#### Evidence

- `python3 -B -m unittest tests.test_page_contract -v`
- Summary: `Ran 7 tests in 1.425s` and `FAILED (failures=2, errors=1)`

#### Failures / Observations

The failure is the missing P4 adaptation, not a changed hardware fact. No distribution was created.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

None.

#### Disposition

Do not treat the pages as the P4 candidate. Adapt the generator and add the denial module, then rerun. Packaging remains closed.

---

---

### TEST-2026-11-19-017 — P4 module file validation

**Date:** 2026-11-19  
**Time:** 16:45 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T0  
**Result:** PASS

#### Scope

Parse and compile the P4 implementation files.

#### Files Under Validation

- src/ysl_components/reference_pages.py
- src/ysl_components/packaging.py
- tests/page_checks.py
- tests/test_page_contract.py
- tests/collect_page_evidence.py

#### Objective

Verify that the adapted generator, denial module, checks, and evidence collector compile.

#### Preconditions

Python 3.12.3 on Linux. No package installation of this repository.

#### Procedure

Run `python3 -m py_compile` on the five files listed above.

#### Expected Result

The command exits 0 and writes no diagnostic.

#### Actual Result

The command exited 0 with no output.

#### Evidence

- `python3 -m py_compile src/ysl_components/reference_pages.py src/ysl_components/packaging.py tests/page_checks.py tests/test_page_contract.py tests/collect_page_evidence.py`

#### Failures / Observations

Compilation does not exercise page generation. Runtime coverage is TEST-2026-11-19-018 and TEST-2026-11-19-020.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

TEST-2026-11-19-016.

#### Disposition

File validation passed. Runtime results are recorded separately.

---

---

### TEST-2026-11-19-018 — Adapted pages, fact oracle, and packaging denial

**Date:** 2026-11-19  
**Time:** 16:36 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T1  
**Result:** PASS

#### Scope

AC-401 through AC-405 and AC-501 after adapting `reference_pages.py` and adding `packaging.py`.

#### Files Under Validation

- src/ysl_components/reference_pages.py
- src/ysl_components/packaging.py
- tests/test_page_contract.py
- tests/page_checks.py
- docs/catalog.md
- hardware/controllers/arduino/uno_r3/README.md
- hardware/controllers/arduino/ventuno_q/README.md
- hardware/controllers/microchip/attiny_x5/README.md
- hardware/drivers/ti/l293_family/README.md
- hardware/sensors/generic/hc_sr04/README.md

#### Objective

Generate the six pages from the migrated definitions and observe the frozen fact, link, determinism, escaping, manifest, and denial behavior.

#### Preconditions

Pages were regenerated with `python3 src/ysl_components/reference_pages.py`. Linux, Python 3.12.3, PyYAML 6.0.1. `pyproject.toml` had no build backend. `dist/` was absent.

#### Procedure

1. Regenerate the catalog and five component pages.
2. Run `python3 -B -m unittest tests.test_page_contract -v`.

#### Expected Result

Seven methods pass. The fact oracle holds, planted faults are reported, 45 missing manual images stay out of the generated-asset count, two clean directories match, labels stay escaped, manifest tamper is detected, and every packaging request is denied without calling a builder.

#### Actual Result

Ran 7 tests in 3.671 seconds. OK. The regenerated catalog lists `arduino/uno-r3`, `arduino/ventuno-q`, `microchip/attiny-x5`, `ti/l293-family`, and `generic/hc-sr04`. VENTUNO records 6 source issues. No distribution was written.

#### Evidence

- `python3 src/ysl_components/reference_pages.py`
- `python3 -B -m unittest tests.test_page_contract -v`
- Summary: `Ran 7 tests in 3.671s` and `OK`

#### Failures / Observations

This run is self-evaluated. It does not include Windows or an independent reviewer. The same seven methods ran again inside TEST-2026-11-19-020.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

TEST-2026-11-19-016.

#### Disposition

The adapted generator and denial module meet the frozen page contract in this Linux run. G4 is not approved. The full suite still had to be rerun.

---

---

### TEST-2026-11-19-019 — Full suite before jsonschema was installed

**Date:** 2026-11-19  
**Time:** 16:40 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T3  
**Result:** FAIL

#### Scope

First P4 regression of the existing suite plus the new page cases, through `tests/collect_page_evidence.py`.

#### Files Under Validation

- tests/
- src/ysl_components/

#### Objective

Run the repository unittest suite in the evidence collector.

#### Preconditions

The page adaptation was in place. This Linux environment did not have the `jsonschema` distribution installed. PyYAML 6.0.1 was installed. The P3 journal names jsonschema 4.23.0 and referencing 0.30.2.

#### Procedure

Run `python3 -B tests/collect_page_evidence.py`. The collector starts `python3 -B -m unittest discover -s tests -v`.

#### Expected Result

The suite completes with no failures. Query cases import `jsonschema` inside the `python -m ysl_components` subprocess.

#### Actual Result

The unittest process exited 1. The captured summary was `Ran 31 tests in 10.265s` and `FAILED (failures=11, errors=8)`. The export case stderr contained `ModuleNotFoundError: No module named 'jsonschema'` from `src/ysl_components/loader.py`. The collector then stopped with `PackageNotFoundError: No package metadata was found for jsonschema` before it wrote the final manifest. That raw log was replaced by the later successful collector run.

#### Evidence

- `python3 -B tests/collect_page_evidence.py`
- Subprocess traceback ending at `from jsonschema import Draft202012Validator, FormatChecker`

#### Failures / Observations

The failure is a missing test dependency in this environment, not a page-generation assertion. No wheel was built.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

TEST-2026-11-19-013, TEST-2026-11-19-018.

#### Disposition

Install jsonschema 4.23.0 and referencing 0.30.2, matching the versions named by the P3 run, and rerun. Do not treat this failure as a hardware-fact change. The rerun is TEST-2026-11-19-020.

---

---

### TEST-2026-11-19-020 — P4 evidence run and repository regression

**Date:** 2026-11-19  
**Time:** 16:44 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T3  
**Result:** PASS

#### Scope

Milestone regression for P4: AC-401 through AC-405, the AC-501 denial, and the existing AC-101 through AC-308 cases, plus link, fact, determinism, tamper, and view capture.

#### Files Under Validation

- src/ysl_components/reference_pages.py
- src/ysl_components/packaging.py
- tests/collect_page_evidence.py
- tests/test_page_contract.py
- tests/test_query_contract.py
- tests/test_migration.py
- tests/test_schema_review.py
- tests/test_repository_content.py
- docs/catalog.md
- hardware/**/README.md generated pages
- docs/evidence/pages-2026-11-19/

#### Objective

Execute the full local suite and assemble the P4 evidence bundle without producing a distribution.

#### Preconditions

Linux 6.12.113+, Python 3.12.3, PyYAML 6.0.1, jsonschema 4.23.0, referencing 0.30.2. The last two were installed for this environment after TEST-2026-11-19-019. They are not project packaging. `pyproject.toml` remained a scaffold. Head at collection was `efbe756a74911bf1e9d468756b29c0ca8ba806ec` with the P4 edits uncommitted. Chrome was available for the PNG views. Results are self-evaluated.

#### Procedure

Run `python3 -B tests/collect_page_evidence.py` from the repository root. The collector runs `python3 -B -m unittest discover -s tests -v`, checks the fact oracle and links, inventories manual images, repeats generation, denies packaging, tampers with a temporary manifest, renders four views, and writes `docs/evidence/pages-2026-11-19/manifest.json`.

#### Expected Result

Unittest exit 0. Fact, generated-link, generated-image, and repository-navigation errors are empty. Two generations match the files on disk. Forty-five manual images are missing and none of those paths are present. Packaging denial matches all six reason codes, the builder is not called, and `dist/` does not exist. The tamper copy reports missing and changed. Each PNG view starts with the PNG signature. Manifest verification reports no problems.

#### Actual Result

The collector exited 0. Unittest reported `Ran 37 tests in 49.869s` and `OK`. Fact errors 0, link errors 0, navigation errors 0. Manual images missing 45, present 0. Determinism matched. Packaging denial was ok. Tamper demo was ok. Screenshot errors were empty. Manifest problems were 0. The catalog view shows the five IDs and 6 VENTUNO source issues. The VENTUNO pin view shows D5 mapped to PB5. The conflict view shows the six source conflicts, including Bluetooth 5.3 and 5.1 with no selected version. The ATtiny view shows ATtiny25, ATtiny45, ATtiny85 and the three V profiles. The HTML view of the catalog also prints the regeneration fence markers as text; the Markdown source keeps them as a fence.

#### Evidence

- `python3 -B tests/collect_page_evidence.py`
- `docs/evidence/pages-2026-11-19/after.stdout.txt`
- `docs/evidence/pages-2026-11-19/after.stderr.txt`
- `docs/evidence/pages-2026-11-19/after.exit-code.txt`
- `docs/evidence/pages-2026-11-19/checks.json`
- `docs/evidence/pages-2026-11-19/views/catalog.png`
- `docs/evidence/pages-2026-11-19/views/ventuno-d5-pins.png`
- `docs/evidence/pages-2026-11-19/views/ventuno-conflicts.png`
- `docs/evidence/pages-2026-11-19/views/attiny-family.png`

#### Failures / Observations

Linux only. Windows was not run. No independent reviewer ran this collector. The manifest is a local inventory, not a signature. G4 is not approved. The six VENTUNO discrepancies remain unresolved and verification remains `not_verified`.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

TEST-2026-11-19-014, TEST-2026-11-19-016, TEST-2026-11-19-018, TEST-2026-11-19-019.

#### Disposition

The local Linux P4 candidate can be reviewed. It does not authorize packaging, close the Windows gap, or establish bench verification. A reviewer outside this workspace has not reproduced the bundle.

---

---

### TEST-2026-11-19-021 — Windows page generation and AC-307

**Date:** 2026-11-19  
**Time:** 16:45 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T3  
**Result:** NOT_EXECUTED

#### Scope

Windows execution of page generation and of AC-307 query behavior carried forward from G3.

#### Files Under Validation

- src/ysl_components/reference_pages.py
- src/ysl_components/cli.py

#### Objective

Record that Windows was not run for the P4 candidate or for the still-open AC-307 gap.

#### Preconditions

This session had a Linux checkout only. No Windows runner was available.

#### Procedure

No Windows command was run.

#### Expected Result

The same page and query observations as the Linux run, on Windows.

#### Actual Result

The procedure was not started. Linux coverage is TEST-2026-11-19-020. Windows is unverified.

#### Evidence

- `platform.platform()` during the Linux evidence run: `Linux-6.12.113+-x86_64-with-glibc2.39`

#### Failures / Observations

Missing platform coverage remains an unresolved item. G3 approval did not include a Windows run.

#### Related DEVNOTES

DEV-2026-11-19-009.

#### Related Tests

TEST-2026-11-19-015, TEST-2026-11-19-020.

#### Disposition

Leave Windows unverified. Do not mark AC-307 or the page views as covered on Windows.

---

---

### TEST-2026-11-19-022 — P5 packaging under the Ventuno Q G4 scope

**Date:** 2026-11-19  
**Time:** 17:03 America/New_York  
**Tester:** Cursor cloud agent  
**Level:** T3  
**Result:** BLOCKED

#### Scope

P5 packaging for the G4 statement that authorizes `arduino/ventuno-q` only. AC-502 through AC-505.

#### Files Under Validation

- docs/planning/CLI_IMPLEMENTATION_PLAN.md
- docs/planning/CLI_ACCEPTANCE_TESTS.md
- docs/planning/CLI_PAGE_CONTRACT.md
- docs/reviews/g4-approval-2026-11-19.md
- pyproject.toml

#### Objective

Determine whether the frozen packaging contract can build a distribution for `arduino/ventuno-q` without also packaging the other four definitions.

#### Preconditions

Clean checkout of commit `bbf013354b3ac7d4fdc9be8b44090634b431b118`. The user statement is "authorized for the Ventuno Q." No broader packaging approval was received.

#### Procedure

1. Bind the statement to that commit and to `hardware/controllers/arduino/ventuno_q/definition.yml`.
2. Compare the statement with P5, AC-502, AC-503, AC-401, the page-contract denial table, and the five-entry identity registry.
3. Parse `pyproject.toml` and check for a build backend, a project table, `packaging_enabled`, and a `dist/` directory.
4. Do not invoke a builder.

#### Expected Result

A contract path that packages the authorized definition alone would allow a wheel and sdist. A contract that packages the five-definition catalog would block that build.

#### Actual Result

The contract packages the five-definition catalog as one unit. AC-502 requires the installed command to serve that catalog and to include all approved schemas and data. AC-503 treats missing catalog data as a failure. No row defines a one-component distribution. The build was not started. `pyproject.toml` has only the tool table, `packaging_enabled` is false, and `dist/` is absent. The Ventuno Q definition digest is `db3c7fe1af1a69a61dae54787cf7f70b5222a9c066284c75e7f83e455d6826c2`.

#### Evidence

- Candidate commit `bbf013354b3ac7d4fdc9be8b44090634b431b118`, tree `4eb01ea1ec9bea7bf7d537da5495890f9e03f0f3`, clean before this record.
- `python3` `tomllib` parse of `pyproject.toml`: keys `['tool']`, `packaging_enabled` false, no project table, no build backend, `dist/` absent.
- `pyproject.toml` SHA-256 `5d5782d73c9c2ea0630b2090b7739ac30f055919032f5dba7d186e1f8fe6ec18`, unchanged from the candidate.

#### Failures / Observations

AC-502 through AC-505 were not executed. Windows remains not executed. No independent reviewer ran this inspection. The six VENTUNO discrepancies remain unresolved and verification remains `not_verified`. The existing unittest suite was not re-run.

#### Related DEVNOTES

DEV-2026-11-19-011.

#### Related Tests

TEST-2026-11-19-020, TEST-2026-11-19-021.

#### Disposition

Do not implement P5 on this statement. Do not publish. Packaging remains on the AC-501 denial path. A later human decision has to cover the catalog package, or revise the contract, before a wheel or sdist is built.

---

---

