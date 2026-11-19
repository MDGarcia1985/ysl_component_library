# YSL Component Library

A hardware definition library for describing controllers, driver ICs, sensors,
and actuators. The current scope is **hardware definitions only**: component
identity, pin mappings, electrical characteristics, interfaces, physical details,
and operating constraints.

Definitions are project-independent YAML data. Here, `drivers/` means hardware
driver components, such as H-bridge ICs. Firmware, software drivers, application
logic, and project-specific wiring assignments are outside the current scope.

## Current contents

| Category | Definition | Coverage |
| --- | --- | --- |
| Controllers | [ATtiny x5](hardware/controllers/microchip/attiny_x5/definition.yml) | ATtiny25/45/85 family, pin mapping, power pins, interfaces, reset constraints, and V profiles |
| Controllers | [Arduino Uno R3](hardware/controllers/arduino/uno_r3/definition.yml) | Board pin names, MCU signal mappings, aliases, special pins, and ICSP interface |
| Controllers | [Arduino VENTUNO Q](hardware/controllers/arduino/ventuno_q/definition.yml) | Dual-processor board, UNO and expansion pin mappings, interfaces, power limits, and source discrepancies |
| Drivers | [TI L293 / L293D](hardware/drivers/ti/l293_family/definition.yml) | Shared PDIP-16 pinout, variant ratings, H-bridge interfaces, logic states, and constraints |
| Sensors | [HC-SR04](hardware/sensors/generic/hc_sr04/definition.yml) | Trigger/echo interface, pinout, electrical and timing characteristics, ranging, and dimensions |

Browse the generated [hardware catalog](docs/catalog.md) or open the README beside
each definition. The VENTUNO Q definition is transcribed from the included
[user manual](hardware/controllers/arduino/ventuno_q/sources/user_manual.md). Conflicting claims and
incomplete pinouts are identified under its `source` section. There are no
actuator definitions yet.

## Repository layout

```text
README.md
CONTRIBUTING.md
DEVNOTES.md
TEST_LOG.md
pyproject.toml                 Inactive tooling scaffold; packaging disabled
hardware/
  controllers/
    arduino/
      ventuno_q/
        definition.yml
        README.md             Generated reference page
        sources/user_manual.md
      uno_r3/definition.yml
      uno_r3/README.md
    microchip/attiny_x5/definition.yml
    microchip/attiny_x5/README.md
  drivers/ti/l293_family/definition.yml
  drivers/ti/l293_family/README.md
  sensors/generic/hc_sr04/definition.yml
  sensors/generic/hc_sr04/README.md
  actuators/                  Reserved; no definitions yet
schemas/                      Approved schema/ID snapshot and adoption guide
src/ysl_components/           Development package: loader, queries, and python -m entry
tests/test_repository_content.py
tests/test_query_contract.py  Local AC-301–AC-308 cases
docs/
  catalog.md                  Generated browsing index
  standards/                  Annotation, decision, and verification standards
  planning/                   CLI phases, acceptance contracts, and gate template
  evidence/                   Local preparation baselines and check results
```

Each hardware directory groups a definition with its generated reference and
available sources. `generic` identifies an unspecified manufacturer namespace;
it is not a manufacturer claim. Original paths and file digests are recorded in
the [relocation baseline](docs/evidence/reorganization-2026-11-19/baseline.json).

## Planned catalog and CLI

The [phased implementation plan](docs/planning/CLI_IMPLEMENTATION_PLAN.md) describes
schemas and stable IDs, migration, validation and local queries, generated browsing
pages, and evidence collection. [Acceptance contracts](docs/planning/CLI_ACCEPTANCE_TESTS.md)
define required tests before implementation, with independent evaluation and
deliberate corruption cases. Use the [gate review template](docs/planning/CLI_GATE_REVIEW_TEMPLATE.md)
to record reviews against an exact candidate and evidence bundle.

The user-authorized layout preparation and source enrichment have been completed.
The user [approved the schemas and IDs](docs/reviews/schema-approval-2026-11-19.md).
All five definitions now use that contract. The [P2 migration evidence](docs/evidence/migration-2026-11-19/README.md)
includes original bytes, a complete field map, source checks, and corruption tests.
The user approved G2 for that draft; the cross-reference is
[g2-approval-2026-11-19.md](docs/reviews/g2-approval-2026-11-19.md). Local catalog
queries run as `PYTHONPATH=src python -m ysl_components --catalog . <operation>`
under the [query contract](docs/planning/CLI_QUERY_CONTRACT.md). The user approved
G3 for that query draft; the cross-reference is
[g3-approval-2026-11-19.md](docs/reviews/g3-approval-2026-11-19.md). Windows query
coverage was not run. Generated pages follow the
[page contract](docs/planning/CLI_PAGE_CONTRACT.md). The user authorized G4
packaging for `arduino/ventuno-q` only; the cross-reference is
[g4-approval-2026-11-19.md](docs/reviews/g4-approval-2026-11-19.md). That scope
does not cover the other four definitions. Packaging remains unimplemented;
`pyproject.toml` still has no build backend or project entry point. Publishing
is not authorized.

