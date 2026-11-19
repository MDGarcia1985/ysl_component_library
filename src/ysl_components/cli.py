# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/cli.py
Purpose: Parse the frozen invocation and write the JSON envelope.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Stdout is only the JSON document. Diagnostics go to stderr.
Queries do not modify the catalog. Packaging is not invoked from here.
Related decision: DEV-2026-11-19-006.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from ysl_components import QUERY_CONTRACT, QUERY_REVISION, SUPPORTED_SCHEMA_VERSION
from ysl_components.loader import diagnostic, load_catalog
from ysl_components.query import (
    CATEGORIES,
    FACT_STATUSES,
    KINDS,
    QueryFailure,
    export_component,
    file_inventory,
    interface_result,
    invalid_result,
    list_components,
    pin_result,
    pins_result,
    query_diagnostic,
    selection_block,
    show_component,
)


class UsageError(Exception):
    """Purpose: Stop argument parsing without writing argparse's own text to stdout.
    Design: The message becomes a USAGE diagnostic. Workflow: Parser errors.
    Data Handoff: Message string.
    """


class Parser(argparse.ArgumentParser):
    """Purpose: Keep usage failures inside the JSON contract.
    Design: Raise UsageError instead of printing and exiting.
    Workflow: main. Data Handoff: Namespace or UsageError.
    """

    def error(self, message):
        """Purpose: Convert argparse errors. Design: No direct stdout write.
        Workflow: Unknown arguments. Data Handoff: UsageError.
        """
        raise UsageError(message)


