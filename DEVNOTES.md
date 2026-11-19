# Engineering Decisions

### DEV-2026-11-19-001 — Transcribe the local VENTUNO Q manual with explicit uncertainties

**Date:** 2026-11-19  
**Time:** 05:48 America/New_York  
**Engineer:** Codex  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

Add a hardware-only VENTUNO Q YAML definition from the repository's user manual.
The manual conflicts on Qwiic controller numbering, onboard CAN TX/RX routing,
Bluetooth version, ISP model, Wi-Fi band wording, and a PWM example range.

#### Context and Constraints

The manual snapshot was pulled on 2026-11-19. Existing definitions use a component
root, pin mappings, capabilities, interfaces, and constraints, without a shared
schema. The local manual is the requested source; linked PDFs and physical hardware
were not used for this transcription.

#### Solutions Considered

- Select one claim for each disagreement, which would hide uncertainty.
- Limit the definition to the UNO headers, omitting documented expansion hardware.
- Capture all four complete expansion tables and UNO pins, preserving disagreements
  and incomplete coverage in the source record.

#### Trade-offs

The complete pin map is larger but retains the manual's connector positions and
signal labels. Unresolved ratings and routes remain unsuitable for definitive
connection planning until checked against primary pinouts or schematics. Keeping
separate voltage domains avoids implying universal GPIO compatibility.

#### Final Outcome

Use `arduino_ventuno_q` as the root. Keep A0-A5 canonical with D14-D19 aliases,
matching the Uno definition. Qualify expansion pins as `CONNECTOR_position`, with
`physical_pin` scoped to `connector`. Preserve the published expansion signal in
`maps_to` and its separate function column in `source_function` where present.

Record six discrepancies under `source.discrepancies`. Preserve Qwiic PA8/PC9
from the explicit table and flag the controller-number conflict. Omit definitive
PD0/PD1 CAN routing, Bluetooth version, and ISP model. Capture hardware facts and
constraints without firmware examples or application instructions.

#### Implementation Impact

- Add `controllers/arduino/yaml/arduino_ventuno_q.yml`.
- Update the README inventory and document static verification in `TEST_LOG.md`.
- Preserve the source manual and existing hardware definitions.

#### Verification Required

T0 YAML parsing with duplicate-key rejection, comparison against source pin tables,
and interface-reference validation. No runtime module or integration is introduced;
T1-T3 runtime checks do not apply to this transcription.

#### Related Records

- DEVNOTES: None
- Tests: TEST-2026-11-19-001
- Source: `controllers/arduino/md/arduino_ventuno_q.md`;
  `controllers/arduino/yaml/arduino_ventuno_q.yml`

#### Next Steps

None for the manual transcription. This decision authorizes a source-derived
library entry with static evidence; it does not establish electrical or bench
verification. Codex owns identifying these limitations in the delivered entry.

#### Deferred Decisions

Resolve the six source discrepancies and unspecified pinouts only when primary
pinout, datasheet, schematic, or suitable hardware evidence is available. Update
the definition and append new decision and verification records at that time.

---

---

### DEV-2026-11-19-002 — Propose test-first catalog and CLI phases with human packaging approval

**Date:** 2026-11-19  
**Time:** 06:26 America/New_York  
**Engineer:** Codex  
**Status:** PROPOSED  
**Type:** DECISION

#### Problem

Plan schemas and IDs, migration, validation/local queries, generated browsing
pages, evidence collection, and CLI packaging. The user requires tests defined
first, review gates, resistance to agent shortcuts, and human validation of the
evidence before packaging. The user clarified that this turn is plan and test
contracts only.

#### Context and Constraints

The current collection has five logical definitions with different structures.
An implementing agent can alter local tests, expected outputs, logs, and approval
files; those files alone cannot prove independent verification or human approval.
Existing append-only journals must retain their historical contents.

#### Solutions Considered

- Agent-authored tests and a self-reported success summary.
- A frozen contract and independent source oracle, evaluated through a
  reviewer-controlled runner, with mutation cases and digest-bound evidence.

#### Trade-offs

Independent evaluation and review add setup and reviewer effort. They reduce
correlated mistakes and expose weakened tests, data loss, canned answers, and
stale approvals. They cannot establish electrical correctness or prevent all
evasion. Without an external trust boundary, label results self-evaluated.

#### Final Outcome

Propose P0-P5 and G0-G5 in `repo_docs/CLI_IMPLEMENTATION_PLAN.md`, acceptance
contracts in `repo_docs/CLI_ACCEPTANCE_TESTS.md`, and a reusable gate-review
template. G4 requires an actual human to validate the exact candidate and
evidence before any distribution build or installation of this project. G5
reviews installed-package evidence; publishing remains separate.

