# Schema review evidence

**State:** Local self-evaluation of a review draft. No human or independent gate
approval is claimed. No migration, query package, packaging metadata, distribution,
or installation was implemented. Existing hardware files are unchanged.

Start with the [schema guide](../../../schemas/README.md),
[root schema](../../../schemas/component.schema.json), and
[proposed identity registry](../../../schemas/identity-registry.json).

## Test-first record

The three synthetic examples and seven review test methods were authored before
replacing the rejecting placeholder. The initial run returned 1 with two failures
and three errors among seven methods because the draft resources, ID registry,
and semantic/parsing harness did not yet exist. Expected missing implementation
was retained as a red baseline rather than reported as success:

- [Initial stdout](before.stdout.txt)
- [Initial stderr](before.stderr.txt)
- [Initial exit status](before.exit-code.txt)
- [Pre-change hardware, pyproject, and journal-prefix digests](before.json)

The earlier preparation test's expectation that the schema always reject every
input was replaced with a check that the now-authorized schema is explicitly an
unapproved draft. Its packaging-disabled checks remain. The new suite additionally
requires all five legacy catalog definitions to remain unchanged and to be rejected
by the new flat schema until migration is separately authorized.

## Coverage and boundaries

| Acceptance contract | Local review evidence | Remaining boundary |
| --- | --- | --- |
| AC-101 | Board/family/module fixtures validate, including unknown manufacturer and uncited facts; all six schemas pass metaschema checking. | Synthetic examples; no claim that catalog migration is complete. |
| AC-102 | Required identity, versions, closed fields, kind discrimination, quantities/units, unknown/conflicting payloads, and formats reject deliberate invalid inputs. | JSON Schema keyword diagnostics plus local semantic codes; the stable production CLI diagnostic envelope is not implemented. |
| AC-103 | Strict review loader rejects duplicate keys, aliases/anchors/merge keys/tags, extra documents, non-string keys, implicit dates, and nonfinite numbers; quoted labels survive. | Test-only loader; no installed parser or CLI. |
| AC-104 | Proposed registry shape, exact five IDs, actual legacy aliases/selectors, and case-folded alias/ID collision rejection. Filesystem paths do not determine IDs. | No real query command exists; moving/query behavior is not claimed as exercised. |
| AC-105 | Reference existence, scoped positions including numeric equivalent positions, upper position bounds, quantity ordering, member scope, and inheritance/power cycles. | Full migrated-data validation and query semantics remain later work. |

The harness also rejects a claimed bench-tested state backed only by failed bench
records and a conflict with identical competing values. Such structural checks do
not authenticate records or establish actual physical verification.

## Reproduce

With Python 3.11+, PyYAML, jsonschema, and referencing already available, run:

```shell
python -B -m unittest discover -s tests -p test_schema_review.py -v
python -B tests/collect_schema_review_evidence.py
```

The collector runs all preparation and schema methods, records successful and
failing subtests, refuses optimization, and requires nonempty collection and no
skips. It registers schemas locally and enables date/URI format checks. No
dependency installation or project package build is part of these commands.

- [Final stdout](after.stdout.txt)
- [Final stderr and test results](after.stderr.txt)
- [Final exit status](after.exit-code.txt)
- [Structured methods/subcases, environment, and navigation checks](checks.json)
- [Local file digest inventory](manifest.json)

The [first collector attempt](first-collector-attempt/checks.json) retained all
15 successful test methods but failed navigation because three report targets
had not been written yet. Its exit status and raw reports remain archived.
The collector now writes explicitly pending, non-success states before checking
links to its own outputs, then finalizes the actual results and digests.

The existing hardware tree and `pyproject.toml` must retain their pre-change byte
digests; historical root journal prefixes must remain unchanged. Root journals
and the current manifest are excluded from the final file inventory to permit
append-only recording. Earlier preparation evidence is historical and is not
rewritten to impersonate a current run.

These fixtures, tests, and logs remain agent-writable. A reviewer must independently
freeze and reproduce the candidate before any gate is approved. G0/G1 and all
later gates remain pending; no package work is authorized by this evidence page.
