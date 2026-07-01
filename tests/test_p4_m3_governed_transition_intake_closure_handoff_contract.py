from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m3_governed_transition_intake_closure_handoff_contract import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    TRUE_STATUS_FLAGS,
    GovernedTransitionIntakeClosureHandoffContractField,
    governed_transition_intake_closure_handoff_contract_as_dicts,
    governed_transition_intake_closure_handoff_contract_field_ids,
    governed_transition_intake_closure_handoff_contract_report,
    list_governed_transition_intake_closure_handoff_contract_fields,
    render_governed_transition_intake_closure_handoff_contract_markdown,
)


FIELD_IDS = (
    "p4-m3-governed-transition-intake-closure-handoff-contract-id",
    "p4-m3-governed-transition-intake-final-non-validation-boundary-audit-reference",
    "p4-m3-governed-transition-intake-package-assembly-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-safeguard-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-assumption-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-risk-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-impact-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-dependency-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-constraint-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-reason-envelope-contract-reference",
    "p4-m3-governed-transition-intake-target-phase-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-human-context-envelope-contract-reference",
    "p4-m3-governed-transition-intake-evidence-reference-envelope-contract-reference",
    "p4-m3-governed-transition-intake-request-envelope-contract-reference",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m3-governed-transition-intake-closure-handoff-scope",
    "p4-m3-governed-transition-intake-closure-handoff-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m3_closure_handoff_contract_category",
    "p4_m3_closure_handoff_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = (
    "P4-M3.14",
    "Governed Transition Intake Closure Handoff Contract",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M3.14 closure handoff contract definition only",
    "P4-M3.13 Governed Transition Intake Final Non-Validation Boundary Audit remains the source final non-validation boundary audit",
    "P4-M3.12 Governed Transition Intake Package Assembly Envelope Contract remains the source package assembly envelope boundary",
    "P4-M3.11 Governed Transition Intake Declared Transition Safeguard Envelope Contract remains the source declared transition safeguard envelope boundary",
    "P4-M3.10 Governed Transition Intake Declared Transition Assumption Envelope Contract remains the source declared transition assumption envelope boundary",
    "P4-M3.9 Governed Transition Intake Declared Transition Risk Envelope Contract remains the source declared transition risk envelope boundary",
    "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract remains the source declared transition impact envelope boundary",
    "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract remains the source declared transition dependency envelope boundary",
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract remains the source declared transition constraint envelope boundary",
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract remains the source declared transition reason envelope boundary",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract remains the source target phase envelope boundary",
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary",
    "P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary",
    "P4-M2.17 P4-M2 Closure Handoff Contract remains the prior closure handoff reference",
    "P4-M3.14 is not live validation",
    "P4-M3.14 is not transition intake validation",
    "P4-M3.14 is not package validation",
    "P4-M3.14 is not final audit validation",
    "P4-M3.14 is not closure validation",
    "P4-M3.14 is not handoff validation",
    "P4-M3.14 is not closure execution",
    "P4-M3.14 is not handoff execution",
    "P4-M3.14 is not package correctness validation",
    "P4-M3.14 is not package completeness validation",
    "P4-M3.14 is not package consistency validation",
    "P4-M3.14 is not package integrity validation",
    "P4-M3.14 is not package readiness validation",
    "P4-M3.14 is not package readiness verdict",
    "P4-M3.14 is not package validation verdict",
    "P4-M3.14 is not reference resolution",
    "P4-M3.14 is not reference integrity validation",
    "P4-M3.14 is not reference completeness validation",
    "P4-M3.14 is not transition safeguard validation",
    "P4-M3.14 is not transition assumption validation",
    "P4-M3.14 is not transition risk validation",
    "P4-M3.14 is not transition impact validation",
    "P4-M3.14 is not transition dependency validation",
    "P4-M3.14 is not transition constraint validation",
    "P4-M3.14 is not transition reason validation",
    "P4-M3.14 is not target phase validation",
    "P4-M3.14 is not target phase selection",
    "P4-M3.14 is not transition readiness validation",
    "P4-M3.14 is not readiness verdict",
    "P4-M3.14 is not validation verdict",
    "P4-M3.14 is not closure verdict",
    "P4-M3.14 is not handoff verdict",
    "P4-M3.14 is not boundary certification",
    "P4-M3.14 is not approval",
    "P4-M3.14 is not authorization",
    "P4-M3.14 is not confirmation",
    "P4-M3.14 is not recommendation",
    "P4-M3.14 is not ranking",
    "P4-M3.14 is not next action generation",
    "P4-M3.14 is not transition execution",
    "P4-M3.14 is not request validation",
    "P4-M3.14 is not evidence validation",
    "P4-M3.14 is not human context validation",
    "P4-M3.14 is not source validation",
    "P4-M3.14 is not citation validation",
    "P4-M3.14 is not transition record creation",
    "P4-M3.14 is not request record creation",
    "P4-M3.14 is not package record creation",
    "P4-M3.14 is not closure record creation",
    "P4-M3.14 is not handoff record creation",
    "P4-M3.14 is not memory mutation",
    "P4-M3.14 is not roadmap mutation",
    "P4-M3.14 is not lifecycle mutation",
    "P4-M3.14 is not proposal mutation",
    "P4-M3.14 is not source fetching",
    "P4-M3.14 is not provenance writing",
    "P4-M3.14 is not citation mutation",
    "no live validation",
    "no transition intake validation",
    "no package validation",
    "no final audit validation",
    "no closure validation",
    "no handoff validation",
    "no closure execution",
    "no handoff execution",
    "no package correctness validation",
    "no package completeness validation",
    "no package consistency validation",
    "no package integrity validation",
    "no package readiness validation",
    "no package readiness verdict",
    "no package validation verdict",
    "no reference resolution",
    "no reference integrity validation",
    "no reference completeness validation",
    "no transition safeguard validation",
    "no transition assumption validation",
    "no transition risk validation",
    "no transition impact validation",
    "no transition dependency validation",
    "no transition constraint validation",
    "no transition reason validation",
    "no target phase validation",
    "no target phase selection",
    "no readiness validation",
    "no readiness verdict",
    "no validation verdict",
    "no closure verdict",
    "no handoff verdict",
    "no boundary certification",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no next action generation",
    "no transition execution",
    "no request validation",
    "no evidence validation",
    "no memory mutation",
    "no roadmap mutation",
    "no closure record creation",
    "no handoff record creation",
    "no closure mutation",
    "no handoff mutation",
    "no P4-M4",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no MVP",
    "no deploy",
    "no full Memory Graph",
    "no version bump",
    "no tag",
)