The plan, ID registry, and test contracts are drafts for review. No executable
acceptance harness, schemas, migration, query tooling, browsing generator, or
packaging has been implemented in this turn. No review gate is approved.

#### Implementation Impact

- Add the three catalog/CLI planning documents under `repo_docs/`.
- Link them from README and CONTRIBUTING; correct their existing ATtiny links
  to the current `controllers/microchip/attiny.yml` location.
- Preserve definitions, the manual, and earlier decision/test records.

#### Verification Required

Documentation-only static checks: local links/fragments, Markdown fences,
uniqueness and coverage of planned AC IDs, baseline counts, and explicit pending
gate status. Future product tests remain unimplemented and unexecuted; they are
defined by the new acceptance contract rather than claimed as results.

#### Related Records

- DEVNOTES: DEV-2026-11-19-001
- Tests: Pending documentation validation; product acceptance not executed
- Source: `repo_docs/CLI_IMPLEMENTATION_PLAN.md`,
  `repo_docs/CLI_ACCEPTANCE_TESTS.md`, `repo_docs/CLI_GATE_REVIEW_TEMPLATE.md`

#### Next Steps

Review the plan and test contracts. When implementation is separately requested,
start P0 and obtain G0 review before production implementation. Do not infer
packaging approval from the user's request to create this plan.

#### Deferred Decisions

Select the protected evaluation/approval channel and approve the baseline,
schema/identity contract, supported toolchain, packaging metadata, distribution
license, and later release destination through the specified gates.

---

---


### DEV-2026-11-19-003 ? Prepare hardware layout and enrich source references before CLI execution

**Date:** 2026-11-19  
**Time:** 06:57 America/New_York  
**Engineer:** Codex  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

The user explicitly requested the proposed folder layout and six VENTUNO Q
additions before executing the gated CLI plan: inventory, connection relationships,
structured conflicts, power distribution, precise provenance, and reference pages.

#### Context and Constraints

This later instruction authorizes the preparation work despite the earlier
plan-only scope in DEV-2026-11-19-002. It does not authorize human gate approval,
common-schema/ID migration, local query CLI execution, package builds, installation,
or publication. Root journal history and original source bytes must be preserved.

#### Solutions Considered

- Move files only and leave the requested additions for later phases.
- Execute the entire gated CLI plan immediately.
- Perform the explicitly requested preparation, preserve legacy data structures,
  and leave schema/CLI/packaging activation behind the existing gates.

#### Trade-offs

The reference generator provides useful browsing before the common schema exists.
It will need independent validation or adaptation during the later CLI phases.
The requested schema filename is reserved with an intentionally rejecting schema,
so a placeholder cannot accidentally claim that hardware data validates. The
pyproject scaffold contains only tool settings, with packaging disabled and no
project metadata, build backend, or installed entry point.

#### Final Outcome

Move five definitions to hardware/<category>/<namespace>/<component>/definition.yml,
the VENTUNO manual to its sources/user_manual.md, standards to docs/standards,
and planning documents to docs/planning. Preserve the manual, four other hardware
definitions, and standards byte-for-byte. Preserve every original VENTUNO semantic
field except its source path; add metadata without silently resolving contradictions.

The VENTUNO definition now records 15 onboard inventory entries, 76 typed connection
relationships, four resource-conflict groups, 37 section/date references, and input/
output power dependencies. Keep the current 288 named pins and all six source
contradictions. Add an explicit MIPI-DSI interface using the published JMEDIA table,
bringing its interface count from 25 to 26. Carrier outputs outside limited nets
are not described as unlimited current; their complete current limits are unknown.

Generate all five component reference READMEs and docs/catalog.md directly from
YAML using a source-only documentation utility. Add preparation tests and a local
evidence collector. These are self-evaluation, not the independent AC evaluator.
All G0-G5 gates remain pending. Update current links and planning scope while
retaining historical journal contents; the relocation baseline maps old paths.

#### Implementation Impact

- hardware/: relocated definitions and source, enriched VENTUNO YAML, generated pages.
- docs/: catalog, moved standards/planning, source baseline and local evidence.
- src/ysl_components/reference_pages.py: deterministic Markdown generation only.
- tests/: layout/enrichment checks and local evidence capture.
- schemas/component.schema.json and pyproject.toml: explicitly inactive scaffolds.
- README.md and CONTRIBUTING.md: layout, generation, and gate guidance.

#### Verification Required

T0 safe parsing, original field/byte preservation, provenance and typed-reference
resolution, navigation/fragments, and journal-prefix hashes. T1 execute the page
generator, reproduce its outputs, run the eight preparation cases, and demonstrate
specified corruptions/markup/duplicate-key failures. No physical hardware, query
CLI, Linux installation, distribution build, or independent gate evaluation is
claimed. Capture raw results and distinguish initial red tests from the final run.

