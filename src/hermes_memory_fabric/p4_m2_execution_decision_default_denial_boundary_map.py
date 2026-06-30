from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
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


P4_M2_11_PACKAGE_VERSION = "6.16.0"

EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_BOUNDARY = (
    "P4-M2.11 Execution Decision Default Denial Boundary Map read-only "
    "definition-only inspection-only. It defines a stable read-only structure "
    "that explicitly prevents absence of confirmation, authorization, approval, "
    "recommendation, readiness, validation, risk acceptance, risk waiver, operator "
    "action, or decision evidence from being treated as permission, recommendation, "
    "ranking, suggested next action, default approval, default readiness, auto-pass, "
    "auto-execution hint, advisory verdict, execution hint, authorization hint, "
    "confirmation hint, readiness hint, validation hint, execution, authorization, "
    "confirmation, approval, rejection, risk acceptance, risk waiver, readiness, "
    "validation, or mutation. It references P4-M2.1 Execution Surface Contract Definition, "
    "P4-M2.2 Execution Contract Validation Matrix, P4-M2.3 Manual Authorization "
    "Evidence Envelope, P4-M2.4 Human Confirmation Snapshot Contract, P4-M2.5 "
    "Execution Preconditions Snapshot Map, P4-M2.6 Execution Risk Acknowledgement "
    "Map, P4-M2.7 Execution Risk Acceptance Prohibition Map, P4-M2.8 Execution "
    "Risk Waiver Prohibition Map, P4-M2.9 Execution Decision Non-Equivalence "
    "Map, and P4-M2.10 Execution Decision Recommendation Prohibition Map as "
    "definition layers only. no execution. no decision execution. "
    "no confirmation. no decision confirmation. no authorization. "
    "no decision authorization. no approval. no default approval. "
    "no decision approval. no rejection. no decision rejection. no risk acceptance. "
    "no risk waiver. no implied risk acceptance. no implied risk waiver. "
    "no acknowledgement-as-acceptance. no acknowledgement-as-waiver. "
    "no acceptance-prohibition-as-waiver. no absence-of-acceptance-as-waiver. "
    "no waiver evidence creation. no waiver approval. no waiver authorization. "
    "no manual-decision-as-execution. no manual-decision-as-authorization. "
    "no manual-decision-as-confirmation. no manual-decision-as-approval. "
    "no manual-decision-as-recommendation. no operator-as-authorization. "
    "no operator-as-confirmation. no operator-as-approval. "
    "no operator-as-recommendation. no risk-map-as-readiness. "
    "no risk-map-as-validation. no risk-map-as-recommendation. "
    "no non-equivalence-map-as-recommendation. no reference-as-verdict. "
    "no reference-as-execution. no reference-as-authorization. "
    "no reference-as-confirmation. no reference-as-approval. "
    "no reference-as-recommendation. no recommendation-map-as-approval. "
    "no recommendation-map-as-readiness. no decision recommendation. "
    "no decision ranking. no suggested next action. no default readiness. "
    "no default allow. no default permit. no default continue. no default execute. "
    "no default mutate. no auto-pass. no auto-execution hint. no advisory verdict. no execution hint. "
    "no authorization hint. no confirmation hint. no readiness hint. "
    "no validation hint. no live risk acknowledgement. no memory mutation. "
    "no memory record creation. no memory record update. no memory record deletion. "
    "no proposal mutation. no lifecycle mutation. no retry policy mutation. "
    "no source fetching. no provenance writing. no evidence mutation. "
    "no citation mutation. no live confirmation validation. "
    "no live authorization validation. no live contract validation. "
    "no input validation. no record validation. no live rejection. no active denial. "
    "no absence-as-permission. no absence-as-approval. no absence-as-recommendation. "
    "no absence-as-readiness. no absence-as-validation. no absence-as-authorization. "
    "no absence-as-confirmation. no absence-as-risk-acceptance. no absence-as-risk-waiver. "
    "no validation verdict. no readiness verdict. no automatic readiness verdict. "
    "no decision equivalence semantics. no recommendation semantics. "
    "no ranking semantics. no next-action semantics. no default-allowance semantics. "
    "no permission semantics. no denial execution semantics. no rejection execution semantics. no acceptance semantics. "
    "no waiver semantics. no acknowledgement semantics. no confirmation semantics. "
    "no authorization semantics. no execution semantics. no API. no MCP. "
    "no connector. no agent call. no Codex/Hermes/ChatGPT product-code auto-call. "
    "no P4-M3. no P4-M4. no P4-M5. no v7. no productization. no UI. "
    "no Operator Console. no MVP. no deploy. no full Memory Graph."
)


