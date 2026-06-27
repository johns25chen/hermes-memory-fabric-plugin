# Civilization Core P4-M0.2 Subspace Memory Manual Operator Commands

## Status

P4-M0.2 is human-authorized.

This document records the P4-M0.2 manual operator command boundary for the
Hermes Memory Fabric repository.

## Scope

P4-M0.2 adds manual operator commands for the local Subspace Memory store.

It supports:

- `propose`
- `approve`
- `reject`
- `recall`
- `audit`

It uses the existing local workspace store.

The default local workspace storage root remains:

```text
.local/subspace_memory/
```

The commands are intended for human-operated local use only.

## Manual Local Boundary

The command module uses the existing workspace resolver and factory for
`SubspaceMemoryStore`.

It is file-backed local operation only. Successful commands emit deterministic
JSON to standard output. Runtime validation errors are reported to standard
error with a nonzero exit code.

`recall` and `audit` are read operations over existing local records. They do
not create additional memory records.

## Non-Authorization

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

This does not auto-inject memory into agents.

This does not grant authorization semantics.

This does not grant execution semantics.

This does not change package version.

This does not tag.

This does not create v6.17.

## Final Boundary Statement

P4-M0.2 is manual local operator commands only. It makes the P4-M0 local
Subspace Memory store easier for a human to operate without adding product,
API, MCP, connector, deployment, autonomous writer, agent injection, full Memory
Graph, v6.17, or v7 semantics.