EXPECTED_TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m3_closure_handoff_contract_definition_started",
    "p4_m3_14_governed_transition_intake_closure_handoff_contract_started",
    "p4_m3_14_definition_only",
    "p4_m3_13_final_non_validation_boundary_audit_reference_defined",
    "p4_m3_12_package_assembly_envelope_contract_reference_defined",
    "p4_m3_11_declared_transition_safeguard_envelope_contract_reference_defined",
    "p4_m3_10_declared_transition_assumption_envelope_contract_reference_defined",
    "p4_m3_9_declared_transition_risk_envelope_contract_reference_defined",
    "p4_m3_8_declared_transition_impact_envelope_contract_reference_defined",
    "p4_m3_7_declared_transition_dependency_envelope_contract_reference_defined",
    "p4_m3_6_declared_transition_constraint_envelope_contract_reference_defined",
    "p4_m3_5_declared_transition_reason_envelope_contract_reference_defined",
    "p4_m3_4_target_phase_envelope_contract_reference_defined",
    "p4_m3_3_declared_human_context_envelope_contract_reference_defined",
    "p4_m3_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m3_1_request_envelope_contract_reference_defined",
    "p4_m3_0_intake_boundary_contract_reference_defined",
    "p4_m2_17_closure_handoff_contract_reference_defined",
    "p4_m3_closure_handoff_contract_defined",
    "p4_m3_closure_handoff_scope_defined",
    "p4_m3_closure_handoff_field_shape_defined",
    "p4_m3_governed_transition_intake_static_definition_chain_closed_for_handoff",
    "p4_m3_live_validation_semantics_prohibited",
    "p4_m3_transition_intake_validation_semantics_prohibited",
    "p4_m3_transition_intake_package_validation_semantics_prohibited",
    "p4_m3_final_audit_validation_semantics_prohibited",
    "p4_m3_closure_validation_semantics_prohibited",
    "p4_m3_handoff_validation_semantics_prohibited",
    "p4_m3_closure_execution_semantics_prohibited",
    "p4_m3_handoff_execution_semantics_prohibited",
    "p4_m3_package_correctness_validation_semantics_prohibited",
    "p4_m3_package_completeness_validation_semantics_prohibited",
    "p4_m3_package_consistency_validation_semantics_prohibited",
    "p4_m3_package_integrity_validation_semantics_prohibited",
    "p4_m3_package_readiness_validation_semantics_prohibited",
    "p4_m3_package_readiness_verdict_semantics_prohibited",
    "p4_m3_package_validation_verdict_semantics_prohibited",
    "p4_m3_reference_resolution_semantics_prohibited",
    "p4_m3_reference_integrity_validation_semantics_prohibited",
    "p4_m3_reference_completeness_validation_semantics_prohibited",
    "p4_m3_boundary_certification_semantics_prohibited",
    "p4_m3_transition_safeguard_validation_semantics_prohibited",
    "p4_m3_transition_assumption_validation_semantics_prohibited",
    "p4_m3_transition_risk_validation_semantics_prohibited",
    "p4_m3_transition_impact_validation_semantics_prohibited",
    "p4_m3_transition_dependency_validation_semantics_prohibited",
    "p4_m3_transition_constraint_validation_semantics_prohibited",
    "p4_m3_transition_reason_validation_semantics_prohibited",
    "p4_m3_target_phase_validation_semantics_prohibited",
    "p4_m3_target_phase_selection_semantics_prohibited",
    "p4_m3_transition_readiness_validation_semantics_prohibited",
    "p4_m3_transition_readiness_verdict_semantics_prohibited",
    "p4_m3_transition_validation_verdict_semantics_prohibited",
    "p4_m3_closure_verdict_semantics_prohibited",
    "p4_m3_handoff_verdict_semantics_prohibited",
    "p4_m3_transition_execution_semantics_prohibited",
    "p4_m3_transition_authorization_semantics_prohibited",
    "p4_m3_transition_approval_semantics_prohibited",
    "p4_m3_transition_confirmation_semantics_prohibited",
    "p4_m3_transition_recommendation_semantics_prohibited",
    "p4_m3_transition_ranking_semantics_prohibited",
    "p4_m3_transition_next_action_semantics_prohibited",
    "p4_m3_request_validation_semantics_prohibited",
    "p4_m3_evidence_validation_semantics_prohibited",
    "p4_m3_human_context_validation_semantics_prohibited",
    "p4_m3_transition_mutation_semantics_prohibited",
    "p4_m3_closure_mutation_semantics_prohibited",
    "p4_m3_handoff_mutation_semantics_prohibited",
    "p4_m4_start_deferred",
)

