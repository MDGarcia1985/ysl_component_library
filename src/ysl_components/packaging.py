# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: src/ysl_components/packaging.py
Purpose: Admit a package build only for the human-approved G4 candidate.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: A local approved flag is not authorization. This module does not upload.
Related decision: DEV-2026-11-19-012.
"""

# The widened G4 statement binds the catalog package to this commit.
APPROVED_CANDIDATE = 'bbf013354b3ac7d4fdc9be8b44090634b431b118'


def denial_reason(approval, candidate_digest):
    """Purpose: Classify a closed packaging request. Design: External G4 wording is not enough
    unless the digest is the approved commit. A repository flag never opens the gate.
    Workflow: request_package_build. Data Handoff: A reason code, or None when the request matches.
    """
    if not isinstance(approval, dict):
        return 'approval_absent'
    if approval.get('channel') != 'external':
        return 'local_approval_is_not_authorization'
    if approval.get('gate') != 'G4':
        return 'wrong_gate'
    if approval.get('candidate') != candidate_digest:
        return 'candidate_mismatch'
    if candidate_digest != APPROVED_CANDIDATE:
        return 'candidate_not_approved'
    return None


def request_package_build(approval, candidate_digest, builder=None):
    """Purpose: Deny every request except the approved candidate, then optionally call a builder.
    Design: The builder is ignored unless the digest is the human-approved commit.
    The function does not choose an upload target and does not read a local approval file.
    Workflow: AC-501 for denials, and the P5 success boundary for the approved digest.
    Data Handoff: A result record. distribution_written is true only after the builder returns.
    """
    reason = denial_reason(approval, candidate_digest)
    if reason is not None:
        return {
            'authorized': False,
            'built': False,
            'reason': reason,
            'candidate_digest': candidate_digest,
            'distribution_written': False,
        }
    if builder is not None:
        builder(candidate_digest)
    return {
        'authorized': True,
        'built': builder is not None,
        'reason': 'approved',
        'candidate_digest': candidate_digest,
        'distribution_written': builder is not None,
    }
