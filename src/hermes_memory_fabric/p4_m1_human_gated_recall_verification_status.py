from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_2_PACKAGE_VERSION = "6.16.0"

HUMAN_GATED_RECALL_VERIFICATION_STATUS_BOUNDARY = (
    "P4-M1.2 is read-only recall verification status only and advisory only. "
    "It does not run recall automatically. It does not claim recall passed. "
    "It does not claim recall failed. It does not write memory. "
    "It does not approve memory. It does not reject memory. "
    "It does not mutate proposal records. It does not inject memory into agents. "
    "It does not bulk import memory. It does not auto-ingest chat history. "
    "It does not auto-ingest files. It does not auto-ingest external systems. "
    "It does not call agents. It does not call external APIs. "
    "It does not create API/MCP/connector behavior. It does not start v7. "
    "It does not productize. It does not grant authorization semantics. "
    "It does not grant execution semantics."
)


@dataclass(frozen=True)
class HumanGatedRecallVerificationStatusItem:
    verification_order: int
    verification_id: str
    verification_name: str
    human_verification_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_RECALL_VERIFICATION_STATUS_ITEMS: tuple[HumanGatedRecallVerificationStatusItem, ...] = (
    HumanGatedRecallVerificationStatusItem(
        verification_order=1,
        verification_id="query-visible",
        verification_name="Query visible",
        human_verification_question="Can the human see the recall query before verification?",
        allowed_system_output="Show the intended recall query for human inspection.",
        prohibited_automation="No automatic recall execution, pass claim, fail claim, or agent call.",
        ready_signal="The recall query is visible before any later manual recall run.",
        blocking_signal="The human cannot inspect the recall query before verification.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 recall-verification gate and P4-M1.1 recall plan visibility.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=2,
        verification_id="scope-visible",
        verification_name="Scope visible",
        human_verification_question="Can the human see project, namespace, or scope before verification?",
        allowed_system_output="Show available project, namespace, and scope context without fetching external systems.",
        prohibited_automation="No scope enrichment, external API call, memory injection, or hidden expansion.",
        ready_signal="Project, namespace, or scope is visible or explicitly absent.",
        blocking_signal="Project, namespace, or scope is hidden, fabricated, or externally enriched.",
        p4_m0_or_p4_m1_dependency="P4-M0 workspace/project scoping and P4-M1.1 scope boundary visibility.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=3,
        verification_id="candidate-memory-visible",
        verification_name="Candidate memory visible",
        human_verification_question="Can the human see what memory or candidate would be checked?",
        allowed_system_output="Show candidate memory/proposal context for human inspection only.",
        prohibited_automation="No memory write, approval, rejection, proposal mutation, or recall result injection.",
        ready_signal="The memory or candidate to be checked is visible to the human.",
        blocking_signal="The memory or candidate is hidden, changed, approved, rejected, or written by this status.",
        p4_m0_or_p4_m1_dependency="P4-M0.7 project seed candidates and P4-M1.1 proposal visibility.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=4,
        verification_id="trace-plan-visible",
        verification_name="Trace plan visible",
        human_verification_question="Can the human see that explainable trace should be inspected later?",
        allowed_system_output="Describe later manual inspection of explainable trace without running recall.",
        prohibited_automation="No automatic trace execution, trace verdict, recall pass/fail, or agent injection.",
        ready_signal="A later manual explainable-trace inspection step is visible.",
        blocking_signal="The status claims trace inspection has already run or decided the result.",
        p4_m0_or_p4_m1_dependency="P4-M0.5 explainable recall trace.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=5,
        verification_id="manual-review-required",
        verification_name="Manual review required",
        human_verification_question="Is manual inspection of recall result and trace clearly required?",
        allowed_system_output="State that the human must manually inspect recall result and trace later.",
        prohibited_automation="No automatic recall truth judgment, quality verdict, pass, fail, approval, or write.",
        ready_signal="Manual human review remains required before trust or continuity is inferred.",
        blocking_signal="The status implies the recall result or trace has already been manually accepted.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 human content review and recall-verification gates.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=6,
        verification_id="pass-fail-not-taken",
        verification_name="Pass/fail not taken",
        human_verification_question="Is it clear this status does not claim recall passed or failed?",
        allowed_system_output="State that no recall pass or fail claim is made by this status.",
        prohibited_automation="No automatic recall pass, automatic recall fail, approval, rejection, or proposal mutation.",
        ready_signal="The status remains advisory and contains no pass/fail recall verdict.",
        blocking_signal="The status claims recall passed, recall failed, or changes proposal/memory state.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 decision-not-taken and recall-plan-visible items.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=7,
        verification_id="no-agent-injection",
        verification_name="No agent injection",
        human_verification_question="Is it clear no recall result is injected into agents?",
        allowed_system_output="Report that memory injection and agent calls are disabled.",
        prohibited_automation="No Codex, Hermes, ChatGPT, agent call, auto-injection, or memory injection.",
        ready_signal="Agent call and memory injection flags remain disabled.",
        blocking_signal="Any recall result is sent to or injected into an agent.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 and P4-M1.1 no-agent boundary discipline.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=8,
        verification_id="no-memory-write",
        verification_name="No memory write",
        human_verification_question="Is it clear no memory write, approval, rejection, or proposal mutation happens?",
        allowed_system_output="Report disabled memory writing, approval, rejection, and proposal mutation flags.",
        prohibited_automation="No memory write, approval, rejection, proposal mutation, import, ingest, or approved memory creation.",
        ready_signal="Write, approval, rejection, and proposal mutation flags remain disabled.",
        blocking_signal="Any proposal record, approved memory, approval, rejection, or memory file is created or changed.",
        p4_m0_or_p4_m1_dependency="P4-M0.2 manual write commands remain separate from P4-M1 read-only status surfaces.",
    ),
    HumanGatedRecallVerificationStatusItem(
        verification_order=9,
        verification_id="automation-boundary-intact",
        verification_name="Automation boundary intact",
        human_verification_question="Are recall execution, write, approval, rejection, import, agent, API/MCP, v7, and productization disabled?",
        allowed_system_output="Report disabled recall execution, pass/fail, write, approval, rejection, import, ingestion, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No recall execution/write/approval/rejection/import/ingest/agent/API/MCP/connector/v7/productization behavior.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.1 read-only and manual boundary discipline.",
    ),
)


