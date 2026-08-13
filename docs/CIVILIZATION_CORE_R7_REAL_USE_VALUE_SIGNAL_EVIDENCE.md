# Civilization Core R7 Real-Use Value-Signal Evidence

## 1. Purpose and Classification

This document records one Human Owner-confirmed and validated R7 real-use actual result and its value-signal assessment. It is a governance evidence record, classified as `REAL-USE-ACTUAL-RESULT-AND-VALUE-SIGNAL-EVIDENCE`.

This file is a local draft. It does not become repository-effective Evidence unless the independent review, commit, push, pull-request, merge, and post-merge verification gates in this document are completed. It is not an R7 Formal Closure decision and grants no successor authority.

## 2. Repository and Authority Identity

- Repository: `/Users/han/hermes-memory-fabric-plugin`
- Base branch: `main`
- Base commit: `e040faaf15f4b5aa199dab781a91f7d54125a132`
- Package version: `6.16.0`
- Work branch: `docs/civilization-core-r7-real-use-value-signal-evidence`
- Target file: `docs/CIVILIZATION_CORE_R7_REAL_USE_VALUE_SIGNAL_EVIDENCE.md`
- PR #382 merged R7 Minimum Value-Signal Slice 2.
- PR #384 merged the unified real-use observation and validation entrypoint.
- Latest roadmap control: `R7-POST-SLICE-2-REAL-USE-VALIDATION-READINESS-DECISION-WHEN-MERGED`
- Source roadmap stage: `R7-SLICE-2-MERGED-REAL-USE-SNAPSHOT-PENDING`

The repository authority chain used by this record consists of exactly these three paths:

1. `docs/CIVILIZATION_CORE_POST_IDG_MASTER_EXECUTION_ROADMAP.md`
2. `docs/CIVILIZATION_CORE_R7_POST_IMPLEMENTATION_ROADMAP_RECONCILIATION_DECISION.md`
3. `docs/CIVILIZATION_CORE_R7_POST_SLICE_2_REAL_USE_VALIDATION_READINESS_DECISION.md`

The third document is the latest repository-effective R7 control source. It supersedes the second document's historical Slice 2 `AUTHORIZED-NOT-STARTED` implementation-status fields without deleting, invalidating, or rewriting that historical authority chain.

## 3. Evidence Sources and Integrity Limits

This governance record is based on the Human Owner-confirmed and validated task results supplied for the real-use sessions, the independent exit adjudication, and the three repository authority documents listed above.

The temporary stdout, stderr, and temporary workspace from the successful execution are not claimed to have been persisted as raw attachments. This record does not invent or claim any raw log attachment, external evidence file, artifact hash, or timestamp beyond the two supplied Session 3 epoch values. It records the validated result fields without representing that the product entrypoint created or persisted this Evidence.

The baseline was supplied from previously Human Owner-confirmed and validated real-use observation. The product did not automatically measure, generate, infer, or reconstruct the baseline. The product workflow did not create or persist an assessment or Evidence outside the terminal, non-applied result described below.

Session 2 and Session 3 remain distinct historical results. Session 3 does not overwrite, delete, correct, or reinterpret Session 2.

## 4. Validated Baseline

- `baseline_available`: `true`
- `baseline_human_correction_count`: `1`
- `baseline_recovery_time_seconds`: `131`
- `baseline_source`: `previously Human Owner-confirmed and validated real-use observation`
- `measurement_scope`: `NEW-WINDOW-HANDOFF-TO-VERIFIED-TERMINAL-STATE`

The baseline is valid for the stated comparison and is caller-provided historical real-use data. No claim is made that the product automatically measured or generated it.

## 5. Session 2 Negative Result Preserved

Session 2 is preserved as an independent negative historical result:

- `recovery_time_seconds`: `175`
- `human_correction_count`: `0`
- `governance_burden_worthwhile`: `false`
- `reduced_human_correction`: `true`
- `shortened_recovery_time`: `false`
- `benefit_inference_allowed`: `false`