#### Related Records

- DEVNOTES: DEV-2026-11-19-001, DEV-2026-11-19-002
- Tests: TEST-2026-11-19-003, TEST-2026-11-19-004
- Source: hardware/controllers/arduino/ventuno_q/sources/user_manual.md;
  docs/evidence/reorganization-2026-11-19/baseline.json

#### Next Steps

Human review of the preparation can use docs/catalog.md and the local evidence
index. Future execution of the CLI plan starts with a fresh P0 baseline including
these additions and independent G0 evaluation, rather than treating this work as
approval or completion of any CLI phase.

#### Deferred Decisions

Approve the common schema, stable IDs, protected evaluator, and CLI behavior
through the original gates. Packaging remains contingent on explicit human
validation at G4; neither the scaffold files nor this decision grants approval.

---

---


### DEV-2026-11-19-004 - Build a schema review draft without adopting it or implementing packages

**Date:** 2026-11-19  
**Time:** 07:31 America/New_York  
**Engineer:** Codex  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

The user requested the next schema phase for review and an explicit stop before
implementing packages. Replace the reserved rejecting schema with a concrete
review candidate, without migrating the hardware catalog or creating a CLI package.

#### Context and Constraints

The earlier plan's independent G0/G1 evidence has not been established. The latest
instruction authorizes drafting schemas for review; it is not a gate approval.
Existing hardware files and pyproject.toml must retain their bytes. Historical
journals remain append-only. Existing dependencies are available; no dependency
installation, project package, build backend, or console entry point is needed.

#### Solutions Considered

- One permissive schema accepting arbitrary legacy dictionaries.
- A production migration/query implementation alongside the schema.
- Modular closed schemas, typed facts and uncertainty, proposed identities, and
  authored synthetic fixtures with a test-only parsing/semantic review harness.

#### Trade-offs

Typed facts and explicit uncertainty add verbosity but distinguish unknown,
uncited, derived, conflicting, and documented statements. Closed object shapes
catch misspelled fields; extensible fact keys/capabilities still require semantic
review and a complete field map in P2. JSON Schema checks shape/types, while local
checks handle references, connector positions, range ordering, inheritance/power
cycles, identity collisions, and matching verification evidence. Neither layer
can establish source truth, authenticated approvals, or physical compatibility.

#### Final Outcome

Build six Draft 2020-12 schemas at version 1.0.0-draft.1, each marked
x-ysl-review-status: draft-not-approved, plus a five-entry proposed identity registry.
The draft uses flat component objects, board/ic_family/module discrimination,
connector-scoped pin coordinates, typed quantities with dimension/unit rules,
source-bearing claims, explicit unknown/conflicting states, and scoped verification.

Author board, family, and module fixtures and review tests before replacing the
placeholder. Keep parser/reference helpers under tests/ only. The review loader
uses a JSON-compatible YAML subset with duplicate keys, tags, aliases/anchors,
multiple documents, implicit dates, and nonfinite values rejected. Schema references
resolve through a local registry with explicit format checking and no downloads.

The previously reserved-schema assertion in the preparation test is updated to
require an explicitly unapproved draft, while packaging-disabled checks remain.
New tests require unchanged hardware/pyproject bytes and reject every legacy wrapped
definition under the new schema, proving migration has not been silently performed.
Only catalog status text in the existing reference generator is updated.

Prepare the schema guide, acceptance-coverage limitations, and a new evidence folder.
Preserve earlier preparation evidence. No G0/G1 or later gate is approved; no
runtime query package, migration, build, installation, or publication is performed.

#### Implementation Impact

- schemas/: six modular schema files, identity registry, review guide.
- tests/: synthetic fixtures, schema-review tests/helpers and evidence collector.
- docs/evidence/schema-review-2026-11-19/: before hashes, red baseline, retained
  collector failure, final raw/structured outcomes and digest manifest.
