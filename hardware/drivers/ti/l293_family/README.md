<!-- Generated from definition.yml; SHA-256: f06b44363eb83aede66911784cade72d2bf87dd2da7a9556cac2ad2a9d54dbaf. Do not edit manually. -->
# L293 / L293D

[Catalog](../../../../docs/catalog.md) · [Hardware YAML](definition.yml)

This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.

## Identity and capabilities

| Property | Value |
| --- | --- |
| ID | ti/l293-family |
| Schema version | 1.0.0-draft.1 |
| Kind | ic_family |
| Manufacturer | Texas Instruments |
| Legacy aliases | l293_family |
| Named pin records | 16 |
| Interfaces | 3 |
| Verification | not_verified |

**Declared pin capabilities:** active_high, digital_input, enable, ground_reference, half_bridge_output, high_impedance, high_impedance_disable, logic_power_input, motor_direction_control, motor_drive, motor_power_input, output_stage_supply, pwm_input, pwm_output_conditional, thermal_dissipation

**Family selectors:** variants L293, L293D

**Verification limits:** status not_verified. Source statements on this page are not bench verification.

## Component facts

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| device_type | legacy_uncited | quadruple_half_h_driver | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Variants

### L293

**Inherits:** Base component

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| continuous_output_current_a | legacy_uncited | dimension: current; unit: A; rating kind: continuous; value: 1.0 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| peak_output_current_a | legacy_uncited | dimension: current; unit: A; rating kind: peak; value: 2.0 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| peak_duration_us | legacy_uncited | dimension: time; unit: us; rating kind: peak; value: 5000 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| integrated_clamp_diodes | legacy_uncited | no | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### L293D

**Inherits:** Base component

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| continuous_output_current_a | legacy_uncited | dimension: current; unit: A; rating kind: continuous; value: 0.6 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| peak_output_current_a | legacy_uncited | dimension: current; unit: A; rating kind: peak; value: 1.2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| peak_duration_us | legacy_uncited | dimension: time; unit: us; rating kind: peak; value: 100 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| integrated_clamp_diodes | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Power and electrical summary

### logic_supply

**Role:** rail; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | legacy_uncited | dimension: voltage; unit: V; rating kind: operating; nominal: 5.0; min: 4.5; max: 7.0 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### motor_supply

**Role:** rail; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | legacy_uncited | dimension: voltage; unit: V; rating kind: operating; min: 4.5; max: 36.0 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### input_logic

**Role:** reference; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| high_min_v | legacy_uncited | dimension: voltage; unit: V; rating kind: unspecified; min: 2.3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| low_max_v | legacy_uncited | dimension: voltage; unit: V; rating kind: unspecified; max: 1.5 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Interfaces

| ID | Type | Processor | Signal roles / pins | Sources |
| --- | --- | --- | --- | --- |
| MOTOR_A | h_bridge | Not specified | enable: EN1_2; inputs: IN1, IN2; outputs: OUT1, OUT2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| MOTOR_B | h_bridge | Not specified | enable: EN3_4; inputs: IN3, IN4; outputs: OUT3, OUT4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| power | power | Not specified | logic: VCC1; motor: VCC2; ground: GND1, GND2, GND3, GND4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### MOTOR_A

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | legacy_uncited | full_h_bridge | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### MOTOR_B

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | legacy_uncited | full_h_bridge | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Connector summary

| ID | Type | Positions | Processor | Sources |
| --- | --- | --- | --- | --- |
| PACKAGE | ic_package | Not specified | Not specified | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Pin tables

