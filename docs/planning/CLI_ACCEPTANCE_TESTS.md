# Hardware Catalog and CLI Acceptance Contracts

**Status:** Contracts defined. The user approved G2 for the current P2 draft.
AC-301 through AC-308 now have a frozen query contract and local executable cases.
Independently frozen fixtures and product acceptance are not established.  
**Contract revision:** Draft 1, 2026-11-19  
**Scope:** Schemas and IDs, migration, validation, local queries, generated browsing
pages, evidence review, and subsequent CLI packaging.

These contracts precede implementation. `AC-*` identifies a planned requirement;
it is not a `TEST-*` execution record. Each future execution must receive its own
TEST ID under [TEST_LOG standards](../standards/TEST_LOG_STANDARDS.md). Follow the phases and
gates in the [implementation plan](CLI_IMPLEMENTATION_PLAN.md).

The user-authorized [schema review candidate](../../schemas/README.md) exercises
AC-101 through AC-105 locally, with a coverage/limitations map in its evidence
index. This is not the protected evaluator, stable CLI diagnostic interface, or
human approval required to close a gate. Remaining AC groups are not claimed as
executed by those review tests. The user subsequently approved the schema/ID
snapshot; [P2 migration checks](../evidence/migration-2026-11-19/README.md) now
exercise AC-201 through AC-206 locally. G2 review and independent evaluation
remain separate from a successful local run.

## Trust boundary and test ownership

An agent with write access to the implementation, tests, expected results, and
approval records can make them agree incorrectly. Local hashes, append-only
instructions, and another agent using the same credentials do not prevent that.

Use these controls together:

1. A human freezes the acceptance contract, input fixtures, independently derived
   expected results, required test inventory, and their SHA-256 digests before
   implementation of the behavior being evaluated.
2. Keep the authoritative copies and evaluator outside the implementation agent's
   write access. A protected CI job or a reviewer-owned local checkout can serve
   this role. An editable workspace copy is only a convenience copy.
3. Run the candidate as a subprocess with read-only test inputs. Query tests must
   not import its normalization, migration, rendering, or expected-output helpers.
4. Derive hardware expectations from the preserved pre-migration files and cited
   source sections, with human spot checks. Never regenerate expected results
   from the candidate implementation or accept its own validator as the oracle.
5. The reviewer adds held-out cases and selects corruption targets after the
   implementation is submitted. Record the seed and fixtures in reviewer-owned
   evidence so the run can be reproduced.
6. Capture test collection, skips, failures, raw stdout/stderr, exit codes, and the
   candidate and evaluator identities. A green summary alone is insufficient.
7. Changes to contracts, exclusions, thresholds, expected results, or evaluator
   code require a separate human-reviewed revision and affected-suite rerun.
   Never repair a failed product check by silently relaxing its expectation.

These measures reduce correlated mistakes and tampering. They do not prove
electrical correctness or eliminate deliberate evasion. Until the independent
runner is available, results are explicitly **self-evaluated** and cannot close
the final human evidence gate solely on the agent's report.

## Baseline and oracle rules

The current planning inventory has five logical definitions:

| Current file | Legacy root | Source pin records to account for |
| --- | --- | --- |
| `hardware/controllers/arduino/uno_r3/definition.yml` | `arduino_uno_r3` | 20 primary + 9 special |
| `hardware/controllers/arduino/ventuno_q/definition.yml` | `arduino_ventuno_q` | 288 |
| `hardware/controllers/microchip/attiny_x5/definition.yml` | `attiny_x5` | 6 primary + 2 power |
| `hardware/drivers/ti/l293_family/definition.yml` | `l293_family` | 16 |
| `hardware/sensors/generic/hc_sr04/definition.yml` | `hc_sr04` | 4 |

Freeze actual bytes and a complete field inventory in phase 0; this table is not
a substitute for that inventory. The 345 source pin records include shared
connections and aliases, not necessarily 345 independent electrical signals.
Counts alone do not establish preservation.

The later user-authorized preparation moved these files and added source-linked
VENTUNO inventory, relationships, conflicts, power distribution, and reference
pages without normalizing the data schema or approving IDs. Its
[local baseline/evidence](../evidence/reorganization-2026-11-19/README.md) is not an
independently frozen oracle. P0 must include the added facts and provenance in its
actual baseline. No AC contract is considered executed merely because a similarly
named preparation check exists under `tests/`.

Every scalar and relationship must have a destination or an explicitly reviewed
transformation. Numeric conversion must have declared source units, target units,
and a predetermined exact conversion or tolerance. Uncited facts retain an
explicit legacy/uncited provenance state. Source discrepancies remain unresolved
unless new evidence and human review authorize a correction.

## Test contracts

Each row specifies a required observable outcome. Phase 0 expands rows into
individual executable cases with fixed inputs, expected diagnostic codes and
locations, and independently reviewed expected outputs. If a serialization detail
is unresolved, resolve and freeze that part before implementing its behavior.

