# Civilization Core P4-M0.8 Subspace Memory Seed Approval Runbook

## Status

P4-M0.8 is human-authorized.

This document records a narrow Subspace Memory implementation increment only: a deterministic seed approval runbook for existing P4-M0.7 project seed candidates.

P4-M0.8 remains P4-M0.

P4-M0.8 does not start P4-M1.

P4-M0.8 does not start v7.

## Purpose

P4-M0.8 adds a deterministic seed approval runbook.

The runbook explains which seed candidates should be approved first.

The runbook explains why each seed exists.

The runbook explains how to propose one seed manually.

The runbook explains how to approve one proposal manually using the existing approve command.

The runbook explains how to recall-verify approved seed memory.

The runbook is human guidance only.

## Preserved P4-M0.7 Seed Candidate Behavior

P4-M0.8 preserves P4-M0.7 seed candidate behavior.

P4-M0.7 seed candidates remain deterministic candidates.

P4-M0.7 manual proposal behavior remains one seed at a time.

P4-M0.8 does not change seed candidate content.

P4-M0.8 does not add automatic seed import.

P4-M0.8 does not add automatic seed approval.

P4-M0.8 does not add automatic approved memory writing.

P4-M0.8 explicitly forbids bulk approval.

P4-M0.8 explicitly forbids automatic seed import.

P4-M0.8 explicitly forbids automatic seed approval.

P4-M0.8 explicitly forbids automatic approved memory writing.

## Manual Operator Flow

The human operator reviews the runbook order.

The human operator selects exactly one seed candidate.

The human operator proposes that one seed manually with the existing `project-seed propose` command.

The human operator reviews the single pending proposal.

The human operator approves that one proposal manually with the existing `approve` command.

The human operator recall-verifies the approved seed memory with the existing `recall` command.

Approval remains a separate human action.

Recall verification remains a separate human action.

Lifecycle changes remain separate human actions.

Do-not-retry changes remain separate human actions.

## Composition Boundary

P4-M0.8 preserves P4-M0.5 explainable recall trace after approval.

P4-M0.8 preserves P4-M0.4 lifecycle behavior after approval.

P4-M0.8 composes with P4-M0.6 do-not-retry guard after approval.

P4-M0.8 does not call recall automatically.

P4-M0.8 does not call lifecycle automatically.

P4-M0.8 does not call do-not-retry automatically.

P4-M0.8 does not automatically detect failures.

P4-M0.8 does not automatically mark do-not-retry.

P4-M0.8 does not automatically block execution.

P4-M0.8 does not enforce policy.

P4-M0.8 does not create a safety policy engine.

## Agent Boundary

P4-M0.8 does not call Codex.

P4-M0.8 does not call Hermes.

P4-M0.8 does not call ChatGPT.

P4-M0.8 does not call any agent.

P4-M0.8 does not write prompts into agents automatically.

P4-M0.8 does not auto-inject memory into agents.

## Product Boundary

P4-M0.8 is not productization.

P4-M0.8 is not MVP.

P4-M0.8 is not deployment.

P4-M0.8 is not UI or Operator Console.

P4-M0.8 is not API/MCP/connector.

P4-M0.8 is not external project adoption.

P4-M0.8 is not full Memory Graph.

P4-M0.8 does not add dependencies.

P4-M0.8 does not add adapters.

P4-M0.8 does not add pyproject entry points.

P4-M0.8 does not change README.

## Authorization Boundary

P4-M0.8 does not grant authorization.

P4-M0.8 does not grant execution semantics.

P4-M0.8 does not approve memory.

P4-M0.8 does not authorize execution.

P4-M0.8 does not approve all seeds.

P4-M0.8 does not import seeds.

P4-M0.8 does not bulk import seeds.

P4-M0.8 does not write approved memory.

## Version Boundary

P4-M0.8 does not change package version.

P4-M0.8 does not tag.

P4-M0.8 does not create v6.17.

P4-M0.8 does not create v7.

The package version remains sealed at `6.16.0`.

## Runbook Order

The deterministic runbook order is:

1. `civilization-core-identity`
2. `subspace-memory-system-role`
3. `v6-16-stable-kernel-boundary`
4. `no-v7-without-human-authorization`
5. `no-productization-no-deployment-boundary`
6. `p4-m0-human-gated-chain`
7. `manual-operator-validation-discipline`
8. `do-not-retry-and-lifecycle-governance`

Each runbook entry includes approval stage, rationale, manual propose example, manual approve note, recall query, validation expectation, and boundary statement.

## Final Statement

P4-M0.8 adds a deterministic seed approval runbook only.

It does not automatically propose seeds, approve seeds, write approved memory, bulk import, import seeds, inject memory into agents, call Codex, call Hermes, call ChatGPT, call any agent, grant authorization, grant execution semantics, create API/MCP/connector behavior, adopt external projects, productize, build MVP, deploy, create UI, create Operator Console, start P4-M1, start v7, implement full Memory Graph, change package version, tag, create v6.17, create automatic failure detection, automatically mark do-not-retry, automatically block execution, enforce policy, run benchmarks, run evaluation, or automatically archive, delete, or clean memory.
