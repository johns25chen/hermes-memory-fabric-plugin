from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
)
from .p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)


P4_M2_3_PACKAGE_VERSION = "6.16.0"

MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY = (
    "P4-M2.3 manual authorization evidence envelope only. "
    "Read-only evidence envelope definition only. Inspection-only. "
    "Not P4-M3. P4-M2 hardening remains active. "
    "P4-M2.1 execution surface contract definition remains the source field contract. "
    "P4-M2.2 execution contract validation matrix remains the source validation matrix definition. "
    "Manual authorization evidence envelope does not authorize anything. "
    "Authorization is disabled. Authorization command is disabled. "
    "Live authorization validation is disabled. Live contract validation is disabled. "
    "Input validation is disabled. Record validation is disabled. "
    "Validation verdicts are disabled. Readiness verdicts are disabled. "
    "Actual decision execution is disabled. Automatic decision execution is disabled. "
    "Manual execution command is disabled. Execute command is disabled. "
    "Approval is disabled. Rejection is disabled. "
    "It does not recommend a decision. It does not rank decisions. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not authorize decisions. "
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
    "It does not grant authorization semantics. "
    "It does not grant execution semantics. It does not start P4-M3. "
    "It does not start P4-M4. It does not start P4-M5. "
    "It does not start v7. It does not productize."
)


@dataclass(frozen=True)
class ManualAuthorizationEvidenceEnvelopeField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    required_evidence_signal: str
    trace_requirement: str
    prohibited_semantics: str
    blocking_signal: str
    future_authorization_note: str


_MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_FIELDS: tuple[
    ManualAuthorizationEvidenceEnvelopeField,
    ...,
] = (
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=1,
        field_id="authorization-evidence-envelope-id",
        field_name="Authorization Evidence Envelope Identifier",
        field_purpose="Names the inspection-only envelope without creating authorization state.",
        required_evidence_signal="A stable envelope identifier signal must be visible for future human trace review.",
        trace_requirement="Trace references must preserve the identifier without deriving readiness or authorization.",
        prohibited_semantics="No authorization grant, approval, rejection, execution, or mutation may derive from the identifier.",
        blocking_signal="Missing envelope identifier signal or identifier-derived authorization semantics would block later consideration.",
        future_authorization_note="A later human-authorized path may compare this identifier to records; P4-M2.3 does not validate records.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=2,
        field_id="human-operator-reference",
        field_name="Human Operator Reference",
        field_purpose="Identifies the future human operator reference required for inspection.",
        required_evidence_signal="A human operator reference signal must be visible and separate from approval or authorization.",
        trace_requirement="Trace material must preserve the operator reference without confirming identity or authority.",
        prohibited_semantics="No operator confirmation, approval, rejection, authorization, or execution semantics.",
        blocking_signal="Missing operator reference or operator-derived authorization semantics would block later consideration.",
        future_authorization_note="A later path may inspect operator evidence, but P4-M2.3 confirms no operator authority.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=3,
        field_id="human-authorization-intent-reference",
        field_name="Human Authorization Intent Reference",
        field_purpose="Records a future intent reference without treating intent as authorization.",
        required_evidence_signal="A human authorization intent reference signal must be visible as evidence text only.",
        trace_requirement="Trace material must link the intent reference to human inspection without granting intent fulfillment.",
        prohibited_semantics="No inferred authorization, implicit approval, confirmation, readiness, or execution.",
        blocking_signal="Missing intent reference or intent-derived authorization semantics would block later consideration.",
        future_authorization_note="A later human-authorized path may define intent inspection rules; P4-M2.3 grants none.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=4,
        field_id="manual-decision-reference",
        field_name="Manual Decision Reference",
        field_purpose="Links to a future manual decision reference without selecting or executing a decision.",
        required_evidence_signal="A manual decision reference signal must be visible and non-ranking.",
        trace_requirement="Trace material must preserve the decision reference without recommendation, approval, rejection, or execution.",
        prohibited_semantics="No decision recommendation, ranking, approval, rejection, authorization, or execution.",
        blocking_signal="Missing manual decision reference or automatic decision semantics would block later consideration.",
        future_authorization_note="A later path may inspect a human-selected decision reference; P4-M2.3 selects none.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=5,
        field_id="execution-surface-reference",
        field_name="Execution Surface Reference",
        field_purpose="References the P4-M2.1 execution surface field contract as source context.",
        required_evidence_signal="A visible reference to the P4-M2.1 execution surface contract must be present.",
        trace_requirement="Trace material must preserve the relationship to P4-M2.1 without modifying that source contract.",
        prohibited_semantics="No execution-surface mutation, live contract validation, execution, or connector behavior.",
        blocking_signal="Missing execution surface reference or execution-surface mutation would block later consideration.",
        future_authorization_note="A later path may inspect the P4-M2.1 contract, but P4-M2.3 does not validate live contracts.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=6,
        field_id="execution-contract-validation-matrix-reference",
        field_name="Execution Contract Validation Matrix Reference",
        field_purpose="References the P4-M2.2 validation matrix definition as source context.",
        required_evidence_signal="A visible reference to the P4-M2.2 validation matrix definition must be present.",
        trace_requirement="Trace material must preserve the relationship to P4-M2.2 without running validation.",
        prohibited_semantics="No live validation, validation verdict, readiness verdict, input validation, or record validation.",
        blocking_signal="Missing validation matrix reference or live validation behavior would block later consideration.",
        future_authorization_note="A later path may inspect matrix requirements, but P4-M2.3 emits no validation verdict.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=7,
        field_id="authorization-scope-statement",
        field_name="Authorization Scope Statement",
        field_purpose="Defines the future authorization scope text as a boundary artifact only.",
        required_evidence_signal="A scope statement signal must be visible and bounded to human inspection.",
        trace_requirement="Trace material must preserve scope text without converting it into a grant.",
        prohibited_semantics="No authorization scope grant, approval, rejection, execution, or automatic readiness.",
        blocking_signal="Missing scope statement or scope-derived authorization semantics would block later consideration.",
        future_authorization_note="A later path may inspect scope sufficiency; P4-M2.3 does not authorize scope.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=8,
        field_id="authorization-boundary-statement",
        field_name="Authorization Boundary Statement",
        field_purpose="States the authorization-disabled boundary for future inspection.",
        required_evidence_signal="A boundary statement signal must be visible and must keep authorization disabled.",
        trace_requirement="Trace material must preserve the disabled authorization boundary in reports.",
        prohibited_semantics="No authorization command, authorization grant, approval, rejection, or execution.",
        blocking_signal="Missing boundary statement or authorization-enabled semantics would block later consideration.",
        future_authorization_note="A later path may define authorization controls; P4-M2.3 keeps authorization disabled.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=9,
        field_id="precondition-evidence-reference",
        field_name="Precondition Evidence Reference",
        field_purpose="References precondition evidence without fetching, trusting, writing, or validating evidence.",
        required_evidence_signal="A precondition evidence reference signal must be visible and read-only.",
        trace_requirement="Trace material must preserve evidence references without source fetching or provenance writes.",
        prohibited_semantics="No source fetch, web browse, external API call, source trust, evidence write, citation write, or provenance write.",
        blocking_signal="Missing precondition evidence reference or evidence/source/provenance mutation would block later consideration.",
        future_authorization_note="A later path may inspect evidence references; P4-M2.3 fetches and writes none.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=10,
        field_id="risk-acknowledgement-reference",
        field_name="Risk Acknowledgement Reference",
        field_purpose="References future risk acknowledgement evidence without making readiness decisions.",
        required_evidence_signal="A risk acknowledgement reference signal must be visible and non-verdict-bearing.",
        trace_requirement="Trace material must preserve risk acknowledgement references for human inspection.",
        prohibited_semantics="No readiness verdict, validation verdict, decision ranking, recommendation, approval, rejection, or execution.",
        blocking_signal="Missing risk acknowledgement reference or automatic readiness semantics would block later consideration.",
        future_authorization_note="A later path may inspect risk acknowledgement; P4-M2.3 determines no readiness.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=11,
        field_id="audit-trace-reference",
        field_name="Audit Trace Reference",
        field_purpose="References audit trace material without writing audit, provenance, or execution state.",
        required_evidence_signal="An audit trace reference signal must be visible and stable.",
        trace_requirement="Trace material must preserve audit references without mutating trace, source, evidence, or citation records.",
        prohibited_semantics="No audit write, provenance write, source mutation, evidence mutation, citation mutation, or execution trace mutation.",
        blocking_signal="Missing audit trace reference or trace/provenance mutation would block later consideration.",
        future_authorization_note="A later path may compare audit traces; P4-M2.3 writes no trace state.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=12,
        field_id="operator-confirmation-placeholder",
        field_name="Operator Confirmation Placeholder",
        field_purpose="Keeps a placeholder for future operator confirmation without confirming anything.",
        required_evidence_signal="A non-confirming operator confirmation placeholder signal must be visible.",
        trace_requirement="Trace material must preserve the placeholder separately from any actual human confirmation.",
        prohibited_semantics="No confirmation, approval, rejection, authorization, execute command, or manual execution command.",
        blocking_signal="Missing placeholder or placeholder-derived confirmation semantics would block later consideration.",
        future_authorization_note="A later path may define confirmation evidence; P4-M2.3 confirms nothing.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=13,
        field_id="revocation-or-expiry-note",
        field_name="Revocation Or Expiry Note",
        field_purpose="Captures future revocation or expiry note expectations without lifecycle mutation.",
        required_evidence_signal="A revocation or expiry note signal must be visible as definition text only.",
        trace_requirement="Trace material must preserve revocation or expiry notes without changing lifecycle state.",
        prohibited_semantics="No lifecycle mutation, retry policy mutation, do-not-retry guard mutation, cleanup, archive, stale, or delete behavior.",
        blocking_signal="Missing revocation/expiry note or lifecycle mutation behavior would block later consideration.",
        future_authorization_note="A later path may inspect expiry evidence; P4-M2.3 mutates no lifecycle or guard state.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=14,
        field_id="authorization-semantics-disabled",
        field_name="Authorization Semantics Disabled",
        field_purpose="Makes the disabled authorization semantics signal explicit.",
        required_evidence_signal="An authorization-semantics-disabled signal must be visible.",
        trace_requirement="Trace material must preserve disabled authorization status in reports and boundaries.",
        prohibited_semantics="No authorization grant, authorization command, approval, rejection, confirmation, or human authorization fulfillment.",
        blocking_signal="Any authorization semantics would block later consideration.",
        future_authorization_note="A later path may define authorization checks; P4-M2.3 grants no authorization semantics.",
    ),
    ManualAuthorizationEvidenceEnvelopeField(
        field_order=15,
        field_id="execution-semantics-disabled",
        field_name="Execution Semantics Disabled",
        field_purpose="Makes the disabled execution semantics signal explicit.",
        required_evidence_signal="An execution-semantics-disabled signal must be visible.",
        trace_requirement="Trace material must preserve disabled execution status in reports and boundaries.",
        prohibited_semantics="No actual execution, automatic execution, manual execution command, execute command, deployment, or productization.",
        blocking_signal="Any execution semantics would block later consideration.",
        future_authorization_note="A later path may define execution checks; P4-M2.3 grants no execution semantics.",
    ),
)


