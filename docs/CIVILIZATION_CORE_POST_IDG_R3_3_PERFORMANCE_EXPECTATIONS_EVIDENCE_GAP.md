# Civilization Core POST-IDG R3.3 Performance Expectations Evidence Gap

## 1. Task identity and authority boundary

This document is the single repository artifact for the bounded POST-IDG
R3.3 performance-expectations evidence-gap task. Its baseline is commit
`e44f3b92e4e681b526843313d2acd19616a6412c`, and the package version remains
`6.16.0`.

The task defines provisional, measurable pre-implementation acceptance
targets for a future bounded runtime vertical slice. It does not report an
observation, implement measurement or instrumentation, create runtime, or
authorize implementation, deployment, release, version, tag, or successor
work. R4, R5, and R6 remain outside this task's authority.

## 2. Controlling R3 state

R1 and R2 are complete. R3 is active and incomplete. R3.1 and R3.2 are
reconciled complete with hold, R3.4 is reconciled complete with hold, and
R3.5 is reconciled complete with not required. Before this artifact, R3.3
required new bounded evidence for its unresolved performance-expectations
criterion.

Implementation readiness is not established. There is no implementation
authority, implementation start is not authorized, and no successor work
starts automatically. The overall R3 exit criterion remains deferred to a
separate integrated R3.6 resynthesis.

## 3. Historical R3.3 evidence retained

Historical R3.3A evidence is retained without upgrade or erasure:

- eight exact source/test pairs formed the bounded operating substrate;
- 130 focused tests passed for bounded contract behavior, not as a full-suite
  or performance result;
- tested behavior included fail-closed contracts, bounded status and audit
  surfaces, and non-mutating recovery or rollback preview substrate;
- operating responsibilities, incident-handling requirements, audit
  requirements, observability requirements, recovery expectations, and
  lifecycle requirements were partially identified;
- repeated Human Owner intervention showed support burden, but that burden
  was not measured;
- no live operating model, staffed operating process, live review queue, live
  incident process, backup inventory, restoration test, executed recovery,
  operational revocation/deletion process, implemented monitoring, or
  production operating evidence was established; and
- no service-level targets and no measured support workload existed.

The 130 focused contract tests do not establish latency, throughput,
capacity, performance, service levels, or operating capability. Every
historical HOLD and limitation remains active.

## 4. Performance scope and exclusions

The envelope applies only to a future non-production bounded vertical slice
for one Human Operator of AI memory workflows. It covers local bounded
control-plane behavior and defines engineering expectations that must be
validated later.

It excludes enterprise scale, multi-tenant scale, production traffic,
production service levels, public-cloud service levels, geographic
replication, production availability, production durability, production
recovery capability, external protocol performance, and market demand.
Human thinking, review, and approval time are not system latency. External
network time is excluded unless a later bounded implementation explicitly
introduces it and separately defines how to measure it.

## 5. Workload assumptions

The workload class is one Human Operator. Expected execution is sequential
or low-concurrency. No production concurrency number is inferred. Enterprise
scale and production traffic are out of scope.

Measurement begins when the bounded local system accepts a valid operation
request and ends when it makes the complete system response or explicit
held/fail-closed status available to the caller. Human decision time and
external network time are outside that interval.

## 6. PEX-01 Interactive inspection/status target

- **Scope:** bounded local read, status, provenance, and audit inspection for
  one operator.
- **Target:** the 95th-percentile system response time is at most 1,000 ms for
  the future validation sample. A normal inspection should remain
  interactive.
- **Exclusions:** human interpretation or approval, external network time,
  production traffic, and unrelated batch work.
- **Future validation:** record per-operation elapsed system time over a
  declared bounded sample, calculate P95 with the calculation method and
  sample size disclosed, and retain failures and held states in the result.
- **Current result:** `NOT-MEASURED`. No current-code compliance is claimed.

## 7. PEX-02 Candidate/review/decision target

- **Scope:** bounded non-mutating candidate, evidence, review, decision, and
  authority-check dry-run operations.
- **Target:** the 95th-percentile system response time is at most 2,000 ms for
  the future validation sample.
- **Exclusions:** Human Owner or reviewer decision duration, external network
  time, mutation or adoption execution, and production traffic.