- README, CONTRIBUTING, planning documents and generated catalog: current draft status.
- hardware/** and pyproject.toml: unchanged.

#### Verification Required

T0 metaschema validation, positive and negative shape/quantity/provenance examples,
identity proposal checks, preservation hashes, and current documentation links.
T1 execute strict parsing and semantic-reference rejection cases and the full local
regression suite, with no skips or empty collection. Capture failures and retests;
results remain local self-evaluation rather than independent gate evidence.

#### Related Records

- DEVNOTES: DEV-2026-11-19-002, DEV-2026-11-19-003
- Tests: TEST-2026-11-19-005, TEST-2026-11-19-006, TEST-2026-11-19-007
- Source: schemas/README.md, schemas/component.schema.json,
  schemas/identity-registry.json, docs/evidence/schema-review-2026-11-19/README.md

#### Next Steps

Human review of the schema/identity decisions and independently controlled test
baseline. Freeze an accepted revision before any catalog migration or production
query implementation. Stop here as requested; no package implementation follows.

#### Deferred Decisions

Approve or revise the draft IDs, fact/unit vocabulary, member overrides and source
requirements. Complete field-by-field migration mapping and real query diagnostic
contracts later. G4 human packaging approval remains separate and pending.

---

---


### DEV-2026-11-19-005 - Adopt approved schema IDs and migrate the five hardware definitions

**Date:** 2026-11-19  
**Time:** 10:52 America/New_York  
**Engineer:** Codex  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

The user approved the delivered schema/ID candidate and requested the next phase.
Execute P2 catalog migration with preservation evidence, then stop for G2 review.

#### Context and Constraints

Approval was actually received in the conversation: "approved. Please move to next
phase." The repository review record binds the exact schema/registry bytes to that
instruction. It is not an agent-generated signature, proof of an independent G0
runner, G2 migration acceptance, or G4 packaging approval. No CLI/package phase is
included. Original YAML comments/values, source bytes, and journal history matter.

#### Solutions Considered

- Keep legacy wrappers behind an adapter without migrating the stored definitions.
- Edit definitions by hand without complete preservation mapping.
- Preserve originals first, convert deterministically to the approved contract,
  and compare every original value with declared destinations independently.

#### Trade-offs

Typed facts and repeated provenance increase document size but keep unknown,
conflicting, and uncited values explicit. Supplemental nested values use descriptive
path-keyed typed facts rather than unrestricted blobs. Unit suffixes/explicit units
are interpreted without numeric conversion; unknown numeric contexts fail conversion.
The field map is complete but agent-writable, so it does not replace independent
source review. Historical schema/registry draft annotations stay byte-identical;
the dated human adoption record records their approval separately.

#### Final Outcome

Migrate five definitions to schema 1.0.0-draft.1 and the approved stable IDs. Preserve
345 named pin records, 3403 original data leaves, variants/profiles, shared Uno
connections, H-bridge states, reset/USI constraints, voltage/timing limits, onboard
relationships, all six source discrepancies, and the unselected Bluetooth claims.
All components retain not_verified physical verification state.

Every source leaf maps to one or more exact-type/exact-value destinations. Every
additional leaf has a recorded generated value and reason, enabling detection of
changed unit labels, identity metadata, source state, and other structural additions.
Original comments/formatting remain in byte-identical .yml.txt snapshots. Approved
schema/registry bytes, source/standards bytes, and pyproject.toml are unchanged.

A source-only migration utility validates every converted component before writes
and always reads the original snapshots. Update the existing documentation renderer
for the flat contract and regenerate six pages. Adapt phase-specific regression
expectations to compare archived originals and valid migrated documents, while
retaining original synthetic negative cases and packaging restrictions.

Two defects were detected and corrected: schematics versus schematic source-kind
classification, and a review walker that interpreted a fact called processor as a
reference. Fix the converter/checker, not the approved schemas; add a reserved-name
regression. Retain the failures and final test evidence in the P2 evidence folder.

#### Implementation Impact

- hardware/**/definition.yml: five normalized instances and stable IDs.
- tools/migrate_catalog.py: reproducible snapshot-based conversion; no query CLI.
- tests/migration_checks.py and test_migration.py: independent leaf comparison,
  direct manual oracles, real-schema checks, deterministic conversion and corruptions.
- tests/schema_review_support.py: typed map traversal correction.
- src/ysl_components/reference_pages.py: normalized-data documentation support.
- docs/evidence/migration-2026-11-19/: originals, baseline, field map, failures/results.
- docs/reviews/schema-approval-2026-11-19.md: received human schema/ID approval.
- Current README, CONTRIBUTING, schema guide and planning documents: adoption status.

#### Verification Required

T0 all five approved-schema instances and semantic references; exact source and
addition accounting; original source/schema/registry/config/journal preservation.
T1 strict parsing, direct 22 UNO and 260 expansion-table comparisons, family/safety
facts, six corruption detections, deterministic conversion and reference generation.
Retain failures and retests. Record local self-evaluation; do not claim bench tests,
independent acceptance, Linux execution, query CLI behavior, or package installation.

#### Related Records

- DEVNOTES: DEV-2026-11-19-002, DEV-2026-11-19-003, DEV-2026-11-19-004
- Tests: TEST-2026-11-19-008 through TEST-2026-11-19-011
- Source: docs/reviews/schema-approval-2026-11-19.md;
  docs/evidence/migration-2026-11-19/README.md and baseline.json

#### Next Steps

Human G2 review of the migrated definitions, source-field mapping, generated pages,
and retained evidence. Do not start P3 query/validator CLI work or packaging here.