EXPECTED_FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
    "boundary_validation_enabled",
    "transition_intake_validation_enabled",
    "transition_intake_package_validation_enabled",
    "final_audit_validation_enabled",
    "closure_validation_enabled",
    "handoff_validation_enabled",
    "closure_execution_enabled",
    "handoff_execution_enabled",
    "package_correctness_validation_enabled",
    "package_completeness_validation_enabled",
    "package_consistency_validation_enabled",
    "package_integrity_validation_enabled",
    "package_readiness_validation_enabled",
    "package_readiness_verdict_enabled",
    "package_validation_verdict_enabled",
    "reference_resolution_enabled",
    "reference_integrity_validation_enabled",
    "reference_completeness_validation_enabled",
    "boundary_certification_enabled",
    "package_assembly_execution_enabled",
    "package_persistence_enabled",
    "package_storage_enabled",
    "package_mutation_enabled",
    "closure_persistence_enabled",
    "closure_storage_enabled",
    "closure_mutation_enabled",
    "handoff_persistence_enabled",
    "handoff_storage_enabled",
    "handoff_mutation_enabled",
    "transition_intake_package_record_creation_enabled",
    "transition_intake_package_record_update_enabled",
    "transition_intake_package_record_deletion_enabled",
    "closure_record_creation_enabled",
    "closure_record_update_enabled",
    "closure_record_deletion_enabled",
    "handoff_record_creation_enabled",
    "handoff_record_update_enabled",
    "handoff_record_deletion_enabled",
    "transition_safeguard_validation_enabled",
    "transition_assumption_validation_enabled",
    "transition_risk_validation_enabled",
    "transition_impact_validation_enabled",
    "transition_dependency_validation_enabled",
    "transition_constraint_validation_enabled",
    "transition_reason_validation_enabled",
    "target_phase_validation_enabled",
    "target_phase_selection_enabled",
    "transition_readiness_validation_enabled",
    "live_transition_readiness_validation_enabled",
    "readiness_verdict_enabled",
    "transition_readiness_verdict_enabled",
    "validation_verdict_enabled",
    "transition_validation_verdict_enabled",
    "closure_verdict_enabled",
    "handoff_verdict_enabled",
    "execution_enabled",
    "decision_execution_enabled",
    "transition_execution_enabled",
    "transition_command_execution_enabled",
    "authorization_enabled",
    "transition_authorization_enabled",
    "approval_enabled",
    "transition_approval_enabled",
    "confirmation_enabled",
    "transition_confirmation_enabled",
    "recommendation_enabled",
    "transition_recommendation_enabled",
    "ranking_enabled",
    "transition_ranking_enabled",
    "suggested_next_action_enabled",
    "next_action_generation_enabled",
    "transition_record_creation_enabled",
    "request_record_creation_enabled",
    "package_record_creation_enabled",
    "transition_readiness_record_creation_enabled",
    "transition_validation_record_creation_enabled",
    "transition_approval_record_creation_enabled",
    "transition_authorization_record_creation_enabled",
    "transition_confirmation_record_creation_enabled",
    "transition_execution_record_creation_enabled",
    "transition_recommendation_record_creation_enabled",
    "transition_ranking_record_creation_enabled",
    "transition_next_action_record_creation_enabled",
    "live_request_intake_enabled",
    "request_acceptance_enabled",
    "request_rejection_enabled",
    "request_validation_enabled",
    "request_schema_validation_enabled",
    "request_content_validation_enabled",
    "request_completeness_validation_enabled",
    "request_eligibility_validation_enabled",
    "request_persistence_enabled",
    "request_storage_enabled",
    "request_mutation_enabled",
    "request_record_update_enabled",
    "request_record_deletion_enabled",
    "evidence_validation_enabled",
    "evidence_scoring_enabled",
    "evidence_ranking_enabled",
    "evidence_precedence_enabled",
    "evidence_arbitration_enabled",
    "evidence_winner_selection_enabled",
    "evidence_record_creation_enabled",
    "human_context_validation_enabled",
    "human_context_mutation_enabled",
    "human_context_record_creation_enabled",
    "human_confirmation_enabled",
    "human_approval_enabled",
    "human_authorization_enabled",
    "consent_validation_enabled",
    "identity_verification_enabled",
    "source_validation_enabled",
    "citation_validation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "citation_mutation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "memory_mutation_enabled",
    "memory_record_creation_enabled",
    "memory_record_update_enabled",
    "memory_record_deletion_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "retry_policy_mutation_enabled",
    "evidence_mutation_enabled",
    "roadmap_mutation_enabled",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "codex_hermes_chatgpt_product_code_auto_call_enabled",
    "p4_m4_started",
    "p4_m4_command_enabled",
    "p4_m4_activation_enabled",
    "p4_m4_implementation_enabled",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
    "version_bump_enabled",
    "tag_creation_enabled",
)

