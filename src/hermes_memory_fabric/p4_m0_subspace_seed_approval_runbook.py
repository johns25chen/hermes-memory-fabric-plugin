from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m0_subspace_project_seed import get_project_memory_seed, project_memory_seed_ids


SEED_APPROVAL_RUNBOOK_BOUNDARY = (
    "This runbook is human guidance only. It does not propose seeds. It does not approve seeds. "
    "It does not write approved memory. It does not bulk import. It does not authorize execution. "
    "It does not call agents. It does not start P4-M1. It does not start v7."
)


@dataclass(frozen=True)
class SeedApprovalRunbookEntry:
    order: int
    seed_id: str
    approval_stage: str
    rationale: str
    manual_propose_example: str
    manual_approve_note: str
    recall_query: str
    validation_expectation: str
    boundary: str


_ENTRY_BOUNDARY = (
    "Manual one-seed approval only; no automatic approval, no bulk import, no automatic approved "
    "memory writing, no agent call, no P4-M1, and no v7."
)


_SEED_APPROVAL_RUNBOOK_ENTRIES: tuple[SeedApprovalRunbookEntry, ...] = (
    SeedApprovalRunbookEntry(
        order=1,
        seed_id="civilization-core-identity",
        approval_stage="foundation",
        rationale=(
            "Approve this first because it anchors Civilization Core as the total system identity "
            "before any narrower tool, plugin, or workflow interpretation can dominate recall."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id civilization-core-identity --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command on the single proposal id returned by the manual "
            "propose step; review the content before approval."
        ),
        recall_query="Civilization Core total system identity",
        validation_expectation=(
            "Recall should return the approved project-seed memory for Civilization Core identity "
            "with a P4-M0.5 explainable trace."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=2,
        seed_id="subspace-memory-system-role",
        approval_stage="system-role",
        rationale=(
            "Approve this after identity because it defines Subspace Memory System as a bounded "
            "engineering carrier rather than product, API, MCP, connector, UI, or full Memory Graph."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id subspace-memory-system-role --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Approve only the reviewed single proposal with the existing approve command; do not "
            "approve the whole seed list."
        ),
        recall_query="Subspace Memory System bounded engineering layer",
        validation_expectation=(
            "Recall should explain the system-role boundary and include deterministic trace fields."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=3,
        seed_id="v6-16-stable-kernel-boundary",
        approval_stage="version-boundary",
        rationale=(
            "Approve this before route/product boundaries because it preserves v6.16.0 as the "
            "sealed stable kernel and prevents P4-M0 seed approval from implying v6.17."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id v6-16-stable-kernel-boundary --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command on one proposal id manually only after confirming "
            "package version remains 6.16.0."
        ),
        recall_query="v6.16.0 sealed stable kernel",
        validation_expectation=(
            "Recall should surface the v6.16.0 stable-kernel boundary without creating v6.17."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=4,
        seed_id="no-v7-without-human-authorization",
        approval_stage="route-boundary",
        rationale=(
            "Approve this before product and flow seeds because it keeps future-route recall "
            "explicitly blocked from treating P4-M0 as v7 authorization."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id no-v7-without-human-authorization --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command for one reviewed proposal id; approval records memory "
            "only and does not authorize v7."
        ),
        recall_query="no v7 without human authorization",
        validation_expectation=(
            "Recall should return the no-v7 boundary with trace metadata and no v7 branch or tag."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=5,
        seed_id="no-productization-no-deployment-boundary",
        approval_stage="product-boundary",
        rationale=(
            "Approve this after the route boundary so recall keeps seed approval separate from "
            "productization, MVP, deployment, UI, Operator Console, API, MCP, and connector work."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id no-productization-no-deployment-boundary --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command on the one proposal manually only if the reviewed "
            "content remains a boundary, not a product operation plan."
        ),
        recall_query="not productization not deployment not API MCP connector",
        validation_expectation=(
            "Recall should preserve product and deployment prohibitions without exposing a product "
            "operation surface."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=6,
        seed_id="p4-m0-human-gated-chain",
        approval_stage="governance-flow",
        rationale=(
            "Approve this after the major boundaries because it describes the human-gated flow that "
            "connects proposal, approval, lifecycle, trace, do-not-retry, and seed behavior."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id p4-m0-human-gated-chain --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Approve only the one pending proposal with the existing approve command; keep proposal "
            "and approval as separate human actions."
        ),
        recall_query="P4-M0 human-gated proposal approval lifecycle trace",
        validation_expectation=(
            "Recall should return the human-gated flow and preserve P4-M0.5 explainable trace."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=7,
        seed_id="manual-operator-validation-discipline",
        approval_stage="operator-discipline",
        rationale=(
            "Approve this near the end because it reinforces deterministic validation, no README "
            "drift, no pyproject entry points, no uv.lock, no commit, and no tag discipline."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id manual-operator-validation-discipline --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command on a single reviewed proposal only after running the "
            "local validation corridor."
        ),
        recall_query="operator validation discipline no uv.lock no tag",
        validation_expectation=(
            "Recall should return validation discipline with deterministic trace and no repository "
            "metadata drift."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
    SeedApprovalRunbookEntry(
        order=8,
        seed_id="do-not-retry-and-lifecycle-governance",
        approval_stage="lifecycle-and-do-not-retry",
        rationale=(
            "Approve this last because lifecycle and do-not-retry are post-approval governance "
            "concerns and must remain manual after memory is approved."
        ),
        manual_propose_example=(
            "project-seed propose --seed-id do-not-retry-and-lifecycle-governance --actor human "
            "--workspace-root <workspace>"
        ),
        manual_approve_note=(
            "Use the existing approve command on one reviewed proposal first; lifecycle and "
            "do-not-retry commands remain later manual actions and are not called by this runbook."
        ),
        recall_query="do-not-retry lifecycle governance manual",
        validation_expectation=(
            "Recall should include the approved seed with trace; lifecycle and do-not-retry behavior "
            "remain separate manual P4-M0.4 and P4-M0.6 operations."
        ),
        boundary=_ENTRY_BOUNDARY,
    ),
)


def list_seed_approval_runbook_entries() -> tuple[SeedApprovalRunbookEntry, ...]:
    _validate_entries_reference_project_seeds(_SEED_APPROVAL_RUNBOOK_ENTRIES)
    return _SEED_APPROVAL_RUNBOOK_ENTRIES


def get_seed_approval_runbook_entry(seed_id: str) -> SeedApprovalRunbookEntry:
    clean_seed_id = str(seed_id or "").strip()
    if not clean_seed_id:
        raise ValueError("seed_id_must_be_non_empty")
    for entry in list_seed_approval_runbook_entries():
        if entry.seed_id == clean_seed_id:
            return entry
    raise ValueError("seed_approval_runbook_entry_not_found")


def seed_approval_runbook_seed_ids() -> tuple[str, ...]:
    return tuple(entry.seed_id for entry in list_seed_approval_runbook_entries())


def render_seed_approval_runbook_markdown(
    entries: Sequence[SeedApprovalRunbookEntry] | None = None,
) -> str:
    entry_values = tuple(entries) if entries is not None else list_seed_approval_runbook_entries()
    lines = [
        "# P4-M0.8 Seed Approval Runbook",
        "",
        SEED_APPROVAL_RUNBOOK_BOUNDARY,
        "",
        "Use this order to review, propose, approve, and recall-verify one seed at a time.",
        "",
    ]
    for entry in entry_values:
        lines.extend(
            [
                f"## {entry.order}. {entry.seed_id}",
                "",
                f"- Approval stage: {entry.approval_stage}",
                f"- Rationale: {entry.rationale}",
                f"- Manual propose example: `{entry.manual_propose_example}`",
                f"- Manual approve note: {entry.manual_approve_note}",
                f"- Recall query: `{entry.recall_query}`",
                f"- Validation expectation: {entry.validation_expectation}",
                f"- Boundary: {entry.boundary}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def seed_approval_runbook_as_dicts(
    entries: Sequence[SeedApprovalRunbookEntry] | None = None,
) -> tuple[dict[str, object], ...]:
    entry_values = tuple(entries) if entries is not None else list_seed_approval_runbook_entries()
    return tuple(asdict(entry) for entry in entry_values)


def _validate_entries_reference_project_seeds(entries: Sequence[SeedApprovalRunbookEntry]) -> None:
    existing_seed_ids = set(project_memory_seed_ids())
    for entry in entries:
        if entry.seed_id not in existing_seed_ids:
            raise ValueError("seed_approval_runbook_references_unknown_project_seed")
        get_project_memory_seed(entry.seed_id)
