from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


PROJECT_MEMORY_SEED_SOURCE = "p4-m0.7-project-memory-seed"
PROJECT_MEMORY_SEED_PROJECT = "civilization-core"
PROJECT_MEMORY_SEED_NAMESPACE = "project-seed"


@dataclass(frozen=True)
class ProjectMemorySeed:
    seed_id: str
    project: str
    namespace: str
    content: str
    source: str
    tags: tuple[str, ...]
    confidence: float


_PROJECT_MEMORY_SEEDS: tuple[ProjectMemorySeed, ...] = (
    ProjectMemorySeed(
        seed_id="civilization-core-identity",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Civilization Core is the total system identity. Subspace Memory System is the "
            "engineering carrier for governed memory. The project must not be reduced to a "
            "Hermes plugin, OpenClaw tool, or Codex workflow."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("civilization-core-identity", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="subspace-memory-system-role",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Subspace Memory System carries local governed project memory for Civilization Core. "
            "It remains a bounded engineering layer and does not become full Memory Graph, API, "
            "MCP, connector, UI, or product runtime."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("p4-m0.7", "project-seed", "subspace-memory-system-role"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="v6-16-stable-kernel-boundary",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Civilization Core v6.16.0 remains the sealed stable kernel. P4-M0 work may add "
            "bounded Subspace Memory layers without changing the package version or creating "
            "v6.17."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("p4-m0.7", "project-seed", "v6-16-stable-kernel-boundary"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="p4-m0-human-gated-chain",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "The P4-M0 chain is human-gated: proposal, approval, lifecycle, trace, do-not-retry, "
            "and seed behavior require explicit manual operator actions before memory becomes "
            "approved and recallable."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("p4-m0-human-gated-chain", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="no-v7-without-human-authorization",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "No v7 work starts without separate explicit human authorization. P4-M0 project "
            "memory seed candidates do not create v7, authorize v7, or imply a v7 branch."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("no-v7-without-human-authorization", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="no-productization-no-deployment-boundary",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Subspace Memory project seed work is not productization, MVP, deployment, API, MCP, "
            "connector, external project adoption, UI, or Operator Console."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("no-productization-no-deployment-boundary", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="manual-operator-validation-discipline",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Operator discipline prefers small deterministic changes, exact validation corridors, "
            "literal boundary preservation, no README drift, no pyproject entry points, no uv.lock, "
            "no commit, and no tag unless separately requested."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("manual-operator-validation-discipline", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
    ProjectMemorySeed(
        seed_id="do-not-retry-and-lifecycle-governance",
        project=PROJECT_MEMORY_SEED_PROJECT,
        namespace=PROJECT_MEMORY_SEED_NAMESPACE,
        content=(
            "Approved project memory keeps P4-M0.4 lifecycle behavior and P4-M0.6 do-not-retry "
            "governance. Stale, archived, and do-not-retry states remain manual and do not "
            "auto-detect, auto-block, auto-delete, or auto-clean."
        ),
        source=PROJECT_MEMORY_SEED_SOURCE,
        tags=("do-not-retry-and-lifecycle-governance", "p4-m0.7", "project-seed"),
        confidence=1.0,
    ),
)


def list_project_memory_seeds() -> tuple[ProjectMemorySeed, ...]:
    return _PROJECT_MEMORY_SEEDS


def get_project_memory_seed(seed_id: str) -> ProjectMemorySeed:
    clean_seed_id = str(seed_id or "").strip()
    if not clean_seed_id:
        raise ValueError("seed_id_must_be_non_empty")
    for seed in _PROJECT_MEMORY_SEEDS:
        if seed.seed_id == clean_seed_id:
            return seed
    raise ValueError("project_memory_seed_not_found")


def project_memory_seed_ids() -> tuple[str, ...]:
    return tuple(seed.seed_id for seed in _PROJECT_MEMORY_SEEDS)


def render_project_memory_seed_pack(seeds: Sequence[ProjectMemorySeed] | None = None) -> str:
    seed_values = tuple(seeds) if seeds is not None else list_project_memory_seeds()
    lines = [
        "# P4-M0.7 Project Memory Seed Pack",
        "",
        "This seed pack is human-provided context only.",
        "",
        "It does not approve memory.",
        "",
        "It does not write approved memory.",
        "",
        "It does not authorize execution.",
        "",
        "It does not call agents.",
        "",
    ]
    for seed in seed_values:
        lines.extend(
            [
                f"## {seed.seed_id}",
                "",
                f"- Project: {seed.project}",
                f"- Namespace: {seed.namespace}",
                f"- Source: {seed.source}",
                f"- Confidence: {seed.confidence:.1f}",
                f"- Tags: {', '.join(seed.tags)}",
                "",
                seed.content,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
