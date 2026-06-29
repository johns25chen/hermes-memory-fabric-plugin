from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_9_PACKAGE_VERSION = "6.16.0"

FINAL_BOUNDARY_AUDIT_BOUNDARY = (
    "P4-M1.9 is read-only final boundary audit / closure only, advisory only, "
    "and for human audit and P4-M1 closure review only. "
    "P4-M1 closure is not P4-M2 execution. "
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
    "It does not start P4-M2. It does not start v7. "
    "It does not productize. It does not grant authorization semantics. "
    "It does not grant execution semantics."
)


@dataclass(frozen=True)
class FinalBoundaryAuditItem:
    audit_order: int
    audit_id: str
    audit_name: str
    source_status_surface: str
    closure_question: str
    closure_signal: str
    allowed_closure_output: str
    prohibited_automation: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_FINAL_BOUNDARY_AUDIT_ITEMS: tuple[FinalBoundaryAuditItem, ...] = (
    FinalBoundaryAuditItem(
        audit_order=1,
        audit_id="checklist-boundary-audit",
        audit_name="Checklist boundary audit",
        source_status_surface="P4-M1.0 Human-Gated Memory Loop Checklist.",
        closure_question="Is the P4-M1.0 checklist still a read-only human-gated checklist surface?",
        closure_signal="Checklist status is visible as advisory closure evidence only.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.0 checklist boundary.",
        prohibited_automation="No recommendation, ranking, readiness verdict, approval, rejection, execution, memory write, or proposal mutation.",
        blocking_signal="The checklist boundary is missing or converted into recommendation, readiness, approval, rejection, write, mutation, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 Human-Gated Memory Loop Checklist.",
    ),
    FinalBoundaryAuditItem(
        audit_order=2,
        audit_id="proposal-review-boundary-audit",
        audit_name="Proposal review boundary audit",
        source_status_surface="P4-M1.1 Human-Gated Proposal Review Status.",
        closure_question="Is the P4-M1.1 proposal review status still review-only and mutation-free?",
        closure_signal="Proposal review status is visible without proposal approval, rejection, or mutation.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.1 proposal review boundary.",
        prohibited_automation="No proposal approval, proposal rejection, proposal mutation, decision recommendation, ranking, readiness verdict, or execution.",
        blocking_signal="Proposal review status is treated as approval, rejection, mutation, recommendation, ranking, readiness, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 Human-Gated Proposal Review Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=3,
        audit_id="recall-verification-boundary-audit",
        audit_name="Recall verification boundary audit",
        source_status_surface="P4-M1.2 Human-Gated Recall Verification Status.",
        closure_question="Is the P4-M1.2 recall verification status still read-only and verdict-free?",
        closure_signal="Recall verification status is visible without automatic readiness or decision semantics.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.2 recall verification boundary.",
        prohibited_automation="No recall verdict, decision recommendation, decision ranking, automatic readiness verdict, approval, rejection, memory write, or execution.",
        blocking_signal="Recall verification status is treated as recommendation, ranking, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 Human-Gated Recall Verification Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=4,
        audit_id="lifecycle-verification-boundary-audit",
        audit_name="Lifecycle verification boundary audit",
        source_status_surface="P4-M1.3 Human-Gated Lifecycle Verification Status.",
        closure_question="Is the P4-M1.3 lifecycle verification status still read-only and lifecycle-mutation-free?",
        closure_signal="Lifecycle verification status is visible while lifecycle mutation remains disabled.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.3 lifecycle verification boundary.",
        prohibited_automation="No lifecycle mutation, readiness verdict, decision recommendation, approval, rejection, memory write, or execution.",
        blocking_signal="Lifecycle verification status is treated as lifecycle mutation, recommendation, readiness, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.3 Human-Gated Lifecycle Verification Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=5,
        audit_id="do-not-retry-boundary-audit",
        audit_name="Do-not-retry boundary audit",
        source_status_surface="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
        closure_question="Is the P4-M1.4 do-not-retry status still read-only and guard-mutation-free?",
        closure_signal="Do-not-retry status is visible while guard and retry policy mutation remain disabled.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.4 do-not-retry boundary.",
        prohibited_automation="No do-not-retry guard mutation, retry policy mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        blocking_signal="Do-not-retry status is treated as guard mutation, retry policy mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=6,
        audit_id="source-provenance-boundary-audit",
        audit_name="Source/provenance boundary audit",
        source_status_surface="P4-M1.5 Source / Provenance Verification Status.",
        closure_question="Is the P4-M1.5 source/provenance status still read-only without fetching, trusting, writing, or mutating evidence?",
        closure_signal="Source/provenance status is visible without source fetch, trust, write, or mutation behavior.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.5 source/provenance boundary.",
        prohibited_automation="No source fetching, source trust, provenance writing, source/provenance/evidence/citation mutation, decision recommendation, readiness verdict, approval, rejection, or execution.",
        blocking_signal="Source/provenance status is treated as source fetch, source trust, provenance write, mutation, recommendation, readiness, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.5 Source / Provenance Verification Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=7,
        audit_id="decision-readiness-boundary-audit",
        audit_name="Decision readiness boundary audit",
        source_status_surface="P4-M1.6 Decision Readiness Status.",
        closure_question="Is the P4-M1.6 decision readiness status still advisory without automatic readiness verdict or execution?",
        closure_signal="Decision readiness status is visible while automatic readiness verdict and execution remain disabled.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.6 decision readiness boundary.",
        prohibited_automation="No automatic readiness verdict, decision recommendation, decision ranking, approval, rejection, authorization, execution, memory write, or proposal mutation.",
        blocking_signal="Decision readiness status is converted into recommendation, ranking, automatic readiness, authorization, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.6 Decision Readiness Status.",
    ),
    FinalBoundaryAuditItem(
        audit_order=8,
        audit_id="manual-decision-preview-boundary-audit",
        audit_name="Manual decision preview boundary audit",
        source_status_surface="P4-M1.7 Manual Decision Preview.",
        closure_question="Is the P4-M1.7 manual decision preview still preview-only without recommending, ranking, deciding, or executing?",
        closure_signal="Manual decision preview is visible as advisory inspection material only.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.7 manual decision preview boundary.",
        prohibited_automation="No decision recommendation, decision ranking, automatic readiness verdict, approval, rejection, execution, authorization, memory write, or mutation.",
        blocking_signal="Manual decision preview is converted into recommendation, ranking, readiness verdict, authorization, approval, rejection, write, mutation, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.7 Manual Decision Preview.",
    ),
    FinalBoundaryAuditItem(
        audit_order=9,
        audit_id="governance-pack-export-boundary-audit",
        audit_name="Governance pack export boundary audit",
        source_status_surface="P4-M1.8 Governance Pack Export.",
        closure_question="Is the P4-M1.8 governance pack export still read-only package material without granting decision or execution semantics?",
        closure_signal="Governance pack export is visible as advisory package material only.",
        allowed_closure_output="Read-only closure audit text for the P4-M1.8 governance pack export boundary.",
        prohibited_automation="No decision recommendation, ranking, automatic readiness verdict, approval, rejection, execution, authorization, memory write, state mutation, import, ingest, injection, agent call, API/MCP/connector behavior, v7, or productization.",
        blocking_signal="Governance pack export grants recommendation, readiness, authorization, approval, rejection, write, mutation, or execution semantics.",
        p4_m0_or_p4_m1_dependency="P4-M1.8 Governance Pack Export.",
    ),
    FinalBoundaryAuditItem(
        audit_order=10,
        audit_id="p4-m1-read-only-corridor-closure",
        audit_name="P4-M1 read-only corridor closure",
        source_status_surface="P4-M1.0 through P4-M1.8 read-only governance corridor.",
        closure_question="Can P4-M1.0 through P4-M1.8 be inspected together as a read-only closure corridor only?",
        closure_signal="The closure report frames P4-M1.0 through P4-M1.8 as read-only governance closure material.",
        allowed_closure_output="Read-only P4-M1 closure report for human audit and P4-M1 closure review only.",
        prohibited_automation="No automatic closure decision, recommendation, ranking, readiness verdict, approval, rejection, execution, memory write, mutation, import, ingest, injection, agent call, API/MCP/connector behavior, P4-M2 start, v7, or productization.",
        blocking_signal="P4-M1 closure is treated as P4-M2 execution, authorization, decision, approval, rejection, write, mutation, or productization.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 through P4-M1.8 read-only governance surfaces.",
    ),
    FinalBoundaryAuditItem(
        audit_order=11,
        audit_id="p4-m2-not-started",
        audit_name="P4-M2 not started",
        source_status_surface="P4-M1.9 roadmap boundary.",
        closure_question="Does P4-M1.9 avoid starting P4-M2 decision execution hardening?",
        closure_signal="P4-M2 started flag is false and the boundary states P4-M1 closure is not P4-M2 execution.",
        allowed_closure_output="Read-only statement that P4-M2 is not started in P4-M1.9.",
        prohibited_automation="No P4-M2 decision execution hardening, start-p4-m2 command, decision execution, approval, rejection, authorization, write, or mutation.",
        blocking_signal="Any P4-M2 execution, hardening, command, state, authorization, approval, rejection, write, mutation, or readiness verdict is introduced.",
        p4_m0_or_p4_m1_dependency="P4-M1 route lock and P4-M1.9 closure boundary.",
    ),
    FinalBoundaryAuditItem(
        audit_order=12,
        audit_id="v7-productization-not-started",
        audit_name="v7 and productization not started",
        source_status_surface="P4-M1.9 roadmap boundary.",
        closure_question="Does P4-M1.9 avoid starting v7, v6.17, productization, MVP, deployment, UI, Operator Console, or full Memory Graph work?",
        closure_signal="v7 and productization started flags are false and package version remains 6.16.0.",
        allowed_closure_output="Read-only statement that v7 and productization are not started in P4-M1.9.",
        prohibited_automation="No v7 start, v6.17 creation, productization, MVP, deployment, UI, Operator Console, full Memory Graph, dependency, version, tag, or commit behavior.",
        blocking_signal="Any v7, v6.17, productization, MVP, deployment, UI, Operator Console, full Memory Graph, dependency, version, tag, or commit behavior is introduced.",
        p4_m0_or_p4_m1_dependency="P4-M1 route lock and package version 6.16.0.",
    ),
    FinalBoundaryAuditItem(
        audit_order=13,
        audit_id="automation-boundary-intact",
        audit_name="Automation boundary intact",
        source_status_surface="P4-M1.9 disabled automation status report.",
        closure_question="Are all prohibited recommendation, ranking, verdict, execution, approval, rejection, write, mutation, import, ingest, injection, agent, API/MCP/connector, P4-M2, v7, and productization flags disabled?",
        closure_signal="Disabled automation flags remain false and package version remains 6.16.0.",
        allowed_closure_output="Report disabled decision recommendation, decision ranking, automatic readiness verdict, execution, approval, rejection, memory write, memory/proposal/lifecycle/do-not-retry/retry-policy/source/provenance mutation, source fetching, import, ingestion, injection, agent, API/MCP/connector, P4-M2, v7, and productization flags.",
        prohibited_automation="No recommendation, ranking, readiness verdict, decision, execution, approval, rejection, write, mutation, fetch, import, ingest, injection, agent call, API/MCP/connector behavior, P4-M2 start, v7 start, or productization.",
        blocking_signal="Any disabled automation flag is enabled, a recommendation or verdict is emitted, a decision is executed, state is mutated, P4-M2 starts, v7 starts, productization starts, or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.8 read-only/manual boundary discipline.",
    ),
)