#### Deferred Decisions

Independent evaluator infrastructure remains unestablished. G2 acceptance, P3
query behavior, and later human G4 packaging approval remain separate decisions.

---

---

### DEV-2026-11-19-006 — Record G2 approval and freeze the P3 query contract

**Date:** 2026-11-19  
**Time:** 14:40 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** ACCEPTED  
**Type:** DECISION

#### Problem

P3 cannot start until G2 is decided. The user approved the current P2 draft.
The approval has to be recorded as a human decision, and the query invocation,
filters, JSON envelope, and exit codes have to be frozen before the module is
treated as the contract.

#### Context and Constraints

The user statement is exactly: "G2 is approved". It names no other reviewer.
The approved draft is commit `5442a1a62359bfb34b04b29e4d277d2ecbd7f820`: five
migrated definitions, the field map, six unresolved VENTUNO discrepancies, and
the AC-205 corruption detections. An agent-written review file is only a
cross-reference. The statement does not approve packaging, publication, page
acceptance, or copying definitions into embedded projects. Exit codes 0–5 were
proposed and are now an implementation contract. Development invocation remains
`python -m ysl_components` with an explicit catalog path.

#### Solutions Considered

- Treat the P2 evidence README as approval because its checks passed.
- Invent a named reviewer or mark the gate template as signed.
- Record the user's sentence against the draft digests, freeze revision 1 of the
  query contract, and implement only the local loader and read-only operations.

#### Trade-offs

A repository copy can be edited by the same agent that implements the queries, so
it cannot prove an independent review. Citing the chat statement keeps the
decision attached to the user without pretending the file is the approval.
Freezing rejection of a stale index, rather than a silent rebuild, makes AC-308
observable and keeps queries read-only. Exit 1 has no portable catalog input, so
the contract exposes one fault seam instead of leaving that code untested.

#### Final Outcome

G2 is approved for the identified P2 draft. The six VENTUNO discrepancies stay
unresolved and verification stays `not_verified`. P3 may implement catalog
loading, validation, and the operations `list`, `search`, `show`, `pin`, `pins`,
`interface`, `export`, and `validate`. Stdout is the JSON envelope. Diagnostics
go to stderr. Exit codes are 0 success, 1 unexpected failure, 2 invalid
usage or data, 3 not found, 4 ambiguous pin alias, and 5 unsupported schema.
No wheel, installed command, page regeneration, or embedded-project inclusion
is part of this decision.

#### Implementation Impact

- `docs/reviews/g2-approval-2026-11-19.md`: cross-reference of the user statement.
- `docs/planning/CLI_QUERY_CONTRACT.md`: frozen revision 1.
- `src/ysl_components/`: loader, query operations, and `python -m` entry.
- `tests/test_query_contract.py`: executable AC-301–AC-308 cases.
- Planning status text that still said G2 was pending.

#### Verification Required

T0 compile and import the new modules. T1 run each operation through a
subprocess against fixed catalogs, including invalid, missing, ambiguous,
unsupported-schema, export, read-only, and stale-index cases. T2 confirm the
module reads the real five-definition catalog without writing it. T3 rerun the
existing repository suite and record the pre-existing Linux baseline mismatch
separately. Do not predict a pass. Windows remains unexecuted.

#### Related Records

- DEVNOTES: DEV-2026-11-19-005, DEV-2026-11-19-007
- Tests: Pending
- Source: `docs/reviews/g2-approval-2026-11-19.md`;
  `docs/planning/CLI_QUERY_CONTRACT.md`

#### Next Steps

Implement the frozen contract and record the executed results. G3 is still open.
Packaging remains unauthorized.

#### Deferred Decisions

Independent evaluator infrastructure, Windows execution, G3 acceptance, P4 page
generation, and G4 packaging approval remain separate. JSON Schema library
message text is not frozen.

---

---

### DEV-2026-11-19-007 — Accept the Linux line-ending gap in the Windows byte baseline

**Date:** 2026-11-19  
**Time:** 14:42 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** ACCEPTED  
**Type:** DECISION

#### Problem

On this Linux checkout, several preservation tests fail before any P3 edit.
Their recorded SHA-256 values match the CRLF translation of the current LF git
blobs, not the LF bytes. The git objects are LF. The P2 journal says the
baseline was captured on Windows.

#### Context and Constraints

Files that already match as LF stay exact. Files that differ only by a newline
translation match after LF is rewritten to CRLF. A content change matches
neither digest. Schema, manual, and standards bytes are not to be rewritten to
chase the Windows hash. Journal prefix checks stay exact. G2 approved the
current draft, which is the LF commit, not a CRLF working tree.

#### Solutions Considered

