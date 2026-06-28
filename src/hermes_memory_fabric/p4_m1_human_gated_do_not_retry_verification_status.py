from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_4_PACKAGE_VERSION = "6.16.0"

HUMAN_GATED_DO_NOT_RETRY_VERIFICATION_STATUS_BOUNDARY = (
    "P4-M1.4 is read-only do-not-retry verification status only and advisory only. "
    "It does not judge failure automatically. It does not block retry automatically. "
    "It does not mark do-not-retry. It does not create do-not-retry records. "
    "It does not update do-not-retry records. It does not delete do-not-retry records. "
    "It does not mutate guard state. It does not mutate retry policy. "
    "It does not mutate lifecycle records. It does not write memory. "
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
class HumanGatedDoNotRetryVerificationStatusItem:
    verification_order: int
    verification_id: str
    verification_name: str
    human_verification_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_DO_NOT_RETRY_VERIFICATION_STATUS_ITEMS: tuple[
    HumanGatedDoNotRetryVerificationStatusItem, ...
] = (
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=1,
        verification_id="failure-context-visible",
        verification_name="Failure context visible",
        human_verification_question="Can the human see failure context before any do-not-retry decision?",
        allowed_system_output="Show failure context for human inspection only.",
        prohibited_automation="No automatic failure judgment, do-not-retry marking, retry blocking, guard mutation, or policy mutation.",
        ready_signal="Failure context is visible without any automatic failure verdict.",
        blocking_signal="Failure context is hidden or treated as an automatic do-not-retry decision.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 do-not-retry guard remains manual and P4-M1 human-gated inspection discipline.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=2,
        verification_id="retry-scope-visible",
        verification_name="Retry scope visible",
        human_verification_question="Can the human see what action or scope would be retried?",
        allowed_system_output="Describe retry scope for human inspection without retry execution or retry blocking.",
        prohibited_automation="No retry execution, retry blocking, failure verdict, do-not-retry mark, or retry policy mutation.",
        ready_signal="Retry scope is visible before any later manual retry handling.",
        blocking_signal="Retry scope is hidden, blocked automatically, or treated as already decided.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 checklist requires human review before later action.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=3,
        verification_id="blocked-action-visible",
        verification_name="Blocked action visible",
        human_verification_question="Can the human see what action would be blocked only as a later manual possibility?",
        allowed_system_output="Describe a possible later blocked action without blocking retry.",
        prohibited_automation="No automatic retry block, guard-state mutation, do-not-retry record creation, or policy mutation.",
        ready_signal="The possibly blocked action is visible only as a later manual possibility.",
        blocking_signal="The status blocks retry or implies retry blocking has already been authorized.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 do-not-retry guard state remains separate from P4-M1.4 status.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=4,
        verification_id="retry-risk-visible",
        verification_name="Retry risk visible",
        human_verification_question="Can the human see retry risk without automatic failure judgment?",
        allowed_system_output="Report retry risk context as advisory text only.",
        prohibited_automation="No automatic failure judgment, failure verdict, retry blocking, do-not-retry marking, or guard mutation.",
        ready_signal="Retry risk is visible while failure judgment remains disabled.",
        blocking_signal="Retry risk becomes an automatic failure judgment or retry block.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 recall verification status and P4-M1.3 lifecycle verification status remain advisory.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=5,
        verification_id="do-not-retry-plan-visible",
        verification_name="Do-not-retry plan visible",
        human_verification_question="Can the human see a possible do-not-retry plan without marking it?",
        allowed_system_output="Describe a possible later do-not-retry plan without creating or updating any mark.",
        prohibited_automation="No do-not-retry mark, do-not-retry record creation/update/delete, guard-state mutation, or retry policy mutation.",
        ready_signal="A possible do-not-retry plan is visible but not marked.",
        blocking_signal="The status creates, updates, deletes, or implies an active do-not-retry mark.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 do-not-retry guard command remains the separate manual mutation surface.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=6,
        verification_id="do-not-retry-not-marked",
        verification_name="Do-not-retry not marked",
        human_verification_question="Is it clear this status does not create or update do-not-retry marks?",
        allowed_system_output="State that do-not-retry marking and do-not-retry record mutation are disabled.",
        prohibited_automation="No do-not-retry set, update, clear, delete, guard set, guard update, retry-policy set, or retry-policy update.",
        ready_signal="No do-not-retry mark or do-not-retry record is changed by this status.",
        blocking_signal="Any do-not-retry record, guard record, retry policy, lifecycle record, proposal, or memory changes.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 do-not-retry guard tests remain the mutation compatibility boundary.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=7,
        verification_id="manual-review-required",
        verification_name="Manual review required",
        human_verification_question="Must the human manually inspect failure and retry risk before later action?",
        allowed_system_output="State that manual inspection is required before any later do-not-retry or retry action.",
        prohibited_automation="No automatic failure decision, authorization, execution, retry block, do-not-retry mark, approval, rejection, or write.",
        ready_signal="Manual human review remains required before do-not-retry handling proceeds.",
        blocking_signal="The status implies do-not-retry handling is authorized, executed, blocked, or already approved.",
        p4_m0_or_p4_m1_dependency="P4-M1 human-gated memory loop checklist.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=8,
        verification_id="guard-state-unchanged",
        verification_name="Guard state unchanged",
        human_verification_question="Is it clear no do-not-retry guard record or retry policy is changed?",
        allowed_system_output="Report disabled guard-state mutation and retry-policy mutation flags.",
        prohibited_automation="No guard-state mutation, do-not-retry record creation/update/delete, retry policy mutation, lifecycle mutation, or proposal mutation.",
        ready_signal="Guard state and retry policy remain unchanged by this status.",
        blocking_signal="Any guard state, retry policy, lifecycle record, proposal record, or memory record changes.",
        p4_m0_or_p4_m1_dependency="P4-M0.6 guard state remains local and manually operated.",
    ),
    HumanGatedDoNotRetryVerificationStatusItem(
        verification_order=9,
        verification_id="automation-boundary-intact",
        verification_name="Automation boundary intact",
        human_verification_question="Are failure judgment, retry blocking, do-not-retry marking, guard mutation, write, approval, rejection, import, agent, API/MCP, v7, and productization flags disabled?",
        allowed_system_output="Report disabled failure judgment, retry blocking, do-not-retry marking, guard mutation, retry policy mutation, lifecycle mutation, write, approval, rejection, proposal mutation, injection, import, ingestion, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No failure judgment/retry blocking/do-not-retry marking/guard mutation/write/approval/rejection/import/ingest/agent/API/MCP/connector/v7/productization behavior.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.3 read-only and manual boundary discipline.",
    ),
)


