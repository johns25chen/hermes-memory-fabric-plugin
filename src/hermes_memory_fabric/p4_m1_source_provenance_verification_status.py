from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M1_5_PACKAGE_VERSION = "6.16.0"

SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY = (
    "P4-M1.5 is read-only source/provenance verification status only and advisory only. "
    "It does not fetch sources. It does not browse the web. "
    "It does not call external APIs. It does not call connectors. "
    "It does not create API/MCP/connector behavior. "
    "It does not automatically trust a source. "
    "It does not automatically verify a source. "
    "It does not automatically score a source. "
    "It does not automatically accept evidence. "
    "It does not automatically reject evidence. "
    "It does not write provenance. It does not create provenance records. "
    "It does not update provenance records. It does not delete provenance records. "
    "It does not mutate source records. It does not mutate evidence records. "
    "It does not mutate citation records. It does not mutate lifecycle records. "
    "It does not mutate do-not-retry guard state. It does not write memory. "
    "It does not approve memory. It does not reject memory. "
    "It does not mutate proposal records. It does not inject memory into agents. "
    "It does not bulk import memory. It does not auto-ingest chat history. "
    "It does not auto-ingest files. It does not auto-ingest external systems. "
    "It does not call agents. It does not start v7. It does not productize. "
    "It does not grant authorization semantics. It does not grant execution semantics."
)


@dataclass(frozen=True)
class SourceProvenanceVerificationStatusItem:
    verification_order: int
    verification_id: str
    verification_name: str
    human_verification_question: str
    allowed_system_output: str
    prohibited_automation: str
    ready_signal: str
    blocking_signal: str
    p4_m0_or_p4_m1_dependency: str


_SOURCE_PROVENANCE_VERIFICATION_STATUS_ITEMS: tuple[
    SourceProvenanceVerificationStatusItem, ...
] = (
    SourceProvenanceVerificationStatusItem(
        verification_order=1,
        verification_id="source-presence-visible",
        verification_name="Source presence visible",
        human_verification_question="Can the human see whether a source is present before any later memory decision?",
        allowed_system_output="Show source-presence status for human inspection only.",
        prohibited_automation="No source fetching, external lookup, trust judgment, source verdict, evidence acceptance, or evidence rejection.",
        ready_signal="Source presence is visible without fetching, trusting, verifying, scoring, accepting, or rejecting the source.",
        blocking_signal="Source presence is hidden or treated as automatic trust, verification, acceptance, or rejection.",
        p4_m0_or_p4_m1_dependency="P4-M1 human-gated inspection discipline before later memory decisions.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=2,
        verification_id="source-type-visible",
        verification_name="Source type visible",
        human_verification_question="Can the human see source type or category without automatic trust judgment?",
        allowed_system_output="Display source type or category as advisory context only.",
        prohibited_automation="No automatic trust judgment, source scoring, source verification verdict, evidence acceptance, or evidence rejection.",
        ready_signal="Source type is visible while trust judgment and scoring remain disabled.",
        blocking_signal="Source type is converted into automatic trust, score, acceptance, rejection, or authorization.",
        p4_m0_or_p4_m1_dependency="P4-M1.1 proposal review status remains advisory only.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=3,
        verification_id="provenance-chain-visible",
        verification_name="Provenance chain visible",
        human_verification_question="Can the human see source/provenance chain requirements before later action?",
        allowed_system_output="Describe required provenance-chain visibility for human inspection.",
        prohibited_automation="No provenance write, provenance record creation, provenance record update, provenance record deletion, or source/evidence/citation mutation.",
        ready_signal="Provenance-chain requirements are visible without writing or mutating provenance records.",
        blocking_signal="The status creates, updates, deletes, or implies accepted provenance records.",
        p4_m0_or_p4_m1_dependency="P4-M1.0 checklist requires manual human review before later action.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=4,
        verification_id="evidence-context-visible",
        verification_name="Evidence context visible",
        human_verification_question="Can the human see evidence context without automatic acceptance or rejection?",
        allowed_system_output="Show evidence context as read-only advisory text.",
        prohibited_automation="No evidence acceptance, evidence rejection, evidence scoring, evidence mutation, citation mutation, memory write, approval, or rejection.",
        ready_signal="Evidence context is visible while acceptance and rejection remain disabled.",
        blocking_signal="Evidence context is treated as accepted, rejected, scored, approved, or written.",
        p4_m0_or_p4_m1_dependency="P4-M1.2 recall verification status remains advisory and non-verdict.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=5,
        verification_id="citation-boundary-visible",
        verification_name="Citation boundary visible",
        human_verification_question="Can the human see citation/source boundary before any later claim?",
        allowed_system_output="State citation/source boundary requirements without creating or mutating citation records.",
        prohibited_automation="No citation record creation, citation record update, citation record deletion, source record mutation, evidence record mutation, or provenance write.",
        ready_signal="Citation/source boundary is visible before any later claim.",
        blocking_signal="Citation/source boundary is hidden or treated as a verified citation claim.",
        p4_m0_or_p4_m1_dependency="P4-M1 human-gated checklist and review-status boundaries.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=6,
        verification_id="unverified-source-not-trusted",
        verification_name="Unverified source not trusted",
        human_verification_question="Is it clear this status does not treat unverified sources as trusted?",
        allowed_system_output="State that unverified sources are not automatically trusted, verified, scored, accepted, or rejected.",
        prohibited_automation="No automatic source trust, source verification verdict, source scoring, evidence acceptance, evidence rejection, or approval.",
        ready_signal="Unverified source context remains visible but not trusted by this status.",
        blocking_signal="The status treats an unverified source as trusted, verified, scored, accepted, rejected, or approved.",
        p4_m0_or_p4_m1_dependency="P4-M1.5 source/provenance status remains before any later decision execution.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=7,
        verification_id="provenance-write-not-taken",
        verification_name="Provenance write not taken",
        human_verification_question="Is it clear this status does not create, update, or delete provenance, source, evidence, or citation records?",
        allowed_system_output="Report disabled provenance writing and disabled source/evidence/citation mutation flags.",
        prohibited_automation="No provenance write, provenance record creation/update/delete, source mutation, evidence mutation, citation mutation, memory write, or proposal mutation.",
        ready_signal="No provenance, source, evidence, citation, memory, proposal, lifecycle, or do-not-retry state is changed.",
        blocking_signal="Any provenance, source, evidence, citation, memory, proposal, lifecycle, or do-not-retry state changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 local store mutation surfaces remain separate from P4-M1.5 status.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=8,
        verification_id="manual-review-required",
        verification_name="Manual review required",
        human_verification_question="Must the human manually inspect source/provenance before later action?",
        allowed_system_output="State that manual source/provenance inspection is required before later action.",
        prohibited_automation="No automatic source verification, trust judgment, evidence acceptance/rejection, authorization, execution, memory write, approval, or rejection.",
        ready_signal="Manual human review remains required before source/provenance handling proceeds.",
        blocking_signal="The status implies source/provenance handling is authorized, executed, approved, rejected, accepted, or trusted.",
        p4_m0_or_p4_m1_dependency="P4-M1 human-gated memory loop checklist.",
    ),
    SourceProvenanceVerificationStatusItem(
        verification_order=9,
        verification_id="automation-boundary-intact",
        verification_name="Automation boundary intact",
        human_verification_question="Are fetch, lookup, trust judgment, source verdict, evidence acceptance/rejection, provenance writing, mutation, write, approval, rejection, import, agent, API/MCP, v7, and productization flags disabled?",
        allowed_system_output="Report disabled source fetching, external lookup, trust judgment, source verdict, evidence acceptance/rejection, provenance writing, source/evidence/citation mutation, write, approval, rejection, proposal mutation, lifecycle mutation, do-not-retry mutation, injection, import, ingestion, agent, API/MCP/connector, v7, and productization flags.",
        prohibited_automation="No fetch/lookup/trust/verdict/accept/reject/provenance-write/source-mutation/evidence-mutation/citation-mutation/write/approval/rejection/import/ingest/agent/API/MCP/connector/v7/productization behavior.",
        ready_signal="All disabled automation flags are false and package version remains 6.16.0.",
        blocking_signal="Any disabled automation flag is enabled or the package version changes.",
        p4_m0_or_p4_m1_dependency="P4-M0 through P4-M1.4 read-only and manual boundary discipline.",
    ),
)