def list_human_gated_recall_verification_status_items() -> tuple[HumanGatedRecallVerificationStatusItem, ...]:
    return _RECALL_VERIFICATION_STATUS_ITEMS


def human_gated_recall_verification_status_ids() -> tuple[str, ...]:
    return tuple(item.verification_id for item in list_human_gated_recall_verification_status_items())


def render_human_gated_recall_verification_status_markdown(
    items: Sequence[HumanGatedRecallVerificationStatusItem] | None = None,
) -> str:
    item_values = (
        tuple(items) if items is not None else list_human_gated_recall_verification_status_items()
    )
    status = human_gated_recall_verification_status_report()
    lines = [
        "# P4-M1.2 Human-Gated Recall Verification Status",
        "",
        "P4-M1.2 is recall verification status only.",
        "",
        "Recall verification status is advisory only.",
        "",
        "No recall execution is performed by this status.",
        "",
        "No recall pass/fail is claimed by this status.",
        "",
        "No memory or agent injection is performed by this status.",
        "",
        HUMAN_GATED_RECALL_VERIFICATION_STATUS_BOUNDARY,
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


def human_gated_recall_verification_status_as_dicts(
    items: Sequence[HumanGatedRecallVerificationStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items) if items is not None else list_human_gated_recall_verification_status_items()
    )
    return tuple(asdict(item) for item in item_values)


def human_gated_recall_verification_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.2",
        "feature": "Human-Gated Recall Verification Status",
        "mode": "read-only",
        "verification_item_count": len(_RECALL_VERIFICATION_STATUS_ITEMS),
        "recall_verification_status_advisory_only": True,
        "recall_execution_enabled": False,
        "automatic_recall_pass_enabled": False,
        "automatic_recall_fail_enabled": False,
        "memory_write_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "proposal_mutation_enabled": False,
        "memory_injection_enabled": False,
        "bulk_import_enabled": False,
        "auto_ingest_enabled": False,
        "agent_call_enabled": False,
        "api_mcp_connector_enabled": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M1_2_PACKAGE_VERSION,
        "boundary": HUMAN_GATED_RECALL_VERIFICATION_STATUS_BOUNDARY,
    }