- Convert the git blobs to CRLF so the recorded hashes match.
- Leave the suite red and block P3.
- Compare each preserved file with its recorded digest or, when the file has no
  CR, with the digest of its CRLF translation. Keep content changes failing.

#### Trade-offs

Accepting the newline translation lets Linux run the preservation tests without
hiding a changed character. It does not recreate the Windows capture and does
not prove those files were reviewed again. Rewriting bytes would change the
draft the user approved. Leaving the tests red would make every later run look
like a new P3 failure.

#### Final Outcome

Accept this limit for Linux execution. Preservation checks may treat a pure
LF-to-CRLF translation as the recorded Windows digest. They still reject any
other byte difference. Do not modify schema, source-manual, standards, or
snapshot bytes for this reason. The P2 guard that forbade `python -m`
modules is retired because G2 now authorizes that entry point; packaging files
remain forbidden. Owner of a future Windows rehash: the G3 reviewer. Until
then, AC-206 byte identity is established on Linux only up to newline
translation.

#### Implementation Impact

- `tests/test_migration.py`
- `tests/test_schema_review.py`
- `tests/test_repository_content.py`

#### Verification Required

T0 rerun the three preservation tests on Linux and confirm content-identical
files pass while the assertion still computes both digests. No Windows run is
claimed. This decision does not by itself pass P3 query tests.

#### Related Records

- DEVNOTES: DEV-2026-11-19-005, DEV-2026-11-19-006
- Tests: Pending
- Source: `docs/evidence/migration-2026-11-19/baseline.json`

#### Next Steps

Keep the newline comparison local to those preservation tests. Do not use it as
a reason to change hardware facts.

#### Deferred Decisions

A reviewer-owned Windows rehash of the baseline. Not required to implement P3.

---

---

### DEV-2026-11-19-008 — P3 query module is implemented on Linux only

**Date:** 2026-11-19  
**Time:** 14:49 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

DEV-2026-11-19-006 authorized the query module. The implementation now exists, and the verification outcome needs its own record. G3 is still open.

#### Context and Constraints

The module follows query contract revision 1. It is started with `python -m ysl_components` and an explicit catalog path. Stdout is the JSON envelope. Diagnostics go to stderr. Queries do not modify the catalog. A stale index is rejected rather than rebuilt. Packaging files were not added. The run is self-evaluated on Linux. Windows was not executed.

#### Solutions Considered

- Wait for a Windows run before recording any implementation result.
- Record the Linux execution and leave Windows as not executed.

#### Trade-offs

Recording the Linux result makes the evidence findable. Calling the phase accepted on one platform would hide the missing Windows run required by AC-307. The implementation status does not close G3.

#### Final Outcome

The loader and the eight operations are implemented. Linux unittest coverage passed, including AC-301 through AC-308 and the previous local suite. Windows AC-307 is not executed. G3, page generation, packaging, and publication remain unauthorized. The six VENTUNO discrepancies stay unresolved.

#### Implementation Impact

- src/ysl_components/__init__.py, __main__.py, loader.py, query.py, and cli.py
- tests/test_query_contract.py
- docs/planning/CLI_QUERY_CONTRACT.md

#### Verification Required

The Linux T0, T2, and T3 runs are recorded. No further product change is implied by this entry. A Windows run remains required before AC-307 can be called complete.

#### Related Records

- DEVNOTES: DEV-2026-11-19-006, DEV-2026-11-19-007
- Tests: TEST-2026-11-19-012, TEST-2026-11-19-013, TEST-2026-11-19-014, TEST-2026-11-19-015
- Source: src/ysl_components/cli.py; docs/planning/CLI_QUERY_CONTRACT.md

#### Next Steps

G3 review of the real loader, including reviewer-made catalogs. Do not package.

#### Deferred Decisions

Windows execution, G3 acceptance, P4 page generation, and G4 packaging approval.

---

---

### DEV-2026-11-19-009 — Record G3 approval and freeze P4 page generation

**Date:** 2026-11-19  
**Time:** 16:20 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** ACCEPTED  
**Type:** DECISION

#### Problem

P4 cannot start until G3 is decided. The user approved the current P3 draft.
The approval has to be recorded as a human decision, and the page outputs, fact
oracle, and packaging-denial reasons have to be frozen before the generator is
treated as the P4 contract.

#### Context and Constraints

The user statement is exactly: "G3 is approved." It names no other reviewer.
The approved draft is commit `efbe756a74911bf1e9d468756b29c0ca8ba806ec`, the
merge of pull request 2. An agent-written review file is only a cross-reference.
The statement does not approve packaging, publication, or copying definitions
into embedded projects. Windows AC-307 was not executed. That gap stays
disclosed under the approval. Query contract revision 1 stays as frozen.
Page generation remains the existing script, not a new query operation.

