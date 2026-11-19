# Hardware schemas for review

**Status:** User-approved for P2 migration; adopted by the catalog.  
**Instance version:** `1.0.0-draft.1`  
**Dialect:** JSON Schema Draft 2020-12  
**Scope:** Approved schemas/IDs, synthetic examples, and local review tests.
All five definitions have now been migrated, and the user approved that G2 draft.
Local queries use `python -m ysl_components` with an explicit catalog path.
Package/build metadata, installation, and distribution remain outside this phase.

The user approved the delivered review candidate and requested the next phase.
The [approval record](../docs/reviews/schema-approval-2026-11-19.md) binds the reviewed
schema/ID bytes to that instruction. It does not establish independent evaluation
or approve packaging. See the [CLI plan](../docs/planning/CLI_IMPLEMENTATION_PLAN.md),
historical [schema review evidence](../docs/evidence/schema-review-2026-11-19/README.md),
and current [P2 migration evidence](../docs/evidence/migration-2026-11-19/README.md).

## Review entry points

| File | Responsibility |
| --- | --- |
| [component.schema.json](component.schema.json) | Closed root, identity, common sections, and board/family/module discrimination |
| [common.schema.json](common.schema.json) | Local keys, IDs, typed quantities, facts, uncertainty, and typed entity references |
| [hardware.schema.json](hardware.schema.json) | Pins, connectors, interfaces, processors/components, features, variants, and profiles |
| [relations.schema.json](relations.schema.json) | Connections, resource conflicts, power domains, and constraints |
| [provenance.schema.json](provenance.schema.json) | Source locators, provenance, and scoped verification records |
| [identity-registry.schema.json](identity-registry.schema.json) | Shape of the proposed identity registry |
| [identity-registry.json](identity-registry.json) | Five proposed IDs, current paths, legacy aliases, variant/profile selectors |

Each schema has a distinct URN `$id`; these are identifiers, not download URLs.
The tests register all local resources before validation and require no schema
downloads. To preserve the exact approved bytes, schema files retain their original
`x-ysl-review-status: draft-not-approved` annotation, and the registry retains its
historical `proposed` status. The dated human approval record supersedes those
historical labels for adoption; neither annotation is a runtime packaging approval.

## Adopted identities

| ID | Kind | Legacy alias |
| --- | --- | --- |
| `arduino/uno-r3` | board | `arduino_uno_r3` |
| `arduino/ventuno-q` | board | `arduino_ventuno_q` |
| `microchip/attiny-x5` | ic_family | `attiny_x5` |
| `ti/l293-family` | ic_family | `l293_family` |
| `generic/hc-sr04` | module | `hc_sr04` |

IDs are lowercase `<namespace>/<hyphenated-name>` and independent of filesystem
paths. `generic` records an unspecified manufacturer namespace, not a manufacturer
claim. Alias matching is case-insensitive by `casefold()` for collision checks;
punctuation is not silently normalized. Variants and profiles retain explicit
selectors in separate namespaces, such as `variant:ATtiny85` and
`profile:ATtiny85V`. Changing these choices after review requires a new revision.

## Document structure

The normalized draft is a flat component object rather than a legacy root-name
wrapper. Required fields are `schema_version`, `id`, `name`, `category`, `kind`,
`manufacturer`, `aliases`, `provenance`, `sources`, `verification`, `facts`, `pins`,
`connectors`, and `interfaces`. Empty optional inventories are represented by
omission or explicit empty maps where permitted; empty required pins are invalid.

- `board` requires a processor map. Processor models, architectures, and measured
  characteristics belong to that processor, not an implied global MCU voltage.
- `ic_family` requires family details and at least one variant. Keep a family
  together only where a shared pin/connector model is supported by its sources.
- `module` requires its module type. Manufacturer may be explicitly unknown.
- Other sections cover onboard components, features, connections, constraints,
  conflicts, power domains, variants, and profiles.

