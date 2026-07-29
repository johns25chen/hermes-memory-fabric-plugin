# Civilization Core POST-IDG R6.0 Implementation Learning Assessment

## 1. Purpose and authority boundary

This document is the sole repository artifact for the bounded
`POST_IDG_R6_0_IMPLEMENTATION_LEARNING_ASSESSMENT` at baseline
`9647226b4c54507041503655f9f919a27a3a8827`, on branch
`docs/post-idg-r6-0-implementation-learning-assessment`, for package version
`6.16.0`.

This is an assessment of the repository-effective R6.0 governed-memory
learning slice. It determines what the implementation proved, what remains
unknown, how the twenty-two material unknowns and six provisional success
targets changed, and which separate decision surface has the highest
information value.

This assessment creates no implementation authority, does not start R6.1,
does not define or authorize a future write set, and starts no successor work.
The R5 bounded authority has been exercised and satisfied. Authority for any
new implementation work is absent.

This remains an implementation-to-learn assessment: zero material unknowns
are resolved, and no new implementation authority is created.
No durable adoption occurs, no real proposal is created, and no execution
occurs.

## 2. Controlling state and evidence basis

R3 remains complete with hold and all twenty-two material unknowns remain
unresolved. R4 recommended READY with zero blocking HOLDs, seventeen
boundable HOLDs, and five deferable HOLDs. The Human Owner selected bounded
implementation, R5 completed with an AUTHORIZED decision, and R6.0
successfully exercised that exact authority.

R6.0 is complete and repository-effective. R6 has therefore started on main.
The authorized runtime surface is `governed_memory_learning_slice`; its
terminal artifact is `human_review_outcome_candidate`; continuation remains
unauthorized. No successor begins automatically.

The assessment relies on the repository-effective R6.0 implementation,
focused tests, evidence record, and the prior R3.6, R4, Human Owner, and R5
governance documents. It preserves their distinction between bounded runtime
evidence and product, production, operating, security, privacy, or lifecycle
claims.

## 3. What R6.0 actually proved

R6.0 successfully exercised the R5 bounded authority. Within the exact
single-candidate, single-project, local, in-memory slice, it established a
technically coherent orchestration from an accepted candidate through an
explicit human-review outcome and then a hard stop.

Verified runtime evidence includes:

- one exact public single-candidate API;
- an exact project-equality gate with deterministic mismatch rejection;
- a caller-asserted classification gate limited to `SYNTHETIC` and
  `NON_SENSITIVE`;
- preservation of declared source and provenance;
- reuse of repository-effective builders and validators rather than
  replacement logic;
- validation after every intermediate artifact;
- one deterministic fail-closed exception contract;
- deterministic semantic output for identical explicit inputs;
- exact preservation of reviewer, outcome, and rationale;
- a terminal validated `human_review_outcome_candidate`;
- a hard stop with `continuation_authorized` false;
- recursive evidence that no promotion state is true;
- no runtime files, `HERMES_HOME` state, or `.local` state;
- no durable adoption, real-proposal creation, execution, or persistence;
- no provider, model, connector, API, MCP, or network behavior;
- 26 passing focused tests;
- 73 passing compatibility tests;
- 321 passing inherited evidence tests; and
- a successful fresh temporary-environment operator smoke.

The result establishes bounded runtime-chain feasibility and runtime evidence
for fail-closed, deterministic, no-write, no-promotion, and single-project
boundaries for this exact slice.

## 4. What R6.0 did not prove

R6.0 did not establish broad-user value, product-market fit, product
usefulness, adoption, solution effectiveness, acceptable governance burden,
or measurable net value. It supplied no independent-user result and measured
no PEX target.