EXPECTED_MEMORY_LOOP_COMMANDS = {
    "checklist",
    "review-status",
    "recall-verification-status",
    "lifecycle-verification-status",
    "do-not-retry-verification-status",
    "source-provenance-verification-status",
    "decision-readiness-status",
    "manual-decision-preview",
    "governance-pack-export",
    "final-boundary-audit",
    "manual-execution-hardening",
    "execution-surface-contract",
    "execution-contract-validation-matrix",
    "manual-authorization-evidence-envelope",
    "human-confirmation-snapshot-contract",
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
    "execution-decision-silence-non-consent-map",
    "execution-decision-negative-evidence-non-override-map",
    "execution-decision-conflicting-evidence-isolation-map",
    "execution-decision-evidence-precedence-prohibition-map",
    "final-non-execution-boundary-audit",
    "p4-m2-closure-handoff-contract",
    "governed-transition-intake-boundary-contract",
    "governed-transition-intake-request-envelope-contract",
    "governed-transition-intake-evidence-reference-envelope-contract",
    "governed-transition-intake-declared-human-context-envelope-contract",
    "governed-transition-intake-target-phase-envelope-contract",
    "governed-transition-intake-declared-transition-reason-envelope-contract",
    "governed-transition-intake-declared-transition-constraint-envelope-contract",
    "governed-transition-intake-declared-transition-dependency-envelope-contract",
    "governed-transition-intake-declared-transition-impact-envelope-contract",
    "governed-transition-intake-declared-transition-risk-envelope-contract",
    "governed-transition-intake-declared-transition-assumption-envelope-contract",
    "governed-transition-intake-declared-transition-safeguard-envelope-contract",
    "governed-transition-intake-package-assembly-envelope-contract",
    "governed-transition-intake-final-non-validation-boundary-audit",
    "governed-transition-intake-closure-handoff-contract",
}

