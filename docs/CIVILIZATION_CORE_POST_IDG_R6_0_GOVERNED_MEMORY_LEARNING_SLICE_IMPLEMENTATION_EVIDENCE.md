# Civilization Core POST-IDG R6.0 Governed Memory Learning Slice Implementation Evidence

## Purpose and controlling authority

This evidence records the bounded implementation-to-learn runtime authorized
by the repository-effective R5 decision. The implementation accepts one
explicitly classified, low-risk candidate for one exact project scope,
constructs the existing read-only governance artifacts in memory, records an
explicit human-review outcome candidate, and stops.

The package remains version 6.16.0. This task did not modify package metadata,
dependencies, versions, releases, tags, or existing repository files.

## Exact write set

Exactly three files were created:

1. `src/hermes_memory_fabric/governed_memory_learning_slice.py`
2. `tests/test_governed_memory_learning_slice.py`
3. `docs/CIVILIZATION_CORE_POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION_EVIDENCE.md`

No existing file was modified as part of the authored implementation.

## Implementation architecture

The public runtime is
`run_governed_memory_learning_slice(candidate, *, project_id, reviewer,
outcome, rationale, input_classification)`. It deep-copies the caller's
candidate before validation, preserves the caller's exact project scope and
explicit human inputs, and returns a deep-copied deterministic result.

The implementation directly reuses repository-effective public builders and
validators. It does not call the existing whole-chain dry-run entry point and
does not import or call real-proposal planning, real-proposal dry-run, durable
proposal creation, token writers, executors, provider tools, network APIs, or
model APIs.

`GovernedMemoryLearningSliceError` is the single deterministic fail-closed
exception. It exposes `code`, `stage`, and immutable tuple `reasons`; its
rendering contains only those stable control values and does not render
candidate memory content.

## Input and fail-closed boundaries

The runtime requires a Mapping candidate, a non-blank invocation project ID,
an exactly matching non-blank candidate project ID, a non-blank reviewer, an
explicit supported human outcome, a non-blank rationale, and the exact
classification `SYNTHETIC` or `NON_SENSITIVE`.

The candidate must declare a non-empty provenance Mapping and must receive an
`accepted` disposition from the existing candidate validator under its
low-risk default. Rejected governance input and locked higher-risk input
preserve the existing validator reasons in the bounded exception. Every
intermediate validator must return exactly valid with an empty error list;
otherwise the runtime stops with `invalid_intermediate_artifact` and the
failed artifact stage.

## Exact orchestration and terminal boundary

The implemented sequence is:

1. candidate validation;
2. candidate to memory-block candidate;
3. memory-block candidate validation;
4. review-queue item creation;
5. review-queue item validation;
6. review-queue evaluation;
7. review-decision candidate validation;
8. memory-proposal draft creation using the explicit reviewer as author;
9. memory-proposal draft validation;
10. governance-submission candidate creation;
11. governance-submission candidate validation;
12. governance-submission packet creation;
13. governance-submission packet validation;
14. human-review outcome candidate creation with the explicit outcome and rationale;
15. human-review outcome candidate validation;
16. hard stop.

The terminal artifact is the validated human-review outcome candidate.
Existing nested recommendation objects remain informational. The top-level
result denies continuation and invokes no recommended downstream action.

## No-write and non-promotion guarantees

The result explicitly declares no memory, graph, SQLite, proposal-file,
operation-ledger, approval-audit, token, configuration, or cache write. It
also declares no real-proposal creation, operation event, proposal
application, approval persistence, memory adoption, action execution, or
provider tool.

Focused tests recursively inspect mappings and sequences for exact promotion
keys and promotion-key suffixes. No applied, persisted, adopted, executed,
real-proposal-created, operation-event-created, approval-persisted, proposal-
applied, memory-adopted, or action-executed value is true. The explicit
`non_applied` and `non_persisted` assertions remain non-promotion guarantees.

The runtime module imports no filesystem, database, process, socket, HTTP, or
path API and performs no filesystem access.