It did not establish production readiness; persistent storage or recovery;
correction, revocation, deletion, or complete lifecycle behavior; complete
authorization mediation; authenticated identity, roles, delegation,
credentials, or permissions; privacy compliance; poisoning, forgery, or
prompt-injection resistance; multi-project or tenant isolation; API, MCP, or
connector behavior; immutable live audit logging; monitoring or operating
readiness; availability, durability, concurrency, scale, or reliability; or
complete security.

The no-write design contains several risk exposures by making them inactive.
It does not test the corresponding controls and must not be converted into a
claim that those risks are resolved.

## 5. Material-unknown delta assessment

The material-unknown total remains twenty-two and the resolved count remains
zero. The assessment arithmetic is exactly 22 total, 0 resolved, 7 with
runtime evidence gained, 5 with a boundary confirmed but not resolved, 5
deferred as designed, and 5 unchanged HOLDs.

### 5.1 Runtime evidence gained, still unresolved

| ID | R6.0 delta and retained limitation |
|---|---|
| MU-02 | A real bounded implementation now exists, but usefulness, adoption, and solution effectiveness remain unvalidated. |
| MU-04 | A coherent runtime path now exists from accepted candidate through explicit human-review outcome, but correction, revocation, deletion, adoption, persistent audit, and full lifecycle orchestration remain absent. |
| MU-13 | Deterministic, inspectable local validations and status output now exist, but monitoring, alerting, retention, signal-quality study, and live audit operation do not. |
| MU-15 | Declared provenance is preserved through the runtime, but origin is not authenticated and forgery resistance is untested. |
| MU-16 | Runtime evidence now supports explicit non-promotion, no continuation, recursive negative promotion checks, and fail-closed intermediate validation, but complete repository-wide mediation, concurrency, replay, and bypass resistance remain unproven. |
| MU-19 | Exact project equality and mismatch rejection are established for one invocation, but multi-project, namespace, tenant, role, client, and audit-visibility isolation are unproven. |
| MU-21 | An explicit caller-asserted `SYNTHETIC`/`NON_SENSITIVE` gate and no-storage behavior now exist, but classification verification, minimization, consent, retention, disposal, subject rights, and incident-response controls do not. |

### 5.2 Boundary confirmed, not resolved

| ID | R6.0 delta and retained limitation |
|---|---|
| MU-05 | Persistence and recovery obligations were structurally excluded; their behavior remains untested. |
| MU-08 | Durable adoption and applied approval were structurally excluded; complete authority mediation and zero unauthorized durable adoption remain unproven. |
| MU-14 | Poisoning and semantic-manipulation exposure was contained through fixed synthetic/non-sensitive input and non-execution, not adversarially tested. |
| MU-18 | Prompt-injection exposure was contained by no model/tool execution and no external recall, not tested for resistance. |
| MU-22 | No external dependency was introduced, so the conditional external-evidence trigger remains inactive rather than resolved. |

### 5.3 Deferred as designed

| ID | Deliberately excluded unresolved area |
|---|---|
| MU-06 | Revocation and deletion authorization, propagation, derived/backup/cache treatment, and lifecycle audit completeness. |
| MU-07 | MCP, API, connector, interoperability, and live authentication or failure behavior. |
| MU-10 | Availability, durability, concurrency, scale, and production reliability. |
| MU-12 | Incident recovery, backup inventory, restoration, executed recovery, and operational RTO. |
| MU-17 | Authenticated identity, roles, delegation, credentials, and permission enforcement. |

### 5.4 Unchanged HOLD

| ID | Unchanged evidence deficit |
|---|---|
| MU-01 | No independent-user evidence or generalizability result. |
| MU-03 | No measurement that governance overhead is acceptable or produces net value. |
| MU-09 | No PEX result. |
| MU-11 | No staffing, support, escalation, audit-cadence, or operating-burden result. |
| MU-20 | No immutable live audit-log tamper-resistance evidence. |

No category reduces the unknown count. Runtime evidence narrows uncertainty
about an exact implementation path; it does not resolve the larger material
question represented by any MU.

## 6. Provisional success-target delta