Objects reject undeclared fields. Maps accept descriptive local keys but their
values must use the declared types. There is no unrestricted `attributes`,
`extensions`, or raw legacy-data blob to hide unmapped content. Fact names and
capability names are extensible identifiers; this draft does not claim an
exhaustive hardware vocabulary or validate every name's engineering meaning.

## Quantities and factual uncertainty

Every numerical hardware fact uses a quantity with `dimension`, `unit`, and
`rating_kind`, plus at least one of `value`, `min`, `max`, `nominal`, `typical`, or
`values`. Bare numerical facts and mixed untyped arrays are not accepted.

```yaml
facts:
  operating_voltage:
    status: documented
    value:
      dimension: voltage
      unit: V
      min: 2.7
      max: 5.5
      rating_kind: operating
    source_refs: [datasheet_supply]
```

The units table supports voltage, current, time, frequency, length, angle, power,
storage, data rate, temperature, resolution, count, ratio, compute rate, speed,
resistance, and capacitance. It distinguishes decimal storage units from binary
units. A voltage in `mA` is rejected. Unlisted units need an explicit draft change;
there is no automatic unit conversion. Numerical range ordering is a semantic check.

Fact states are deliberately separate from physical verification:

| State | Required payload |
| --- | --- |
| `documented` | Value and at least one source reference |
| `derived` | Value, sources, and a derivation explanation |
| `legacy_uncited` | Value; missing source evidence remains explicit |
| `unknown` | Explanation; no selected value or claims |
| `conflicting` | Explanation and at least two source-bearing claims; no selected value |

Values are text, boolean, or typed quantities. Unknown is not zero, false, or an
empty string. Distinct competing claims are checked semantically; equal text
values cannot masquerade as a conflict simply by naming different sources.
Derived claims are labeled but their arithmetic is not evaluated by the schema.

## Pins, references, and inheritance

Pins have a canonical local key, optional `maps_to`, direction, capabilities,
aliases, typed facts, and provenance. A physical `location` always contains both
connector ID and position. IC package positions use an explicit package connector.
Position is a positive integer or a labeled coordinate such as `A1`.

Connector position counts are optional when unknown. Neither missing positions
nor missing limits are filled with guessed defaults. Position 1 on J1 and position
1 on J2 are distinct; two pins cannot occupy J1 position 1. Numeric representations
`1`, `1.0`, and `"1"` identify the same coordinate for collision checking.

Interface signal roles map to a pin or list of alternative pins. Lists do not
imply simultaneous use. Connections, conflicts, power feeds, and constraint targets
use typed references: `pin:`, `connector:`, `interface:`, `processor:`, `component:`,
`feature:`, or `power_domain:`. Source and evidence references use their separate
record maps. Signal/position references are validated in component scope.

Variant/profile inheritance uses `variant:<key>` or `profile:<key>`. Member scope
contains base pins/interfaces plus ancestor and member overrides. Override entries
are complete typed entities; there is no implicit deep merge or deletion marker.
Facts are intended to override by fact key. Full expansion/merge execution belongs
to the later implementation; the review harness checks names, cycles, and scoped
references without generating migrated catalog definitions.

Pin aliases may be ambiguous in manufacturer documentation; the schema does not
silently choose an alias target. Future query behavior must require disambiguation.
Component ID/alias collisions, in contrast, are rejected by the review checks.

## Sources and verification

`sources` holds document or section records with title, kind, a repository-relative
path or HTTP(S) URL, and optional section/page, date, revision, author, and digest.
A `legacy_note` can instead hold an explicit note about unavailable attribution.
Relative source paths disallow traversal and use the portable filename subset
defined in the common schema. A locator's shape does not prove its existence,
contents, licensing, or authenticity.

