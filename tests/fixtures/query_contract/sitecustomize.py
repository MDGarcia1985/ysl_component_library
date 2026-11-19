# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/fixtures/query_contract/sitecustomize.py
Purpose: Fail closed if a query process opens a network socket.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Imported only when a subprocess adds this directory to PYTHONPATH.
Related decision: DEV-2026-11-19-006.
"""

import socket


def _blocked(*_args, **_kwargs):
    """Purpose: Stop a connection. Design: Raise before any bytes leave the process.
    Workflow: AC-307 subprocess. Data Handoff: OSError.
    """
    raise OSError('AC-307 network access is disabled')


socket.socket.connect = _blocked
socket.create_connection = _blocked
