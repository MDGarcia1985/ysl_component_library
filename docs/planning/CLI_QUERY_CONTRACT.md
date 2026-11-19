# P3 local query contract

**Status:** Frozen for P3 implementation. G3 review is still open.  
**Revision:** 1  
**Date:** 2026-11-19  
**Related decision:** DEV-2026-11-19-006  
**Governs:** AC-301 through AC-308

This document freezes invocation, filters, the JSON envelope, diagnostic codes,
and exit codes before query behavior is treated as accepted. It does not approve
packaging, an installed command, page generation, or publication.

An agent-writable copy of this file is not a human approval of the results.
Expected observations for the executable cases live in
`tests/test_query_contract.py` and the authored fixtures it reads. Those tests
are self-evaluated until a reviewer runs them outside this workspace.

## Invocation

Development invocation, and the only one this phase provides:

```text
PYTHONPATH=src python -m ysl_components --catalog CATALOG OPERATION [options]
```

- `CATALOG` is required and explicit. There is no default catalog and no search
  of the process working directory.
- The evaluator supplies `PYTHONPATH` so `src/` is imported. This phase does not
  build a wheel, sdist, editable install, or `ysl-components` console script.
- `CATALOG` is a directory. Every regular file named `definition.yml` under it
  is in scope, at any depth. Other files are not component documents.
- Symlinked `definition.yml` files are ignored.
- Queries do not use the network. Schema resources are the local `schemas/`
  directory next to `src/`. Unknown component schema versions are not read as
  the current version.
- Relative `CATALOG` and export paths resolve from the process working directory.
  Stored paths in the envelope are absolute and use `/` separators.
- `--help` and `-h` are usage errors. This phase has no text mode on stdout.

`YSL_COMPONENTS_FAULT=unexpected` is the only observation seam for exit 1. When
it is set to that exact value, the process writes the error envelope and exits 1
before it reads a catalog. Any other value is ignored. Unset, it does not change
query results. It is not a catalog operation.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success, including a search or list with no matches and validation of a valid catalog |
| 1 | Unexpected failure, including the fault seam |
| 2 | Invalid usage or invalid catalog data |
| 3 | The catalog path, component, variant, profile, pin, or interface was not found |
| 4 | A pin alias matches more than one pin. No pin is selected. |
| 5 | A component declares a schema version other than `1.0.0-draft.1` |

Precedence after arguments parse: 5 if any in-scope file declares an unsupported
schema version; otherwise 2 if the catalog has any other diagnostic or the index
is stale or invalid; otherwise the operation's 4, 3, or 0. Usage errors are 2
and are decided before a missing catalog becomes 3. Component ID and alias
collisions are invalid catalog data (exit 2), not a guessed match. A query does
not return component entries when the catalog is invalid or the schema version
is unsupported.

## Operations and filters

| Operation | Arguments | Filters |
| --- | --- | --- |
| `validate` | none | none |
| `list` | none | `--kind`, `--category`, `--manufacturer` |
| `search` | none | `--text`, `--kind`, `--category`, `--manufacturer`, `--capability`, `--interface-type`, `--fact-status` |
| `show` | selector | `--variant` or `--profile`, not both |
| `pin` | selector, pin selector | `--variant` or `--profile`, not both |
| `pins` | selector | `--connector`, `--capability`, `--variant` or `--profile` |
| `interface` | selector, interface id | `--variant` or `--profile`, not both |
| `export` | selector | `--format json\|yaml`, `--output PATH`, optional `--force` |

Selectors match a component `id` or alias with `casefold()`. Pin selectors match
a canonical pin key or an alias exactly, including case. A canonical key wins
over another pin's alias. `maps_to` is not a selector. Variant and profile
selectors are exact member names. Passing both `--variant` and `--profile` is
exit 2, code `SELECTION_CONFLICT`.

`--kind` is `board`, `ic_family`, or `module`. `--category` is one of the
component schema categories. `--fact-status` is `documented`, `derived`,
`legacy_uncited`, `unknown`, or `conflicting`. A value outside those sets is
exit 2, code `USAGE`. `--manufacturer` is an exact `casefold()` match against a
known manufacturer name. The filter `unknown` matches `manufacturer.status`
of `unknown`. `--text` is a non-empty `casefold()` substring of id, name, or
aliases. `--capability` is an exact capability token on a base-document pin.
`--interface-type` is an exact `type` on a base-document interface. Variant-only
pins and interfaces are not searched. `--fact-status` inspects every `facts`
map in the document, including variants and profiles.

