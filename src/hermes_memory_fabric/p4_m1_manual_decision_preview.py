from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_7_PACKAGE_VERSION = "6.16.0"

MANUAL_DECISION_PREVIEW_BOUNDARY = (
    "P4-M1.7 is read-only manual decision preview only, advisory only, "
    "and for human inspection only. It does not recommend a decision. "
    "It does not rank decisions. It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. It does not make decisions. "
    "It does not execute decisions. It does not approve memory. "
    "It does not reject memory. It does not approve proposals. "
    "It does not reject proposals. It does not write memory. "
    "It does not create memory records. It does not update memory records. "
    "It does not delete memory records. It does not mutate proposal records. "
    "It does not mutate lifecycle records. "
    "It does not mutate do-not-retry guard state. "
    "It does not mutate retry policy. It does not fetch sources. "
    "It does not browse the web. It does not call external APIs. "
    "It does not call connectors. It does not create API/MCP/connector behavior. "
    "It does not automatically trust a source. It does not write provenance. "
    "It does not mutate source/provenance/evidence/citation records. "
    "It does not inject memory into agents. It does not bulk import memory. "
    "It does not auto-ingest chat history. It does not auto-ingest files. "
    "It does not auto-ingest external systems. It does not call agents. "
    "It does not start v7. It does not productize. "
    "It does not grant authorization semantics. "
    "It does not grant execution semantics."
)


