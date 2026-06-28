# Civilization Core P4-M1.7 Manual Decision Preview

P4-M1.7 is human-authorized.

P4-M1.7 is read-only manual decision preview only.

P4-M1.7 is advisory only.

P4-M1.7 is for human inspection only.

P4-M1.7 combines P4-M1.0 through P4-M1.6 status surfaces into one manual preview frame.

P4-M1.7 does not recommend a decision.

P4-M1.7 does not rank decisions.

P4-M1.7 does not automatically determine readiness.

P4-M1.7 does not emit an automatic readiness verdict.

P4-M1.7 does not make decisions.

P4-M1.7 does not execute decisions.

P4-M1.7 does not approve memory.

P4-M1.7 does not reject memory.

P4-M1.7 does not approve proposals.

P4-M1.7 does not reject proposals.

P4-M1.7 does not write memory.

P4-M1.7 does not create memory records.

P4-M1.7 does not update memory records.

P4-M1.7 does not delete memory records.

P4-M1.7 does not mutate proposal records.

P4-M1.7 does not mutate lifecycle records.

P4-M1.7 does not mutate do-not-retry guard state.

P4-M1.7 does not mutate retry policy.

P4-M1.7 does not fetch sources.

P4-M1.7 does not browse the web.

P4-M1.7 does not call external APIs.

P4-M1.7 does not call connectors.

P4-M1.7 does not create API/MCP/connector behavior.

P4-M1.7 does not automatically trust a source.

P4-M1.7 does not write provenance.

P4-M1.7 does not mutate source/provenance/evidence/citation records.

P4-M1.7 does not inject memory into agents.

P4-M1.7 does not bulk import memory.

P4-M1.7 does not auto-ingest chat history.

P4-M1.7 does not auto-ingest files.

P4-M1.7 does not auto-ingest external systems.

P4-M1.7 does not call Codex, Hermes, ChatGPT, or any agent from product code.

P4-M1.7 does not start v7.

P4-M1.7 does not create v6.17.

P4-M1.7 does not productize.

P4-M1.7 does not build MVP.

P4-M1.7 does not deploy.

P4-M1.7 does not create UI or Operator Console.

P4-M1.7 does not implement full Memory Graph.

P4-M1.7 does not grant authorization semantics.

P4-M1.7 does not grant execution semantics.

Package version remains 6.16.0.

No tag is created.

## Scope

P4-M1.7 lands a deterministic Manual Decision Preview layer for human inspection before any later manual decision.

The preview layer exposes ten static preview frames, disabled automation flags, and a boundary statement. It does not inspect live stores, fetch sources, call agents, connect external systems, derive a recommendation, rank options, emit a readiness verdict, approve, reject, execute, or mutate state.

## Preview Frames

1. `checklist-preview`: shows the P4-M1.0 checklist frame before any later manual decision.
2. `proposal-review-preview`: shows the P4-M1.1 proposal review frame before any later manual decision.
3. `recall-verification-preview`: shows the P4-M1.2 recall verification frame before any later manual decision.
4. `lifecycle-verification-preview`: shows the P4-M1.3 lifecycle verification frame before any later manual decision.
5. `do-not-retry-preview`: shows the P4-M1.4 do-not-retry verification frame before any later manual decision.
6. `source-provenance-preview`: shows the P4-M1.5 source/provenance verification frame before any later manual decision.
7. `decision-readiness-preview`: shows the P4-M1.6 decision readiness frame before any later manual decision.
8. `unified-human-review-frame`: shows the unified human review frame across P4-M1.0 through P4-M1.6.
9. `decision-not-recommended`: states that no decision recommendation, approval, rejection, execution, or memory write is produced.
10. `automation-boundary-intact`: proves disabled decision recommendation, readiness verdict, execution, approval, rejection, write, mutation, import, ingest, injection, agent, API/MCP/connector, v7, and productization flags.

## Roadmap Guard

P4-M1.7 lands manual decision preview only.

P4-M1.8 should be Governance Pack Export.

P4-M1.9 should be P4-M1 Final Boundary Audit / Closure.

P4-M2.x may later harden manual decision execution.

P4-M3.x may later harden local governance stability.

P4-M4.x may later prepare cross-project memory governance.

P4-M5.x may later audit connector/API/MCP readiness only.

v7/productization/UI/Operator Console must not start in P4-M1.7.
