# Civilization Core POST-IDG R5 Bounded Implementation Authorization

## 1. Task identity and document authority

This document is the sole repository artifact for
`POST_IDG_R5_BOUNDED_IMPLEMENTATION_AUTHORIZATION` at baseline
`d0fcdac1f27117750ff89f0e2b6baa5a8d71d343`, on branch
`docs/post-idg-r5-bounded-implementation-authorization`, for package version
`6.16.0`.

R5 is documentation only. It creates no runtime and starts no implementation
automatically. Once repository-effective, it authorizes exactly one future
bounded implementation-to-learn task and no other implementation work.

## 2. Controlling repository-effective state

The controlling R3 state remains complete with hold. The R4 readiness
recommendation is READY with zero blocking HOLDs, seventeen HOLDs boundable by
an exact implementation scope, and five HOLDs deferable beyond a bounded
learning slice.

The repository-effective Human Owner R4 decision is
`AUTHORIZE_BOUNDED_IMPLEMENTATION`, and the R4 decision is complete. R5
eligibility is therefore established.

The preserved controlling values are:

- `R3_STATUS=COMPLETE-WITH-HOLD`;
- `R4_READINESS_RECOMMENDATION=READY`;
- `R4_BLOCKING_HOLD_COUNT=0`;
- `R4_BOUNDABLE_HOLD_COUNT=17`;
- `R4_DEFERABLE_HOLD_COUNT=5`;
- `R5_ELIGIBILITY=ESTABLISHED`;
- before repository effectiveness,
  `IMPLEMENTATION_AUTHORITY=NONE`; and
- before repository effectiveness,
  `IMPLEMENTATION_START=NOT_AUTHORIZED`.

Before this authorization becomes repository-effective, implementation
authority remains absent and implementation start remains unauthorized. This
document does not reinterpret the R3 or R4 evidence and does not resolve any
of the twenty-two material unknowns.

## 3. R5 authorization decision

The R5 decision is `AUTHORIZED` for exactly this future task:

`POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION`

The selected first runtime surface is:

`governed_memory_learning_slice`

This is deliberately narrower than the complete governed-memory control plane
selected as the R2 product direction. It is a bounded, local, non-production,
single-candidate, single-project orchestration path whose purpose is
implementation-to-learn. It is not an MVP-complete lifecycle, product
validation, production capability, or general implementation authority.

## 4. Exact future R6.0 write set

The future R6.0 task may create or modify exactly these three files:

1. `src/hermes_memory_fabric/governed_memory_learning_slice.py`
2. `tests/test_governed_memory_learning_slice.py`
3. `docs/CIVILIZATION_CORE_POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION_EVIDENCE.md`

No other repository write is authorized. In particular, R6.0 may not modify
any existing source, test, or documentation file.

## 5. Exact authorized runtime path

The only authorized orchestration path is:

```text
declared source/provenance
->
memory candidate
->
evidence/review chain
->
human review outcome
->
STOP
```

The terminal artifact is a `human_review_outcome_candidate`. It is
non-authoritative, non-applied, and non-persisted.

There is no adoption, recall, correction, revocation, deletion, real proposal
creation, or execution step. The runtime must not represent any of those
steps as completed, implied, or authorized.

## 6. Reuse strategy and orchestration boundary

R6.0 must reuse the repository-effective read-only builders and validators
rather than reproduce their logic. Where appropriate, the orchestration may
use:

- `validate_candidate_for_proposal_dry_run`;
- `candidate_to_memory_block_candidate`;
- `create_review_queue_item`;
- `evaluate_review_queue_item`;
- `create_memory_proposal_draft`;
- `create_governance_submission_candidate`;
- `create_governance_submission_packet`;
- `create_human_review_outcome_candidate`; and
- the validators corresponding to each produced artifact.

The implementation must validate every intermediate artifact before
progressing. Invalid intermediate state must fail closed and must not produce
a decision artifact.

The existing whole-chain candidate proposal dry-run entry point is not an
authorized shortcut for R6.0 because its current chain continues beyond the
human-review outcome into real-proposal planning and dry-run preview
artifacts. R6.0 must compose only the bounded stages above and stop after the
validated human-review outcome candidate.