@dataclass(frozen=True)
class ManualDecisionPreviewFrame:
    preview_order: int
    preview_id: str
    preview_name: str
    human_preview_question: str
    source_status_surface: str
    allowed_preview_output: str
    prohibited_automation: str
    human_review_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_MANUAL_DECISION_PREVIEW_FRAMES: tuple[ManualDecisionPreviewFrame, ...] = (
    ManualDecisionPreviewFrame(
        preview_order=1,
        preview_id="checklist-preview",
        preview_name="Checklist preview",
        human_preview_question="What P4-M1.0 checklist items should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.0 Human-Gated Memory Loop Checklist.",
        allowed_preview_output="Show the checklist frame for human inspection only.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, approval, rejection, execution, memory write, or proposal mutation.",
        human_review_signal="The P4-M1.0 checklist frame is visible as advisory preview material.",
        blocking_signal="The checklist frame is hidden or converted into recommendation, readiness, approval, rejection, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 Human-Gated Memory Loop Checklist.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=2,
        preview_id="proposal-review-preview",
        preview_name="Proposal review preview",
        human_preview_question="What P4-M1.1 proposal review status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.1 Human-Gated Proposal Review Status.",
        allowed_preview_output="Show the proposal review frame for human inspection only.",
        prohibited_automation="No proposal approval, proposal rejection, proposal mutation, decision recommendation, readiness verdict, or execution.",
        human_review_signal="The proposal review frame is visible without approving, rejecting, or mutating proposals.",
        blocking_signal="Proposal review status is treated as approval, rejection, mutation, authorization, recommendation, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 Human-Gated Proposal Review Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=3,
        preview_id="recall-verification-preview",
        preview_name="Recall verification preview",
        human_preview_question="What P4-M1.2 recall verification status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.2 Human-Gated Recall Verification Status.",
        allowed_preview_output="Show the recall verification frame for human inspection only.",
        prohibited_automation="No recall verdict, decision recommendation, decision ranking, readiness verdict, approval, rejection, memory write, or execution.",
        human_review_signal="The recall verification frame is visible without automatic verdicts or state mutation.",
        blocking_signal="Recall verification status is treated as recommendation, ranking, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 Human-Gated Recall Verification Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=4,
        preview_id="lifecycle-verification-preview",
        preview_name="Lifecycle verification preview",
        human_preview_question="What P4-M1.3 lifecycle verification status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.3 Human-Gated Lifecycle Verification Status.",
        allowed_preview_output="Show the lifecycle verification frame for human inspection only.",
        prohibited_automation="No lifecycle mutation, readiness verdict, decision recommendation, approval, rejection, memory write, or execution.",
        human_review_signal="The lifecycle verification frame is visible while lifecycle mutation remains disabled.",
        blocking_signal="Lifecycle verification status is treated as lifecycle mutation, recommendation, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.3 Human-Gated Lifecycle Verification Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=5,
        preview_id="do-not-retry-preview",
        preview_name="Do-not-retry preview",
        human_preview_question="What P4-M1.4 do-not-retry verification status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
        allowed_preview_output="Show the do-not-retry verification frame for human inspection only.",
        prohibited_automation="No do-not-retry guard mutation, retry policy mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        human_review_signal="The do-not-retry frame is visible while guard and retry policy mutation remain disabled.",
        blocking_signal="Do-not-retry status is treated as guard mutation, retry policy mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=6,
        preview_id="source-provenance-preview",
        preview_name="Source/provenance preview",
        human_preview_question="What P4-M1.5 source/provenance verification status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.5 Source / Provenance Verification Status.",
        allowed_preview_output="Show the source/provenance verification frame for human inspection only.",
        prohibited_automation="No source fetching, source trust, provenance writing, source/provenance/evidence/citation mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        human_review_signal="The source/provenance frame is visible without fetching, trusting, writing, or mutating source/provenance records.",
        blocking_signal="Source/provenance status is treated as source fetch, source trust, provenance write, mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.5 Source / Provenance Verification Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=7,
        preview_id="decision-readiness-preview",
        preview_name="Decision readiness preview",
        human_preview_question="What P4-M1.6 decision readiness status should the human inspect before any later manual decision?",
        source_status_surface="P4-M1.6 Decision Readiness Status.",
        allowed_preview_output="Show the decision readiness frame for human inspection only.",
        prohibited_automation="No automatic readiness verdict, decision recommendation, decision ranking, approval, rejection, authorization, execution, memory write, or proposal mutation.",
        human_review_signal="The decision readiness frame is visible while automatic readiness verdict and decision execution remain disabled.",
        blocking_signal="Decision readiness status is converted into recommendation, ranking, automatic readiness, authorization, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.6 Decision Readiness Status.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=8,
        preview_id="unified-human-review-frame",
        preview_name="Unified human review frame",
        human_preview_question="Can the human inspect P4-M1.0 through P4-M1.6 together before any later manual decision?",
        source_status_surface="Unified P4-M1.0 through P4-M1.6 read-only governance surfaces.",
        allowed_preview_output="Show a unified frame across P4-M1.0 through P4-M1.6 for human inspection only.",
        prohibited_automation="No decision recommendation, decision ranking, automatic readiness verdict, approval, rejection, execution, memory write, or state mutation.",
        human_review_signal="All seven P4-M1 source status surfaces are visible together as advisory preview material.",
        blocking_signal="The unified frame hides a required source surface or converts the preview into recommendation, readiness, approval, rejection, write, mutation, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 through P4-M1.6 read-only governance corridor.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=9,
        preview_id="decision-not-recommended",
        preview_name="Decision not recommended",
        human_preview_question="Is it clear that this preview produces no decision recommendation, approval, rejection, execution, or memory write?",
        source_status_surface="P4-M1.7 Manual Decision Preview boundary.",
        allowed_preview_output="State that no decision recommendation, approval, rejection, execution, or memory write is produced.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, approval, rejection, execution, memory write, memory record mutation, proposal mutation, lifecycle mutation, do-not-retry mutation, or provenance write.",
        human_review_signal="The preview explicitly states that no decision recommendation, approval, rejection, execution, or memory write is produced.",
        blocking_signal="Any decision recommendation, ranking, approval, rejection, execution, memory write, or state mutation is produced.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only governance corridor.",
    ),
    ManualDecisionPreviewFrame(
        preview_order=10,
        preview_id="automation-boundary-intact",
        preview_name="Automation boundary intact",
        human_preview_question="Are disabled recommendation, readiness verdict, execution, approval, rejection, write, mutation, import, ingest, injection, agent, API/MCP/connector, v7, and productization flags intact?",
        source_status_surface="P4-M1.7 disabled automation status report.",
        allowed_preview_output="Report disabled decision recommendation, readiness verdict, execution, approval, rejection, memory write, memory/proposal/lifecycle/do-not-retry/retry-policy/source/provenance mutation, source fetching, import, ingestion, injection, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No recommendation, ranking, readiness verdict, decision, execution, approval, rejection, write, mutation, fetch, import, ingest, injection, agent call, API/MCP/connector behavior, v7 start, or productization.",
        human_review_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled, a recommendation or verdict is emitted, a decision is executed, state is mutated, or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.6 read-only/manual boundary discipline.",
    ),
)


