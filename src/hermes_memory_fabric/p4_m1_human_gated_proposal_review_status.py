from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_1_PACKAGE_VERSION = "6.16.0"

HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY = (
    "P4-M1.1 is read-only proposal review status only and advisory only. "
    "It does not write memory. It does not approve memory. It does not reject memory. "
    "It does not mutate proposal records. It does not bulk import memory. "
    "It does not auto-ingest chat history. It does not auto-ingest files. "
    "It does not auto-ingest external systems. It does not inject memory into agents. "
    "It does not call agents. It does not call external APIs. "
    "It does not create API/MCP/connector behavior. It does not start v7. "
    "It does not productize. It does not grant authorization semantics. "
    "It does not grant execution semantics."
)


@dataclass(frozen=True)
class HumanGatedProposalReviewStatusItem:
    review_order: int
    review_id: str
    review_name: str
    human_review_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_REVIEW_STATUS_ITEMS: tuple[HumanGatedProposalReviewStatusItem, ...] = (
    HumanGatedProposalReviewStatusItem(
        review_order=1,
        review_id="proposal-visible",
        review_name="Proposal visible",
        human_review_question="Can the human see the proposal or candidate text before any decision?",
        allowed_system_output="Show proposal or candidate text and review context for human inspection.",
        prohibited_automation="No approval, rejection, mutation, memory write, or hidden decision.",
        ready_signal="The proposal or candidate text is visible to the human.",
        blocking_signal="The human cannot inspect the proposal or candidate text.",
        p4_m0_or_p4_m1_dependency="P4-M0.7 project seed candidates and P4-M1.0 checklist visibility.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=2,
        review_id="scope-boundary-visible",
        review_name="Scope boundary visible",
        human_review_question="Can the human see the boundary and prohibited automation scope?",
        allowed_system_output="Show read-only advisory boundary text and disabled automation flags.",
        prohibited_automation="No implicit authorization, execution, write, approval, rejection, or product surface.",
        ready_signal="The boundary and prohibited automation scope are visible.",
        blocking_signal="The review surface omits disabled automation or boundary scope.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 human-gated checklist boundary.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=3,
        review_id="source-visible",
        review_name="Source visible",
        human_review_question="Can the human see source or context information when it is present?",
        allowed_system_output="Show available source/context fields without fetching external systems.",
        prohibited_automation="No external API call, agent call, auto-ingest, or hidden source enrichment.",
        ready_signal="Available source/context information is visible or explicitly absent.",
        blocking_signal="Source/context information is hidden, fabricated, or externally enriched.",
        p4_m0_or_p4_m1_dependency="P4-M0 proposal/source metadata discipline.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=4,
        review_id="content-review-required",
        review_name="Content review required",
        human_review_question="Has the human reviewed content accuracy, scope fit, and usefulness?",
        allowed_system_output="Ask for human content review and present advisory checklist/status text.",
        prohibited_automation="No truth judgment, quality score, freshness verdict, approval, rejection, or write.",
        ready_signal="Human content review is clearly required before any later manual decision.",
        blocking_signal="The status implies content is already approved, rejected, true, fresh, or fit.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 human content review gate.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=5,
        review_id="decision-not-taken",
        review_name="Decision not taken",
        human_review_question="Is it clear that this status performs no approve, reject, or write action?",
        allowed_system_output="State that no approval or rejection is performed by this status.",
        prohibited_automation="No approve, reject, approve-all, reject-all, proposal mutation, or memory write.",
        ready_signal="The status remains advisory and does not change proposal or memory state.",
        blocking_signal="Any proposal state, approval state, rejection state, or memory record changes.",
        p4_m0_or_p4_m1_dependency="P4-M0.2 manual approve/reject commands stay separate.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=6,
        review_id="recall-plan-visible",
        review_name="Recall plan visible",
        human_review_question="Can the human see how recall verification should be done later?",
        allowed_system_output="Describe later manual recall verification without running recall automatically.",
        prohibited_automation="No automatic recall verification, memory injection, or agent call.",
        ready_signal="Later manual recall verification is visible as a separate optional step.",
        blocking_signal="The status claims recall verification has already run or injects recall into agents.",
        p4_m0_or_p4_m1_dependency="P4-M0.3 recall pack and P4-M0.5 explainable recall trace.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=7,
        review_id="lifecycle-plan-visible",
        review_name="Lifecycle plan visible",
        human_review_question="Can the human see that lifecycle remains optional and manual later?",
        allowed_system_output="Describe lifecycle as a later optional manual operation.",
        prohibited_automation="No automatic lifecycle state, archive, stale marking, cleanup, or deletion.",
        ready_signal="Lifecycle remains a visible later manual option.",
        blocking_signal="The status changes lifecycle state or implies lifecycle enforcement.",
        p4_m0_or_p4_m1_dependency="P4-M0.4 Subspace Memory lifecycle state.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=8,
        review_id="do-not-retry-plan-visible",
        review_name="Do-not-retry plan visible",
        human_review_question="Can the human see that do-not-retry remains optional and manual later?",
        allowed_system_output="Describe do-not-retry as a later optional manual operation.",
        prohibited_automation="No automatic failure detection, retry blocking, or do-not-retry marking.",
        ready_signal="Do-not-retry remains a visible later manual option.",
        blocking_signal="The status marks, infers, or enforces do-not-retry.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 Subspace Memory do-not-retry guard.",
    ),
    HumanGatedProposalReviewStatusItem(
        review_order=9,
        review_id="automation-boundary-intact",
        review_name="Automation boundary intact",
        human_review_question="Are write, approval, rejection, import, agent, API/MCP, v7, and productization disabled?",
        allowed_system_output="Report disabled write, approval, rejection, import, ingestion, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No write/import/ingest/agent/API/MCP/connector/v7/productization behavior.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.0 read-only and manual boundary discipline.",
    ),
)


