# Repository preparation evidence

This evidence covers the separately authorized folder reorganization, VENTUNO Q
source enrichment, and generated reference pages. It is **local self-evaluation**,
not the protected runner, approved oracle, or human acceptance required by the
[CLI plan](../../planning/CLI_IMPLEMENTATION_PLAN.md). All G0-G5 gates remain pending.

## Before changes

[baseline.json](baseline.json) records the 12 original-to-current file paths,
pre-edit SHA-256 digests, all five parsed definitions, and the byte lengths/hashes
of the pre-existing journal prefixes. The manual, four other definitions, and
engineering standards must retain their exact bytes. VENTUNO enrichment preserves
every previous semantic field except its intentionally relocated source path.

The preparation tests were written before moves/enrichment. Their initial run
collected eight cases, with one passing history check and seven non-successes
(one failure, six errors) because the required layout, generator, scaffolds, and
enrichment did not yet exist. Preserve this expected red baseline:

- [Initial stdout](before.stdout.txt)
- [Initial stderr](before.stderr.txt)
- [Initial exit code](before.exit-code.txt)

## Current verification

Run from the repository root with Python 3.11+ and PyYAML:

```shell
python src/ysl_components/reference_pages.py
python -m unittest discover -s tests -v
python tests/collect_preparation_evidence.py
```

The checks compare the definitions with the captured original field tree, resolve
typed connection and provenance references, check manual-specific conflict/power
facts, verify historical journal prefixes, reproduce generated pages in memory,
and confirm that packaging scaffolds are inactive.

The prepared VENTUNO definition has 288 existing named pin records, 15 inventory
entries, 76 connection relationships, four resource-conflict groups, and 37
manual-section references. It retains all six conflicting source claims. The
MIPI-DSI interface is now explicit, bringing the interface count from 25 to 26.

The final run's stdout, stderr, exit status, source/output digests, local-link
checks, and deliberate-corruption observations are recorded beside this page.
The manifest excludes itself and the append-only root journals; journal-prefix
integrity is independently checked against the baseline. It is a local digest
inventory, not a signature or an independently approved release identity.

- [Final stdout](after.stdout.txt)
- [Final stderr and case results](after.stderr.txt)
- [Final exit code](after.exit-code.txt)
- [Navigation, corruption, and renderer observations](checks.json)
- [File digest manifest](manifest.json)

The five corruption demonstrations use in-memory input substitution or direct
comparison against the original field tree. They demonstrate these local checks
reject the specified faults; they are not the held-out black-box evaluator of the
future CLI plan. Markup escaping and duplicate YAML keys are also exercised.

## Limitations

- These tests and their baseline are in the agent-writable workspace; a reviewer
  must reproduce and retain trusted copies to establish independent acceptance.
- Static source comparisons and renderer tests do not establish electrical
  correctness, current manufacturer specifications, or bench operation.
- The copied manual retains its original unavailable local images and site-relative
  links. Authored/generated page navigation is checked separately from those
  disclosed inherited limitations.
- Common-schema/ID migration, local query CLI, package builds/installations,
  protected acceptance infrastructure, and human gate reviews have not occurred.
- `component.schema.json` is a deliberately rejecting placeholder; no hardware
  definition is claimed to validate against it.
