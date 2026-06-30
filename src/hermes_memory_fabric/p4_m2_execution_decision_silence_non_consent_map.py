from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
)
from .p4_m2_execution_decision_default_denial_boundary_map import (
    execution_decision_default_denial_boundary_map_field_ids,
)
from .p4_m2_execution_decision_non_equivalence_map import (
    execution_decision_non_equivalence_map_field_ids,
)
from .p4_m2_execution_decision_recommendation_prohibition_map import (
    execution_decision_recommendation_prohibition_map_field_ids,
)
from .p4_m2_execution_preconditions_snapshot_map import (
    execution_preconditions_snapshot_map_field_ids,
)
from .p4_m2_execution_risk_acceptance_prohibition_map import (
    execution_risk_acceptance_prohibition_map_field_ids,
)
from .p4_m2_execution_risk_acknowledgement_map import (
    execution_risk_acknowledgement_map_field_ids,
)
from .p4_m2_execution_risk_waiver_prohibition_map import (
    execution_risk_waiver_prohibition_map_field_ids,
)
from .p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)
from .p4_m2_human_confirmation_snapshot_contract import (
    human_confirmation_snapshot_contract_field_ids,
)
from .p4_m2_manual_authorization_evidence_envelope import (
    manual_authorization_evidence_envelope_field_ids,
)


P4_M2_12_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class ExecutionDecisionSilenceNonConsentMapField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    silence_non_consent_boundary_category: str
    missing_evidence_as_consent_prohibition_signal: str
    consent_semantics_disabled: str
    non_consent_execution_semantics_disabled: str


_BOUNDARY_PHRASE_LINES = (
    "P4-M2.12",
    "Execution Decision Silence Non-Consent Map",
    "read-only",
    "definition-only",
    "inspection-only",
    "silence is not consent",
    "non-response is not consent",
    "missing record is not consent",
    "missing evidence is not consent",
    "missing objection is not approval",
    "missing rejection is not approval",
    "missing denial is not permission",
    "no execution",
    "no decision execution",
    "no confirmation",
    "no decision confirmation",
    "no authorization",
    "no decision authorization",
    "no approval",
    "no default approval",
    "no decision approval",
    "no rejection",
    "no live rejection",
    "no active denial",
    "no decision rejection",
    "no consent validation",
    "no live consent validation",
    "no consent record creation",
    "no non-consent record creation",
    "no risk acceptance",
    "no risk waiver",
    "no implied risk acceptance",
    "no implied risk waiver",
    "no acknowledgement-as-acceptance",
    "no acknowledgement-as-waiver",
    "no acceptance-prohibition-as-waiver",
    "no absence-of-acceptance-as-waiver",
    "no silence-as-consent",
    "no silence-as-authorization",
    "no silence-as-confirmation",
    "no silence-as-approval",
    "no silence-as-recommendation",
    "no silence-as-readiness",
    "no silence-as-validation",
    "no silence-as-risk-acceptance",
    "no silence-as-risk-waiver",
    "no non-response-as-consent",
    "no missing-record-as-consent",
    "no missing-evidence-as-consent",
    "no missing-objection-as-approval",
    "no missing-rejection-as-approval",
    "no missing-denial-as-permission",
    "no missing-confirmation-as-confirmation",
    "no missing-authorization-as-authorization",
    "no missing-recommendation-as-recommendation",
    "no missing-readiness-as-readiness",
    "no missing-validation-as-validation",
    "no missing-risk-acceptance-as-risk-acceptance",
    "no missing-risk-waiver-as-risk-waiver",
    "no absence-as-permission",
    "no absence-as-approval",
    "no absence-as-recommendation",
    "no absence-as-readiness",
    "no absence-as-validation",
    "no absence-as-authorization",
    "no absence-as-confirmation",
    "no absence-as-risk-acceptance",
    "no absence-as-risk-waiver",
    "no waiver evidence creation",
    "no waiver approval",
    "no waiver authorization",
    "no manual-decision-as-execution",
    "no manual-decision-as-authorization",
    "no manual-decision-as-confirmation",
    "no manual-decision-as-approval",
    "no manual-decision-as-recommendation",
    "no operator-as-authorization",
    "no operator-as-confirmation",
    "no operator-as-approval",
    "no operator-as-recommendation",
    "no risk-map-as-readiness",
    "no risk-map-as-validation",
    "no risk-map-as-recommendation",
    "no non-equivalence-map-as-recommendation",
    "no recommendation-map-as-approval",
    "no recommendation-map-as-readiness",
    "no default-denial-map-as-consent",
    "no default-denial-map-as-execution",
    "no reference-as-verdict",
    "no reference-as-execution",
    "no reference-as-authorization",
    "no reference-as-confirmation",
    "no reference-as-approval",
    "no reference-as-recommendation",
    "no reference-as-consent",
    "no decision recommendation",
    "no decision ranking",
    "no suggested next action",
    "no default readiness",
    "no default allow",
    "no default permit",
    "no default continue",
    "no default execute",
    "no default mutate",
    "no auto-pass",
    "no auto-execution hint",
    "no advisory verdict",
    "no execution hint",
    "no authorization hint",
    "no confirmation hint",
    "no readiness hint",
    "no validation hint",
    "no live risk acknowledgement",
    "no memory mutation",
    "no memory record creation",
    "no memory record update",
    "no memory record deletion",
    "no proposal mutation",
    "no lifecycle mutation",
    "no retry policy mutation",
    "no source fetching",
    "no provenance writing",
    "no evidence mutation",
    "no citation mutation",
    "no live confirmation validation",
    "no live authorization validation",
    "no live contract validation",
    "no input validation",
    "no record validation",
    "no validation verdict",
    "no readiness verdict",
    "no automatic readiness verdict",
    "no consent semantics",
    "no non-consent execution semantics",
    "no decision equivalence semantics",
    "no recommendation semantics",
    "no ranking semantics",
    "no next-action semantics",
    "no default-allowance semantics",
    "no permission semantics",
    "no denial execution semantics",
    "no rejection execution semantics",
    "no acceptance semantics",
    "no waiver semantics",
    "no acknowledgement semantics",
    "no confirmation semantics",
    "no authorization semantics",
    "no execution semantics",
    "no API",
    "no MCP",
    "no connector",
    "no agent call",
    "no Codex/Hermes/ChatGPT product-code auto-call",
    "no P4-M3",
    "no P4-M4",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no MVP",
    "no deploy",
    "no full Memory Graph",
)

EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY = (
    "P4-M2.12 Execution Decision Silence Non-Consent Map read-only "
    "definition-only inspection-only. It defines a stable read-only structure "
    "that explicitly prevents silence, non-response, missing record, missing "
    "evidence, missing objection, missing rejection, missing denial, missing "
    "confirmation, missing authorization, missing approval, missing recommendation, "
    "missing readiness, missing validation, missing risk acceptance, missing risk "
    "waiver, missing operator action, and missing decision evidence from being "
    "treated as consent, permission, recommendation, ranking, suggested next action, "
    "default approval, default readiness, auto-pass, auto-execution hint, advisory "
    "verdict, execution hint, authorization hint, confirmation hint, readiness hint, "
    "validation hint, execution, authorization, confirmation, approval, rejection, "
    "risk acceptance, risk waiver, readiness, validation, continuation, or mutation. "
    + " ".join(f"{phrase}." for phrase in _BOUNDARY_PHRASE_LINES)
)

_EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_FIELDS: tuple[
    ExecutionDecisionSilenceNonConsentMapField,
    ...,
] = (
    ExecutionDecisionSilenceNonConsentMapField(
        1,
        "execution-decision-silence-non-consent-map-id",
        "Execution Decision Silence Non-Consent Map Identifier",
        "Names the inspection-only map; silence is not consent and non-response is not consent.",
        "map-identity",
        "no missing-evidence-as-consent; no missing-record-as-consent",
        "no consent semantics; no permission semantics",
        "no non-consent execution semantics; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        2,
        "execution-decision-default-denial-boundary-map-reference",
        "Execution Decision Default Denial Boundary Map Reference",
        "References P4-M2.11 without treating default-denial boundaries as consent, execution, approval, readiness, or verdict.",
        "default-denial-map-reference",
        "no default-denial-map-as-consent; no default-denial-map-as-execution",
        "no consent semantics; no denial execution semantics",
        "no execution semantics; no rejection execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        3,
        "execution-decision-recommendation-prohibition-map-reference",
        "Execution Decision Recommendation Prohibition Map Reference",
        "References P4-M2.10 without creating recommendation, approval, readiness, ranking, suggested next action, or consent.",
        "recommendation-map-reference",
        "no recommendation-map-as-approval; no recommendation-map-as-readiness",
        "no recommendation semantics; no ranking semantics",
        "no next-action semantics; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        4,
        "execution-decision-non-equivalence-map-reference",
        "Execution Decision Non-Equivalence Map Reference",
        "References P4-M2.9 without converting non-equivalence boundaries into consent, recommendation, permission, verdict, or mutation.",
        "non-equivalence-map-reference",
        "no non-equivalence-map-as-recommendation; no reference-as-consent",
        "no decision equivalence semantics; no consent semantics",
        "no execution semantics; no authorization semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        5,
        "manual-decision-reference",
        "Manual Decision Reference",
        "References manual decision material without treating missing decision evidence as execution, authorization, confirmation, approval, or recommendation.",
        "manual-decision-reference",
        "no manual-decision-as-execution; no manual-decision-as-authorization",
        "no manual-decision-as-confirmation; no manual-decision-as-approval",
        "no manual-decision-as-recommendation; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        6,
        "operator-reference",
        "Operator Reference",
        "References an operator label without treating operator silence or missing operator action as authorization, confirmation, approval, or recommendation.",
        "operator-reference",
        "no operator-as-authorization; no operator-as-confirmation",
        "no operator-as-approval; no operator-as-recommendation",
        "no authorization semantics; no confirmation semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        7,
        "human-confirmation-snapshot-reference",
        "Human Confirmation Snapshot Reference",
        "References P4-M2.4 without treating missing confirmation as confirmation or validating confirmation live.",
        "human-confirmation-snapshot-reference",
        "no missing-confirmation-as-confirmation; no live confirmation validation",
        "no confirmation semantics; no consent semantics",
        "no decision confirmation; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        8,
        "manual-authorization-evidence-envelope-reference",
        "Manual Authorization Evidence Envelope Reference",
        "References P4-M2.3 without treating missing authorization as authorization or validating authorization live.",
        "manual-authorization-evidence-envelope-reference",
        "no missing-authorization-as-authorization; no live authorization validation",
        "no authorization semantics; no consent semantics",
        "no decision authorization; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        9,
        "execution-preconditions-snapshot-map-reference",
        "Execution Preconditions Snapshot Map Reference",
        "References P4-M2.5 without treating missing readiness or missing validation as readiness, validation, auto-pass, or default readiness.",
        "preconditions-snapshot-map-reference",
        "no missing-readiness-as-readiness; no missing-validation-as-validation",
        "no default readiness; no auto-pass",
        "no readiness verdict; no validation verdict",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        10,
        "execution-risk-acknowledgement-map-reference",
        "Execution Risk Acknowledgement Map Reference",
        "References P4-M2.6 without treating acknowledgement or missing risk evidence as risk acceptance, risk waiver, readiness, validation, or recommendation.",
        "risk-acknowledgement-map-reference",
        "no acknowledgement-as-acceptance; no acknowledgement-as-waiver",
        "no missing-risk-acceptance-as-risk-acceptance",
        "no missing-risk-waiver-as-risk-waiver",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        11,
        "execution-risk-acceptance-prohibition-map-reference",
        "Execution Risk Acceptance Prohibition Map Reference",
        "References P4-M2.7 without treating missing acceptance as risk acceptance or absence of acceptance as waiver.",
        "risk-acceptance-prohibition-map-reference",
        "no acceptance-prohibition-as-waiver; no absence-of-acceptance-as-waiver",
        "no missing-risk-acceptance-as-risk-acceptance",
        "no acceptance semantics; no waiver semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        12,
        "execution-risk-waiver-prohibition-map-reference",
        "Execution Risk Waiver Prohibition Map Reference",
        "References P4-M2.8 without creating waiver evidence, waiver approval, waiver authorization, or risk waiver.",
        "risk-waiver-prohibition-map-reference",
        "no waiver evidence creation; no waiver approval; no waiver authorization",
        "no missing-risk-waiver-as-risk-waiver",
        "no waiver semantics; no authorization semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        13,
        "execution-surface-reference",
        "Execution Surface Reference",
        "References P4-M2.1 without activating an executable surface, API, MCP, connector, agent call, UI, deploy, or product-code auto-call.",
        "execution-surface-reference",
        "no reference-as-execution; no execution hint",
        "no API; no MCP; no connector; no agent call",
        "no Codex/Hermes/ChatGPT product-code auto-call; no execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        14,
        "execution-contract-validation-matrix-reference",
        "Execution Contract Validation Matrix Reference",
        "References P4-M2.2 without live contract validation, input validation, record validation, validation verdict, or readiness verdict.",
        "contract-validation-matrix-reference",
        "no live contract validation; no input validation; no record validation",
        "no validation verdict; no readiness verdict",
        "no validation semantics; no readiness semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        15,
        "silence-non-consent-boundary-category",
        "Silence Non-Consent Boundary Category",
        "Classifies silence, non-response, missing records, and missing evidence as non-consent boundaries only.",
        "silence-non-consent-boundary-category",
        "silence is not consent; non-response is not consent",
        "missing record is not consent; missing evidence is not consent",
        "no consent semantics; no non-consent execution semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        16,
        "missing-evidence-as-consent-prohibition-signal",
        "Missing Evidence As Consent Prohibition Signal",
        "Defines the signal that missing evidence, missing record, missing objection, missing rejection, and missing denial never become consent, approval, or permission.",
        "missing-evidence-prohibition-signal",
        "no missing-evidence-as-consent; no missing-record-as-consent",
        "no missing-objection-as-approval; no missing-rejection-as-approval",
        "no missing-denial-as-permission; no permission semantics",
    ),
    ExecutionDecisionSilenceNonConsentMapField(
        17,
        "consent-semantics-disabled",
        "Consent Semantics Disabled",
        "Makes explicit that the map grants no consent semantics, permission semantics, authorization semantics, confirmation semantics, approval semantics, recommendation semantics, readiness semantics, validation semantics, or execution semantics.",
        "consent-semantics-disabled",
        "no silence-as-consent; no non-response-as-consent",
        "no consent validation; no consent record creation; no non-consent record creation",
        "no consent semantics; no non-consent execution semantics; no execution semantics",
    ),
)


