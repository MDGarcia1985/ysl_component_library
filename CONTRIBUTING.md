# Contributing to YSL Component Library

The current scope is **hardware definitions only**. Contributions describe
component identity, pins, interfaces, electrical characteristics, timing,
dimensions, and operating constraints, with sources supporting those facts.
Documentation needed to interpret or maintain definitions is also welcome.

Firmware, software drivers, runtime libraries, application logic, project-specific
wiring, host pin assignments, and deployment configuration are outside this scope.
The `drivers/` directory describes hardware driver ICs and modules, such as
H-bridge drivers.

## File placement

| Directory | Contents |
| --- | --- |
| `hardware/controllers/` | Microcontrollers and controller boards |
| `hardware/drivers/` | Hardware driver ICs and modules |
| `hardware/sensors/` | Sensing components and modules |
| `hardware/actuators/` | Components that produce motion or another physical output |

Use `hardware/<category>/<namespace>/<component>/definition.yml`, following the
nearest existing model or family. Keep its source documents in `sources/` and its
generated reference in the adjacent `README.md`. Use `generic` only as a namespace
when the manufacturer is unspecified; do not infer a manufacturer from that label.
Preserve existing definition keys and identifiers when correcting a definition.
Add a root inventory entry when adding hardware, then regenerate reference pages
and the catalog using `python src/ysl_components/reference_pages.py`.

Keep reference documents separate from definitions and preserve attribution.
Include local assets referenced by new documentation, or use attributable source
links.

Existing examples:

- [Controller family: ATtiny x5](hardware/controllers/microchip/attiny_x5/definition.yml)
- [Controller board: Arduino Uno R3](hardware/controllers/arduino/uno_r3/definition.yml)
- [Driver family: L293 / L293D](hardware/drivers/ti/l293_family/definition.yml)
- [Sensor module: HC-SR04](hardware/sensors/generic/hc_sr04/definition.yml)

## YAML conventions

All definitions use the [approved common schema](schemas/README.md) at
`1.0.0-draft.1`. Use the closest current definition as a starting point, preserve
stable IDs and aliases, and run schema/semantic/migration checks after edits.

### Formatting

- Use UTF-8 text, two-space indentation, and no tabs.
- Use one YAML document with a flat schema-versioned component object and stable `id`.
- Use stable `snake_case` component identifiers and descriptive field names.
- Preserve manufacturer pin labels and established aliases, including their case.
- Use `true` and `false` for booleans and numeric scalars for measured quantities.
- Quote strings that a YAML parser could interpret as booleans, nulls, dates, or numbers.
- Do not repeat mapping keys; some parsers silently discard earlier values.
- Prefer plain mappings and lists; avoid custom tags, anchors, aliases, and merge keys in new definitions.

### Component identity

- Identify the exact model or family and manufacturer when known.
- Identify the package, board revision, and pin-numbering orientation where relevant.
- Share a family definition only when its common facts apply to every listed variant.
- Keep variant-specific ratings and features explicit.

### Pin mappings

- Use `pins` for primary, power, and special pin records.
- Preserve separate shared connections with `shared_with` and explicit aliases.
- Use `maps_to` for the underlying signal and `location.connector`/`location.position` for a documented physical coordinate.
- Do not substitute an MCU package number for a board header label.
- Record direction, capabilities, and useful aliases where supported by the source.
- Identify the connector when physical pin numbers repeat across headers.
- Distinguish shared signals from independent pins and disclose conditional functions.
- Resolve interface pin references against the definition's pin sections and documented aliases.
- Do not assume every interface value is a pin reference; some fields describe implementation or metadata.

### Quantities and ratings

- Store numeric facts as typed quantities with `dimension`, `unit`, `rating_kind`, and the relevant value/range fields.
- Distinguish minimum, typical, nominal, maximum, and absolute maximum ratings.
- Include relevant test conditions, supply voltage, temperature, and pulse duration for ratings.
- Do not present peak current as continuous current or absolute maximum values as operating recommendations.

### Operating constraints

- Record supply requirements, logic compatibility, shared grounds, and level shifting where applicable.
- Include reset defaults, fuse dependencies, multiplexing restrictions, and software-assisted peripherals.
- Identify timing limits, timeout requirements, thermal requirements, and protection dependencies where applicable.
- Keep host requirements descriptive and independent of a particular project or firmware implementation.

### Unknown specifications

- Do not guess missing specifications or encode unknown values as zero or `false`.
- Omit unsupported optional facts and explain material gaps in a note or source record.
- Label derived values and assumptions separately from documented specifications.
- Do not generalize one manufacturer's module specifications to every similarly named module.