def list_manual_decision_preview_frames() -> tuple[ManualDecisionPreviewFrame, ...]:
    return _MANUAL_DECISION_PREVIEW_FRAMES


def manual_decision_preview_ids() -> tuple[str, ...]:
    return tuple(frame.preview_id for frame in list_manual_decision_preview_frames())


def render_manual_decision_preview_markdown(
    frames: Sequence[ManualDecisionPreviewFrame] | None = None,
) -> str:
    frame_values = (
        tuple(frames) if frames is not None else list_manual_decision_preview_frames()
    )
    status = manual_decision_preview_report()
    lines = [
        "# P4-M1.7 Manual Decision Preview",
        "",
        "P4-M1.7 is manual decision preview only.",
        "",
        "Manual decision preview is advisory only.",
        "",
        "Manual decision preview is for human inspection only.",
        "",
        "No decision recommendation is performed by this preview.",
        "",
        "No decision ranking is performed by this preview.",
        "",
        "No automatic readiness verdict is performed by this preview.",
        "",
        "No decision execution is performed by this preview.",
        "",
        "No approval or rejection is performed by this preview.",
        "",
        "No memory writing is performed by this preview.",
        "",
        "No proposal mutation is performed by this preview.",
        "",
        "No lifecycle mutation is performed by this preview.",
        "",
        "No do-not-retry mutation is performed by this preview.",
        "",
        "No source/provenance mutation is performed by this preview.",
        "",
        "No API/MCP/connector behavior is performed by this preview.",
        "",
        MANUAL_DECISION_PREVIEW_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Preview Frames", ""])
    for frame in frame_values:
        lines.extend(
            [
                f"### {frame.preview_order}. {frame.preview_id}",
                "",
                f"- Preview name: {frame.preview_name}",
                f"- Human preview question: {frame.human_preview_question}",
                f"- Source status surface: {frame.source_status_surface}",
                f"- Allowed preview output: {frame.allowed_preview_output}",
                f"- Prohibited automation: {frame.prohibited_automation}",
                f"- Human review signal: {frame.human_review_signal}",
                f"- Blocking signal: {frame.blocking_signal}",
                f"- P4-M0/P4-M1 dependency: {frame.p4_m0_or_p4_m1_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def manual_decision_preview_as_dicts(
    frames: Sequence[ManualDecisionPreviewFrame] | None = None,
) -> tuple[dict[str, object], ...]:
    frame_values = (
        tuple(frames) if frames is not None else list_manual_decision_preview_frames()
    )
    return tuple(asdict(frame) for frame in frame_values)


def manual_decision_preview_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.7",
        "feature": "Manual Decision Preview",
        "mode": "read-only",
        "preview_frame_count": len(_MANUAL_DECISION_PREVIEW_FRAMES),
        "manual_decision_preview_advisory_only": True,
        "human_inspection_only": True,
        "automatic_decision_recommendation_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "decision_execution_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "memory_write_enabled": False,
        "memory_record_mutation_enabled": False,
        "proposal_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "do_not_retry_guard_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "source_fetching_enabled": False,
        "source_provenance_mutation_enabled": False,
        "provenance_write_enabled": False,
        "memory_injection_enabled": False,
        "bulk_import_enabled": False,
        "auto_ingest_enabled": False,
        "agent_call_enabled": False,
        "api_mcp_connector_enabled": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M1_7_PACKAGE_VERSION,
        "boundary": MANUAL_DECISION_PREVIEW_BOUNDARY,
    }