def list_manual_authorization_evidence_envelope_fields() -> tuple[
    ManualAuthorizationEvidenceEnvelopeField,
    ...,
]:
    return _MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_FIELDS


def manual_authorization_evidence_envelope_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_manual_authorization_evidence_envelope_fields()
    )


def render_manual_authorization_evidence_envelope_markdown(
    fields: Sequence[ManualAuthorizationEvidenceEnvelopeField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_manual_authorization_evidence_envelope_fields()
    )
    status = manual_authorization_evidence_envelope_report()
    lines = [
        "# P4-M2.3 Manual Authorization Evidence Envelope",
        "",
        "P4-M2.3 manual authorization evidence envelope only.",
        "",
        "Read-only evidence envelope definition only.",
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
        "Manual authorization evidence envelope does not authorize anything.",
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
        "No authorization semantics are granted by this evidence envelope.",
        "",
        "No execution semantics are granted by this evidence envelope.",
        "",
        "No memory writing is performed by this evidence envelope.",
        "",
        "No mutation is performed by this evidence envelope.",
        "",
        "No API/MCP/connector behavior is performed by this evidence envelope.",
        "",
        "No agent call is performed by this evidence envelope.",
        "",
        MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Evidence Envelope Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Required evidence signal: {field.required_evidence_signal}",
                f"- Trace requirement: {field.trace_requirement}",
                f"- Prohibited semantics: {field.prohibited_semantics}",
                f"- Blocking signal: {field.blocking_signal}",
                f"- Future authorization note: {field.future_authorization_note}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def manual_authorization_evidence_envelope_as_dicts(
    fields: Sequence[ManualAuthorizationEvidenceEnvelopeField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_manual_authorization_evidence_envelope_fields()
    )
    return tuple(asdict(field) for field in field_values)


def manual_authorization_evidence_envelope_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.3",
        "feature": "Manual Authorization Evidence Envelope",
        "mode": "read-only",
        "envelope_field_count": len(_MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_FIELDS),
        "p4_m2_started": True,
        "execution_surface_contract_definition_available": True,
        "execution_contract_validation_matrix_available": True,
        "manual_authorization_evidence_envelope_started": True,
        "manual_authorization_evidence_envelope_definition_only": True,
        "evidence_envelope_fields_defined": True,
        "trace_requirements_defined": True,
        "blocking_signal_rules_defined": True,
        "inspection_only": True,
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
        "package_version": P4_M2_3_PACKAGE_VERSION,
        "boundary": MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY,
    }


if not execution_surface_contract_field_ids():
    raise RuntimeError("execution_surface_contract_definition_unavailable")

if not execution_contract_validation_matrix_field_ids():
    raise RuntimeError("execution_contract_validation_matrix_unavailable")
