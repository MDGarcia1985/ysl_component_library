<!-- Generated from definition.yml; SHA-256: ad4941e41c70630117326bc7bc72eb97260a83827acb7acab92a480eaba3a5e7. Do not edit manually. -->
# ATtiny25 / ATtiny45 / ATtiny85

[Catalog](../../../../docs/catalog.md) · [Hardware YAML](definition.yml)

This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.

## Identity and capabilities

| Property | Value |
| --- | --- |
| ID | microchip/attiny-x5 |
| Schema version | 1.0.0-draft.1 |
| Kind | ic_family |
| Manufacturer | Microchip |
| Legacy aliases | attiny_x5 |
| Named pin records | 8 |
| Interfaces | 6 |
| Verification | not_verified |

## Component facts

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |

## Variants

### ATtiny25

**Inherits:** Base component

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| flash_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 2048 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| sram_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 128 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| eeprom_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 128 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### ATtiny45

**Inherits:** Base component

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| flash_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 4096 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| sram_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 256 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| eeprom_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 256 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### ATtiny85

**Inherits:** Base component

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| flash_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 8192 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| sram_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 512 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| eeprom_bytes | legacy_uncited | dimension: storage; unit: byte; rating kind: unspecified; value: 512 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Profiles

### ATtiny25V

**Inherits:** variant:ATtiny25

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| inherits | legacy_uncited | ATtiny25 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| voltage_profile | legacy_uncited | v_variant | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| max_clock_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; max: 10000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### ATtiny45V

**Inherits:** variant:ATtiny45

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| inherits | legacy_uncited | ATtiny45 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| voltage_profile | legacy_uncited | v_variant | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| max_clock_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; max: 10000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### ATtiny85V

**Inherits:** variant:ATtiny85

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| inherits | legacy_uncited | ATtiny85 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| voltage_profile | legacy_uncited | v_variant | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| max_clock_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; max: 10000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Power and electrical summary

### standard

**Role:** rail; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | legacy_uncited | dimension: voltage; unit: V; rating kind: operating; min: 2.7; max: 5.5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### v_variant

**Role:** rail; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | legacy_uncited | dimension: voltage; unit: V; rating kind: operating; min: 1.8; max: 5.5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Interfaces

| ID | Type | Processor | Signal roles / pins | Sources |
| --- | --- | --- | --- | --- |
| USI_SPI | spi | Not specified | MOSI: PB0; MISO: PB1; SCK: PB2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| USI_I2C | i2c | Not specified | SDA: PB0; SCL: PB2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| ISP | programming | Not specified | MOSI: PB0; MISO: PB1; SCK: PB2; RESET: PB5; VCC: VCC; GND: GND | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PWM | pwm | Not specified | TIMER0  OC0A: PB0; TIMER0  OC0B: PB1; TIMER1  OC1A: PB0, PB1; TIMER1  OC1B: PB3, PB4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| ADC | adc | Not specified | channels  ADC0: PB5; channels  ADC1: PB2; channels  ADC2: PB4; channels  ADC3: PB3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| ANALOG_COMPARATOR | analog_comparator | Not specified | positive input: PB0; negative input: PB1 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### ADC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| resolution_bits | legacy_uncited | dimension: resolution; unit: bit; rating kind: resolution; value: 10 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Connector summary

| ID | Type | Positions | Processor | Sources |
| --- | --- | --- | --- | --- |
| PACKAGE | ic_package | Not specified | Not specified | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Pin tables

### PACKAGE

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PB0 | 5 | PB0 |  | gpio, pwm, spi_mosi, usi_data_input, i2c_sda, analog_comparator, adc_reference_input, pin_change_interrupt | MOSI, DI, SDA, AIN0, OC0A, OC1A, AREF, PCINT0 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PB1 | 6 | PB1 |  | gpio, pwm, spi_miso, usi_data_output, analog_comparator, pin_change_interrupt | MISO, DO, AIN1, OC0B, OC1A, PCINT1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PB2 | 7 | PB2 |  | gpio, adc, spi_clock, usi_clock, i2c_scl, timer_external_clock, external_interrupt, pin_change_interrupt | ADC1, SCK, USCK, SCL, T0, INT0, PCINT2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PB3 | 2 | PB3 |  | gpio, adc, pwm, crystal_oscillator, external_clock_input, pin_change_interrupt | ADC3, OC1B, XTAL1, CLKI, PCINT3 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PB4 | 3 | PB4 |  | gpio, adc, pwm, crystal_oscillator, clock_output, pin_change_interrupt | ADC2, OC1B, XTAL2, CLKO, PCINT4 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| PB5 | 1 | PB5 |  | hardware_reset, adc, debugwire, pin_change_interrupt, gpio_conditional | RESET, RESET_N, ADC0, DW, PCINT5 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| VCC | 8 | Not specified |  | power_input | VDD |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| GND | 4 | Not specified |  | ground_reference | VSS |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Constraints and known issues

### reset

**requirement:** Preserve source constraint group: reset

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| pin | legacy_uncited | PB5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| default_function | legacy_uncited | hardware_reset | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| gpio_requires_fuse_change | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| fuse | legacy_uncited | RSTDISBL | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| warning | legacy_uncited | Disabling RESET prevents ordinary low-voltage ISP programming. High-voltage programming may be required to recover the device.<br> | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### gpio

**requirement:** Preserve source constraint group: gpio

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| standard_available | legacy_uncited | dimension: count; unit: count; rating kind: unspecified; value: 5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| conditional_available | legacy_uncited | dimension: count; unit: count; rating kind: unspecified; value: 1 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### peripheral_multiplexing

**requirement:** Preserve source constraint group: peripheral_multiplexing

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| simultaneous_functions | legacy_uncited | restricted | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### voltage

**requirement:** Preserve source constraint group: voltage

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| gpio_high_level | legacy_uncited | VCC | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| five_volt_tolerant_at_3v3 | legacy_uncited | no | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

### clock

**requirement:** Preserve source constraint group: clock

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| factory_oscillator_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; value: 8000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| factory_clock_divider | legacy_uncited | dimension: ratio; unit: 1; rating kind: unspecified; value: 8 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |
| default_cpu_clock_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; value: 1000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt) |

## Sources

- legacy_snapshot: [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/microchip__attiny-x5.yml.txt)

Original source snapshots and the [migration field map](../../../../docs/evidence/migration-2026-11-19/field-map.json) preserve historical context. No unresolved source claim was silently corrected.
