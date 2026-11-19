"""File: tests/migration_checks.py
Purpose: Independently compare frozen source leaves with migrated destinations.
Author: Codex; contact: Pending confirmation; license: Pending confirmation.
Constraints: Does not import migration code or manufacture expected hardware values.
Related decision: DEV-2026-11-19-005.
"""
import json


def pointer(parts):
    """Purpose: Identify exact fields. Design: JSON Pointer encoding. Workflow: Comparison. Data Handoff: String path."""
    return '/' + '/'.join(str(part).replace('~', '~0').replace('/', '~1') for part in parts)


def leaves(node, path=()):
    """Purpose: Inventory source data. Design: Include empty containers. Workflow: Conservation checks. Data Handoff: Pointer/value map."""
    if isinstance(node, dict) and node:
        result = {}
        for key, value in node.items():
            result.update(leaves(value, path + (key,)))
        return result
    if isinstance(node, list) and node:
        result = {}
        for index, value in enumerate(node):
            result.update(leaves(value, path + (index,)))
        return result
    return {pointer(path): node}


def lookup(node, path):
    """Purpose: Resolve declared destinations. Design: Strict pointer traversal. Workflow: Comparison. Data Handoff: Value or error."""
    for raw in path.lstrip('/').split('/'):
        key = raw.replace('~1', '/').replace('~0', '~')
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def conservation_errors(before, after, mapping):
    """Purpose: Detect loss or changed values. Design: Original snapshots are oracle. Workflow: Tests/evidence. Data Handoff: Error list."""
    errors = []
    original = leaves(before)
    if set(original) != set(mapping['fields']):
        errors.append({'kind': 'SOURCE_COVERAGE', 'missing': sorted(set(original) - set(mapping['fields'])), 'extra': sorted(set(mapping['fields']) - set(original))})
    for path, expected in original.items():
        destinations = mapping['fields'].get(path, [])
        if not destinations:
            errors.append({'kind': 'UNMAPPED', 'source': path})
        for target in destinations:
            try:
                actual = lookup(after, target)
            except (KeyError, IndexError, TypeError, ValueError):
                errors.append({'kind': 'MISSING_TARGET', 'source': path, 'target': target})
                continue
            if type(actual) is not type(expected) or actual != expected:
                errors.append({'kind': 'VALUE_CHANGED', 'source': path, 'target': target, 'expected': expected, 'actual': actual})
    mapped = {target for targets in mapping['fields'].values() for target in targets}
    current = set(leaves(after))
    generated = set(mapping['generated_fields'])
    for path, record in mapping['generated_fields'].items():
        try:
            actual = lookup(after, path)
        except (KeyError, IndexError, TypeError, ValueError):
            errors.append({'kind': 'MISSING_GENERATED_TARGET', 'target': path})
            continue
        if type(actual) is not type(record['value']) or actual != record['value']:
            errors.append({'kind': 'GENERATED_VALUE_CHANGED', 'target': path})
    if current != mapped | generated or mapped & generated:
        errors.append({'kind': 'DESTINATION_COVERAGE', 'unexplained': sorted(current - mapped - generated), 'stale': sorted((mapped | generated) - current)})
    return errors
