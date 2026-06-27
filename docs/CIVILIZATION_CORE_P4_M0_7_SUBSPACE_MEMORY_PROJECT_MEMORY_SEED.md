# Civilization Core P4-M0.7 Subspace Memory Project Memory Seed

## Status

P4-M0.7 is human-authorized.

This document records a narrow Subspace Memory implementation increment only: deterministic project memory seed candidates for Civilization Core project self-context.

## Purpose

P4-M0.7 adds deterministic project memory seed candidates.

It allows human inspection of seed candidates.

It allows manual proposal of exactly one seed at a time.

It does not automatically approve seeds.

It does not automatically write approved memory.

It does not bulk import.

It does not auto-inject memory into agents.

## Seed Scope

Project memory seed candidates cover:

- project identity
- project boundary
- version route
- P4-M0 chain status
- human-gated memory flow
- no-v7-before-authorization rule
- no-productization boundary
- operator discipline and validation preference

The seed list is deterministic.

The seed pack is human-provided context only.

## Manual Proposal Boundary

P4-M0.7 may propose one selected seed as one pending proposal through a manual operator command.

Proposal requires an explicit seed id.

Proposal requires an explicit actor.

Proposal preserves seed project, namespace, content, source lineage, tags, and confidence.

Proposal does not approve the seed.

Proposal does not create an approved memory record.

Proposal does not alter lifecycle directly.

Proposal does not set do-not-retry.

Proposal does not call recall.

Approval remains a separate human action through the existing approve command.

## Read-Only Boundary

Seed list is read-only.

Seed show is read-only.

Seed pack render is read-only.

Seed list does not create storage files.

Seed show does not create storage files.

Seed pack render does not create storage files.

Module import does not write files.

Test collection does not write seed memory.

Recall does not create seed proposals.

## Approval and Write Boundary

P4-M0.7 does not automatically approve seeds.

P4-M0.7 does not automatically write approved memory.

P4-M0.7 does not create durable approved memories during import, install, test collection, module import, operator list, operator show, operator pack, or recall.

The only P4-M0.7 write behavior is the explicit manual operator command that proposes exactly one selected seed as a pending proposal.

Approved memory creation remains separate and requires the existing approve command.

## Agent Boundary

P4-M0.7 does not call Codex.

P4-M0.7 does not call Hermes.

P4-M0.7 does not call ChatGPT.

P4-M0.7 does not call any agent.

P4-M0.7 does not write prompts into agents automatically.

P4-M0.7 does not auto-inject memory into agents.

## Authorization Boundary

P4-M0.7 does not grant authorization.

P4-M0.7 does not grant execution semantics.

P4-M0.7 does not approve memory.

P4-M0.7 does not authorize execution.

P4-M0.7 does not enforce policy.

P4-M0.7 is not a safety policy engine.

## Composition Boundary

P4-M0.7 preserves P4-M0.4 lifecycle behavior.

P4-M0.7 preserves P4-M0.5 explainable recall trace.

P4-M0.7 composes with P4-M0.6 do-not-retry guard after human approval.

P4-M0.7 does not automatically detect failures.

P4-M0.7 does not automatically mark do-not-retry.

P4-M0.7 does not automatically block execution.

P4-M0.7 does not automatically archive, delete, or clean memory.

## Product Boundary

P4-M0.7 is not API/MCP/connector.

P4-M0.7 is not external project adoption.

P4-M0.7 is not productization.

P4-M0.7 is not MVP.

P4-M0.7 is not deployment.

P4-M0.7 is not UI or Operator Console.

P4-M0.7 does not add dependencies.

P4-M0.7 does not add pyproject entry points.

P4-M0.7 does not change README.

## Version Boundary

P4-M0.7 is not v7.

P4-M0.7 is not full Memory Graph.

P4-M0.7 does not change package version.

P4-M0.7 does not tag.

P4-M0.7 does not create v6.17.

The package version remains sealed at `6.16.0`.

## Final Statement

P4-M0.7 adds deterministic project memory seed candidates and manual one-seed pending proposal tooling only.

It does not automatically approve seeds, write approved memory, bulk import, inject memory into agents, call Codex, call Hermes, call ChatGPT, call any agent, grant authorization, grant execution semantics, create API/MCP/connector behavior, adopt external projects, productize, build MVP, deploy, create UI, create Operator Console, start v7, implement full Memory Graph, change package version, tag, create v6.17, create automatic failure detection, automatically mark do-not-retry, automatically block execution, enforce policy, run benchmarks, run evaluation, or automatically archive, delete, or clean memory.
