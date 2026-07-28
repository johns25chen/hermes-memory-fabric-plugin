# Civilization Core R5 Bounded Implementation Authorization

## 1. Task Identity

TASK_ID=R5-BOUNDED-IMPLEMENTATION-AUTHORIZATION

AUTHORIZED_SUCCESSOR_SLICE=R6.0-MINIMUM-GOVERNED-MEMORY-LOOP-VERTICAL-SLICE

## 2. Authority Basis

R4_STATUS=COMPLETE

HUMAN_OWNER_IMPLEMENTATION_DECISION=AUTHORIZE-BOUNDED-IMPLEMENTATION

IMPLEMENTATION_AUTHORITY=BOUNDED

R5_STATUS=ACTIVE

R6_STATUS=NOT-STARTED

AUTOMATIC_SUCCESSOR_WORK=NONE

## 3. Authorized Objective

Authorize one minimal governed-memory control-plane vertical slice:

Source Record
→ Candidate Memory
→ Evidence Attachment
→ Human Review
→ Explicit Human Approval
→ Scoped Adoption
→ Auditable Record
→ Correction / Revocation / Deletion

The slice must preserve provenance, human authority, scope, lifecycle state,
and auditability.

## 4. Exact Allowed Write Set

Only these files may be created or modified during the R6.0 implementation task:

1. `src/hermes_memory_fabric/governed_memory_control_plane.py`
2. `tests/test_governed_memory_control_plane.py`
3. `docs/CIVILIZATION_CORE_R6_0_MINIMUM_GOVERNED_MEMORY_LOOP_IMPLEMENTATION_EVIDENCE.md`

ALLOWED_WRITE_FILE_COUNT=3

No other repository file is authorized.

## 5. Required Bounded Behaviors

The R6.0 slice may implement only:

- creation of a scoped candidate-memory record;
- attachment of traceable evidence;
- recording of a human review decision;
- explicit human approval before durable adoption;
- scoped recall of approved and active records;
- correction with preserved audit history;
- revocation that removes a record from active recall;
- deletion that removes durable content while retaining a non-content audit tombstone;
- read-only audit inspection.

## 6. Mandatory Safety Properties

- A candidate cannot adopt itself.
- Evidence cannot approve a candidate.
- A reviewer identity string alone is not authorization.
- Rejected candidates cannot enter active recall.
- Unapproved candidates cannot enter active recall.
- Revoked records cannot remain actively recallable.
- Deleted content cannot remain durably retrievable.
- Audit inspection cannot mutate state.
- No hidden or automatic durable adoption is permitted.
- No automatic execution follows memory adoption.

## 7. Forbidden Write Set

The R6.0 task must not modify:

- `pyproject.toml`;
- package version files;
- dependency or lock files;
- existing source modules;
- existing tests;
- repository configuration;
- GitHub workflow files;
- API, MCP, Connector, Agent, UI, deployment, release, or migration files;
- `.codex/`;
- `AGENTS.md`;
- `AGENTS.override.md`;
- `uv.lock`.

## 8. Forbidden Capabilities

The R6.0 task must not create:

- autonomous approval;
- authorization inference;
- automatic durable memory writes;
- automatic execution;
- network access;
- external API calls;
- adapters or connectors;
- databases or migrations;
- multi-tenant or cross-organization behavior;
- production deployment;
- V7 runtime identity;
- version bump, tag, or release.

## 9. Exact Validation Scope

Required focused tests:

1. `tests/test_governed_memory_control_plane.py`
2. `tests/test_p4_m0_subspace_operator.py`
3. `tests/test_memory_fabric_bridge.py`
4. `tests/test_p4_m2_execution_decision_negative_evidence_non_override_map.py`

Full test suite is not authorized.

Required validation:

- Python syntax validation for the exact allowed Python files;
- exact four-file focused pytest run;
- deterministic temporary-workspace operator smoke;
- read-only audit no-mutation check;
- rejected candidate not recalled;
- unapproved candidate not recalled;
- approved candidate recalled only within scope;
- revoked candidate no longer recalled;
- deleted content unavailable while audit tombstone remains;
- clean repository scope check.

## 10. Operator Smoke Sequence

The bounded smoke must execute:

1. create source;
2. create candidate;
3. attach evidence;
4. record human review;
5. approve explicitly;
6. adopt within one scope;
7. recall within that scope;
8. revoke;
9. confirm recall absence;
10. delete durable content;
11. confirm content absence;
12. confirm non-content audit tombstone;
13. confirm audit inspection is read-only.

## 11. Implementation-Agent Restrictions

The R6.0 implementation agent may implement and validate only.

It must not:

- commit;
- push;
- create a pull request;
- merge;
- tag;
- change version;
- expand the allowed write set;
- run the full test suite.

## 12. Stop Conditions

Stop immediately if:

- any file outside the allowed write set changes;
- an existing source or test file requires modification;
- a dependency appears necessary;
- an API, adapter, migration, or network integration appears necessary;
- authorization semantics cannot remain explicit and human-controlled;
- any focused test fails;
- the repository contains an unexpected forbidden artifact;
- scope expansion appears necessary.

## 13. Rollback Boundary

Rollback consists only of removing or reverting the three authorized files.

No migration, external state, version change, deployment, or release rollback
is permitted or required.

## 14. R5 Exit State

IMPLEMENTATION_CHARTER=APPROVED-UPON-MERGE

ALLOWED_WRITE_SET=FIXED

FORBIDDEN_WRITE_SET=FIXED

ACCEPTANCE_TESTS=FIXED

STOP_CONDITIONS=FIXED

R5_STATUS=COMPLETE-UPON-MERGE

R6_ELIGIBILITY=ESTABLISHED-UPON-R5-MERGE

R6_STATUS=NOT-STARTED

R6_AUTOMATIC_START=NO

IMPLEMENTATION_AUTHORITY=BOUNDED

AUTOMATIC_SUCCESSOR_WORK=NONE
