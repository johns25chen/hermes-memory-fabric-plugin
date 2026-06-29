from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
)
from .p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)
from .p4_m2_manual_authorization_evidence_envelope import (
    manual_authorization_evidence_envelope_field_ids,
)


P4_M2_4_PACKAGE_VERSION = "6.16.0"

HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_BOUNDARY = (
    "P4-M2.4 human confirmation snapshot contract only. "
    "Read-only snapshot contract definition only. Inspection-only. "
    "Not P4-M3. P4-M2 hardening remains active. "
    "P4-M2.1 execution surface contract definition remains the source field contract. "
    "P4-M2.2 execution contract validation matrix remains the source validation matrix definition. "
    "P4-M2.3 manual authorization evidence envelope remains the source evidence envelope definition. "
    "Human confirmation snapshot contract does not confirm anything. "
    "Manual authorization evidence envelope does not authorize anything. "
    "Confirmation is disabled. Confirmation command is disabled. "
    "Live confirmation validation is disabled. Authorization is disabled. "
    "Authorization command is disabled. Live authorization validation is disabled. "
    "Live contract validation is disabled. Input validation is disabled. "
    "Record validation is disabled. Validation verdicts are disabled. "
    "Readiness verdicts are disabled. Actual decision execution is disabled. "
    "Automatic decision execution is disabled. Manual execution command is disabled. "
    "Execute command is disabled. Approval is disabled. Rejection is disabled. "
    "It does not recommend a decision. It does not rank decisions. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not confirm decisions. "
    "It does not authorize decisions. It does not execute decisions. "
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
    "It does not grant confirmation semantics. "
    "It does not grant authorization semantics. "
    "It does not grant execution semantics. It does not start P4-M3. "
    "It does not start P4-M4. It does not start P4-M5. "
    "It does not start v7. It does not productize."
)


@dataclass(frozen=True)
class HumanConfirmationSnapshotContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    required_snapshot_signal: str
    trace_requirement: str
    prohibited_semantics: str
    blocking_signal: str
    future_confirmation_note: str


_HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_FIELDS: tuple[
    HumanConfirmationSnapshotContractField,
    ...,
] = (
    HumanConfirmationSnapshotContractField(
        field_order=1,
        field_id="human-confirmation-snapshot-id",
        field_name="Human Confirmation Snapshot Identifier",
        field_purpose="Names the inspection-only snapshot without creating confirmation state.",
        required_snapshot_signal="A stable snapshot identifier signal must be visible for future human trace review.",
        trace_requirement="Trace references must preserve the snapshot identifier without deriving confirmation, authorization, readiness, or execution.",
        prohibited_semantics="No confirmation grant, authorization grant, approval, rejection, execution, or mutation may derive from the identifier.",
        blocking_signal="Missing snapshot identifier signal or identifier-derived confirmation semantics would block later consideration.",
        future_confirmation_note="A later human-confirmed path may compare this identifier to records; P4-M2.4 does not validate records.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=2,
        field_id="human-operator-reference",
        field_name="Human Operator Reference",
        field_purpose="Identifies the future human operator reference required for snapshot inspection.",
        required_snapshot_signal="A human operator reference signal must be visible and separate from confirmation or authorization.",
        trace_requirement="Trace material must preserve the operator reference without confirming identity, authority, or intent.",
        prohibited_semantics="No operator confirmation, authorization, approval, rejection, or execution semantics.",
        blocking_signal="Missing operator reference or operator-derived confirmation semantics would block later consideration.",
        future_confirmation_note="A later path may inspect operator evidence, but P4-M2.4 confirms no operator authority.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=3,
        field_id="human-confirmation-intent-reference",
        field_name="Human Confirmation Intent Reference",
        field_purpose="Records a future confirmation intent reference without treating intent as confirmation.",
        required_snapshot_signal="A human confirmation intent reference signal must be visible as snapshot text only.",
        trace_requirement="Trace material must link the intent reference to human inspection without granting intent fulfillment.",
        prohibited_semantics="No inferred confirmation, implicit authorization, approval, readiness, or execution.",
        blocking_signal="Missing confirmation intent reference or intent-derived confirmation semantics would block later consideration.",
        future_confirmation_note="A later human-confirmed path may define intent inspection rules; P4-M2.4 grants none.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=4,
        field_id="manual-authorization-evidence-envelope-reference",
        field_name="Manual Authorization Evidence Envelope Reference",
        field_purpose="References the P4-M2.3 evidence envelope definition as source context.",
        required_snapshot_signal="A visible reference to the P4-M2.3 manual authorization evidence envelope must be present.",
        trace_requirement="Trace material must preserve the relationship to P4-M2.3 without authorizing anything.",
        prohibited_semantics="No authorization grant, evidence mutation, live authorization validation, approval, rejection, or execution.",
        blocking_signal="Missing evidence envelope reference or authorization behavior would block later consideration.",
        future_confirmation_note="A later path may inspect the P4-M2.3 envelope, but P4-M2.4 does not validate live envelopes.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=5,
        field_id="manual-decision-reference",
        field_name="Manual Decision Reference",
        field_purpose="Links to a future manual decision reference without selecting, confirming, or executing a decision.",
        required_snapshot_signal="A manual decision reference signal must be visible and non-ranking.",
        trace_requirement="Trace material must preserve the decision reference without recommendation, approval, rejection, confirmation, authorization, or execution.",
        prohibited_semantics="No decision recommendation, ranking, confirmation, authorization, approval, rejection, or execution.",
        blocking_signal="Missing manual decision reference or automatic decision semantics would block later consideration.",
        future_confirmation_note="A later path may inspect a human-selected decision reference; P4-M2.4 selects none.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=6,
        field_id="execution-surface-reference",
        field_name="Execution Surface Reference",
        field_purpose="References the P4-M2.1 execution surface field contract as source context.",
        required_snapshot_signal="A visible reference to the P4-M2.1 execution surface contract must be present.",
        trace_requirement="Trace material must preserve the relationship to P4-M2.1 without modifying that source contract.",
        prohibited_semantics="No execution-surface mutation, live contract validation, execution, API, MCP, or connector behavior.",
        blocking_signal="Missing execution surface reference or execution-surface mutation would block later consideration.",
        future_confirmation_note="A later path may inspect the P4-M2.1 contract, but P4-M2.4 does not validate live contracts.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=7,
        field_id="execution-contract-validation-matrix-reference",
        field_name="Execution Contract Validation Matrix Reference",
        field_purpose="References the P4-M2.2 validation matrix definition as source context.",
        required_snapshot_signal="A visible reference to the P4-M2.2 validation matrix definition must be present.",
        trace_requirement="Trace material must preserve the relationship to P4-M2.2 without running validation.",
        prohibited_semantics="No live validation, validation verdict, readiness verdict, input validation, or record validation.",
        blocking_signal="Missing validation matrix reference or live validation behavior would block later consideration.",
        future_confirmation_note="A later path may inspect matrix requirements, but P4-M2.4 emits no validation verdict.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=8,
        field_id="authorization-scope-snapshot",
        field_name="Authorization Scope Snapshot",
        field_purpose="Defines future authorization scope snapshot text as a boundary artifact only.",
        required_snapshot_signal="An authorization scope snapshot signal must be visible and bounded to human inspection.",
        trace_requirement="Trace material must preserve scope text without converting it into a grant.",
        prohibited_semantics="No authorization scope grant, confirmation, approval, rejection, execution, or automatic readiness.",
        blocking_signal="Missing authorization scope snapshot or scope-derived authorization semantics would block later consideration.",
        future_confirmation_note="A later path may inspect scope sufficiency; P4-M2.4 does not authorize scope.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=9,
        field_id="authorization-boundary-snapshot",
        field_name="Authorization Boundary Snapshot",
        field_purpose="States the authorization-disabled boundary for future snapshot inspection.",
        required_snapshot_signal="An authorization boundary snapshot signal must be visible and must keep authorization disabled.",
        trace_requirement="Trace material must preserve the disabled authorization boundary in reports.",
        prohibited_semantics="No authorization command, authorization grant, confirmation, approval, rejection, or execution.",
        blocking_signal="Missing authorization boundary snapshot or authorization-enabled semantics would block later consideration.",
        future_confirmation_note="A later path may define authorization controls; P4-M2.4 keeps authorization disabled.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=10,
        field_id="precondition-evidence-snapshot",
        field_name="Precondition Evidence Snapshot",
        field_purpose="References precondition evidence snapshot expectations without fetching, trusting, writing, or validating evidence.",
        required_snapshot_signal="A precondition evidence snapshot signal must be visible and read-only.",
        trace_requirement="Trace material must preserve evidence references without source fetching, source trust, or provenance writes.",
        prohibited_semantics="No source fetch, web browse, external API call, source trust, evidence write, citation write, or provenance write.",
        blocking_signal="Missing precondition evidence snapshot or evidence/source/provenance mutation would block later consideration.",
        future_confirmation_note="A later path may inspect evidence snapshots; P4-M2.4 fetches and writes none.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=11,
        field_id="risk-acknowledgement-snapshot",
        field_name="Risk Acknowledgement Snapshot",
        field_purpose="References future risk acknowledgement snapshot expectations without making readiness decisions.",
        required_snapshot_signal="A risk acknowledgement snapshot signal must be visible and non-verdict-bearing.",
        trace_requirement="Trace material must preserve risk acknowledgement snapshots for human inspection.",
        prohibited_semantics="No readiness verdict, validation verdict, decision ranking, recommendation, approval, rejection, confirmation, authorization, or execution.",
        blocking_signal="Missing risk acknowledgement snapshot or automatic readiness semantics would block later consideration.",
        future_confirmation_note="A later path may inspect risk acknowledgement; P4-M2.4 determines no readiness.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=12,
        field_id="audit-trace-snapshot",
        field_name="Audit Trace Snapshot",
        field_purpose="References audit trace snapshot material without writing audit, provenance, confirmation, authorization, or execution state.",
        required_snapshot_signal="An audit trace snapshot signal must be visible and stable.",
        trace_requirement="Trace material must preserve audit references without mutating trace, source, evidence, or citation records.",
        prohibited_semantics="No audit write, provenance write, source mutation, evidence mutation, citation mutation, confirmation trace mutation, or execution trace mutation.",
        blocking_signal="Missing audit trace snapshot or trace/provenance mutation would block later consideration.",
        future_confirmation_note="A later path may compare audit traces; P4-M2.4 writes no trace state.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=13,
        field_id="operator-confirmation-placeholder",
        field_name="Operator Confirmation Placeholder",
        field_purpose="Keeps a placeholder for future operator confirmation without confirming anything.",
        required_snapshot_signal="A non-confirming operator confirmation placeholder signal must be visible.",
        trace_requirement="Trace material must preserve the placeholder separately from any actual human confirmation.",
        prohibited_semantics="No confirmation, approval, rejection, authorization, execute command, or manual execution command.",
        blocking_signal="Missing placeholder or placeholder-derived confirmation semantics would block later consideration.",
        future_confirmation_note="A later path may define confirmation evidence; P4-M2.4 confirms nothing.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=14,
        field_id="revocation-or-expiry-snapshot",
        field_name="Revocation Or Expiry Snapshot",
        field_purpose="Captures future revocation or expiry snapshot expectations without lifecycle mutation.",
        required_snapshot_signal="A revocation or expiry snapshot signal must be visible as definition text only.",
        trace_requirement="Trace material must preserve revocation or expiry notes without changing lifecycle state.",
        prohibited_semantics="No lifecycle mutation, retry policy mutation, do-not-retry guard mutation, cleanup, archive, stale, or delete behavior.",
        blocking_signal="Missing revocation/expiry snapshot or lifecycle mutation behavior would block later consideration.",
        future_confirmation_note="A later path may inspect expiry evidence; P4-M2.4 mutates no lifecycle or guard state.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=15,
        field_id="confirmation-semantics-disabled",
        field_name="Confirmation Semantics Disabled",
        field_purpose="Makes the disabled confirmation semantics signal explicit.",
        required_snapshot_signal="A confirmation-semantics-disabled signal must be visible.",
        trace_requirement="Trace material must preserve disabled confirmation status in reports and boundaries.",
        prohibited_semantics="No confirmation grant, confirmation command, approval, rejection, authorization, or human confirmation fulfillment.",
        blocking_signal="Any confirmation semantics would block later consideration.",
        future_confirmation_note="A later path may define confirmation checks; P4-M2.4 grants no confirmation semantics.",
    ),
    HumanConfirmationSnapshotContractField(
        field_order=16,
        field_id="execution-semantics-disabled",
        field_name="Execution Semantics Disabled",
        field_purpose="Makes the disabled execution semantics signal explicit.",
        required_snapshot_signal="An execution-semantics-disabled signal must be visible.",
        trace_requirement="Trace material must preserve disabled execution status in reports and boundaries.",
        prohibited_semantics="No actual execution, automatic execution, manual execution command, execute command, deployment, or productization.",
        blocking_signal="Any execution semantics would block later consideration.",
        future_confirmation_note="A later path may define execution checks; P4-M2.4 grants no execution semantics.",
    ),
)