@dataclass(frozen=True)
class ExecutionDecisionDefaultDenialBoundaryMapField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    default_denial_boundary_category: str
    absence_as_permission_prohibition_signal: str
    default_no_action_signal: str
    default_allowance_semantics_disabled: str
    default_denial_semantics_disabled: str


_EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_FIELDS: tuple[
    ExecutionDecisionDefaultDenialBoundaryMapField,
    ...,
] = (
    ExecutionDecisionDefaultDenialBoundaryMapField(
        1,
        "execution-decision-default-denial-boundary-map-id",
        "Execution Decision Default Denial Boundary Map Identifier",
        "Names the inspection-only default denial boundary map without creating recommendation, ranking, suggested next action, default approval, default readiness, hint, verdict, execution, decision, risk, validation, or mutation state.",
        "map-identity",
        "The identifier is no decision ranking and no ranking semantics.",
        "The identifier is no suggested next action and no next-action semantics.",
        "The identifier is no default approval, no default readiness, no auto-pass, and no automatic readiness verdict.",
        "no recommendation semantics; no ranking semantics; no next-action semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        2,
        "execution-decision-recommendation-prohibition-map-reference",
        "Execution Decision Recommendation Prohibition Map Reference",
        "References P4-M2.10 as read-only context without treating recommendation prohibition boundaries as approval, readiness, recommendation, ranking, suggested next action, advisory verdict, hint, permission, or mutation.",
        "recommendation-prohibition-map-reference",
        "Recommendation prohibition map reference is no recommendation-map-as-approval, no recommendation-map-as-readiness, and no absence-as-recommendation.",
        "Recommendation prohibition map reference is no suggested next action, no default continue, no default execute, and no execution hint.",
        "Recommendation prohibition map reference is no default allow, no default permit, no default approval, no default readiness, and no default-allowance semantics.",
        "no recommendation-map-as-approval; no recommendation-map-as-readiness; no permission semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        3,
        "execution-decision-non-equivalence-map-reference",
        "Execution Decision Non-Equivalence Map Reference",
        "References P4-M2.9 as read-only context without treating non-equivalence boundaries as permission, recommendation, ranking, suggested next action, default readiness, advisory verdict, hint, or mutation.",
        "non-equivalence-map-reference",
        "Non-equivalence map reference is no non-equivalence-map-as-recommendation and no absence-as-permission.",
        "Non-equivalence map reference is no suggested next action, no execution hint, and no authorization hint.",
        "Non-equivalence map reference is no reference-as-verdict, no default allow, no default readiness, and no readiness hint.",
        "no non-equivalence-map-as-recommendation; no reference-as-recommendation; no permission semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        4,
        "manual-decision-reference",
        "Manual Decision Reference",
        "References future manual decision material without treating absence of separate evidence as permission, recommendation, ranking, suggested next action, default approval, default readiness, execution, authorization, confirmation, approval, rejection, or mutation.",
        "manual-decision-reference",
        "Manual decision reference is no manual-decision-as-recommendation and no absence-as-permission.",
        "Manual decision reference is no suggested next action, no default execute, no auto-execution hint, and no execution hint.",
        "Manual decision reference is no default approval, no default readiness, no readiness hint, and no validation hint.",
        "no manual-decision-as-recommendation; no decision recommendation; no permission semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        5,
        "operator-reference",
        "Operator Reference",
        "References an operator label without treating operator presence or silence as authorization, confirmation, approval, recommendation, permission, execution, default allow, default continue, or mutation.",
        "operator-reference",
        "Operator reference is no operator-as-recommendation, no operator-as-authorization, and no absence-as-permission.",
        "Operator reference is no suggested next action, no confirmation hint, no authorization hint, and no default continue.",
        "Operator reference is no default approval, no default readiness, no operator-as-approval, and no operator-as-confirmation.",
        "no operator-as-recommendation; no permission semantics; no authorization semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        6,
        "execution-risk-acknowledgement-map-reference",
        "Execution Risk Acknowledgement Map Reference",
        "References P4-M2.6 as read-only context without treating acknowledgement or absence of acceptance/waiver evidence as permission, recommendation, readiness, validation, live risk acknowledgement, risk acceptance, risk waiver, hint, verdict, or mutation.",
        "risk-acknowledgement-map-reference",
        "Risk acceptance prohibition map reference is no risk-map-as-recommendation and no ranking semantics.",
        "Risk acceptance prohibition map reference is no suggested next action, no acceptance-prohibition-as-waiver, and no absence-of-acceptance-as-waiver.",
        "Risk acceptance prohibition map reference is no default readiness, no risk-map-as-readiness, no risk-map-as-validation, and no reference-as-verdict.",
        "no acceptance semantics; no waiver semantics; no recommendation semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        7,
        "execution-risk-acceptance-prohibition-map-reference",
        "Execution Risk Acceptance Prohibition Map Reference",
        "References P4-M2.7 as read-only context without converting acceptance prohibition or absence of acceptance into recommendation, waiver, permission, readiness, validation, approval, next action, or mutation.",
        "risk-acceptance-prohibition-map-reference",
        "Risk waiver prohibition map reference is no risk-map-as-recommendation and no decision ranking.",
        "Risk waiver prohibition map reference is no suggested next action, no waiver evidence creation, no waiver approval, and no waiver authorization.",
        "Risk waiver prohibition map reference is no default readiness, no risk-map-as-readiness, no risk-map-as-validation, and no reference-as-verdict.",
        "no waiver semantics; no recommendation semantics; no authorization semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        8,
        "execution-risk-waiver-prohibition-map-reference",
        "Execution Risk Waiver Prohibition Map Reference",
        "References P4-M2.8 as read-only context without creating recommendation, waiver evidence, waiver approval, waiver authorization, readiness, validation, next action, hint, verdict, permission, or mutation.",
        "risk-waiver-prohibition-map-reference",
        "Preconditions snapshot map reference is no decision ranking and no recommendation semantics.",
        "Preconditions snapshot map reference is no suggested next action, no execution hint, and no live contract validation.",
        "Preconditions snapshot map reference is no default readiness, no readiness verdict, no validation verdict, no input validation, and no record validation.",
        "no next-action semantics; no readiness hint; no validation hint.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        9,
        "execution-preconditions-snapshot-map-reference",
        "Execution Preconditions Snapshot Map Reference",
        "References P4-M2.5 as read-only context without satisfying preconditions, recommending action, ranking decisions, creating default readiness, validating live input, validating records, permitting, or mutating.",
        "preconditions-snapshot-map-reference",
        "Execution surface reference is no decision ranking, no auto-pass, and no recommendation semantics.",
        "Execution surface reference is no suggested next action, no auto-execution hint, no execution hint, and no Codex/Hermes/ChatGPT product-code auto-call.",
        "Execution surface reference is no default approval, no default readiness, no readiness hint, and no validation hint.",
        "no execution semantics; no API; no MCP; no connector; no agent call.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        10,
        "execution-surface-reference",
        "Execution Surface Reference",
        "References P4-M2.1 as read-only context without activating an executable surface, API, MCP, connector, agent call, product-code auto-call, UI, Operator Console, deploy, recommendation, permission, or hint.",
        "execution-surface-reference",
        "Validation matrix reference is no decision ranking and no recommendation semantics.",
        "Validation matrix reference is no suggested next action, no advisory verdict, and no validation hint.",
        "Validation matrix reference is no live contract validation, no validation verdict, no readiness verdict, no default readiness, and no reference-as-verdict.",
        "no validation verdict; no readiness verdict; no recommendation semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        11,
        "execution-contract-validation-matrix-reference",
        "Execution Contract Validation Matrix Reference",
        "References P4-M2.2 as read-only context without live contract validation, validation verdict, readiness verdict, recommendation, ranking, suggested next action, default readiness, approval, permission, or mutation.",
        "contract-validation-matrix-reference",
        "Authorization evidence envelope reference is no decision ranking and no recommendation semantics.",
        "Authorization evidence envelope reference is no suggested next action, no authorization hint, and no live authorization validation.",
        "Authorization evidence envelope reference is no default approval, no default readiness, no provenance writing, no evidence mutation, and no citation mutation.",
        "no authorization semantics; no recommendation semantics; no confirmation semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        12,
        "manual-authorization-evidence-envelope-reference",
        "Manual Authorization Evidence Envelope Reference",
        "References P4-M2.3 as read-only context without validating authorization live, authorizing, approving, recommending, ranking, suggesting action, permitting, writing provenance, mutating evidence, or mutating citations.",
        "manual-authorization-evidence-envelope-reference",
        "Human confirmation snapshot reference is no decision ranking and no recommendation semantics.",
        "Human confirmation snapshot reference is no suggested next action, no confirmation hint, and no live confirmation validation.",
        "Human confirmation snapshot reference is no default approval, no default readiness, no readiness verdict, and no validation verdict.",
        "no confirmation semantics; no authorization semantics; no recommendation semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        13,
        "human-confirmation-snapshot-reference",
        "Human Confirmation Snapshot Reference",
        "References P4-M2.4 as read-only context without validating confirmation live, confirming, authorizing, approving, recommending, ranking, suggesting action, permitting, readiness, or mutation.",
        "human-confirmation-snapshot-reference",
        "The category marks decision ranking, ranking semantics, and advisory verdicts as disabled.",
        "The category marks suggested next action, next-action semantics, execution hint, authorization hint, and confirmation hint as disabled.",
        "The category marks default approval, default readiness, readiness hint, validation hint, readiness verdict, and validation verdict as disabled.",
        "no recommendation semantics; no ranking semantics; no next-action semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        14,
        "default-denial-boundary-category",
        "Absence As Permission Prohibition Signal",
        "Defines the signal that no field ranks decisions, creates priorities, establishes recommendation order, auto-passes readiness, or produces advisory verdicts.",
        "default-denial-boundary-category",
        "The signal is no decision ranking and no ranking semantics.",
        "The signal is no suggested next action and no next-action semantics.",
        "The signal is no auto-pass, no advisory verdict, no readiness verdict, no validation verdict, and no automatic readiness verdict.",
        "no ranking semantics; no recommendation semantics; no readiness verdict.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        15,
        "absence-as-permission-prohibition-signal",
        "Default No Action Signal",
        "Defines the signal that no field suggests, hints, defaults, recommends, executes, authorizes, confirms, approves, rejects, validates, accepts risk, waives risk, or mutates.",
        "absence-as-permission-prohibition-signal",
        "The signal is no decision recommendation, no decision ranking, and no ranking semantics.",
        "The signal is no suggested next action, no auto-execution hint, no execution hint, no authorization hint, and no confirmation hint.",
        "The signal is no default approval, no default readiness, no readiness hint, and no validation hint.",
        "no next-action semantics; no execution semantics; no authorization semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        16,
        "default-no-action-signal",
        "Default Allowance Semantics Disabled",
        "Defines the signal that no field creates default readiness, automatic readiness verdict, auto-pass, validation hint, readiness hint, default approval, readiness verdict, validation verdict, or advisory verdict.",
        "default-no-action-signal",
        "The signal is no decision ranking, no advisory verdict, and no reference-as-recommendation.",
        "The signal is no suggested next action, no default approval, and no auto-execution hint.",
        "The signal is no default readiness, no auto-pass, no readiness hint, no validation hint, no readiness verdict, and no automatic readiness verdict.",
        "no readiness verdict; no validation verdict; no recommendation semantics.",
    ),
    ExecutionDecisionDefaultDenialBoundaryMapField(
        17,
        "default-allowance-semantics-disabled",
        "Default Denial Semantics Disabled",
        "Makes explicit that the map grants no recommendation semantics, ranking semantics, next-action semantics, decision equivalence semantics, acceptance semantics, waiver semantics, acknowledgement semantics, confirmation semantics, authorization semantics, execution semantics, or mutation.",
        "default-allowance-semantics-disabled",
        "Disabled recommendation semantics prevent decision recommendation, reference-as-recommendation, manual-decision-as-recommendation, operator-as-recommendation, risk-map-as-recommendation, and non-equivalence-map-as-recommendation.",
        "Disabled recommendation semantics prevent suggested next action, next-action semantics, hints, authorization hints, confirmation hints, and execution hints.",
        "Disabled recommendation semantics prevent default approval, default readiness, auto-pass, advisory verdict, readiness verdict, validation verdict, and automatic readiness verdict.",
        "no recommendation semantics; no ranking semantics; no next-action semantics; no decision equivalence semantics; no execution semantics.",
    ),
)


