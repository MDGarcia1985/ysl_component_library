# P5 packaging evidence

**State:** Local Linux self-evaluation of the installed package. This index is not G5 acceptance and not permission to publish.  
**Date:** 2026-11-19  
**Contract:** [Packaging contract revision 1](../../planning/CLI_PACKAGING_CONTRACT.md)  
**Approval:** [G4 catalog approval](../../reviews/g4-catalog-approval-2026-11-19.md)

The user statement "go ahead and package all of them. It's only five and will be a good test." authorizes one package of the five definitions. It is bound to commit `bbf013354b3ac7d4fdc9be8b44090634b431b118`. No other reviewer is named. Nothing was uploaded.

## What was run

The wheel `ysl_components-1.0.0a1-py3-none-any.whl` and the sdist `ysl_components-1.0.0a1.tar.gz` were built outside the repository. The wheel was installed in a new virtual environment. `ysl-components` then ran with a working directory that was not the repository and with `PYTHONPATH` unset.

| Command | Exit |
| --- | --- |
| `ysl-components list` | 0 |
| `ysl-components show arduino/ventuno-q` | 0 |
| `ysl-components pin arduino/ventuno-q D5` | 0 |
| `ysl-components export arduino/ventuno-q --format json --output ventuno.json` | 0 |
| `ysl-components list` with network sockets blocked | 0 |

`list` returned `arduino/uno-r3`, `arduino/ventuno-q`, `generic/hc-sr04`, `microchip/attiny-x5`, and `ti/l293-family`. The pin query mapped VENTUNO `D5` to `PB5`. Packaged definition and schema digests are in [checks.json](checks.json). The wheel does not contain `user_manual.md`.

The same observations are executed by `python -m unittest tests.test_packaging_contract`. That run also rebuilds a wheel from the sdist and compares the digests again. An earlier wheel omitted the Python modules and the installed command failed; that result is TEST-2026-11-19-023. After the package selection was corrected, the full suite on this machine was 40 tests, OK. That result is TEST-2026-11-19-024.

## Limitations

- Windows AC-504 was not executed.
- No independent evaluator ran the install.
- Generated pages still say packaging is disabled. Their text was not changed.
- The VENTUNO manual snapshot is not in the package. `LICENSE.md` says to confirm Arduino's terms before redistributing it.
- G5 has not reviewed the installed package. Publication remains unauthorized.
- The six VENTUNO discrepancies remain unresolved. Verification remains `not_verified`.