The schema set includes six modular schemas and synthetic board/family/module
examples. Historical [schema review evidence](docs/evidence/schema-review-2026-11-19/README.md)
is retained. The complete original YAML for each component is archived so that the
pre-migration values and comments remain inspectable.

## VENTUNO Q reference additions

The [board reference](hardware/controllers/arduino/ventuno_q/README.md) includes
the onboard component inventory, typed connection relationships, resource-conflict
groups, power distribution and input dependencies, and section-level citations.
Unknown component identifiers and the six conflicting manual claims remain
explicit. The original pre-migration definitions, including all comments, remain
available in the migration evidence snapshots.

## Regenerating references and checking preparation

With Python 3.11 or newer and PyYAML available, run from the repository root:

```shell
python src/ysl_components/reference_pages.py
python -m unittest discover -s tests -v
```

The full test command also runs schema-review tests, which require jsonschema and
referencing in addition to PyYAML. No project package installation is required.
The generator writes the five component READMEs and `docs/catalog.md` from YAML.
Edit hardware facts in `definition.yml`, then regenerate; do not edit generated
pages directly. These local preparation tests are self-evaluated checks, separate
from the future reviewer-controlled CLI acceptance suite.

## Reading a definition

Open a `.yml` file directly or load it with a YAML parser. No application build
or hardware connection is needed to read the library.

Each current definition uses a component or family identifier as its top-level
`id` in a flat schema-versioned object. Common sections include:

- `pins`: public pin names, mapped device signals, capabilities, aliases, and connector-scoped locations.
- `interfaces`: groups of pins and their roles in a peripheral or connection.
- `facts` and `power_domains`: typed quantities, source states, and supply dependencies.
- `constraints`: electrical, timing, multiplexing, or operating restrictions.
- `variants` and `profiles`: differences within a shared component family.

All definitions validate against the approved common schema. Legacy root keys are
component aliases. Facts distinguish documented, derived, uncited, unknown, and
conflicting values. No migration turns uncited hardware facts into bench results.

`maps_to` identifies the underlying signal; `location`, where provided,
identifies a connector and its position. Board labels and aliases do not always
represent separate physical signals. Capabilities can depend on configuration
and may share pins or peripherals; read the associated constraints.

Numerical facts carry dimension, unit, and rating kind in a quantity object.
Use the exact package, board revision, and variant when interpreting a definition.
Check its cited source before using electrical limits or planning connections;
the presence of a definition does not establish bench verification.

## Contributing hardware definitions

Read [CONTRIBUTING.md](CONTRIBUTING.md) for scope, file placement, YAML
conventions, source requirements, validation, and the submission checklist.
Use the closest existing definition as a starting point while preserving
device-specific differences. The HC-SR04 definition includes a structured source
record; the L293 family demonstrates shared pinouts with variant-specific limits.

The repository also contains these engineering documentation standards:

- [Annotation standards](docs/standards/ANNOTATION_STANDARDS.md)
- [Engineering decision standards](docs/standards/DEVNOTES_STANDARDS.md)
- [Verification record standards](docs/standards/TEST_LOG_STANDARDS.md)

Record material schema or interface decisions in [DEVNOTES.md](DEVNOTES.md) and
executed verification in [TEST_LOG.md](TEST_LOG.md) when applicable, following
those standards. Routine documentation edits do not require a decision entry.

## Local syntax check

There is no production validator CLI or CI workflow yet. Migration tests validate
the real catalog against the approved schemas and semantic checks. For an optional YAML
syntax check, use Python with PyYAML installed:

```shell
python -m pip install PyYAML
python -c "from pathlib import Path; import yaml; paths = sorted(p for p in Path('.').rglob('*') if p.suffix in ('.yml', '.yaml')); [(yaml.safe_load(p.read_text(encoding='utf-8-sig')), print('Parsed:', p)) for p in paths]"
```

Run this from the repository root. It checks the hardware YAML files.
Parsing alone does not check duplicate keys, pin references,
electrical correctness, or agreement with a datasheet; review those separately.

## Current gaps

- The approved schema is adopted; production query/validation CLI and CI enforcement remain future work.
- The ATtiny and Uno definitions do not yet cite source documents. The L293
  definition names a TI document in comments; HC-SR04 includes a source URL.
- The VENTUNO Q reference uses local `assets/` images and site-relative links
  whose targets are not included in this repository.
- The VENTUNO Q manual contains conflicting hardware claims, preserved in the
  definition's source notes. Its transcription received static validation;
  bench verification evidence is not included in the current checkout.

## License

Original component definitions and catalog documentation are licensed under
CC BY 4.0. The Python tooling and tests are licensed under MPL 2.0. See
[LICENSE.md](LICENSE.md) for attribution and third-party source information.
