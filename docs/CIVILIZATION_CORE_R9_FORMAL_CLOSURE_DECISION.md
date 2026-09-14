# Civilization Core R9 System Validation and Pilot Readiness Formal Closure Decision

## 1. Decision identity

```text
DECISION_ID=CIVILIZATION_CORE_R9_SYSTEM_VALIDATION_AND_PILOT_READINESS_FORMAL_CLOSURE_DECISION
DECISION_CLASSIFICATION=R9-FORMAL-CLOSURE-GOVERNANCE-DECISION
HUMAN_OWNER_AUTHORIZATION=AUTHORIZE-R9-BOUNDED-FORMAL-CLOSURE-AND-CONDITIONAL-PUBLICATION
HUMAN_OWNER_R9_DECISION=PASS-BOUNDED-SCOPE
HUMAN_OWNER_SIGNATURE=NOT-CLAIMED
R9_STATE_TRANSITION=OPEN-TO-CLOSED-WHEN-THIS-DECISION-AND-CANDIDATE-ARE-MERGED-AND-POST-MERGE-VERIFIED
R9_FORMAL_CLOSURE_REPOSITORY_EFFECTIVE=PENDING-MERGE-AND-POST-MERGE-VERIFICATION
R10_ENTRY_DECISION_ELIGIBLE=ONLY-AFTER-REPOSITORY-EFFECTIVE-R9-PASS
R10_ENTRY_AUTHORIZED=FALSE
REAL_PILOT_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
```

The Human Owner approves R9 as `PASS-BOUNDED-SCOPE` for system validation and
pilot readiness of one local Founder-Operator, the Civilization Core project,
and one continuity workflow. This document records the current authorization;
it does not invent a signature or a historical approval date.

## 2. R8 baseline and R9 candidate identity

R9 began from repository-effective R8 PASS on `main` at
`f39399491b9ec408900a4e11539a4392b36f3aa6`. R8 made R9 eligible only for a
separate entry decision and did not authorize R9 or successor execution.

The reviewed R9 candidate keeps package version `6.16.0`, adds no repository
root `uv.lock`, and changes exactly these six files:

```text
docs/HERMES_INTEGRATION.md
docs/CIVILIZATION_CORE_R9_SYSTEM_VALIDATION_RUNBOOK.md
tests/fixtures/r9/continuity_allow_observation.json
tests/fixtures/r9/continuity_allow_security_envelope.json
tests/fixtures/r9/continuity_block_sensitive_observation.json
tests/fixtures/r9/continuity_block_sensitive_security_envelope.json
```

The authenticated candidate manifest is `FINAL_CANDIDATE.sha256` in the R9
consolidated completion and handoff package. This closure decision is the
seventh and only additional repository path in the publication commit.

## 3. Independent review and R9-IR-001

The final independent reviewer authenticated the consolidated handoff and its
frozen source packages, verified the unchanged six-file candidate, and issued:

```text
INDEPENDENT_REVIEW_STATUS=PASS
R9_IR_001_STATUS=RESOLVED
R9_READINESS_RECOMMENDATION=RECOMMEND-PASS-BOUNDED-SCOPE
PUBLICATION_PREPARATION_STATUS=READY
```

The final review manifest SHA-256 is
`613f1a7c6d82e964c0bdae41109901fb37e34c50b0242fe7e9f9893942c46a9d`.
The consolidated handoff manifest SHA-256 is
`4f3c9361cdfed046f8ad28c14feae7c9b01a94784fb860f5d5084a01828918f4`.

`R9-IR-001` identified false historical statements that the first smoke had not
started and that the second was the unique execution. The authenticated
correction preserves the original receipts and supersedes only those claims.
There were two historical smoke-script executions. Attempt 1 emitted all ten
scripted success lines, but its child exit code, PID/PGID, exact completion
time, receipt-failure ordering, and overlap or concurrency state remain
`UNKNOWN`; its wrapper exited 1. Attempt 2 recorded wrapper exit 0 and its
available process receipt. The final review did not rewrite those unknowns.

A later, separately authorized current validation used a frozen wrapper and
recorded input identity, child PID/PGID, terminal completion, child return code
0, wrapper exit 0, no timeout, and final process absence. This new evidence
establishes the current candidate's bounded smoke result; it does not
retroactively prove that the first historical run succeeded or was compliant.

## 4. Evidence accepted within scope

The Human Owner accepts the following evidence only in its stated scope:

1. The synthetic CLI ALLOW scenario exited 0 and produced the expected terminal,
   non-persisted observation result.
2. The synthetic sensitive BLOCK scenario exited 2 and produced the minimized,
   sanitized three-field receipt without prohibited payload disclosure.
3. The focused four-file validation corridor recorded `361 passed in 1.01s`,
   exit 0. It is not a full-repository rerun.
4. The authenticated source copy built and installed offline into an isolated
   environment with dependency resolution disabled. Plugin distribution and
   module version `6.16.0`, Hermes runtime `0.18.2`, and the real Hermes loader
   origin were established separately.
5. The separately authorized current no-model smoke proved provider discovery
   and load, provider name, empty tool schemas, and the presence of
   `build_active_context`. Its fresh external `HERMES_HOME` gained only the
   Hermes-generated `SOUL.md`; the authenticated shim files remained unchanged.

The runbook is an operator procedure and is not treated as the authority source
for the separately authorized current validation.

## 5. Accepted limits and unperformed pilot work

The Human Owner expressly accepts that synthetic CLI scenarios and isolated
no-model integration are not a real pilot. Method-presence inspection is not
actual `build_active_context` business execution and is not a model call.

This R9 decision establishes neither real-user value nor product-wide maturity,
production readiness, deployment approval, release approval, multi-user or
cross-project behavior, live-model behavior, or generalized performance. No
real user, real data, model call, network service, fee, deployment, release,
Checkpoint B, or R10-R13 execution occurred as part of this decision.

## 6. Repository-effectiveness condition

This decision becomes repository-effective only after the exact reviewed six
files and this decision document are committed, published in a pull request
against the expected `main`, merged without bypassing applicable review or
repository rules, and verified on synchronized `main`. This document does not
predeclare its own future commit or merge commit. Actual publication and merge
identities belong in the external post-merge evidence report.

Until that chain succeeds:

```text
R9_FORMAL_CLOSURE_REPOSITORY_EFFECTIVE=FALSE
R10_ENTRY_DECISION_ELIGIBLE=FALSE
R10_ENTRY_AUTHORIZED=FALSE
REAL_PILOT_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
```

## 7. Successor boundary

After repository effectiveness, R9 PASS makes R10 eligible only for a separate
Human Owner entry decision under the master roadmap. Eligibility is not entry
authorization and starts no pilot or successor work.

```text
R10_ENTRY_DECISION_ELIGIBLE=ONLY-AFTER-REPOSITORY-EFFECTIVE-R9-PASS
R10_ENTRY_AUTHORIZED=FALSE
REAL_PILOT_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
```