def list_human_gated_proposal_review_status_items() -> tuple[HumanGatedProposalReviewStatusItem, ...]:
    return _REVIEW_STATUS_ITEMS


def human_gated_proposal_review_status_ids() -> tuple[str, ...]:
    return tuple(item.review_id for item in list_human_gated_proposal_review_status_items())


def render_human_gated_proposal_review_status_markdown(
    items: Sequence[HumanGatedProposalReviewStatusItem] | None = None,
) -> str:
    item_values = tuple(items) if items is not None else list_human_gated_proposal_review_status_items()
    status = human_gated_proposal_review_status_report()
    lines = [
        "# P4-M1.1 Human-Gated Proposal Review Status",
        "",
        "P4-M1.1 is proposal review status only.",
        "",
        "Review status is advisory only.",
        "",
        "No approval or rejection is performed by this status.",
        "",
        HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Review Items", ""])
    for item in item_values:
        lines.extend(
            [
                f"### {item.review_order}. {item.review_id}",
                "",
                f"- Review name: {item.review_name}",
                f"- Human review question: {item.human_review_question}",
                f"- Allowed system output: {item.allowed_system_output}",
                f"- Prohibited automation: {item.prohibited_automation}",
                f"- Ready signal: {item.ready_signal}",
                f"- Blocking signal: {item.blocking_signal}",
                f"- P4-M0/P4-M1 dependency: {item.p4_m0_or_p4_m1_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def human_gated_proposal_review_status_as_dicts(
    items: Sequence[HumanGatedProposalReviewStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = tuple(items) if items is not None else list_human_gated_proposal_review_status_items()
    return tuple(asdict(item) for item in item_values)


def human_gated_proposal_review_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.1",
        "feature": "Human-Gated Proposal Review Status",
        "mode": "read-only",
        "review_item_count": len(_REVIEW_STATUS_ITEMS),
        "review_status_advisory_only": True,
        "memory_write_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "proposal_mutation_enabled": False,
        "bulk_import_enabled": False,
        "auto_ingest_enabled": False,
        "agent_call_enabled": False,
        "api_mcp_connector_enabled": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M1_1_PACKAGE_VERSION,
        "boundary": HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY,
    }
