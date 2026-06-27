# Civilization Core P4-M0.4 Subspace Memory Lifecycle State

## Status

P4-M0.4 is human-authorized.

This document records the P4-M0.4 lifecycle-state addition for approved local Subspace Memory records.

## Scope

P4-M0.4 adds manual lifecycle state to approved local Subspace Memory records.

Supported lifecycle states are:

- `active`
- `stale`
- `archived`

New approved memories default to `active`.

Existing records without lifecycle are treated as `active`.

Lifecycle updates require explicit human/operator action.

Lifecycle changes are audit logged.

Default recall is active-only.

Stale recall requires an explicit manual include flag.

Archived recall requires an explicit manual include flag.

Recall pack export follows the same default: active-only unless explicit stale or archived include flags are passed.

The recall pack remains human-copyable Markdown only.

## Manual Governance Boundary

This is manual governance only.

This does not automatically judge truth.

This does not automatically judge freshness.

This does not automatically judge importance.

This does not automatically judge correctness.

This does not automatically judge quality.

This does not automatically detect stale memory.

This does not automatically archive.

This does not automatically delete.

This does not automatically clean memory.

This does not automatically rewrite memory.

This does not automatically rank memory.

This does not automatically suppress memory.

This does not perform AI evaluation.

Lifecycle updates require an explicit human/operator command input.

Lifecycle update does not create a new proposal.

Lifecycle update does not create a new memory.

Lifecycle update changes the existing approved memory record safely and deterministically.

## Non-Authorization Boundary

This does not grant authorization.

This does not grant execution semantics.

This is not automatic injection.

This does not auto-call any agent.

This does not auto-call Codex.

This does not auto-call Hermes.

This does not auto-call ChatGPT.

This does not auto-call any external or local agent.

This is not product CLI.

This is not API/MCP/connector.

This is not external project adoption.

This is not productization.

This is not MVP.

This is not deployment.

This is not UI or Operator Console.

This is not v7.

This is not full Memory Graph.

This does not change package version.

This does not tag.

This does not create v6.17.

## Implementation Boundary

P4-M0.4 is limited to local Subspace Memory lifecycle state for approved records.

The lifecycle values only describe manual operator handling state inside the local store.

The lifecycle values do not prove whether a memory is true, fresh, important, correct, or high quality.

Default recall excludes `stale` and `archived` records only because a human/operator set those states.

Explicit include flags are manual recall controls.

Explicit include flags are not agent authorization.

Explicit include flags are not automatic memory injection.

Explicit include flags are not product behavior.

No package version change is authorized by this document.

No tag is authorized by this document.

No v6.17 is authorized by this document.

No v7 is authorized by this document.
