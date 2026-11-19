<!-- Generated from hardware/**/definition.yml. Do not edit manually. -->
# Hardware catalog

[Repository overview](../README.md) · [Implementation plan](planning/CLI_IMPLEMENTATION_PLAN.md)

Browse reference pages by category and namespace. The catalog uses the user-approved schema and stable IDs. CLI queries and packaging remain separate gated work.

| Category | Namespace | Reference page | Definition | Recorded source issues |
| --- | --- | --- | --- | --- |
| controllers | arduino | [Arduino Uno R3](../hardware/controllers/arduino/uno_r3/README.md) | [YAML](../hardware/controllers/arduino/uno_r3/definition.yml) | 0 |
| controllers | arduino | [Arduino VENTUNO Q](../hardware/controllers/arduino/ventuno_q/README.md) | [YAML](../hardware/controllers/arduino/ventuno_q/definition.yml) | 6 |
| controllers | microchip | [ATtiny25 / ATtiny45 / ATtiny85](../hardware/controllers/microchip/attiny_x5/README.md) | [YAML](../hardware/controllers/microchip/attiny_x5/definition.yml) | 0 |
| drivers | ti | [L293 / L293D](../hardware/drivers/ti/l293_family/README.md) | [YAML](../hardware/drivers/ti/l293_family/definition.yml) | 0 |
| sensors | generic | [HC-SR04](../hardware/sensors/generic/hc_sr04/README.md) | [YAML](../hardware/sensors/generic/hc_sr04/definition.yml) | 0 |

## Migration status

The user approved the schema/ID candidate and authorized P2 migration. All five definitions now use that contract. [Migration evidence](evidence/migration-2026-11-19/README.md) preserves original bytes and a complete source-field map. G2 review, query CLI implementation, and G4 packaging approval remain separate; packaging is disabled.