R6.0 must not call or recreate downstream real-proposal execution or planning
paths. It specifically must not call:

- `create_real_proposal_creation_plan`;
- `create_real_proposal_dry_run`;
- `create_memory_write_proposal`;
- any memory human approval token writer;
- any real write executor;
- any write-lock executor;
- provider tools;
- network APIs; or
- model APIs.

Even non-writing downstream real-proposal previews are outside this first
R6.0 scope.

## 7. Required runtime API

The new module must expose one primary bounded orchestration entry point:

```python
run_governed_memory_learning_slice(
    candidate,
    *,
    project_id,
    reviewer,
    outcome,
    rationale,
    input_classification,
)
```

A trivial naming adjustment is permitted only if required by an established
repository convention. The entry point remains single-candidate and
single-project by design. No batch, multi-project, multi-tenant, service, or
external-channel entry point is authorized.

## 8. Explicit human-decision boundary

Every invocation must require explicit non-blank `reviewer`, explicit
`outcome`, and explicit non-blank `rationale`. The runtime must not infer,
default, synthesize, or silently substitute the final human-review outcome.

The supplied outcome must be checked by the existing supported human-review
outcome contract. An unsupported outcome fails closed. A supported outcome
produces only a human-decision artifact; it does not apply the decision,
persist approval, submit to governance, convert to a real proposal, or grant
authority to continue.

## 9. Input-classification boundary

The only allowed caller-asserted input classifications are:

- `SYNTHETIC`
- `NON_SENSITIVE`

Anything else, including blank or missing classification, must fail closed
before orchestration progresses.

The classification is an explicit caller assertion for this bounded
evaluation only. R6.0 must not claim to detect, infer, verify, or classify
sensitive data. It may not accept real sensitive, personal, confidential, or
production data on the theory that the runtime can classify it.

## 10. Single-scope boundary

Exactly one explicit, non-blank `project_id` is permitted per invocation. The
candidate's `project_id` must exactly equal the invocation `project_id`.
Blank scope or any mismatch must fail closed before artifact progression.

R6.0 authorizes no cross-project, cross-role, multi-tenant, namespace
federation, external-channel, account, delegation, or authenticated-role
behavior.

## 11. Candidate risk and governance boundary

Only a candidate accepted by the existing bounded candidate dry-run
validation may proceed. The authorized allowed-risk envelope is the existing
low-risk default; R6.0 must not widen it.

Malformed candidates and candidates with unsafe governance flags must fail
closed. A non-allowed risk level must remain non-progressing under the
existing locked disposition. Existing required dry-run, read-only, and
proposal-governed protections must remain intact, and existing forbidden
write, apply, persist, submit, convert, executor, and provider-tool flags must
not be weakened or bypassed.

## 12. Runtime storage and side-effect boundary

R6.0 must operate in memory only and must create no runtime files. No
persistence across process restart is authorized. No `.local` runtime state
is authorized.

The runtime must not write:

- memory or graph state;
- SQLite or any other database;
- proposal files;
- operation-ledger records;
- approval-audit records;
- approval or token files;
- configuration;
- cache;
- migrations;
- tombstones; or
- any durable lifecycle state.

It must not use provider tools, external services, network APIs, model APIs,
production credentials, public serving, MCP, connectors, or adapters.

## 13. Deterministic and inspectable output

Identical explicit inputs must produce deterministic semantic output. The
result must preserve enough inspectable material to demonstrate:

- declared source and provenance;
- the input candidate state;
- evidence and review-chain state;
- the terminal human-decision state;
- the exact project scope;
- the explicit reviewer;
- the explicit human outcome;
- the explicit rationale;
- validation results for the candidate and every intermediate artifact; and
- explicit no-write and non-application guarantees.

The result must identify itself as non-authoritative and non-applied. It must
contain no `true` state for applied, persisted, adopted, executed,
real-proposal-created, operation-event-created, approval-persisted, or any
equivalent promotion state.

It must not contain a real-proposal creation plan or real-proposal dry-run
artifact. Any non-applying recommendation already present in the existing
human-outcome contract remains informational only and must not be treated as
authorization or runtime progression beyond the decision boundary.

## 14. Required fail-closed behavior