#### Solutions Considered

- Treat the Linux query run as G3 approval because its tests passed.
- Invent a named reviewer or mark the blank gate template as signed.
- Record the user's sentence against the P3 digests, freeze page-contract
  revision 1, and limit the next code change to generated pages plus a denial
  that never builds a distribution.

#### Trade-offs

A repository copy can be edited by the same agent that generates the pages, so
it cannot prove an independent review. Citing the chat statement keeps the
decision attached to the user without pretending the file is the approval.
Keeping page generation out of `python -m ysl_components` avoids a second query
contract. A denial function with no success path makes AC-501 observable without
opening packaging. Carrying the Windows gap forward is more accurate than
treating the user's sentence as a Windows run.

#### Final Outcome

G3 is approved for the identified P3 draft. The six VENTUNO discrepancies stay
unresolved and verification stays `not_verified`. P4 may adapt
`src/ysl_components/reference_pages.py` to the migrated definitions, check links
and the literal fact oracle, and assemble a self-evaluated evidence bundle.
`request_package_build` may only classify denials. It must not call a builder
or write a wheel, sdist, or `dist/` directory. G4 remains open.

#### Implementation Impact

- `docs/reviews/g3-approval-2026-11-19.md`: cross-reference of the user statement.
- `docs/planning/CLI_PAGE_CONTRACT.md`: frozen revision 1.
- `tests/page_checks.py` and `tests/test_page_contract.py`: executable AC-401–AC-405 and AC-501 cases.
- `src/ysl_components/reference_pages.py`: migrated-page adaptation.
- `src/ysl_components/packaging.py`: denial only.
- Planning status text that still says G3 is pending.

#### Verification Required

T0 parse the new modules. T1 generate the six pages and compare them with the
fact oracle, including a second clean-directory run and a metacharacter label.
T2 show that a removed link, broken fragment, missing image, and a VENTUNO D5
signal changed to PD5 are detected, and that a manifest detects a missing or
changed evidence file. Run each AC-501 request and confirm no distribution is
written. T3 rerun the existing suite, including AC-301 through AC-308. Do not
predict a pass. Windows remains unexecuted. Do not claim an independent reviewer.

#### Related Records

- DEVNOTES: DEV-2026-11-19-006, DEV-2026-11-19-008
- Tests: Pending
- Source: `docs/reviews/g3-approval-2026-11-19.md`;
  `docs/planning/CLI_PAGE_CONTRACT.md`

#### Next Steps

Implement the frozen page contract and record the executed results. G4 is still
open. Packaging remains unauthorized.

#### Deferred Decisions

Independent evaluator infrastructure, Windows execution, G4 packaging approval,
and publication remain separate.

---

---

### DEV-2026-11-19-010 — P4 pages are generated and packaging stays closed

**Date:** 2026-11-19  
**Time:** 16:46 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** IMPLEMENTED  
**Type:** DECISION

#### Problem

DEV-2026-11-19-009 authorized P4. The generator and denial module now exist, and the verification outcome needs its own record. G4 is still open.

#### Context and Constraints

Page contract revision 1 is the behavior contract. Query contract revision 1 is unchanged. Page generation stays `python src/ysl_components/reference_pages.py` and is not a query operation. `request_package_build` has no success path. The run is self-evaluated on Linux. Windows was not executed. The first full-suite run failed because this environment had no `jsonschema` install; the passing rerun used jsonschema 4.23.0 and referencing 0.30.2, the versions named by the P3 record. Those installs are environment tools, not project packaging.

#### Solutions Considered

- Treat the passing page tests as G4 approval.
- Add a build backend while refusing to publish.
- Record the Linux evidence, keep the Windows gap, and leave packaging unimplemented.

#### Trade-offs

A local evidence bundle makes the candidate reviewable. Calling the phase accepted would hide the missing Windows run, the missing independent reviewer, and the open G4 decision. Filling in packaging would cross the gate the user left for later.

#### Final Outcome

The six generated pages follow the migrated definitions. The fact oracle, link checks, clean-directory match, label escaping, manifest tamper check, and AC-501 denials passed on Linux inside the 37-test run. Forty-five manual images remain missing and are inventoried as source limitations. The six VENTUNO discrepancies stay unresolved. Verification stays `not_verified`. No wheel, sdist, or `dist/` directory was produced. G4, publication, and copying definitions into an embedded project remain unauthorized.

#### Implementation Impact

- `src/ysl_components/reference_pages.py`
- `src/ysl_components/packaging.py`
- `tests/page_checks.py`, `tests/test_page_contract.py`, `tests/collect_page_evidence.py`
- `docs/catalog.md` and the five component README pages
- `docs/evidence/pages-2026-11-19/`
- `docs/reviews/g3-approval-2026-11-19.md`
- `docs/planning/CLI_PAGE_CONTRACT.md`

