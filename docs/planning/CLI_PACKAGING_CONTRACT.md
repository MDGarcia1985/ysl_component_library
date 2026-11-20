# P5 packaging contract

**Status:** Frozen for the widened G4 approval. G5 has not accepted the installed package. Publication is not authorized.  
**Revision:** 1  
**Date:** 2026-11-19  
**Related decision:** DEV-2026-11-19-012  
**Governs:** AC-502 through AC-505, and the AC-501 success boundary that P4 left closed

The [catalog approval](../reviews/g4-catalog-approval-2026-11-19.md) authorizes
one package of the five definitions. The approved candidate is commit
`bbf013354b3ac7d4fdc9be8b44090634b431b118`. Query contract revision 1 still
governs `python -m ysl_components`. This document freezes only the installed
command and the package contents. It does not approve upload.

## Package identity

- Distribution name: `ysl-components`
- Import package: `ysl_components`
- Version: `1.0.0a1`
- Console script: `ysl-components`
- Python: 3.11 or newer
- Dependencies: `jsonschema==4.23.0`, `referencing==0.30.2`, `PyYAML==6.0.2`
- License expression: `MPL-2.0 AND CC-BY-4.0`
- `tool.ysl_component_library.packaging_enabled` is true
- `tool.ysl_component_library.publish_authorized` is false

`1.0.0a1` names the first packaged candidate. It is not a release and not G5 acceptance.

## Approved inputs

The wheel and the sdist contain these files, byte for byte, at the paths below.
The packaged catalog root is `ysl_components/data/catalog/`. Relative definition
paths stay `hardware/.../definition.yml`, so the catalog digest matches a
checkout of the approved commit when `--catalog` is the repository root.

| Repository path | SHA-256 |
| --- | --- |
| `hardware/controllers/arduino/uno_r3/definition.yml` | `75d1a787a0bc25efe6ea6e8b0a28a13e99536c6faf3a5f4a5891aef3410bf424` |
| `hardware/controllers/arduino/ventuno_q/definition.yml` | `db3c7fe1af1a69a61dae54787cf7f70b5222a9c066284c75e7f83e455d6826c2` |
| `hardware/controllers/microchip/attiny_x5/definition.yml` | `ad4941e41c70630117326bc7bc72eb97260a83827acb7acab92a480eaba3a5e7` |
| `hardware/drivers/ti/l293_family/definition.yml` | `f06b44363eb83aede66911784cade72d2bf87dd2da7a9556cac2ad2a9d54dbaf` |
| `hardware/sensors/generic/hc_sr04/definition.yml` | `87df349469095a0b91948b5d6a126b147656ce3700520abc6e47c6f31ca576a6` |
| `schemas/common.schema.json` | `5b73aa2fc6df9750574ef6c47d79220fea219ae01c80ea7b209d4822be476d89` |
| `schemas/component.schema.json` | `a1e6cad3ee234e821313d308776e7ec3bfdef7a097769f3a2da01c70fa0806fd` |
| `schemas/hardware.schema.json` | `489cf4f87810ea9de156035b579b0e1031757533a2cb4d7193bbdc9943d45b37` |
| `schemas/identity-registry.schema.json` | `277e25a3b28f50a9d9239fae5a733a0da4cf2cc70bbeb0f96b4baa04bc7f2c05` |
| `schemas/provenance.schema.json` | `845a31e2c27a762da3c1631a6d385437692fc6b4d595712ba1c6613c7eb45bc9` |
| `schemas/relations.schema.json` | `51d893f726a0e30ebfee2d5c4fb41c6b9d1e3096264343e0f56d2a8acc4ebdb8` |
| `schemas/identity-registry.json` | `f25ec4890fe085a5a948b2bea2d98952244a780d618a73fcbdf0328cfa2620a6` |

The VENTUNO manual snapshot is not in the wheel or the sdist. `LICENSE.md` says
to confirm Arduino's terms before redistributing that snapshot. The definitions
keep their source citations. `LICENSE.md` and the two license texts are included.

Generated pages are not package data. Their text is unchanged, including the
sentence that packaging is disabled.

## Installed command

```text
ysl-components [ --catalog CATALOG ] OPERATION [options]
```

Omitting `--catalog` selects the packaged catalog. Passing `--catalog` selects
that directory instead and does not read the packaged definitions. Stdout, stderr,
exit codes, and operations stay on query contract revision 1.

`python -m ysl_components` still requires `--catalog`. It does not grow a default.

Schemas load from `ysl_components/data/schemas` inside an installed package. A
source checkout that has no packaged data directory still loads `schemas/` beside
`src/`. No schema is downloaded.

## AC-501 boundary

Absent approval, a local `approved` flag, a non-external channel, and a gate
other than G4 stay denied. An external G4 whose candidate does not match the
requested digest is `candidate_mismatch`. An external G4 whose digest matches
the request but is not `bbf013354b3ac7d4fdc9be8b44090634b431b118` is
`candidate_not_approved`. The builder is not called for those requests.

An external G4 bound to that commit returns `approved` and may call a supplied
builder. The function does not upload and does not treat a repository file as
the human decision.

## Build and install check

From a temporary directory outside the repository, build a wheel and an sdist,
install the wheel in a new virtual environment, and run `list`, `show`, `pin`,
and `export` with a working directory that is not the repository. Rebuild a wheel
from the sdist and compare the packaged definition and schema digests with the
table above. Do not upload.

Windows is not claimed. A missing platform stays unverified.
