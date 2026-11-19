<!-- Generated from definition.yml; SHA-256: 87df349469095a0b91948b5d6a126b147656ce3700520abc6e47c6f31ca576a6. Do not edit manually. -->
# HC-SR04

[Catalog](../../../../docs/catalog.md) · [Hardware YAML](definition.yml)

This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.

## Identity and capabilities

| Property | Value |
| --- | --- |
| ID | generic/hc-sr04 |
| Schema version | 1.0.0-draft.1 |
| Kind | module |
| Manufacturer | Unknown: Manufacturer not specified in the original definition. |
| Legacy aliases | hc_sr04 |
| Named pin records | 4 |
| Interfaces | 1 |
| Verification | not_verified |

## Component facts

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| variant_warning | documented | Specifications can vary between HC-SR04 manufacturers and revisions. | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| model | documented | HC-SR04 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| interface_type | documented | trigger_echo_pulse | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__operating_voltage | documented | dimension: voltage; unit: V; rating kind: operating; nominal: 5.0 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__operating_current | documented | dimension: current; unit: mA; rating kind: operating; typical: 15 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__logic__trigger_input | documented | 5V_TTL | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__logic__echo_output | documented | 5V_TTL | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__logic__trigger_high_min_v | documented | dimension: voltage; unit: V; rating kind: unspecified; min: 2.4 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| electrical__logic__trigger_low_max_v | documented | dimension: voltage; unit: V; rating kind: unspecified; max: 0.8 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__nominal_frequency_hz | documented | dimension: frequency; unit: Hz; rating kind: unspecified; nominal: 40000 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__transmitted_cycles_per_measurement | documented | dimension: count; unit: count; rating kind: unspecified; value: 8 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__range__min_mm | documented | dimension: length; unit: mm; rating kind: unspecified; min: 20 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__range__max_mm | documented | dimension: length; unit: mm; rating kind: unspecified; max: 4000 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__stated_resolution_mm | documented | dimension: length; unit: mm; rating kind: resolution; value: 3 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__nominal_detection_angle_deg | documented | dimension: angle; unit: deg; rating kind: unspecified; nominal: 15 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__minimum_measurement_interval_ms | documented | dimension: time; unit: ms; rating kind: unspecified; value: 60 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__conversion__method | documented | echo_pulse_width | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__conversion__equation | documented | distance_m = echo_high_time_s &#42; speed_of_sound_m_per_s / 2 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__conversion__reference_speed_of_sound_m_per_s | documented | dimension: speed; unit: m/s; rating kind: unspecified; value: 340 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ranging__conversion__note | documented | Speed of sound varies with temperature and environmental conditions. | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__positions | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__pitch_mm | documented | dimension: length; unit: mm; rating kind: unspecified; value: 2.54 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__pin_order__0 | documented | VCC | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__pin_order__1 | documented | TRIG | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__pin_order__2 | documented | ECHO | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__header__pin_order__3 | documented | GND | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__nominal_dimensions_mm__width | documented | dimension: length; unit: mm; rating kind: unspecified; value: 45 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__nominal_dimensions_mm__height | documented | dimension: length; unit: mm; rating kind: unspecified; value: 20 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| physical__nominal_dimensions_mm__depth | documented | dimension: length; unit: mm; rating kind: unspecified; value: 15 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

## Power and electrical summary

## Interfaces

| ID | Type | Processor | Signal roles / pins | Sources |
| --- | --- | --- | --- | --- |
| range_measurement | ultrasonic_time_of_flight | Not specified | trigger: TRIG; response: ECHO; power: VCC; ground: GND | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

## Connector summary

| ID | Type | Positions | Processor | Sources |
| --- | --- | --- | --- | --- |
| HEADER | module_header | 4 | Not specified | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

## Pin tables

### HEADER

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VCC | 1 | VCC |  | power_input | 5V, VDD |  | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| TRIG | 2 | TRIG |  | digital_input, ranging_trigger, pulse_trigger_input | TRIGGER, TRIGGER_INPUT |  | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| ECHO | 3 | ECHO |  | digital_output, pulse_width_output, time_of_flight_output | ECHO_OUTPUT, RETURN_PULSE |  | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| GND | 4 | GND |  | ground_reference | GROUND, VSS |  | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

#### TRIG

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| signal__polarity | documented | active_high | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| signal__minimum_high_pulse_us | documented | dimension: time; unit: us; rating kind: unspecified; value: 10 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| signal__recommended_high_pulse_us | documented | dimension: time; unit: us; rating kind: unspecified; value: 10 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

#### ECHO

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| signal__polarity | documented | active_high | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| signal__encoding | documented | pulse_width | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| signal__measurement | documented | round_trip_sound_time | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| signal__output_logic | documented | 5V_TTL | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

## Constraints and known issues

### supply

**requirement:** Preserve source constraint group: supply

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| requires_regulated_5v | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| common_ground_with_host_required | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

### interface

**requirement:** Preserve source constraint group: interface

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| host_must_generate_trigger_pulse | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| host_must_measure_echo_pulse_width | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| echo_level_shift_required_for_3v3_only_host | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

### timing

**requirement:** Preserve source constraint group: timing

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| trigger_min_high_us | documented | dimension: time; unit: us; rating kind: unspecified; min: 10 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| measurement_interval_min_ms | documented | dimension: time; unit: ms; rating kind: unspecified; min: 60 | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| missing_echo_timeout_required_in_host | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| timeout_value_module_dependent | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

### environment

**requirement:** Preserve source constraint group: environment

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| acoustic_crosstalk_possible_with_multiple_sensors | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| reflection_depends_on_target_geometry_and_material | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| not_safety_rated | documented | yes | [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |

## Sources

- legacy_snapshot: [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/generic__hc-sr04.yml.txt)
- datasheet: [HC-SR04 Ultrasonic Ranging Module Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)

Original source snapshots and the [migration field map](../../../../docs/evidence/migration-2026-11-19/field-map.json) preserve historical context. No unresolved source claim was silently corrected.
