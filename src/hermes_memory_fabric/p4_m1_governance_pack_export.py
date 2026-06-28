from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_8_PACKAGE_VERSION = "6.16.0"

GOVERNANCE_PACK_EXPORT_BOUNDARY = (
    "P4-M1.8 is read-only governance pack export only, advisory only, "
    "and for human audit, archive, handoff, and review only. "
    "It does not recommend a decision. It does not rank decisions. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not execute decisions. "
    "It does not approve memory. It does not reject memory. "
    "It does not approve proposals. It does not reject proposals. "
    "It does not write memory. It does not create memory records. "
    "It does not update memory records. It does not delete memory records. "
    "It does not mutate proposal records. "
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
class GovernancePackSection:
    section_order: int
    section_id: str
    section_name: str
    source_status_surface: str
    export_purpose: str
    allowed_export_output: str
    prohibited_automation: str
    human_audit_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_GOVERNANCE_PACK_SECTIONS: tuple[GovernancePackSection, ...] = (
    GovernancePackSection(
        section_order=1,
        section_id="checklist-pack-section",
        section_name="Checklist pack section",
        source_status_surface="P4-M1.0 Human-Gated Memory Loop Checklist.",
        export_purpose="Package the P4-M1.0 checklist surface for human audit.",
        allowed_export_output="Read-only checklist package material for human audit, archive, handoff, and review.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, approval, rejection, execution, memory write, or proposal mutation.",
        human_audit_signal="The P4-M1.0 checklist surface is present in the governance pack.",
        blocking_signal="The checklist surface is missing or converted into recommendation, readiness, approval, rejection, write, mutation, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 Human-Gated Memory Loop Checklist.",
    ),
    GovernancePackSection(
        section_order=2,
        section_id="proposal-review-pack-section",
        section_name="Proposal review pack section",
        source_status_surface="P4-M1.1 Human-Gated Proposal Review Status.",
        export_purpose="Package the P4-M1.1 proposal review status surface for human audit.",
        allowed_export_output="Read-only proposal review package material without approval, rejection, or mutation.",
        prohibited_automation="No proposal approval, proposal rejection, proposal mutation, decision recommendation, ranking, readiness verdict, or execution.",
        human_audit_signal="The P4-M1.1 proposal review status surface is present without mutating proposals.",
        blocking_signal="Proposal review status is treated as approval, rejection, mutation, recommendation, ranking, readiness, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 Human-Gated Proposal Review Status.",
    ),
    GovernancePackSection(
        section_order=3,
        section_id="recall-verification-pack-section",
        section_name="Recall verification pack section",
        source_status_surface="P4-M1.2 Human-Gated Recall Verification Status.",
        export_purpose="Package the P4-M1.2 recall verification status surface for human audit.",
        allowed_export_output="Read-only recall verification package material without automatic verdicts.",
        prohibited_automation="No recall verdict, decision recommendation, decision ranking, automatic readiness verdict, approval, rejection, memory write, or execution.",
        human_audit_signal="The P4-M1.2 recall verification surface is present without automatic readiness or decision semantics.",
        blocking_signal="Recall verification status is treated as recommendation, ranking, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 Human-Gated Recall Verification Status.",
    ),
    GovernancePackSection(
        section_order=4,
        section_id="lifecycle-verification-pack-section",
        section_name="Lifecycle verification pack section",
        source_status_surface="P4-M1.3 Human-Gated Lifecycle Verification Status.",
        export_purpose="Package the P4-M1.3 lifecycle verification status surface for human audit.",
        allowed_export_output="Read-only lifecycle verification package material while lifecycle mutation remains disabled.",
        prohibited_automation="No lifecycle mutation, readiness verdict, decision recommendation, approval, rejection, memory write, or execution.",
        human_audit_signal="The P4-M1.3 lifecycle verification surface is present while lifecycle mutation remains disabled.",
        blocking_signal="Lifecycle verification status is treated as lifecycle mutation, recommendation, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.3 Human-Gated Lifecycle Verification Status.",
    ),
    GovernancePackSection(
        section_order=5,
        section_id="do-not-retry-pack-section",
        section_name="Do-not-retry pack section",
        source_status_surface="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
        export_purpose="Package the P4-M1.4 do-not-retry verification status surface for human audit.",
        allowed_export_output="Read-only do-not-retry verification package material while guard and retry policy mutation remain disabled.",
        prohibited_automation="No do-not-retry guard mutation, retry policy mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        human_audit_signal="The P4-M1.4 do-not-retry surface is present while guard and retry policy mutation remain disabled.",
        blocking_signal="Do-not-retry status is treated as guard mutation, retry policy mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
    ),
    GovernancePackSection(
        section_order=6,
        section_id="source-provenance-pack-section",
        section_name="Source/provenance pack section",
        source_status_surface="P4-M1.5 Source / Provenance Verification Status.",
        export_purpose="Package the P4-M1.5 source/provenance verification status surface for human audit.",
        allowed_export_output="Read-only source/provenance package material without fetching, trusting, writing, or mutating source/provenance records.",
        prohibited_automation="No source fetching, source trust, provenance writing, source/provenance/evidence/citation mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        human_audit_signal="The P4-M1.5 source/provenance surface is present without source fetch, trust, write, or mutation behavior.",
        blocking_signal="Source/provenance status is treated as source fetch, source trust, provenance write, mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.5 Source / Provenance Verification Status.",
    ),
    GovernancePackSection(
        section_order=7,
        section_id="decision-readiness-pack-section",
        section_name="Decision readiness pack section",
        source_status_surface="P4-M1.6 Decision Readiness Status.",
        export_purpose="Package the P4-M1.6 decision readiness status surface for human audit without generating a verdict.",
        allowed_export_output="Read-only decision readiness package material while automatic readiness verdict and decision execution remain disabled.",
        prohibited_automation="No automatic readiness verdict, decision recommendation, decision ranking, approval, rejection, authorization, execution, memory write, or proposal mutation.",
        human_audit_signal="The P4-M1.6 decision readiness surface is present while automatic readiness verdict remains disabled.",
        blocking_signal="Decision readiness status is converted into recommendation, ranking, automatic readiness, authorization, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.6 Decision Readiness Status.",
    ),
    GovernancePackSection(
        section_order=8,
        section_id="manual-decision-preview-pack-section",
        section_name="Manual decision preview pack section",
        source_status_surface="P4-M1.7 Manual Decision Preview.",
        export_purpose="Package the P4-M1.7 manual decision preview surface for human audit without recommending, ranking, deciding, or executing.",
        allowed_export_output="Read-only manual decision preview package material for human audit, archive, handoff, and review.",
        prohibited_automation="No decision recommendation, decision ranking, automatic readiness verdict, approval, rejection, execution, authorization, memory write, or mutation.",
        human_audit_signal="The P4-M1.7 manual decision preview surface is present as advisory package material.",
        blocking_signal="Manual decision preview is converted into recommendation, ranking, readiness verdict, authorization, approval, rejection, write, mutation, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.7 Manual Decision Preview.",
    ),
    GovernancePackSection(
        section_order=9,
        section_id="unified-governance-pack",
        section_name="Unified governance pack",
        source_status_surface="Unified P4-M1.0 through P4-M1.7 read-only governance surfaces.",
        export_purpose="Package P4-M1.0 through P4-M1.7 together for human audit only.",
        allowed_export_output="Unified read-only governance pack for human audit, archive, handoff, and review only.",
        prohibited_automation="No decision recommendation, ranking, automatic readiness verdict, approval, rejection, execution, memory write, state mutation, import, ingest, injection, agent call, API/MCP/connector behavior, v7, or productization.",
        human_audit_signal="All eight P4-M1 source status surfaces are visible together as advisory export material.",
        blocking_signal="Any required source surface is absent or the unified pack grants recommendation, readiness, authorization, approval, rejection, write, mutation, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 through P4-M1.7 read-only governance corridor.",
    ),
    GovernancePackSection(
        section_order=10,
        section_id="export-not-decision",
        section_name="Export is not a decision",
        source_status_surface="P4-M1.8 Governance Pack Export boundary.",
        export_purpose="State that governance pack export does not recommend, rank, decide, approve, reject, execute, or write memory.",
        allowed_export_output="Boundary language proving export is advisory package material only.",
        prohibited_automation="No recommendation, ranking, decision, approval, rejection, execution, memory write, memory record mutation, proposal mutation, lifecycle mutation, do-not-retry mutation, retry policy mutation, or provenance write.",
        human_audit_signal="The export explicitly states that no decision recommendation, ranking, approval, rejection, execution, or memory write is performed.",
        blocking_signal="Any recommendation, ranking, decision, approval, rejection, execution, memory write, or state mutation is produced.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only governance corridor.",
    ),
    GovernancePackSection(
        section_order=11,
        section_id="automation-boundary-intact",
        section_name="Automation boundary intact",
        source_status_surface="P4-M1.8 disabled automation status report.",
        export_purpose="Prove disabled recommendation, ranking, readiness verdict, execution, approval, rejection, write, mutation, import, ingest, injection, agent, API/MCP/connector, v7, and productization flags.",
        allowed_export_output="Report disabled decision recommendation, decision ranking, automatic readiness verdict, execution, approval, rejection, memory write, memory/proposal/lifecycle/do-not-retry/retry-policy/source/provenance mutation, source fetching, import, ingestion, injection, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No recommendation, ranking, readiness verdict, decision, execution, approval, rejection, write, mutation, fetch, import, ingest, injection, agent call, API/MCP/connector behavior, v7 start, or productization.",
        human_audit_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled, a recommendation or verdict is emitted, a decision is executed, state is mutated, or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.7 read-only/manual boundary discipline.",
    ),
)


def list_governance_pack_sections() -> tuple[GovernancePackSection, ...]:
    return _GOVERNANCE_PACK_SECTIONS


def governance_pack_section_ids() -> tuple[str, ...]:
    return tuple(section.section_id for section in list_governance_pack_sections())


def render_governance_pack_markdown(
    sections: Sequence[GovernancePackSection] | None = None,
) -> str:
    section_values = (
        tuple(sections) if sections is not None else list_governance_pack_sections()
    )
    status = governance_pack_export_report()
    lines = [
        "# P4-M1.8 Governance Pack Export",
        "",
        "P4-M1.8 is governance pack export only.",
        "",
        "Governance pack export is read-only.",
        "",
        "Governance pack export is advisory only.",
        "",
        "Governance pack export is for human audit, archive, handoff, and review only.",
        "",
        "No decision recommendation is performed by this export.",
        "",
        "No decision ranking is performed by this export.",
        "",
        "No automatic readiness verdict is performed by this export.",
        "",
        "No decision execution is performed by this export.",
        "",
        "No approval or rejection is performed by this export.",
        "",
        "No memory writing is performed by this export.",
        "",
        "No proposal mutation is performed by this export.",
        "",
        "No lifecycle mutation is performed by this export.",
        "",
        "No do-not-retry mutation is performed by this export.",
        "",
        "No source/provenance mutation is performed by this export.",
        "",
        "No API/MCP/connector behavior is performed by this export.",
        "",
        GOVERNANCE_PACK_EXPORT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Governance Pack Sections", ""])
    for section in section_values:
        lines.extend(
            [
                f"### {section.section_order}. {section.section_id}",
                "",
                f"- Section name: {section.section_name}",
                f"- Source status surface: {section.source_status_surface}",
                f"- Export purpose: {section.export_purpose}",
                f"- Allowed export output: {section.allowed_export_output}",
                f"- Prohibited automation: {section.prohibited_automation}",
                f"- Human audit signal: {section.human_audit_signal}",
                f"- Blocking signal: {section.blocking_signal}",
                f"- P4-M0/P4-M1 dependency: {section.p4_m0_or_p4_m1_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def governance_pack_as_dicts(
    sections: Sequence[GovernancePackSection] | None = None,
) -> tuple[dict[str, object], ...]:
    section_values = (
        tuple(sections) if sections is not None else list_governance_pack_sections()
    )
    return tuple(asdict(section) for section in section_values)


def governance_pack_export_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.8",
        "feature": "Governance Pack Export",
        "mode": "read-only",
        "pack_section_count": len(_GOVERNANCE_PACK_SECTIONS),
        "governance_pack_export_read_only": True,
        "governance_pack_export_advisory_only": True,
        "human_audit_archive_handoff_review_only": True,
        "automatic_decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
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
        "package_version": P4_M1_8_PACKAGE_VERSION,
        "boundary": GOVERNANCE_PACK_EXPORT_BOUNDARY,
    }