def list_final_boundary_audit_items() -> tuple[FinalBoundaryAuditItem, ...]:
    return _FINAL_BOUNDARY_AUDIT_ITEMS


def final_boundary_audit_item_ids() -> tuple[str, ...]:
    return tuple(item.audit_id for item in list_final_boundary_audit_items())


def render_final_boundary_audit_markdown(
    items: Sequence[FinalBoundaryAuditItem] | None = None,
) -> str:
    item_values = (
        tuple(items) if items is not None else list_final_boundary_audit_items()
    )
    status = final_boundary_audit_report()
    lines = [
        "# P4-M1.9 Final Boundary Audit / Closure",
        "",
        "P4-M1.9 is final boundary audit / closure only.",
        "",
        "Final boundary audit is read-only.",
        "",
        "Closure report is advisory only.",
        "",
        "Closure report is for human audit and P4-M1 closure review only.",
        "",
        "P4-M1 closure is not P4-M2 execution.",
        "",
        "No decision recommendation is performed by this closure report.",
        "",
        "No decision ranking is performed by this closure report.",
        "",
        "No automatic readiness verdict is performed by this closure report.",
        "",
        "No decision execution is performed by this closure report.",
        "",
        "No approval or rejection is performed by this closure report.",
        "",
        "No memory writing is performed by this closure report.",
        "",
        "No proposal mutation is performed by this closure report.",
        "",
        "No lifecycle mutation is performed by this closure report.",
        "",
        "No do-not-retry mutation is performed by this closure report.",
        "",
        "No source/provenance mutation is performed by this closure report.",
        "",
        "No API/MCP/connector behavior is performed by this closure report.",
        "",
        "P4-M2 is not started by this closure report.",
        "",
        "v7 is not started by this closure report.",
        "",
        "Productization is not started by this closure report.",
        "",
        FINAL_BOUNDARY_AUDIT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Final Boundary Audit Items", ""])
    for item in item_values:
        lines.extend(
            [
                f"### {item.audit_order}. {item.audit_id}",
                "",
                f"- Audit name: {item.audit_name}",
                f"- Source status surface: {item.source_status_surface}",
                f"- Closure question: {item.closure_question}",
                f"- Closure signal: {item.closure_signal}",
                f"- Allowed closure output: {item.allowed_closure_output}",
                f"- Prohibited automation: {item.prohibited_automation}",
                f"- Blocking signal: {item.blocking_signal}",
                f"- P4-M0/P4-M1 dependency: {item.p4_m0_or_p4_m1_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def final_boundary_audit_as_dicts(
    items: Sequence[FinalBoundaryAuditItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items) if items is not None else list_final_boundary_audit_items()
    )
    return tuple(asdict(item) for item in item_values)


def final_boundary_audit_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.9",
        "feature": "Final Boundary Audit / Closure",
        "mode": "read-only",
        "audit_item_count": len(_FINAL_BOUNDARY_AUDIT_ITEMS),
        "final_boundary_audit_read_only": True,
        "closure_report_advisory_only": True,
        "human_audit_and_closure_review_only": True,
        "p4_m1_closure_only": True,
        "p4_m2_started": False,
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
        "package_version": P4_M1_9_PACKAGE_VERSION,
        "boundary": FINAL_BOUNDARY_AUDIT_BOUNDARY,
    }
