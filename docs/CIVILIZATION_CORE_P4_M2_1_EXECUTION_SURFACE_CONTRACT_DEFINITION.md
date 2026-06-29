# Civilization Core P4-M2.1 Execution Surface Contract Definition

P4-M2.1 is human-authorized.

P4-M2.x is Manual Decision Execution Hardening.

P4-M2.1 is Execution Surface Contract Definition.

P4-M2.1 defines a future controlled execution surface contract/schema/trace boundary.

P4-M2.1 is read-only.

P4-M2.1 is inspection-only.

P4-M2.1 is not P4-M3.

P4-M2.1 defines execution surface fields, execution contract schema fields, execution trace fields, inspection-only validation signals, prohibited semantics, and blocking signals.

P4-M2.1 does not execute decisions.

P4-M2.1 does not create a manual execution command.

P4-M2.1 does not create an execute command.

P4-M2.1 does not recommend a decision.

P4-M2.1 does not rank decisions.

P4-M2.1 does not automatically determine readiness.

P4-M2.1 does not emit an automatic readiness verdict.

P4-M2.1 does not make decisions.

P4-M2.1 does not approve memory.

P4-M2.1 does not reject memory.

P4-M2.1 does not approve proposals.

P4-M2.1 does not reject proposals.

P4-M2.1 does not write memory.

P4-M2.1 does not create memory records.

P4-M2.1 does not update memory records.

P4-M2.1 does not delete memory records.

P4-M2.1 does not mutate proposal records.

P4-M2.1 does not mutate lifecycle records.

P4-M2.1 does not mutate do-not-retry guard state.

P4-M2.1 does not mutate retry policy.

P4-M2.1 does not fetch sources.

P4-M2.1 does not browse the web.

P4-M2.1 does not call external APIs.

P4-M2.1 does not call connectors.

P4-M2.1 does not create API/MCP/connector behavior.

P4-M2.1 does not automatically trust a source.

P4-M2.1 does not write provenance.

P4-M2.1 does not mutate source/provenance/evidence/citation records.

P4-M2.1 does not inject memory into agents.

P4-M2.1 does not bulk import memory.

P4-M2.1 does not auto-ingest chat history.

P4-M2.1 does not auto-ingest files.

P4-M2.1 does not auto-ingest external systems.

P4-M2.1 does not call Codex, Hermes, ChatGPT, or any agent from product code.

P4-M2.1 does not start P4-M3.

P4-M2.1 does not start P4-M4.

P4-M2.1 does not start P4-M5.

P4-M2.1 does not start v7.

P4-M2.1 does not create v6.17.

P4-M2.1 does not productize.

P4-M2.1 does not build MVP.

P4-M2.1 does not deploy.

P4-M2.1 does not create UI or Operator Console.

P4-M2.1 does not implement full Memory Graph.

P4-M2.1 does not grant authorization semantics.

P4-M2.1 does not grant execution semantics.

Package version remains 6.16.0.

No tag is created.

## Roadmap Guard

P4-M2.1 defines execution surface contract/schema/trace fields only.

Later P4-M2.x may add explicit human-authorized execution paths, but P4-M2.1 does not add them.

P4-M3.x may later harden local governance stability.

P4-M4.x may later prepare cross-project memory governance.

P4-M5.x may later audit connector/API/MCP readiness only.

v7/productization/UI/Operator Console must not start in P4-M2.1.

## Operator Surface

`memory-loop execution-surface-contract` is read-only and returns Markdown by default.

`memory-loop execution-surface-contract --format json` is read-only and returns deterministic JSON with `status`, `count`, `fields`, and `boundary`.

The operator command does not instantiate the workspace store and does not create `.local/subspace_memory`.