## PR #357 disposition

PR #357 was not inspected, checked out, copied, merged, cherry-picked, or used
as an implementation source. Its disposition remains reference-only, with no
code transfer. Persistent state and the broader adopted-memory lifecycle
remain outside this slice.

## Validation commands and actual results

Syntax validation used the required interpreter and exactly the new runtime
and focused test files:

```text
$PWD/.venv/bin/python -m py_compile \
  src/hermes_memory_fabric/governed_memory_learning_slice.py \
  tests/test_governed_memory_learning_slice.py
```

Actual result: exit code 0 with no output.

The required new focused test command completed with:

```text
26 passed in 0.18s
```

The required five-file compatibility command completed with:

```text
73 passed in 1.09s
```

The required inherited twenty-file evidence command completed with:

```text
321 passed in 145.63s (0:02:25)
```

## Operator smoke

A fresh `TemporaryDirectory` was used as the working directory. `HERMES_HOME`
pointed to a not-yet-created child directory. The inline smoke program invoked
only the new public runtime API through `$PWD/.venv/bin/python`.

The smoke proved a synthetic low-risk candidate reached the explicit human
outcome; reviewer, outcome, and rationale were preserved; two identical calls
produced equal objects and equal deterministic JSON; project mismatch,
unsupported classification, unsafe governance, and high risk failed closed;
recursive promotion checks passed; neither real-proposal artifact appeared;
the before and after file sets were both empty; `.local` did not exist; and
the `HERMES_HOME` directory was not created.

Actual smoke result:

```json
{"deterministic_output": true, "explicit_human_decision": true, "hermes_home_created": false, "negative_boundaries": 4, "operator_smoke": "PASSED", "real_proposal_artifacts": 0, "runtime_files_created": 0}
```

## Limitations and unresolved HOLDs

This is a local, single-candidate, single-project, in-memory learning slice.
It does not classify or verify data sensitivity; the caller supplies the
classification assertion. It does not create a real proposal, persist a
human decision, adopt memory, recall memory, correct, revoke, delete, create a
tombstone, execute an action, serve an API, expose MCP or connector behavior,
or survive process restart.

The implementation does not resolve the broader R3/R4 material unknowns or
authorize the deferred control-plane lifecycle. Durable adoption,
persistence, privacy, authenticated roles, multi-project behavior, recovery,
external services, deployment, release, version, and tag authority remain
HOLD or absent according to their existing repository-effective boundaries.

## Repository-effective status boundary

The authorized implementation is complete on the required feature branch but
is unmerged. It is not repository-effective on main. No commit, PR, merge, or
tag was created by this task. The only allowed successor is the separately
authorized implementation commit-and-PR task.

## Machine-readable evidence

```text
TASK_ID=POST_IDG_R6_0_GOVERNED_MEMORY_LEARNING_SLICE_IMPLEMENTATION
BASE_COMMIT=1651729f62e3724254895e6246793ac8c95179a5
ALLOWED_WRITE_FILE_COUNT=3

R5_STATUS=COMPLETE
R5_AUTHORIZATION_DECISION=AUTHORIZED
IMPLEMENTATION_AUTHORITY=BOUNDED
IMPLEMENTATION_AUTHORITY_SCOPE=EXACT-R6_0-TASK-ONLY

AUTHORIZED_RUNTIME_SURFACE=governed_memory_learning_slice
PR357_REUSE_DISPOSITION=REFERENCE-ONLY-NO-CODE-TRANSFER

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

R6_0_BRANCH_STATUS=COMPLETE-UNMERGED
R6_0_REPOSITORY_EFFECTIVE=FALSE
R6_REPOSITORY_STATUS=NOT-STARTED-ON-MAIN

DURABLE_ADOPTION_AUTHORITY=NONE
PERSISTENT_STORAGE_AUTHORITY=NONE
EXTERNAL_SERVICE_AUTHORITY=NONE
DEPLOYMENT_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R6_0_IMPLEMENTATION_COMMIT_AND_PR
```