Session 2 reduced human correction relative to the validated baseline but did not shorten recovery time, and the Human Owner did not find its governance burden worthwhile. Its negative result is not replaced, hidden, deleted, or rewritten by Session 3.

## 6. Session 3 Real-Use Observation

- `recovery_start_epoch_seconds`: `1786625848`
- `recovery_end_epoch_seconds`: `1786625863`
- `recovery_time_seconds`: `15`
- `human_correction_count`: `0`
- `task_completed`: `true`
- `state_traceable`: `true`
- `governance_burden_worthwhile`: `true`
- `human_owner_confirmation`: `准确且值得`
- `measurement_scope`: `NEW-WINDOW-HANDOFF-TO-VERIFIED-TERMINAL-STATE`
- `caller_observed`: `true`

The supplied start and end epochs differ by 15 seconds, matching the recorded recovery time. The measurement scope exactly matches the validated baseline scope.

## 7. Pre-Workflow Failures

Two pre-workflow failures occurred before the final correct product execution and are disclosed in full at the available classification level:

1. The first attempt failed because a required CLI argument was missing.
2. The second attempt failed because it used the wrong module entrypoint.

Neither failure entered the product observation/validation workflow. Neither produced an assessment, Evidence, or persisted result. Neither modified the observation measurement, belonged to `NEW-WINDOW-HANDOFF-TO-VERIFIED-TERMINAL-STATE`, or contaminated the final real-use observation.

These failures are not hidden, but they are not product workflow executions and are not included in the product observation/validation execution count. That count remains exactly `1`.

## 8. Successful Observation Validation

- `correct_module`: `hermes_memory_fabric.p4_m0_subspace_operator`
- `observation_validation_execution_count`: `1`
- `exit_code`: `0`
- `stdout_complete_json_object`: `true`
- `stderr_empty`: `true`
- `terminal`: `true`
- `non_applied`: `true`
- `non_persisted`: `true`
- `continuation_authorized`: `false`
- `snapshot_exact_match`: `true`
- `measurement_scope_match`: `true`
- `baseline_source_match`: `true`
- `temporary_workspace_empty`: `true`
- `assessment_status`: `validated`
- `benefit_inference_allowed`: `false`

This was the only execution that entered the product observation/validation workflow. The result was terminal, non-applied, non-persisted, and did not authorize continuation. The complete-JSON and empty-stderr fields are validated result facts; this document does not claim that their temporary streams were retained as raw attachments.

## 9. Five Value Signals

The validated baseline and Session 3 observation support all five required R7 value signals:

1. `task_completion=true`
2. `state_traceability=true`
3. `reduced_human_correction=true`
4. `shortened_recovery_time=true`
5. `governance_burden_worthwhile=true`

Human correction decreased from `1` to `0`, and recovery time decreased from `131` seconds to `15` seconds within the same measurement scope. The Human Owner confirmed the observed result as `准确且值得`.

`benefit_inference_allowed=false` means that the product entrypoint must not independently infer, promote, or exaggerate broader benefits. It does not negate the Human Owner-confirmed real result, is not a condition requiring the R7 exit requirement to be false, and must not be rewritten as `true`.

## 10. Exit Adjudication

The independent exit adjudication is recorded as follows:

- `adjudication_id`: `R7_POST_REAL_USE_VALUE_SIGNAL_EXIT_ADJUDICATION_1`
- `adjudication_state`: `PASS`
- `authority_chain_valid`: `true`
- `baseline_valid`: `true`
- `measurement_comparable`: `true`
- `evidence_integrity_valid`: `true`
- `safety_boundaries_preserved`: `true`
- `all_five_exit_signals_satisfied`: `true`
- `blocking_reason_count`: `0`
- `r7_exit_requirement_satisfied`: `true`
- `r7_formal_closure_eligible`: `true`
- `evidence_recording_eligible`: `true`