Filters combine with AND. Omitted filters add no constraint. No matches is exit 0
and an empty `components` array. Component order is `id` ascending. Pin order is
the pin key ascending. Interface, connector, and constraint ids used as lists
are ascending. Diagnostic order is file, path, code, then message.

## JSON envelope

Stdout is one UTF-8 JSON document, indented by two spaces, with object keys
sorted, `ensure_ascii` disabled, and a trailing newline. No other bytes are
written to stdout. Diagnostics are JSON objects, one per line, on stderr.
Success writes no stderr.

```json
{
  "catalog": {"digest": "<sha256>", "path": "<absolute posix path>"},
  "envelope": {
    "contract": "ysl-components-query",
    "revision": "1",
    "schema_version": "1.0.0-draft.1"
  },
  "operation": "list",
  "result": {},
  "safety": {
    "bench_verification_inferred": false,
    "connection_asserted_safe": false
  },
  "selection": {
    "component": null,
    "profile": null,
    "resolved_by": null,
    "variant": null
  }
}
```

`safety` is constant. The tool never reports that a connection is safe and never
promotes verification to bench-tested or document-reviewed. `catalog` is null
when the catalog was not opened. `selection.resolved_by` is `id` or `alias`
when one component was selected.

Catalog digest, over in-scope definition files sorted by relative POSIX path:

```text
sha256(utf-8 of each relative_path + NUL + sha256(file bytes) + newline)
```

The digest does not include `catalog-index.json`.

### Result shapes

`validate`: `status` is `valid` or `invalid`; `index` is `absent`, `fresh`,
`stale`, or `invalid`; `files` lists every in-scope file with `path`, `id`,
`schema_version`, `sha256`, and `diagnostics`; `diagnostic_count` counts catalog
diagnostics. Invalid files stay in the list.

`list` and `search`: `status` `ok` and `components`. Each component has `id`,
`name`, `kind`, `category`, `manufacturer`, `aliases`, and `verification_status`.

`show`: identity, manufacturer, aliases, `schema_version`, provenance status,
verification status, sorted source and section ids, pin summaries (`pin`,
`maps_to`, `aliases`, `direction`, `capabilities`, `connector`, `position`),
the stored `constraints` and `resource_conflicts`, and `uncertainty`.
`selected_variant` or `selected_profile` is the requested member. `selected_facts`
is that member's own facts map, not a deep merge. Uncertainty facts are objects
inside any `facts` map whose status is `unknown`, `conflicting`, or
`legacy_uncited`. Conflicting and unknown facts set `selected_value` to null and
do not gain a chosen value. Conflicting connections are listed from
`routing_status`.

`pin`: the selected pin's stored fields needed to preserve mapping and
uncertainty (`maps_to`, aliases, direction, capabilities, location, facts,
provenance, `shared_with`), `verification_status`, and related constraint or
resource-conflict summaries. A related record is one whose stored strings
include the pin key or `pin:<key>`.

`pins`: pin summaries, optionally limited to a connector or capability.

`interface`: `type`, `signals`, `facts`, provenance status, and related records
whose strings include the interface id or `interface:<id>`. Signals stay pin
references. Lists of alternative pins do not mean simultaneous use.

Not found: `status` `not_found`, a `code`, and `query`. Ambiguous pin: `status`
`ambiguous`, code `AMBIGUOUS_PIN`, and sorted `candidates`. Invalid catalog:
`status` `invalid` and `diagnostic_count`, with no `components` array.
Invalid usage: `status` `invalid_usage` and code `USAGE` or `SELECTION_CONFLICT`.

Numbers, strings, and booleans keep the types produced by the strict loader.
Component aliases and pin aliases keep document order.

## Diagnostics

Stderr lines use compact JSON with sorted keys: `code`, `file`, `message`, `path`.
`path` is a JSON pointer inside the component, or empty when the diagnostic is
not at a field. `file` is the catalog-relative POSIX path, `catalog-index.json`,
or empty.

