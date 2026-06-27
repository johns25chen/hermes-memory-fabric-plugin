# Civilization Core P4-M0.3 Subspace Memory Recall Pack Export

## Status

P4-M0.3 is human-authorized.

This document records the P4-M0.3 recall pack export boundary for the Hermes
Memory Fabric repository.

## Scope

P4-M0.3 exports local recall results into a human-copyable context pack.

The flow is:

```text
recall -> format -> export human-copyable context pack
```

It uses the existing local workspace store.

It uses approved recalled memories only.

The default local workspace storage root remains:

```text
.local/subspace_memory/
```

The context pack is intended for manual paste into Codex, Hermes, ChatGPT, or
another human-operated reasoning session.

## Manual Export Boundary

The export module uses the existing workspace resolver and factory for
`SubspaceMemoryStore`.

The default export target is standard output. An optional output file is only a
human-specified destination for the same deterministic context pack.

The export formats existing approved recall results as Markdown/text suitable
for copy and paste. It creates no proposals, creates no memories, approves no
records, rejects no records, and adds no authorization or execution meaning.

## Non-Authorization

This is not automatic injection.

This does not auto-call any agent.

This does not write prompts into agents.

This does not grant authorization.

This does not grant authorization semantics.

This does not grant execution semantics.

This is not product CLI.

This is not API, MCP, or connector.

This is not external project adoption.

This is not productization.

This is not MVP.

This is not deployment.

This is not UI or Operator Console.

This is not v7.

This is not full Memory Graph.

This is not autonomous memory writing.

This does not change package version.

This does not tag.

This does not create v6.17.

## Final Boundary Statement

P4-M0.3 is recall pack export only. It lets a human copy approved local recall
results into another reasoning session without adding product, API, MCP,
connector, deployment, autonomous writer, agent injection, full Memory Graph,
v6.17, or v7 semantics.
