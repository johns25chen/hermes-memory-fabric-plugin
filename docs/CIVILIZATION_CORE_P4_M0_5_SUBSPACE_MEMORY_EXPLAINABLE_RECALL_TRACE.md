# Civilization Core P4-M0.5 Subspace Memory Explainable Recall Trace

## Status

P4-M0.5 is human-authorized.

This document records a narrow Subspace Memory implementation increment only: deterministic explainable recall trace for approved local recall results.

## Purpose

P4-M0.5 adds deterministic explainable recall trace.

The trace explains why a memory was recalled.

The trace is:

```text
recall result -> deterministic trace -> human-readable explanation
```

The trace explains matching mechanics only.

## Trace Inputs

Trace is based on query terms, matched terms, score, rank, project, namespace, source, and lifecycle.

Each included recall result can expose:

- query
- query terms
- matched terms
- score
- rank
- memory id
- project
- namespace
- source
- lifecycle
- include stale flag
- include archived flag
- deterministic explanation

The deterministic explanation is derived only from the query terms that matched the recalled memory content.

## Lifecycle Preservation

Trace preserves P4-M0.4 lifecycle behavior.

Default recall remains active-only.

Stale recall still requires an explicit include flag.

Archived recall still requires an explicit include flag.

Trace explains included results only.

Trace does not make stale or archived memories visible by default.

## Read-Only Boundary

Trace generation is read-only.

Trace generation does not create proposals.

Trace generation does not create memories.

Trace generation does not write audit events.

Trace generation does not mutate storage.

Trace generation does not call any external or local agent.

Trace generation does not perform online research.

## Non-Evaluation Boundary

Trace is not AI evaluation.

Trace is not truth judgment.

Trace is not freshness judgment.

Trace is not quality judgment.

Trace is not automatic scoring optimization.

Trace is not benchmark runner.

Trace is not evaluation runner.

Trace does not add AI scoring.

Trace does not add freshness scoring.

Trace does not add quality scoring.

Trace does not add truth scoring.

## Authorization Boundary

Trace does not grant authorization.

Trace does not grant execution semantics.

Trace does not approve an action.

Trace does not authorize an action.

Trace does not start autonomous memory writing.

Trace does not start automatic lifecycle judgment.

Trace does not auto-archive, auto-delete, auto-clean, or auto-suppress memories.

## Injection and Agent Boundary

This is not automatic injection.

This does not auto-call any agent.

This does not auto-call Codex.

This does not auto-call Hermes.

This does not auto-call ChatGPT.

This does not write prompts into agents automatically.

Recall pack output remains human-copyable context only.

## Product Boundary

This is not product CLI.

This is not API/MCP/connector.

This is not external project adoption.

This is not productization.

This is not MVP.

This is not deployment.

This is not UI or Operator Console.

This does not add console scripts.

This does not add pyproject entry points.

This does not add dependencies.

## Version Boundary

This is not v7.

This is not full Memory Graph.

This does not change package version.

This does not tag.

This does not create v6.17.

The package version remains sealed at `6.16.0`.

## Final Statement

P4-M0.5 adds deterministic explainable recall trace only.

It explains why included recall results matched a query using local matching mechanics.

It does not judge truth, freshness, quality, importance, or correctness.

It does not optimize scoring.

It does not create durable memory, proposals, audit events, agents, APIs, connectors, UI, deployment, product surface, v6.17, or v7.