PREVIOUS_P4_M3_13_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "governed-transition-intake-closure-handoff-contract"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "validate-transition-intake",
    "validate-package",
    "validate-package-correctness",
    "validate-package-completeness",
    "validate-package-consistency",
    "validate-package-integrity",
    "validate-package-readiness",
    "validate-final-audit",
    "validate-closure",
    "validate-handoff",
    "execute-closure",
    "execute-handoff",
    "package-readiness-verdict",
    "package-validation-verdict",
    "resolve-references",
    "validate-reference-integrity",
    "validate-reference-completeness",
    "validate-transition-safeguard",
    "validate-transition-assumption",
    "validate-transition-risk",
    "validate-transition-impact",
    "validate-transition-dependency",
    "validate-transition-constraint",
    "validate-transition-reason",
    "validate-target-phase",
    "select-target-phase",
    "validate-transition-readiness",
    "readiness-verdict",
    "validation-verdict",
    "closure-verdict",
    "handoff-verdict",
    "certify-boundaries",
    "execute-transition",
    "authorize-transition",
    "approve-transition",
    "confirm-transition",
    "recommend-transition",
    "rank-transition",
    "suggest-next-action",
    "create-transition-record",
    "create-request-record",
    "create-package-record",
    "create-closure-record",
    "create-handoff-record",
    "validate-request",
    "validate-evidence",
    "validate-human-context",
    "fetch-source",
    "write-provenance",
    "mutate-citation",
    "write-memory",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}


def test_closure_handoff_contract_field_order_count_and_ids_are_stable():
    fields = list_governed_transition_intake_closure_handoff_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 19))
    assert len(fields) == 18
    assert governed_transition_intake_closure_handoff_contract_field_ids() == FIELD_IDS