### Evaluator integrity — phase 0 and every subsequent gate

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-001 | Change a fixture, expected answer, or evaluator after its approved digest is recorded. | The reviewer-controlled runner rejects the altered evaluation before reporting product success. |
| AC-002 | Collect zero tests, skip a required test, disable assertions, or suppress a subprocess failure. | The gate fails; collected/executed counts and every non-success are present in the report. Run assertion-based tests without optimization. |
| AC-003 | Submit a program that always prints success, always returns an empty catalog, or returns canned answers for the visible corpus. | Positive, negative, and reviewer-supplied synthetic catalogs expose the incorrect behavior. The original candidate's result is reported separately from these deliberately bad candidates. |
| AC-004 | Change a candidate file after evidence is captured; edit a local approval file or replay approval for a different phase. | Subject digest or gate identity no longer matches; the prior evidence and approval cannot authorize that candidate or phase. |

### Schemas, IDs, and parsing — phase 1

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-101 | Valid board, IC-family, and sensor-module fixtures, including unknown manufacturer and uncited legacy facts. | Each validates against its declared schema version; unknown and uncited states remain visible rather than becoming invented values. |
| AC-102 | Missing required identity, invalid ID, unsupported schema version, wrong scalar type, invalid quantity/unit pair, or misspelled field. | Each is rejected with a stable diagnostic code and field location. Unknown versions are not silently interpreted as the current version. |
| AC-103 | Duplicate YAML keys, custom object tags, extra YAML documents, merge/alias constructs forbidden by the contract, or a quoted boolean-like pin label. | Unsafe or forbidden inputs are rejected; the quoted label remains a string. No arbitrary object construction or implicit loss of a duplicate value occurs. |
| AC-104 | Same canonical ID in two files; colliding component aliases; a component moved to another directory. | Duplicates/ambiguity fail explicitly; moving a definition preserves its ID and query result. |
| AC-105 | A dangling pin/connector/source reference, duplicate physical position within one connector, or the same position on different connectors. | Dangling references and same-connector collisions fail; positions scoped to different connectors are valid. |

### Migration and factual preservation — phase 2

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-201 | Migrate the frozen five-definition inventory. | Every source field and relationship is accounted for by the reviewed migration map; no unexplained additions, omissions, or changes. Preserve 345 source pin records semantically, even when shared connections are represented differently. |
| AC-202 | Compare VENTUNO Q with the preserved manual and pre-migration definition. | All 22 UNO table mappings and 260 numbered expansion positions retain their signals and function columns; all 288 named pin entries are accounted for. All six source discrepancies and incomplete-coverage notes survive. |
| AC-203 | Query or inspect discriminating hardware facts. | VENTUNO D5 maps to PB5; Uno R3 D5 maps to PD5. Preserve each board's distinct I2C mapping, the six VENTUNO PWM pins, and its four Bluetooth-conflicting JHAT positions. |
| AC-204 | Check family, profile, and safety distinctions. | Preserve ATtiny25/45/85 and their three V profiles, PB5 reset/fuse restrictions and software-assisted USI behavior; L293 versus L293D ratings/diode distinction; HC-SR04 echo-level and timing constraints. |
| AC-205 | Delete JOMEGA_100, alter a pin's signal while retaining total count, swap continuous/peak ratings, drop a variant, or promote an unresolved fact to verified. | Independent comparisons reject every specified corruption. Run each mutation separately against a disposable copy and identify which contract detected it. |
| AC-206 | Repeat migration from the same frozen inputs; inspect the source/manual snapshots and journal histories. | Semantically deterministic results; source bytes and historical journal prefixes unchanged. Moves have a complete old-path-to-ID/new-path map and updated current links. |

### Validation and local queries — phase 3

Before these cases run, freeze the invocation and response contract. The proposed
development invocation is `python -m ysl_components`; the installed command is
introduced only after the packaging gate. It must accept an explicit local catalog
path so held-out fixtures exercise the real loader.

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-301 | Run validation on valid and deliberately invalid catalogs, including a malformed file among valid files. | Enumerate and diagnose all in-scope files; invalid data produces a nonzero result rather than being silently skipped. Schema shape and semantic-reference checks are both exercised. |
| AC-302 | List/search the baseline and an unrelated reviewer-created catalog. | Independently expected IDs and filter results, deterministic ordering, and no entries read from the wrong catalog. A search with no matches succeeds with an empty result. |
| AC-303 | Show a component, query a canonical pin, resolve an alias, query a connector/interface, and request a family variant. | Structured results preserve identity, pin mapping, relevant constraints, provenance, and uncertainty; ambiguous aliases require disambiguation. Unknown IDs/variants/pins are explicit failures. |
| AC-304 | Query conflicting Bluetooth or CAN facts and uncited legacy facts; request the same output repeatedly. | No invented definitive answer or bench verification. Stable JSON envelope, strings/numbers/booleans retain types, and result ordering is deterministic. |
| AC-305 | Parse stdout as JSON, inspect stderr, and exercise each exit category. | Stdout contains only the response document; diagnostics go to stderr. Proposed codes: 0 success, 1 unexpected failure, 2 invalid usage/data, 3 not found, 4 ambiguous, 5 unsupported schema. Freeze these before implementation. |
| AC-306 | Export YAML/JSON, reload it independently, and compare semantic content. | Identity, quantities, references, constraints, provenance, and uncertainty survive round trips. Existing output files require explicit overwrite authorization. |
| AC-307 | Run with network unavailable, a changed working directory, and catalog paths containing spaces, on Windows and Linux. | Local queries use only the selected catalog, perform no network access, and do not modify definitions or sources. Before/after hashes prove read-only behavior. |
| AC-308 | Corrupt an index or change a definition without refreshing a generated index. | Freshness checks reject or rebuild the derived index; a stale result is never silently returned. |