Eligibility is not authority. This Evidence record does not make the Formal Closure decision and does not execute closure.

## 11. Safety and Non-Persistence Boundaries

The successful execution remained terminal, non-applied, and non-persisted. It authorized no continuation. Its snapshot, measurement scope, and baseline source exactly matched the validated inputs, and the temporary workspace was empty at the verified terminal state.

No automatic baseline generation, automatic product measurement, durable assessment write, Evidence persistence by the product entrypoint, graph write, configuration mutation, or successor execution is claimed or authorized by this record.

The two disclosed pre-workflow failures remain outside the measurement and product workflow execution count. Their disclosure does not convert them into product observations or persisted evidence.

## 12. Explicit Non-Authorities

This local draft grants none of the following:

- R7 Formal Closure authority;
- Checkpoint B authority;
- R8 through R13 entry, implementation, or execution authority;
- automatic continuation or automatic successor work;
- commit, push, pull-request, merge, tag, release, or version-change authority; or
- authority for the product to infer or advertise macro-level benefit.

The independent adjudication establishes that R7 is eligible for Formal Closure; it does not grant or exercise Formal Closure authority. Formal Closure, Checkpoint B, and R8-R13 remain unexecuted and unauthorized.

## 13. Successor Gate

This local draft does not create repository-effective Evidence. Repository effectiveness requires a separately authorized independent review, commit, push, pull request, merge, and post-merge verification.

Even after this Evidence is merged, Formal Closure must not execute automatically. R7 Formal Closure requires separate, explicit Human Owner authorization and its own bounded task. Checkpoint B and R8-R13 remain unauthorized. No successor task may start automatically from this record.

The next recommended task is `INDEPENDENT-R7-REAL-USE-EVIDENCE-REVIEW`.

## 14. Machine-Readable Control Fields

```text
EVIDENCE_ID=CIVILIZATION_CORE_R7_REAL_USE_VALUE_SIGNAL_EVIDENCE
EVIDENCE_CLASSIFICATION=REAL-USE-ACTUAL-RESULT-AND-VALUE-SIGNAL-EVIDENCE
EVIDENCE_RECORDING_STATE=LOCAL-DRAFT-REPOSITORY-EFFECTIVE-WHEN-MERGED
SOURCE_ROADMAP_CONTROL=R7-POST-SLICE-2-REAL-USE-VALIDATION-READINESS-DECISION-WHEN-MERGED
SOURCE_ROADMAP_STAGE=R7-SLICE-2-MERGED-REAL-USE-SNAPSHOT-PENDING
EXIT_ADJUDICATION_ID=R7_POST_REAL_USE_VALUE_SIGNAL_EXIT_ADJUDICATION_1
EXIT_ADJUDICATION_STATE=PASS
SESSION_2_RESULT_PRESERVED=TRUE
SESSION_3_OBSERVATION_VALID=TRUE
PRE_WORKFLOW_FAILURE_COUNT=2
PRODUCT_OBSERVATION_VALIDATION_EXECUTION_COUNT=1
BASELINE_VALID=TRUE
MEASUREMENT_COMPARABLE=TRUE
TASK_COMPLETION=TRUE
STATE_TRACEABILITY=TRUE
REDUCED_HUMAN_CORRECTION=TRUE
SHORTENED_RECOVERY_TIME=TRUE
GOVERNANCE_BURDEN_WORTHWHILE=TRUE
ALL_FIVE_EXIT_SIGNALS_SATISFIED=TRUE
BENEFIT_INFERENCE_ALLOWED=FALSE
R7_EXIT_REQUIREMENT_SATISFIED=TRUE
R7_FORMAL_CLOSURE_ELIGIBLE=TRUE
FORMAL_CLOSURE_AUTHORITY=NONE
CHECKPOINT_B_AUTHORITY=NONE
R8_TO_R13_AUTHORITY=NONE
AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_TASK=INDEPENDENT-R7-REAL-USE-EVIDENCE-REVIEW
```
