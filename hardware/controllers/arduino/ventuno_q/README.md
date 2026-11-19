<!-- Generated from definition.yml; SHA-256: db3c7fe1af1a69a61dae54787cf7f70b5222a9c066284c75e7f83e455d6826c2. Do not edit manually. -->
# Arduino VENTUNO Q

[Catalog](../../../../docs/catalog.md) · [Hardware YAML](definition.yml)

This reference preserves documented and uncited source statements. Schema validation does not establish electrical compatibility or bench operation.

## Identity and capabilities

| Property | Value |
| --- | --- |
| ID | arduino/ventuno-q |
| Schema version | 1.0.0-draft.1 |
| Kind | board |
| Manufacturer | Arduino |
| Legacy aliases | arduino_ventuno_q |
| Named pin records | 288 |
| Interfaces | 26 |
| Verification | not_verified |

**Declared pin capabilities:** adc, adc_reference_input, can_bus_high, can_bus_low, can_rx, can_tx, dac, gpio, ground_reference, i2c_scl, i2c_sda, not_connected, opamp_negative_input, opamp_output, opamp_positive_input, power_input, power_output, pwm, spi_chip_select, spi_clock, spi_miso, spi_mosi, uart_rx, uart_tx

**Verification limits:** status not_verified. Source statements on this page are not bench verification.