def list_human_confirmation_snapshot_contract_fields() -> tuple[
    HumanConfirmationSnapshotContractField,
    ...,
]:
    return _HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_FIELDS


def human_confirmation_snapshot_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_human_confirmation_snapshot_contract_fields()
    )


def render_human_confirmation_snapshot_contract_markdown(
    fields: Sequence[HumanConfirmationSnapshotContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_human_confirmation_snapshot_contract_fields()
    )
    status = human_confirmation_snapshot_contract_report()
    lines = [
        "# P4-M2.4 Human Confirmation Snapshot Contract",
        "",
        "P4-M2.4 human confirmation snapshot contract only.",
        "",
        "Read-only snapshot contract definition only.",
        "",
        "Inspection-only.",
        "",
        "Not P4-M3.",
        "",
        "P4-M2 hardening remains active.",
        "",
        "P4-M2.1 execution surface contract definition remains the source field contract.",
        "",
        "P4-M2.2 execution contract validation matrix remains the source validation matrix definition.",
        "",
        "P4-M2.3 manual authorization evidence envelope remains the source evidence envelope definition.",
        "",
        "Human confirmation snapshot contract does not confirm anything.",
        "",
        "Manual authorization evidence envelope does not authorize anything.",
        "",
        "Confirmation is disabled.",
        "",
        "Confirmation command is disabled.",
        "",
        "Live confirmation validation is disabled.",
        "",
        "Authorization is disabled.",
        "",
        "Authorization command is disabled.",
        "",
        "Live authorization validation is disabled.",
        "",
        "Live contract validation is disabled.",
        "",
        "Input validation is disabled.",
        "",
        "Record validation is disabled.",
        "",
        "Validation verdicts are disabled.",
        "",
        "Readiness verdicts are disabled.",
        "",
        "Actual decision execution is disabled.",
        "",
        "Automatic decision execution is disabled.",
        "",
        "Manual execution command is disabled.",
        "",
        "Execute command is disabled.",
        "",
        "No confirmation semantics are granted by this snapshot contract.",
        "",
        "No authorization semantics are granted by this snapshot contract.",
        "",
        "No execution semantics are granted by this snapshot contract.",
        "",
        "No memory writing is performed by this snapshot contract.",
        "",
        "No mutation is performed by this snapshot contract.",
        "",
        "No API/MCP/connector behavior is performed by this snapshot contract.",
        "",
        "No agent call is performed by this snapshot contract.",
        "",
        HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Snapshot Contract Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Required snapshot signal: {field.required_snapshot_signal}",
                f"- Trace requirement: {field.trace_requirement}",
                f"- Prohibited semantics: {field.prohibited_semantics}",
                f"- Blocking signal: {field.blocking_signal}",
                f"- Future confirmation note: {field.future_confirmation_note}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def human_confirmation_snapshot_contract_as_dicts(
    fields: Sequence[HumanConfirmationSnapshotContractField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_human_confirmation_snapshot_contract_fields()
    )
    return tuple(asdict(field) for field in field_values)


def human_confirmation_snapshot_contract_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.4",
        "feature": "Human Confirmation Snapshot Contract",
        "mode": "read-only",
        "snapshot_field_count": len(_HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_FIELDS),
        "p4_m2_started": True,
        "execution_surface_contract_definition_available": True,
        "execution_contract_validation_matrix_available": True,
        "manual_authorization_evidence_envelope_available": True,
        "human_confirmation_snapshot_contract_started": True,
        "human_confirmation_snapshot_contract_definition_only": True,
        "snapshot_contract_fields_defined": True,
        "trace_requirements_defined": True,
        "blocking_signal_rules_defined": True,
        "inspection_only": True,
        "confirmation_enabled": False,
        "confirmation_command_enabled": False,
        "live_confirmation_validation_enabled": False,
        "authorization_enabled": False,
        "authorization_command_enabled": False,
        "live_authorization_validation_enabled": False,
        "live_contract_validation_enabled": False,
        "input_validation_enabled": False,
        "record_validation_enabled": False,
        "validation_verdict_enabled": False,
        "readiness_verdict_enabled": False,
        "actual_decision_execution_enabled": False,
        "automatic_decision_execution_enabled": False,
        "manual_execution_command_enabled": False,
        "execute_command_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "automatic_decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "confirmation_semantics_granted": False,
        "authorization_semantics_granted": False,
        "execution_semantics_granted": False,
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
        "p4_m3_started": False,
        "p4_m4_started": False,
        "p4_m5_started": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M2_4_PACKAGE_VERSION,
        "boundary": HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_BOUNDARY,
    }


if not execution_surface_contract_field_ids():
    raise RuntimeError("execution_surface_contract_definition_unavailable")

if not execution_contract_validation_matrix_field_ids():
    raise RuntimeError("execution_contract_validation_matrix_unavailable")

if not manual_authorization_evidence_envelope_field_ids():
    raise RuntimeError("manual_authorization_evidence_envelope_unavailable")
