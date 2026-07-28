# Civilization Core R6.0 Minimum Governed Memory Loop Implementation Evidence

## 1. Task Identity and Boundary

TASK_ID=R6.0-MINIMUM-GOVERNED-MEMORY-LOOP-VERTICAL-SLICE

BASE_COMMIT=82366e9b8d3c3b0c41e07153b072712ca7b19898

BRANCH=feat/civilization-core-r6-0-minimum-governed-memory-loop

PACKAGE_VERSION=6.16.0

IMPLEMENTATION_AUTHORITY=BOUNDED

The exact authorized write set is:

1. `src/hermes_memory_fabric/governed_memory_control_plane.py`
2. `tests/test_governed_memory_control_plane.py`
3. `docs/CIVILIZATION_CORE_R6_0_MINIMUM_GOVERNED_MEMORY_LOOP_IMPLEMENTATION_EVIDENCE.md`

No dependency, lock, package-initialization, API, MCP, connector, adapter,
migration, workflow, deployment, version, or release file was changed.

## 2. Source Implementation Summary

The implementation is a workspace-local control plane backed by deterministic
JSON state at
`.local/governed_memory_control_plane/state.json` beneath an explicitly
provided workspace root. It uses atomic temporary-file replacement for state
writes and does not create storage during fresh read operations.

Runtime imports are limited to the Python standard library: `json`, `os`,
`dataclasses`, `pathlib`, `typing`, and `__future__`.

Returned records are frozen dataclasses. Sequential source, candidate,
evidence, review, memory, and audit identifiers are persisted in state and
remain stable after control-plane restart.

## 3. Public Records and Control-Plane Surfaces

Public immutable record types:

- `SourceRecord`
- `CandidateMemory`
- `EvidenceAttachment`
- `HumanReview`
- `AdoptedMemory`
- `AuditEvent`
- `DeletionTombstone`

Public error types:

- `GovernedMemoryError`
- `NotFoundError`
- `InvalidTransitionError`
- `AuthorizationError`
- `ScopeError`

Public control-plane surfaces:

- `state_path`
- `create_source`
- `create_candidate`
- `attach_evidence`
- `record_human_review`
- `approve_candidate`
- `adopt_candidate`
- `recall`
- `correct_memory`
- `revoke_memory`
- `delete_memory`
- `get_tombstone`
- `list_audit_events`

## 4. Lifecycle and Authorization Semantics

The implemented lifecycle is:

`source -> pending candidate -> evidence -> human review -> explicit human
approval -> exact-scope adoption -> active memory -> correction or revocation
-> deletion tombstone`

Evidence attachment does not approve a candidate. An approve review does not
authorize adoption. `approve_candidate` requires a non-empty human approver,
prior evidence, a prior approve review, and the exact
`EXPLICIT_HUMAN_APPROVAL` confirmation value. Adoption before that separate
approval raises `AuthorizationError`.

Rejected candidates cannot be approved or adopted. Adoption scope must equal
candidate scope exactly. A candidate identifier cannot act as its own adoption
actor. Adoption performs no automatic execution.

## 5. Recall, Correction, Revocation, and Deletion

Recall returns an immutable tuple of frozen `AdoptedMemory` records ordered by
memory identifier. Matching is case-insensitive, active-only, and requires an
exact scope match. Pending, reviewed-but-unapproved, approved-but-unadopted,
rejected, revoked, and deleted records are not recalled.

Correction replaces active memory content, preserves the memory identity and
scope, increments the revision, and appends an audit record without old or new
memory-content fields.

Revocation immediately changes an active memory to `revoked`, removing it from
active recall.

Deletion removes the durable memory record, clears candidate-memory content,
and retains a frozen tombstone containing identifiers, scope, final revision,
actor, and reason but no content field. The observed state JSON, tombstone, and
audit records did not contain the deleted smoke-test content.

Audit and tombstone inspection are read-only. Observed audit inspection changed
no state bytes, nanosecond mtime, counters, or event count.

## 6. Validation Evidence

Actual interpreter:

`/Users/han/hermes-memory-fabric-plugin/.venv/bin/python`

Python version: `3.12.11`

Pytest version: `9.0.3`

Syntax command:

```text
.venv/bin/python -m py_compile \
  src/hermes_memory_fabric/governed_memory_control_plane.py \
  tests/test_governed_memory_control_plane.py
```

Observed result: exit code `0`.

Focused test command:

```text
.venv/bin/python -m pytest -q \
  tests/test_governed_memory_control_plane.py \
  tests/test_p4_m0_subspace_operator.py \
  tests/test_memory_fabric_bridge.py \
  tests/test_p4_m2_execution_decision_negative_evidence_non_override_map.py
```

Observed result: `85 passed in 0.73s`, exit code `0`.

The deterministic fresh-temporary-workspace operator smoke passed all required
steps: fresh reads without storage; source, candidate, evidence, and approve
review creation; adoption rejection before explicit approval; explicit human
approval; exact-scope adoption; restart persistence and deterministic IDs;
case-insensitive exact-scope recall; correction with revision increment; audit
byte, mtime, counter, and event-count stability; revocation; deletion; deleted
content absence from state JSON; and retention of a non-content tombstone.

The pre-evidence repository-scope guard observed the exact branch and baseline,
package version `6.16.0`, no staged files, only the two then-created authorized
Python paths, no `uv.lock`, no repository `.codex`, no tag at `HEAD`, and zero
commits after the baseline. The final exact-three-file scope result is recorded
in the markers after the post-document guard.

## 7. Limitations

- This is a bounded, local, single-workspace control-plane slice, not a
  production multi-user or distributed memory service.
- Human actors are explicit non-empty strings and the confirmation is an exact
  control value; this slice does not create an identity, authentication, role,
  permission, or external approval system.
- There is no API, MCP, connector, adapter, database, migration, network
  access, autonomous approval, automatic memory adoption, or automatic
  execution.
- Concurrent multi-process mutation and production deployment behavior are
  outside this authorized slice.
- No full repository test suite was run because it was outside the authorized
  validation scope.

## 8. Final Markers

TASK_ID=R6.0-MINIMUM-GOVERNED-MEMORY-LOOP-VERTICAL-SLICE
BASE_COMMIT=82366e9b8d3c3b0c41e07153b072712ca7b19898
ALLOWED_WRITE_FILE_COUNT=3
IMPLEMENTATION_AUTHORITY=BOUNDED
PYTHON_SYNTAX_VALIDATION=PASSED
FOCUSED_TEST_SUITE=PASSED
OPERATOR_SMOKE=PASSED
AUDIT_READ_ONLY_CHECK=PASSED
REJECTED_NOT_RECALLED=PASSED
UNAPPROVED_NOT_RECALLED=PASSED
EXACT_SCOPE_RECALL=PASSED
REVOCATION_REMOVES_RECALL=PASSED
DELETION_REMOVES_CONTENT=PASSED
NON_CONTENT_TOMBSTONE_RETAINED=PASSED
REPOSITORY_SCOPE_CHECK=PASSED
PACKAGE_VERSION_LOCKED_AT_6.16.0=PASSED
NO_UV_LOCK=PASSED
NO_REPO_CODEX=PASSED
NO_TAG_CREATED=PASSED
NO_COMMIT_CREATED=PASSED
R6_0_STATUS=IMPLEMENTED_AND_VALIDATED
AUTOMATIC_SUCCESSOR_WORK=NONE
