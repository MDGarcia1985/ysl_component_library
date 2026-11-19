# Phased Hardware Catalog and CLI Plan

**Status:** The user authorized G4 packaging for `arduino/ventuno-q` only, bound to commit `bbf013354b3ac7d4fdc9be8b44090634b431b118`. That scope does not authorize the other four definitions or publication. P5 has not started, because this plan packages the five-definition catalog as one unit. G5 remains pending. No independent evaluator is claimed. Windows AC-307 was not executed.  
**Date:** 2026-11-19  
**Gates:** User approval covers the schema/ID candidate, P2 execution, G2 for that draft, G3 for the P3 query draft, and a G4 scope limited to `arduino/ventuno-q` on the P4 candidate. That G4 scope does not authorize packaging the catalog. Windows AC-307 remains not executed. G5 remains pending. Publishing is not authorized.  
**Related decision:** DEV-2026-11-19-002

## Objective and scope

Turn the five existing hardware definitions into a browsable, validated catalog
with stable IDs and a local query interface. Preserve hardware facts, uncertainty,
sources, variants, and constraints through migration. Generate browsing pages and
collect independently reviewable evidence before building an installable CLI.

The initial planning request was for the plan and test contracts only. A later
user instruction separately authorized the folder reorganization, VENTUNO source
enrichment, and generated reference pages before executing this plan. Those
preparation changes do not approve any gate or establish independent acceptance.
The user then explicitly requested schemas for review and a stop before package
implementation. The [schema draft](../../schemas/README.md), proposed IDs, and
local review harness were prepared under that instruction. The user then approved
the delivered candidate and requested the next phase. The
[approval record](../reviews/schema-approval-2026-11-19.md) binds its exact bytes.
All five definitions are now migrated for G2 review; no independent evaluation or
migration acceptance is implied. The pyproject file remains
an inactive scaffold. CLI packaging starts only after explicit human validation
of the pre-package evidence.

The preparation baseline and local test results are in
[docs/evidence/reorganization-2026-11-19](../evidence/reorganization-2026-11-19/README.md).
They are self-evaluated. P0 must capture and independently review the actual
prepared starting state rather than assume the earlier directory layout remains.

Hardware remains the catalog's subject. The CLI is tooling for that catalog.
Firmware, application examples, automatic electrical compatibility judgments,
remote synchronization, a hosted API, and publishing are separate future work.
Independent source review and static checks do not establish bench verification.

## Required sequence

```text
P0: Freeze acceptance tests, source baseline, and independent oracle
  -> G0: Human approves the test contract and trusted evaluation setup
P1: Build schemas, identity rules, and parsing/reference primitives
  -> G1: Review the schema, IDs, fixtures, and validation evidence
P2: Migrate definitions and organize hardware directories
  -> G2: Review complete preservation evidence and source samples
P3: Build catalog validation and local queries
  -> G3: Review independent behavior and corruption-test results
P4: Generate browsing pages and assemble reproducible evidence
  -> G4: HUMAN VALIDATES THE EXACT CANDIDATE AND EVIDENCE
P5: Package and test the installed CLI
  -> G5: Human reviews packaging evidence; publication is separately authorized
```

Review G1-G3 may use a human reviewer or an evaluator controlled independently of
the implementing agent. Contract changes, factual corrections, and exceptions
always require human review. G0, G4, and G5 require an actual human decision.
Another agent sharing the same writable files and credentials is not independent.

## Governance and evidence rules

- Define and freeze tests and expected observations before implementing the
  behavior under test. The [acceptance contracts](CLI_ACCEPTANCE_TESTS.md) are the
  starting specification, not executable proof.
- Keep authoritative fixtures, oracle results, required-case inventory, approval
  records, and evaluator outside the implementation agent's write access.
- Candidate identity includes all implementation, hardware, schema, and generation
  inputs. Use a commit plus clean-tree check when available; otherwise record a
  complete sorted path/SHA-256 inventory. Account for untracked files too.
- Run tests on the candidate being reviewed, without network access for local
  behavior. Capture raw subprocess evidence and evaluator identity.
- Require every applicable case to execute. Review skipped tests, expected-failure
  markers, changed fixtures, reduced coverage, and mutation survivors as failures
  to satisfy the gate. Do not accept a summary emitted by the candidate as proof.
- Preserve failed runs and historical journal entries. Append corrections and
  retests using [TEST_LOG standards](../standards/TEST_LOG_STANDARDS.md) and
  [DEVNOTES standards](../standards/DEVNOTES_STANDARDS.md).
- Source uncertainty may remain when explicitly modeled and accepted. Missing
  verification cannot silently become a passing result or a verified hardware fact.
