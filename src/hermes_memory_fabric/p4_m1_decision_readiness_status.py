from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_6_PACKAGE_VERSION = "6.16.0"

DECISION_READINESS_STATUS_BOUNDARY = (
    "P4-M1.6 is read-only decision readiness status only and advisory only. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not execute decisions. "
    "It does not approve memory. It does not reject memory. "
    "It does not approve proposals. It does not reject proposals. "
    "It does not write memory. It does not create memory records. "
    "It does not update memory records. It does not delete memory records. "
    "It does not mutate proposal records. It does not mutate lifecycle records. "
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
class DecisionReadinessStatusItem:
    verification_order: int
    verification_id: str
    verification_name: str
    human_verification_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_DECISION_READINESS_STATUS_ITEMS: tuple[DecisionReadinessStatusItem, ...] = (
    DecisionReadinessStatusItem(
        verification_order=1,
        verification_id="checklist-readiness-visible",
        verification_name="Checklist readiness visible",
        human_verification_question="Can the human see the P4-M1.0 checklist readiness requirement before any later decision?",
        allowed_system_output="Show checklist readiness prerequisites for human inspection only.",
        prohibited_automation="No automatic readiness verdict, approval, rejection, decision, execution, memory write, or proposal mutation.",
        ready_signal="The P4-M1.0 checklist readiness requirement is visible without automatic readiness determination.",
        blocking_signal="Checklist readiness is hidden or converted into an automatic readiness, approval, rejection, decision, or execution verdict.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 Human-Gated Memory Loop Checklist.",
    ),
    DecisionReadinessStatusItem(
        verification_order=2,
        verification_id="proposal-review-readiness-visible",
        verification_name="Proposal review readiness visible",
        human_verification_question="Can the human see proposal review status requirements before any later decision?",
        allowed_system_output="Show proposal review readiness prerequisites for human inspection only.",
        prohibited_automation="No proposal approval, proposal rejection, proposal mutation, memory approval, memory rejection, or decision execution.",
        ready_signal="Proposal review status requirements are visible without mutating proposal records or approving/rejecting anything.",
        blocking_signal="Proposal review status is hidden or treated as approval, rejection, mutation, authorization, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 Human-Gated Proposal Review Status.",
    ),
    DecisionReadinessStatusItem(
        verification_order=3,
        verification_id="recall-readiness-visible",
        verification_name="Recall readiness visible",
        human_verification_question="Can the human see recall verification status requirements before any later decision?",
        allowed_system_output="Show recall verification prerequisites for human inspection only.",
        prohibited_automation="No recall verdict, automatic readiness determination, memory write, proposal mutation, approval, rejection, or decision execution.",
        ready_signal="Recall verification status requirements are visible without generating an automatic verdict.",
        blocking_signal="Recall verification status is hidden or treated as readiness, approval, rejection, decision, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 Human-Gated Recall Verification Status.",
    ),
    DecisionReadinessStatusItem(
        verification_order=4,
        verification_id="lifecycle-readiness-visible",
        verification_name="Lifecycle readiness visible",
        human_verification_question="Can the human see lifecycle verification status requirements before any later decision?",
        allowed_system_output="Show lifecycle verification prerequisites for human inspection only.",
        prohibited_automation="No lifecycle mutation, lifecycle verdict, automatic readiness determination, approval, rejection, or decision execution.",
        ready_signal="Lifecycle verification status requirements are visible while lifecycle mutation remains disabled.",
        blocking_signal="Lifecycle requirements are hidden or treated as lifecycle mutation, approval, rejection, decision, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.3 Human-Gated Lifecycle Verification Status.",
    ),
    DecisionReadinessStatusItem(
        verification_order=5,
        verification_id="do-not-retry-readiness-visible",
        verification_name="Do-not-retry readiness visible",
        human_verification_question="Can the human see do-not-retry verification status requirements before any later decision?",
        allowed_system_output="Show do-not-retry verification prerequisites for human inspection only.",
        prohibited_automation="No do-not-retry guard mutation, retry policy mutation, automatic readiness determination, approval, rejection, or decision execution.",
        ready_signal="Do-not-retry verification status requirements are visible while guard and retry-policy mutation remain disabled.",
        blocking_signal="Do-not-retry requirements are hidden or treated as guard mutation, retry policy mutation, approval, rejection, write, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.4 Human-Gated Do-Not-Retry Verification Status.",
    ),
    DecisionReadinessStatusItem(
        verification_order=6,
        verification_id="source-provenance-readiness-visible",
        verification_name="Source/provenance readiness visible",
        human_verification_question="Can the human see source/provenance verification status requirements before any later decision?",
        allowed_system_output="Show source/provenance verification prerequisites for human inspection only.",
        prohibited_automation="No source fetching, source trust, provenance writing, source/provenance/evidence/citation mutation, approval, rejection, or decision execution.",
        ready_signal="Source/provenance verification status requirements are visible without fetching, trusting, writing, or mutating source/provenance records.",
        blocking_signal="Source/provenance requirements are hidden or treated as source trust, provenance write, mutation, approval, rejection, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.5 Source / Provenance Verification Status.",
    ),
    DecisionReadinessStatusItem(
        verification_order=7,
        verification_id="decision-inputs-visible",
        verification_name="Decision inputs visible",
        human_verification_question="Can the human see required decision inputs without automatic readiness verdict?",
        allowed_system_output="List decision input visibility requirements as advisory status only.",
        prohibited_automation="No automatic readiness verdict, decision, approval, rejection, authorization, execution, memory write, or proposal mutation.",
        ready_signal="Decision inputs are visible while automatic readiness verdict and decision execution remain disabled.",
        blocking_signal="Decision inputs are hidden or converted into automatic readiness, decision, approval, rejection, authorization, or execution.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 through P4-M1.5 read-only status surfaces.",
    ),
    DecisionReadinessStatusItem(
        verification_order=8,
        verification_id="decision-not-taken",
        verification_name="Decision not taken",
        human_verification_question="Is it clear this status does not approve, reject, execute, or write memory?",
        allowed_system_output="Report that decision, approval, rejection, execution, and memory writing are disabled by this feature.",
        prohibited_automation="No decision, decision execution, approval, rejection, memory write, memory record mutation, proposal mutation, or lifecycle mutation.",
        ready_signal="The report states no decision is taken and no memory/proposal/lifecycle/do-not-retry/source/provenance state is changed.",
        blocking_signal="Any approval, rejection, execution, memory write, proposal mutation, lifecycle mutation, do-not-retry mutation, or provenance write occurs.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only governance corridor.",
    ),
    DecisionReadinessStatusItem(
        verification_order=9,
        verification_id="automation-boundary-intact",
        verification_name="Automation boundary intact",
        human_verification_question="Are disabled readiness verdict, decision execution, approval, rejection, memory write, proposal mutation, lifecycle mutation, do-not-retry mutation, source/provenance mutation, import, agent, API/MCP, v7, and productization flags intact?",
        allowed_system_output="Report disabled automatic readiness verdict, decision execution, approval, rejection, memory write, memory/proposal/lifecycle/do-not-retry/retry-policy/source/provenance mutation, source fetching, import, ingestion, injection, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No readiness verdict, decision, execution, approval, rejection, write, mutation, fetch, import, ingest, injection, agent call, API/MCP/connector behavior, v7 start, or productization.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled, an automatic verdict is emitted, a decision is executed, state is mutated, or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.5 read-only/manual boundary discipline.",
    ),
)


def list_decision_readiness_status_items() -> tuple[DecisionReadinessStatusItem, ...]:
    return _DECISION_READINESS_STATUS_ITEMS


def decision_readiness_status_ids() -> tuple[str, ...]:
    return tuple(item.verification_id for item in list_decision_readiness_status_items())


def render_decision_readiness_status_markdown(
    items: Sequence[DecisionReadinessStatusItem] | None = None,
) -> str:
    item_values = (
        tuple(items) if items is not None else list_decision_readiness_status_items()
    )
    status = decision_readiness_status_report()
    lines = [
        "# P4-M1.6 Decision Readiness Status",
        "",
        "P4-M1.6 is decision readiness status only.",
        "",
        "Decision readiness status is advisory only.",
        "",
        "No automatic readiness verdict is performed by this status.",
        "",
        "No decision execution is performed by this status.",
        "",
        "No approval or rejection is performed by this status.",
        "",
        "No memory writing is performed by this status.",
        "",
        "No proposal mutation is performed by this status.",
        "",
        "No lifecycle mutation is performed by this status.",
        "",
        "No do-not-retry mutation is performed by this status.",
        "",
        "No source/provenance mutation is performed by this status.",
        "",
        "No API/MCP/connector behavior is performed by this status.",
        "",
        DECISION_READINESS_STATUS_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Verification Items", ""])
    for item in item_values:
        lines.extend(
            [
                f"### {item.verification_order}. {item.verification_id}",
                "",
                f"- Verification name: {item.verification_name}",
                f"- Human verification question: {item.human_verification_question}",
                f"- Allowed system output: {item.allowed_system_output}",
                f"- Prohibited automation: {item.prohibited_automation}",
                f"- Ready signal: {item.ready_signal}",
                f"- Blocking signal: {item.blocking_signal}",
                f"- P4-M0/P4-M1 dependency: {item.p4_m0_or_p4_m1_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def decision_readiness_status_as_dicts(
    items: Sequence[DecisionReadinessStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items) if items is not None else list_decision_readiness_status_items()
    )
    return tuple(asdict(item) for item in item_values)


def decision_readiness_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.6",
        "feature": "Decision Readiness Status",
        "mode": "read-only",
        "verification_item_count": len(_DECISION_READINESS_STATUS_ITEMS),
        "decision_readiness_status_advisory_only": True,
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
        "package_version": P4_M1_6_PACKAGE_VERSION,
        "boundary": DECISION_READINESS_STATUS_BOUNDARY,
    }