- **Future validation:** time only the declared system dry-run boundary,
  disclose sample composition and P95 calculation, and preserve all error or
  hold outcomes rather than filtering them into a pass.
- **Current result:** `NOT-MEASURED`. No dry-run latency result exists.

## 8. PEX-03 Recovery/rollback preview target

- **Scope:** non-mutating recovery decision, recovery execution preview, and
  rollback drill preview only.
- **Target:** the 95th-percentile preview response time is at most 5,000 ms for
  the future validation sample.
- **Exclusions:** human recovery decisions, executed recovery, restoration,
  rollback execution, backup validation, RTO, and production recovery.
- **Future validation:** measure the bounded preview request-to-complete-preview
  interval, disclose the scenario set and P95 method, and separately report
  invalid, conflict, and held cases.
- **Current result:** `NOT-MEASURED`. This target is neither an RTO nor a
  restoration-performance result.

## 9. PEX-04 Bounded batch/reconciliation target

- **Scope:** one future bounded non-production batch or reconciliation corpus
  containing no more than 100 declared items.
- **Target:** complete the entire declared bounded operation within 30,000 ms.
- **Exclusions:** production throughput, hidden follow-on work, unbounded
  discovery, external network time, and human review time.
- **Future validation:** declare the corpus and item count before execution,
  measure the complete bounded system interval, verify that scope did not
  silently expand, and report partial completion or expansion as a miss or
  invalid measurement as applicable.
- **Current result:** `NOT-MEASURED`. This is not a production throughput
  service level.

## 10. PEX-05 Fail-closed visibility target

- **Scope:** surfacing a held or fail-closed system state after detecting
  invalid evidence, conflict, lock failure, unsupported authority, or a
  required human hold.
- **Target:** make that status visible within 1,000 ms of the bounded system
  detecting the triggering condition.
- **Exclusions:** Human Owner acknowledgement or response, incident
  resolution, correction, recovery, routing, notification transport, and
  external network time.
- **Future validation:** capture the detection timestamp and complete visible
  status timestamp, verify the status preserves the reason and does not
  authorize action, and report every scenario disposition.
- **Current result:** `NOT-MEASURED`. Existing fail-closed contract tests do
  not establish this visibility latency.

## 11. PEX-06 Bounded stability expectation

- **Scope:** one future sequential run of 100 bounded control-plane
  operations under the single-operator workload assumptions.
- **Target:** complete all 100 operations without unexpected
  repository/storage mutation, unauthorized authority transition, process
  crash, unhandled exception, or silent loss of an audit/status result.
- **Exclusions:** production reliability, availability, durability,
  concurrency stress, long-duration soak behavior, and recovery capability.
- **Future validation:** predeclare the operation sequence and permitted
  state, capture each result and audit/status output, compare repository and
  storage state before and after, and treat any named forbidden event as a
  target miss rather than reinterpret it as success.
- **Current result:** `NOT-MEASURED`. No bounded stability run was performed
  by this task.

## 12. Measurement and future validation semantics

Each PEX separates three concepts:

| Concept | Meaning in this task |
|---|---|
| Target | A provisional engineering acceptance threshold defined before implementation. |
| Measurement | A future execution using a declared workload, timing boundary, sample, and calculation method. |
| Result | A future evidence-backed disposition derived from a valid measurement. |

Targets are defined; measurements have not been performed; results are not
established. This artifact assigns `NOT-MEASURED` to PEX-01 through PEX-06.
It neither converts a target into evidence nor converts historical contract
test success into performance success.

A future bounded validation may assign exactly one of these dispositions to
each PEX: `MEETS-TARGET`, `MISSES-TARGET`, `NOT-MEASURED`, or
`INVALID-MEASUREMENT`. A miss must remain visible and cannot be converted to
pass by interpretation. A measurement with an undeclared or violated timing
boundary, workload, sample, calculation, or scope must be reported as
invalid rather than used to support compliance.

## 13. R33-01 gap disposition

All six PEX expectations now identify a bounded scope, measurable threshold,
explicit exclusions, future validation semantics, and an unambiguous
not-measured result. None makes a false current-performance claim.

Therefore R33-01 is addressed with bounded expectations. This closes only
the missing pre-implementation target-definition gap; it does not establish
measured performance or operating capability.

