from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stderr
from dataclasses import asdict
from pathlib import Path
from typing import Any, TextIO

from .p4_m0_subspace_memory import VALID_LIFECYCLE_STATES
from .p4_m1_human_gated_memory_loop_checklist import (
    HUMAN_GATED_MEMORY_LOOP_BOUNDARY,
    human_gated_memory_loop_checklist_as_dicts,
    human_gated_memory_loop_status_report,
    render_human_gated_memory_loop_checklist_markdown,
)
from .p4_m1_human_gated_do_not_retry_verification_status import (
    HUMAN_GATED_DO_NOT_RETRY_VERIFICATION_STATUS_BOUNDARY,
    human_gated_do_not_retry_verification_status_as_dicts,
    human_gated_do_not_retry_verification_status_report,
    render_human_gated_do_not_retry_verification_status_markdown,
)
from .p4_m1_human_gated_lifecycle_verification_status import (
    HUMAN_GATED_LIFECYCLE_VERIFICATION_STATUS_BOUNDARY,
    human_gated_lifecycle_verification_status_as_dicts,
    human_gated_lifecycle_verification_status_report,
    render_human_gated_lifecycle_verification_status_markdown,
)
from .p4_m1_human_gated_proposal_review_status import (
    HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY,
    human_gated_proposal_review_status_as_dicts,
    human_gated_proposal_review_status_report,
    render_human_gated_proposal_review_status_markdown,
)
from .p4_m1_human_gated_recall_verification_status import (
    HUMAN_GATED_RECALL_VERIFICATION_STATUS_BOUNDARY,
    human_gated_recall_verification_status_as_dicts,
    human_gated_recall_verification_status_report,
    render_human_gated_recall_verification_status_markdown,
)
from .p4_m1_decision_readiness_status import (
    DECISION_READINESS_STATUS_BOUNDARY,
    decision_readiness_status_as_dicts,
    decision_readiness_status_report,
    render_decision_readiness_status_markdown,
)
from .p4_m1_manual_decision_preview import (
    MANUAL_DECISION_PREVIEW_BOUNDARY,
    manual_decision_preview_as_dicts,
    manual_decision_preview_report,
    render_manual_decision_preview_markdown,
)
from .p4_m1_governance_pack_export import (
    GOVERNANCE_PACK_EXPORT_BOUNDARY,
    governance_pack_as_dicts,
    governance_pack_export_report,
    render_governance_pack_markdown,
)
from .p4_m1_final_boundary_audit_closure import (
    FINAL_BOUNDARY_AUDIT_BOUNDARY,
    final_boundary_audit_as_dicts,
    final_boundary_audit_report,
    render_final_boundary_audit_markdown,
)
from .p4_m2_manual_decision_execution_hardening import (
    MANUAL_EXECUTION_HARDENING_BOUNDARY,
    manual_execution_hardening_as_dicts,
    manual_execution_hardening_report,
    render_manual_execution_hardening_markdown,
)
from .p4_m2_execution_surface_contract_definition import (
    EXECUTION_SURFACE_CONTRACT_BOUNDARY,
    execution_surface_contract_as_dicts,
    execution_surface_contract_report,
    render_execution_surface_contract_markdown,
)
from .p4_m2_execution_contract_validation_matrix import (
    EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY,
    execution_contract_validation_matrix_as_dicts,
    execution_contract_validation_matrix_report,
    render_execution_contract_validation_matrix_markdown,
)
from .p4_m2_manual_authorization_evidence_envelope import (
    MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY,
    manual_authorization_evidence_envelope_as_dicts,
    manual_authorization_evidence_envelope_report,
    render_manual_authorization_evidence_envelope_markdown,
)
from .p4_m2_human_confirmation_snapshot_contract import (
    HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_BOUNDARY,
    human_confirmation_snapshot_contract_as_dicts,
    human_confirmation_snapshot_contract_report,
    render_human_confirmation_snapshot_contract_markdown,
)
from .p4_m2_execution_preconditions_snapshot_map import (
    EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY,
    execution_preconditions_snapshot_map_as_dicts,
    execution_preconditions_snapshot_map_report,
    render_execution_preconditions_snapshot_map_markdown,
)
from .p4_m2_execution_risk_acknowledgement_map import (
    EXECUTION_RISK_ACKNOWLEDGEMENT_MAP_BOUNDARY,
    execution_risk_acknowledgement_map_as_dicts,
    execution_risk_acknowledgement_map_report,
    render_execution_risk_acknowledgement_map_markdown,
)
from .p4_m2_execution_risk_acceptance_prohibition_map import (
    EXECUTION_RISK_ACCEPTANCE_PROHIBITION_MAP_BOUNDARY,
    execution_risk_acceptance_prohibition_map_as_dicts,
    execution_risk_acceptance_prohibition_map_report,
    render_execution_risk_acceptance_prohibition_map_markdown,
)
from .p4_m2_execution_risk_waiver_prohibition_map import (
    EXECUTION_RISK_WAIVER_PROHIBITION_MAP_BOUNDARY,
    execution_risk_waiver_prohibition_map_as_dicts,
    execution_risk_waiver_prohibition_map_report,
    render_execution_risk_waiver_prohibition_map_markdown,
)
from .p4_m2_execution_decision_non_equivalence_map import (
    EXECUTION_DECISION_NON_EQUIVALENCE_MAP_BOUNDARY,
    execution_decision_non_equivalence_map_as_dicts,
    execution_decision_non_equivalence_map_report,
    render_execution_decision_non_equivalence_map_markdown,
)
from .p4_m2_execution_decision_recommendation_prohibition_map import (
    EXECUTION_DECISION_RECOMMENDATION_PROHIBITION_MAP_BOUNDARY,
    execution_decision_recommendation_prohibition_map_as_dicts,
    execution_decision_recommendation_prohibition_map_report,
    render_execution_decision_recommendation_prohibition_map_markdown,
)
from .p4_m2_execution_decision_default_denial_boundary_map import (
    EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_BOUNDARY,
    execution_decision_default_denial_boundary_map_as_dicts,
    execution_decision_default_denial_boundary_map_report,
    render_execution_decision_default_denial_boundary_map_markdown,
)
from .p4_m2_execution_decision_silence_non_consent_map import (
    EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY,
    execution_decision_silence_non_consent_map_as_dicts,
    execution_decision_silence_non_consent_map_report,
    render_execution_decision_silence_non_consent_map_markdown,
)
from .p4_m2_execution_decision_negative_evidence_non_override_map import (
    EXECUTION_DECISION_NEGATIVE_EVIDENCE_NON_OVERRIDE_MAP_BOUNDARY,
    execution_decision_negative_evidence_non_override_map_as_dicts,
    execution_decision_negative_evidence_non_override_map_report,
    render_execution_decision_negative_evidence_non_override_map_markdown,
)
from .p4_m2_execution_decision_conflicting_evidence_isolation_map import (
    EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_BOUNDARY,
    execution_decision_conflicting_evidence_isolation_map_as_dicts,
    execution_decision_conflicting_evidence_isolation_map_report,
    render_execution_decision_conflicting_evidence_isolation_map_markdown,
)
from .p4_m2_execution_decision_evidence_precedence_prohibition_map import (
    EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY,
    execution_decision_evidence_precedence_prohibition_map_as_dicts,
    execution_decision_evidence_precedence_prohibition_map_report,
    render_execution_decision_evidence_precedence_prohibition_map_markdown,
)
from .p4_m2_final_non_execution_boundary_audit import (
    FINAL_NON_EXECUTION_BOUNDARY_AUDIT_BOUNDARY,
    final_non_execution_boundary_audit_as_dicts,
    final_non_execution_boundary_audit_report,
    render_final_non_execution_boundary_audit_markdown,
)
from .p4_m2_closure_handoff_contract import (
    CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    closure_handoff_contract_as_dicts,
    closure_handoff_contract_report,
    render_closure_handoff_contract_markdown,
)
from .p4_m3_governed_transition_intake_boundary_contract import (
    GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY,
    governed_transition_intake_boundary_contract_as_dicts,
    governed_transition_intake_boundary_contract_report,
    render_governed_transition_intake_boundary_contract_markdown,
)
from .p4_m3_governed_transition_intake_request_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_request_envelope_contract_as_dicts,
    governed_transition_intake_request_envelope_contract_report,
    render_governed_transition_intake_request_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_evidence_reference_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_EVIDENCE_REFERENCE_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_evidence_reference_envelope_contract_as_dicts,
    governed_transition_intake_evidence_reference_envelope_contract_report,
    render_governed_transition_intake_evidence_reference_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_human_context_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_human_context_envelope_contract_as_dicts,
    governed_transition_intake_declared_human_context_envelope_contract_report,
    render_governed_transition_intake_declared_human_context_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_target_phase_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_target_phase_envelope_contract_as_dicts,
    governed_transition_intake_target_phase_envelope_contract_report,
    render_governed_transition_intake_target_phase_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_reason_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_reason_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_reason_envelope_contract_report,
    render_governed_transition_intake_declared_transition_reason_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_constraint_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_constraint_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_constraint_envelope_contract_report,
    render_governed_transition_intake_declared_transition_constraint_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_dependency_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_dependency_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_dependency_envelope_contract_report,
    render_governed_transition_intake_declared_transition_dependency_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_impact_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_impact_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_impact_envelope_contract_report,
    render_governed_transition_intake_declared_transition_impact_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_risk_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_RISK_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_risk_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_risk_envelope_contract_report,
    render_governed_transition_intake_declared_transition_risk_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_assumption_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_assumption_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_assumption_envelope_contract_report,
    render_governed_transition_intake_declared_transition_assumption_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_declared_transition_safeguard_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_SAFEGUARD_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_declared_transition_safeguard_envelope_contract_as_dicts,
    governed_transition_intake_declared_transition_safeguard_envelope_contract_report,
    render_governed_transition_intake_declared_transition_safeguard_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_package_assembly_envelope_contract import (
    GOVERNED_TRANSITION_INTAKE_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY,
    governed_transition_intake_package_assembly_envelope_contract_as_dicts,
    governed_transition_intake_package_assembly_envelope_contract_report,
    render_governed_transition_intake_package_assembly_envelope_contract_markdown,
)
from .p4_m3_governed_transition_intake_final_non_validation_boundary_audit import (
    GOVERNED_TRANSITION_INTAKE_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY,
    governed_transition_intake_final_non_validation_boundary_audit_as_dicts,
    governed_transition_intake_final_non_validation_boundary_audit_report,
    render_governed_transition_intake_final_non_validation_boundary_audit_markdown,
)
from .p4_m3_governed_transition_intake_closure_handoff_contract import (
    GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    governed_transition_intake_closure_handoff_contract_as_dicts,
    governed_transition_intake_closure_handoff_contract_report,
    render_governed_transition_intake_closure_handoff_contract_markdown,
)
from .p4_m3_governed_transition_intake_phase_closure_review import (
    GOVERNED_TRANSITION_INTAKE_PHASE_CLOSURE_REVIEW_BOUNDARY,
    governed_transition_intake_phase_closure_review_as_dicts,
    governed_transition_intake_phase_closure_review_report,
    render_governed_transition_intake_phase_closure_review_markdown,
)
from .p4_m3_governed_transition_intake_final_phase_handoff_summary import (
    GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY,
    governed_transition_intake_final_phase_handoff_summary_as_dicts,
    governed_transition_intake_final_phase_handoff_summary_report,
    render_governed_transition_intake_final_phase_handoff_summary_markdown,
)
from .p4_m4_entry_gate_design_boundary_contract import (
    ENTRY_GATE_DESIGN_BOUNDARY_CONTRACT_BOUNDARY,
    entry_gate_design_boundary_contract_as_dicts,
    entry_gate_design_boundary_contract_report,
    render_entry_gate_design_boundary_contract_markdown,
)
from .p4_m4_entry_gate_design_request_envelope_contract import (
    ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
    entry_gate_design_request_envelope_contract_as_dicts,
    entry_gate_design_request_envelope_contract_report,
    render_entry_gate_design_request_envelope_contract_markdown,
)
from .p4_m4_evidence_reference_envelope_contract import (
    EVIDENCE_REFERENCE_ENVELOPE_CONTRACT_BOUNDARY,
    evidence_reference_envelope_contract_as_dicts,
    evidence_reference_envelope_contract_report,
    render_evidence_reference_envelope_contract_markdown,
)
from .p4_m4_declared_human_context_envelope_contract import (
    DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY,
    declared_human_context_envelope_contract_as_dicts,
    declared_human_context_envelope_contract_report,
    render_declared_human_context_envelope_contract_markdown,
)
from .p4_m4_target_phase_envelope_contract import (
    TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
    render_target_phase_envelope_contract_markdown,
    target_phase_envelope_contract_as_dicts,
    target_phase_envelope_contract_report,
)
from .p4_m4_declared_transition_reason_envelope_contract import (
    DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_reason_envelope_contract_as_dicts,
    declared_transition_reason_envelope_contract_report,
    render_declared_transition_reason_envelope_contract_markdown,
)
from .p4_m4_declared_transition_constraint_envelope_contract import (
    DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_constraint_envelope_contract_as_dicts,
    declared_transition_constraint_envelope_contract_report,
    render_declared_transition_constraint_envelope_contract_markdown,
)
from .p4_m4_declared_transition_dependency_envelope_contract import (
    DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_dependency_envelope_contract_as_dicts,
    declared_transition_dependency_envelope_contract_report,
    render_declared_transition_dependency_envelope_contract_markdown,
)
from .p4_m4_declared_transition_impact_envelope_contract import (
    DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_impact_envelope_contract_as_dicts,
    declared_transition_impact_envelope_contract_report,
    render_declared_transition_impact_envelope_contract_markdown,
)
from .p4_m4_declared_transition_risk_envelope_contract import (
    DECLARED_TRANSITION_RISK_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_risk_envelope_contract_as_dicts,
    declared_transition_risk_envelope_contract_report,
    render_declared_transition_risk_envelope_contract_markdown,
)
from .p4_m4_declared_transition_assumption_envelope_contract import (
    DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_assumption_envelope_contract_as_dicts,
    declared_transition_assumption_envelope_contract_report,
    render_declared_transition_assumption_envelope_contract_markdown,
)
from .p4_m4_declared_transition_safeguard_envelope_contract import (
    DECLARED_TRANSITION_SAFEGUARD_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_safeguard_envelope_contract_as_dicts,
    declared_transition_safeguard_envelope_contract_report,
    render_declared_transition_safeguard_envelope_contract_markdown,
)
from .p4_m4_declared_transition_package_assembly_envelope_contract import (
    DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY,
    declared_transition_package_assembly_envelope_contract_as_dicts,
    declared_transition_package_assembly_envelope_contract_report,
    render_declared_transition_package_assembly_envelope_contract_markdown,
)
from .p4_m4_entry_gate_design_final_non_validation_boundary_audit import (
    ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY,
    entry_gate_design_final_non_validation_boundary_audit_as_dicts,
    entry_gate_design_final_non_validation_boundary_audit_report,
    render_entry_gate_design_final_non_validation_boundary_audit_markdown,
)
from .p4_m4_entry_gate_design_closure_handoff_contract import (
    ENTRY_GATE_DESIGN_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    entry_gate_design_closure_handoff_contract_as_dicts,
    entry_gate_design_closure_handoff_contract_report,
    render_entry_gate_design_closure_handoff_contract_markdown,
)
from .p4_m4_entry_gate_design_phase_closure_review import (
    ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY,
    entry_gate_design_phase_closure_review_as_dicts,
    entry_gate_design_phase_closure_review_report,
    render_entry_gate_design_phase_closure_review_markdown,
)
from .p4_m4_entry_gate_design_final_phase_handoff_summary import (
    ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY,
    entry_gate_design_final_phase_handoff_summary_as_dicts,
    entry_gate_design_final_phase_handoff_summary_report,
    render_entry_gate_design_final_phase_handoff_summary_markdown,
)
from .p4_m4_entry_gate_design_phase_terminal_closure_seal import (
    ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL_BOUNDARY,
    entry_gate_design_phase_terminal_closure_seal_as_dicts,
    entry_gate_design_phase_terminal_closure_seal_report,
    render_entry_gate_design_phase_terminal_closure_seal_markdown,
)
from .p4_m4_final_closure_index_entry_planning_gate import (
    P4_M4_FINAL_CLOSURE_INDEX_ENTRY_PLANNING_GATE_BOUNDARY,
    p4_m4_final_closure_index_entry_planning_gate_as_dicts,
    p4_m4_final_closure_index_entry_planning_gate_report,
    render_p4_m4_final_closure_index_entry_planning_gate_markdown,
)
from .p4_m4_final_closure_evidence_index import (
    P4_M4_FINAL_CLOSURE_EVIDENCE_INDEX_BOUNDARY,
    p4_m4_final_closure_evidence_index_as_dicts,
    p4_m4_final_closure_evidence_index_report,
    render_p4_m4_final_closure_evidence_index_markdown,
)
from .p4_m4_final_closure_operator_handoff_index import (
    P4_M4_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX_BOUNDARY,
    p4_m4_final_closure_operator_handoff_index_as_dicts,
    p4_m4_final_closure_operator_handoff_index_report,
    render_p4_m4_final_closure_operator_handoff_index_markdown,
)
from .p4_m4_final_closure_transition_readiness_non_start_index import (
    P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_BOUNDARY,
    p4_m4_final_closure_transition_readiness_non_start_index_as_dicts,
    p4_m4_final_closure_transition_readiness_non_start_index_report,
    render_p4_m4_final_closure_transition_readiness_non_start_index_markdown,
)
from .p4_m4_final_closure_non_start_bridge_index import (
    P4_M4_FINAL_CLOSURE_NON_START_BRIDGE_INDEX_BOUNDARY,
    p4_m4_final_closure_non_start_bridge_index_as_dicts,
    p4_m4_final_closure_non_start_bridge_index_report,
    render_p4_m4_final_closure_non_start_bridge_index_markdown,
)
from .p4_m4_final_closure_boundary_freeze_index import (
    P4_M4_FINAL_CLOSURE_BOUNDARY_FREEZE_INDEX_BOUNDARY,
    p4_m4_final_closure_boundary_freeze_index_as_dicts,
    p4_m4_final_closure_boundary_freeze_index_report,
    render_p4_m4_final_closure_boundary_freeze_index_markdown,
)
from .p4_m4_final_closure_roadmap_alignment_snapshot import (
    P4_M4_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT_BOUNDARY,
    p4_m4_final_closure_roadmap_alignment_snapshot_as_dicts,
    p4_m4_final_closure_roadmap_alignment_snapshot_report,
    render_p4_m4_final_closure_roadmap_alignment_snapshot_markdown,
)
from .p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract import (
    P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT_BOUNDARY,
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_as_dicts,
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_report,
    render_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_markdown,
)
from .p4_m5_1_api_readiness_audit_surface_map import (
    P4_M5_1_API_READINESS_AUDIT_SURFACE_MAP_BOUNDARY,
    p4_m5_1_api_readiness_audit_surface_map_as_dicts,
    p4_m5_1_api_readiness_audit_surface_map_report,
    render_p4_m5_1_api_readiness_audit_surface_map_markdown,
)
from .p4_m5_2_mcp_readiness_audit_surface_map import (
    P4_M5_2_MCP_READINESS_AUDIT_SURFACE_MAP_BOUNDARY,
    p4_m5_2_mcp_readiness_audit_surface_map_as_dicts,
    p4_m5_2_mcp_readiness_audit_surface_map_report,
    render_p4_m5_2_mcp_readiness_audit_surface_map_markdown,
)
from .p4_m5_3_connector_readiness_audit_surface_map import (
    P4_M5_3_CONNECTOR_READINESS_AUDIT_SURFACE_MAP_BOUNDARY,
    p4_m5_3_connector_readiness_audit_surface_map_as_dicts,
    p4_m5_3_connector_readiness_audit_surface_map_report,
    render_p4_m5_3_connector_readiness_audit_surface_map_markdown,
)
from .p4_m5_4_cross_surface_alignment_map import (
    FALSE_STATUS_FLAGS as P4_M5_4_FALSE_STATUS_FLAGS,
    P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M5_4_TRUE_STATUS_FLAGS,
    p4_m5_4_cross_surface_alignment_map_as_dicts,
    p4_m5_4_cross_surface_alignment_map_report,
    render_p4_m5_4_cross_surface_alignment_map_markdown,
)
from .p4_m5_5_readiness_audit_closure_non_start_boundary_seal import (
    FALSE_STATUS_FLAGS as P4_M5_5_FALSE_STATUS_FLAGS,
    P4_M5_5_READINESS_AUDIT_CLOSURE_NON_START_BOUNDARY_SEAL_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M5_5_TRUE_STATUS_FLAGS,
    p4_m5_5_readiness_audit_closure_non_start_boundary_seal_as_dicts,
    p4_m5_5_readiness_audit_closure_non_start_boundary_seal_report,
    render_p4_m5_5_readiness_audit_closure_non_start_boundary_seal_markdown,
)
from .p4_m5_6_final_closure_handoff_next_corridor_non_start_index import (
    FALSE_STATUS_FLAGS as P4_M5_6_FALSE_STATUS_FLAGS,
    P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M5_6_TRUE_STATUS_FLAGS,
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_as_dicts,
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_report,
    render_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_markdown,
)
from .p4_m6_0_next_corridor_entry_boundary_contract import (
    FALSE_STATUS_FLAGS as P4_M6_0_FALSE_STATUS_FLAGS,
    P4_M6_0_NEXT_CORRIDOR_ENTRY_BOUNDARY_CONTRACT_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_0_TRUE_STATUS_FLAGS,
    p4_m6_0_next_corridor_entry_boundary_contract_as_dicts,
    p4_m6_0_next_corridor_entry_boundary_contract_report,
    render_p4_m6_0_next_corridor_entry_boundary_contract_markdown,
)
from .p4_m6_1_entry_preconditions_definition_surface import (
    FALSE_STATUS_FLAGS as P4_M6_1_FALSE_STATUS_FLAGS,
    P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_1_TRUE_STATUS_FLAGS,
    p4_m6_1_entry_preconditions_definition_surface_as_dicts,
    p4_m6_1_entry_preconditions_definition_surface_report,
    render_p4_m6_1_entry_preconditions_definition_surface_markdown,
)
from .p4_m6_2_entry_acceptance_non_evidence_surface import (
    FALSE_STATUS_FLAGS as P4_M6_2_FALSE_STATUS_FLAGS,
    P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_2_TRUE_STATUS_FLAGS,
    p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts,
    p4_m6_2_entry_acceptance_non_evidence_surface_report,
    render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown,
)
from .p4_m6_3_entry_deferral_non_execution_surface import (
    FALSE_STATUS_FLAGS as P4_M6_3_FALSE_STATUS_FLAGS,
    P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_3_TRUE_STATUS_FLAGS,
    p4_m6_3_entry_deferral_non_execution_surface_as_dicts,
    p4_m6_3_entry_deferral_non_execution_surface_report,
    render_p4_m6_3_entry_deferral_non_execution_surface_markdown,
)
from .p4_m6_4_entry_rejection_non_execution_surface import (
    FALSE_STATUS_FLAGS as P4_M6_4_FALSE_STATUS_FLAGS,
    P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_4_TRUE_STATUS_FLAGS,
    p4_m6_4_entry_rejection_non_execution_surface_as_dicts,
    p4_m6_4_entry_rejection_non_execution_surface_report,
    render_p4_m6_4_entry_rejection_non_execution_surface_markdown,
)
from .p4_m6_5_entry_escalation_non_routing_surface import (
    FALSE_STATUS_FLAGS as P4_M6_5_FALSE_STATUS_FLAGS,
    P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_5_TRUE_STATUS_FLAGS,
    p4_m6_5_entry_escalation_non_routing_surface_as_dicts,
    p4_m6_5_entry_escalation_non_routing_surface_report,
    render_p4_m6_5_entry_escalation_non_routing_surface_markdown,
)
from .p4_m6_6_entry_exception_non_override_surface import (
    FALSE_STATUS_FLAGS as P4_M6_6_FALSE_STATUS_FLAGS,
    P4_M6_6_ENTRY_EXCEPTION_NON_OVERRIDE_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_6_TRUE_STATUS_FLAGS,
    p4_m6_6_entry_exception_non_override_surface_as_dicts,
    p4_m6_6_entry_exception_non_override_surface_report,
    render_p4_m6_6_entry_exception_non_override_surface_markdown,
)
from .p4_m6_7_entry_conflict_non_resolution_surface import (
    FALSE_STATUS_FLAGS as P4_M6_7_FALSE_STATUS_FLAGS,
    P4_M6_7_ENTRY_CONFLICT_NON_RESOLUTION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_7_TRUE_STATUS_FLAGS,
    p4_m6_7_entry_conflict_non_resolution_surface_as_dicts,
    p4_m6_7_entry_conflict_non_resolution_surface_report,
    render_p4_m6_7_entry_conflict_non_resolution_surface_markdown,
)
from .p4_m6_8_entry_ambiguity_non_inference_surface import (
    FALSE_STATUS_FLAGS as P4_M6_8_FALSE_STATUS_FLAGS,
    P4_M6_8_ENTRY_AMBIGUITY_NON_INFERENCE_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_8_TRUE_STATUS_FLAGS,
    p4_m6_8_entry_ambiguity_non_inference_surface_as_dicts,
    p4_m6_8_entry_ambiguity_non_inference_surface_report,
    render_p4_m6_8_entry_ambiguity_non_inference_surface_markdown,
)
from .p4_m6_9_entry_dependency_non_activation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_9_FALSE_STATUS_FLAGS,
    P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_9_TRUE_STATUS_FLAGS,
    p4_m6_9_entry_dependency_non_activation_surface_as_dicts,
    p4_m6_9_entry_dependency_non_activation_surface_report,
    render_p4_m6_9_entry_dependency_non_activation_surface_markdown,
)
from .p4_m6_10_entry_constraint_non_enforcement_surface import (
    FALSE_STATUS_FLAGS as P4_M6_10_FALSE_STATUS_FLAGS,
    P4_M6_10_ENTRY_CONSTRAINT_NON_ENFORCEMENT_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_10_TRUE_STATUS_FLAGS,
    p4_m6_10_entry_constraint_non_enforcement_surface_as_dicts,
    p4_m6_10_entry_constraint_non_enforcement_surface_report,
    render_p4_m6_10_entry_constraint_non_enforcement_surface_markdown,
)
from .p4_m6_11_entry_risk_non_mitigation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_11_FALSE_STATUS_FLAGS,
    P4_M6_11_ENTRY_RISK_NON_MITIGATION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_11_TRUE_STATUS_FLAGS,
    p4_m6_11_entry_risk_non_mitigation_surface_as_dicts,
    p4_m6_11_entry_risk_non_mitigation_surface_report,
    render_p4_m6_11_entry_risk_non_mitigation_surface_markdown,
)
from .p4_m6_12_entry_safeguard_non_activation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_12_FALSE_STATUS_FLAGS,
    P4_M6_12_ENTRY_SAFEGUARD_NON_ACTIVATION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_12_TRUE_STATUS_FLAGS,
    p4_m6_12_entry_safeguard_non_activation_surface_as_dicts,
    p4_m6_12_entry_safeguard_non_activation_surface_report,
    render_p4_m6_12_entry_safeguard_non_activation_surface_markdown,
)
from .p4_m6_13_entry_definition_corridor_closure_review import (
    FALSE_STATUS_FLAGS as P4_M6_13_FALSE_STATUS_FLAGS,
    P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_13_TRUE_STATUS_FLAGS,
    p4_m6_13_entry_definition_corridor_closure_review_as_dicts,
    p4_m6_13_entry_definition_corridor_closure_review_report,
    render_p4_m6_13_entry_definition_corridor_closure_review_markdown,
)
from .p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index import (
    FALSE_STATUS_FLAGS as P4_M6_14_FALSE_STATUS_FLAGS,
    P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY,
    TRUE_STATUS_FLAGS as P4_M6_14_TRUE_STATUS_FLAGS,
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_as_dicts,
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report,
    render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown,
)
from .p4_m1_source_provenance_verification_status import (
    SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY,
    render_source_provenance_verification_status_markdown,
    source_provenance_verification_status_as_dicts,
    source_provenance_verification_status_report,
)
from .p4_m0_subspace_project_seed import (
    get_project_memory_seed,
    list_project_memory_seeds,
    render_project_memory_seed_pack,
)
from .p4_m0_subspace_seed_approval_runbook import (
    SEED_APPROVAL_RUNBOOK_BOUNDARY,
    render_seed_approval_runbook_markdown,
    seed_approval_runbook_as_dicts,
)
from .p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="p4-m0-subspace-operator",
        description="Manual local operator commands for the P4-M0 Subspace Memory store.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose = subparsers.add_parser("propose")
    _add_workspace_root(propose)
    propose.add_argument("--project", required=True)
    propose.add_argument("--namespace", required=True)
    propose.add_argument("--content", required=True)
    propose.add_argument("--source", default="local")
    propose.add_argument("--tag", action="append", default=[])
    propose.add_argument("--confidence", type=float, default=1.0)

    approve = subparsers.add_parser("approve")
    _add_workspace_root(approve)
    approve.add_argument("--proposal-id", required=True)
    approve.add_argument("--approver", required=True)
    approve.add_argument("--note")

    reject = subparsers.add_parser("reject")
    _add_workspace_root(reject)
    reject.add_argument("--proposal-id", required=True)
    reject.add_argument("--reviewer", required=True)
    reject.add_argument("--reason", required=True)

    recall = subparsers.add_parser("recall")
    _add_workspace_root(recall)
    recall.add_argument("--query", required=True)
    recall.add_argument("--project")
    recall.add_argument("--namespace")
    recall.add_argument("--limit", type=int, default=10)
    recall.add_argument("--include-stale", action="store_true")
    recall.add_argument("--include-archived", action="store_true")

    lifecycle = subparsers.add_parser("lifecycle")
    _add_workspace_root(lifecycle)
    lifecycle.add_argument("--memory-id", required=True)
    lifecycle.add_argument("--state", choices=VALID_LIFECYCLE_STATES, required=True)
    lifecycle.add_argument("--actor", required=True)
    lifecycle.add_argument("--reason")

    do_not_retry = subparsers.add_parser("do-not-retry")
    do_not_retry_subparsers = do_not_retry.add_subparsers(dest="do_not_retry_command", required=True)

    do_not_retry_set = do_not_retry_subparsers.add_parser("set")
    _add_workspace_root(do_not_retry_set)
    do_not_retry_set.add_argument("--memory-id", required=True)
    do_not_retry_set.add_argument("--reason", required=True)
    do_not_retry_set.add_argument("--actor", required=True)
    do_not_retry_set.add_argument("--alternative")

    do_not_retry_clear = do_not_retry_subparsers.add_parser("clear")
    _add_workspace_root(do_not_retry_clear)
    do_not_retry_clear.add_argument("--memory-id", required=True)
    do_not_retry_clear.add_argument("--actor", required=True)
    do_not_retry_clear.add_argument("--reason")

    project_seed = subparsers.add_parser("project-seed")
    project_seed_subparsers = project_seed.add_subparsers(dest="project_seed_command", required=True)

    project_seed_list = project_seed_subparsers.add_parser("list")
    _add_workspace_root(project_seed_list)

    project_seed_show = project_seed_subparsers.add_parser("show")
    _add_workspace_root(project_seed_show)
    project_seed_show.add_argument("--seed-id", required=True)

    project_seed_pack = project_seed_subparsers.add_parser("pack")
    _add_workspace_root(project_seed_pack)

    project_seed_approval_runbook = project_seed_subparsers.add_parser("approval-runbook")
    _add_workspace_root(project_seed_approval_runbook)
    project_seed_approval_runbook.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    project_seed_propose = project_seed_subparsers.add_parser("propose")
    _add_workspace_root(project_seed_propose)
    project_seed_propose.add_argument("--seed-id", required=True)
    project_seed_propose.add_argument("--actor", required=True)

    memory_loop = subparsers.add_parser("memory-loop")
    memory_loop_subparsers = memory_loop.add_subparsers(dest="memory_loop_command", required=True)

    memory_loop_checklist = memory_loop_subparsers.add_parser("checklist")
    _add_workspace_root(memory_loop_checklist)
    memory_loop_checklist.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_review_status = memory_loop_subparsers.add_parser("review-status")
    _add_workspace_root(memory_loop_review_status)
    memory_loop_review_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_recall_verification_status = memory_loop_subparsers.add_parser(
        "recall-verification-status"
    )
    _add_workspace_root(memory_loop_recall_verification_status)
    memory_loop_recall_verification_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_lifecycle_verification_status = memory_loop_subparsers.add_parser(
        "lifecycle-verification-status"
    )
    _add_workspace_root(memory_loop_lifecycle_verification_status)
    memory_loop_lifecycle_verification_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_do_not_retry_verification_status = memory_loop_subparsers.add_parser(
        "do-not-retry-verification-status"
    )
    _add_workspace_root(memory_loop_do_not_retry_verification_status)
    memory_loop_do_not_retry_verification_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_source_provenance_verification_status = memory_loop_subparsers.add_parser(
        "source-provenance-verification-status"
    )
    _add_workspace_root(memory_loop_source_provenance_verification_status)
    memory_loop_source_provenance_verification_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_decision_readiness_status = memory_loop_subparsers.add_parser(
        "decision-readiness-status"
    )
    _add_workspace_root(memory_loop_decision_readiness_status)
    memory_loop_decision_readiness_status.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_manual_decision_preview = memory_loop_subparsers.add_parser(
        "manual-decision-preview"
    )
    _add_workspace_root(memory_loop_manual_decision_preview)
    memory_loop_manual_decision_preview.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governance_pack_export = memory_loop_subparsers.add_parser(
        "governance-pack-export"
    )
    _add_workspace_root(memory_loop_governance_pack_export)
    memory_loop_governance_pack_export.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_final_boundary_audit = memory_loop_subparsers.add_parser(
        "final-boundary-audit"
    )
    _add_workspace_root(memory_loop_final_boundary_audit)
    memory_loop_final_boundary_audit.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_manual_execution_hardening = memory_loop_subparsers.add_parser(
        "manual-execution-hardening"
    )
    _add_workspace_root(memory_loop_manual_execution_hardening)
    memory_loop_manual_execution_hardening.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_surface_contract = memory_loop_subparsers.add_parser(
        "execution-surface-contract"
    )
    _add_workspace_root(memory_loop_execution_surface_contract)
    memory_loop_execution_surface_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_contract_validation_matrix = memory_loop_subparsers.add_parser(
        "execution-contract-validation-matrix"
    )
    _add_workspace_root(memory_loop_execution_contract_validation_matrix)
    memory_loop_execution_contract_validation_matrix.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_manual_authorization_evidence_envelope = memory_loop_subparsers.add_parser(
        "manual-authorization-evidence-envelope"
    )
    _add_workspace_root(memory_loop_manual_authorization_evidence_envelope)
    memory_loop_manual_authorization_evidence_envelope.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_human_confirmation_snapshot_contract = memory_loop_subparsers.add_parser(
        "human-confirmation-snapshot-contract"
    )
    _add_workspace_root(memory_loop_human_confirmation_snapshot_contract)
    memory_loop_human_confirmation_snapshot_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_preconditions_snapshot_map = memory_loop_subparsers.add_parser(
        "execution-preconditions-snapshot-map"
    )
    _add_workspace_root(memory_loop_execution_preconditions_snapshot_map)
    memory_loop_execution_preconditions_snapshot_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_risk_acknowledgement_map = memory_loop_subparsers.add_parser(
        "execution-risk-acknowledgement-map"
    )
    _add_workspace_root(memory_loop_execution_risk_acknowledgement_map)
    memory_loop_execution_risk_acknowledgement_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_risk_acceptance_prohibition_map = memory_loop_subparsers.add_parser(
        "execution-risk-acceptance-prohibition-map"
    )
    _add_workspace_root(memory_loop_execution_risk_acceptance_prohibition_map)
    memory_loop_execution_risk_acceptance_prohibition_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_risk_waiver_prohibition_map = memory_loop_subparsers.add_parser(
        "execution-risk-waiver-prohibition-map"
    )
    _add_workspace_root(memory_loop_execution_risk_waiver_prohibition_map)
    memory_loop_execution_risk_waiver_prohibition_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_non_equivalence_map = memory_loop_subparsers.add_parser(
        "execution-decision-non-equivalence-map"
    )
    _add_workspace_root(memory_loop_execution_decision_non_equivalence_map)
    memory_loop_execution_decision_non_equivalence_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_recommendation_prohibition_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-recommendation-prohibition-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_recommendation_prohibition_map)
    memory_loop_execution_decision_recommendation_prohibition_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_default_denial_boundary_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-default-denial-boundary-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_default_denial_boundary_map)
    memory_loop_execution_decision_default_denial_boundary_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_silence_non_consent_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-silence-non-consent-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_silence_non_consent_map)
    memory_loop_execution_decision_silence_non_consent_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_negative_evidence_non_override_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-negative-evidence-non-override-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_negative_evidence_non_override_map)
    memory_loop_execution_decision_negative_evidence_non_override_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_conflicting_evidence_isolation_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-conflicting-evidence-isolation-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_conflicting_evidence_isolation_map)
    memory_loop_execution_decision_conflicting_evidence_isolation_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_execution_decision_evidence_precedence_prohibition_map = (
        memory_loop_subparsers.add_parser(
            "execution-decision-evidence-precedence-prohibition-map"
        )
    )
    _add_workspace_root(memory_loop_execution_decision_evidence_precedence_prohibition_map)
    memory_loop_execution_decision_evidence_precedence_prohibition_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_final_non_execution_boundary_audit = memory_loop_subparsers.add_parser(
        "final-non-execution-boundary-audit"
    )
    _add_workspace_root(memory_loop_final_non_execution_boundary_audit)
    memory_loop_final_non_execution_boundary_audit.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_closure_handoff_contract = memory_loop_subparsers.add_parser(
        "p4-m2-closure-handoff-contract"
    )
    _add_workspace_root(memory_loop_closure_handoff_contract)
    memory_loop_closure_handoff_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_boundary_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-boundary-contract"
        )
    )
    _add_workspace_root(memory_loop_governed_transition_intake_boundary_contract)
    memory_loop_governed_transition_intake_boundary_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_request_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-request-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_governed_transition_intake_request_envelope_contract)
    memory_loop_governed_transition_intake_request_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_evidence_reference_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-evidence-reference-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_governed_transition_intake_evidence_reference_envelope_contract)
    memory_loop_governed_transition_intake_evidence_reference_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_human_context_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-human-context-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_human_context_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_human_context_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_target_phase_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-target-phase-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_target_phase_envelope_contract
    )
    memory_loop_governed_transition_intake_target_phase_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_reason_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-reason-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_reason_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_reason_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_constraint_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-constraint-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_constraint_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_constraint_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_dependency_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-dependency-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_dependency_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_dependency_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_impact_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-impact-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_impact_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_impact_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_risk_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-risk-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_risk_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_risk_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_assumption_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-assumption-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_assumption_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_assumption_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_declared_transition_safeguard_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-declared-transition-safeguard-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_declared_transition_safeguard_envelope_contract
    )
    memory_loop_governed_transition_intake_declared_transition_safeguard_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_package_assembly_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-package-assembly-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_package_assembly_envelope_contract
    )
    memory_loop_governed_transition_intake_package_assembly_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_final_non_validation_boundary_audit = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-final-non-validation-boundary-audit"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_final_non_validation_boundary_audit
    )
    memory_loop_governed_transition_intake_final_non_validation_boundary_audit.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_closure_handoff_contract = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-closure-handoff-contract"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_closure_handoff_contract
    )
    memory_loop_governed_transition_intake_closure_handoff_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_phase_closure_review = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-phase-closure-review"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_phase_closure_review
    )
    memory_loop_governed_transition_intake_phase_closure_review.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_governed_transition_intake_final_phase_handoff_summary = (
        memory_loop_subparsers.add_parser(
            "governed-transition-intake-final-phase-handoff-summary"
        )
    )
    _add_workspace_root(
        memory_loop_governed_transition_intake_final_phase_handoff_summary
    )
    memory_loop_governed_transition_intake_final_phase_handoff_summary.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_boundary_contract = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-boundary-contract"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_boundary_contract)
    memory_loop_entry_gate_design_boundary_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_request_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-request-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_request_envelope_contract)
    memory_loop_entry_gate_design_request_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_evidence_reference_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "evidence-reference-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_evidence_reference_envelope_contract)
    memory_loop_evidence_reference_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_human_context_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-human-context-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_human_context_envelope_contract)
    memory_loop_declared_human_context_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_target_phase_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "target-phase-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_target_phase_envelope_contract)
    memory_loop_target_phase_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_reason_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-reason-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_reason_envelope_contract)
    memory_loop_declared_transition_reason_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_constraint_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-constraint-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_constraint_envelope_contract)
    memory_loop_declared_transition_constraint_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_dependency_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-dependency-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_dependency_envelope_contract)
    memory_loop_declared_transition_dependency_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_impact_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-impact-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_impact_envelope_contract)
    memory_loop_declared_transition_impact_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_risk_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-risk-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_risk_envelope_contract)
    memory_loop_declared_transition_risk_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_assumption_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-assumption-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_assumption_envelope_contract)
    memory_loop_declared_transition_assumption_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_safeguard_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-safeguard-envelope-contract"
        )
    )
    _add_workspace_root(memory_loop_declared_transition_safeguard_envelope_contract)
    memory_loop_declared_transition_safeguard_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_declared_transition_package_assembly_envelope_contract = (
        memory_loop_subparsers.add_parser(
            "declared-transition-package-assembly-envelope-contract"
        )
    )
    _add_workspace_root(
        memory_loop_declared_transition_package_assembly_envelope_contract
    )
    memory_loop_declared_transition_package_assembly_envelope_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_final_non_validation_boundary_audit = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-final-non-validation-boundary-audit"
        )
    )
    _add_workspace_root(
        memory_loop_entry_gate_design_final_non_validation_boundary_audit
    )
    memory_loop_entry_gate_design_final_non_validation_boundary_audit.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_closure_handoff_contract = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-closure-handoff-contract"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_closure_handoff_contract)
    memory_loop_entry_gate_design_closure_handoff_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_phase_closure_review = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-phase-closure-review"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_phase_closure_review)
    memory_loop_entry_gate_design_phase_closure_review.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    memory_loop_entry_gate_design_final_phase_handoff_summary = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-final-phase-handoff-summary"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_final_phase_handoff_summary)
    memory_loop_entry_gate_design_final_phase_handoff_summary.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_entry_gate_design_phase_terminal_closure_seal = (
        memory_loop_subparsers.add_parser(
            "entry-gate-design-phase-terminal-closure-seal"
        )
    )
    _add_workspace_root(memory_loop_entry_gate_design_phase_terminal_closure_seal)
    memory_loop_entry_gate_design_phase_terminal_closure_seal.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_index_entry_planning_gate = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-index-entry-planning-gate"
        )
    )
    _add_workspace_root(memory_loop_p4_m4_final_closure_index_entry_planning_gate)
    memory_loop_p4_m4_final_closure_index_entry_planning_gate.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_evidence_index = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-evidence-index"
        )
    )
    _add_workspace_root(memory_loop_p4_m4_final_closure_evidence_index)
    memory_loop_p4_m4_final_closure_evidence_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_operator_handoff_index = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-operator-handoff-index"
        )
    )
    _add_workspace_root(memory_loop_p4_m4_final_closure_operator_handoff_index)
    memory_loop_p4_m4_final_closure_operator_handoff_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_transition_readiness_non_start_index = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-transition-readiness-non-start-index"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m4_final_closure_transition_readiness_non_start_index
    )
    memory_loop_p4_m4_final_closure_transition_readiness_non_start_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_non_start_bridge_index = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-non-start-bridge-index"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m4_final_closure_non_start_bridge_index
    )
    memory_loop_p4_m4_final_closure_non_start_bridge_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_boundary_freeze_index = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-boundary-freeze-index"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m4_final_closure_boundary_freeze_index
    )
    memory_loop_p4_m4_final_closure_boundary_freeze_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m4_final_closure_roadmap_alignment_snapshot = (
        memory_loop_subparsers.add_parser(
            "p4-m4-final-closure-roadmap-alignment-snapshot"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m4_final_closure_roadmap_alignment_snapshot
    )
    memory_loop_p4_m4_final_closure_roadmap_alignment_snapshot.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract = (
        memory_loop_subparsers.add_parser(
            "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract
    )
    memory_loop_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_1_api_readiness_audit_surface_map = (
        memory_loop_subparsers.add_parser(
            "p4-m5-1-api-readiness-audit-surface-map"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_1_api_readiness_audit_surface_map
    )
    memory_loop_p4_m5_1_api_readiness_audit_surface_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_2_mcp_readiness_audit_surface_map = (
        memory_loop_subparsers.add_parser(
            "p4-m5-2-mcp-readiness-audit-surface-map"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_2_mcp_readiness_audit_surface_map
    )
    memory_loop_p4_m5_2_mcp_readiness_audit_surface_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_3_connector_readiness_audit_surface_map = (
        memory_loop_subparsers.add_parser(
            "p4-m5-3-connector-readiness-audit-surface-map"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_3_connector_readiness_audit_surface_map
    )
    memory_loop_p4_m5_3_connector_readiness_audit_surface_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_4_cross_surface_alignment_map = (
        memory_loop_subparsers.add_parser(
            "p4-m5-4-cross-surface-alignment-map"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_4_cross_surface_alignment_map
    )
    memory_loop_p4_m5_4_cross_surface_alignment_map.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_5_readiness_audit_closure_non_start_boundary_seal = (
        memory_loop_subparsers.add_parser(
            "p4-m5-5-readiness-audit-closure-non-start-boundary-seal"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_5_readiness_audit_closure_non_start_boundary_seal
    )
    memory_loop_p4_m5_5_readiness_audit_closure_non_start_boundary_seal.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m5_6_final_closure_handoff_next_corridor_non_start_index = (
        memory_loop_subparsers.add_parser(
            "p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m5_6_final_closure_handoff_next_corridor_non_start_index
    )
    memory_loop_p4_m5_6_final_closure_handoff_next_corridor_non_start_index.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_0_next_corridor_entry_boundary_contract = (
        memory_loop_subparsers.add_parser(
            "p4-m6-0-next-corridor-entry-boundary-contract"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_0_next_corridor_entry_boundary_contract
    )
    memory_loop_p4_m6_0_next_corridor_entry_boundary_contract.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_1_entry_preconditions_definition_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-1-entry-preconditions-definition-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_1_entry_preconditions_definition_surface
    )
    memory_loop_p4_m6_1_entry_preconditions_definition_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_2_entry_acceptance_non_evidence_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-2-entry-acceptance-non-evidence-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_2_entry_acceptance_non_evidence_surface
    )
    memory_loop_p4_m6_2_entry_acceptance_non_evidence_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_3_entry_deferral_non_execution_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-3-entry-deferral-non-execution-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_3_entry_deferral_non_execution_surface
    )
    memory_loop_p4_m6_3_entry_deferral_non_execution_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_4_entry_rejection_non_execution_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-4-entry-rejection-non-execution-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_4_entry_rejection_non_execution_surface
    )
    memory_loop_p4_m6_4_entry_rejection_non_execution_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_5_entry_escalation_non_routing_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-5-entry-escalation-non-routing-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_5_entry_escalation_non_routing_surface
    )
    memory_loop_p4_m6_5_entry_escalation_non_routing_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_6_entry_exception_non_override_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-6-entry-exception-non-override-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_6_entry_exception_non_override_surface
    )
    memory_loop_p4_m6_6_entry_exception_non_override_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_7_entry_conflict_non_resolution_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-7-entry-conflict-non-resolution-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_7_entry_conflict_non_resolution_surface
    )
    memory_loop_p4_m6_7_entry_conflict_non_resolution_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_8_entry_ambiguity_non_inference_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-8-entry-ambiguity-non-inference-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_8_entry_ambiguity_non_inference_surface
    )
    memory_loop_p4_m6_8_entry_ambiguity_non_inference_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_9_entry_dependency_non_activation_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-9-entry-dependency-non-activation-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_9_entry_dependency_non_activation_surface
    )
    memory_loop_p4_m6_9_entry_dependency_non_activation_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_10_entry_constraint_non_enforcement_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-10-entry-constraint-non-enforcement-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_10_entry_constraint_non_enforcement_surface
    )
    memory_loop_p4_m6_10_entry_constraint_non_enforcement_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_11_entry_risk_non_mitigation_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-11-entry-risk-non-mitigation-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_11_entry_risk_non_mitigation_surface
    )
    memory_loop_p4_m6_11_entry_risk_non_mitigation_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_12_entry_safeguard_non_activation_surface = (
        memory_loop_subparsers.add_parser(
            "p4-m6-12-entry-safeguard-non-activation-surface"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_12_entry_safeguard_non_activation_surface
    )
    memory_loop_p4_m6_12_entry_safeguard_non_activation_surface.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_13_entry_definition_corridor_closure_review = (
        memory_loop_subparsers.add_parser(
            "p4-m6-13-entry-definition-corridor-closure-review"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_13_entry_definition_corridor_closure_review
    )
    memory_loop_p4_m6_13_entry_definition_corridor_closure_review.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    memory_loop_p4_m6_14_entry_definition_corridor_final_closure_handoff = (
        memory_loop_subparsers.add_parser(
            "p4-m6-14-entry-definition-corridor-final-closure-handoff-"
            "next-corridor-non-start-index"
        )
    )
    _add_workspace_root(
        memory_loop_p4_m6_14_entry_definition_corridor_final_closure_handoff
    )
    memory_loop_p4_m6_14_entry_definition_corridor_final_closure_handoff.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    audit = subparsers.add_parser("audit")
    _add_workspace_root(audit)
    audit.add_argument("--limit", type=int, default=50)

    return parser


def run_operator_command(
    argv: list[str],
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = build_parser()

    try:
        with redirect_stderr(err):
            args = parser.parse_args(argv)
        payload = _run_parsed_command(args)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    except (OSError, ValueError) as exc:
        err.write(f"{exc}\n")
        return 1

    if isinstance(payload, str):
        out.write(payload)
    else:
        _write_json(out, payload)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_operator_command(sys.argv[1:] if argv is None else argv)


def _add_workspace_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace-root", default=".")


def _run_parsed_command(args: argparse.Namespace) -> dict[str, Any] | str:
    if args.command == "propose":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        proposal = store.propose_memory(
            project=args.project,
            namespace=args.namespace,
            content=args.content,
            source=args.source,
            tags=args.tag,
            confidence=args.confidence,
        )
        return {
            "proposal_id": proposal.id,
            "status": proposal.status,
            "project": proposal.project,
            "namespace": proposal.namespace,
            "storage_root": storage_root,
        }

    if args.command == "approve":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        memory = store.approve_proposal(
            args.proposal_id,
            approver=args.approver,
            note=args.note,
        )
        return {
            "memory_id": memory.id,
            "proposal_id": memory.proposal_id,
            "status": memory.status,
            "storage_root": storage_root,
        }

    if args.command == "reject":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        rejected = store.reject_proposal(
            args.proposal_id,
            reviewer=args.reviewer,
            reason=args.reason,
        )
        return {
            "proposal_id": rejected.id,
            "status": rejected.status,
            "reason": rejected.reason,
            "storage_root": storage_root,
        }

    if args.command == "recall":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        _validate_positive_limit(args.limit)
        results = store.recall(
            args.query,
            project=args.project,
            namespace=args.namespace,
            limit=args.limit,
            include_stale=args.include_stale,
            include_archived=args.include_archived,
        )
        return {
            "query": args.query,
            "count": len(results),
            "results": [asdict(result) for result in results],
            "storage_root": storage_root,
        }

    if args.command == "lifecycle":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        memory = store.set_memory_lifecycle(
            args.memory_id,
            args.state,
            actor=args.actor,
            reason=args.reason,
        )
        previous_lifecycle = _latest_lifecycle_audit_previous(store, memory.id)
        return {
            "memory_id": memory.id,
            "lifecycle": memory.lifecycle,
            "previous_lifecycle": previous_lifecycle,
            "status": memory.status,
            "storage_root": storage_root,
        }

    if args.command == "do-not-retry":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        if args.do_not_retry_command == "set":
            memory = store.set_do_not_retry(
                args.memory_id,
                reason=args.reason,
                actor=args.actor,
                alternative=args.alternative,
            )
            return {
                "memory_id": memory.id,
                "status": memory.status,
                "do_not_retry": asdict(memory.do_not_retry) if memory.do_not_retry is not None else None,
                "storage_root": storage_root,
            }

        if args.do_not_retry_command == "clear":
            memory = store.clear_do_not_retry(
                args.memory_id,
                actor=args.actor,
                reason=args.reason,
            )
            previous = _latest_do_not_retry_clear_previous(store, memory.id)
            return {
                "memory_id": memory.id,
                "status": memory.status,
                "do_not_retry": None,
                "previous_do_not_retry": previous,
                "storage_root": storage_root,
            }

        raise ValueError(f"unsupported_do_not_retry_command:{args.do_not_retry_command}")

    if args.command == "project-seed":
        if args.project_seed_command == "list":
            seeds = list_project_memory_seeds()
            return {
                "count": len(seeds),
                "seeds": [_seed_summary(seed) for seed in seeds],
            }

        if args.project_seed_command == "show":
            seed = get_project_memory_seed(args.seed_id)
            return _seed_detail(seed)

        if args.project_seed_command == "pack":
            return render_project_memory_seed_pack()

        if args.project_seed_command == "approval-runbook":
            if args.format == "markdown":
                return render_seed_approval_runbook_markdown()
            if args.format == "json":
                entries = seed_approval_runbook_as_dicts()
                return {
                    "boundary": SEED_APPROVAL_RUNBOOK_BOUNDARY,
                    "count": len(entries),
                    "entries": list(entries),
                }
            raise ValueError(f"unsupported_project_seed_approval_runbook_format:{args.format}")

        if args.project_seed_command == "propose":
            seed = get_project_memory_seed(args.seed_id)
            actor = _required_text(args.actor, "actor")
            store = create_workspace_subspace_memory_store(Path(args.workspace_root))
            proposal = store.propose_memory(
                project=seed.project,
                namespace=seed.namespace,
                content=seed.content,
                source=f"{seed.source}:proposed-by:{actor}",
                tags=seed.tags,
                confidence=seed.confidence,
            )
            return {
                "seed_id": seed.seed_id,
                "proposal_id": proposal.id,
                "status": proposal.status,
                "project": proposal.project,
                "namespace": proposal.namespace,
                "storage_root": str(store.storage_root),
                "requires_human_approval": True,
            }

        raise ValueError(f"unsupported_project_seed_command:{args.project_seed_command}")

    if args.command == "memory-loop":
        if args.memory_loop_command == "checklist":
            if args.format == "markdown":
                return render_human_gated_memory_loop_checklist_markdown()
            if args.format == "json":
                items = human_gated_memory_loop_checklist_as_dicts()
                return {
                    "boundary": HUMAN_GATED_MEMORY_LOOP_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": human_gated_memory_loop_status_report(),
                }
            raise ValueError(f"unsupported_memory_loop_checklist_format:{args.format}")

        if args.memory_loop_command == "review-status":
            if args.format == "markdown":
                return render_human_gated_proposal_review_status_markdown()
            if args.format == "json":
                items = human_gated_proposal_review_status_as_dicts()
                return {
                    "boundary": HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": human_gated_proposal_review_status_report(),
                }
            raise ValueError(f"unsupported_memory_loop_review_status_format:{args.format}")

        if args.memory_loop_command == "recall-verification-status":
            if args.format == "markdown":
                return render_human_gated_recall_verification_status_markdown()
            if args.format == "json":
                items = human_gated_recall_verification_status_as_dicts()
                return {
                    "boundary": HUMAN_GATED_RECALL_VERIFICATION_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": human_gated_recall_verification_status_report(),
                }
            raise ValueError(f"unsupported_memory_loop_recall_verification_status_format:{args.format}")

        if args.memory_loop_command == "lifecycle-verification-status":
            if args.format == "markdown":
                return render_human_gated_lifecycle_verification_status_markdown()
            if args.format == "json":
                items = human_gated_lifecycle_verification_status_as_dicts()
                return {
                    "boundary": HUMAN_GATED_LIFECYCLE_VERIFICATION_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": human_gated_lifecycle_verification_status_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_lifecycle_verification_status_format:{args.format}"
            )

        if args.memory_loop_command == "do-not-retry-verification-status":
            if args.format == "markdown":
                return render_human_gated_do_not_retry_verification_status_markdown()
            if args.format == "json":
                items = human_gated_do_not_retry_verification_status_as_dicts()
                return {
                    "boundary": HUMAN_GATED_DO_NOT_RETRY_VERIFICATION_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": human_gated_do_not_retry_verification_status_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_do_not_retry_verification_status_format:{args.format}"
            )

        if args.memory_loop_command == "source-provenance-verification-status":
            if args.format == "markdown":
                return render_source_provenance_verification_status_markdown()
            if args.format == "json":
                items = source_provenance_verification_status_as_dicts()
                return {
                    "boundary": SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": source_provenance_verification_status_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_source_provenance_verification_status_format:{args.format}"
            )

        if args.memory_loop_command == "decision-readiness-status":
            if args.format == "markdown":
                return render_decision_readiness_status_markdown()
            if args.format == "json":
                items = decision_readiness_status_as_dicts()
                return {
                    "boundary": DECISION_READINESS_STATUS_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": decision_readiness_status_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_decision_readiness_status_format:{args.format}"
            )

        if args.memory_loop_command == "manual-decision-preview":
            if args.format == "markdown":
                return render_manual_decision_preview_markdown()
            if args.format == "json":
                frames = manual_decision_preview_as_dicts()
                return {
                    "boundary": MANUAL_DECISION_PREVIEW_BOUNDARY,
                    "count": len(frames),
                    "frames": list(frames),
                    "status": manual_decision_preview_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_manual_decision_preview_format:{args.format}"
            )

        if args.memory_loop_command == "governance-pack-export":
            if args.format == "markdown":
                return render_governance_pack_markdown()
            if args.format == "json":
                sections = governance_pack_as_dicts()
                return {
                    "boundary": GOVERNANCE_PACK_EXPORT_BOUNDARY,
                    "count": len(sections),
                    "sections": list(sections),
                    "status": governance_pack_export_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_governance_pack_export_format:{args.format}"
            )

        if args.memory_loop_command == "final-boundary-audit":
            if args.format == "markdown":
                return render_final_boundary_audit_markdown()
            if args.format == "json":
                items = final_boundary_audit_as_dicts()
                return {
                    "boundary": FINAL_BOUNDARY_AUDIT_BOUNDARY,
                    "count": len(items),
                    "items": list(items),
                    "status": final_boundary_audit_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_final_boundary_audit_format:{args.format}"
            )

        if args.memory_loop_command == "manual-execution-hardening":
            if args.format == "markdown":
                return render_manual_execution_hardening_markdown()
            if args.format == "json":
                requirements = manual_execution_hardening_as_dicts()
                return {
                    "boundary": MANUAL_EXECUTION_HARDENING_BOUNDARY,
                    "count": len(requirements),
                    "requirements": list(requirements),
                    "status": manual_execution_hardening_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_manual_execution_hardening_format:{args.format}"
            )

        if args.memory_loop_command == "execution-surface-contract":
            if args.format == "markdown":
                return render_execution_surface_contract_markdown()
            if args.format == "json":
                fields = execution_surface_contract_as_dicts()
                return {
                    "boundary": EXECUTION_SURFACE_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_surface_contract_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_surface_contract_format:{args.format}"
            )

        if args.memory_loop_command == "execution-contract-validation-matrix":
            if args.format == "markdown":
                return render_execution_contract_validation_matrix_markdown()
            if args.format == "json":
                rows = execution_contract_validation_matrix_as_dicts()
                return {
                    "boundary": EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY,
                    "count": len(rows),
                    "rows": list(rows),
                    "status": execution_contract_validation_matrix_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_contract_validation_matrix_format:{args.format}"
            )

        if args.memory_loop_command == "manual-authorization-evidence-envelope":
            if args.format == "markdown":
                return render_manual_authorization_evidence_envelope_markdown()
            if args.format == "json":
                fields = manual_authorization_evidence_envelope_as_dicts()
                return {
                    "boundary": MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": manual_authorization_evidence_envelope_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_manual_authorization_evidence_envelope_format:{args.format}"
            )

        if args.memory_loop_command == "human-confirmation-snapshot-contract":
            if args.format == "markdown":
                return render_human_confirmation_snapshot_contract_markdown()
            if args.format == "json":
                fields = human_confirmation_snapshot_contract_as_dicts()
                return {
                    "boundary": HUMAN_CONFIRMATION_SNAPSHOT_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": human_confirmation_snapshot_contract_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_human_confirmation_snapshot_contract_format:{args.format}"
            )

        if args.memory_loop_command == "execution-preconditions-snapshot-map":
            if args.format == "markdown":
                return render_execution_preconditions_snapshot_map_markdown()
            if args.format == "json":
                fields = execution_preconditions_snapshot_map_as_dicts()
                return {
                    "boundary": EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_preconditions_snapshot_map_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_preconditions_snapshot_map_format:{args.format}"
            )

        if args.memory_loop_command == "execution-risk-acknowledgement-map":
            if args.format == "markdown":
                return render_execution_risk_acknowledgement_map_markdown()
            if args.format == "json":
                fields = execution_risk_acknowledgement_map_as_dicts()
                return {
                    "boundary": EXECUTION_RISK_ACKNOWLEDGEMENT_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_risk_acknowledgement_map_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_risk_acknowledgement_map_format:{args.format}"
            )

        if args.memory_loop_command == "execution-risk-acceptance-prohibition-map":
            if args.format == "markdown":
                return render_execution_risk_acceptance_prohibition_map_markdown()
            if args.format == "json":
                fields = execution_risk_acceptance_prohibition_map_as_dicts()
                return {
                    "boundary": EXECUTION_RISK_ACCEPTANCE_PROHIBITION_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_risk_acceptance_prohibition_map_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_risk_acceptance_prohibition_map_format:{args.format}"
            )

        if args.memory_loop_command == "execution-risk-waiver-prohibition-map":
            if args.format == "markdown":
                return render_execution_risk_waiver_prohibition_map_markdown()
            if args.format == "json":
                fields = execution_risk_waiver_prohibition_map_as_dicts()
                return {
                    "boundary": EXECUTION_RISK_WAIVER_PROHIBITION_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_risk_waiver_prohibition_map_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_risk_waiver_prohibition_map_format:{args.format}"
            )

        if args.memory_loop_command == "execution-decision-non-equivalence-map":
            if args.format == "markdown":
                return render_execution_decision_non_equivalence_map_markdown()
            if args.format == "json":
                fields = execution_decision_non_equivalence_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_NON_EQUIVALENCE_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_non_equivalence_map_report(),
                }
            raise ValueError(
                f"unsupported_memory_loop_execution_decision_non_equivalence_map_format:{args.format}"
            )

        if args.memory_loop_command == "execution-decision-recommendation-prohibition-map":
            if args.format == "markdown":
                return render_execution_decision_recommendation_prohibition_map_markdown()
            if args.format == "json":
                fields = execution_decision_recommendation_prohibition_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_RECOMMENDATION_PROHIBITION_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_recommendation_prohibition_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_recommendation_prohibition_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "execution-decision-default-denial-boundary-map":
            if args.format == "markdown":
                return render_execution_decision_default_denial_boundary_map_markdown()
            if args.format == "json":
                fields = execution_decision_default_denial_boundary_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_DEFAULT_DENIAL_BOUNDARY_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_default_denial_boundary_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_default_denial_boundary_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "execution-decision-silence-non-consent-map":
            if args.format == "markdown":
                return render_execution_decision_silence_non_consent_map_markdown()
            if args.format == "json":
                fields = execution_decision_silence_non_consent_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_silence_non_consent_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_silence_non_consent_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "execution-decision-negative-evidence-non-override-map":
            if args.format == "markdown":
                return render_execution_decision_negative_evidence_non_override_map_markdown()
            if args.format == "json":
                fields = execution_decision_negative_evidence_non_override_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_NEGATIVE_EVIDENCE_NON_OVERRIDE_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_negative_evidence_non_override_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_negative_evidence_non_override_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "execution-decision-conflicting-evidence-isolation-map":
            if args.format == "markdown":
                return render_execution_decision_conflicting_evidence_isolation_map_markdown()
            if args.format == "json":
                fields = execution_decision_conflicting_evidence_isolation_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_CONFLICTING_EVIDENCE_ISOLATION_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_conflicting_evidence_isolation_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_conflicting_evidence_isolation_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "execution-decision-evidence-precedence-prohibition-map":
            if args.format == "markdown":
                return render_execution_decision_evidence_precedence_prohibition_map_markdown()
            if args.format == "json":
                fields = execution_decision_evidence_precedence_prohibition_map_as_dicts()
                return {
                    "boundary": EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": execution_decision_evidence_precedence_prohibition_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_execution_decision_evidence_precedence_prohibition_map_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "final-non-execution-boundary-audit":
            if args.format == "markdown":
                return render_final_non_execution_boundary_audit_markdown()
            if args.format == "json":
                fields = final_non_execution_boundary_audit_as_dicts()
                return {
                    "boundary": FINAL_NON_EXECUTION_BOUNDARY_AUDIT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": final_non_execution_boundary_audit_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_final_non_execution_boundary_audit_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "p4-m2-closure-handoff-contract":
            if args.format == "markdown":
                return render_closure_handoff_contract_markdown()
            if args.format == "json":
                fields = closure_handoff_contract_as_dicts()
                return {
                    "boundary": CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": closure_handoff_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m2_closure_handoff_contract_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "governed-transition-intake-boundary-contract":
            if args.format == "markdown":
                return render_governed_transition_intake_boundary_contract_markdown()
            if args.format == "json":
                fields = governed_transition_intake_boundary_contract_as_dicts()
                return {
                    "boundary": GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": governed_transition_intake_boundary_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_boundary_contract_format:"
                f"{args.format}"
            )

        if args.memory_loop_command == "governed-transition-intake-request-envelope-contract":
            if args.format == "markdown":
                return render_governed_transition_intake_request_envelope_contract_markdown()
            if args.format == "json":
                fields = governed_transition_intake_request_envelope_contract_as_dicts()
                return {
                    "boundary": GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": governed_transition_intake_request_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_request_envelope_contract_format:"
                f"{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-evidence-reference-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_evidence_reference_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_evidence_reference_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_EVIDENCE_REFERENCE_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_evidence_reference_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_evidence_reference_"
                f"envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-human-context-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_human_context_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_human_context_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_human_context_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_human_"
                f"context_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-target-phase-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_target_phase_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_target_phase_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": governed_transition_intake_target_phase_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_target_phase_"
                f"envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-reason-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_reason_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_reason_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_reason_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"reason_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-constraint-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_constraint_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_constraint_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_constraint_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"constraint_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-dependency-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_dependency_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_dependency_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_dependency_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"dependency_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-impact-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_impact_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_impact_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_impact_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"impact_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-risk-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_risk_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_risk_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_RISK_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_risk_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"risk_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-assumption-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_assumption_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_assumption_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_assumption_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"assumption_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-declared-transition-safeguard-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_declared_transition_safeguard_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_declared_transition_safeguard_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_SAFEGUARD_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_declared_transition_safeguard_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_declared_transition_"
                f"safeguard_envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-package-assembly-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_package_assembly_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_package_assembly_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_package_assembly_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_package_assembly_"
                f"envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-final-non-validation-boundary-audit"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_final_non_validation_boundary_audit_markdown()
                )
            if args.format == "json":
                fields = (
                    governed_transition_intake_final_non_validation_boundary_audit_as_dicts()
                )
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_final_non_validation_boundary_audit_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_final_"
                f"non_validation_boundary_audit_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-closure-handoff-contract"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_closure_handoff_contract_markdown()
                )
            if args.format == "json":
                fields = governed_transition_intake_closure_handoff_contract_as_dicts()
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": governed_transition_intake_closure_handoff_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_closure_"
                f"handoff_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-phase-closure-review"
        ):
            if args.format == "markdown":
                return render_governed_transition_intake_phase_closure_review_markdown()
            if args.format == "json":
                fields = governed_transition_intake_phase_closure_review_as_dicts()
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_PHASE_CLOSURE_REVIEW_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": governed_transition_intake_phase_closure_review_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_phase_"
                f"closure_review_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "governed-transition-intake-final-phase-handoff-summary"
        ):
            if args.format == "markdown":
                return (
                    render_governed_transition_intake_final_phase_handoff_summary_markdown()
                )
            if args.format == "json":
                fields = governed_transition_intake_final_phase_handoff_summary_as_dicts()
                return {
                    "boundary": (
                        GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        governed_transition_intake_final_phase_handoff_summary_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_governed_transition_intake_final_phase_"
                f"handoff_summary_format:{args.format}"
            )

        if args.memory_loop_command == "entry-gate-design-boundary-contract":
            if args.format == "markdown":
                return render_entry_gate_design_boundary_contract_markdown()
            if args.format == "json":
                fields = entry_gate_design_boundary_contract_as_dicts()
                return {
                    "boundary": ENTRY_GATE_DESIGN_BOUNDARY_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": entry_gate_design_boundary_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_boundary_contract_"
                f"format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "entry-gate-design-request-envelope-contract"
        ):
            if args.format == "markdown":
                return render_entry_gate_design_request_envelope_contract_markdown()
            if args.format == "json":
                fields = entry_gate_design_request_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": entry_gate_design_request_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_request_envelope_"
                f"contract_format:{args.format}"
            )

        if args.memory_loop_command == "evidence-reference-envelope-contract":
            if args.format == "markdown":
                return render_evidence_reference_envelope_contract_markdown()
            if args.format == "json":
                fields = evidence_reference_envelope_contract_as_dicts()
                return {
                    "boundary": EVIDENCE_REFERENCE_ENVELOPE_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": evidence_reference_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_evidence_reference_envelope_"
                f"contract_format:{args.format}"
            )

        if args.memory_loop_command == "declared-human-context-envelope-contract":
            if args.format == "markdown":
                return render_declared_human_context_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_human_context_envelope_contract_as_dicts()
                return {
                    "boundary": DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": declared_human_context_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_human_context_envelope_"
                f"contract_format:{args.format}"
            )

        if args.memory_loop_command == "target-phase-envelope-contract":
            if args.format == "markdown":
                return render_target_phase_envelope_contract_markdown()
            if args.format == "json":
                fields = target_phase_envelope_contract_as_dicts()
                return {
                    "boundary": TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": target_phase_envelope_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_target_phase_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-reason-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_reason_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_reason_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_reason_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_reason_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-constraint-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_constraint_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_constraint_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_constraint_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_constraint_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-dependency-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_dependency_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_dependency_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_dependency_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_dependency_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-impact-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_impact_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_impact_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_impact_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_impact_envelope_"
                f"contract_format:{args.format}"
            )

        if args.memory_loop_command == "declared-transition-risk-envelope-contract":
            if args.format == "markdown":
                return render_declared_transition_risk_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_risk_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_RISK_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_risk_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_risk_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-assumption-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_assumption_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_assumption_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_assumption_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_assumption_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-safeguard-envelope-contract"
        ):
            if args.format == "markdown":
                return render_declared_transition_safeguard_envelope_contract_markdown()
            if args.format == "json":
                fields = declared_transition_safeguard_envelope_contract_as_dicts()
                return {
                    "boundary": (
                        DECLARED_TRANSITION_SAFEGUARD_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_safeguard_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_safeguard_envelope_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "declared-transition-package-assembly-envelope-contract"
        ):
            if args.format == "markdown":
                return (
                    render_declared_transition_package_assembly_envelope_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    declared_transition_package_assembly_envelope_contract_as_dicts()
                )
                return {
                    "boundary": (
                        DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        declared_transition_package_assembly_envelope_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_declared_transition_package_assembly_"
                f"envelope_contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "entry-gate-design-final-non-validation-boundary-audit"
        ):
            if args.format == "markdown":
                return (
                    render_entry_gate_design_final_non_validation_boundary_audit_markdown()
                )
            if args.format == "json":
                fields = (
                    entry_gate_design_final_non_validation_boundary_audit_as_dicts()
                )
                return {
                    "boundary": (
                        ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        entry_gate_design_final_non_validation_boundary_audit_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_final_non_validation_"
                f"boundary_audit_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "entry-gate-design-closure-handoff-contract"
        ):
            if args.format == "markdown":
                return render_entry_gate_design_closure_handoff_contract_markdown()
            if args.format == "json":
                fields = entry_gate_design_closure_handoff_contract_as_dicts()
                return {
                    "boundary": ENTRY_GATE_DESIGN_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": entry_gate_design_closure_handoff_contract_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_closure_handoff_"
                f"contract_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "entry-gate-design-phase-closure-review"
        ):
            if args.format == "markdown":
                return render_entry_gate_design_phase_closure_review_markdown()
            if args.format == "json":
                fields = entry_gate_design_phase_closure_review_as_dicts()
                return {
                    "boundary": ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": entry_gate_design_phase_closure_review_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_phase_closure_"
                f"review_format:{args.format}"
            )

        if (
            args.memory_loop_command
            == "entry-gate-design-final-phase-handoff-summary"
        ):
            if args.format == "markdown":
                return (
                    render_entry_gate_design_final_phase_handoff_summary_markdown()
                )
            if args.format == "json":
                fields = entry_gate_design_final_phase_handoff_summary_as_dicts()
                return {
                    "boundary": ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        entry_gate_design_final_phase_handoff_summary_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_final_phase_handoff_"
                f"summary_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "entry-gate-design-phase-terminal-closure-seal"
        ):
            if args.format == "markdown":
                return (
                    render_entry_gate_design_phase_terminal_closure_seal_markdown()
                )
            if args.format == "json":
                fields = entry_gate_design_phase_terminal_closure_seal_as_dicts()
                return {
                    "boundary": ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        entry_gate_design_phase_terminal_closure_seal_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_entry_gate_design_phase_terminal_closure_"
                f"seal_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-index-entry-planning-gate"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m4_final_closure_index_entry_planning_gate_markdown()
                )
            if args.format == "json":
                fields = p4_m4_final_closure_index_entry_planning_gate_as_dicts()
                return {
                    "boundary": P4_M4_FINAL_CLOSURE_INDEX_ENTRY_PLANNING_GATE_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_index_entry_planning_gate_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_index_entry_"
                f"planning_gate_format:{args.format}"
            )
        if args.memory_loop_command == "p4-m4-final-closure-evidence-index":
            if args.format == "markdown":
                return render_p4_m4_final_closure_evidence_index_markdown()
            if args.format == "json":
                fields = p4_m4_final_closure_evidence_index_as_dicts()
                return {
                    "boundary": P4_M4_FINAL_CLOSURE_EVIDENCE_INDEX_BOUNDARY,
                    "count": len(fields),
                    "fields": list(fields),
                    "status": p4_m4_final_closure_evidence_index_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_evidence_"
                f"index_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-operator-handoff-index"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m4_final_closure_operator_handoff_index_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m4_final_closure_operator_handoff_index_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M4_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_operator_handoff_index_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_operator_"
                f"handoff_index_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-transition-readiness-non-start-index"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m4_final_closure_transition_readiness_non_start_index_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m4_final_closure_transition_readiness_non_start_index_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_transition_readiness_non_start_index_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_transition_"
                f"readiness_non_start_index_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-non-start-bridge-index"
        ):
            if args.format == "markdown":
                return render_p4_m4_final_closure_non_start_bridge_index_markdown()
            if args.format == "json":
                fields = p4_m4_final_closure_non_start_bridge_index_as_dicts()
                return {
                    "boundary": (
                        P4_M4_FINAL_CLOSURE_NON_START_BRIDGE_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_non_start_bridge_index_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_non_start_"
                f"bridge_index_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-boundary-freeze-index"
        ):
            if args.format == "markdown":
                return render_p4_m4_final_closure_boundary_freeze_index_markdown()
            if args.format == "json":
                fields = (
                    p4_m4_final_closure_boundary_freeze_index_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M4_FINAL_CLOSURE_BOUNDARY_FREEZE_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_boundary_freeze_index_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_boundary_"
                f"freeze_index_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m4-final-closure-roadmap-alignment-snapshot"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m4_final_closure_roadmap_alignment_snapshot_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m4_final_closure_roadmap_alignment_snapshot_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M4_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m4_final_closure_roadmap_alignment_snapshot_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m4_final_closure_roadmap_"
                f"alignment_snapshot_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_0_api_mcp_connector_"
                "readiness_audit_boundary_contract_format:"
                f"{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-1-api-readiness-audit-surface-map"
        ):
            if args.format == "markdown":
                return render_p4_m5_1_api_readiness_audit_surface_map_markdown()
            if args.format == "json":
                fields = p4_m5_1_api_readiness_audit_surface_map_as_dicts()
                return {
                    "boundary": (
                        P4_M5_1_API_READINESS_AUDIT_SURFACE_MAP_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": p4_m5_1_api_readiness_audit_surface_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_1_api_readiness_audit_"
                f"surface_map_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-2-mcp-readiness-audit-surface-map"
        ):
            if args.format == "markdown":
                return render_p4_m5_2_mcp_readiness_audit_surface_map_markdown()
            if args.format == "json":
                fields = p4_m5_2_mcp_readiness_audit_surface_map_as_dicts()
                return {
                    "boundary": (
                        P4_M5_2_MCP_READINESS_AUDIT_SURFACE_MAP_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": p4_m5_2_mcp_readiness_audit_surface_map_report(),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_2_mcp_readiness_audit_"
                f"surface_map_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-3-connector-readiness-audit-surface-map"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m5_3_connector_readiness_audit_surface_map_markdown()
                )
            if args.format == "json":
                fields = p4_m5_3_connector_readiness_audit_surface_map_as_dicts()
                return {
                    "boundary": (
                        P4_M5_3_CONNECTOR_READINESS_AUDIT_SURFACE_MAP_BOUNDARY
                    ),
                    "count": len(fields),
                    "fields": list(fields),
                    "status": (
                        p4_m5_3_connector_readiness_audit_surface_map_report()
                    ),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_3_connector_readiness_audit_"
                f"surface_map_format:{args.format}"
            )
        if args.memory_loop_command == "p4-m5-4-cross-surface-alignment-map":
            if args.format == "markdown":
                return render_p4_m5_4_cross_surface_alignment_map_markdown()
            if args.format == "json":
                fields = p4_m5_4_cross_surface_alignment_map_as_dicts()
                return {
                    "boundary": P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_BOUNDARY,
                    "count": len(fields),
                    "false_flags": len(P4_M5_4_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m5_4_cross_surface_alignment_map_report(),
                    "true_flags": len(P4_M5_4_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_4_cross_surface_alignment_"
                f"map_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-5-readiness-audit-closure-non-start-boundary-seal"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m5_5_readiness_audit_closure_non_start_boundary_seal_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m5_5_readiness_audit_closure_non_start_boundary_seal_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M5_5_READINESS_AUDIT_CLOSURE_NON_START_BOUNDARY_SEAL_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M5_5_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m5_5_readiness_audit_closure_non_start_boundary_seal_report()
                    ),
                    "true_flags": len(P4_M5_5_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_5_readiness_audit_closure_"
                "non_start_boundary_seal_format:"
                f"{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M5_6_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m5_6_final_closure_handoff_next_corridor_non_start_index_report()
                    ),
                    "true_flags": len(P4_M5_6_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m5_6_final_closure_handoff_"
                "next_corridor_non_start_index_format:"
                f"{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-0-next-corridor-entry-boundary-contract"
        ):
            if args.format == "markdown":
                return render_p4_m6_0_next_corridor_entry_boundary_contract_markdown()
            if args.format == "json":
                fields = p4_m6_0_next_corridor_entry_boundary_contract_as_dicts()
                return {
                    "boundary": (
                        P4_M6_0_NEXT_CORRIDOR_ENTRY_BOUNDARY_CONTRACT_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_0_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_0_next_corridor_entry_boundary_contract_report()
                    ),
                    "true_flags": len(P4_M6_0_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_0_next_corridor_entry_"
                f"boundary_contract_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-1-entry-preconditions-definition-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_1_entry_preconditions_definition_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_1_entry_preconditions_definition_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_1_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m6_1_entry_preconditions_definition_surface_report(),
                    "true_flags": len(P4_M6_1_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_1_entry_preconditions_"
                f"definition_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-2-entry-acceptance-non-evidence-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_2_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m6_2_entry_acceptance_non_evidence_surface_report(),
                    "true_flags": len(P4_M6_2_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_2_entry_acceptance_"
                f"non_evidence_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-3-entry-deferral-non-execution-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_3_entry_deferral_non_execution_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_3_entry_deferral_non_execution_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_3_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m6_3_entry_deferral_non_execution_surface_report(),
                    "true_flags": len(P4_M6_3_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_3_entry_deferral_"
                f"non_execution_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-4-entry-rejection-non-execution-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_4_entry_rejection_non_execution_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_4_entry_rejection_non_execution_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_4_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m6_4_entry_rejection_non_execution_surface_report(),
                    "true_flags": len(P4_M6_4_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_4_entry_rejection_"
                f"non_execution_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-5-entry-escalation-non-routing-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_5_entry_escalation_non_routing_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_5_entry_escalation_non_routing_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_5_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_5_entry_escalation_non_routing_surface_report()
                    ),
                    "true_flags": len(P4_M6_5_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_5_entry_escalation_"
                f"non_routing_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-6-entry-exception-non-override-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_6_entry_exception_non_override_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_6_entry_exception_non_override_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_6_ENTRY_EXCEPTION_NON_OVERRIDE_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_6_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_6_entry_exception_non_override_surface_report()
                    ),
                    "true_flags": len(P4_M6_6_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_6_entry_exception_"
                f"non_override_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-7-entry-conflict-non-resolution-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_7_entry_conflict_non_resolution_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_7_entry_conflict_non_resolution_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_7_ENTRY_CONFLICT_NON_RESOLUTION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_7_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_7_entry_conflict_non_resolution_surface_report()
                    ),
                    "true_flags": len(P4_M6_7_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_7_entry_conflict_"
                f"non_resolution_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-8-entry-ambiguity-non-inference-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_8_entry_ambiguity_non_inference_surface_markdown()
                )
            if args.format == "json":
                fields = p4_m6_8_entry_ambiguity_non_inference_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_8_ENTRY_AMBIGUITY_NON_INFERENCE_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_8_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_8_entry_ambiguity_non_inference_surface_report()
                    ),
                    "true_flags": len(P4_M6_8_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_8_entry_ambiguity_"
                f"non_inference_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-9-entry-dependency-non-activation-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_9_entry_dependency_non_activation_surface_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m6_9_entry_dependency_non_activation_surface_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_9_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_9_entry_dependency_non_activation_surface_report()
                    ),
                    "true_flags": len(P4_M6_9_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_9_entry_dependency_"
                f"non_activation_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-10-entry-constraint-non-enforcement-surface"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_10_entry_constraint_non_enforcement_surface_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m6_10_entry_constraint_non_enforcement_surface_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M6_10_ENTRY_CONSTRAINT_NON_ENFORCEMENT_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_10_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_10_entry_constraint_non_enforcement_surface_report()
                    ),
                    "true_flags": len(P4_M6_10_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_10_entry_constraint_"
                f"non_enforcement_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-11-entry-risk-non-mitigation-surface"
        ):
            if args.format == "markdown":
                return render_p4_m6_11_entry_risk_non_mitigation_surface_markdown()
            if args.format == "json":
                fields = p4_m6_11_entry_risk_non_mitigation_surface_as_dicts()
                return {
                    "boundary": P4_M6_11_ENTRY_RISK_NON_MITIGATION_SURFACE_BOUNDARY,
                    "count": len(fields),
                    "false_flags": len(P4_M6_11_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": p4_m6_11_entry_risk_non_mitigation_surface_report(),
                    "true_flags": len(P4_M6_11_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_11_entry_risk_"
                f"non_mitigation_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-12-entry-safeguard-non-activation-surface"
        ):
            if args.format == "markdown":
                return render_p4_m6_12_entry_safeguard_non_activation_surface_markdown()
            if args.format == "json":
                fields = p4_m6_12_entry_safeguard_non_activation_surface_as_dicts()
                return {
                    "boundary": (
                        P4_M6_12_ENTRY_SAFEGUARD_NON_ACTIVATION_SURFACE_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_12_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_12_entry_safeguard_non_activation_surface_report()
                    ),
                    "true_flags": len(P4_M6_12_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_12_entry_safeguard_"
                f"non_activation_surface_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-13-entry-definition-corridor-closure-review"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_13_entry_definition_corridor_closure_review_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m6_13_entry_definition_corridor_closure_review_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_13_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_13_entry_definition_corridor_closure_review_report()
                    ),
                    "true_flags": len(P4_M6_13_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_13_entry_definition_"
                f"corridor_closure_review_format:{args.format}"
            )
        if (
            args.memory_loop_command
            == "p4-m6-14-entry-definition-corridor-final-closure-handoff-"
            "next-corridor-non-start-index"
        ):
            if args.format == "markdown":
                return (
                    render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown()
                )
            if args.format == "json":
                fields = (
                    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_as_dicts()
                )
                return {
                    "boundary": (
                        P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY
                    ),
                    "count": len(fields),
                    "false_flags": len(P4_M6_14_FALSE_STATUS_FLAGS),
                    "fields": list(fields),
                    "status": (
                        p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
                    ),
                    "true_flags": len(P4_M6_14_TRUE_STATUS_FLAGS),
                }
            raise ValueError(
                "unsupported_memory_loop_p4_m6_14_entry_definition_"
                "corridor_final_closure_handoff_next_corridor_non_start_"
                f"index_format:{args.format}"
            )

        raise ValueError(f"unsupported_memory_loop_command:{args.memory_loop_command}")

    if args.command == "audit":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        _validate_positive_limit(args.limit)
        events = store.list_audit_events()
        limited_events = events[-args.limit :]
        return {
            "count": len(limited_events),
            "events": [asdict(event) for event in limited_events],
            "storage_root": storage_root,
        }

    raise ValueError(f"unsupported_command:{args.command}")


def _seed_summary(seed: Any) -> dict[str, Any]:
    return {
        "seed_id": seed.seed_id,
        "project": seed.project,
        "namespace": seed.namespace,
        "source": seed.source,
        "tags": list(seed.tags),
        "confidence": seed.confidence,
    }


def _seed_detail(seed: Any) -> dict[str, Any]:
    return {
        **_seed_summary(seed),
        "content": seed.content,
    }


def _latest_lifecycle_audit_previous(store: Any, memory_id: str) -> str:
    for event in reversed(store.list_audit_events()):
        if event.event_type == "memory_lifecycle_updated" and event.target_id == memory_id:
            return str(event.detail["previous_lifecycle"])
    raise ValueError("memory_lifecycle_audit_not_found")


def _latest_do_not_retry_clear_previous(store: Any, memory_id: str) -> dict[str, Any] | None:
    for event in reversed(store.list_audit_events()):
        if event.event_type == "memory_do_not_retry_cleared" and event.target_id == memory_id:
            previous = event.detail["previous_do_not_retry"]
            if previous is None:
                return None
            return dict(previous)
    raise ValueError("memory_do_not_retry_clear_audit_not_found")


def _validate_positive_limit(limit: int) -> None:
    if limit < 1:
        raise ValueError("limit_must_be_positive")


def _required_text(value: object, field: str) -> str:
    cleaned = str(value or "").strip()
    if not cleaned:
        raise ValueError(f"{field}_must_be_non_empty")
    return cleaned


def _write_json(stdout: TextIO, payload: dict[str, Any]) -> None:
    json.dump(payload, stdout, ensure_ascii=False, sort_keys=True)
    stdout.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