- If a gate fails, work is limited to investigation and correction for that gate.
  A material scope/contract exception requires a human-reviewed decision and new
  evidence; mandatory human packaging approval cannot be waived by an agent.
- Record reviews with the [gate template](CLI_GATE_REVIEW_TEMPLATE.md). A template,
  checklist tick, local approval file, or elapsed time is never human approval.

## P0 — Establish acceptance tests and the source baseline

**Implement first:** an evaluator and fixtures, before product behavior changes.
Keep the current definitions/manual intact while establishing their baseline.

Deliverables:

1. Freeze the five input definitions, VENTUNO manual, source paths, and hashes.
   Include missing references and known contradictions in the inventory.
2. Inventory every field, pin record, relationship, variant, alias, and source
   discrepancy. Preserve existing decision/test journal bytes as historical records.
3. Translate every AC contract into executable cases and a required-case manifest.
   Create independent synthetic valid/invalid catalogs and expected query answers.
4. Create a human-reviewed source oracle and migration expectation map, separate
   from the eventual migration code. Hardware-specific expectations come from the
   frozen files/manual, with explicit limits on what those sources establish.
5. Prove the evaluator detects changed fixtures, empty/skipped collections, fake
   success, and altered candidates. Arrange reviewer-owned held-out tests.
6. Record expected pre-implementation failures as failures or unimplemented work;
   G0 approves test adequacy, not product behavior. Implementing missing behavior
   is the corrective work those failing acceptance cases require.

**Tests defined first:** AC-001 through AC-004; prepare the fixture/input/expected
result contracts for all subsequent AC groups. If later design review changes a
contract, freeze its reviewed revision before implementing the affected behavior.

**Evidence:** source manifests, independent field inventory, reviewed fact samples,
case inventory, evaluator integrity demonstrations, and the known-red baseline.

**G0 exit:** human approves the contract revision, baseline/oracle, trust boundary,
held-out test process, and required checks. No production schema/migration/query
implementation starts before this gate. If protected infrastructure is unavailable,
use a reviewer-owned local evaluation; do not claim tamper resistance from an
agent-editable test directory alone.

## P1 — Build schemas and stable identities

**User-approved snapshot:** six schemas and the identity registry under
`schemas/`, with authored synthetic fixtures and parsing/semantic checks under
`tests/`. The user approved the delivered schema/ID snapshot and authorized P2.
The approved artifact bytes are unchanged; separate adoption records supersede
their historical draft annotations. Query/packaging gates remain pending. See the
[review evidence](../evidence/schema-review-2026-11-19/README.md).

Deliverables:

- A versioned common schema with reusable typed definitions for quantities, pins,
  connectors, interfaces, variants/profiles, constraints, relationships, sources,
  and verification. Declare the JSON Schema dialect and schema version explicitly.
- Minimum common identity fields: `schema_version`, `id`, `name`, `category`,
  `kind`, and manufacturer value or explicit unknown state. Preserve legacy roots
  as aliases. Document IDs independently of filenames.
- Distinct board, IC-family, and module details. Reject misspelled fields; do not
  hide unmapped legacy content in an unrestricted extension blob to pass migration.
- Explicit states for unknown/conflicting/uncited information and separate evidence
  of document review versus bench measurement. A generated confidence score does
  not substitute for source evidence.
- Variant/profile inheritance and connector-scoped pin references with documented
  cycle, collision, alias, and ambiguity rules. Never infer simultaneous pin use.
- Strict YAML loading and schema/reference primitives required to exercise the
  contracts; the user-facing validation/query interface arrives in P3.

Proposed identity registry to freeze at G1:

| Canonical ID | Kind | Legacy root alias | Family selectors |
| --- | --- | --- | --- |
| `arduino/uno-r3` | board | `arduino_uno_r3` | None |
| `arduino/ventuno-q` | board | `arduino_ventuno_q` | None |
| `microchip/attiny-x5` | ic_family | `attiny_x5` | ATtiny25, ATtiny45, ATtiny85; ATtiny25V, ATtiny45V, ATtiny85V profiles |
| `ti/l293-family` | ic_family | `l293_family` | L293, L293D |
| `generic/hc-sr04` | module | `hc_sr04` | None |

`generic` is a namespace for an unspecified manufacturer, not a manufacturer claim.
Keep variant selection explicit, for example `--variant L293D`; do not manufacture
new independent components for every family selector. Preserve existing canonical
pin labels; any consolidation of shared pins needs an explicit relationship and
complete old-to-new mapping.

**Tests defined first:** AC-101 through AC-105, plus evaluator-integrity checks.

