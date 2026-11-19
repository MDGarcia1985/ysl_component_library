# Schema and identity approval

**Decision received:** The user approved the delivered schema/ID review candidate
and instructed the agent to move to the next phase.  
**User message:** "approved. Please move to next phase."  
**Recorded date:** 2026-11-19  
**Scope:** Adopt the exact reviewed `1.0.0-draft.1` contract and proposed IDs for P2
catalog migration. CLI implementation, packaging, and publication are not approved
by this record. G2 migration review remains a separate review.

This is a repository copy of authorization actually received in the conversation,
not an agent-created signature or proof of an independent evaluation environment.
No externally controlled G0 test runner is claimed. Local test evidence remains
self-evaluated, and that limitation is retained through P2.

## Approved artifact identity

The migration baseline captured these bytes before changes. Schema and registry
files remain byte-identical, including their historical draft/proposed annotations;
this dated user decision records their adoption without rewriting the approved
artifacts or silently changing the contract. A stable release/version change is
separate future work.

| Reviewed file | SHA-256 |
| --- | --- |
| `schemas/common.schema.json` | `dadb536021ff0b86d306cffc693301fc4798363234522cad0e1c12d15358290c` |
| `schemas/component.schema.json` | `bcde9d946602ffa8daad1037f08083e8d6271031016a313bbe2b755f2e81f86e` |
| `schemas/hardware.schema.json` | `9578832cc1fc98f93d0881bc5d90effe609576c5c6b7d9ef4474fa8d36ccaf49` |
| `schemas/identity-registry.schema.json` | `fa5b7a63ac7722bf3cf0f1e7e337983ba8ffc5dd89678309210e757938598c3a` |
| `schemas/provenance.schema.json` | `a2860a69c364d5a1a1dbaf89e8a5eff28e42d8829d106da1d8178df00b05bc37` |
| `schemas/relations.schema.json` | `964b36b4cc4baa0987ee8c53b5b08a43576d96b6eef562dbc6bb899cda656906` |
| `schemas/identity-registry.json` | `1d57e6b00defbc08b42e4679fb58af2b3d8efa2ed6799a3c6cd4073d9ff3cd53` |

## Next action and review boundary

Perform P2 normalization and preservation checks against this contract. Retain
original YAML bytes, every original data value, all variants/shared pins and source
conflicts, and complete source/destination mappings. Present the migrated catalog
and evidence at [the migration review index](../evidence/migration-2026-11-19/README.md).
Do not infer G2 acceptance or G4 packaging approval from the schema approval.
