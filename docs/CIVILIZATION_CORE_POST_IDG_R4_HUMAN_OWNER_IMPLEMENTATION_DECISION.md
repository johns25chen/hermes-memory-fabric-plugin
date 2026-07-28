# Civilization Core POST-IDG R4 Human Owner Implementation Decision

## 1. Task identity

This document is the sole repository artifact for the POST-IDG R4 Human
Owner implementation decision at the required baseline. It is recorded on
branch `docs/post-idg-r4-human-owner-implementation-decision` for package
version `6.16.0`.

This task records a decision only. It does not implement code, create bounded
implementation authority, start R5 or R6 automatically, or authorize
deployment, release, version, or tag activity.

## 2. Controlling R4 recommendation

The repository-effective R4 reassessment is complete with a READY
recommendation. It records zero blocking HOLDs, seventeen HOLDs that can be
isolated by explicit R5 scope boundaries, five HOLDs that can be deferred
beyond a bounded learning slice, and all eight readiness dimensions as
`READY-WITH-BOUNDS`.

The controlling recommendation supports consideration of a coherent,
non-production implementation-to-learn slice. It does not establish product
validation, production readiness, implementation authority, or an
implementation start.

## 3. Human Owner instruction provenance

The Human Owner explicitly instructed:

> “不准将问题抛给我，你要用专业的知识筛选择优。”

This instruction delegates selection of the optimal R4 decision from the
established repository-effective evidence. It removes the need for another
A/B/C confirmation, but it does not delegate or internalize the Human Owner's
authority inside any future implementation.

## 4. Professional option selection

The selected option is `DECISION_OPTION=A`, named
`AUTHORIZE_BOUNDED_IMPLEMENTATION`.

The decision means: proceed to the separate R5 Bounded Implementation
Authorization task. It is a decision to enter that authorization gate, not
the authorization that the gate must separately define and issue.

## 5. Decision rationale

The selected option is supported because:

1. the independent R4 recommendation is READY;
2. no R4 HOLD blocks every reasonable bounded R5 learning slice;
3. all eight readiness dimensions are ready with explicit bounds;
4. seventeen unresolved HOLDs can be isolated by a future exact R5 scope;
5. five unresolved HOLDs are material only beyond a bounded learning slice;
6. a coherent, non-production implementation-to-learn slice exists;
7. deferral would not resolve an identified blocker because no item is
   classified as `BLOCKS-BOUNDED-R5`; and
8. rejection is unsupported because no readiness dimension is negative and
   the direction retains bounded product and technical justification.

This decision does not resolve any HOLD. It selects the professionally
supported next governance gate while preserving every unresolved limitation.

## 6. Decision versus implementation-authority distinction

The Human Owner decision authorizes proceeding to R5 Bounded Implementation
Authorization consideration only. It does not permit implementation to begin
immediately, grant bounded or general implementation authority, make R5
repository-effective, start R6, permit PR #357 to merge, or authorize a
production runtime, deployment, release, version change, or tag.

R5 must independently define the exact implementation scope, allowed files,
components, success criteria, validation requirements, forbidden behavior,
and authority limits. Until that authorization is repository-effective,
implementation authority remains absent and implementation start remains
unauthorized.

## 7. Preserved R5 candidate envelope

R5 must begin from the R4 candidate envelope and preserve these constraints:

- non-production only;
- local single-operator only;
- fixed/synthetic or non-sensitive inputs;
- no public or external service exposure;
- no production credentials;
- no enterprise multi-tenancy;
- no autonomous memory adoption;
- no self-authorization;
- no durable adoption unless explicitly and separately proven necessary and
  authorized inside the bounded R5 scope;
- no production persistent store;
- no production database migration;
- no production deployment;
- no release;
- no tag;
- no external API, MCP, Connector, adapter, or dependency unless specifically
  justified and separately authorized;
- unsupported or invalid states fail closed;
- Human Owner authority remains external to implementation; and
- outputs remain bounded, auditable, and removable.

This envelope remains a candidate constraint set. It is neither an
implementation design nor implementation authority.

## 8. PR #357 boundary

PR #357 remains closed, unmerged, and preserved. Its artifact gains no
authority from this decision and may not be merged or adopted on this basis.

It may be reconsidered only after repository-effective R5 authorization
explicitly determines whether any part of it falls inside the authorized
scope.

## 9. R5 entry condition

The next permitted task is the separate POST-IDG R5 Bounded Implementation
Authorization. Entry into that task creates no automatic successor work.

R5 may establish implementation authority only through a new,
repository-effective authorization that explicitly fixes scope, files,
components, success criteria, validation, forbidden behavior, and authority
limits while preserving or further narrowing the candidate envelope above.
Unless and until that condition is satisfied, neither implementation nor R6
may start.

## 10. Final machine state

```text
TASK_ID=POST_IDG_R4_HUMAN_OWNER_IMPLEMENTATION_DECISION
BASE_COMMIT=1834986a9e467f6c36b5a60b262dfd3234f82d5c
ALLOWED_WRITE_FILE_COUNT=1

R3_STATUS=COMPLETE-WITH-HOLD

R4_READINESS_RECOMMENDATION=READY
R4_BLOCKING_HOLD_COUNT=0
R4_BOUNDABLE_HOLD_COUNT=17
R4_DEFERABLE_HOLD_COUNT=5

HUMAN_OWNER_SELECTION_MODE=DELEGATED-PROFESSIONAL-SELECTION
HUMAN_OWNER_R4_DECISION=AUTHORIZE_BOUNDED_IMPLEMENTATION
R4_DECISION_STATUS=COMPLETE

R4_STATUS=COMPLETE-WITH-AUTHORIZE-BOUNDED-IMPLEMENTATION-DECISION

R5_ELIGIBILITY=ESTABLISHED
R5_CANDIDATE_SCOPE_ENVELOPE=DEFINED-NOT-AUTHORIZED
R5_STATUS=NOT_STARTED
R6_STATUS=NOT_STARTED

IMPLEMENTATION_READINESS=READY-FOR-BOUNDED-R5-AUTHORIZATION-CONSIDERATION
IMPLEMENTATION_AUTHORITY=NONE
IMPLEMENTATION_START=NOT_AUTHORIZED

R6_0_ARTIFACT_STATUS=PRESERVED_UNMERGED
R6_0_IMPLEMENTATION_AUTHORITY=NONE

DEPLOYMENT_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R5_BOUNDED_IMPLEMENTATION_AUTHORIZATION
```

The decision is complete. It creates eligibility for the separate R5
authorization gate and creates no implementation, deployment, release,
version, tag, or automatic successor authority.
