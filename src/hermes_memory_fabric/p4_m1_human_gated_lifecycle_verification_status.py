from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_3_PACKAGE_VERSION = "6.16.0"

HUMAN_GATED_LIFECYCLE_VERIFICATION_STATUS_BOUNDARY = (
    "P4-M1.3 is read-only lifecycle verification status only and advisory only. "
    "It does not archive memory. It does not mark memory stale. "
    "It does not clean up memory. It does not delete memory. "
    "It does not change lifecycle state. It does not mutate lifecycle records. "
    "It does not write memory. It does not approve memory. "
    "It does not reject memory. It does not mutate proposal records. "
    "It does not inject memory into agents. It does not bulk import memory. "
    "It does not auto-ingest chat history. It does not auto-ingest files. "
    "It does not auto-ingest external systems. It does not call agents. "
    "It does not call external APIs. It does not create API/MCP/connector behavior. "
    "It does not start v7. It does not productize. "
    "It does not grant authorization semantics. It does not grant execution semantics."
)


@dataclass(frozen=True)
class HumanGatedLifecycleVerificationStatusItem:
    verification_order: int
    verification_id: str
    verification_name: str
    human_verification_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_LIFECYCLE_VERIFICATION_STATUS_ITEMS: tuple[HumanGatedLifecycleVerificationStatusItem, ...] = (
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=1,
        verification_id="lifecycle-state-visible",
        verification_name="Lifecycle state visible",
        human_verification_question="Can the human see current or intended lifecycle state before any decision?",
        allowed_system_output="Show lifecycle state context for human inspection only.",
        prohibited_automation="No lifecycle state change, lifecycle record mutation, archive, stale marking, cleanup, or deletion.",
        ready_signal="The current or intended lifecycle state is visible before any later manual decision.",
        blocking_signal="The lifecycle state is hidden, changed, or treated as already decided.",
        p4_m0_or_p4_m1_dependency="P4-M0.4 lifecycle state and P4-M1 human-gated inspection discipline.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=2,
        verification_id="archive-plan-visible",
        verification_name="Archive plan visible",
        human_verification_question="Can the human see an archive plan as a later optional manual action?",
        allowed_system_output="Describe any later manual archive plan without archiving memory.",
        prohibited_automation="No automatic archive, lifecycle update, cleanup, deletion, approval, or memory write.",
        ready_signal="Archive handling is visible only as a later optional manual plan.",
        blocking_signal="The status archives memory or implies archive has already been approved.",
        p4_m0_or_p4_m1_dependency="P4-M0.4 archived lifecycle state remains manual.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=3,
        verification_id="stale-plan-visible",
        verification_name="Stale plan visible",
        human_verification_question="Can the human see stale marking as a later optional manual action?",
        allowed_system_output="Describe later manual stale marking without marking memory stale.",
        prohibited_automation="No automatic stale marking, lifecycle update, cleanup, deletion, approval, or memory write.",
        ready_signal="Stale handling is visible only as a later optional manual plan.",
        blocking_signal="The status marks memory stale or implies stale marking has already been approved.",
        p4_m0_or_p4_m1_dependency="P4-M0.4 stale lifecycle state remains manual.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=4,
        verification_id="cleanup-plan-visible",
        verification_name="Cleanup plan visible",
        human_verification_question="Can the human see cleanup as a later optional manual action?",
        allowed_system_output="Describe later manual cleanup without cleaning up memory or lifecycle records.",
        prohibited_automation="No automatic cleanup, archive, stale marking, deletion, lifecycle update, or memory write.",
        ready_signal="Cleanup is visible only as a later optional manual plan.",
        blocking_signal="The status cleans up memory, deletes files, or mutates lifecycle records.",
        p4_m0_or_p4_m1_dependency="P4-M0 local store remains separate from P4-M1 read-only status surfaces.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=5,
        verification_id="delete-not-taken",
        verification_name="Delete not taken",
        human_verification_question="Is it clear this status does not delete memory or approve deletion?",
        allowed_system_output="State that deletion and deletion approval are disabled by this status.",
        prohibited_automation="No deletion, delete approval, cleanup delete, lifecycle mutation, or proposal mutation.",
        ready_signal="Deletion remains disabled and no delete approval is granted.",
        blocking_signal="Any memory, proposal, lifecycle record, or storage file is deleted or deletion is approved.",
        p4_m0_or_p4_m1_dependency="P4-M1 manual-review boundary and P4-M0 local persistence safety.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=6,
        verification_id="state-mutation-not-taken",
        verification_name="State mutation not taken",
        human_verification_question="Is it clear this status does not change lifecycle state?",
        allowed_system_output="State that lifecycle mutation and lifecycle record mutation are disabled.",
        prohibited_automation="No lifecycle-set, lifecycle-update, lifecycle-mutate, archive, stale marking, cleanup, or deletion.",
        ready_signal="Lifecycle mutation flags remain disabled.",
        blocking_signal="Any lifecycle state, lifecycle record, memory record, or proposal record changes.",
        p4_m0_or_p4_m1_dependency="P4-M0.4 lifecycle state command remains separate from this P4-M1.3 status.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=7,
        verification_id="manual-review-required",
        verification_name="Manual review required",
        human_verification_question="Is manual inspection of lifecycle impact required before any later action?",
        allowed_system_output="State that a human must manually inspect lifecycle impact before later action.",
        prohibited_automation="No automatic lifecycle decision, authorization, execution, approval, rejection, or write.",
        ready_signal="Manual human review remains required before lifecycle handling proceeds.",
        blocking_signal="The status implies lifecycle handling is authorized, executed, or already approved.",
        p4_m0_or_p4_m1_dependency="P4-M1 human-gated memory loop checklist.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=8,
        verification_id="proposal-memory-unchanged",
        verification_name="Proposal and memory unchanged",
        human_verification_question="Is it clear no proposal or memory record is changed?",
        allowed_system_output="Report disabled memory writing, approval, rejection, and proposal mutation flags.",
        prohibited_automation="No memory write, approval, rejection, proposal mutation, import, ingest, or injection.",
        ready_signal="Proposal and memory records remain unchanged by this status.",
        blocking_signal="Any proposal record, memory record, approval, rejection, import, ingest, or injection occurs.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 proposal review status and P4-M1.2 recall verification status.",
    ),
    HumanGatedLifecycleVerificationStatusItem(
        verification_order=9,
        verification_id="automation-boundary-intact",
        verification_name="Automation boundary intact",
        human_verification_question="Are lifecycle mutation/archive/stale/cleanup/delete/write/approval/rejection/import/agent/API/MCP/v7/productization flags disabled?",
        allowed_system_output="Report disabled lifecycle mutation, archive, stale marking, cleanup, delete, write, approval, rejection, import, ingestion, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No lifecycle mutation/archive/stale/cleanup/delete/write/approval/rejection/import/ingest/agent/API/MCP/connector/v7/productization behavior.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.2 read-only and manual boundary discipline.",
    ),
)


