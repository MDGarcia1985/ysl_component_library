Excerpt of generated Markdown for review. The generated page is authoritative.

```markdown
## Resource conflicts

| ID | Pins | Participants | Policy | Condition | Source rule | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| jhat_bluetooth_uart | JHAT_8, JHAT_10, JHAT_11, JHAT_36 | component:nfa725b, interface:JHAT_UART_SE2 | unavailable_when | target: component:nfa725b; state: bluetooth_active | unavailable_to_external_header_while_bluetooth_active | [RPi 40-Pin Header](sources/user_manual.md#rpi-40-pin-header) |
| display_output_mux |  | connector:HDMI, interface:JMEDIA_MIPI_DSI | at_most_one_active |  | at_most_one_active | [HDMI](sources/user_manual.md#hdmi) |
| adc_dac_exclusion |  | interface:UNO_ADC, interface:UNO_DAC | not_simultaneous |  | not_simultaneous_as_stated_by_manual | [Digital to Analog Converter (DAC)](sources/user_manual.md#digital-to-analog-converter-dac) |
| analog_pin_functions | A0, A1, A2, A3, A4, A5 |  | per_pin_exclusion |  | gpio_and_alternate_function_not_simultaneous_on_same_pin | [Analog Pins](sources/user_manual.md#analog-pins) |


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

```