The future implementation must fail closed for at least:

1. malformed candidate;
2. unsafe governance flags;
3. unsupported risk level;
4. blank `project_id`;
5. candidate/project mismatch;
6. blank `reviewer`;
7. unsupported or missing `outcome`;
8. blank `rationale`;
9. unsupported or missing input classification;
10. invalid intermediate artifact; and
11. any attempted unsupported progression beyond the decision boundary.

Failure must not produce a misleading successful decision artifact, mutate
the caller's candidate, create runtime state, or activate a downstream path.

## 15. PR #357 disposition

PR #357 remains closed, unmerged, and preserved. R5 does not authorize
merging it, cherry-picking it, transferring its complete control-plane
module, or copying its persistent JSON state design.

Its historical implementation remains provenance only. No code transfer is
authorized. Adoption, recall, correction, revocation, deletion, persistent
workspace state, and tombstones remain outside R6.0.

The broader historical design is not selected because persistent workspace
state and an end-to-end adopted-memory lifecycle would activate unresolved
authorization, persistence, lifecycle, privacy, recovery, and audit
assumptions too early. The selected slice instead reuses established
read-only substrate and stops before durable or applied authority.

## 16. Exact R6.0 validation requirements

### 16.1 Syntax validation

Run `python -m py_compile` on exactly the new runtime module and new focused
test:

- `src/hermes_memory_fabric/governed_memory_learning_slice.py`
- `tests/test_governed_memory_learning_slice.py`

### 16.2 New focused test

Run:

- `tests/test_governed_memory_learning_slice.py`

The new test file must cover all authorized positive behavior, negative
behavior, deterministic-output guarantees, boundary stops, and no-write
requirements.

### 16.3 Existing focused compatibility tests

Run:

- `tests/test_memory_candidate_proposal_dry_run.py`
- `tests/test_memory_human_review_outcome_gate.py`
- `tests/test_memory_review_decision_gate.py`
- `tests/test_p4_m1_source_provenance_verification_status.py`
- `tests/test_p4_m2_execution_decision_negative_evidence_non_override_map.py`

### 16.4 Inherited R3 evidence-focused suite

Run the exact inherited twenty-test evidence suite used at R3.6/R4:

1. `tests/test_p4_m1_source_provenance_verification_status.py`
2. `tests/test_memory_candidate_proposal_dry_run.py`
3. `tests/test_memory_human_review_outcome_gate.py`
4. `tests/test_memory_review_decision_gate.py`
5. `tests/test_memory_approval_intent_review_gate_dry_run.py`
6. `tests/test_memory_evidence_repair_recovery_decision_gate.py`
7. `tests/test_memory_evidence_repair_rollback_drill_preview.py`
8. `tests/test_memory_evidence_repair_write_lock_gate.py`
9. `tests/test_p4_m5_4_cross_surface_alignment_map.py`
10. `tests/test_p4_m6_0_next_corridor_entry_boundary_contract.py`
11. `tests/test_governance_multi_cycle_continuity_protocol.py`
12. `tests/test_governance_post_sandbox_review_boundary.py`
13. `tests/test_memory_evidence_repair_recovery_execution_preview.py`
14. `tests/test_p4_m1_human_gated_do_not_retry_verification_status.py`
15. `tests/test_p4_m6_5_entry_escalation_non_routing_surface.py`
16. `tests/test_p4_m0_subspace_operator.py`
17. `tests/test_memory_fabric_bridge.py`
18. `tests/test_skill_fabric.py`
19. `tests/test_p4_m2_execution_decision_negative_evidence_non_override_map.py`
20. `tests/test_memory_evidence_repair_recovery_closure_finalization_readiness_preview.py`

## 17. R6.0 operator smoke requirements

The future R6.0 task must use a fresh temporary evaluation environment and
prove all of the following:

1. a synthetic low-risk candidate with explicit provenance reaches a
   non-applied human-decision artifact;
2. the explicit reviewer, outcome, and rationale are preserved;
3. identical inputs produce deterministic semantic output;
4. candidate/project mismatch fails closed;
5. unsupported classification fails closed;
6. unsafe governance fails closed;
7. unsupported risk does not progress;
8. no runtime files are created;
9. no `HERMES_HOME` files are created;
10. no memory, proposal, token, audit, configuration, or database files are
    created;
