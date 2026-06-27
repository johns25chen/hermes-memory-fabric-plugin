from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_0_PACKAGE_VERSION = "6.16.0"

HUMAN_GATED_MEMORY_LOOP_BOUNDARY = (
    "P4-M1.0 is read-only checklist/status only. It does not write memory. "
    "It does not approve memory. It does not reject memory. It does not bulk import memory. "
    "It does not auto-ingest chat history. It does not auto-ingest files. "
    "It does not auto-ingest external systems. It does not inject memory into agents. "
    "It does not call agents. It does not call external APIs. "
    "It does not create MCP/connector behavior. It does not start v7. "
    "It does not productize. It does not grant authorization semantics. "
    "It does not grant execution semantics."
)


@dataclass(frozen=True)
class HumanGatedMemoryLoopChecklistItem:
    gate_order: int
    gate_id: str
    gate_name: str
    required_human_action: str
    allowed_system_output: str
    prohibited_automation: str
    validation_signal: str
    p4_m0_dependency: str


_CHECKLIST_ITEMS: tuple[HumanGatedMemoryLoopChecklistItem, ...] = (
    HumanGatedMemoryLoopChecklistItem(
        gate_order=1,
        gate_id="human-intent-requested",
        gate_name="Human intent requested",
        required_human_action="Human explicitly requests a memory-loop action.",
        allowed_system_output="Acknowledge the requested action and present the read-only gate boundary.",
        prohibited_automation="No automatic memory write, approval, rejection, import, ingestion, or agent call.",
        validation_signal="The request is explicit and human-authored before any candidate is considered.",
        p4_m0_dependency="P4-M0 manual operator command boundary.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=2,
        gate_id="candidate-presented",
        gate_name="Candidate presented",
        required_human_action="Human receives a candidate proposal or checklist for review.",
        allowed_system_output="Present deterministic candidate/checklist text only.",
        prohibited_automation="No candidate may be converted into approved memory by this checklist.",
        validation_signal="The candidate is visible before any human review decision.",
        p4_m0_dependency="P4-M0.7 project memory seed candidate and P4-M0.8 approval runbook patterns.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=3,
        gate_id="human-content-review",
        gate_name="Human content review",
        required_human_action="Human reviews proposal/checklist content for accuracy, scope, and boundary fit.",
        allowed_system_output="Provide read-only status, checklist, and boundary statements.",
        prohibited_automation="No truth judgment, freshness judgment, quality scoring, or autonomous review decision.",
        validation_signal="Review remains a human action and is not inferred from system output.",
        p4_m0_dependency="P4-M0.5 explainable recall trace for later manual verification context.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=4,
        gate_id="human-approve-or-reject",
        gate_name="Human approve or reject",
        required_human_action="Human explicitly approves or rejects using an existing/manual action.",
        allowed_system_output="Point to existing/manual action boundaries without performing approval or rejection.",
        prohibited_automation="No approve, reject, approve-all, reject-all, auto-approve, or auto-reject behavior.",
        validation_signal="Approval or rejection is explicit, manual, and outside this P4-M1.0 feature.",
        p4_m0_dependency="P4-M0.2 manual approve/reject operator commands.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=5,
        gate_id="recall-verification",
        gate_name="Recall verification",
        required_human_action="Human recall-verifies approved memory with explicit query and review.",
        allowed_system_output="Return read-only recall output and explainable trace when existing commands are used.",
        prohibited_automation="No automatic recall-verification pass, no automatic memory injection, and no agent call.",
        validation_signal="Human can inspect recall result and trace before trusting continuity.",
        p4_m0_dependency="P4-M0.3 recall pack export and P4-M0.5 explainable recall trace.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=6,
        gate_id="lifecycle-optional",
        gate_name="Lifecycle optional",
        required_human_action="Human optionally sets lifecycle state after approval and review.",
        allowed_system_output="Describe lifecycle as a separate manual operation.",
        prohibited_automation="No automatic lifecycle state assignment, archive, stale marking, cleanup, or deletion.",
        validation_signal="Lifecycle state changes only through a separate human-operated command.",
        p4_m0_dependency="P4-M0.4 Subspace Memory lifecycle state.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=7,
        gate_id="do-not-retry-optional",
        gate_name="Do-not-retry optional",
        required_human_action="Human optionally sets do-not-retry when failed-attempt memory requires it.",
        allowed_system_output="Describe do-not-retry as a separate manual operation.",
        prohibited_automation="No automatic failure detection, automatic blocking, or automatic do-not-retry marking.",
        validation_signal="Do-not-retry state changes only through a separate human-operated command.",
        p4_m0_dependency="P4-M0.6 Subspace Memory do-not-retry guard.",
    ),
    HumanGatedMemoryLoopChecklistItem(
        gate_order=8,
        gate_id="automation-boundary-confirmed",
        gate_name="Automation boundary confirmed",
        required_human_action="Human confirms no automation boundary was crossed.",
        allowed_system_output="Report disabled memory writing, approval, rejection, import, ingestion, agent, API, MCP, connector, v7, and productization flags.",
        prohibited_automation="No API, MCP, connector, external project connection, deployment, UI, product, or execution surface.",
        validation_signal="Status report shows all P4-M1.0 automation flags disabled and package version 6.16.0.",
        p4_m0_dependency="P4-M0 through P4-M0.8 read/write boundary discipline.",
    ),
)


def list_human_gated_memory_loop_checklist_items() -> tuple[HumanGatedMemoryLoopChecklistItem, ...]:
    return _CHECKLIST_ITEMS


def human_gated_memory_loop_checklist_gate_ids() -> tuple[str, ...]:
    return tuple(item.gate_id for item in list_human_gated_memory_loop_checklist_items())


def render_human_gated_memory_loop_checklist_markdown(
    items: Sequence[HumanGatedMemoryLoopChecklistItem] | None = None,
) -> str:
    item_values = tuple(items) if items is not None else list_human_gated_memory_loop_checklist_items()
    status = human_gated_memory_loop_status_report()
    lines = [
        "# P4-M1.0 Human-Gated Memory Loop Checklist",
        "",
        "P4-M1.0 is checklist/status only.",
        "",
        HUMAN_GATED_MEMORY_LOOP_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Human Gates", ""])
    for item in item_values:
        lines.extend(
            [
                f"### {item.gate_order}. {item.gate_id}",
                "",
                f"- Gate name: {item.gate_name}",
                f"- Required human action: {item.required_human_action}",
                f"- Allowed system output: {item.allowed_system_output}",
                f"- Prohibited automation: {item.prohibited_automation}",
                f"- Validation signal: {item.validation_signal}",
                f"- P4-M0 dependency: {item.p4_m0_dependency}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def human_gated_memory_loop_checklist_as_dicts(
    items: Sequence[HumanGatedMemoryLoopChecklistItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = tuple(items) if items is not None else list_human_gated_memory_loop_checklist_items()
    return tuple(asdict(item) for item in item_values)


def human_gated_memory_loop_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.0",
        "feature": "Human-Gated Memory Loop Checklist",
        "mode": "read-only",
        "checklist_count": len(_CHECKLIST_ITEMS),
        "memory_write_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "bulk_import_enabled": False,
        "auto_ingest_enabled": False,
        "agent_call_enabled": False,
        "api_mcp_connector_enabled": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M1_0_PACKAGE_VERSION,
        "boundary": HUMAN_GATED_MEMORY_LOOP_BOUNDARY,
    }
