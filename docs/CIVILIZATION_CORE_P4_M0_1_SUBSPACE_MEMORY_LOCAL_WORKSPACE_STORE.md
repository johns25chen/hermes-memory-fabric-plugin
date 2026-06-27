# Civilization Core P4-M0.1 Subspace Memory Local Workspace Store

## Status

P4-M0.1 is human-authorized.

This document records the P4-M0.1 local workspace store boundary for the Hermes
Memory Fabric repository.

## Scope

P4-M0.1 extends P4-M0 by adding a local workspace storage resolver and factory
for the existing `SubspaceMemoryStore`.

The default local workspace storage root is:

```text
.local/subspace_memory/
```

The storage directory itself is local runtime data and must not be committed.

## Local Workspace Store Boundary

The P4-M0.1 helper requires an explicit workspace root. The workspace root must
exist and must be a directory.

The storage directory must be relative. Absolute storage directories are
rejected. Parent-directory escape through `..` is rejected. The resolved storage
root must stay inside the workspace root.

The factory returns the existing P4-M0 `SubspaceMemoryStore` using the resolved
local workspace storage root.

## Non-Authorization

This is not CLI.

This is not API, MCP, or connector.

This is not external project adoption.

This is not productization.

This is not MVP.

This is not deployment.

This is not v7.

This is not full Memory Graph.

This is not autonomous memory writing.

This does not auto-inject memory into agents.

This does not change package version.

This does not tag.

This does not create v6.17.

## Final Boundary Statement

P4-M0.1 is local workspace store resolution only. It makes the P4-M0 local
runtime practically usable under a repo-local `.local/subspace_memory/` storage
root without adding product, API, MCP, connector, deployment, autonomous writer,
agent injection, full Memory Graph, v6.17, or v7 semantics.