def list_human_gated_do_not_retry_verification_status_items() -> tuple[
    HumanGatedDoNotRetryVerificationStatusItem, ...
]:
    return _DO_NOT_RETRY_VERIFICATION_STATUS_ITEMS


def human_gated_do_not_retry_verification_status_ids() -> tuple[str, ...]:
    return tuple(
        item.verification_id
        for item in list_human_gated_do_not_retry_verification_status_items()
    )


def render_human_gated_do_not_retry_verification_status_markdown(
    items: Sequence[HumanGatedDoNotRetryVerificationStatusItem] | None = None,
) -> str:
    item_values = (
        tuple(items)
        if items is not None
        else list_human_gated_do_not_retry_verification_status_items()
    )
    status = human_gated_do_not_retry_verification_status_report()
    lines = [
        "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status",
        "",
        "P4-M1.4 is do-not-retry verification status only.",
        "",
        "Do-not-retry verification status is advisory only.",
        "",
        "No failure judgment is performed by this status.",
        "",
        "No retry blocking is performed by this status.",
        "",
        "No do-not-retry marking is performed by this status.",
        "",
        "No guard state mutation is performed by this status.",
        "",
        "No retry policy mutation is performed by this status.",
        "",
        "No memory or proposal mutation is performed by this status.",
        "",
        HUMAN_GATED_DO_NOT_RETRY_VERIFICATION_STATUS_BOUNDARY,
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


def human_gated_do_not_retry_verification_status_as_dicts(
    items: Sequence[HumanGatedDoNotRetryVerificationStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items)
        if items is not None
        else list_human_gated_do_not_retry_verification_status_items()
    )
    return tuple(asdict(item) for item in item_values)


def human_gated_do_not_retry_verification_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.4",
        "feature": "Human-Gated Do-Not-Retry Verification Status",
        "mode": "read-only",
        "verification_item_count": len(_DO_NOT_RETRY_VERIFICATION_STATUS_ITEMS),
        "do_not_retry_verification_status_advisory_only": True,
        "failure_judgment_enabled": False,
        "retry_blocking_enabled": False,
        "do_not_retry_marking_enabled": False,
        "guard_state_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
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
        "package_version": P4_M1_4_PACKAGE_VERSION,
        "boundary": HUMAN_GATED_DO_NOT_RETRY_VERIFICATION_STATUS_BOUNDARY,
    }
