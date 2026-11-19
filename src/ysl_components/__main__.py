# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/__main__.py
Purpose: Start the development catalog tool with python -m ysl_components.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: This path requires --catalog. The console script is ysl_components.cli.installed_main.
Related decision: DEV-2026-11-19-006, DEV-2026-11-19-012.
"""

import sys

from ysl_components.cli import main


if __name__ == '__main__':
    sys.exit(main())