R33-02 through R33-06 remain reusable with hold. Their reliability,
recovery, audit, observability, and data-lifecycle requirements are not pass
claims and are not operational-capability claims.

## 14. R3.3 reconciliation disposition

Because R33-01 is addressed under the bounded rule, this gap task is complete
with hold and the R3.3 current outcome is reconciled complete with hold. The
hold preserves every historical staffing, process, recovery, lifecycle,
monitoring, workload, and production-evidence limitation.

Complete with hold does not establish an operating model. The overall R3
exit remains active and incomplete pending independent integrated R3.6
resynthesis.

## 15. Next allowed task

The next allowed task is the POST-IDG R3.6 evidence resynthesis because R3.1
through R3.4 are now reconciled complete with hold and R3.5 is reconciled
complete with not required. Eligibility is not automatic execution. R3.6
must independently synthesize the overall evidence and must not
automatically start R4.

## 16. Final machine state

```text
TASK_ID=POST-IDG-R3_3_PERFORMANCE_EXPECTATIONS_EVIDENCE_GAP
BASE_COMMIT=e44f3b92e4e681b526843313d2acd19616a6412c
ALLOWED_WRITE_FILE_COUNT=1

PERFORMANCE_SCOPE=BOUNDED-PRE-IMPLEMENTATION-SINGLE-OPERATOR

P95_SYSTEM_RESPONSE_TARGET_MS=1000
P95_DRY_RUN_RESPONSE_TARGET_MS=2000
P95_RECOVERY_PREVIEW_TARGET_MS=5000
BOUNDED_BATCH_ITEM_COUNT=100
BOUNDED_BATCH_COMPLETION_TARGET_MS=30000
FAIL_CLOSED_STATUS_VISIBILITY_TARGET_MS=1000
BOUNDED_STABILITY_OPERATION_COUNT=100

WORKLOAD_CLASS=SINGLE-HUMAN-OPERATOR
CONCURRENCY_EXPECTATION=SEQUENTIAL-OR-LOW-CONCURRENCY
ENTERPRISE_SCALE_EXPECTATION=OUT-OF-SCOPE
PRODUCTION_TRAFFIC_EXPECTATION=OUT-OF-SCOPE
HUMAN_DECISION_TIME_INCLUDED_IN_SYSTEM_LATENCY=NO
EXTERNAL_NETWORK_TIME_INCLUDED=NO

PERFORMANCE_TARGET_STATUS=DEFINED
PERFORMANCE_MEASUREMENT_STATUS=NOT-PERFORMED
PERFORMANCE_RESULT_STATUS=NOT-ESTABLISHED
TARGET_IS_NOT_MEASUREMENT=TRUE
TARGET_IS_NOT_PASS_RESULT=TRUE

R33_01_GAP_DISPOSITION=ADDRESSED-WITH-BOUNDED-EXPECTATIONS

R33_02_RELIABILITY_REQUIREMENTS=REUSABLE-WITH-HOLD
R33_03_RECOVERY_EXPECTATIONS=REUSABLE-WITH-HOLD
R33_04_AUDIT_REQUIREMENTS=REUSABLE-WITH-HOLD
R33_05_OBSERVABILITY_REQUIREMENTS=REUSABLE-WITH-HOLD
R33_06_DATA_LIFECYCLE_REQUIREMENTS=REUSABLE-WITH-HOLD

R3_3_GAP_TASK_DISPOSITION=COMPLETE-WITH-HOLD
R3_3_CURRENT_OUTCOME=RECONCILED-COMPLETE-WITH-HOLD

OPERATING_MODEL=NOT-ESTABLISHED

R3_STATUS=ACTIVE_INCOMPLETE
R4_STATUS=NOT_STARTED
R5_STATUS=NOT_STARTED
R6_STATUS=NOT_STARTED

IMPLEMENTATION_READINESS=NOT-ESTABLISHED
IMPLEMENTATION_AUTHORITY=NONE
IMPLEMENTATION_START=NOT_AUTHORIZED

R6_0_ARTIFACT_STATUS=PRESERVED_UNMERGED
R6_0_IMPLEMENTATION_AUTHORITY=NONE

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R3_6_EVIDENCE_RESYNTHESIS
```

This disposition creates no implementation, deployment, release, version,
tag, successor-stage, or automatic-work authority.