def list_human_gated_lifecycle_verification_status_items() -> tuple[
    HumanGatedLifecycleVerificationStatusItem, ...
]:
    return _LIFECYCLE_VERIFICATION_STATUS_ITEMS


def human_gated_lifecycle_verification_status_ids() -> tuple[str, ...]:
    return tuple(
        item.verification_id for item in list_human_gated_lifecycle_verification_status_items()
    )


def render_human_gated_lifecycle_verification_status_markdown(
    items: Sequence[HumanGatedLifecycleVerificationStatusItem] | None = None,
) -> str:
    item_values = (
        tuple(items)
        if items is not None
        else list_human_gated_lifecycle_verification_status_items()
    )
    status = human_gated_lifecycle_verification_status_report()
    lines = [
        "# P4-M1.3 Human-Gated Lifecycle Verification Status",
        "",
        "P4-M1.3 is lifecycle verification status only.",
        "",
        "Lifecycle verification status is advisory only.",
        "",
        "No archive is performed by this status.",
        "",
        "No stale marking is performed by this status.",
        "",
        "No cleanup is performed by this status.",
        "",
        "No deletion is performed by this status.",
        "",
        "No lifecycle mutation is performed by this status.",
        "",
        "No memory or proposal mutation is performed by this status.",
        "",
        HUMAN_GATED_LIFECYCLE_VERIFICATION_STATUS_BOUNDARY,
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


def human_gated_lifecycle_verification_status_as_dicts(
    items: Sequence[HumanGatedLifecycleVerificationStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items)
        if items is not None
        else list_human_gated_lifecycle_verification_status_items()
    )
    return tuple(asdict(item) for item in item_values)


def human_gated_lifecycle_verification_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.3",
        "feature": "Human-Gated Lifecycle Verification Status",
        "mode": "read-only",
        "verification_item_count": len(_LIFECYCLE_VERIFICATION_STATUS_ITEMS),
        "lifecycle_verification_status_advisory_only": True,
        "lifecycle_mutation_enabled": False,
        "archive_enabled": False,
        "stale_marking_enabled": False,
        "cleanup_enabled": False,
        "delete_enabled": False,
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
        "package_version": P4_M1_3_PACKAGE_VERSION,
        "boundary": HUMAN_GATED_LIFECYCLE_VERIFICATION_STATUS_BOUNDARY,
    }
