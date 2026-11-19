# P2 catalog migration evidence

**State:** Migration complete locally; ready for G2 review.  
**Authorization:** The user approved the delivered schema/ID candidate and requested
the next phase. See the [approval record](../../reviews/schema-approval-2026-11-19.md).
**Boundary:** No query CLI, packaging backend, project installation, or publication
was implemented. No independent evaluation or hardware bench verification is claimed.

## Preserved inputs and mappings

The [baseline](baseline.json) binds all five original YAML snapshots, immutable
sources/standards, approved schema/registry bytes, pyproject bytes, and journal
prefixes before edits. Original comments, whitespace, and attribution remain in
the byte-identical snapshots under `before/`.

| Component ID | Original snapshot | Pins | Original scalar/container leaves |
| --- | --- | --- | --- |
| `arduino/uno-r3` | [Original](before/arduino__uno-r3.yml.txt) | 29 | 206 |
| `arduino/ventuno-q` | [Original](before/arduino__ventuno-q.yml.txt) | 288 | 2722 |
| `microchip/attiny-x5` | [Original](before/microchip__attiny-x5.yml.txt) | 8 | 158 |
| `ti/l293-family` | [Original](before/ti__l293-family.yml.txt) | 16 | 231 |
| `generic/hc-sr04` | [Original](before/generic__hc-sr04.yml.txt) | 4 | 86 |
| Total | Five definitions | 345 | 3403 |

The complete [field map](field-map.json) maps every original leaf pointer to one
or more exact-value destination pointers. No values are rounded, silently corrected,
or discarded. Every additional destination leaf has a recorded value and reason:
schema/identity metadata, structural normalization, explicit unit interpretation,
source-supported classification, or uncertainty. This supports review; it is not
an independent truth oracle merely because it has complete coverage.

The [comparison code](../../../tests/migration_checks.py) does not import the
converter. It inventories the original snapshots independently, requires full
source/destination accounting, compares types and values, and detects missing or
modified generated metadata. The separate deterministic-conversion test invokes
the converter, but it is not the sole preservation oracle.

## Meaningful normalization decisions

- Stable IDs replace legacy root wrappers; those legacy names remain aliases.
- Primary, power, and special pins share `pins`. Preserve all 345 records, including
  Uno SDA/SCL connections with `shared_with`; do not invent header positions.
- Physical coordinates require a connector context. IC pins use a `PACKAGE`
  connector; incomplete position counts are omitted rather than guessed.
- Original ambiguous `direction: power` becomes a typed `facts.direction` value,
  preserving its meaning without guessing input/output/return direction.
- Numeric fields become typed quantities. Suffixes or explicit source units define
  dimensions; unsupported numeric contexts make conversion fail. Decimal/binary
  storage is not silently converted. Count quantities cover discrete counts/indexes.
- Supplemental nested values become named, typed scalar facts with descriptive
  path keys. No opaque JSON blob or unrestricted extension field is used.
- H-bridge truth-table states remain typed facts in a condition constraint; they
  are descriptive source rules, not an executable safety engine.
- Variants/profiles retain their selectors and original facts; profile inheritance
  gains the explicit `variant:` reference while retaining the original selector.
- Onboard components, processor ownership, connections, four resource conflicts,
  and power-domain data retain their source details. Unknown carrier current limits
  remain unknown; outputs outside limited nets are not treated as unlimited current.
- All six VENTUNO source discrepancies survive as source-conflict constraints.
  Bluetooth additionally uses a conflicting fact with both original claims and no
  selected value. All components remain `verification.status: not_verified`.
- Existing manuscript/primary-source citations are carried forward; uncited
  ATtiny/Uno/L293 facts are not upgraded into verified manufacturer facts.

## Tests and required corruptions

[Migration tests](../../../tests/test_migration.py) were written before migration.
Their [initial stderr](before.stderr.txt) and [exit code](before.exit-code.txt)
record a red baseline: seven methods, one failure and five errors, before the flat
definitions, field map, and converter existed. One preservation-only method passed.

The final suite covers all five schema instances, semantic references, complete
field conservation, direct comparison of all 22 UNO mappings and 260 expansion
positions with the manual, PWM/Bluetooth pins, family/profile distinctions, reset/
USI restrictions, current/diode variants, echo/timing constraints, original bytes,
deterministic conversion, and six independently introduced corruptions:

1. Remove JOMEGA_100.
2. Change VENTUNO D5 to the Uno R3's PD5 while preserving the pin count.
3. Swap L293 continuous/peak current facts.
4. Delete ATtiny45.
5. Replace the unresolved Bluetooth claims with a selected documented version.
6. Mislabel current as voltage while retaining the numeric value.

Tests reject these against original/recorded values and metadata. Tests, snapshots,
and mappings remain agent-writable; human sampling and independent reproduction
are still required for stronger assurance.

## Retained defects and corrections

- [First schema failure](first-validation-failure.json): a generated source kind
  used `schematics`; the approved enum is `schematic`. Fix the converter, not the schema.
- [Semantic walker failure](semantic-walker-failure.txt): a fact named `processor`
  was mistaken for a reference field. The checker now walks typed map values
  without interpreting arbitrary entry names; a synthetic regression covers this.

The approved JSON schemas and registry are unchanged. Phase-specific regression
tests now inspect frozen original bytes and valid migrated instances, rather than
requiring the intentionally superseded legacy root shape or unchanged derived pages.
Packaging guards and the original synthetic negative cases remain active.

## Reproduce and inspect

With the existing Python/PyYAML/jsonschema/referencing environment:

```shell
python -B tools/migrate_catalog.py
python -B src/ysl_components/reference_pages.py
python -B -m unittest discover -s tests -v
python -B tests/collect_migration_evidence.py
```

The converter always reads preserved snapshots; it does not migrate already-migrated
data again. It writes only the registered definitions and P2 field map. The source
documentation generator updates component references and the catalog for the flat
schema. No installed command or project package is needed.

- [Final raw test results](after.stderr.txt)
- [Final stdout](after.stdout.txt)
- [Final exit code](after.exit-code.txt)
- [Structured case/subcase and navigation observations](checks.json)
- [Current file digest inventory](manifest.json)

Root journals are append-only; their original prefixes are verified. The current
manifest excludes itself and root journals so final results can be appended. It is
a local inventory, not a signature or substitute for G2 human approval. Historical
preparation/schema evidence remains historical and is not rewritten to simulate
a current run. The manual's inherited missing assets/site-relative links remain
disclosed limitations. G2 acceptance and later query/packaging phases remain pending.
