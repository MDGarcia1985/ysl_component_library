# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/__init__.py
Purpose: Identify the development catalog package and the frozen query revision.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Importing this package does not publish it. The installed command is a separate entry point.
Related decision: DEV-2026-11-19-006, DEV-2026-11-19-012.
"""

QUERY_CONTRACT = 'ysl-components-query'
QUERY_REVISION = '1'
SUPPORTED_SCHEMA_VERSION = '1.0.0-draft.1'