11. no result state marks applied, persisted, adopted, or executed as true;
    and
12. no real-proposal plan or real-proposal dry-run artifact is produced.

## 18. R6.0 success criteria

R6.0 succeeds only if every one of these criteria passes:

```text
R6_0_SOURCE_CREATED=PASSED
R6_0_TEST_CREATED=PASSED
R6_0_EVIDENCE_DOC_CREATED=PASSED
R6_0_SYNTAX_VALIDATION=PASSED
R6_0_NEW_FOCUSED_TEST=PASSED
R6_0_COMPATIBILITY_SUITE=PASSED
R6_0_INHERITED_EVIDENCE_SUITE=PASSED
R6_0_OPERATOR_SMOKE=PASSED

EXPLICIT_HUMAN_DECISION=PASSED
SINGLE_PROJECT_SCOPE=PASSED
INPUT_CLASSIFICATION_GATE=PASSED
UNSAFE_INPUT_FAIL_CLOSED=PASSED
NO_RUNTIME_STORAGE=PASSED
NO_DURABLE_ADOPTION=PASSED
NO_REAL_PROPOSAL_CREATION=PASSED
NO_EXECUTION=PASSED
DETERMINISTIC_OUTPUT=PASSED
```

The R6.0 evidence document must record these results using the exact
machine-readable success keys specified by this authorization request.
Failure, omission, or unverified status for any criterion prevents R6.0 from
claiming completion.

## 19. Forbidden future R6.0 writes and changes

R6.0 must not modify:

- `pyproject.toml`;
- `uv.lock`;
- `.codex/`;
- `AGENTS.md`;
- `AGENTS.override.md`;
- any existing source file;
- any existing test file;
- any existing documentation file;
- `scripts/`; or
- `.github/`.

No dependency file, package initialization file, API, MCP, connector,
adapter, migration, UI, deployment, release, version change, or tag is
authorized.

## 20. Authority semantics and stage transition

Once this document is repository-effective, bounded implementation authority
exists only for the exact R6.0 task and exact three-file write set defined
above. It creates no general implementation authority and cannot be
transferred to another task, surface, file, phase, or lifecycle operation.

R6 eligibility is then established, while R6 remains not started.
Implementation may start only through the exact authorized R6.0 task; nothing
starts automatically.

Deployment, release, version, and tag authority remain absent. R6.0 itself
may not grant, infer, or expand any of those authorities.

## 21. Final machine state

```text
TASK_ID=POST_IDG_R5_BOUNDED_IMPLEMENTATION_AUTHORIZATION
BASE_COMMIT=d0fcdac1f27117750ff89f0e2b6baa5a8d71d343
ALLOWED_WRITE_FILE_COUNT=1

HUMAN_OWNER_R4_DECISION=AUTHORIZE_BOUNDED_IMPLEMENTATION
R4_DECISION_STATUS=COMPLETE

R5_STATUS=COMPLETE
R5_AUTHORIZATION_DECISION=AUTHORIZED

AUTHORIZED_IMPLEMENTATION_TASK=POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION
AUTHORIZED_WRITE_FILE_COUNT=3
AUTHORIZED_RUNTIME_SURFACE=governed_memory_learning_slice

PR357_REUSE_DISPOSITION=REFERENCE-ONLY-NO-CODE-TRANSFER

IMPLEMENTATION_AUTHORITY=BOUNDED
IMPLEMENTATION_AUTHORITY_SCOPE=EXACT-R6_0-TASK-ONLY
IMPLEMENTATION_START=AUTHORIZED-FOR-EXACT-R6_0-TASK-ONLY

R6_ELIGIBILITY=ESTABLISHED
R6_STATUS=NOT_STARTED

DURABLE_ADOPTION_AUTHORITY=NONE
PERSISTENT_STORAGE_AUTHORITY=NONE
EXTERNAL_SERVICE_AUTHORITY=NONE
DEPLOYMENT_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION
```

R5 is complete when this document is repository-effective. It authorizes
only the future bounded R6.0 implementation defined here and performs no
implementation itself.
