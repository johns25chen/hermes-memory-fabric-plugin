# Civilization Core P4-M0 Subspace Memory Minimal Runtime

## Status

P4-M0 minimal runtime is now authorized by human instruction.

This document records the first minimal local Subspace Memory runtime landing in
the Hermes Memory Fabric repository. It is an implementation boundary for P4-M0
only.

## What It Supports

The P4-M0 minimal runtime supports:

- memory proposal
- human approval
- human rejection
- approved-memory storage
- keyword recall from approved memories only
- project isolation
- namespace isolation
- append-only audit events
- explicit local storage root
- deterministic, explainable recall result structure
- Python standard-library operation only

## Runtime Boundary

The runtime is local and file-backed. It writes only the fixed JSONL files under
the storage root supplied to the store constructor:

- `proposals.jsonl`
- `memories.jsonl`
- `audit.jsonl`

Proposal is not approved memory. Rejected proposal is not recallable approved
memory. Approved memory can be recalled only after an explicit approval call.

## Non-Authorization

This P4-M0 minimal runtime does not start v7.

It is not productization.

It is not MVP.

It is not deployment.

It is not external project adoption.

It is not API, MCP, or connector operation.

It is not full Memory Graph.

It is not a benchmark runner.

It is not an evaluation runner.

It is not autonomous memory writing.

It does not auto-inject memory into agents.

It does not grant authorization semantics.

It does not grant execution semantics.

It does not tag.

It does not change package version.

It does not create v6.17.

## Final Boundary Statement

This file documents P4-M0 minimal runtime only. It does not claim full
Civilization Core memory platform capability.