def emit(payload, diagnostics, exit_code):
    """Purpose: Write the response contract. Design: Canonical JSON on stdout, one diagnostic per stderr line.
    Workflow: Every exit. Data Handoff: Process exit code.
    """
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    for item in diagnostics:
        sys.stderr.write(json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n')
    return exit_code


def envelope(operation, catalog, selection, result):
    """Purpose: Build the frozen document. Design: Safety flags stay false.
    Workflow: All handled exits. Data Handoff: Envelope mapping.
    """
    return {
        'catalog': None if catalog is None else {'digest': catalog.digest, 'path': catalog.root.as_posix()},
        'envelope': {
            'contract': QUERY_CONTRACT,
            'revision': QUERY_REVISION,
            'schema_version': SUPPORTED_SCHEMA_VERSION,
        },
        'operation': operation,
        'result': result,
        'safety': {'bench_verification_inferred': False, 'connection_asserted_safe': False},
        'selection': selection if selection is not None else selection_block(),
    }


def unexpected(message):
    """Purpose: Report exit 1. Design: One UNEXPECTED diagnostic and an error result.
    Workflow: Fault seam and unhandled exceptions. Data Handoff: Exit code 1.
    """
    result = {'code': 'UNEXPECTED', 'message': message, 'status': 'unexpected'}
    return emit(envelope(None, None, None, result), [diagnostic('UNEXPECTED', '', '', message)], 1)


def usage(message, code='USAGE'):
    """Purpose: Report bad arguments. Design: Exit 2 before catalog reads when parsing fails.
    Workflow: Usage and selection conflicts. Data Handoff: Exit code 2.
    """
    result = {'code': code, 'status': 'invalid_usage'}
    return emit(envelope(None, None, None, result), [diagnostic(code, '', '', message)], 2)


def check_choice(value, allowed, label):
    """Purpose: Reject a filter outside the frozen set. Design: Empty means the filter is omitted.
    Workflow: Argument validation. Data Handoff: The value or UsageError.
    """
    if value is not None and value not in allowed:
        raise UsageError(f'{label} must be one of {", ".join(sorted(allowed))}')
    return value


def build_parser():
    """Purpose: Describe the frozen operations. Design: Help flags are handled before parse.
    Workflow: main. Data Handoff: Parser.
    """
    parser = Parser(prog='python -m ysl_components', add_help=False)
    parser.add_argument('--catalog')
    commands = parser.add_subparsers(dest='operation')
    commands.add_parser('validate', add_help=False)
    for name in ('list', 'search'):
        command = commands.add_parser(name, add_help=False)
        command.add_argument('--kind')
        command.add_argument('--category')
        command.add_argument('--manufacturer')
        if name == 'search':
            command.add_argument('--text')
            command.add_argument('--capability')
            command.add_argument('--interface-type')
            command.add_argument('--fact-status')
    for name in ('show', 'pin', 'pins', 'interface', 'export'):
        command = commands.add_parser(name, add_help=False)
        command.add_argument('selector')
        if name == 'pin':
            command.add_argument('pin')
        if name == 'interface':
            command.add_argument('interface_id')
        if name in ('show', 'pin', 'pins', 'interface'):
            command.add_argument('--variant')
            command.add_argument('--profile')
        if name == 'pins':
            command.add_argument('--connector')
            command.add_argument('--capability')
        if name == 'export':
            command.add_argument('--format', required=True, choices=('json', 'yaml'))
            command.add_argument('--output', required=True)
            command.add_argument('--force', action='store_true')
    return parser


def open_catalog(path):
    """Purpose: Resolve the explicit catalog. Design: Missing and non-directory paths use frozen codes.
    Workflow: After usage checks. Data Handoff: Catalog, or an emitted exit via QueryFailure-like tuple.
    """
    catalog_path = Path(path)
    if not catalog_path.exists():
        result = {'code': 'CATALOG_NOT_FOUND', 'query': path, 'status': 'not_found'}
        code = emit(envelope(None, None, None, result), [diagnostic('CATALOG_NOT_FOUND', '', '', path)], 3)
        return None, code
    if not catalog_path.is_dir():
        result = {'code': 'INVALID_CATALOG', 'status': 'invalid'}
        code = emit(envelope(None, None, None, result), [diagnostic('INVALID_CATALOG', '', '', path)], 2)
        return None, code
    return load_catalog(catalog_path), None


def run(argv):
    """Purpose: Execute one operation. Design: Invalid catalogs do not return component entries.
    Workflow: main after the fault seam. Data Handoff: Exit code.
    """
    if any(argument in ('-h', '--help') for argument in argv):
        return usage('usage: python -m ysl_components --catalog CATALOG {validate,list,search,show,pin,pins,interface,export}')
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.operation:
        return usage('operation is required')
    if not args.catalog:
        return usage('catalog path is required')
    if getattr(args, 'variant', None) and getattr(args, 'profile', None):
        return usage('pass only one of --variant or --profile', 'SELECTION_CONFLICT')
    if args.operation == 'search' and args.text is not None and args.text == '':
        return usage('--text must be non-empty')
    if args.operation in ('list', 'search'):
        check_choice(args.kind, KINDS, '--kind')
        check_choice(args.category, CATEGORIES, '--category')
    if args.operation == 'search':
        check_choice(args.fact_status, FACT_STATUSES, '--fact-status')
    catalog, early = open_catalog(args.catalog)
    if early is not None:
        return early
    if args.operation == 'validate':
        return emit(envelope('validate', catalog, None, file_inventory(catalog)), catalog.diagnostics, catalog.exit_code())
    if catalog.exit_code() != 0:
        return emit(envelope(args.operation, catalog, None, invalid_result(catalog)), catalog.diagnostics, catalog.exit_code())
    try:
        if args.operation in ('list', 'search'):
            result = list_components(
                catalog,
                kind=args.kind,
                category=args.category,
                manufacturer=args.manufacturer,
                text=getattr(args, 'text', None),
                capability=getattr(args, 'capability', None),
                interface_type=getattr(args, 'interface_type', None),
                fact_status=getattr(args, 'fact_status', None),
            )
            return emit(envelope(args.operation, catalog, None, result), [], 0)
        variant = getattr(args, 'variant', None)
        profile = getattr(args, 'profile', None)
        if args.operation == 'show':
            result, selection = show_component(catalog, args.selector, variant, profile)
        elif args.operation == 'pin':
            result, selection = pin_result(catalog, args.selector, args.pin, variant, profile)
        elif args.operation == 'pins':
            result, selection = pins_result(catalog, args.selector, args.connector, args.capability, variant, profile)
        elif args.operation == 'interface':
            result, selection = interface_result(catalog, args.selector, args.interface_id, variant, profile)
        else:
            result, selection = export_component(catalog, args.selector, args.format, args.output, args.force)
        return emit(envelope(args.operation, catalog, selection, result), [], 0)
    except QueryFailure as failure:
        file_name = ''
        return emit(envelope(args.operation, catalog, None, failure.result), [query_diagnostic(failure, file_name)], failure.exit_code)


def main(argv=None):
    """Purpose: Provide the process entry. Design: The fault seam runs before any catalog read.
    Workflow: python -m ysl_components. Data Handoff: Exit code.
    """
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    sys.stderr.reconfigure(encoding='utf-8', newline='\n')
    if os.environ.get('YSL_COMPONENTS_FAULT') == 'unexpected':
        return unexpected('forced unexpected failure')
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        return run(arguments)
    except UsageError as error:
        return usage(str(error))
    except Exception as error:
        return unexpected(f'{type(error).__name__}: {error}')