Verification has a status plus keyed records with kind, result, reviewer, date,
scope, procedure, observations, and an artifact path. `document_reviewed` requires
a passing document-review record; `bench_tested` requires a passing bench record.
These matching-record rules are semantic checks. A nonempty map of failed tests
cannot justify a passing verification status. Nor does a matching record alone
authenticate human authorship or prove a real bench test: that requires independent
evidence review. Verification applies only to the recorded scope, not every fact.

## Validation boundaries

| Check | JSON Schema | Local semantic/parsing review harness |
| --- | --- | --- |
| Field names, types, kind sections, version, quantity/unit pairs | Yes | Version selection remains explicit |
| Source dates and URI formats | With format checking enabled | No remote retrieval |
| Unknown/conflicting payload shape | Yes | Distinct conflict values checked |
| Source/pin/processor/connector/evidence reference existence | Shape only | Yes |
| ID/alias collisions across documents or registry entries | Shape only | Yes |
| Connector-scoped uniqueness and position bounds | Basic types | Yes |
| Range ordering and values inside declared bounds | No | Yes |
| Inheritance, shared-pin, and power-dependency cycles | No | Yes |
| Passing record matching verification status | Nonempty records | Yes |
| YAML duplicates, tags, anchors/aliases, extra documents | No | Strict review loader |
| Truth, complete migration, physical compatibility, genuine human approval | No | Independent review required; no automated claim |

The strict loader supports a JSON-compatible YAML subset. Boolean literals are
lowercase `true` and `false`; quote boolean-like labels. Dates must be quoted
strings; implicit YAML dates, non-string keys, nonfinite floats, tags, anchors,
aliases, merge keys, multiple documents, and duplicate keys are rejected.

## Examples and review commands

The authored fixtures are synthetic; they are not partial migrations or verified
hardware specifications:

- [Board](../tests/fixtures/schema_review/board.json)
- [IC family with variants/profiles](../tests/fixtures/schema_review/family.json)
- [Module with unknown manufacturer](../tests/fixtures/schema_review/module.json)
- [Tests defined before the schema draft](../tests/test_schema_review.py)
- [Parsing and semantic review helpers](../tests/schema_review_support.py)

With Python 3.11+, PyYAML, jsonschema, and referencing available:

```shell
python -B -m unittest discover -s tests -p test_schema_review.py -v
python -B -m unittest discover -s tests -v
```

No dependencies were installed during schema review. Local verification used Python
3.13.5, PyYAML 6.0.2, jsonschema 4.23.0, and referencing 0.30.2. The tests load
schemas in an offline registry and enable `FormatChecker` explicitly. Tests and
fixtures remain agent-writable, so results are self-evaluated rather than an
independent or human-approved gate decision.

## Approved decisions and migration review

The user approved the schema/ID candidate. The items below describe its review
surface; the completed P2 field map now supports the remaining migration review.
The seven schema-review tests still exercise synthetic inputs, while the separate
migration tests exercise all five real definitions. Historical schema-review hash
checks now use archived pre-migration definitions and current immutable sources;
derived pages must instead match their new definition digests and regeneration.

- Approve or revise the proposed IDs, kind/category distinction, and flat root.
- Approve typed fact wrappers, explicit uncertainty, and the initial unit/type vocabulary.
- Approve position/alias conventions and full-entity member override rules.
- Check that all existing fields can be mapped meaningfully, including USI/PWM
  alternatives, source inconsistencies, module timing, supply limits, protection,
  and physical details. A complete field map is a P2 deliverable, not asserted here.
- Approve source/evidence requirements and externally controlled evaluation.
- Freeze the accepted revision and fixtures before migration. Keep G4 human
  packaging approval separate; schema review does not authorize package work.

## Primary technical references

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Modular schemas and identifiers](https://json-schema.org/understanding-json-schema/structuring)
- [Closed object properties](https://json-schema.org/understanding-json-schema/reference/object)
- [jsonschema local referencing registry](https://python-jsonschema.readthedocs.io/en/stable/referencing/)
- [Explicit format validation](https://python-jsonschema.readthedocs.io/en/stable/validate/#validating-formats)