## Component facts

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| scope | documented | Transcription of the local manual; linked PDFs were not used to resolve discrepancies. | [VENTUNO Q User Manual](sources/user_manual.md) |
| pin_naming | documented | UNO analog pins use A0-A5 with D14-D19 aliases, following the Uno R3 definition. Expansion keys use CONNECTOR_position, with physical_pin scoped to connector. maps_to preserves each expansion table's signal label; mcu_pin or source_function preserves its separate port or function column when supplied. | [VENTUNO Q User Manual](sources/user_manual.md) |
| coverage_gaps__0 | documented | Complete UNO power-header positions, Qwiic positions, JCTL pinout, and camera pinouts are not provided in the manual text. | [VENTUNO Q User Manual](sources/user_manual.md) |
| coverage_gaps__1 | documented | MCU package pin numbers, board revision, and per-pin electrical limits are not specified. | [VENTUNO Q User Manual](sources/user_manual.md) |
| coverage_gaps__2 | documented | High-speed and carrier signal labels are transcribed as published, without schematic verification. | [VENTUNO Q User Manual](sources/user_manual.md) |
| related_decision | documented | DEV-2026-11-19-001 | [VENTUNO Q User Manual](sources/user_manual.md) |
| enrichment_decision | documented | DEV-2026-11-19-003 | [VENTUNO Q User Manual](sources/user_manual.md) |
| relationship_reference_convention | documented | Typed references use processor:, component:, interface:, connector:, or pin: followed by a key in the corresponding local mapping. | [VENTUNO Q User Manual](sources/user_manual.md) |
| preparation_status | documented | Additive source transcription; no common-schema or ID migration; no CLI review gate approved. | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__input_rating_refs__0 | documented | usb_c_pd_input | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__input_rating_refs__1 | documented | barrel_jack_input | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__input_rating_refs__2 | documented | screw_terminal_input | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__input_rating_refs__3 | documented | uno_vin_input | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__budget_rule | documented | Select the actual input path and account for board load plus all peripherals; the input connector limit is not a per-output guarantee. | [VENTUNO Q User Manual](sources/user_manual.md) |
| power_distribution__source_context | documented | Source context for this section | [Power Overview](sources/user_manual.md#power-overview); [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw); [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails); [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| model | documented | VENTUNO Q | [VENTUNO Q User Manual](sources/user_manual.md) |
| device_type | documented | dual_processor_controller_board | [VENTUNO Q User Manual](sources/user_manual.md) |
| memory__ram__type | documented | LPDDR5 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| memory__ram__capacity_gb | documented | dimension: storage; unit: GB; rating kind: unspecified; value: 16 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| memory__ram__source_context | documented | Source context for this section | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| memory__storage__type | documented | eMMC | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| memory__storage__capacity_gb | documented | dimension: storage; unit: GB; rating kind: unspecified; value: 64 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| memory__storage__source_context | documented | Source context for this section | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| physical__board_dimensions_mm__length | documented | dimension: length; unit: mm; rating kind: unspecified; value: 160 | [Form Factor](sources/user_manual.md#form-factor); [Board Clearance](sources/user_manual.md#board-clearance) |
| physical__board_dimensions_mm__width | documented | dimension: length; unit: mm; rating kind: unspecified; value: 100 | [Form Factor](sources/user_manual.md#form-factor); [Board Clearance](sources/user_manual.md#board-clearance) |
| physical__mounting_standoffs | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [Form Factor](sources/user_manual.md#form-factor); [Board Clearance](sources/user_manual.md#board-clearance) |
| physical__uno_style_headers | documented | yes | [Form Factor](sources/user_manual.md#form-factor); [Board Clearance](sources/user_manual.md#board-clearance) |
| physical__source_context | documented | Source context for this section | [Form Factor](sources/user_manual.md#form-factor); [Board Clearance](sources/user_manual.md#board-clearance) |

## Processors

### mcu

**Model:** STM32H5F5

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| clock_hz | documented | dimension: frequency; unit: Hz; rating kind: unspecified; value: 250000000 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| flash | documented | dimension: storage; unit: MB; rating kind: unspecified; value: 4 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| sram | documented | dimension: storage; unit: MB; rating kind: unspecified; value: 1.5 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |

### mpu

**Model:** Qualcomm Dragonwing QCS8275

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| cpu_cores | documented | dimension: count; unit: count; rating kind: unspecified; value: 8 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| max_clock_hz | documented | dimension: frequency; unit: Hz; rating kind: unspecified; max: 2350000000 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| gpu | documented | Adreno_A623 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| gpu_clock_hz | documented | dimension: frequency; unit: Hz; rating kind: unspecified; value: 877000000 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| npu | documented | Hexagon_Tensor | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| npu_max_dense_tops | documented | dimension: compute_rate; unit: TOPS; rating kind: unspecified; max: 40 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| note | documented | ISP model is omitted because the manual names both Spectra 690 and Spectra 692. | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |

## Onboard component inventory

| ID | Part | Role | Sources |
| --- | --- | --- | --- |
| stm32h5f5 | STM32H5F5 | Real-time MCU and UNO-header peripheral controller | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| qcs8275 | QCS8275 | Application MPU serving the high-speed expansion and multimedia interfaces | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| ata6563 | ATA6563 | CAN physical-layer transceiver between MCU CAN signals and the bus terminals | [CAN-FD](sources/user_manual.md#can-fd); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| max98091 | MAX98091 | Audio codec exposing audio connections through JMISC and JOMEGA | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [JMISC](sources/user_manual.md#jmisc); [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| tusb7340 | TUSB7340 | USB host controller connected to the JOMEGA expansion header | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| qca8081 | QCA-8081 | Ethernet PHY for the RJ45 network interface | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| trjt9010a98nl | TRJT9010A98NL | RJ45 Ethernet connector | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| nfa725b | NFA725B | Wi-Fi and Bluetooth radio module; Bluetooth version remains disputed | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| tf31_camera_connectors | TF31-22S-0.5SH | 22-pin, 0.5 mm-pitch camera connectors J3_1, J3_2, and J3_3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| camera_lane_esd | RCLAMP0524TCT | ESD protection on high-speed camera lanes | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| camera_power_i2c_esd | DF2B7ASL,L3F | ESD protection on camera power and I2C lines; part label preserved as written | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| jhat_level_translation | Part number unspecified | Translate MPU-side 1.8 V signals to JHAT-side 3.3 V | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| vin_ptc | Part number unspecified | PTC protection on the UNO VIN input | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| hdmi_tvs | Part number unspecified | TVS protection on HDMI data and hot-plug-detect lines | [HDMI](sources/user_manual.md#hdmi) |
| hdmi_polyfuse | Part number unspecified | Protection described for the HDMI hot-plug-detect path | [HDMI](sources/user_manual.md#hdmi) |

### jhat_level_translation

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| identification | documented | unspecified_in_manual | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| mpu_side_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| header_side_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

### vin_ptc

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| identification | documented | unspecified_in_manual | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| fuse_rating_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 1.1 | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |

### hdmi_tvs

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| identification | documented | unspecified_in_manual | [HDMI](sources/user_manual.md#hdmi) |

### hdmi_polyfuse

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| identification | documented | unspecified_in_manual | [HDMI](sources/user_manual.md#hdmi) |
| manual_stated_fuse_rating_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 0.5 | [HDMI](sources/user_manual.md#hdmi) |
| note | documented | Preserves the manual description; not an independently verified HDMI supply-current rating. | [HDMI](sources/user_manual.md#hdmi) |

## Connection relationships

| ID | From | To | Relationship | Via | Routing state | Notes | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| uno_uart_owner | processor:mcu | interface:UNO_UART | owns |  | documented |  | [UART](sources/user_manual.md#uart) |
| uno_uart_at_jdigital | interface:UNO_UART | connector:JDIGITAL | exposed_at |  | documented |  | [UART](sources/user_manual.md#uart) |
| uno_spi_owner | processor:mcu | interface:UNO_SPI | owns |  | documented |  | [SPI](sources/user_manual.md#spi) |
| uno_spi_at_jdigital | interface:UNO_SPI | connector:JDIGITAL | exposed_at |  | documented |  | [SPI](sources/user_manual.md#spi) |
| uno_i2c_owner | processor:mcu | interface:UNO_I2C | owns |  | documented |  | [I2C](sources/user_manual.md#i2c) |
| uno_i2c_at_jdigital | interface:UNO_I2C | connector:JDIGITAL | exposed_at |  | documented |  | [I2C](sources/user_manual.md#i2c) |
| qwiic_i2c_owner | processor:mcu | interface:QWIIC_I2C | owns |  | documented |  | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| qwiic_i2c_at_qwiic | interface:QWIIC_I2C | connector:QWIIC | exposed_at |  | documented |  | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| uno_adc_owner | processor:mcu | interface:UNO_ADC | owns |  | documented |  | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| uno_adc_at_janalog | interface:UNO_ADC | connector:JANALOG | exposed_at |  | documented |  | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| uno_dac_owner | processor:mcu | interface:UNO_DAC | owns |  | documented |  | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| uno_dac_at_janalog | interface:UNO_DAC | connector:JANALOG | exposed_at |  | documented |  | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| uno_opamp_owner | processor:mcu | interface:UNO_OPAMP | owns |  | documented |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| uno_opamp_at_janalog | interface:UNO_OPAMP | connector:JANALOG | exposed_at |  | documented |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| uno_opamp_at_jdigital | interface:UNO_OPAMP | connector:JDIGITAL | exposed_at |  | documented |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| uno_pwm_owner | processor:mcu | interface:UNO_PWM | owns |  | documented |  | [PWM Pins](sources/user_manual.md#pwm-pins) |
| uno_pwm_at_jdigital | interface:UNO_PWM | connector:JDIGITAL | exposed_at |  | documented |  | [PWM Pins](sources/user_manual.md#pwm-pins) |
| uno_can_owner | processor:mcu | interface:UNO_CAN | owns |  | documented |  | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |
| uno_can_at_jdigital | interface:UNO_CAN | connector:JDIGITAL | exposed_at |  | documented |  | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |
| jhat_i2c_se0_owner | processor:mpu | interface:JHAT_I2C_SE0 | owns |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_i2c_se0_at_jhat | interface:JHAT_I2C_SE0 | connector:JHAT | exposed_at |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_i2c_se1_owner | processor:mpu | interface:JHAT_I2C_SE1 | owns |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_i2c_se1_at_jhat | interface:JHAT_I2C_SE1 | connector:JHAT | exposed_at |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_spi_se3_owner | processor:mpu | interface:JHAT_SPI_SE3 | owns |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_spi_se3_at_jhat | interface:JHAT_SPI_SE3 | connector:JHAT | exposed_at |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_uart_se2_owner | processor:mpu | interface:JHAT_UART_SE2 | owns |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_uart_se2_at_jhat | interface:JHAT_UART_SE2 | connector:JHAT | exposed_at |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_i2s1_owner | processor:mpu | interface:JHAT_I2S1 | owns |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jhat_i2s1_at_jhat | interface:JHAT_I2S1 | connector:JHAT | exposed_at |  | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jmisc_usart2_owner | processor:mcu | interface:JMISC_USART2 | owns |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_usart2_at_jmisc | interface:JMISC_USART2 | connector:JMISC | exposed_at |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_uart4_owner | processor:mcu | interface:JMISC_UART4 | owns |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_uart4_at_jmisc | interface:JMISC_UART4 | connector:JMISC | exposed_at |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_i2c2_owner | processor:mcu | interface:JMISC_I2C2 | owns |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_i2c2_at_jmisc | interface:JMISC_I2C2 | connector:JMISC | exposed_at |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_spi_se0_owner | processor:mpu | interface:JMISC_SPI_SE0 | owns |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_spi_se0_at_jmisc | interface:JMISC_SPI_SE0 | connector:JMISC | exposed_at |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_i2s2_owner | processor:mpu | interface:JMISC_I2S2 | owns |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jmisc_i2s2_at_jmisc | interface:JMISC_I2S2 | connector:JMISC | exposed_at |  | documented |  | [JMISC](sources/user_manual.md#jmisc) |
| jomega_spi_owner | processor:mpu | interface:JOMEGA_SPI | owns |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_spi_at_jomega | interface:JOMEGA_SPI | connector:JOMEGA | exposed_at |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_uart_se7_owner | processor:mpu | interface:JOMEGA_UART_SE7 | owns |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_uart_se7_at_jomega | interface:JOMEGA_UART_SE7 | connector:JOMEGA | exposed_at |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan1_owner | processor:mcu | interface:JOMEGA_FDCAN1 | owns |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan1_at_jomega | interface:JOMEGA_FDCAN1 | connector:JOMEGA | exposed_at |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan2_owner | processor:mcu | interface:JOMEGA_FDCAN2 | owns |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan2_at_jomega | interface:JOMEGA_FDCAN2 | connector:JOMEGA | exposed_at |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan3_owner | processor:mcu | interface:JOMEGA_FDCAN3 | owns |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| jomega_fdcan3_at_jomega | interface:JOMEGA_FDCAN3 | connector:JOMEGA | exposed_at |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| can_bus_owner | processor:mcu | interface:CAN_BUS | owns |  | documented |  | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| can_bus_at_can_screw_terminal | interface:CAN_BUS | connector:CAN_SCREW_TERMINAL | exposed_at |  | documented |  | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| jmedia_mipi_dsi_owner | processor:mpu | interface:JMEDIA_MIPI_DSI | owns |  | documented |  | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| jmedia_mipi_dsi_at_jmedia | interface:JMEDIA_MIPI_DSI | connector:JMEDIA | exposed_at |  | documented |  | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| can_bus_path | processor:mcu | connector:CAN_SCREW_TERMINAL | bus_connection | component:ata6563 | conflicting | PD0_PD1_TX_RX_assignment_unresolved | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| jhat_path | processor:mpu | connector:JHAT | level_translated_connection | component:jhat_level_translation | documented |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| jmedia_path | processor:mpu | connector:JMEDIA | direct_signal_connection |  | documented |  | [JMEDIA](sources/user_manual.md#jmedia) |
| audio_jmisc | component:max98091 | connector:JMISC | connected_to |  | documented |  | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [JMISC](sources/user_manual.md#jmisc) |
| audio_jomega | component:max98091 | connector:JOMEGA | connected_to |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| usb_host_jomega | component:tusb7340 | connector:JOMEGA | connected_to |  | documented |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| ethernet_path | component:qca8081 | connector:ETHERNET | ethernet_phy_connection | component:trjt9010a98nl | documented |  | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| radio_owner | processor:mpu | component:nfa725b | connected_to |  | documented |  | [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| mcu_identity | processor:mcu | component:stm32h5f5 | implemented_by |  | documented |  | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| mpu_identity | processor:mpu | component:qcs8275 | implemented_by |  | documented |  | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview) |
| j3_1_owner | processor:mpu | connector:J3_1 | camera_interface_connection |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_1_camera_lane_esd | component:camera_lane_esd | connector:J3_1 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_1_camera_power_i2c_esd | component:camera_power_i2c_esd | connector:J3_1 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_2_owner | processor:mpu | connector:J3_2 | camera_interface_connection |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_2_camera_lane_esd | component:camera_lane_esd | connector:J3_2 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_2_camera_power_i2c_esd | component:camera_power_i2c_esd | connector:J3_2 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_3_owner | processor:mpu | connector:J3_3 | camera_interface_connection |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_3_camera_lane_esd | component:camera_lane_esd | connector:J3_3 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| j3_3_camera_power_i2c_esd | component:camera_power_i2c_esd | connector:J3_3 | protects |  | documented |  | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| usb_a_owner | processor:mpu | connector:USB_A | connected_to |  | documented |  | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| hdmi_owner | processor:mpu | connector:HDMI | connected_to |  | documented |  | [HDMI](sources/user_manual.md#hdmi) |
| m2_owner | processor:mpu | connector:M2 | connected_to |  | documented |  | [M.2 Connector](sources/user_manual.md#m2-connector) |
| jctl_owner | processor:mpu | connector:JCTL | connected_to |  | documented |  | [Hardware Debug UART Interface](sources/user_manual.md#hardware-debug-uart-interface) |

## Resource conflicts

| ID | Pins | Participants | Policy | Condition | Source rule | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| jhat_bluetooth_uart | JHAT_8, JHAT_10, JHAT_11, JHAT_36 | component:nfa725b, interface:JHAT_UART_SE2 | unavailable_when | target: component:nfa725b; state: bluetooth_active | unavailable_to_external_header_while_bluetooth_active | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| display_output_mux |  | connector:HDMI, interface:JMEDIA_MIPI_DSI | at_most_one_active |  | at_most_one_active | [HDMI](sources/user_manual.md#hdmi) |
| adc_dac_exclusion |  | interface:UNO_ADC, interface:UNO_DAC | not_simultaneous |  | not_simultaneous_as_stated_by_manual | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| analog_pin_functions | A0, A1, A2, A3, A4, A5 |  | per_pin_exclusion |  | gpio_and_alternate_function_not_simultaneous_on_same_pin | [Analog Pins](sources/user_manual.md#analog-pins) |

## Power and electrical summary

### usb_c_pd_input

**Role:** input; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; min: 9; max: 20 | [Power Overview](sources/user_manual.md#power-overview); [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 3 | [Power Overview](sources/user_manual.md#power-overview); [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| power_delivery_negotiation_required | documented | yes | [Power Overview](sources/user_manual.md#power-overview); [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| accepts_5v_only_source | documented | no | [Power Overview](sources/user_manual.md#power-overview); [USB-C Connector](sources/user_manual.md#usb-c-connector) |

### barrel_jack_input

**Role:** input; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; min: 7; max: 24 | [Power Overview](sources/user_manual.md#power-overview); [Power Safety Considerations](sources/user_manual.md#power-safety-considerations) |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 5 | [Power Overview](sources/user_manual.md#power-overview); [Power Safety Considerations](sources/user_manual.md#power-safety-considerations) |
| documented_power_examples_w__at_12v | documented | dimension: power; unit: W; rating kind: unspecified; value: 60 | [Power Overview](sources/user_manual.md#power-overview); [Power Safety Considerations](sources/user_manual.md#power-safety-considerations) |
| documented_power_examples_w__at_24v | documented | dimension: power; unit: W; rating kind: unspecified; value: 120 | [Power Overview](sources/user_manual.md#power-overview); [Power Safety Considerations](sources/user_manual.md#power-safety-considerations) |

### screw_terminal_input

**Role:** input; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; min: 7; max: 24 | [Power Overview](sources/user_manual.md#power-overview) |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 10 | [Power Overview](sources/user_manual.md#power-overview) |

### uno_vin_input

**Role:** input; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; min: 7; max: 24 | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| ptc_fuse_rating_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 1.1 | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| recommended_for_board_power | documented | no | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |

### limited_rails

**Role:** rail; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| nets__0 | documented | +3V3_LIMITED | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| nets__1 | documented | +5V_LIMITED | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| nominal_voltages_v__0 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| nominal_voltages_v__1 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| stated_current_limit_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 2.8 | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| note | documented | The manual does not clarify whether the stated limit applies independently to each rail. | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |

### jhat_logic

**Role:** reference; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| header_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| mpu_side_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| level_translated | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

### jmedia_logic

**Role:** reference; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; nominal: 1.8 | [JMEDIA](sources/user_manual.md#jmedia) |
| note | documented | Logic-domain statement only; the connector also carries VIN and 3.3 V power pins. | [JMEDIA](sources/user_manual.md#jmedia) |

### rtc_backup_input

**Role:** input; **Limit scope:** Not independently classified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rating | documented | dimension: voltage; unit: V; rating kind: operating; max: 3.3 | [JMISC](sources/user_manual.md#jmisc) |
| powers_rtc_only | documented | yes | [JMISC](sources/user_manual.md#jmisc) |

### limited_outputs

**Role:** output; **Limit scope:** unknown

**Feeds:** connector:JHAT, connector:QWIIC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| nets__0 | documented | +3V3_LIMITED | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| nets__1 | documented | +5V_LIMITED | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| stated_current_limit_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 2.8 | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| connectors__0 | documented | JHAT | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| connectors__1 | documented | QWIIC | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| consumer_groups__0 | documented | UNO headers | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| consumer_groups__1 | documented | shields | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| consumer_groups__2 | documented | hats | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| limit_scope | documented | Manual does not establish whether 2.8 A is independent per rail or combined. | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |

### usb_a_outputs

**Role:** output; **Limit scope:** unknown

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | USB_A | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| onboard_ports | documented | dimension: count; unit: count; rating kind: unspecified; value: 2 | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| max_current_per_port_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 1.71 | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| max_power_per_port_w | documented | dimension: power; unit: W; rating kind: unspecified; max: 8.55 | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| depends_on_total_input_budget | documented | yes | [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |

### usb_c_source

**Role:** output; **Limit scope:** unknown

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | USB_C | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 3 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| max_power_w | documented | dimension: power; unit: W; rating kind: unspecified; max: 15 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| depends_on_total_input_budget | documented | yes | [USB-C Connector](sources/user_manual.md#usb-c-connector) |

### low_input_voltage_example

**Role:** output; **Limit scope:** unknown

**Possible input dependencies:** barrel_jack_input

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| input_ref | documented | barrel_jack_input | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| input_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 7 | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| input_current_limit_a | documented | dimension: current; unit: A; rating kind: unspecified; value: 5 | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| manual_stated_input_power_w | documented | dimension: power; unit: W; rating kind: unspecified; value: 35 | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| approximate_board_full_load_w | documented | dimension: power; unit: W; rating kind: unspecified; value: 25 | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| manual_example_usb_a_load_w | documented | dimension: power; unit: W; rating kind: unspecified; value: 17 | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |
| disposition | documented | Manual warns this combined load can damage the jack; not an approved operating budget. | [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw) |

### uno_vin

**Role:** output; **Limit scope:** unknown

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| pin | documented | VIN | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| voltage_ref | documented | uno_vin_input | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| protected_by | documented | component:vin_ptc | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |
| limited_power_headroom | documented | yes | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |

### rtc_backup

**Role:** output; **Limit scope:** unknown

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| pin | documented | JMISC_59 | [JMISC](sources/user_manual.md#jmisc) |
| max_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; max: 3.3 | [JMISC](sources/user_manual.md#jmisc) |
| loads__0 | documented | MPU RTC | [JMISC](sources/user_manual.md#jmisc) |
| loads__1 | documented | MCU RTC | [JMISC](sources/user_manual.md#jmisc) |
| powers_board | documented | no | [JMISC](sources/user_manual.md#jmisc) |

### carrier_outputs_outside_limited_nets

**Role:** output; **Limit scope:** unknown

**Feeds:** connector:JMEDIA, connector:JMISC, connector:JOMEGA

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connectors__0 | documented | JMEDIA | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| connectors__1 | documented | JMISC | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| connectors__2 | documented | JOMEGA | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| meaning | documented | Outside the named limited nets, not unlimited current. | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |
| current_limit_status | documented | not_fully_specified_in_manual | [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails) |

## Interfaces

| ID | Type | Processor | Signal roles / pins | Sources |
| --- | --- | --- | --- | --- |
| UNO_UART | uart | mcu | RX: D0; TX: D1 | [UART](sources/user_manual.md#uart) |
| UNO_SPI | spi | mcu | SS: D10; MOSI: D11; MISO: D12; SCK: D13 | [SPI](sources/user_manual.md#spi) |
| UNO_I2C | i2c | mcu | SDA: D20; SCL: D21 | [I2C](sources/user_manual.md#i2c) |
| QWIIC_I2C | i2c | mcu | SDA: QWIIC_SDA; SCL: QWIIC_SCL | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| UNO_ADC | adc | mcu | pins: A0, A1, A2, A3, A4, A5; external reference  pin: AREF | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| UNO_DAC | dac | mcu | channels  DAC0: A0; channels  DAC1: A1 | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| UNO_OPAMP | opamp | mcu | positive input: A2; negative input: A3; output: D3 | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| UNO_PWM | pwm | mcu | pins: D3, D5, D6, D9, D10, D11 | [PWM Pins](sources/user_manual.md#pwm-pins) |
| UNO_CAN | can_controller | mcu | TX: D4; RX: D5 | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |
| JHAT_I2C_SE0 | i2c | mpu | SDA: JHAT_3; SCL: JHAT_5 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_I2C_SE1 | i2c | mpu | SDA: JHAT_27; SCL: JHAT_28 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_SPI_SE3 | spi | mpu | MOSI: JHAT_19; MISO: JHAT_21; SCK: JHAT_23; CS: JHAT_24 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_UART_SE2 | uart | mpu | TX: JHAT_8; RX: JHAT_10; RFR: JHAT_11; CTS: JHAT_36 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_I2S1 | i2s | mpu | SCK: JHAT_12; WS: JHAT_35; DATA0: JHAT_38; DATA1: JHAT_40 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JMISC_USART2 | uart | mcu | RX: JMISC_12; TX: JMISC_14 | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_UART4 | uart | mcu | RX: JMISC_23; TX: JMISC_25 | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_I2C2 | i2c | mcu | SCL: JMISC_16; SDA: JMISC_18 | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_SPI_SE0 | spi | mpu | MISO: JMISC_37; MOSI: JMISC_39; SCK: JMISC_41; chip selects: JMISC_43, JMISC_47, JMISC_45 | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_I2S2 | i2s | mpu | SCK: JMISC_46; WS: JMISC_48; DATA0: JMISC_50; DATA1: JMISC_52 | [JMISC](sources/user_manual.md#jmisc) |
| JOMEGA_SPI | spi | mpu | MISO: JOMEGA_62; MOSI: JOMEGA_64; SCK: JOMEGA_66; CS: JOMEGA_68 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_UART_SE7 | uart | mpu | TX: JOMEGA_83; RX: JOMEGA_85 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_FDCAN1 | can_controller | mcu | TX: JOMEGA_86; RX: JOMEGA_88 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_FDCAN2 | can_controller | mcu | TX: JOMEGA_92; RX: JOMEGA_94 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_FDCAN3 | can_controller | mcu | TX: JOMEGA_98; RX: JOMEGA_100 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| CAN_BUS | can_bus | mcu | high: CAN_H; low: CAN_L | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| JMEDIA_MIPI_DSI | mipi_dsi | mpu | clock negative: JMEDIA_3; clock positive: JMEDIA_5 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |

### UNO_UART

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| peripheral | documented | USART3 | [UART](sources/user_manual.md#uart) |

### QWIIC_I2C

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| logic_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| onboard_pullups | documented | yes | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| note | documented | PA8 and PC9 follow the Communication / I2C table; I2C3 versus I2C4 naming is unresolved. | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |

### UNO_ADC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| supported_resolution_bits__0 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 8 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| supported_resolution_bits__1 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 10 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| supported_resolution_bits__2 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 12 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| default_reference_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| internal_reference_options_v__0 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.5 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| internal_reference_options_v__1 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| internal_reference_options_v__2 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 2.048 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| internal_reference_options_v__3 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 2.5 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| external_reference__min_v | documented | dimension: voltage; unit: V; rating kind: unspecified; min: 2.0 | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| external_reference__max_reference | documented | VDD | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

### UNO_DAC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| supported_resolution_bits__0 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 8 | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| supported_resolution_bits__1 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 10 | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| supported_resolution_bits__2 | documented | dimension: resolution; unit: bit; rating kind: unspecified; value: 12 | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |

### UNO_OPAMP

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | operational_amplifier | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

### UNO_PWM

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| default_resolution_bits | documented | dimension: resolution; unit: bit; rating kind: resolution; value: 8 | [PWM Pins](sources/user_manual.md#pwm-pins) |

### UNO_CAN

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | can_controller_signals | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |
| peripheral | documented | FDCAN2 | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |
| note | documented | These are MCU logic signals, not the transceiver bus terminals. | [Digital Pins](sources/user_manual.md#digital-pins); [CAN Interfaces](sources/user_manual.md#can-interfaces) |

### JHAT_UART_SE2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| unavailable_while_bluetooth_active | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

### JOMEGA_FDCAN1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | can_controller_signals | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| shared_with_onboard_can_bus | documented | yes | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### JOMEGA_FDCAN2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | can_controller_signals | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### JOMEGA_FDCAN3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | can_controller_signals | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### CAN_BUS

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | can_fd | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| transceiver | documented | ATA6563 | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| physical_bitrate_limit_bps | documented | dimension: data_rate; unit: bit/s; rating kind: unspecified; value: 5000000 | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| transceiver_supply_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| transceiver_logic_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| standby_mcu_pin | documented | PI11 | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| note | documented | PD0/PD1 TX/RX assignments conflict in the manual and are not resolved here. | [CAN-FD](sources/user_manual.md#can-fd); [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |

### JMEDIA_MIPI_DSI

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| data_pairs__0__0 | documented | JMEDIA_10 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__0__1 | documented | JMEDIA_12 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__1__0 | documented | JMEDIA_4 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__1__1 | documented | JMEDIA_6 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__2__0 | documented | JMEDIA_11 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__2__1 | documented | JMEDIA_9 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__3__0 | documented | JMEDIA_17 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |
| data_pairs__3__1 | documented | JMEDIA_15 | [JMEDIA](sources/user_manual.md#jmedia); [HDMI](sources/user_manual.md#hdmi) |

## Connector summary

| ID | Type | Positions | Processor | Sources |
| --- | --- | --- | --- | --- |
| USB_C | usb_type_c | Not specified | Not specified | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| USB_A | usb_type_a | Not specified | mpu | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| QWIIC | qwiic | Not specified | Not specified | [Qwiic](sources/user_manual.md#qwiic) |
| ETHERNET | RJ45_8P8C | Not specified | Not specified | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| HDMI | HDMI_Type_A | 19 | mpu | [HDMI](sources/user_manual.md#hdmi) |
| M2 | M_2_M_key | Not specified | mpu | [M.2 Connector](sources/user_manual.md#m2-connector) |
| JHAT | male_header | 40 | mpu | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JMEDIA | documented_header | 60 | mpu | [JMEDIA](sources/user_manual.md#jmedia) |
| JMISC | documented_header | 60 | Not specified | [JMISC](sources/user_manual.md#jmisc) |
| JOMEGA | documented_header | 100 | Not specified | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JCTL | debug_uart | Not specified | mpu | [Hardware Debug UART Interface](sources/user_manual.md#hardware-debug-uart-interface) |
| J3_1 | TF31-22S-0.5SH | 22 | mpu | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| J3_3 | TF31-22S-0.5SH | 22 | mpu | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| J3_2 | TF31-22S-0.5SH | 22 | mpu | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| CAN_SCREW_TERMINAL | screw_terminal | Not specified | Not specified | [CAN-FD](sources/user_manual.md#can-fd) |
| JDIGITAL | uno_style_digital_header | Not specified | mcu | [Digital Pins](sources/user_manual.md#digital-pins); [UART](sources/user_manual.md#uart) |
| JANALOG | uno_style_analog_header | Not specified | mcu | [Analog Pins](sources/user_manual.md#analog-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

### USB_C

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| usb_standard | documented | USB_3.1_Gen_1 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| max_data_rate_bps | documented | dimension: data_rate; unit: bit/s; rating kind: unspecified; max: 5000000000 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| dual_role_power | documented | yes | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| display_output | documented | DisplayPort | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| source_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| source_max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 3 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| source_max_power_w | documented | dimension: power; unit: W; rating kind: unspecified; max: 15 | [USB-C Connector](sources/user_manual.md#usb-c-connector) |
| sink_supply | documented | usb_c_pd_input | [USB-C Connector](sources/user_manual.md#usb-c-connector) |

### USB_A

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| onboard_ports | documented | dimension: current; unit: A; rating kind: unspecified; value: 2 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| additional_ports_via_header | documented | dimension: current; unit: A; rating kind: unspecified; value: 2 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| expansion_connector | documented | JOMEGA | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| usb_standard | documented | USB_3.0 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| max_data_rate_bps | documented | dimension: data_rate; unit: bit/s; rating kind: unspecified; max: 5000000000 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 5.0 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| max_current_per_onboard_port_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 1.71 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |
| max_power_per_onboard_port_w | documented | dimension: power; unit: W; rating kind: unspecified; max: 8.55 | [USB-A Connectors](sources/user_manual.md#usb-a-connectors) |

### QWIIC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| interface | documented | QWIIC_I2C | [Qwiic](sources/user_manual.md#qwiic) |
| voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [Qwiic](sources/user_manual.md#qwiic) |

### ETHERNET

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| phy | documented | Qualcomm_QCA_8081 | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| connector_model | documented | TRJT9010A98NL | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| supported_rates_mbps__0 | documented | dimension: data_rate; unit: Mbit/s; rating kind: unspecified; value: 10 | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| supported_rates_mbps__1 | documented | dimension: data_rate; unit: Mbit/s; rating kind: unspecified; value: 100 | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| supported_rates_mbps__2 | documented | dimension: data_rate; unit: Mbit/s; rating kind: unspecified; value: 1000 | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| supported_rates_mbps__3 | documented | dimension: data_rate; unit: Mbit/s; rating kind: unspecified; value: 2500 | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |
| auto_negotiation | documented | yes | [Ethernet Connector](sources/user_manual.md#ethernet-connector) |

### HDMI

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| tmds_data_pairs | documented | dimension: count; unit: count; rating kind: unspecified; value: 3 | [HDMI](sources/user_manual.md#hdmi) |
| tmds_clock_pairs | documented | dimension: count; unit: count; rating kind: unspecified; value: 1 | [HDMI](sources/user_manual.md#hdmi) |
| ddc | documented | yes | [HDMI](sources/user_manual.md#hdmi) |
| cec | documented | yes | [HDMI](sources/user_manual.md#hdmi) |
| shared_display_output | documented | JMEDIA | [HDMI](sources/user_manual.md#hdmi) |
| note | documented | HDMI and JMEDIA MIPI-DSI cannot be active simultaneously. | [HDMI](sources/user_manual.md#hdmi) |

### M2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| interface | documented | PCIe_Gen_4_x4 | [M.2 Connector](sources/user_manual.md#m2-connector) |
| supported_storage | documented | NVMe | [M.2 Connector](sources/user_manual.md#m2-connector) |
| supported_form_factors__0 | documented | 2230 | [M.2 Connector](sources/user_manual.md#m2-connector) |
| sata_supported | documented | no | [M.2 Connector](sources/user_manual.md#m2-connector) |
| smbus | documented | yes | [M.2 Connector](sources/user_manual.md#m2-connector) |
| power_rails_v__0 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [M.2 Connector](sources/user_manual.md#m2-connector) |
| power_rails_v__1 | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [M.2 Connector](sources/user_manual.md#m2-connector) |

### JHAT

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| logic_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| mpu_side_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| level_translated | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| source_section | documented | RPi 40-Pin Header | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

### JMEDIA

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| board_side | documented | bottom | [JMEDIA](sources/user_manual.md#jmedia) |
| logic_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 1.8 | [JMEDIA](sources/user_manual.md#jmedia) |
| source_section | documented | JMEDIA | [JMEDIA](sources/user_manual.md#jmedia) |

### JMISC

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connected_components__0 | documented | STM32H5F5 | [JMISC](sources/user_manual.md#jmisc) |
| connected_components__1 | documented | QCS8275 | [JMISC](sources/user_manual.md#jmisc) |
| connected_components__2 | documented | MAX98091 | [JMISC](sources/user_manual.md#jmisc) |
| source_section | documented | JMISC | [JMISC](sources/user_manual.md#jmisc) |

### JOMEGA

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connected_components__0 | documented | TUSB7340 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| connected_components__1 | documented | STM32H5F5 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| connected_components__2 | documented | QCS8275 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| connected_components__3 | documented | MAX98091 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| source_section | documented | JOMEGA Expansion Header | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### JCTL

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| note | documented | Pin positions and logic levels are not specified in the local manual text. | [Hardware Debug UART Interface](sources/user_manual.md#hardware-debug-uart-interface) |

### J3_1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| label | documented | CAMERA2 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| pitch_mm | documented | dimension: length; unit: mm; rating kind: unspecified; value: 0.5 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| interface | documented | MIPI_CSI_2 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| data_lanes | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_bus | documented | I2C4 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_gpio_physical_pin | documented | dimension: count; unit: count; rating kind: unspecified; value: 17 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| power_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |

### J3_3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| label | documented | CAMERA1 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| pitch_mm | documented | dimension: length; unit: mm; rating kind: unspecified; value: 0.5 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| interface | documented | MIPI_CSI_2 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| data_lanes | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_bus | documented | I2C2 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_gpio_physical_pin | documented | dimension: count; unit: count; rating kind: unspecified; value: 17 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| power_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |

### J3_2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| label | documented | CAMERA0 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| pitch_mm | documented | dimension: length; unit: mm; rating kind: unspecified; value: 0.5 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| interface | documented | MIPI_CSI_2 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| data_lanes | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_bus | documented | I2C0 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_gpio_physical_pin | documented | dimension: count; unit: count; rating kind: unspecified; value: 17 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| control_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| power_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; value: 3.3 | [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |

### CAN_SCREW_TERMINAL

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| interface | documented | CAN_BUS | [CAN-FD](sources/user_manual.md#can-fd) |

### JDIGITAL

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| note | documented | Logical connector grouping; the manual text does not enumerate physical header positions. | [Digital Pins](sources/user_manual.md#digital-pins); [UART](sources/user_manual.md#uart) |

## Pin tables

### CAN_SCREW_TERMINAL

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CAN_H | Not specified | CANH |  | can_bus_high | CAN-H |  | [CAN-FD](sources/user_manual.md#can-fd); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| CAN_L | Not specified | CANL |  | can_bus_low | CAN-L |  | [CAN-FD](sources/user_manual.md#can-fd); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |

#### CAN_H

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | CAN_SCREW_TERMINAL | [CAN-FD](sources/user_manual.md#can-fd); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |

#### CAN_L

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | CAN_SCREW_TERMINAL | [CAN-FD](sources/user_manual.md#can-fd); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |

### JANALOG

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | Not specified | PA4 |  | gpio, adc, dac | D14, DAC0 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc); [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| A1 | Not specified | PA5 |  | gpio, adc, dac | D15, DAC1 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc); [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| A2 | Not specified | PE12 |  | gpio, adc, opamp_positive_input, spi_clock | D16 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| A3 | Not specified | PE13 |  | gpio, adc, opamp_negative_input, spi_miso | D17 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| A4 | Not specified | PE14 |  | gpio, adc, spi_mosi | D18 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| A5 | Not specified | PE15 |  | gpio, adc | D19 |  | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

#### A0

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc); [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |

#### A1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc); [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |

#### A2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

#### A3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

#### A4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

#### A5

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JANALOG | [Digital Pins](sources/user_manual.md#digital-pins); [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |

### JDIGITAL

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D0 | Not specified | PB11 |  | gpio, uart_rx | RX |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D1 | Not specified | PB10 |  | gpio, uart_tx | TX |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D2 | Not specified | PB0 |  | gpio |  |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D3 | Not specified | PB1 |  | gpio, opamp_output, pwm |  |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D4 | Not specified | PB6 |  | gpio, can_tx | FDCAN2_TX |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D5 | Not specified | PB5 |  | gpio, can_rx, pwm | FDCAN2_RX |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D6 | Not specified | PB2 |  | gpio, pwm |  |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D7 | Not specified | PB3 |  | gpio |  |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D8 | Not specified | PB4 |  | gpio |  |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D9 | Not specified | PB7 |  | gpio, pwm |  |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D10 | Not specified | PB12 |  | gpio, spi_chip_select, pwm | SS |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D11 | Not specified | PB15 |  | gpio, spi_mosi, pwm | MOSI |  | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |
| D12 | Not specified | PB14 |  | gpio, spi_miso | MISO |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D13 | Not specified | PB13 |  | gpio, spi_clock | SCK |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D20 | Not specified | PH12 |  | gpio, i2c_sda | SDA |  | [Digital Pins](sources/user_manual.md#digital-pins) |
| D21 | Not specified | PH11 |  | gpio, i2c_scl | SCL |  | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D0

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D5

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D6

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D7

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D8

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D9

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D10

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D11

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins); [PWM Pins](sources/user_manual.md#pwm-pins) |

#### D12

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D13

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D20

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

#### D21

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JDIGITAL | [Digital Pins](sources/user_manual.md#digital-pins) |

### JHAT

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JHAT_1 | 1 | +3V3 |  | power_output |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_2 | 2 | +5V |  | power_output |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_3 | 3 | MD_GPIO_17 | SE0_SDA |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_4 | 4 | +5V |  | power_output |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_5 | 5 | MD_GPIO_18 | SE0_SCL |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_6 | 6 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_7 | 7 | MD_GPIO_83 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_8 | 8 | MD_GPIO_86 | SE2_TX |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_9 | 9 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_10 | 10 | MD_GPIO_87 | SE2_RX |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_11 | 11 | MD_GPIO_85 | SE2_RFR |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_12 | 12 | MD_GPIO_116 | I2S1_SCK |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_13 | 13 | MD_GPIO_109 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_14 | 14 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_15 | 15 | MD_GPIO_90 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_16 | 16 | MD_GPIO_105 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_17 | 17 | +3V3 |  | power_output |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_18 | 18 | MD_GPIO_106 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_19 | 19 | MD_GPIO_26 | SE3_MOSI |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_20 | 20 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_21 | 21 | MD_GPIO_25 | SE3_MISO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_22 | 22 | MD_GPIO_107 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_23 | 23 | MD_GPIO_27 | SE3_SCK |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_24 | 24 | MD_GPIO_28 | SE3_CS |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_25 | 25 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_26 | 26 | MD_GPIO_88 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_27 | 27 | MD_GPIO_19 | SE1_SDA |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_28 | 28 | MD_GPIO_20 | SE1_SCL |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_29 | 29 | MD_GPIO_89 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_30 | 30 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_31 | 31 | MD_GPIO_80 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_32 | 32 | MD_GPIO_77 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_33 | 33 | MD_GPIO_81 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_34 | 34 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_35 | 35 | MD_GPIO_117 | I2S1_WS |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_36 | 36 | MD_GPIO_84 | SE2_CTS |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_37 | 37 | MD_GPIO_108 | GPIO |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_38 | 38 | MD_GPIO_118 | I2S1_DATA0 |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_39 | 39 | GND |  | ground_reference |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| JHAT_40 | 40 | MD_GPIO_119 | I2S1_DATA1 |  |  |  | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE0_SDA | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_5

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE0_SCL | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_7

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_8

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE2_TX | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| unavailable_while_bluetooth_active | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_10

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE2_RX | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| unavailable_while_bluetooth_active | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_11

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE2_RFR | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| unavailable_while_bluetooth_active | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_12

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S1_SCK | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_13

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_15

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_16

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_18

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_19

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE3_MOSI | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_21

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE3_MISO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_22

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_23

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE3_SCK | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_24

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE3_CS | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_26

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_27

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE1_SDA | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_28

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE1_SCL | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_29

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_31

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_32

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_33

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_35

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S1_WS | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_36

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SE2_CTS | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| unavailable_while_bluetooth_active | documented | yes | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_37

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_38

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S1_DATA0 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

#### JHAT_40

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S1_DATA1 | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

### JMEDIA

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JMEDIA_1 | 1 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_2 | 2 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_3 | 3 | MIPI_DSI0_CLK_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_4 | 4 | MIPI_DSI0_L1_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_5 | 5 | MIPI_DSI0_CLK_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_6 | 6 | MIPI_DSI0_L1_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_7 | 7 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_8 | 8 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_9 | 9 | MIPI_DSI0_L2_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_10 | 10 | MIPI_DSI0_L0_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_11 | 11 | MIPI_DSI0_L2_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_12 | 12 | MIPI_DSI0_L0_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_13 | 13 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_14 | 14 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_15 | 15 | MIPI_DSI0_L3_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_16 | 16 | SOC_CAM_MCLK0 | GPIO_67 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_17 | 17 | MIPI_DSI0_L3_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_18 | 18 | SOC_CAM_MCLK1 | GPIO_68 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_19 | 19 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_20 | 20 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_21 | 21 | CSI0_C0_LN0_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_22 | 22 | CCI_I2C2_SDA1 | GPIO_59 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_23 | 23 | CSI0_B0_LN0_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_24 | 24 | CCI_I2C2_SCL1 | GPIO_60 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_25 | 25 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_26 | 26 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_27 | 27 | CSI0_B1_LN1_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_28 | 28 | CSI1_B2_LN3_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_29 | 29 | CSI0_A1_LN1_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_30 | 30 | CSI1_C2_LN3_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_31 | 31 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_32 | 32 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_33 | 33 | CSI0_A0_CLK_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_34 | 34 | CSI1_C1_LN2_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_35 | 35 | CSI0_NC_CLK_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_36 | 36 | CSI1_A2_LN2_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_37 | 37 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_38 | 38 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_39 | 39 | CSI0_A2_LN2_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_40 | 40 | CSI1_NC_CLK_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_41 | 41 | CSI0_C1_LN2_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_42 | 42 | CSI1_A0_CLK_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_43 | 43 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_44 | 44 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_45 | 45 | CSI0_C2_LN3_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_46 | 46 | CSI1_A1_LN1_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_47 | 47 | CSI0_B2_LN3_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_48 | 48 | CSI1_B1_LN1_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_49 | 49 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_50 | 50 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_51 | 51 | CCI_I2C0_SCL1 | GPIO_58 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_52 | 52 | CSI1_B0_LN0_P |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_53 | 53 | CCI_I2C0_SDA1 | GPIO_57 |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_54 | 54 | CSI1_C0_LN0_M |  |  |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_55 | 55 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_56 | 56 | GND |  | ground_reference |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_57 | 57 | VIN (IN, 1.5 A max) |  | power_input |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_58 | 58 | +3V3 (OUT) |  | power_output |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_59 | 59 | VIN (IN, 1.5 A max) |  | power_input |  |  | [JMEDIA](sources/user_manual.md#jmedia) |
| JMEDIA_60 | 60 | +3V3 (OUT) |  | power_output |  |  | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_16

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_67 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_18

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_68 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_22

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_59 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_24

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_60 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_51

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_58 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_53

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_57 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_57

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 1.5 | [JMEDIA](sources/user_manual.md#jmedia) |

#### JMEDIA_59

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| max_current_a | documented | dimension: current; unit: A; rating kind: unspecified; max: 1.5 | [JMEDIA](sources/user_manual.md#jmedia) |

### JMISC

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JMISC_1 | 1 | MCU_PSSI_D0 | PA9 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_2 | 2 | MCU_TRACE_CLK | PE2 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_3 | 3 | MCU_PSSI_D1 | PC7 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_4 | 4 | MCU_TRACE_D0 | PE3 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_5 | 5 | MCU_PSSI_D2 | PC8 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_6 | 6 | MCU_TRACE_D1 | PE4 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_7 | 7 | MCU_PSSI_D3 | PE1 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_8 | 8 | MCU_TRACE_D2 | PE5 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_9 | 9 | MCU_PSSI_D4 | PC11 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_10 | 10 | MCU_TRACE_D3 | PE6 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_11 | 11 | MCU_PSSI_D5 | PD3 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_12 | 12 | MCU_USART2_RX | PE7 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_13 | 13 | MCU_PSSI_D6 | PF4 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_14 | 14 | MCU_USART2_TX | PE8 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_15 | 15 | MCU_PSSI_D7 | PI7 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_16 | 16 | MCU_I2C2_SCL | PF1 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_17 | 17 | MCU_PSSI_PDCK | PA6 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_18 | 18 | MCU_I2C2_SDA | PF0 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_19 | 19 | MCU_PSSI_RDY | PI5 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_20 | 20 | MCU_GPIO_PA0 | PA0 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_21 | 21 | MCU_PSSI_DE | PH8 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_22 | 22 | MCU_GPIO_PA1 | PA1 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_23 | 23 | MCU_UART4_RX | PA11 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_24 | 24 | MCU_GPIO_PA2 | PA2 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_25 | 25 | MCU_UART4_TX | PA12 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_26 | 26 | GND |  | ground_reference |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_27 | 27 | GND |  | ground_reference |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_28 | 28 | EAR_P |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_29 | 29 | MIC_IN+ |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_30 | 30 | EAR_M |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_31 | 31 | MIC_IN- |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_32 | 32 | LINEOUT_P |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_33 | 33 | MIC_BIAS |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_34 | 34 | LINEOUT_M |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_35 | 35 | GND |  | ground_reference |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_36 | 36 | HPH_L |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_37 | 37 | SOC_GPIO_10_SE0 | MISO |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_38 | 38 | HPH_R |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_39 | 39 | SOC_GPIO_11_SE0 | MOSI |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_40 | 40 | HPH_REF |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_41 | 41 | SOC_GPIO_12_SE0 | SCK |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_42 | 42 | HS_DET |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_43 | 43 | SOC_GPIO_13_SE0 | CS0 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_44 | 44 | GND |  | ground_reference |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_45 | 45 | SOC_GPIO_15_SE0 | CS2 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_46 | 46 | SOC_GPIO_120 | I2S2_SCK |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_47 | 47 | SOC_GPIO_14_SE0 | CS1 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_48 | 48 | SOC_GPIO_121 | I2S2_WS |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_49 | 49 | SOC_GPIO_73 |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_50 | 50 | SOC_GPIO_122 | I2S2_DATA0 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_51 | 51 | SOC_GPIO_74 |  |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_52 | 52 | SOC_GPIO_123 | I2S2_DATA1 |  |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_53 | 53 | +3V3 (OUT) |  | power_output |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_54 | 54 | +5V (OUT) |  | power_output |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_55 | 55 | +3V3 (OUT) |  | power_output |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_56 | 56 | +5V (OUT) |  | power_output |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_57 | 57 | +1V8 (OUT) |  | power_output |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_58 | 58 | GND |  | ground_reference |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_59 | 59 | SOC_VCOIN (IN) | MCU_VBAT | power_input |  |  | [JMISC](sources/user_manual.md#jmisc) |
| JMISC_60 | 60 | NC |  | not_connected |  |  | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_1

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA9 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA9 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_2

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE2 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE2 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_3

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PC7 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PC7 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_4

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE3 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE3 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_5

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PC8 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PC8 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_6

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE4 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE4 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_7

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE1 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE1 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_8

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE5 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE5 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_9

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PC11 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PC11 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_10

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE6 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE6 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_11

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PD3 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PD3 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_12

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE7 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE7 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_13

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PF4 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PF4 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_14

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PE8 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PE8 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_15

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PI7 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PI7 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_16

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PF1 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PF1 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_17

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA6 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA6 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_18

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PF0 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PF0 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_19

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PI5 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PI5 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_20

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA0 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA0 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_21

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PH8 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PH8 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_22

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA1 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA1 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_23

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA11 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA11 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_24

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA2 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA2 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_25

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA12 | [JMISC](sources/user_manual.md#jmisc) |
| mcu_pin | documented | PA12 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_37

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | MISO | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_39

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | MOSI | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_41

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | SCK | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_43

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | CS0 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_45

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | CS2 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_46

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S2_SCK | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_47

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | CS1 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_48

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S2_WS | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_50

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S2_DATA0 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_52

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | I2S2_DATA1 | [JMISC](sources/user_manual.md#jmisc) |

#### JMISC_59

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | MCU_VBAT | [JMISC](sources/user_manual.md#jmisc) |
| max_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; max: 3.3 | [JMISC](sources/user_manual.md#jmisc) |
| note | documented | MPU and MCU RTC backup only; not board backup power. | [JMISC](sources/user_manual.md#jmisc) |

### JOMEGA

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JOMEGA_1 | 1 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_2 | 2 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_3 | 3 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_4 | 4 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_5 | 5 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_6 | 6 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_7 | 7 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_8 | 8 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_9 | 9 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_10 | 10 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_11 | 11 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_12 | 12 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_13 | 13 | VIN (IN) |  | power_input |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_14 | 14 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_15 | 15 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_16 | 16 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_17 | 17 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_18 | 18 | USB1_SS_TX_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_19 | 19 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_20 | 20 | USB1_SS_TX_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_21 | 21 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_22 | 22 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_23 | 23 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_24 | 24 | USB1_HS_D_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_25 | 25 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_26 | 26 | USB1_HS_D_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_27 | 27 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_28 | 28 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_29 | 29 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_30 | 30 | USB1_SS_RX_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_31 | 31 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_32 | 32 | USB1_SS_RX_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_33 | 33 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_34 | 34 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_35 | 35 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_36 | 36 | USB2_SS_TX_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_37 | 37 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_38 | 38 | USB2_SS_TX_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_39 | 39 | MCU_GPIO_PC0 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_40 | 40 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_41 | 41 | MCU_GPIO_PC1 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_42 | 42 | USB2_HS_D_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_43 | 43 | MCU_GPIO_PC2 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_44 | 44 | USB2_HS_D_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_45 | 45 | MCU_GPIO_PC3 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_46 | 46 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_47 | 47 | MCU_GPIO_PD12 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_48 | 48 | USB2_SS_RX_P |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_49 | 49 | MCU_GPIO_PD13 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_50 | 50 | USB2_SS_RX_N |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_51 | 51 | MCU_GPIO_PD14 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_52 | 52 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_53 | 53 | MCU_GPIO_PD15 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_54 | 54 | USB1_PWRON |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_55 | 55 | MCU_GPIO_PI2 |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_56 | 56 | USB1_OVERCUR |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_57 | 57 | MIC2_IN+ |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_58 | 58 | USB2_PWRON |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_59 | 59 | MIC2_IN- |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_60 | 60 | USB2_OVERCUR |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_61 | 61 | MIC2_BIAS |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_62 | 62 | MISO | GPIO_39 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_63 | 63 | JTAG_TMS |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_64 | 64 | MOSI | GPIO_40 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_65 | 65 | JTAG_TDO |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_66 | 66 | SCK | GPIO_37 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_67 | 67 | JTAG_TDI |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_68 | 68 | CS | GPIO_38 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_69 | 69 | JTAG_TCK |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_70 | 70 | PM_PS_HOLD |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_71 | 71 | JTAG_SRST |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_72 | 72 | FORCE_USB_BOOT | GPIO_52 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_73 | 73 | JTAG_TRST |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_74 | 74 | POWER_EN |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_75 | 75 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_76 | 76 | USER_BUTTON | GPIO_79 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_77 | 77 | +1V8_SPX3 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_78 | 78 | PMIC_RESET |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_79 | 79 | +1V8 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_80 | 80 | RTSS_RESET |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_81 | 81 | +1V8 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_82 | 82 | RTSS_PS_HOLD |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_83 | 83 | QUP0_SE7_TX | GPIO_71 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_84 | 84 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_85 | 85 | QUP0_SE7_RX | GPIO_72 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_86 | 86 | FDCAN1_TX | PD5 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_87 | 87 | PWR_DISABLE |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_88 | 88 | FDCAN1_RX | PI9 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_89 | 89 | FORCE_BOOT |  |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_90 | 90 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_91 | 91 | +3V3 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_92 | 92 | FDCAN2_TX | PA10 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_93 | 93 | +3V3 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_94 | 94 | FDCAN2_RX | PD9 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_95 | 95 | +3V3 (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_96 | 96 | GND |  | ground_reference |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_97 | 97 | +5V (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_98 | 98 | FDCAN3_TX | PF6 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_99 | 99 | +5V (OUT) |  | power_output |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| JOMEGA_100 | 100 | FDCAN3_RX | PF7 |  |  |  | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_62

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_39 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_64

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_40 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_66

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_37 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_68

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_38 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_72

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_52 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_76

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_79 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_83

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_71 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_85

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | GPIO_72 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_86

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PD5 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PD5 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_88

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PI9 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PI9 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_92

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PA10 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PA10 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_94

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PD9 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PD9 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_98

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PF6 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PF6 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

#### JOMEGA_100

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| source_function | documented | PF7 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| mcu_pin | documented | PF7 | [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### QWIIC

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QWIIC_SCL | Not specified | PA8 |  | i2c_scl | I2C3_SCL |  | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| QWIIC_SDA | Not specified | PC9 |  | i2c_sda | I2C3_SDA |  | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |

#### QWIIC_SCL

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | QWIIC | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| note | documented | Controller designation conflicts with the Qwiic section. | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |

#### QWIIC_SDA

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | QWIIC | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |
| note | documented | Controller designation conflicts with the Qwiic section. | [I2C](sources/user_manual.md#i2c); [Qwiic](sources/user_manual.md#qwiic) |

### Unnumbered or logical board connections

| Pin | Position | Signal | Source function | Capabilities | Aliases | Shared with | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AREF | Not specified | AREF |  | adc_reference_input |  |  | [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc) |
| VIN | Not specified | VIN |  | power_input |  |  | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |

#### VIN

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| note | documented | UNO VIN input; 1.1 A PTC fuse; see voltage.uno_vin_input. | [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings) |

## Constraints and known issues

### source_conflict__qwiic_controller

**source_conflict:** Keep PA8 and PC9 from the explicit table; omit a definitive controller number.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | qwiic_controller | [Qwiic](sources/user_manual.md#qwiic); [I2C](sources/user_manual.md#i2c) |
| sections__0 | documented | Qwiic | [Qwiic](sources/user_manual.md#qwiic); [I2C](sources/user_manual.md#i2c) |
| sections__1 | documented | Communication / I2C | [Qwiic](sources/user_manual.md#qwiic); [I2C](sources/user_manual.md#i2c) |
| claims__0 | documented | I2C4 in the Qwiic section | [Qwiic](sources/user_manual.md#qwiic); [I2C](sources/user_manual.md#i2c) |
| claims__1 | documented | I2C3 on PA8 and PC9 in the I2C table | [Qwiic](sources/user_manual.md#qwiic); [I2C](sources/user_manual.md#i2c) |

### source_conflict__can_pd0_pd1

**source_conflict:** Keep CAN-H/CAN-L as bus signals; omit definitive MCU TX/RX routing for the onboard transceiver.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | can_pd0_pd1 | [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| sections__0 | documented | CAN-FD / CAN Interfaces | [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| sections__1 | documented | CAN-FD / CAN Transceiver Connections | [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| claims__0 | documented | CAN Interfaces lists PD0 as TX and PD1 as RX. | [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |
| claims__1 | documented | The transceiver table lists PD1 at TXD and PD0 at RXD; the terminal table follows that assignment. | [CAN Interfaces](sources/user_manual.md#can-interfaces); [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections) |

### source_conflict__bluetooth_version

**source_conflict:** Record both source claims without selecting a version.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | bluetooth_version | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| sections__0 | documented | Overview | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| sections__1 | documented | Board Architecture Overview | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| sections__2 | documented | Wireless Connectivity | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| claims__0 | documented | Overview and architecture state Bluetooth 5.3 | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| claims__1 | documented | Wireless Connectivity states Bluetooth 5.1 | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |

### source_conflict__isp_model

**source_conflict:** Omit a definitive ISP model.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | isp_model | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| sections__0 | documented | Overview | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| sections__1 | documented | Board Architecture Overview | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| sections__2 | documented | MIPI / CSI Camera | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| claims__0 | documented | Overview names Spectra 690 | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |
| claims__1 | documented | Architecture and camera sections name Spectra 692 | [Overview](sources/user_manual.md#overview); [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera) |

### source_conflict__wifi_band_description

**source_conflict:** Preserve the three stated bands without adopting the band-count wording.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | wifi_band_description | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| sections__0 | documented | Board Architecture Overview | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| sections__1 | documented | Wireless Connectivity | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| claims__0 | documented | Architecture calls Wi-Fi tri-band | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| claims__1 | documented | Wireless Connectivity calls it dual-band while listing 2.4/5/6 GHz | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |

### source_conflict__pwm_example_range

**source_conflict:** Omit the inconsistent example range; retain the documented eight-bit default.

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| topic | documented | pwm_example_range | [PWM Pins](sources/user_manual.md#pwm-pins) |
| sections__0 | documented | PWM Pins | [PWM Pins](sources/user_manual.md#pwm-pins) |
| claims__0 | documented | The ten-bit example comment says 0 to 4095 | [PWM Pins](sources/user_manual.md#pwm-pins) |

### resource_context__jhat_bluetooth_uart

**condition:** Additional source context for resource conflict jhat_bluetooth_uart

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | conditional_pin_ownership | [VENTUNO Q User Manual](sources/user_manual.md) |
| scope | documented | Both UART functions and GPIO use on these four pins | [VENTUNO Q User Manual](sources/user_manual.md) |

### resource_context__display_output_mux

**condition:** Additional source context for resource conflict display_output_mux

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | exclusive_display_route | [VENTUNO Q User Manual](sources/user_manual.md) |

### resource_context__adc_dac_exclusion

**condition:** Additional source context for resource conflict adc_dac_exclusion

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | peripheral_exclusion | [VENTUNO Q User Manual](sources/user_manual.md) |

### resource_context__analog_pin_functions

**condition:** Additional source context for resource conflict analog_pin_functions

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| type | documented | per_pin_function_exclusion | [VENTUNO Q User Manual](sources/user_manual.md) |
| note | documented | Applied separately to each pin, not a prohibition on using separate pins for different functions. | [VENTUNO Q User Manual](sources/user_manual.md) |

### multiplexing

**requirement:** Preserve source constraint group: multiplexing

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| analog_gpio_and_alternate_functions_mutually_exclusive | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| adc_and_dac_simultaneous_use_supported | documented | no | [VENTUNO Q User Manual](sources/user_manual.md) |
| hdmi_and_mipi_dsi_simultaneous_use_supported | documented | no | [VENTUNO Q User Manual](sources/user_manual.md) |
| jhat_unavailable_while_bluetooth_active__0 | documented | JHAT_8 | [VENTUNO Q User Manual](sources/user_manual.md) |
| jhat_unavailable_while_bluetooth_active__1 | documented | JHAT_10 | [VENTUNO Q User Manual](sources/user_manual.md) |
| jhat_unavailable_while_bluetooth_active__2 | documented | JHAT_11 | [VENTUNO Q User Manual](sources/user_manual.md) |
| jhat_unavailable_while_bluetooth_active__3 | documented | JHAT_36 | [VENTUNO Q User Manual](sources/user_manual.md) |
| note | documented | Listed alternate functions are not a guarantee of simultaneous availability. | [VENTUNO Q User Manual](sources/user_manual.md) |

### power

**requirement:** Preserve source constraint group: power

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| approximate_board_full_load_without_peripherals_w | documented | dimension: power; unit: W; rating kind: unspecified; value: 25 | [VENTUNO Q User Manual](sources/user_manual.md) |
| total_peripheral_power_budget_required | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| barrel_jack_over_5a_can_damage_board | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| carrier_and_jomega_rails_outside_limited_nets | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| carrier_current_limits_not_fully_specified | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| vin_header_power_headroom_limited | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| rtc_backup_pin | documented | JMISC_59 | [VENTUNO Q User Manual](sources/user_manual.md) |
| rtc_backup_max_voltage_v | documented | dimension: voltage; unit: V; rating kind: unspecified; max: 3.3 | [VENTUNO Q User Manual](sources/user_manual.md) |
| rtc_backup_cannot_power_whole_board | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |

### debug_uart

**requirement:** Preserve source constraint group: debug_uart

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| connector | documented | JCTL | [VENTUNO Q User Manual](sources/user_manual.md) |
| tx_rx_backpowering_can_prevent_boot | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| board_referenced_adapter_required | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| manufacturer_recommended_adapter | documented | Arduino_Bughopper | [VENTUNO Q User Manual](sources/user_manual.md) |

### expansion

**requirement:** Preserve source constraint group: expansion

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| power_off_before_connecting_external_devices | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| m2_nvme_2230_only | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| camera_module_supported_by_manual | documented | IMX577 | [VENTUNO Q User Manual](sources/user_manual.md) |
| camera_support_note | documented | Support statement belongs to the manual snapshot, not an exhaustive hardware compatibility claim. | [VENTUNO Q User Manual](sources/user_manual.md) |

### physical

**requirement:** Preserve source constraint group: physical

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| mounting_standoffs_required | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| conductive_surface_short_circuit_risk | documented | yes | [VENTUNO Q User Manual](sources/user_manual.md) |
| uno_shield_compatibility | documented | Mechanical and pin compatibility only; software compatibility is not established. | [VENTUNO Q User Manual](sources/user_manual.md) |

### unspecified

**requirement:** Preserve source constraint group: unspecified

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| 0 | documented | UNO header input tolerance and per-pin current limits are not established by the local manual text. | [VENTUNO Q User Manual](sources/user_manual.md) |
| 1 | documented | No global logic voltage is assigned because connectors span multiple voltage domains. | [VENTUNO Q User Manual](sources/user_manual.md) |

## Onboard and wireless features

### led_matrix

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| rows | documented | dimension: count; unit: count; rating kind: unspecified; value: 8 | [LED Matrix](sources/user_manual.md#led-matrix) |
| columns | documented | dimension: count; unit: count; rating kind: unspecified; value: 13 | [LED Matrix](sources/user_manual.md#led-matrix) |
| color | documented | blue | [LED Matrix](sources/user_manual.md#led-matrix) |

### rgb_leds

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| count | documented | dimension: count; unit: count; rating kind: unspecified; value: 4 | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| polarity | documented | active_low | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED1__0 | documented | LED1_R | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED1__1 | documented | LED1_G | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED1__2 | documented | LED1_B | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED2__0 | documented | LED2_R | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED2__1 | documented | LED2_G | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED2__2 | documented | LED2_B | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED3__0 | documented | LED3_R | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED3__1 | documented | LED3_G | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED3__2 | documented | LED3_B | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED4__0 | documented | LED4_R | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED4__1 | documented | LED4_G | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| channel_labels__LED4__2 | documented | LED4_B | [RGB LEDs](sources/user_manual.md#rgb-leds) |
| note | documented | MCU port mappings are not given in the manual text. | [RGB LEDs](sources/user_manual.md#rgb-leds) |

### user_button

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| maps_to | documented | GPIO_79 | [User Button](sources/user_manual.md#user-button); [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |
| exposed_at | documented | JOMEGA_76 | [User Button](sources/user_manual.md#user-button); [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header) |

### power_button

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| long_press_shutdown_min_s | documented | dimension: time; unit: s; rating kind: unspecified; min: 10 | [Power Button](sources/user_manual.md#power-button) |
| power_cycle_required_after_long_press | documented | yes | [Power Button](sources/user_manual.md#power-button) |
| automatic_boot_on_power | documented | yes | [Power Button](sources/user_manual.md#power-button) |

### wireless

| Fact | Evidence state | Value / documented limits | Sources |
| --- | --- | --- | --- |
| bluetooth_version | conflicting | Conflicting claims: 5.3; 5.1 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity) |
| module | documented | NFA725B | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| wifi__standard | documented | Wi-Fi_6 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| wifi__stated_bands_ghz__0 | documented | dimension: frequency; unit: GHz; rating kind: unspecified; value: 2.4 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| wifi__stated_bands_ghz__1 | documented | dimension: frequency; unit: GHz; rating kind: unspecified; value: 5 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| wifi__stated_bands_ghz__2 | documented | dimension: frequency; unit: GHz; rating kind: unspecified; value: 6 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| bluetooth__version_status | documented | conflicting_source_claims | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| onboard_antennas | documented | dimension: count; unit: count; rating kind: unspecified; value: 2 | [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |

## Sources

- legacy_snapshot: [Pre-migration repository definition](../../../../docs/evidence/migration-2026-11-19/before/arduino__ventuno-q.yml.txt)
- manual: [VENTUNO Q User Manual](sources/user_manual.md); snapshot 2026-11-19
- overview: [Overview](sources/user_manual.md#overview); snapshot 2026-11-19
- architecture: [Board Architecture Overview](sources/user_manual.md#board-architecture-overview); snapshot 2026-11-19
- power: [Power Overview](sources/user_manual.md#power-overview); snapshot 2026-11-19
- power_safety: [Power Safety Considerations](sources/user_manual.md#power-safety-considerations); snapshot 2026-11-19
- usb_a_power: [USB-A Power Draw](sources/user_manual.md#usb-a-power-draw); snapshot 2026-11-19
- limited_rails: [5 V / 3.3 V Power Rails](sources/user_manual.md#5-v--33-v-power-rails); snapshot 2026-11-19
- vin: [VIN Pin Ratings](sources/user_manual.md#vin-pin-ratings); snapshot 2026-11-19
- digital: [Digital Pins](sources/user_manual.md#digital-pins); snapshot 2026-11-19
- analog: [Analog Pins](sources/user_manual.md#analog-pins); snapshot 2026-11-19
- adc: [Analog to Digital Converter (ADC)](sources/user_manual.md#analog-to-digital-converter-adc); snapshot 2026-11-19
- dac: [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac); snapshot 2026-11-19
- pwm: [PWM Pins](sources/user_manual.md#pwm-pins); snapshot 2026-11-19
- qwiic: [Qwiic](sources/user_manual.md#qwiic); snapshot 2026-11-19
- usb_c: [USB-C Connector](sources/user_manual.md#usb-c-connector); snapshot 2026-11-19
- usb_a: [USB-A Connectors](sources/user_manual.md#usb-a-connectors); snapshot 2026-11-19
- ethernet: [Ethernet Connector](sources/user_manual.md#ethernet-connector); snapshot 2026-11-19
- hdmi: [HDMI](sources/user_manual.md#hdmi); snapshot 2026-11-19
- m2: [M.2 Connector](sources/user_manual.md#m2-connector); snapshot 2026-11-19
- jhat: [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header); snapshot 2026-11-19
- cameras: [MIPI / CSI Camera](sources/user_manual.md#mipi--csi-camera); snapshot 2026-11-19
- can: [CAN-FD](sources/user_manual.md#can-fd); snapshot 2026-11-19
- can_interfaces: [CAN Interfaces](sources/user_manual.md#can-interfaces); snapshot 2026-11-19
- can_transceiver: [CAN Transceiver Connections](sources/user_manual.md#can-transceiver-connections); snapshot 2026-11-19
- jmedia: [JMEDIA](sources/user_manual.md#jmedia); snapshot 2026-11-19
- jmisc: [JMISC](sources/user_manual.md#jmisc); snapshot 2026-11-19
- jomega: [JOMEGA Expansion Header](sources/user_manual.md#jomega-expansion-header); snapshot 2026-11-19
- spi: [SPI](sources/user_manual.md#spi); snapshot 2026-11-19
- i2c: [I2C](sources/user_manual.md#i2c); snapshot 2026-11-19
- uart: [UART](sources/user_manual.md#uart); snapshot 2026-11-19
- wireless: [Wireless Connectivity](sources/user_manual.md#wireless-connectivity); snapshot 2026-11-19
- form_factor: [Form Factor](sources/user_manual.md#form-factor); snapshot 2026-11-19
- clearance: [Board Clearance](sources/user_manual.md#board-clearance); snapshot 2026-11-19
- debug_uart: [Hardware Debug UART Interface](sources/user_manual.md#hardware-debug-uart-interface); snapshot 2026-11-19
- led_matrix: [LED Matrix](sources/user_manual.md#led-matrix); snapshot 2026-11-19
- rgb_leds: [RGB LEDs](sources/user_manual.md#rgb-leds); snapshot 2026-11-19
- user_button: [User Button](sources/user_manual.md#user-button); snapshot 2026-11-19
- power_button: [Power Button](sources/user_manual.md#power-button); snapshot 2026-11-19
- linked_full_pinout: [Full Pinout](https://docs.arduino.cc/resources/pinouts/ABX00181-full-pinout.pdf)
- linked_datasheet: [Datasheet](https://docs.arduino.cc/resources/datasheets/ABX00181-datasheet.pdf)
- linked_schematics: [Schematics](https://docs.arduino.cc/resources/schematics/ABX00181-schematics.pdf)

Original source snapshots and the [migration field map](../../../../docs/evidence/migration-2026-11-19/field-map.json) preserve historical context. No unresolved source claim was silently corrected.

See [source limitations](sources/README.md) for inherited missing images/site-relative links.
