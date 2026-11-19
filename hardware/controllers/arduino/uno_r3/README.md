<!-- Generated from definition.yml; SHA-256: 75d1a787a0bc25efe6ea6e8b0a28a13e99536c6faf3a5f4a5891aef3410bf424. Do not edit manually. -->
# Arduino Uno R3

[Catalog](../../../../docs/catalog.md) · [Hardware YAML](definition.yml)

This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.

## Identity and capabilities

| Property | Value |
| --- | --- |
| ID | arduino/uno-r3 |
| Schema version | 1.0.0-draft.1 |
| Kind | board |
| Manufacturer | Unknown: Manufacturer not specified in the original definition. |
| Legacy aliases | arduino_uno_r3 |
| Named pin records | 29 |
| Interfaces | 1 |
| Verification | not_verified |

**Declared pin capabilities:** adc, adc_reference_input, analog_comparator, clock_output, external_interrupt, gpio, ground_reference, hardware_reset, i2c_scl, i2c_sda, logic_voltage_reference, onboard_led, pin_change_interrupt, power_input, pwm, regulated_power_output, regulated_power_rail, spi_chip_select, spi_clock, spi_miso, spi_mosi, timer_external_clock, timer_input_capture, uart_rx, uart_tx, usart_external_clock

**Verification limits:** status not_verified. Source statements on this page are not bench verification.

## Component facts

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| logic_voltage | legacy_uncited | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| clock_hz | legacy_uncited | dimension: frequency; unit: Hz; rating kind: unspecified; value: 16000000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |

## Processors

### mcu

**Model:** ATmega328P

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |

## Power and electrical summary

## Interfaces

| ID | Type | Processor | Signal roles / pins | Sources |
| --- | --- | --- | --- | --- |
| ICSP | programming | Not specified | MOSI: D11; MISO: D12; SCK: D13; RESET: RESET; VCC: 5V; GND: GND | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |

## Connector summary

| ID | Type | Positions | Processor | Sources |
| --- | --- | --- | --- | --- |

## Pin tables

### Unnumbered or logical board connections

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D0 | Not specified | PD0 |  | gpio, uart_rx, pin_change_interrupt | RX, RXD, UART_RX, PCINT16 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D1 | Not specified | PD1 |  | gpio, uart_tx, pin_change_interrupt | TX, TXD, UART_TX, PCINT17 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D2 | Not specified | PD2 |  | gpio, external_interrupt, pin_change_interrupt | INT0, PCINT18 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D3 | Not specified | PD3 |  | gpio, pwm, external_interrupt, pin_change_interrupt | OC2B, TIMER2_B, INT1, PCINT19 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D4 | Not specified | PD4 |  | gpio, timer_external_clock, usart_external_clock, pin_change_interrupt | T0, XCK, PCINT20 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D5 | Not specified | PD5 |  | gpio, pwm, timer_external_clock, pin_change_interrupt | OC0B, TIMER0_B, T1, PCINT21 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D6 | Not specified | PD6 |  | gpio, pwm, analog_comparator, pin_change_interrupt | OC0A, TIMER0_A, AIN0, PCINT22 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D7 | Not specified | PD7 |  | gpio, analog_comparator, pin_change_interrupt | AIN1, PCINT23 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D8 | Not specified | PB0 |  | gpio, timer_input_capture, clock_output, pin_change_interrupt | ICP1, CLKO, PCINT0 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D9 | Not specified | PB1 |  | gpio, pwm, pin_change_interrupt | OC1A, TIMER1_A, PCINT1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D10 | Not specified | PB2 |  | gpio, pwm, spi_chip_select, pin_change_interrupt | SS, SPI_SS, OC1B, TIMER1_B, PCINT2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D11 | Not specified | PB3 |  | gpio, pwm, spi_mosi, pin_change_interrupt | MOSI, COPI, SPI_MOSI, OC2A, TIMER2_A, PCINT3 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D12 | Not specified | PB4 |  | gpio, spi_miso, pin_change_interrupt | MISO, CIPO, SPI_MISO, PCINT4 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| D13 | Not specified | PB5 |  | gpio, spi_clock, pin_change_interrupt, onboard_led | SCK, SPI_SCK, LED_BUILTIN, PCINT5 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A0 | Not specified | PC0 |  | gpio, adc, pin_change_interrupt | D14, ADC0, PCINT8 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A1 | Not specified | PC1 |  | gpio, adc, pin_change_interrupt | D15, ADC1, PCINT9 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A2 | Not specified | PC2 |  | gpio, adc, pin_change_interrupt | D16, ADC2, PCINT10 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A3 | Not specified | PC3 |  | gpio, adc, pin_change_interrupt | D17, ADC3, PCINT11 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A4 | Not specified | PC4 |  | gpio, adc, i2c_sda, pin_change_interrupt | D18, ADC4, SDA, TWI_SDA, PCINT12 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| A5 | Not specified | PC5 |  | gpio, adc, i2c_scl, pin_change_interrupt | D19, ADC5, SCL, TWI_SCL, PCINT13 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| SDA | Not specified | PC4 |  | i2c_sda, gpio, adc | A4, D18 | A4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| SCL | Not specified | PC5 |  | i2c_scl, gpio, adc | A5, D19 | A5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| AREF | Not specified | AREF |  | adc_reference_input | ANALOG_REFERENCE |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| RESET | Not specified | PC6 |  | hardware_reset | RESET_N, PCINT14 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| IOREF | Not specified | 5V |  | logic_voltage_reference | VLOGIC |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| VIN | Not specified | VIN |  | power_input | RAW_INPUT |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| 5V | Not specified | VCC |  | regulated_power_rail |  |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| 3V3 | Not specified | 3V3 |  | regulated_power_output |  |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |
| GND | Not specified | GND |  | ground_reference |  |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt) |

## Constraints and known issues

## Sources

- legacy_snapshot: [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__uno-r3.yml.txt)

Original source snapshots and the [migration field map](../../../../docs/evidence/migration-2026-11-19/field-map.json) preserve historical context. No unresolved source claim was silently corrected.