def test_every_closure_handoff_contract_field_has_required_values():
    for field in list_governed_transition_intake_closure_handoff_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m3_closure_handoff_contract_category.strip()
        assert field.p4_m3_closure_handoff_semantics_disabled.strip()


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_governed_transition_intake_closure_handoff_contract_markdown()
    second = render_governed_transition_intake_closure_handoff_contract_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M3.14 Governed Transition Intake Closure Handoff Contract\n"
    )
    assert GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-closure-handoff-contract",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_payload == second_payload
    assert first_payload["boundary"] == GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY
    assert first_payload["count"] == 18
    assert first_payload["status"]["phase"] == "P4-M3.14"
    assert (
        first_payload["status"]["feature"]
        == "Governed Transition Intake Closure Handoff Contract"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == governed_transition_intake_closure_handoff_contract_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert first_payload["status"][flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert first_payload["status"][flag] is False
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = governed_transition_intake_closure_handoff_contract_as_dicts()
    second_fields = governed_transition_intake_closure_handoff_contract_as_dicts()
    first_status = governed_transition_intake_closure_handoff_contract_report()
    second_status = governed_transition_intake_closure_handoff_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M3.14"
    assert (
        first_status["feature"]
        == "Governed Transition Intake Closure Handoff Contract"
    )
    assert first_status["mode"] == "read-only"
    assert first_status["governed_transition_intake_closure_handoff_contract_field_count"] == 18
    assert first_status["boundary"] == GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = governed_transition_intake_closure_handoff_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M3.14 Governed Transition Intake Closure Handoff Contract\n"
    )
    assert "## Status Report" in stdout
    assert GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-closure-handoff-contract",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "markdown",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_payload == {}
    assert second_payload == {}
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_stdout.startswith("# P4-M3.14")
    assert not (tmp_path / ".local").exists()


def test_command_does_not_instantiate_writable_store(monkeypatch, tmp_path):
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("writable store must not be instantiated")

    monkeypatch.setattr(
        "hermes_memory_fabric.p4_m0_subspace_operator.create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    markdown_code, _, markdown_stderr, markdown_stdout = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M3.14")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 18
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "transition_intake_closure_handoff_contract.jsonl",
        "closure_handoff_contract.jsonl",
        "closure_records.jsonl",
        "handoff_records.jsonl",
        "closure_validation.jsonl",
        "handoff_validation.jsonl",
        "closure_execution.jsonl",
        "handoff_execution.jsonl",
        "transition_intake_final_non_validation_boundary_audit.jsonl",
        "final_non_validation_boundary_audit.jsonl",
        "transition_intake_validation.jsonl",
        "transition_intake_package_validation.jsonl",
        "transition_intake_package_records.jsonl",
        "transition_intake_packages.jsonl",
        "package_assembly.jsonl",
        "package_validation.jsonl",
        "reference_resolution.jsonl",
        "reference_validation.jsonl",
        "request_records.jsonl",
        "package_records.jsonl",
        "transition_records.jsonl",
        "transition_readiness_records.jsonl",
        "transition_validation_records.jsonl",
        "transition_approval_records.jsonl",
        "transition_authorization_records.jsonl",
        "transition_confirmation_records.jsonl",
        "transition_execution_records.jsonl",
        "transition_recommendation_records.jsonl",
        "transition_ranking_records.jsonl",
        "transition_next_action_records.jsonl",
        "human_context_records.jsonl",
        "evidence_records.jsonl",
        "execution.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "approvals.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "roadmap.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "governed-transition-intake-closure-handoff-contract" in commands
    assert PREVIOUS_P4_M3_13_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_doc_contains_required_boundaries():
    doc = Path(
        "docs/CIVILIZATION_CORE_P4_M3_14_GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT.md"
    ).read_text()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc
    for field_id in FIELD_IDS:
        assert field_id in doc


def test_package_version_lock_and_no_entry_point():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m3_governed_transition_intake_closure_handoff_contract" not in entry_points
    assert "governed-transition-intake-closure-handoff-contract" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = GovernedTransitionIntakeClosureHandoffContractField(
        field_order=1,
        field_id="custom-governed-transition-intake-closure-handoff-contract",
        field_name="Custom Governed Transition Intake Closure Handoff Contract Field",
        field_purpose="Custom inspection-only purpose.",
        p4_m3_closure_handoff_contract_category=(
            "custom-governed-transition-intake-closure-handoff-contract-category"
        ),
        p4_m3_closure_handoff_semantics_disabled=(
            "Custom governed transition intake closure handoff semantics are disabled."
        ),
    )

    markdown = render_governed_transition_intake_closure_handoff_contract_markdown(
        [field]
    )

    assert "custom-governed-transition-intake-closure-handoff-contract" in markdown
    assert "Custom inspection-only purpose." in markdown


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _memory_loop_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:
        raise AssertionError("memory-loop parser not found")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("memory-loop subcommands not found")