### PACKAGE

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EN1_2 | 1 | 1,2EN |  | enable, pwm_input, active_high, high_impedance_disable | 1,2EN, ENA, MOTOR_A_ENABLE |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| IN1 | 2 | 1A |  | digital_input, pwm_input, motor_direction_control | 1A, INPUT1, MOTOR_A_IN1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| OUT1 | 3 | 1Y |  | half_bridge_output, motor_drive, pwm_output_conditional, high_impedance | 1Y, OUTPUT1, MOTOR_A_OUT1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| GND1 | 4 | GND |  | ground_reference, thermal_dissipation | GROUND1, HEATSINK1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| GND2 | 5 | GND |  | ground_reference, thermal_dissipation | GROUND2, HEATSINK2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| OUT2 | 6 | 2Y |  | half_bridge_output, motor_drive, pwm_output_conditional, high_impedance | 2Y, OUTPUT2, MOTOR_A_OUT2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| IN2 | 7 | 2A |  | digital_input, pwm_input, motor_direction_control | 2A, INPUT2, MOTOR_A_IN2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| VCC2 | 8 | VCC2 |  | motor_power_input, output_stage_supply | VS, MOTOR_VCC, VMOTOR |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| EN3_4 | 9 | 3,4EN |  | enable, pwm_input, active_high, high_impedance_disable | 3,4EN, ENB, MOTOR_B_ENABLE |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| IN3 | 10 | 3A |  | digital_input, pwm_input, motor_direction_control | 3A, INPUT3, MOTOR_B_IN1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| OUT3 | 11 | 3Y |  | half_bridge_output, motor_drive, pwm_output_conditional, high_impedance | 3Y, OUTPUT3, MOTOR_B_OUT1 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| GND3 | 12 | GND |  | ground_reference, thermal_dissipation | GROUND3, HEATSINK3 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| GND4 | 13 | GND |  | ground_reference, thermal_dissipation | GROUND4, HEATSINK4 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| OUT4 | 14 | 4Y |  | half_bridge_output, motor_drive, pwm_output_conditional, high_impedance | 4Y, OUTPUT4, MOTOR_B_OUT2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| IN4 | 15 | 4A |  | digital_input, pwm_input, motor_direction_control | 4A, INPUT4, MOTOR_B_IN2 |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| VCC1 | 16 | VCC1 |  | logic_power_input | VSS, LOGIC_VCC, VLOGIC |  | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### EN1_2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT1 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controls__1 | legacy_uncited | OUT2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### IN1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT1 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### OUT1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controlled_by__0 | legacy_uncited | IN1 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controlled_by__1 | legacy_uncited | EN1_2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### GND1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### GND2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### OUT2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controlled_by__0 | legacy_uncited | IN2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controlled_by__1 | legacy_uncited | EN1_2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### IN2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### VCC2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### EN3_4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controls__1 | legacy_uncited | OUT4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### IN3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### OUT3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controlled_by__0 | legacy_uncited | IN3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controlled_by__1 | legacy_uncited | EN3_4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### GND3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### GND4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### OUT4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controlled_by__0 | legacy_uncited | IN4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| controlled_by__1 | legacy_uncited | EN3_4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### IN4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| controls__0 | legacy_uncited | OUT4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

#### VCC1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| direction | legacy_uncited | power | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Constraints and known issues

### thermal

**requirement:** Preserve source constraint group: thermal

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| ground_pins_are_heat_sinks | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| all_ground_pins_required | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| thermal_design_required | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### inductive_loads

**requirement:** Preserve source constraint group: inductive_loads

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| L293__external_clamp_diodes_required | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| L293D__integrated_clamp_diodes | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### safety

**requirement:** Preserve source constraint group: safety

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| enable_low_disables_output_pair | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| disable_output_state | legacy_uncited | high_impedance | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| enable_is_not_power_isolation | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| fault_detection_integrated | legacy_uncited | no | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| current_sensing_integrated | legacy_uncited | no | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### pwm

**requirement:** Preserve source constraint group: pwm

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| input_pwm_supported | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| enable_pwm_supported | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| independent_half_bridge_control | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| independent_enable_per_half_bridge | legacy_uncited | no | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### power

**requirement:** Preserve source constraint group: power

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| common_ground_required | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| logic_and_motor_supplies_separate | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| supply_decoupling_required | legacy_uncited | yes | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

### logic_truth_table

**condition:** Source H-bridge logic states; no executable safety inference.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| motor_a__enable | legacy_uncited | EN1_2 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__disabled__EN1_2 | legacy_uncited | LOW | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__disabled__IN1 | legacy_uncited | ANY | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__disabled__IN2 | legacy_uncited | ANY | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__disabled__outputs | legacy_uncited | high_impedance | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__forward__EN1_2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__forward__IN1 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__forward__IN2 | legacy_uncited | LOW | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__reverse__EN1_2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__reverse__IN1 | legacy_uncited | LOW | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__reverse__IN2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_low__EN1_2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_low__IN1 | legacy_uncited | LOW | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_low__IN2 | legacy_uncited | LOW | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_high__EN1_2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_high__IN1 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_a__states__brake_high__IN2 | legacy_uncited | HIGH | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_b__enable | legacy_uncited | EN3_4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_b__same_logic_as | legacy_uncited | motor_a | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_b__input_mapping__IN1 | legacy_uncited | IN3 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |
| motor_b__input_mapping__IN2 | legacy_uncited | IN4 | [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt) |

## Sources

- legacy_snapshot: [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/ti__l293-family.yml.txt)

Original source snapshots and the [migration field map](../../../../docs/evidence/migration-2026-11-19/field-map.json) preserve historical context. No unresolved source claim was silently corrected.
