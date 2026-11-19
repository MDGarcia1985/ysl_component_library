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
