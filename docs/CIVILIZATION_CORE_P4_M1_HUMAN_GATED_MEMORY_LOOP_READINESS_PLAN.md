# Civilization Core P4-M1 Human-Gated Memory Loop Readiness Plan

## Status

This is a docs-only readiness plan.

This document does not implement P4-M1.

The package version remains `6.16.0`.

No tag is created.

P4-M1 is not started by this PR.

## Context From P4-M0

The completed P4-M0 chain establishes the local, manual, human-governed memory base that any later P4-M1 work must preserve.

P4-M0 added the minimal local JSONL memory runtime.

P4-M0.1 added the local workspace store.

P4-M0.2 added manual operator commands.

P4-M0.3 added recall pack export.

P4-M0.4 added lifecycle state.

P4-M0.5 added explainable recall trace.

P4-M0.6 added do-not-retry guard.

P4-M0.7 added project memory seed candidates.

P4-M0.8 added the seed approval runbook.

## P4-M1 Purpose

P4-M1 is a future human-gated memory loop.

The future loop may connect human intent, candidate memory proposal, explicit review, explicit approval or rejection, recall verification, lifecycle governance, and do-not-retry governance when needed.

P4-M1 is not autonomous memory.

P4-M1 must preserve the human as the approving actor.

P4-M1 must preserve manual recall verification as a separate action.

P4-M1 must preserve lifecycle governance as explicit human-controlled state.

P4-M1 must preserve do-not-retry governance as explicit human-controlled state.

## P4-M1 Allowed Scope

P4-M1 may later introduce:

- a human-visible loop checklist
- a proposal review step
- a recall verification step
- a manual approval/rejection step
- deterministic loop state reporting
- manual runbook-based operator guidance
- read-only diagnostics
- no automatic write unless a human explicitly performs an existing write command

Allowed future P4-M1 behavior must remain local, deterministic, and human-gated.

Allowed future P4-M1 behavior must not treat readiness planning as implementation authorization.

## P4-M1 Prohibited Scope

P4-M1 must not:

- auto-write approved memory
- auto-approve memory
- auto-reject memory
- bulk import memory
- auto-ingest chat history
- auto-ingest files
- auto-ingest external systems
- inject memory into agents automatically
- call Codex, Hermes, ChatGPT, or any agent automatically
- call external APIs
- create MCP connector behavior
- start v7
- create v6.17
- productize
- build MVP
- deploy
- create UI
- create Operator Console
- implement full Memory Graph
- add dependencies
- change package version
- create tag
- grant authorization
- grant execution semantics

These prohibitions apply to this readiness plan and to the smallest future P4-M1 first step unless the human explicitly replaces the boundary in a later task.

## Human Gates

P4-M1 requires these human gates:

1. Gate 1: human requests memory-loop action.
2. Gate 2: system presents candidate proposal or checklist.
3. Gate 3: human reviews proposal content.
4. Gate 4: human explicitly approves or rejects.
5. Gate 5: human recall-verifies approved memory.
6. Gate 6: human optionally sets lifecycle state.
7. Gate 7: human optionally sets do-not-retry.
8. Gate 8: human confirms no automation boundary was crossed.

No gate may be inferred from silence.

No gate may be satisfied by an automatic agent action.

No gate may authorize behavior outside the exact approved scope.

## Smallest Safe Future P4-M1 First Step

The smallest safe future P4-M1.0 candidate is `P4-M1.0 Human-Gated Memory Loop Checklist`.

This section describes a future candidate only.

This document does not implement P4-M1.0.

P4-M1.0 should be docs or read-only command only.

P4-M1.0 should produce a checklist and status report.

P4-M1.0 should not write memory.

P4-M1.0 should not approve memory.

P4-M1.0 should not reject memory.

P4-M1.0 should not call agents.

P4-M1.0 should not add API/MCP/connector behavior.

P4-M1.0 should not add dependencies.

P4-M1.0 should not change package version.

P4-M1.0 should not create tag.

## Readiness Criteria Before Any P4-M1 Code

Before any P4-M1 code begins:

- P4-M0.8 is merged on main
- tests are passing
- version remains `6.16.0`
- no `uv.lock` exists
- main is not dirty
- no P4-M1 implementation exists yet
- human approves the exact P4-M1.0 scope
- first P4-M1.0 must be read-only or manual-only
- all write operations remain explicit human commands

Readiness criteria are prerequisites only.

Readiness criteria do not grant implementation authorization by themselves.

## Validation Plan For Future P4-M1

Future P4-M1 validation must prove no automatic approval.

Future P4-M1 validation must prove no automatic approved memory write.

Future P4-M1 validation must prove no bulk import.

Future P4-M1 validation must prove no agent call.

Future P4-M1 validation must prove no API/MCP/connector behavior.

Future P4-M1 validation must prove no version change.

Future P4-M1 validation must prove no tag.

Future P4-M1 validation must prove no `uv.lock`.

Future P4-M1 validation must prove recall trace still works.

Future P4-M1 validation must prove lifecycle remains manual.

Future P4-M1 validation must prove do-not-retry remains manual.

Future P4-M1 validation must include a changed-file surface check.

Future P4-M1 validation must include explicit checks that README, `pyproject.toml`, dependency files, source files outside the approved scope, and test files outside the approved scope remain untouched.

## Boundary Statement

This document is not P4-M1 implementation.

This document is not v7.

This document is not productization.

This document is not an operator console.

This document is not a memory graph.

This document is not automation authorization.

This document is readiness planning only.