| Code | When |
| --- | --- |
| `USAGE` | Missing or unknown arguments, empty text, or an illegal filter value |
| `SELECTION_CONFLICT` | Both `--variant` and `--profile` |
| `CATALOG_NOT_FOUND` | Catalog path does not exist |
| `INVALID_CATALOG` | Catalog path is not a directory |
| `YAML_SYNTAX` | The file is not one JSON-compatible YAML document |
| `YAML_DUPLICATE_KEY` | A mapping repeats a key |
| `YAML_KEY_TYPE` | A mapping key is not a string |
| `YAML_CONSTRUCT_FORBIDDEN` | An anchor, alias, or explicit tag is present |
| `YAML_NON_JSON_VALUE` | A value is not JSON-compatible |
| `SCHEMA_UNSUPPORTED` | `schema_version` is a string other than `1.0.0-draft.1` |
| `SCHEMA_INVALID` | The current schema rejects the document |
| `ID_COLLISION` | Two schema-valid documents share an id |
| `ALIAS_COLLISION` | Component ids or aliases collide under `casefold()` |
| `REF_NOT_FOUND` | A typed reference does not resolve |
| `QUANTITY_ORDER` | `min` exceeds `max` |
| `QUANTITY_OUT_OF_RANGE` | A point value is outside min/max |
| `CONFLICT_NOT_DISTINCT` | Conflicting claims do not differ |
| `INHERITANCE_CYCLE` | Variant or profile inheritance cycles |
| `POWER_CYCLE` | Power-domain dependencies cycle |
| `POSITION_COLLISION` | Two pins share one connector position |
| `POSITION_OUT_OF_RANGE` | A numeric position is outside the connector |
| `SHARED_PIN_CYCLE` | `shared_with` cycles |
| `VERIFICATION_EVIDENCE_MISSING` | A passing status lacks the required record |
| `INDEX_STALE` | `catalog-index.json` does not match definition bytes |
| `INDEX_INVALID` | The index is not the required JSON object |
| `OUTPUT_EXISTS` | Export target exists and `--force` was not set |
| `OUTPUT_PROTECTED` | Export target resolves inside the catalog |
| `COMPONENT_NOT_FOUND` | Selector matches nothing |
| `VARIANT_NOT_FOUND` | Variant member is absent |
| `PROFILE_NOT_FOUND` | Profile member is absent |
| `PIN_NOT_FOUND` | Pin key and aliases miss |
| `INTERFACE_NOT_FOUND` | Interface id is absent |
| `AMBIGUOUS_PIN` | The pin alias matches multiple pins |
| `UNEXPECTED` | Unhandled failure or the fault seam |

Schema-valid documents receive the semantic checks. A document whose
`schema_version` is an unsupported string is not validated as the current schema.
A missing or non-string version remains a current-schema failure (`SCHEMA_INVALID`).

## Index freshness

`catalog-index.json` at the catalog root is optional. When absent, answers come
from the definition files and `index` is `absent`. When present, it must be:

```json
{
  "algorithm": "sha256-definition-bytes-v1",
  "definitions": [{"path": "relative/definition.yml", "sha256": "<hex>"}],
  "schema_version": "1.0.0-draft.1"
}
```

`definitions` is the complete set of in-scope relative paths and raw-byte
SHA-256 values. Any extra, missing, or different entry is `INDEX_STALE`.
Malformed JSON or a different shape or algorithm is `INDEX_INVALID`. This phase
rejects a stale or invalid index. It does not rebuild or rewrite one, and it
does not return the index as a query result.

## Export and read-only queries

`export` writes the stored component document, not the show projection and not a
variant overlay. JSON uses the same canonical encoding as stdout. YAML is a
safe dump with sorted keys. The parent directory must already exist. An existing
file is left unchanged unless `--force` is set. A path inside the catalog is
refused even with `--force`. Stdout is still the envelope; the component bytes
are the file. `validate`, `list`, `search`, `show`, `pin`, `pins`, and
`interface` do not create or modify catalog files.

## Explicitly not frozen here

- Windows execution. This checkout can run Linux only.
- The installed command name and package metadata. Those wait for G4 and P5.
- Generated browsing pages. Those wait for P4.
- The wording of JSON Schema library messages. Tests bind `SCHEMA_INVALID` and
  the pointer, not the library sentence.
- Rebuilding a derived index. Rejection is the frozen choice.
- Electrical safety, simultaneous pin use, and resolution of the six VENTUNO
  discrepancies. Query output preserves them and does not decide them.
