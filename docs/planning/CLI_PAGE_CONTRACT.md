# P4 page and evidence contract

**Status:** Frozen for P4 page behavior. The widened G4 approval opened packaging for the five-definition catalog. Unapproved digests stay denied. Publication is not authorized.  
**Revision:** 1  
**Date:** 2026-11-19  
**Related decision:** DEV-2026-11-19-009  
**Governs:** AC-401 through AC-405, and the AC-501 denial only

This document freezes generated paths, the fact oracle, link and asset checks,
and the packaging-denial reasons before page generation is treated as accepted.
It does not approve packaging, an installed command, or publication. Query
contract revision 1 is unchanged. Page generation is not a query operation.

An agent-writable copy of this file is not a human approval of the results.
Executable cases live in `tests/test_page_contract.py`. The literal fact oracle
lives in `tests/page_checks.py`. Those tests are self-evaluated until a reviewer
runs them outside this workspace.

## Generation

From the repository root, with Python 3.11 or newer and PyYAML available:

```text
python src/ysl_components/reference_pages.py
```

The script reads `hardware/**/definition.yml` and writes exactly these files:

| Output | Role |
| --- | --- |
| `docs/catalog.md` | Category and namespace index |
| `hardware/controllers/arduino/uno_r3/README.md` | Uno R3 page |
| `hardware/controllers/arduino/ventuno_q/README.md` | VENTUNO Q page |
| `hardware/controllers/microchip/attiny_x5/README.md` | ATtiny x5 family page |
| `hardware/drivers/ti/l293_family/README.md` | L293 family page |
| `hardware/sensors/generic/hc_sr04/README.md` | HC-SR04 page |

No other path is a generated page. A component `sources/` directory is authored
guidance. Generated files begin with an HTML comment that says they were
generated and tells the reader not to edit them by hand. Component comments
include the SHA-256 of that component's `definition.yml`. Running the generator
twice on the same bytes produces the same text. Development invocation of
queries remains `python -m ysl_components` and does not write these pages.

## What each generated page shows

The catalog lists all five stable IDs, links each reference page and definition,
states the regeneration command, and states that packaging is disabled. It
points at the G3 cross-reference without itself being that approval.

Each component page shows the stable ID, verification status `not_verified`, a
verification-limits line, declared pin capabilities, connector and pin tables,
power facts that exist on the component, sources, and known conflicts. Family
pages name their variant and profile selectors. Uncertainty stays visible.
Conflicting claims are listed and not reduced to one chosen value. A generated
page does not say that a connection is electrically safe or that the hardware
was bench verified.

## Fact oracle

These observations are literals. They are not taken from renderer snapshots.

- Uno pin `D5` maps to `PD5`. VENTUNO pin `D5` maps to `PB5`.
- Uno shows `i2c_sda`. VENTUNO shows `I2C3_SDA`.
- VENTUNO keeps the six conflict topics `qwiic_controller`, `can_pd0_pd1`,
  `bluetooth_version`, `isp_model`, `wifi_band_description`, and
  `pwm_example_range`, and the stated `2.8` rail figure.
- ATtiny selectors are `ATtiny25`, `ATtiny45`, `ATtiny85`, `ATtiny25V`,
  `ATtiny45V`, and `ATtiny85V`.
- L293 continuous current is `1.0` and integrated clamp diodes are false.
  L293D continuous current is `0.6` and integrated clamp diodes are true.
- HC-SR04 keeps `host_must_measure_echo_pulse_width` and
  `echo_level_shift_required_for_3v3_only_host`. Its manufacturer remains unknown.
- Every component page shows `not_verified`.

## Link, asset, and evidence checks

Local links and heading fragments in the generated pages must resolve. A removed
target, a broken fragment, a missing image inserted into generated output, or a
VENTUNO `D5` row changed from `PB5` to `PD5` must be reported. Image references
that already exist inside the VENTUNO manual, and whose files are absent, are
source limitations. They are inventoried and are not counted as generated-page
assets.

Markdown and HTML metacharacters in a component label or fact are rendered as
text. They must not become a live HTML tag, a `javascript:` link, or an extra
table column.

The evidence manifest lists SHA-256 digests of the evidence artifacts. Removing
or changing a listed file is a manifest failure. The report names the candidate,
the tests, the environment, the results, and the remaining limitations. A second
local run can match the first. That match is not an independent reviewer.

## AC-501 denial

`request_package_build` classifies a request and returns. It does not read a
local `approved: true` value as authorization. It calls a builder only for the
approved candidate, and it does not upload.

| Request | Reason |
| --- | --- |
| No approval record | `approval_absent` |
| `approved: true` or any channel other than `external` | `local_approval_is_not_authorization` |
| External channel whose gate is not `G4` | `wrong_gate` |
| External `G4` bound to a different candidate digest | `candidate_mismatch` |
| External `G4` bound to a digest other than `bbf013354b3ac7d4fdc9be8b44090634b431b118` | `candidate_not_approved` |

Absent, local, wrong-gate, and mismatched requests stay denied, and their builder
is not called. A later statement first limited G4 to `arduino/ventuno-q`
([g4-approval-2026-11-19.md](../reviews/g4-approval-2026-11-19.md)). The user then
authorized the five-definition catalog
([g4-catalog-approval-2026-11-19.md](../reviews/g4-catalog-approval-2026-11-19.md)).
The success path for that commit is the [packaging contract](CLI_PACKAGING_CONTRACT.md).
It does not upload. Generated pages still say packaging is disabled; that sentence
was not rewritten.
