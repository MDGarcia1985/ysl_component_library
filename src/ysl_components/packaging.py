# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/packaging.py
Purpose: Refuse package builds until a later human G4 decision.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: This module has no success path. It must not call a builder or write a distribution.
Related decision: DEV-2026-11-19-009.
"""


def denial_reason(approval, candidate_digest):
    """Purpose: Classify why a package request stays closed. Design: A local approved flag is never authorization.
    External G4 wording still does not open packaging in this phase. See the page contract.
    Workflow: request_package_build. Data Handoff: One reason code.
    """
    if not isinstance(approval, dict):
        return 'approval_absent'
    if approval.get('channel') != 'external':
        return 'local_approval_is_not_authorization'
    if approval.get('gate') != 'G4':
        return 'wrong_gate'
    if approval.get('candidate') != candidate_digest:
        return 'candidate_mismatch'
    return 'packaging_closed_until_external_g4'


def request_package_build(approval, candidate_digest, builder=None):
    """Purpose: Accept a packaging request and deny it. Design: The builder argument is ignored on purpose.
    A caller cannot pass a builder and have this phase invoke it. Workflow: AC-501.
    Data Handoff: A denial record. No files are written.
    """
    del builder
    return {
        'authorized': False,
        'built': False,
        'reason': denial_reason(approval, candidate_digest),
        'candidate_digest': candidate_digest,
        'distribution_written': False,
    }