### PST-01 — HOLD

There are no adopted records and no complete provenance-visibility result for
adopted records.

### PST-02 — HOLD-WITH-RUNTIME-EVIDENCE

The runtime now preserves an explicit reviewer, outcome, rationale, and
decision chain, but no durable adopted-record trace or authenticated approval
trace exists.

### PST-03 — HOLD-WITH-STRUCTURAL-NO-ADOPTION-EVIDENCE

The exact R6.0 slice performs no durable adoption and tests no promotion state
as true, but complete mediation and zero unauthorized adoption across all
possible repository paths remain unproven.

### PST-04 — HOLD

Correction, revocation, deletion, propagation, derived state, backup/cache
treatment, and lifecycle completion remain unimplemented.

### PST-05 — PASS-BOUNDED-STRENGTHENED

The implemented output distinguishes candidate, validation, review, decision,
draft, governance packet, explicit human outcome, non-application, and the
hard stop. Independent-user usability remains untested.

### PST-06 — HOLD

No measured comparison establishes net value over an ungoverned workflow.

## 7. Learning judgment

The learning gain is real and justifies separately considering another
bounded experiment. R6.0 converted several documentary feasibility claims
into runtime evidence and showed that the selected orchestration is
technically coherent within its exact scope. It also confirmed that the hard
boundaries can be expressed and tested without persistence, promotion, or
continuation.

The gain does not justify broadening into persistent adoption. Persistent
adoption would activate unresolved authorization, lifecycle, privacy,
recovery, audit, and operational obligations before the principal product
question is answered.

The greatest remaining near-term information deficit is whether a human
operator gains enough decision quality, visibility, and error prevention to
justify the additional governance burden. The highest-information-value next
surface is therefore a separate bounded operator-evaluation authorization
decision, not implementation and not persistent adoption.

## 8. Recommended future experiment, not authorized

The recommended future runtime task is
`POST_IDG_R6_1_GOVERNED_MEMORY_OPERATOR_EVALUATION`. This assessment
recommends consideration only. It neither authorizes nor starts that task and
does not define or authorize its write set.

A later authorization decision should compare a fixed synthetic/non-sensitive
ungoverned review condition against the governed R6.0 condition. It must
predeclare:

- the exact fixed scenario corpus;
- baseline and governed condition definitions;
- condition order and learning-effect controls;
- completion time;
- operator action count;
- invalid or unsafe input detection;
- project-scope error detection;
- state-promotion misunderstanding;
- decision correctness;
- rationale completeness;
- correction and rework burden;
- perceived usefulness;
- perceived governance burden;
- result interpretation limits; and
- the exact write set and test suite.

The proposed experiment must remain one human operator, one exact project,
synthetic or non-sensitive only, local, non-production, and non-persistent.
It must create no durable adoption, real proposal, or execution and must use
no API, MCP, connector, network, model, credentials, accounts, or roles.

## 9. Authority conclusion

R6.0 successfully exercised and satisfied the R5 bounded implementation
authority. That authority is exhausted; implementation authority for new work
is none.

R6.0 established exact-slice feasibility, not product, production, lifecycle,
security-completeness, privacy, IAM, operating, deployment, or release
authority. A future R6.1 experiment is merely eligible for a separate
authorization decision. No successor work starts automatically.

## 10. Machine-readable assessment

