# CLI Gate Review Record Template

**Template only — no approval is granted by this document.**

Use one new record per gate review or follow-up. Preserve rejected and superseded
records. The authoritative human decision must exist outside the candidate agent's
write access; a repository copy is a cross-reference, not independent proof.

See the [implementation plan](CLI_IMPLEMENTATION_PLAN.md) and
[acceptance contracts](CLI_ACCEPTANCE_TESTS.md).

## Review identity

- Gate and phase: Pending
- Review record ID: Pending
- Date, time, and time zone: Pending
- Reviewer identity and role: Pending
- Decision: PENDING / APPROVED / CHANGES_REQUIRED / REJECTED
- Approval scope: Pending
- Trusted human approval reference, when required: Pending
- Prior or superseded review: None

## Candidate and evaluator identity

- Candidate commit and dirty/untracked status, when Git is available: Pending
- Complete candidate file-manifest digest: Pending
- Approved baseline/source manifest digest: Pending
- Contract revision and digest: Pending
- Evaluator and expected-result fixture digests: Pending
- Held-out fixture identities and reproducibility reference: Pending
- Evidence bundle manifest digest: Pending
- Trusted external manifest/evaluator location: Pending
- Compared candidate versus prior approved candidate: Pending

## Required evidence review

- Applicable AC IDs and execution TEST IDs: Pending
- Required / collected / executed case counts: Pending
- Passing / failing / skipped / not-executed case counts: Pending
- Independent reproduction report and executor: Pending
- Raw subprocess logs and exit-status report: Pending
- Independent migration conservation and source-oracle comparisons: Pending
- Deliberate corruption cases and observed detections/survivors: Pending
- Generated pages, navigation checks, and visual evidence: Pending
- Platform/environment coverage: Pending
- Known source contradictions and incomplete hardware verification: Pending
- Test/fixture/expectation changes since freeze and their approvals: Pending
- Exceptions and supporting human-reviewed DEV IDs: None

## Reviewer observations

- Facts personally traced to source sections: Pending
- Commands personally reproduced and observed outcomes: Pending
- Pages/connector/variant views personally inspected: Pending
- Missing evidence or disputed outcomes: Pending
- Required corrections and acceptance conditions: Pending

## Decision and authorized next action

State the concrete gate decision and bind it to the digests above. Specify the
next permitted phase and any conditions; do not use a general "looks good" as
substitute authorization.

For G4, the human must explicitly authorize packaging of the reviewed pre-package
candidate. For G5, distinguish acceptance of package artifacts from authorization
to upload or publish them. Any data/schema/query change after G4 requires renewed
review under the implementation plan.

**Current authorized next action:** Pending human/reviewer decision; this unfilled
template grants no implementation, packaging, or release approval.