def list_source_provenance_verification_status_items() -> tuple[
    SourceProvenanceVerificationStatusItem, ...
]:
    return _SOURCE_PROVENANCE_VERIFICATION_STATUS_ITEMS


def source_provenance_verification_status_ids() -> tuple[str, ...]:
    return tuple(
        item.verification_id
        for item in list_source_provenance_verification_status_items()
    )


def render_source_provenance_verification_status_markdown(
    items: Sequence[SourceProvenanceVerificationStatusItem] | None = None,
) -> str:
    item_values = (
        tuple(items)
        if items is not None
        else list_source_provenance_verification_status_items()
    )
    status = source_provenance_verification_status_report()
    lines = [
        "# P4-M1.5 Source / Provenance Verification Status",
        "",
        "P4-M1.5 is source/provenance verification status only.",
        "",
        "Source/provenance verification status is advisory only.",
        "",
        "No source fetching is performed by this status.",
        "",
        "No external source lookup is performed by this status.",
        "",
        "No source trust judgment is performed by this status.",
        "",
        "No source verification verdict is performed by this status.",
        "",
        "No evidence acceptance or rejection is performed by this status.",
        "",
        "No provenance writing is performed by this status.",
        "",
        "No source/evidence/citation mutation is performed by this status.",
        "",
        "No memory or proposal mutation is performed by this status.",
        "",
        SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY,
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


def source_provenance_verification_status_as_dicts(
    items: Sequence[SourceProvenanceVerificationStatusItem] | None = None,
) -> tuple[dict[str, object], ...]:
    item_values = (
        tuple(items)
        if items is not None
        else list_source_provenance_verification_status_items()
    )
    return tuple(asdict(item) for item in item_values)


def source_provenance_verification_status_report() -> dict[str, object]:
    return {
        "phase": "P4-M1.5",
        "feature": "Source / Provenance Verification Status",
        "mode": "read-only",
        "verification_item_count": len(_SOURCE_PROVENANCE_VERIFICATION_STATUS_ITEMS),
        "source_provenance_verification_status_advisory_only": True,
        "source_fetching_enabled": False,
        "external_source_lookup_enabled": False,
        "source_trust_judgment_enabled": False,
        "source_verification_verdict_enabled": False,
        "evidence_acceptance_enabled": False,
        "evidence_rejection_enabled": False,
        "provenance_write_enabled": False,
        "source_record_mutation_enabled": False,
        "evidence_record_mutation_enabled": False,
        "citation_record_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "do_not_retry_guard_mutation_enabled": False,
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
        "package_version": P4_M1_5_PACKAGE_VERSION,
        "boundary": SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY,
    }