#### Verification Required

The Linux T0, T1, and T3 runs are recorded, including the pre-adaptation failure and the missing-jsonschema failure. No further product change is implied by this entry. A Windows run remains required before page views or AC-307 can be called complete on that platform.

#### Related Records

- DEVNOTES: DEV-2026-11-19-009
- Tests: TEST-2026-11-19-016, TEST-2026-11-19-017, TEST-2026-11-19-018, TEST-2026-11-19-019, TEST-2026-11-19-020, TEST-2026-11-19-021
- Source: `docs/planning/CLI_PAGE_CONTRACT.md`; `docs/evidence/pages-2026-11-19/README.md`

#### Next Steps

Human G4 review of this candidate and its evidence bundle. Do not package unless that review authorizes this exact candidate.

#### Deferred Decisions

Independent evaluator infrastructure, Windows execution, G4 packaging approval, and publication remain separate.

---

---

### DEV-2026-11-19-011 — Record scoped G4 approval and stop before packaging

**Date:** 2026-11-19  
**Time:** 17:03 America/New_York  
**Engineer:** Cursor cloud agent  
**Status:** BLOCKED  
**Type:** DECISION

#### Problem

The user authorized G4 packaging for the Ventuno Q only. The statement has to be recorded as a human decision, and P5 may start only if the packaging contract can ship that one definition without shipping the rest of the catalog.

#### Context and Constraints

The user statement is exactly: "authorized for the Ventuno Q." It names no other reviewer. The bound candidate is commit `bbf013354b3ac7d4fdc9be8b44090634b431b118`, the merge of pull request 3, with a clean tree when the statement was applied. The authorized identity is `arduino/ventuno-q`. The statement does not authorize the other four definitions or publication. An agent-written review file is only a cross-reference. The approval cannot be widened to make the contract fit.

#### Solutions Considered

- Package all five definitions because the candidate commit contains them.
- Fill in `pyproject.toml` with only the Ventuno Q definition and call that the approved catalog.
- Record the scoped approval and leave packaging closed, because neither package matches both the statement and the contract.

#### Trade-offs

The first option ships definitions the user did not authorize. The second option invents a one-component distribution the acceptance rows do not define, and it would omit catalog data AC-503 treats as part of the packaged catalog. Recording the block leaves the installable CLI unbuilt. That is the limit the statement and the contract together impose.

#### Final Outcome

G4 is approved for `arduino/ventuno-q` only, bound to commit `bbf013354b3ac7d4fdc9be8b44090634b431b118` and definition SHA-256 `db3c7fe1af1a69a61dae54787cf7f70b5222a9c066284c75e7f83e455d6826c2`. P5 does not start. The plan packages the five-definition catalog as one unit: P5 includes that catalog, AC-502 requires the installed command to serve it, and AC-503 fails missing catalog data. The page contract still denies an external G4 with `packaging_closed_until_external_g4`. No wheel, sdist, or installed command was produced. `pyproject.toml` stays the inactive scaffold. Publication and G5 remain unauthorized. The six VENTUNO discrepancies stay unresolved and verification stays `not_verified`.

#### Implementation Impact

- `docs/reviews/g4-approval-2026-11-19.md`: cross-reference of the user statement and the block.
- Planning status text in `docs/planning/CLI_IMPLEMENTATION_PLAN.md`, `docs/planning/CLI_ACCEPTANCE_TESTS.md`, and `docs/planning/CLI_PAGE_CONTRACT.md`. The AC-502 through AC-505 rows and the denial table are unchanged.
- `README.md` and `CONTRIBUTING.md`: current status points at the scoped decision.
- `pyproject.toml`, `src/ysl_components/packaging.py`, schemas, and hardware definitions: unchanged.

#### Verification Required

Static inspection that the scaffold still has no project table, build backend, or `dist/` directory, and that the contract text still packages the whole catalog. Do not predict a packaging pass. AC-502 through AC-505 stay unexecuted. Do not claim an independent reviewer or a Windows run.

#### Related Records

- DEVNOTES: DEV-2026-11-19-002, DEV-2026-11-19-010
- Tests: TEST-2026-11-19-022
- Source: `docs/reviews/g4-approval-2026-11-19.md`;
  `docs/planning/CLI_IMPLEMENTATION_PLAN.md`

#### Next Steps

None for packaging under this statement. A later human decision would have to cover the catalog package the contract defines, or revise that contract, before P5 can start. This entry does not request either choice.

#### Deferred Decisions

Publication, G5 review of an installed package, Windows execution, independent evaluation, and any contract revision that would define a one-component distribution remain separate.

---

---