```text
TASK_ID=POST_IDG_R6_0_IMPLEMENTATION_LEARNING_ASSESSMENT
BASE_COMMIT=9647226b4c54507041503655f9f919a27a3a8827
ALLOWED_WRITE_FILE_COUNT=1

R3_STATUS=COMPLETE-WITH-HOLD
R4_READINESS_RECOMMENDATION=READY
R5_STATUS=COMPLETE
R5_AUTHORIZATION_DECISION=AUTHORIZED

R6_0_STATUS=COMPLETE
R6_0_REPOSITORY_EFFECTIVE=TRUE
R6_REPOSITORY_STATUS=STARTED-ON-MAIN

R5_BOUNDED_IMPLEMENTATION_AUTHORITY=EXERCISED-AND-SATISFIED
IMPLEMENTATION_AUTHORITY_FOR_NEW_WORK=NONE

MATERIAL_UNKNOWN_TOTAL=22
MATERIAL_UNKNOWN_RESOLVED_COUNT=0

RUNTIME_EVIDENCE_GAINED_COUNT=7
RUNTIME_EVIDENCE_GAINED_IDS=MU-02,MU-04,MU-13,MU-15,MU-16,MU-19,MU-21

BOUNDARY_CONFIRMED_NOT_RESOLVED_COUNT=5
BOUNDARY_CONFIRMED_NOT_RESOLVED_IDS=MU-05,MU-08,MU-14,MU-18,MU-22

DEFERRED_AS_DESIGNED_COUNT=5
DEFERRED_AS_DESIGNED_IDS=MU-06,MU-07,MU-10,MU-12,MU-17

UNCHANGED_HOLD_COUNT=5
UNCHANGED_HOLD_IDS=MU-01,MU-03,MU-09,MU-11,MU-20

MATERIAL_UNKNOWN_ARITHMETIC=22=7+5+5+5

PST_01_DISPOSITION=HOLD
PST_02_DISPOSITION=HOLD-WITH-RUNTIME-EVIDENCE
PST_03_DISPOSITION=HOLD-WITH-STRUCTURAL-NO-ADOPTION-EVIDENCE
PST_04_DISPOSITION=HOLD
PST_05_DISPOSITION=PASS-BOUNDED-STRENGTHENED
PST_06_DISPOSITION=HOLD

BOUNDED_RUNTIME_CHAIN_FEASIBILITY=ESTABLISHED
FAIL_CLOSED_BOUNDARY=ESTABLISHED-FOR-EXACT-SLICE
NO_WRITE_BEHAVIOR=ESTABLISHED-FOR-EXACT-SLICE
SINGLE_PROJECT_BOUNDARY=ESTABLISHED-FOR-EXACT-SLICE

PRODUCT_USEFULNESS=NOT-ESTABLISHED
GOVERNANCE_OVERHEAD_ACCEPTABILITY=NOT-ESTABLISHED
MEASURABLE_NET_VALUE=NOT-ESTABLISHED
INDEPENDENT_USER_GENERALIZABILITY=NOT-ESTABLISHED
PEX_PERFORMANCE=NOT-MEASURED
PRODUCTION_READINESS=NOT-ESTABLISHED

R6_0_FOCUSED_TEST=26-PASSED
R6_0_COMPATIBILITY_SUITE=73-PASSED
R6_0_INHERITED_EVIDENCE_SUITE=321-PASSED
R6_0_OPERATOR_SMOKE=PASSED

R6_0_LEARNING_ASSESSMENT_DECISION=LEARNING-GAIN-CONFIRMED
R6_0_LEARNING_ASSESSMENT_RECOMMENDATION=PROCEED-TO-SEPARATE-BOUNDED-OPERATOR-EVALUATION-AUTHORIZATION-DECISION

PROPOSED_NEXT_RUNTIME_TASK=POST_IDG_R6_1_GOVERNED_MEMORY_OPERATOR_EVALUATION
R6_1_ELIGIBILITY=AVAILABLE-FOR-SEPARATE-AUTHORIZATION-DECISION
R6_1_STATUS=NOT_STARTED

R6_0_LEARNING_ASSESSMENT_STATUS=COMPLETE-UNMERGED
R6_0_LEARNING_ASSESSMENT_REPOSITORY_EFFECTIVE=FALSE

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R6_1_BOUNDED_OPERATOR_EVALUATION_AUTHORIZATION_DECISION
```

This assessment is complete and unmerged. It creates no authority for new
implementation work.