## Sources and attribution

- Cite the manufacturer's datasheet, schematic, pinout, or board documentation when available.
- Record the source document title, URL or repository-relative path, and revision when available.
- Include page, table, or section references for ambiguous or critical limits.
- Identify which package, variant, or board revision each source covers.
- Explain discrepancies between sources rather than silently combining incompatible specifications.
- Preserve source attribution and confirm permission before adding third-party documents or images.

HC-SR04 carries its original datasheet citation under `sources`. L293's original
TI SLRS008D comment is preserved in its source snapshot. ATtiny and Uno facts
remain explicitly legacy/uncited. Include relevant primary citations when adding
or materially correcting hardware facts.

An illustrative source block:

```yaml
sources:
  manufacturer_datasheet:
    title: "<datasheet or board document title>"
    kind: datasheet
    url: "<primary source URL>"
    revision: "<document revision, when available>"
    section: "<relevant page, table, or section>"
```

Replace placeholders with actual citations; this illustrates a fragment of the
approved `sources` structure, not a complete component definition.

## Contribution workflow

1. Review the closest existing definition and gather sources for the exact hardware.
2. Add or update the definition within the hardware-only scope.
3. Preserve existing keys unless a deliberate format change is needed and documented.
4. Validate YAML syntax, inspect parsed types, and review pin references and hardware facts.
5. Update the README inventory, regenerate references/catalog, and update relevant documentation in the same change.
6. Submit a focused change with source citations, verification performed, and remaining uncertainties.

## Validation

The [schemas and IDs](schemas/README.md) have user approval and are adopted by the
catalog. `pyproject.toml` remains inactive. A production validator/query CLI and CI
remain gated future work. See [README.md](README.md#local-syntax-check) for the optional syntax
check using Python and PyYAML. `python -m unittest discover -s tests -v` checks the
current layout/enrichment, generated references, and schema draft. Schema-review
checks require jsonschema and referencing as well as PyYAML. These local checks do not
replace the future independent acceptance suite or establish electrical correctness.

Before submitting:

- Reject duplicate mapping keys and check that scalar types match their intended meaning.
- Check pin labels, numbering, orientation, aliases, and shared signals against the cited pinout.
- Check interface references and variant inheritance against names defined in the same file.
- Verify units, rating categories, conditions, and constraints against cited source documents.
- Verify local documentation links and included assets; identify unavailable external sources.
- Confirm that unrelated definitions and existing public identifiers have not changed accidentally.

State whether validation was document review, parsing, or an executed bench
measurement. Do not claim hardware operation or electrical compatibility from
syntax checks alone. When bench results are supplied, record the exact hardware
revision, setup, procedure, conditions, and observations. Identify measurements
that remain unverified without presenting them as completed tests.

## Engineering records

Follow the repository's documentation standards:

- [Annotation standards](docs/standards/ANNOTATION_STANDARDS.md)
- [Decision standards](docs/standards/DEVNOTES_STANDARDS.md)
- [Verification standards](docs/standards/TEST_LOG_STANDARDS.md)

Keep units, assumptions, and non-obvious hardware constraints close to their
fields. Hardware data files are exempt from mandatory source-code headers under
the annotation standard.

Record material schema, interface, or format decisions in `DEVNOTES.md` and
executed verification in `TEST_LOG.md` when applicable, using the corresponding
standards. The root journals preserve decisions and executed check results.
Keep journals append-only and reference existing DEV or
TEST IDs only when they exist.

Routine formatting and documentation edits do not require behavioral tests or a
decision entry.

The planned catalog/CLI migration follows the
[phased implementation plan](docs/planning/CLI_IMPLEMENTATION_PLAN.md) and
[test-first acceptance contracts](docs/planning/CLI_ACCEPTANCE_TESTS.md). The proposed
schema/ID candidate was explicitly approved by the user, and P2 migration is ready
for G2 review. Production queries and packaging have not been authorized by that
approval. Packaging requires the explicit human evidence review defined by gate G4.

## Submission checklist

- [ ] The change describes hardware and stays within the current scope.
- [ ] The exact component, package, variant, or board revision is clear.
- [ ] New or corrected hardware facts include traceable source citations.
- [ ] YAML parses, keys are unique, and scalar types were checked.
- [ ] Pin references, aliases, units, limits, and operating constraints were reviewed.
- [ ] Relevant README entries, references, and engineering records were updated.
- [ ] The change description states what changed, why, what was checked, and what remains uncertain.

## Licensing

Project licensing is pending confirmation; no repository license file is
currently present. Preserve attribution and verify reuse terms before including
third-party source material.
