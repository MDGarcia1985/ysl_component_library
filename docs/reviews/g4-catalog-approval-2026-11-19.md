# G4 catalog packaging review

**Template used:** [CLI gate review record](../planning/CLI_GATE_REVIEW_TEMPLATE.md).  
**Decision received:** The user widened the G4 scope to the whole catalog.  
**User message:** "go ahead and package all of them. It's only five and will be a good test."  
**Recorded date:** 2026-11-19  
**Scope:** Package the five-definition catalog as one unit, bound to the same
pre-package candidate as the earlier Ventuno-only statement. This record does
not authorize publication, upload, or G5 acceptance.

This is a repository copy of a decision received in the user conversation. It is
not an agent-created signature, an independent evaluator, or proof that the
agent's own files were outside the agent's write access. The human decision is
the chat statement quoted above. No other reviewer is named because the message
did not name one.

## Review identity

- Gate and phase: G4, authorizing P5 for the five-definition catalog
- Review record ID: g4-catalog-approval-2026-11-19
- Date, time, and time zone: 2026-11-19, recorded 17:16 America/New_York from the user statement received in this session
- Reviewer identity and role: the user, chat decision. No personal name was stated.
- Decision: APPROVED
- Approval scope: one package containing the five definitions and the approved schemas from the candidate below. Publication and upload are outside this approval.
- Trusted human approval reference: user chat statement "go ahead and package all of them. It's only five and will be a good test."
- Prior or superseded review: [Ventuno-only G4 record](g4-approval-2026-11-19.md). That record's commit binding stands. Its limit to `arduino/ventuno-q` is superseded by this statement. The earlier file is unchanged.

## Candidate and evaluator identity

- Candidate commit and dirty/untracked status, when Git is available: `bbf013354b3ac7d4fdc9be8b44090634b431b118`, the merge of pull request 3. Git tree `4eb01ea1ec9bea7bf7d537da5495890f9e03f0f3`. The five definitions and schema files are unchanged after that commit. Packaging edits are the later G4-to-G5 diff.
- Complete candidate file-manifest digest: not a separate sealed manifest. Identity for this approval is that commit plus the digests below.
- Approved baseline/source manifest digest: the definition digests match the Ventuno-only record and the G3 record.
- Contract revision and digest: acceptance contracts remain Draft 1. AC-502 through AC-505 are unchanged. The installed-command details that those rows left open are frozen in [CLI_PACKAGING_CONTRACT.md](../planning/CLI_PACKAGING_CONTRACT.md).
- Evaluator and expected-result fixture digests: local self-evaluation only. No reviewer-controlled runner was supplied.
- Held-out fixture identities and reproducibility reference: none supplied with the approval
- Evidence bundle manifest digest: P4 evidence remains [docs/evidence/pages-2026-11-19](../evidence/pages-2026-11-19/README.md). Packaging evidence is collected separately and is not this approval.
- Trusted external manifest/evaluator location: not provided. The chat statement is the external decision.
- Compared candidate versus prior approved candidate: same commit and the same five definition bytes. The scope now includes all five definitions instead of `arduino/ventuno-q` alone.

Digests covered by this approval (LF bytes):

| Artifact | SHA-256 |
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

## Required evidence review

- Applicable AC IDs and execution TEST IDs: AC-501 remains a denial check for absent, local, wrong-gate, and wrong-candidate requests. AC-502 through AC-505 are the packaging checks. Their execution is recorded in TEST_LOG after the build, not by this approval.
- Required / collected / executed case counts: this record does not claim those cases have already passed
- Passing / failing / skipped / not-executed case counts: not established by the chat statement
- Independent reproduction report and executor: none
- Raw subprocess logs and exit-status report: none in this approval
- Independent migration conservation and source-oracle comparisons: unchanged. This statement does not correct hardware facts.
- Deliberate corruption cases and observed detections/survivors: not re-run for this decision
- Generated pages, navigation checks, and visual evidence: unchanged from the P4 bundle. This statement does not ask for a page rewrite.
- Platform/environment coverage: Windows remains not executed
- Known source contradictions and incomplete hardware verification: all six VENTUNO discrepancies remain unresolved. Physical verification remains `not_verified`.
- Test/fixture/expectation changes since freeze and their approvals: AC rows are not rewritten. The packaging contract freezes only the installed-command choices those rows left open.
- Exceptions and supporting human-reviewed DEV IDs: DEV-2026-11-19-011 recorded the narrower scope and stopped. DEV-2026-11-19-012 records this widening.

## Reviewer observations

- Facts personally traced to source sections: not stated in the approval message
- Commands personally reproduced and observed outcomes: not stated in the approval message
- Pages/connector/variant views personally inspected: not stated in the approval message
- Missing evidence or disputed outcomes: no independent evaluator. Windows remains not executed. The message names the five definitions as the package scope and calls the package a test. It does not authorize upload.
- Required corrections and acceptance conditions: package the five together. Do not publish.

## Decision and authorized next action

APPROVED to package the five-definition catalog as one unit, bound to commit `bbf013354b3ac7d4fdc9be8b44090634b431b118` and the digests above. P5 may fill in `pyproject.toml`, build a wheel and sdist, and install `ysl-components` for a local check. Publication and upload are not authorized. G5 has not started.

The blank gate template still grants nothing by itself. This filled record only
cross-references the user's chat statement.