def list_execution_decision_silence_non_consent_map_fields() -> tuple[
    ExecutionDecisionSilenceNonConsentMapField,
    ...,
]:
    return _EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_FIELDS


def execution_decision_silence_non_consent_map_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_execution_decision_silence_non_consent_map_fields()
    )


def render_execution_decision_silence_non_consent_map_markdown(
    fields: Sequence[ExecutionDecisionSilenceNonConsentMapField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_silence_non_consent_map_fields()
    )
    status = execution_decision_silence_non_consent_map_report()
    lines = [
        "# P4-M2.12 Execution Decision Silence Non-Consent Map",
        "",
        "P4-M2.12 Execution Decision Silence Non-Consent Map.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M2.1 Execution Surface Contract Definition remains a referenced definition layer.",
        "",
        "P4-M2.2 Execution Contract Validation Matrix remains a referenced definition layer.",
        "",
        "P4-M2.3 Manual Authorization Evidence Envelope remains a referenced definition layer.",
        "",
        "P4-M2.4 Human Confirmation Snapshot Contract remains a referenced definition layer.",
        "",
        "P4-M2.5 Execution Preconditions Snapshot Map remains a referenced definition layer.",
        "",
        "P4-M2.6 Execution Risk Acknowledgement Map remains a referenced definition layer.",
        "",
        "P4-M2.7 Execution Risk Acceptance Prohibition Map remains a referenced definition layer.",
        "",
        "P4-M2.8 Execution Risk Waiver Prohibition Map remains a referenced definition layer.",
        "",
        "P4-M2.9 Execution Decision Non-Equivalence Map remains a referenced definition layer.",
        "",
        "P4-M2.10 Execution Decision Recommendation Prohibition Map remains a referenced definition layer.",
        "",
        "P4-M2.11 Execution Decision Default Denial Boundary Map remains a referenced definition layer.",
        "",
    ]
    for phrase in _BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend(
        [
            EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        ["", "## Execution Decision Silence Non-Consent Map Fields", ""]
    )
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Silence non-consent boundary category: {field.silence_non_consent_boundary_category}",
                f"- Missing evidence as consent prohibition signal: {field.missing_evidence_as_consent_prohibition_signal}",
                f"- Consent semantics disabled: {field.consent_semantics_disabled}",
                f"- Non-consent execution semantics disabled: {field.non_consent_execution_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_decision_silence_non_consent_map_as_dicts(
    fields: Sequence[ExecutionDecisionSilenceNonConsentMapField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_silence_non_consent_map_fields()
    )
    return tuple(asdict(field) for field in field_values)


def execution_decision_silence_non_consent_map_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.12",
        "feature": "Execution Decision Silence Non-Consent Map",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "execution_decision_silence_non_consent_map_field_count": len(
            _EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_FIELDS
        ),
        "p4_m2_started": True,
        "execution_surface_contract_definition_available": True,
        "execution_contract_validation_matrix_available": True,
        "manual_authorization_evidence_envelope_available": True,
        "human_confirmation_snapshot_contract_available": True,
        "execution_preconditions_snapshot_map_available": True,
        "execution_risk_acknowledgement_map_available": True,
        "execution_risk_acceptance_prohibition_map_available": True,
        "execution_risk_waiver_prohibition_map_available": True,
        "execution_decision_non_equivalence_map_available": True,
        "execution_decision_recommendation_prohibition_map_available": True,
        "execution_decision_default_denial_boundary_map_available": True,
        "execution_decision_silence_non_consent_map_started": True,
        "execution_decision_silence_non_consent_map_definition_only": True,
        "decision_silence_non_consent_map_fields_defined": True,
        "silence_as_consent_prohibited": True,
        "non_response_as_consent_prohibited": True,
        "missing_record_as_consent_prohibited": True,
        "missing_evidence_as_consent_prohibited": True,
        "missing_objection_as_approval_prohibited": True,
        "missing_rejection_as_approval_prohibited": True,
        "missing_denial_as_permission_prohibited": True,
        "missing_confirmation_as_confirmation_prohibited": True,
        "missing_authorization_as_authorization_prohibited": True,
        "missing_recommendation_as_recommendation_prohibited": True,
        "missing_readiness_as_readiness_prohibited": True,
        "missing_validation_as_validation_prohibited": True,
        "missing_risk_acceptance_as_risk_acceptance_prohibited": True,
        "missing_risk_waiver_as_risk_waiver_prohibited": True,
        "consent_semantics_disabled": True,
        "non_consent_execution_semantics_disabled": True,
        "default_denial_map_as_consent_prohibited": True,
        "default_denial_map_as_execution_prohibited": True,
        "reference_as_consent_prohibited": True,
        "execution_enabled": False,
        "decision_execution_enabled": False,
        "confirmation_enabled": False,
        "decision_confirmation_enabled": False,
        "authorization_enabled": False,
        "decision_authorization_enabled": False,
        "approval_enabled": False,
        "default_approval_enabled": False,
        "decision_approval_enabled": False,
        "rejection_enabled": False,
        "live_rejection_enabled": False,
        "active_denial_enabled": False,
        "decision_rejection_enabled": False,
        "consent_validation_enabled": False,
        "live_consent_validation_enabled": False,
        "consent_record_creation_enabled": False,
        "non_consent_record_creation_enabled": False,
        "risk_acceptance_enabled": False,
        "risk_waiver_enabled": False,
        "implied_risk_acceptance_enabled": False,
        "implied_risk_waiver_enabled": False,
        "acknowledgement_as_acceptance_enabled": False,
        "acknowledgement_as_waiver_enabled": False,
        "acceptance_prohibition_as_waiver_enabled": False,
        "absence_of_acceptance_as_waiver_enabled": False,
        "waiver_evidence_creation_enabled": False,
        "waiver_approval_enabled": False,
        "waiver_authorization_enabled": False,
        "live_risk_acknowledgement_enabled": False,
        "memory_mutation_enabled": False,
        "memory_record_creation_enabled": False,
        "memory_record_update_enabled": False,
        "memory_record_deletion_enabled": False,
        "proposal_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "source_fetching_enabled": False,
        "provenance_writing_enabled": False,
        "evidence_mutation_enabled": False,
        "citation_mutation_enabled": False,
        "live_confirmation_validation_enabled": False,
        "live_authorization_validation_enabled": False,
        "live_contract_validation_enabled": False,
        "input_validation_enabled": False,
        "record_validation_enabled": False,
        "validation_verdict_enabled": False,
        "readiness_verdict_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "suggested_next_action_enabled": False,
        "default_readiness_enabled": False,
        "auto_pass_enabled": False,
        "auto_execution_hint_enabled": False,
        "advisory_verdict_enabled": False,
        "execution_hint_enabled": False,
        "authorization_hint_enabled": False,
        "confirmation_hint_enabled": False,
        "readiness_hint_enabled": False,
        "validation_hint_enabled": False,
        "default_allow_enabled": False,
        "default_permit_enabled": False,
        "default_continue_enabled": False,
        "default_execute_enabled": False,
        "default_mutate_enabled": False,
        "consent_semantics_granted": False,
        "non_consent_execution_semantics_granted": False,
        "decision_equivalence_semantics_granted": False,
        "recommendation_semantics_granted": False,
        "ranking_semantics_granted": False,
        "next_action_semantics_granted": False,
        "default_allowance_semantics_granted": False,
        "permission_semantics_granted": False,
        "denial_execution_semantics_granted": False,
        "rejection_execution_semantics_granted": False,
        "acceptance_semantics_granted": False,
        "waiver_semantics_granted": False,
        "acknowledgement_semantics_granted": False,
        "confirmation_semantics_granted": False,
        "authorization_semantics_granted": False,
        "execution_semantics_granted": False,
        "api_enabled": False,
        "mcp_enabled": False,
        "connector_enabled": False,
        "agent_call_enabled": False,
        "codex_hermes_chatgpt_product_code_auto_call_enabled": False,
        "p4_m3_started": False,
        "p4_m4_started": False,
        "p4_m5_started": False,
        "v7_started": False,
        "productization_started": False,
        "ui_started": False,
        "operator_console_started": False,
        "mvp_started": False,
        "deploy_started": False,
        "full_memory_graph_started": False,
        "package_version": P4_M2_12_PACKAGE_VERSION,
        "boundary": EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY,
    }


_SOURCE_REFERENCE_FIELD_ID_COUNTS = {
    "execution_surface_contract_field_count": len(execution_surface_contract_field_ids()),
    "execution_contract_validation_matrix_field_count": len(
        execution_contract_validation_matrix_field_ids()
    ),
    "manual_authorization_evidence_envelope_field_count": len(
        manual_authorization_evidence_envelope_field_ids()
    ),
    "human_confirmation_snapshot_contract_field_count": len(
        human_confirmation_snapshot_contract_field_ids()
    ),
    "execution_preconditions_snapshot_map_field_count": len(
        execution_preconditions_snapshot_map_field_ids()
    ),
    "execution_risk_acknowledgement_map_field_count": len(
        execution_risk_acknowledgement_map_field_ids()
    ),
    "execution_risk_acceptance_prohibition_map_field_count": len(
        execution_risk_acceptance_prohibition_map_field_ids()
    ),
    "execution_risk_waiver_prohibition_map_field_count": len(
        execution_risk_waiver_prohibition_map_field_ids()
    ),
    "execution_decision_non_equivalence_map_field_count": len(
        execution_decision_non_equivalence_map_field_ids()
    ),
    "execution_decision_recommendation_prohibition_map_field_count": len(
        execution_decision_recommendation_prohibition_map_field_ids()
    ),
    "execution_decision_default_denial_boundary_map_field_count": len(
        execution_decision_default_denial_boundary_map_field_ids()
    ),
}


if len(_EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_FIELDS) != 17:
    raise RuntimeError(
        "P4-M2.12 execution decision silence non-consent map must define 17 fields"
    )

if any(count <= 0 for count in _SOURCE_REFERENCE_FIELD_ID_COUNTS.values()):
    raise RuntimeError("P4-M2.12 source definition references must remain available")