**Evidence:** schemas, ID/alias registry, valid and invalid fixture results,
cross-reference diagnostics, and a schema-to-contract coverage map.

**G1 exit:** identity and representation decisions reviewed; all P1 cases execute
with expected outcomes. Human resolves any contract change before its implementation.

## P2 — Migrate and organize the catalog

**Review candidate accepted for this draft:** all five definitions validate
against the approved snapshot. The [migration evidence](../evidence/migration-2026-11-19/README.md)
contains original bytes, exact source-leaf mappings, generated-field accounting,
direct manual comparisons, corruption checks, and retained failures. The user
approved G2 with the statement "G2 is approved"; the
[review cross-reference](../reviews/g2-approval-2026-11-19.md) cites that
statement and the draft digests. These local checks do not establish an external
trust boundary.

Target layout:

```text
hardware/<category>/<namespace>/<component>/definition.yml
hardware/<category>/<namespace>/<component>/README.md       # generated in P4
hardware/<category>/<namespace>/<component>/sources/        # when sources exist
schemas/
src/ysl_components/                                        # source tooling
tests/                                                     # convenience copy; trusted runner external
docs/catalog.md                                            # generated in P4
docs/standards/                                            # engineering standards
docs/planning/                                             # contracts, plan, and gate template
DEVNOTES.md
TEST_LOG.md
```

The user-authorized preparation has already placed standards under
`docs/standards/`, planning documents under `docs/planning/`, and hardware in the
target hierarchy. P2 must validate that relocation and migrate the data contract
and IDs; it is not complete merely because the folders exist.
Organize definitions by category and identity, including `controllers/arduino/ventuno_q`,
`controllers/microchip/attiny_x5`, `drivers/ti/l293_family`, and
`sensors/generic/hc_sr04` under `hardware/`.

Deliverables:

- Migration code plus an independently checked field-by-field transformation map.
- All five schema-valid definitions, preserving facts and all semantically
  accounted source records: 29 Uno, 288 VENTUNO, 8 ATtiny, 16 L293, 4 HC-SR04.
- Original source/manual snapshots with unchanged bytes, stable source identifiers,
  and updated current references. Preserve licensing/attribution uncertainty.
- Old-path/root-to-new-path/ID mapping. Update current README/contribution links;
  preserve historical journal paths and supply a migration map for locating them.
- Explicit human-reviewed dispositions for any true data correction. Migration
  itself is not authorization to resolve the manual's contradictory claims.

**Tests defined first:** AC-201 through AC-206, with prior groups retained.

**Evidence:** complete conservation report, all source-to-destination field mappings,
separate quantitative/reference checks, deterministic rerun, and corruption results.

**G2 exit:** no unexplained data loss/change; source byte preservation confirmed;
reviewer samples source facts, all six VENTUNO discrepancies, family differences,
and shared-pin handling. Every deliberate corruption in AC-205 is detected.

## P3 — Build validation and local queries

**Local implementation of revision 1:** the [query contract](CLI_QUERY_CONTRACT.md)
freezes invocation, filters, the JSON envelope, and exit codes 0–5. Development
invocation is `python -m ysl_components` with an explicit catalog path. The user
approved G3 for that draft. The cross-reference is
[g3-approval-2026-11-19.md](../reviews/g3-approval-2026-11-19.md). Windows AC-307
remains not executed. No wheel or installed command is produced here.

Deliverables:

- Catalog loader and validator that check schema shape, unique identity, reference
  integrity, quantities, variants, aliases, and derived-index freshness.
- Local `list`, `search`, `show`, `pin`, `pins`, `interface`, `export`, and `validate`
  operations. Freeze argument/filter behavior and JSON response schemas first.
- Development invocation `python -m ysl_components`; the evaluator provides the
  source import path and explicit catalog location. No wheel, source distribution,
  editable installation, or installed command is built during this phase.
- Structured responses with schema/catalog identity, selected component/variant,
  relevant constraints, source references, and uncertainty. Preserve enum states
  and typed quantities; no blanket assertion that a connection is safe.
- Explicit exit codes, deterministic ordering, JSON-only stdout in machine mode,
  diagnostics on stderr, safe overwrite handling, and read-only queries.

**Tests defined first:** AC-301 through AC-308; rerun relevant earlier groups.
Use reviewer-created catalogs and black-box subprocesses, not only real-library
golden files. Run Windows and Linux checks; identify missing platforms honestly.

**Evidence:** raw query/export/validation transcripts, independent expected answers,
negative cases, round-trip comparisons, read-only hashes, platform/environment
records, and stale-index/canned-answer demonstrations.