def list_execution_decision_default_denial_boundary_map_fields() -> tuple[
    ExecutionDecisionDefaultDenialBoundaryMapField,
    ...,
]:
    return _EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_FIELDS


def execution_decision_default_denial_boundary_map_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_execution_decision_default_denial_boundary_map_fields()
    )


def render_execution_decision_default_denial_boundary_map_markdown(
    fields: Sequence[ExecutionDecisionDefaultDenialBoundaryMapField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_default_denial_boundary_map_fields()
    )
    status = execution_decision_default_denial_boundary_map_report()
    lines = [
        "# P4-M2.11 Execution Decision Default Denial Boundary Map",
        "",
        "P4-M2.11 Execution Decision Default Denial Boundary Map.",
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
    ]
    for phrase in _BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend(
        [
            EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        ["", "## Execution Decision Default Denial Boundary Map Fields", ""]
    )
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Default denial boundary category: {field.default_denial_boundary_category}",
                f"- Absence as permission prohibition signal: {field.absence_as_permission_prohibition_signal}",
                f"- Default no action signal: {field.default_no_action_signal}",
                f"- Default allowance semantics disabled: {field.default_allowance_semantics_disabled}",
                f"- Default denial semantics disabled: {field.default_denial_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_decision_default_denial_boundary_map_as_dicts(
    fields: Sequence[ExecutionDecisionDefaultDenialBoundaryMapField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_decision_default_denial_boundary_map_fields()
    )
    return tuple(asdict(field) for field in field_values)


def execution_decision_default_denial_boundary_map_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.11",
        "feature": "Execution Decision Default Denial Boundary Map",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "execution_decision_default_denial_boundary_map_field_count": len(
            _EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_FIELDS
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
        "execution_decision_default_denial_boundary_map_started": True,
        "execution_decision_default_denial_boundary_map_definition_only": True,
        "decision_default_denial_boundary_map_fields_defined": True,
        "absence_as_permission_prohibited": True,
        "absence_as_approval_prohibited": True,
        "absence_as_recommendation_prohibited": True,
        "absence_as_readiness_prohibited": True,
        "absence_as_validation_prohibited": True,
        "absence_as_authorization_prohibited": True,
        "absence_as_confirmation_prohibited": True,
        "absence_as_risk_acceptance_prohibited": True,
        "absence_as_risk_waiver_prohibited": True,
        "default_no_action_signal_defined": True,
        "default_allowance_semantics_disabled": True,
        "manual_decision_as_recommendation_prohibited": True,
        "operator_as_recommendation_prohibited": True,
        "risk_map_as_recommendation_prohibited": True,
        "non_equivalence_map_as_recommendation_prohibited": True,
        "reference_as_recommendation_prohibited": True,
        "suggested_next_action_prohibited": True,
        "default_readiness_prohibited": True,
        "default_approval_prohibited": True,
        "auto_pass_prohibited": True,
        "auto_execution_hint_prohibited": True,
        "advisory_verdict_prohibited": True,
        "execution_hint_prohibited": True,
        "authorization_hint_prohibited": True,
        "confirmation_hint_prohibited": True,
        "readiness_hint_prohibited": True,
        "validation_hint_prohibited": True,
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
        "absence_as_permission_enabled": False,
        "absence_as_approval_enabled": False,
        "absence_as_recommendation_enabled": False,
        "absence_as_readiness_enabled": False,
        "absence_as_validation_enabled": False,
        "absence_as_authorization_enabled": False,
        "absence_as_confirmation_enabled": False,
        "absence_as_risk_acceptance_enabled": False,
        "absence_as_risk_waiver_enabled": False,
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
        "package_version": P4_M2_11_PACKAGE_VERSION,
        "boundary": EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_BOUNDARY,
    }


_BOUNDARY_PHRASE_LINES = (
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
    "no risk acceptance",
    "no risk waiver",
    "no implied risk acceptance",
    "no implied risk waiver",
    "no acknowledgement-as-acceptance",
    "no acknowledgement-as-waiver",
    "no acceptance-prohibition-as-waiver",
    "no absence-of-acceptance-as-waiver",
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
    "no reference-as-verdict",
    "no reference-as-execution",
    "no reference-as-authorization",
    "no reference-as-confirmation",
    "no reference-as-approval",
    "no reference-as-recommendation",
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
}


if len(_EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_FIELDS) != 17:
    raise RuntimeError(
        "P4-M2.11 execution decision default denial boundary map must define 17 fields"
    )

if any(count <= 0 for count in _SOURCE_REFERENCE_FIELD_ID_COUNTS.values()):
    raise RuntimeError("P4-M2.11 source definition references must remain available")
