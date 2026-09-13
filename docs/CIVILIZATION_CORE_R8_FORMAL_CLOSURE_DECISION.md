# Civilization Core R8 SEC-GOV Formal Closure Decision

## 1. Decision identity

```text
DECISION_ID=CIVILIZATION_CORE_R8_SEC_GOV_FORMAL_CLOSURE_DECISION
DECISION_CLASSIFICATION=R8-FORMAL-CLOSURE-GOVERNANCE-DECISION
HUMAN_OWNER_AUTHORIZATION=AUTHORIZE-R8-FORMAL-CLOSURE-REVIEW-AND-CONDITIONAL-REPOSITORY-EFFECTIVENESS
HUMAN_OWNER_R8_DECISION=PASS
HUMAN_OWNER_SIGNATURE=NOT-CLAIMED
R8_STATE_TRANSITION=OPEN-TO-CLOSED-WHEN-THIS-DECISION-IS-MERGED-AND-POST-MERGE-VERIFIED
R8_FORMAL_CLOSURE_REPOSITORY_EFFECTIVE=PENDING-MERGE-AND-POST-MERGE-VERIFICATION
R9_ENTRY_DECISION_ELIGIBLE=ONLY-AFTER-REPOSITORY-EFFECTIVE-R8-PASS
R9_ENTRY_AUTHORIZED=FALSE
R9_IMPLEMENTATION_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
```

This document records the Human Owner's explicit R8 `PASS` decision. It does
not invent a signature or backdate an approval. The decision is limited to the
three implemented R8 Slices: security admission and minimized output, governed
local persistence, and local-process Provider/Federation candidate admission.
It is not a product-wide security certification, release approval, deployment
approval, or real-pilot approval.

## 2. Repository-effective Slice identities

1. Slice 1 — security intake and minimized output:
   `bb2b0325d44407aac7b1b58f65dc51cef4a1913d` (PR #387), Security Envelope
   contract `1.3`.
2. Slice 2 — local persistence authority and integrity:
   `5509dc74dbbba7d2aefe5f9b0f0c73ececad8b57` (PR #388), Local Persistence
   contract `2.2.0`.
3. Slice 3 — Provider/Federation admission boundary:
   `b6e5b3509d34f1d0413570c220336307619fd312` (PR #389), Provider/Federation
   contract `1.0.0`.

The three commits are a verified linear chain. The accepted Slice 3 feature
commit is `ccb0b198eb5fa7bc87313cf02deac3e832d98a46`; its tree and the merged R8
implementation tree are both
`758ce632596b3b7f9330033adf164f3918112ba6`. Package version remains `6.16.0`.

## 3. Decision basis and independent review

The Human Owner accepts the integrated assessment recommendation and the
disclosed limits in this document. The formal-closure reviewer was not the
author of the assessment or closure draft and completed the review before any
repository write.

The review authenticated the integrated-assessment manifest itself as
`a99bdb3880672f02ee06eb5a375678575fef5268453e13b739a214190c950f5a`, then
verified every file listed by that manifest in its assessment directory. It
checked the master-roadmap stage and authority rules, the three Slice commits
and contracts, the current implementation tree, the authenticated Slice 3
acceptance evidence, the post-merge record, the closure wording, and successor
non-authority boundaries. No blocking finding remained.

The authenticated Slice 3 acceptance manifest is
`8aa83abb34c1ae979ee2f889ec418fbe0d90a6cf3f4ba38215bf6d627c335bb1`.
It records independent review `PASS`, `R8-S3-IR-001=RESOLVED`, FV6
`26845 collected / 26845 passed`, zero failures, errors, skips, xfails,
xpasses, or deselections, and implementation acceptance `PASS`. The PR #389
post-merge evidence records `163 passed in 3.47s`, exit code 0, and confirms
that the merged tree equals the accepted implementation tree.

Historical authorization, historical independent review, current-tree tests,
and this formal-closure review remain distinct evidence classes. Commit
presence and current tests are not represented as historical authorization or
as separately frozen historical review evidence.

## 4. Closed R8 capability scope

Within the stated local trust model, R8 closes the following bounded scope:

- strict security-envelope validation, explicit human-decision mapping,
  sensitive or unknown input blocking, review quarantine, and minimized output;
- explicit, scoped, time-bound, payload-bound local persistence decisions,
  replay and sequence checks, resource limits, confined atomic filesystem
  updates, snapshot validation, and linked mutation receipts;
- authoritative local candidate identity, exact scope, explicit
  `READ_CANDIDATE`, payload-digest and compound-identity admission, with only
  `ALLOW` candidates entering downstream retrieval and context paths; and
- separation of candidate retrieval admission from persistence authority.

## 5. Accepted limitations and residual risks

The Human Owner explicitly accepts these limitations for this bounded R8
decision:

1. Slice 1 caller attestation is not cryptographic identity authentication.
2. Slice 2 integrity controls do not resist a trusted local operator able to
   rewrite all mutually consistent state.
3. Slice 3 does not provide network federation, connectors, cross-project
   sharing, or historical cross-batch replay protection.
4. Automated CI and branch protection are currently absent and remain a future
   maintenance risk, not a completed R8 capability.
5. This assessment did not obtain separately frozen Slice 1 or Slice 2
   historical review bundles. R8 entry authorization derives from the
   Human Owner authorization chain outside the repository.

Item 5 is an evidence-provenance limitation, not a waiver of a contract gate.
No missing mandatory gate was excused by this decision. The review found no
unresolved mandatory control within the approved R8 scope.

## 6. Repository-effectiveness condition

The R7 closure process is deliberately adopted here as a governance procedure;
this document does not claim that every R7 procedural step was an original R8
contract requirement.

This decision becomes repository-effective only after the exact reviewed
document is committed, published in a pull request against the expected
`main`, merged without bypassing applicable review or repository rules, and
then verified on the synchronized `main`. The document intentionally does not
predeclare its own future merge commit. The final merge identity belongs in the
external post-merge evidence report.

Until that chain succeeds,
`R8_FORMAL_CLOSURE_REPOSITORY_EFFECTIVE` is not `TRUE` and R8 is not formally
closed in repository state.

## 7. Successor and authority boundary

After repository effectiveness, R8 `PASS` makes R9 eligible only for a separate
entry decision. It grants no R9 entry or implementation authority, starts no
R9 work, and does not authorize Checkpoint B, a pilot, deployment, release,
version change, tag, or any R9-R13 execution.

```text
R9_ENTRY_DECISION_ELIGIBLE=ONLY-AFTER-REPOSITORY-EFFECTIVE-R8-PASS
R9_ENTRY_AUTHORIZED=FALSE
R9_IMPLEMENTATION_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
```
