# Civilization Core P4-M1.0 Human-Gated Memory Loop Checklist

P4-M1.0 is human-authorized.

P4-M1.0 is read-only checklist/status-report only.

P4-M1.0 implements the smallest safe first step from the readiness plan: a deterministic checklist of human gates and a deterministic status report.

## Boundary

P4-M1.0 does not write memory.

P4-M1.0 does not approve memory.

P4-M1.0 does not reject memory.

P4-M1.0 does not bulk import memory.

P4-M1.0 does not auto-ingest chat history.

P4-M1.0 does not auto-ingest files.

P4-M1.0 does not auto-ingest external systems.

P4-M1.0 does not inject memory into agents.

P4-M1.0 does not call Codex, Hermes, ChatGPT, or any agent.

P4-M1.0 does not call external APIs.

P4-M1.0 does not create MCP/connector behavior.

P4-M1.0 does not start v7.

P4-M1.0 does not create v6.17.

P4-M1.0 does not productize.

P4-M1.0 does not build MVP.

P4-M1.0 does not deploy.

P4-M1.0 does not create UI or Operator Console.

P4-M1.0 does not implement full Memory Graph.

P4-M1.0 does not grant authorization semantics.

P4-M1.0 does not grant execution semantics.

Package version remains 6.16.0.

No tag is created.

## Checklist Gates

1. `human-intent-requested`: human explicitly requests a memory-loop action.
2. `candidate-presented`: system presents a candidate proposal or checklist.
3. `human-content-review`: human reviews proposal/checklist content.
4. `human-approve-or-reject`: human explicitly approves or rejects using an existing/manual action.
5. `recall-verification`: human recall-verifies approved memory.
6. `lifecycle-optional`: human optionally sets lifecycle state.
7. `do-not-retry-optional`: human optionally sets do-not-retry.
8. `automation-boundary-confirmed`: human confirms no automation boundary was crossed.

## Status Report Contract

The P4-M1.0 status report is deterministic and read-only. It reports that memory writing, approval, rejection, bulk import, auto-ingest, agent calls, API/MCP/connector behavior, v7, and productization are disabled.

The report also states that package version remains 6.16.0.

## Operator Surface

The only P4-M1.0 operator surface is:

```text
memory-loop checklist
memory-loop checklist --format markdown
memory-loop checklist --format json
```

The command is read-only. It must not instantiate the workspace store and must not create `.local/subspace_memory`.

No write command is added in P4-M1.0.
