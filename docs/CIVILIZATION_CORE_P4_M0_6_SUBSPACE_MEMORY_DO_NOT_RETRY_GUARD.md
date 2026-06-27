# Civilization Core P4-M0.6 Subspace Memory Do-Not-Retry Guard

## Status

P4-M0.6 is human-authorized.

This document records a narrow Subspace Memory implementation increment only: human-governed do-not-retry warning metadata for approved local Subspace Memory records.

## Purpose

P4-M0.6 adds human-governed do-not-retry warning metadata.

It lets an approved memory warn a human operator:

```text
This was tried before.
It failed or should not be repeated.
Do not retry unless a human explicitly decides otherwise.
Here is the reason.
Here is the alternative guidance.
```

This is advisory recall context only.

## Manual Metadata

P4-M0.6 can mark an approved memory as do-not-retry.

P4-M0.6 can clear do-not-retry metadata.

The mark and clear actions are manual operator actions.

The metadata can include:

- enabled flag
- reason
- optional alternative guidance
- actor
- updated timestamp

## Recall Warning

Recall can carry do-not-retry warning metadata when an approved memory has been manually marked.

Recall can expose a deterministic advisory warning string.

Recall does not suppress do-not-retry memories.

Recall does not change deterministic scoring.

Recall does not change deterministic recall ordering.

Recall does not automatically decide whether a memory should be retried.

## Lifecycle Preservation

P4-M0.6 preserves P4-M0.4 lifecycle behavior.

Default recall remains active-only.

Stale recall still requires an explicit include flag.

Archived recall still requires an explicit include flag.

Do-not-retry metadata does not make stale or archived memories visible by default.

## Explainable Trace Preservation

P4-M0.6 preserves P4-M0.5 explainable recall trace.

Explainable trace remains present when do-not-retry warning metadata is present.

Do-not-retry warning metadata does not replace trace metadata.

Do-not-retry warning metadata does not alter trace rank.

Do-not-retry warning metadata does not alter trace explanation.

## Advisory Boundary

This is advisory recall context only.

Do-not-retry metadata does not automatically detect failures.

Do-not-retry metadata does not infer failures.

Do-not-retry metadata does not automatically mark do-not-retry.

Do-not-retry metadata does not automatically block execution.

Do-not-retry metadata does not automatically approve actions.

Do-not-retry metadata does not automatically reject actions.

Do-not-retry metadata does not enforce policy.

It is not a safety policy engine.

It is not AI evaluation.

It is not truth judgment.

It is not freshness judgment.

It is not quality judgment.

It is not automatic score optimization.

It is not benchmark runner.

It is not evaluation runner.

## Authorization Boundary

Do-not-retry metadata does not grant authorization.

Do-not-retry metadata does not grant execution semantics.

Do-not-retry metadata does not approve an action.

Do-not-retry metadata does not authorize an action.

Do-not-retry metadata does not start autonomous memory writing.

Do-not-retry metadata does not auto-archive, auto-delete, auto-clean, or auto-suppress memories.

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

P4-M0.6 adds human-governed do-not-retry warning metadata only.

It records and recalls human-provided warning context for approved local Subspace Memory records.

It does not automatically detect failures, infer failures, mark do-not-retry, block execution, approve, reject, enforce policy, judge truth, judge freshness, judge quality, optimize scoring, run benchmarks, run evaluation, create durable autonomous memory writing, inject memory into agents, call agents, create APIs, create connectors, create UI, deploy, productize, create v6.17, or start v7.
