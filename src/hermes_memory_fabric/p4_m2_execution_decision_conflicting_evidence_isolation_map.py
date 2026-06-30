from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
)
from .p4_m2_execution_decision_default_denial_boundary_map import (
    execution_decision_default_denial_boundary_map_field_ids,
)
from .p4_m2_execution_decision_negative_evidence_non_override_map import (
    execution_decision_negative_evidence_non_override_map_field_ids,
)
from .p4_m2_execution_decision_non_equivalence_map import (
    execution_decision_non_equivalence_map_field_ids,
)
from .p4_m2_execution_decision_recommendation_prohibition_map import (
    execution_decision_recommendation_prohibition_map_field_ids,
)
from .p4_m2_execution_decision_silence_non_consent_map import (
    execution_decision_silence_non_consent_map_field_ids,
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


P4_M2_14_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class ExecutionDecisionConflictingEvidenceIsolationMapField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    conflict_isolation_boundary_category: str
    conflict_context_isolated: str
    isolation_semantics_disabled: str


BOUNDARY_PHRASE_LINES = (
    "P4-M2.14",
    "Execution Decision Conflicting Evidence Isolation Map",
    "read-only",
    "definition-only",
    "inspection-only",
    "conflicting evidence is isolated",
    "conflicting evidence is not resolved",
    "conflicting evidence is not merged",
    "conflicting evidence is not reconciled",
    "conflicting evidence is not valid",
    "conflicting evidence is not approval",
    "conflicting evidence is not authorization",
    "conflicting evidence is not readiness",
    "conflicting evidence is not execution",
    "ambiguous evidence is not resolved",
    "unresolved evidence is not resolved",
    "contradictory evidence is not reconciled",
    "positive-looking reference is not resolution",
    "positive-looking reference is not override",
    "no conflict resolution",
    "no evidence resolution",
    "no evidence merge",
    "no evidence reconciliation",
    "no evidence arbitration",
    "no evidence precedence",
    "no evidence tie-breaker",
    "no conflict resolution record creation",
    "no evidence merge record creation",
    "no evidence arbitration record creation",
    "no evidence override",
    "no approval override",
    "no authorization override",
    "no readiness override",
    "no execution override",
    "no consent override",
    "no risk acceptance override",
    "no risk waiver override",
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
    "no evidence validation",
    "no live evidence validation",
    "no consent validation",
    "no live consent validation",
    "no evidence override record creation",
    "no approval override record creation",
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
    "no conflicting-evidence-as-resolved",
    "no conflicting-evidence-as-merged",
    "no conflicting-evidence-as-reconciled",
    "no conflicting-evidence-as-valid",
    "no conflicting-evidence-as-approval",
    "no conflicting-evidence-as-authorization",
    "no conflicting-evidence-as-readiness",
    "no conflicting-evidence-as-execution",
    "no ambiguous-evidence-as-resolved",
    "no unresolved-evidence-as-resolved",
    "no contradictory-evidence-as-reconciled",
    "no positive-reference-as-resolution",
    "no positive-reference-as-override",
    "no negative-evidence-as-approval",
    "no negative-evidence-as-authorization",
    "no negative-evidence-as-readiness",
    "no negative-evidence-as-execution",
    "no expired-evidence-as-current",
    "no stale-evidence-as-current",
    "no revoked-evidence-as-valid",
    "no superseded-evidence-as-valid",
    "no invalid-evidence-as-valid",
    "no incomplete-evidence-as-sufficient",
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
    "no silence-map-as-consent",
    "no silence-map-as-approval",
    "no silence-map-as-execution",
    "no negative-evidence-map-as-approval",
    "no negative-evidence-map-as-authorization",
    "no negative-evidence-map-as-readiness",
    "no negative-evidence-map-as-execution",
    "no negative-evidence-map-as-override",
    "no reference-as-verdict",
    "no reference-as-execution",
    "no reference-as-authorization",
    "no reference-as-confirmation",
    "no reference-as-approval",
    "no reference-as-recommendation",
    "no reference-as-consent",
    "no reference-as-override",
    "no reference-as-resolution",
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
    "no override hint",
    "no resolution hint",
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
    "no override verdict",
    "no conflict resolution verdict",
    "no automatic readiness verdict",
    "no conflict isolation semantics as execution",
    "no conflict resolution semantics",
    "no evidence resolution semantics",
    "no evidence merge semantics",
    "no evidence arbitration semantics",
    "no evidence precedence semantics",
    "no override semantics",
    "no evidence override semantics",
    "no approval override semantics",
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

EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_BOUNDARY = (
    "P4-M2.14 Execution Decision Conflicting Evidence Isolation Map read-only "
    "definition-only inspection-only. It defines a stable read-only structure "
    "that explicitly isolates conflicting evidence, mutually inconsistent evidence, "
    "contradictory evidence, unresolved evidence, ambiguous evidence, stale conflict "
    "context, expired conflict context, superseded conflict context, revoked conflict "
    "context, invalid conflict context, incomplete conflict context, missing conflict "
    "context, missing evidence, missing record, missing objection, missing rejection, "
    "missing denial, missing confirmation, missing authorization, missing approval, "
    "missing recommendation, missing readiness, missing validation, missing risk "
    "acceptance, missing risk waiver, positive-looking references, manual decision "
    "references, operator references, and prior definition-layer references as "
    "non-executable conflict context. It does not resolve, merge, reconcile, "
    "arbitrate, validate, approve, authorize, confirm, recommend, rank, ready, "
    "execute, override, accept risk, waive risk, continue, pass, suggest next "
    "action, or mutate memory. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)

_FIELD_IDS = (
    "execution-decision-conflicting-evidence-isolation-map-id",
    "execution-decision-negative-evidence-non-override-map-reference",
    "execution-decision-silence-non-consent-map-reference",
    "execution-decision-default-denial-boundary-map-reference",
    "execution-decision-recommendation-prohibition-map-reference",
    "execution-decision-non-equivalence-map-reference",
    "manual-decision-reference",
    "operator-reference",
    "human-confirmation-snapshot-reference",
    "manual-authorization-evidence-envelope-reference",
    "execution-preconditions-snapshot-map-reference",
    "execution-risk-acknowledgement-map-reference",
    "execution-risk-acceptance-prohibition-map-reference",
    "execution-risk-waiver-prohibition-map-reference",
    "execution-surface-reference",
    "execution-contract-validation-matrix-reference",
    "conflict-isolation-semantics-disabled",
)

_FIELD_NAMES = (
    "Execution Decision Conflicting Evidence Isolation Map Identifier",
    "Execution Decision Negative Evidence Non-Override Map Reference",
    "Execution Decision Silence Non-Consent Map Reference",
    "Execution Decision Default Denial Boundary Map Reference",
    "Execution Decision Recommendation Prohibition Map Reference",
    "Execution Decision Non-Equivalence Map Reference",
    "Manual Decision Reference",
    "Operator Reference",
    "Human Confirmation Snapshot Reference",
    "Manual Authorization Evidence Envelope Reference",
    "Execution Preconditions Snapshot Map Reference",
    "Execution Risk Acknowledgement Map Reference",
    "Execution Risk Acceptance Prohibition Map Reference",
    "Execution Risk Waiver Prohibition Map Reference",
    "Execution Surface Reference",
    "Execution Contract Validation Matrix Reference",
    "Conflict Isolation Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only context; "
        "conflicting evidence is isolated, conflicting evidence is not resolved, "
        "conflicting evidence is not merged, conflicting evidence is not reconciled, "
        "ambiguous evidence is not resolved, unresolved evidence is not resolved, "
        "contradictory evidence is not reconciled, positive-looking reference is not "
        "resolution, positive-looking reference is not override, and no reference-as-verdict."
    )


_EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_FIELDS = tuple(
    ExecutionDecisionConflictingEvidenceIsolationMapField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "conflicting-evidence-isolation-boundary-category",
        "conflicting evidence is isolated as non-executable conflict context",
        "no conflict resolution semantics; no evidence merge semantics; no evidence arbitration semantics",
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_execution_decision_conflicting_evidence_isolation_map_fields() -> tuple[
    ExecutionDecisionConflictingEvidenceIsolationMapField,
    ...,
]:
    return _EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_FIELDS


def execution_decision_conflicting_evidence_isolation_map_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_execution_decision_conflicting_evidence_isolation_map_fields()
    )


def render_execution_decision_conflicting_evidence_isolation_map_markdown(
    fields: Sequence[ExecutionDecisionConflictingEvidenceIsolationMapField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_conflicting_evidence_isolation_map_fields()
    )
    status = execution_decision_conflicting_evidence_isolation_map_report()
    lines = [
        "# P4-M2.14 Execution Decision Conflicting Evidence Isolation Map",
        "",
        "P4-M2.14 Execution Decision Conflicting Evidence Isolation Map.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
    ]
    for prior_layer in (
        "P4-M2.1 Execution Surface Contract Definition",
        "P4-M2.2 Execution Contract Validation Matrix",
        "P4-M2.3 Manual Authorization Evidence Envelope",
        "P4-M2.4 Human Confirmation Snapshot Contract",
        "P4-M2.5 Execution Preconditions Snapshot Map",
        "P4-M2.6 Execution Risk Acknowledgement Map",
        "P4-M2.7 Execution Risk Acceptance Prohibition Map",
        "P4-M2.8 Execution Risk Waiver Prohibition Map",
        "P4-M2.9 Execution Decision Non-Equivalence Map",
        "P4-M2.10 Execution Decision Recommendation Prohibition Map",
        "P4-M2.11 Execution Decision Default Denial Boundary Map",
        "P4-M2.12 Execution Decision Silence Non-Consent Map",
        "P4-M2.13 Execution Decision Negative Evidence Non-Override Map",
    ):
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend(
        [
            EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Execution Decision Conflicting Evidence Isolation Map Fields",
            "",
        ]
    )
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Conflict isolation boundary category: {field.conflict_isolation_boundary_category}",
                f"- Conflict context isolated: {field.conflict_context_isolated}",
                f"- Isolation semantics disabled: {field.isolation_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_decision_conflicting_evidence_isolation_map_as_dicts(
    fields: Sequence[ExecutionDecisionConflictingEvidenceIsolationMapField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_conflicting_evidence_isolation_map_fields()
    )
    return tuple(asdict(field) for field in field_values)


def execution_decision_conflicting_evidence_isolation_map_report() -> dict[str, object]:
    disabled_false_flags = {
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
        "conflict_resolution_enabled": False,
        "evidence_resolution_enabled": False,
        "evidence_merge_enabled": False,
        "evidence_reconciliation_enabled": False,
        "evidence_arbitration_enabled": False,
        "evidence_precedence_enabled": False,
        "evidence_tie_breaker_enabled": False,
        "conflict_resolution_record_creation_enabled": False,
        "evidence_merge_record_creation_enabled": False,
        "evidence_arbitration_record_creation_enabled": False,
        "evidence_validation_enabled": False,
        "live_evidence_validation_enabled": False,
        "consent_validation_enabled": False,
        "live_consent_validation_enabled": False,
        "evidence_override_record_creation_enabled": False,
        "approval_override_record_creation_enabled": False,
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
        "decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "suggested_next_action_enabled": False,
        "default_readiness_enabled": False,
        "default_allow_enabled": False,
        "default_permit_enabled": False,
        "default_continue_enabled": False,
        "default_execute_enabled": False,
        "default_mutate_enabled": False,
        "auto_pass_enabled": False,
        "auto_execution_hint_enabled": False,
        "advisory_verdict_enabled": False,
        "execution_hint_enabled": False,
        "authorization_hint_enabled": False,
        "confirmation_hint_enabled": False,
        "readiness_hint_enabled": False,
        "validation_hint_enabled": False,
        "override_hint_enabled": False,
        "resolution_hint_enabled": False,
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
        "override_verdict_enabled": False,
        "conflict_resolution_verdict_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "conflict_isolation_semantics_as_execution_granted": False,
        "conflict_resolution_semantics_granted": False,
        "evidence_resolution_semantics_granted": False,
        "evidence_merge_semantics_granted": False,
        "evidence_arbitration_semantics_granted": False,
        "evidence_precedence_semantics_granted": False,
        "override_semantics_granted": False,
        "evidence_override_semantics_granted": False,
        "approval_override_semantics_granted": False,
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
    }
    return {
        "phase": "P4-M2.14",
        "feature": "Execution Decision Conflicting Evidence Isolation Map",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "execution_decision_conflicting_evidence_isolation_map_field_count": len(
            _EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_FIELDS
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
        "execution_decision_silence_non_consent_map_available": True,
        "execution_decision_negative_evidence_non_override_map_available": True,
        "execution_decision_conflicting_evidence_isolation_map_started": True,
        "execution_decision_conflicting_evidence_isolation_map_definition_only": True,
        "decision_conflicting_evidence_isolation_map_fields_defined": True,
        "conflicting_evidence_isolated": True,
        "conflicting_evidence_as_resolved_prohibited": True,
        "conflicting_evidence_as_merged_prohibited": True,
        "conflicting_evidence_as_reconciled_prohibited": True,
        "conflicting_evidence_as_valid_prohibited": True,
        "conflicting_evidence_as_approval_prohibited": True,
        "conflicting_evidence_as_authorization_prohibited": True,
        "conflicting_evidence_as_readiness_prohibited": True,
        "conflicting_evidence_as_execution_prohibited": True,
        "ambiguous_evidence_as_resolved_prohibited": True,
        "unresolved_evidence_as_resolved_prohibited": True,
        "contradictory_evidence_as_reconciled_prohibited": True,
        "positive_reference_as_resolution_prohibited": True,
        "positive_reference_as_override_prohibited": True,
        "negative_evidence_as_approval_prohibited": True,
        "negative_evidence_as_authorization_prohibited": True,
        "negative_evidence_as_readiness_prohibited": True,
        "negative_evidence_as_execution_prohibited": True,
        "expired_evidence_as_current_prohibited": True,
        "stale_evidence_as_current_prohibited": True,
        "revoked_evidence_as_valid_prohibited": True,
        "superseded_evidence_as_valid_prohibited": True,
        "invalid_evidence_as_valid_prohibited": True,
        "incomplete_evidence_as_sufficient_prohibited": True,
        "package_version": P4_M2_14_PACKAGE_VERSION,
        "boundary": EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_BOUNDARY,
        **disabled_false_flags,
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
    "execution_decision_silence_non_consent_map_field_count": len(
        execution_decision_silence_non_consent_map_field_ids()
    ),
    "execution_decision_negative_evidence_non_override_map_field_count": len(
        execution_decision_negative_evidence_non_override_map_field_ids()
    ),
}


if len(_EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_FIELDS) != 17:
    raise RuntimeError(
        "P4-M2.14 execution decision conflicting evidence isolation map must define 17 fields"
    )

if execution_decision_conflicting_evidence_isolation_map_field_ids() != _FIELD_IDS:
    raise RuntimeError(
        "P4-M2.14 execution decision conflicting evidence isolation map field ids drifted"
    )

if any(count <= 0 for count in _SOURCE_REFERENCE_FIELD_ID_COUNTS.values()):
    raise RuntimeError("P4-M2.14 source definition references must remain available")
