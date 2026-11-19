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
