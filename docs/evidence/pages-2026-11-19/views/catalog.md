Excerpt of generated Markdown for review. The generated page is authoritative.

```markdown
<!-- Generated from hardware/**/definition.yml. Do not edit manually. -->
# Hardware catalog

[Repository overview](../README.md) · [Implementation plan](planning/CLI_IMPLEMENTATION_PLAN.md)

Browse reference pages by category and namespace. The catalog uses the migrated definitions and stable IDs. Packaging remains disabled until a later human G4 decision.

| Category | Namespace | ID | Reference page | Definition | Recorded source issues |
| --- | --- | --- | --- | --- | --- |
| controllers | arduino | arduino/uno-r3 | [Arduino Uno R3](../hardware/controllers/arduino/uno_r3/README.md) | [YAML](../hardware/controllers/arduino/uno_r3/definition.yml) | 0 |
| controllers | arduino | arduino/ventuno-q | [Arduino VENTUNO Q](../hardware/controllers/arduino/ventuno_q/README.md) | [YAML](../hardware/controllers/arduino/ventuno_q/definition.yml) | 6 |
| controllers | microchip | microchip/attiny-x5 | [ATtiny25 / ATtiny45 / ATtiny85](../hardware/controllers/microchip/attiny_x5/README.md) | [YAML](../hardware/controllers/microchip/attiny_x5/definition.yml) | 0 |
| drivers | ti | ti/l293-family | [L293 / L293D](../hardware/drivers/ti/l293_family/README.md) | [YAML](../hardware/drivers/ti/l293_family/definition.yml) | 0 |
| sensors | generic | generic/hc-sr04 | [HC-SR04](../hardware/sensors/generic/hc_sr04/README.md) | [YAML](../hardware/sensors/generic/hc_sr04/definition.yml) | 0 |

## Status

These pages are generated from the migrated definitions. The user approved G3 for the local query draft. The cross-reference is [g3-approval-2026-11-19.md](reviews/g3-approval-2026-11-19.md). This generated page is not that approval.

Regenerate from the repository root:

```shell
python src/ysl_components/reference_pages.py
```

Component README files and this catalog are generated. Guidance under a component `sources/` directory is authored separately. Local queries use `python -m ysl_components` with an explicit catalog path. Packaging is disabled until a later human G4 decision.
```
