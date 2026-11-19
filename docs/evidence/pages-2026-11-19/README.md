# P4 page and evidence bundle

**State:** Local self-evaluation for a later G4 review. This index is not G4 approval.  
**Date:** 2026-11-19  
**Contract:** [Page contract revision 1](../../planning/CLI_PAGE_CONTRACT.md)  
**Prior gate:** [G3 query approval](../../reviews/g3-approval-2026-11-19.md)

The user approved G3 with the chat statement "G3 is approved." That approval is
the query draft merged in pull request 2. It does not authorize packaging.
This folder is the P4 candidate's local evidence. No independent reviewer ran
it. Windows was not available.

## What was generated

`python src/ysl_components/reference_pages.py` writes `docs/catalog.md` and the
five component README pages from `hardware/**/definition.yml`. Those pages are
generated. The VENTUNO `sources/README.md` file is authored guidance, and it
records the missing manual images as source limitations.

Regenerate from the repository root with the command above. Do not edit the
generated pages by hand.

## How to read this folder

| File | What it holds |
| --- | --- |
| [after.stdout.txt](after.stdout.txt) | Unedited unittest stdout |
| [after.stderr.txt](after.stderr.txt) | Unedited unittest stderr |
| [after.exit-code.txt](after.exit-code.txt) | Unittest process exit code |
| [checks.json](checks.json) | Collector summary: platform, results, limitations |
| [fact-report.json](fact-report.json) | Literal fact-oracle result |
| [link-report.json](link-report.json) | Generated-page links and full Markdown navigation |
| [determinism.json](determinism.json) | Two repository generations and two clean-directory generations |
| [packaging-denial.json](packaging-denial.json) | AC-501 reasons. No distribution was built. |
| [source-limitations.json](source-limitations.json) | Manual images that are not in the repository |
| [tamper-demo.json](tamper-demo.json) | A temporary manifest copy with one file removed and one file changed |
| [manifest.json](manifest.json) | SHA-256 inventory. It is not a signature. |
| [views/catalog.md](views/catalog.md) | Catalog excerpt and [PNG](views/catalog.png) |
| [views/ventuno-d5-pins.md](views/ventuno-d5-pins.md) | VENTUNO D5 pin excerpt and [PNG](views/ventuno-d5-pins.png) |
| [views/ventuno-conflicts.md](views/ventuno-conflicts.md) | VENTUNO conflict excerpt and [PNG](views/ventuno-conflicts.png) |
| [views/attiny-family.md](views/attiny-family.md) | ATtiny family excerpt and [PNG](views/attiny-family.png) |

`manifest.json` lists repository files except itself, `DEVNOTES.md`,
`TEST_LOG.md`, `.git/`, and `__pycache__/`. Re-hash a listed file to see
whether it still matches. The journals are excluded so later verification
entries do not pretend to change the candidate that was hashed.

Reproduce the local run from the repository root:

```shell
python -B tests/collect_page_evidence.py
```

A second local run can match these semantic results. That match is still
self-evaluation. A reviewer outside this workspace has not reproduced it.

## Limitations that remain

- Windows page generation and Windows AC-307 were not executed.
- No independent evaluator, held-out fixture set, or external manifest was supplied.
- The six VENTUNO source discrepancies stay unresolved.
- Physical verification stays `not_verified`.
- Manual `assets/` images are missing. They are source limitations, not generated assets.
- Packaging stays closed. `pyproject.toml` has no build backend. No wheel or sdist was produced.
- G4 has not been decided. This folder cannot authorize packaging.