### Generated browsing pages and evidence — phase 4

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-401 | Generate a catalog and component pages from the migrated data. | All five logical entries appear with working navigation, pin/connector summaries, source links, and visible uncertainty. Check content against the independent fact oracle, not only against renderer output snapshots. |
| AC-402 | Remove a target, break a fragment, introduce a missing image, or inject a distinctive wrong hardware fact in generated output. | Link/asset/anchor checks and factual assertions detect the corresponding fault. Existing unavailable manual assets are explicitly inventoried as source limitations, not counted as working generated assets. |
| AC-403 | Generate twice in clean directories, then view representative pages. | Matching content digests for deterministic outputs; human-readable tables and navigation are usable. Capture views of the catalog, VENTUNO pin/conflict sections, and a family/variant page. |
| AC-404 | Introduce Markdown/HTML metacharacters into reviewer-controlled component labels. | Generated output renders labels as data and does not execute embedded content or corrupt navigation. |
| AC-405 | Reproduce a candidate's evidence run independently, then remove or alter one evidence file. | The reproduction matches semantic outcomes; manifest verification detects missing/changed evidence. Reports identify exact candidate, tests, environment, results, and remaining limitations. |

### Human review and packaging — gate G4, then phase 5

| ID | Input or intervention | Required observable outcome |
| --- | --- | --- |
| AC-501 | Request any package build with approval absent, agent-authored, for the wrong gate, or bound to another candidate. | Packaging remains closed. A local `approved: true` value does not constitute human authorization. Human authorization is verified through a channel outside the candidate's write access. |
| AC-502 | After valid G4 approval, build a wheel/source distribution and install the wheel in a fresh environment outside the repository. | The installed command can list/show/query/export the approved catalog offline; all approved schemas and data are included. It must not rely on the working tree, editable installation, or user-site packages. |
| AC-503 | Compare installed package contents and query outputs with the human-approved catalog and schemas. | Inventory and semantic digests match; declared package metadata and included attribution are correct. Missing data, changed constraints, or silently revised sources fail. |
| AC-504 | Repeat installed-command smoke tests on Windows and Linux and run the relevant regression suite. | Supported platforms pass with captured installation, command, and failure-case evidence. Any missing platform is reported as unverified rather than passed. |
| AC-505 | Change data/schema/query behavior while preparing packaging, or request publication without release approval. | Return to affected pre-package tests and renewed G4 review for changed behavior/data. Publication requires its separate human release gate. |

## Required evidence bundle

Use a unique run directory, for example `evidence/<candidate>/<run-id>/`:

- Manifest with contract revision, candidate tree digest (and commit when
  available), evaluator/fixture digests, platform, interpreter/dependency versions,
  commands, working directories, and SHA-256 digests for every evidence artifact.
- Collected test inventory and structured results mapping every required AC ID to
  executed cases and TEST IDs. Record skips and non-executions explicitly.
- Unedited per-command stdout, stderr, exit status, durations, and runner reports.
- Complete migration field map and before/after comparison; separate source-oracle
  checks, corruption results, and any approved transformations or exclusions.
- Generated browsing pages, deterministic-generation comparison, link report,
  representative screenshots/rendered views, and outstanding limitations.
- Reviewer-controlled reproduction results and a human gate decision bound to
  the same candidate and artifact digests.

An artifact manifest is not a signature or proof of independent execution. The
reviewer must retain its trusted copy outside the agent's writable workspace.
Do not include credentials, personal environment dumps, or secrets.

## Passing and changing a contract

Every required case for a gate must execute and satisfy its expected observation.
No unexplained skips, expected-failure markers, weakened assertions, empty test
collections, or replaced golden files count as a pass. Deliberate invalid inputs
pass their negative case only when rejection is independently observed.

Use `STATIC_ONLY` for source/schema inspection and document comparisons;
use `PASS` only for the specific executed behavior that was observed. Neither
means hardware has been bench tested. See the [gate review template](CLI_GATE_REVIEW_TEMPLATE.md)
for the required reviewer record.