**G3 exit:** local behavior meets every applicable contract; negative tests reject
bad inputs for the expected reason; expected answers were not derived from query
or migration code. Unverified platform coverage remains an explicit unresolved gate item.

## P4 — Generate browsing pages and collect evidence

The preparation utility `src/ysl_components/reference_pages.py` already generates
reference pages from the legacy-shaped YAML. Reuse or adapt it under the frozen
contracts; its local tests do not replace this phase's independent validation.

**Local candidate:** pages are generated from the migrated contract under
[CLI_PAGE_CONTRACT.md](CLI_PAGE_CONTRACT.md). Evidence is under
[docs/evidence/pages-2026-11-19](../evidence/pages-2026-11-19/README.md).
A later human statement authorized packaging for `arduino/ventuno-q` only. The
[G4 cross-reference](../reviews/g4-approval-2026-11-19.md) records that scope.
It does not open P5, because this plan packages the five-definition catalog.
Packaging stays closed. The local run is self-evaluated and does not include Windows.

Deliverables:

- A generated category/manufacturer catalog and per-component reference pages.
  Show capabilities, family selectors, connector/pin tables, power constraints,
  sources, known conflicts, and verification limits.
- Navigation/link/fragment checks and a source-asset limitations inventory. Missing
  manual images remain identified gaps unless legitimate copies are supplied.
- Deterministic generation with clearly marked generated files and a documented
  regeneration command. Distinguish generated content from manually authored guidance.
- Complete evidence bundle described in the acceptance contracts, plus a concise
  review index linking raw artifacts, comparisons, screenshots, failures, and reruns.
- Independent reviewer reproduction on the candidate frozen for G4. The evidence
  manifest records the toolchain, required cases, all inputs and artifact digests.

**Tests defined first:** AC-401 through AC-405; regression of AC-001 through AC-308.
Run packaging-denial case AC-501 without starting a package build. No release
artifact, build backend configuration, distribution installation, or publication
is produced before human approval.

**Evidence:** catalog/page outputs, visual captures, link and fact checks,
determinism results, mutation detections, independent reproduction, and limitations.

### G4 — Mandatory human validation before packaging

The human reviewer receives the complete evidence bundle and exact candidate
digest, not only an agent-written success summary. They must:

1. Verify the trusted evaluator/fixtures and the candidate/evidence identities.
2. Inspect migration conservation and independently trace selected facts to sources.
3. Review positive, negative, held-out, and corruption-test results, all skipped or
   unexecuted checks, unresolved hardware claims, and platform coverage.
4. Browse the generated catalog and representative component/connector/variant pages.
5. Reproduce selected queries and verify the independent full-run report.
6. Explicitly authorize packaging of that candidate, with scope and conditions,
   through a human-controlled approval channel. Retain a trusted external record.

No agent can approve G4, write approval on the human's behalf, infer it from
silence, or reuse it for changed data/behavior. Until approval arrives, stop at a
review-ready evidence bundle. This mandatory approval comes directly from the
user's instruction: "then package the cli after human validation of the evidence."

## P5 — Package the approved CLI

**Entry condition:** verified G4 human approval for the exact pre-package candidate.

Deliverables:

- `pyproject.toml`, dependency/build metadata, console entry point
  `ysl-components`, and versioned distribution artifacts.
- Approved catalog and schemas included in the package. Offline operation and
  provenance are preserved when the repository is absent.
- Clean-environment wheel installation and installed-command tests on Windows and
  Linux. Compare packaged data/schema digests with the G4-approved inputs.
- Source distribution rebuild/install evidence and artifact contents/attribution
  inventory. Confirm an appropriate licensing/distribution decision before release.
- Packaging evidence bundle and a new candidate identity binding packaging changes
  to the approved pre-package data and behavior.

**Tests defined first:** AC-502 through AC-505; retain AC-501 as a packaging-entry
check and rerun relevant behavior/regression cases through the installed command.

**G5 exit:** human reviews installed-package evidence and approved-input equality.
Any changes to catalog facts, schema semantics, query behavior, or browsing content
return to affected phases and renewed G4 review. Packaging-only changes can be
reviewed as the explicit G4-to-G5 diff. Uploading/publishing remains a separate
human authorization; package creation does not imply permission to publish.

## Completion criteria and deferred work

The plan is fulfilled only when the gated phases have their required evidence
and review records. Report product behavior, static checks, human acceptance, and
hardware verification separately. Never mark a phase complete because its files
exist or because an agent says its own tests passed.

Versioned remote catalog synchronization, distribution hosting, automatic updates,
an agent skill/MCP adapter, and additional onboard-component definitions are future
phases. They need their own test-first contracts and review gates after this local
catalog and packaging workflow is established.
