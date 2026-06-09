"""Deterministic local release integrity audit for v2.0.0 through v2.58.0."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
from typing import Any, Iterable, Mapping

from .memory_token_authority_boundary_contract_dry_run import (
    NO_TOKEN_NO_WRITE_FLAGS,
    SOURCE_REQUIRED_KEYS,
    run_memory_token_authority_boundary_contract_dry_run,
)
from .governed_memory_proposal_pack_dry_run import (
    build_governed_memory_proposal_pack_dry_run,
)
from .governed_memory_proposal_review_gate_dry_run import (
    run_governed_memory_proposal_review_gate_dry_run,
)
from .governed_memory_approval_request_dry_run import (
    build_governed_memory_approval_request_dry_run,
)
from .openclaw_audit_review import build_openclaw_audit_review
from .provider import MemoryFabricProvider
from .skill_fabric import SkillFabricPaths, initialize_skill_fabric, verify_skill_fabric
from .skill_fabric_simulation import run_skill_fabric_github_archive_simulation


RELEASE_INTEGRITY_AUDIT_VERSION = "2.58.0"

EXPECTED_RELEASE_TAGS = ("v2.0.0", "v2.1.0", "v2.2.0")
EXPECTED_RELEASE_FILES = (
    "src/hermes_memory_fabric/memory_token_authority_boundary_contract_dry_run.py",
    "scripts/smoke_token_authority_boundary_contract_dry_run.py",
    "tests/test_memory_token_authority_boundary_contract_dry_run.py",
    "docs/TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN.md",
    "src/hermes_memory_fabric/skill_fabric.py",
    "scripts/skill_fabric.py",
    "tests/test_skill_fabric.py",
    "docs/SHARED_SKILL_FABRIC.md",
    "src/hermes_memory_fabric/skill_fabric_simulation.py",
    "scripts/smoke_skill_fabric_simulation.py",
    "tests/test_skill_fabric_simulation.py",
    "src/hermes_memory_fabric/governed_memory_proposal_pack_dry_run.py",
    "scripts/smoke_governed_memory_proposal_pack_dry_run.py",
    "tests/test_governed_memory_proposal_pack_dry_run.py",
    "docs/GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN.md",
    "src/hermes_memory_fabric/governed_memory_proposal_review_gate_dry_run.py",
    "scripts/smoke_governed_memory_proposal_review_gate_dry_run.py",
    "tests/test_governed_memory_proposal_review_gate_dry_run.py",
    "docs/GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN.md",
    "src/hermes_memory_fabric/governed_memory_approval_request_dry_run.py",
    "scripts/smoke_governed_memory_approval_request_dry_run.py",
    "tests/test_governed_memory_approval_request_dry_run.py",
    "docs/GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN.md",
    "src/hermes_memory_fabric/openclaw_audit_review.py",
    "src/hermes_memory_fabric/tools/openclaw_audit_review_tool.py",
    "scripts/smoke_openclaw_audit_review.py",
    "tests/test_openclaw_audit_review.py",
    "tests/test_smoke_openclaw_audit_review.py",
    "tests/tools/test_openclaw_audit_review_tool.py",
    "src/hermes_memory_fabric/closed_loop_evidence_validation.py",
    "scripts/smoke_closed_loop_evidence_validation.py",
    "tests/test_closed_loop_evidence_validation.py",
    "tests/test_smoke_closed_loop_evidence_validation.py",
    "src/hermes_memory_fabric/governed_memory_proposal_from_evidence.py",
    "scripts/smoke_governed_memory_proposal_from_evidence.py",
    "tests/test_governed_memory_proposal_from_evidence.py",
    "tests/test_smoke_governed_memory_proposal_from_evidence.py",
    "src/hermes_memory_fabric/governed_memory_proposal_review_gate.py",
    "scripts/smoke_governed_memory_proposal_review_gate.py",
    "tests/test_governed_memory_proposal_review_gate.py",
    "tests/test_smoke_governed_memory_proposal_review_gate.py",
    "src/hermes_memory_fabric/governed_approval_request_preparation.py",
    "scripts/smoke_governed_approval_request_preparation.py",
    "tests/test_governed_approval_request_preparation.py",
    "tests/test_smoke_governed_approval_request_preparation.py",
    "src/hermes_memory_fabric/governed_approval_request_dry_run_envelope.py",
    "scripts/smoke_governed_approval_request_dry_run_envelope.py",
    "tests/test_governed_approval_request_dry_run_envelope.py",
    "tests/test_smoke_governed_approval_request_dry_run_envelope.py",
    "src/hermes_memory_fabric/governed_approval_request_dry_run_envelope_validation.py",
    "scripts/smoke_governed_approval_request_dry_run_envelope_validation.py",
    "tests/test_governed_approval_request_dry_run_envelope_validation.py",
    "tests/test_smoke_governed_approval_request_dry_run_envelope_validation.py",
    "src/hermes_memory_fabric/governed_human_operator_decision_packet_dry_run.py",
    "scripts/smoke_governed_human_operator_decision_packet_dry_run.py",
    "tests/test_governed_human_operator_decision_packet_dry_run.py",
    "tests/test_smoke_governed_human_operator_decision_packet_dry_run.py",
    "src/hermes_memory_fabric/governed_human_operator_decision_packet_validation.py",
    "scripts/smoke_governed_human_operator_decision_packet_validation.py",
    "tests/test_governed_human_operator_decision_packet_validation.py",
    "tests/test_smoke_governed_human_operator_decision_packet_validation.py",
    "src/hermes_memory_fabric/governed_star_dome_chain_closure_audit.py",
    "scripts/smoke_governed_star_dome_chain_closure_audit.py",
    "tests/test_governed_star_dome_chain_closure_audit.py",
    "tests/test_smoke_governed_star_dome_chain_closure_audit.py",
    "src/hermes_memory_fabric/governed_star_dome_closure_boundary_manifest.py",
    "scripts/smoke_governed_star_dome_closure_boundary_manifest.py",
    "tests/test_governed_star_dome_closure_boundary_manifest.py",
    "tests/test_smoke_governed_star_dome_closure_boundary_manifest.py",
    "src/hermes_memory_fabric/governed_star_hub_preflight_boundary_analysis.py",
    "scripts/smoke_governed_star_hub_preflight_boundary_analysis.py",
    "tests/test_governed_star_hub_preflight_boundary_analysis.py",
    "tests/test_smoke_governed_star_hub_preflight_boundary_analysis.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_design_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_design_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_design_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_design_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_design_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_chain_closure_audit.py",
    "scripts/smoke_governed_star_hub_chain_closure_audit.py",
    "tests/test_governed_star_hub_chain_closure_audit.py",
    "tests/test_smoke_governed_star_hub_chain_closure_audit.py",
    "src/hermes_memory_fabric/governed_star_hub_closure_boundary_manifest.py",
    "scripts/smoke_governed_star_hub_closure_boundary_manifest.py",
    "tests/test_governed_star_hub_closure_boundary_manifest.py",
    "tests/test_smoke_governed_star_hub_closure_boundary_manifest.py",
    "src/hermes_memory_fabric/governed_star_law_preflight_boundary_analysis.py",
    "scripts/smoke_governed_star_law_preflight_boundary_analysis.py",
    "tests/test_governed_star_law_preflight_boundary_analysis.py",
    "tests/test_smoke_governed_star_law_preflight_boundary_analysis.py",
    "src/hermes_memory_fabric/governed_star_law_design_boundary_proposal.py",
    "scripts/smoke_governed_star_law_design_boundary_proposal.py",
    "tests/test_governed_star_law_design_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_design_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_design_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_design_boundary_review_gate.py",
    "tests/test_governed_star_law_design_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_design_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_set_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
)
SURFACE_AUDIT_FILES = (
    "src/hermes_memory_fabric/skill_fabric.py",
    "src/hermes_memory_fabric/skill_fabric_simulation.py",
    "src/hermes_memory_fabric/release_integrity_audit.py",
    "scripts/skill_fabric.py",
    "scripts/smoke_skill_fabric_simulation.py",
    "tests/test_skill_fabric.py",
    "tests/test_skill_fabric_simulation.py",
    "src/hermes_memory_fabric/governed_memory_proposal_pack_dry_run.py",
    "scripts/smoke_governed_memory_proposal_pack_dry_run.py",
    "tests/test_governed_memory_proposal_pack_dry_run.py",
    "docs/GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN.md",
    "src/hermes_memory_fabric/governed_memory_proposal_review_gate_dry_run.py",
    "scripts/smoke_governed_memory_proposal_review_gate_dry_run.py",
    "tests/test_governed_memory_proposal_review_gate_dry_run.py",
    "docs/GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN.md",
    "src/hermes_memory_fabric/governed_memory_approval_request_dry_run.py",
    "scripts/smoke_governed_memory_approval_request_dry_run.py",
    "tests/test_governed_memory_approval_request_dry_run.py",
    "docs/GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN.md",
    "src/hermes_memory_fabric/openclaw_audit_review.py",
    "src/hermes_memory_fabric/tools/openclaw_audit_review_tool.py",
    "scripts/smoke_openclaw_audit_review.py",
    "tests/test_openclaw_audit_review.py",
    "tests/test_smoke_openclaw_audit_review.py",
    "tests/tools/test_openclaw_audit_review_tool.py",
    "src/hermes_memory_fabric/closed_loop_evidence_validation.py",
    "scripts/smoke_closed_loop_evidence_validation.py",
    "tests/test_closed_loop_evidence_validation.py",
    "tests/test_smoke_closed_loop_evidence_validation.py",
    "src/hermes_memory_fabric/governed_memory_proposal_from_evidence.py",
    "scripts/smoke_governed_memory_proposal_from_evidence.py",
    "tests/test_governed_memory_proposal_from_evidence.py",
    "tests/test_smoke_governed_memory_proposal_from_evidence.py",
    "src/hermes_memory_fabric/governed_memory_proposal_review_gate.py",
    "scripts/smoke_governed_memory_proposal_review_gate.py",
    "tests/test_governed_memory_proposal_review_gate.py",
    "tests/test_smoke_governed_memory_proposal_review_gate.py",
    "src/hermes_memory_fabric/governed_approval_request_preparation.py",
    "scripts/smoke_governed_approval_request_preparation.py",
    "tests/test_governed_approval_request_preparation.py",
    "tests/test_smoke_governed_approval_request_preparation.py",
    "src/hermes_memory_fabric/governed_approval_request_dry_run_envelope.py",
    "scripts/smoke_governed_approval_request_dry_run_envelope.py",
    "tests/test_governed_approval_request_dry_run_envelope.py",
    "tests/test_smoke_governed_approval_request_dry_run_envelope.py",
    "src/hermes_memory_fabric/governed_approval_request_dry_run_envelope_validation.py",
    "scripts/smoke_governed_approval_request_dry_run_envelope_validation.py",
    "tests/test_governed_approval_request_dry_run_envelope_validation.py",
    "tests/test_smoke_governed_approval_request_dry_run_envelope_validation.py",
    "src/hermes_memory_fabric/governed_human_operator_decision_packet_dry_run.py",
    "scripts/smoke_governed_human_operator_decision_packet_dry_run.py",
    "tests/test_governed_human_operator_decision_packet_dry_run.py",
    "tests/test_smoke_governed_human_operator_decision_packet_dry_run.py",
    "src/hermes_memory_fabric/governed_human_operator_decision_packet_validation.py",
    "scripts/smoke_governed_human_operator_decision_packet_validation.py",
    "tests/test_governed_human_operator_decision_packet_validation.py",
    "tests/test_smoke_governed_human_operator_decision_packet_validation.py",
    "src/hermes_memory_fabric/governed_star_dome_chain_closure_audit.py",
    "scripts/smoke_governed_star_dome_chain_closure_audit.py",
    "tests/test_governed_star_dome_chain_closure_audit.py",
    "tests/test_smoke_governed_star_dome_chain_closure_audit.py",
    "src/hermes_memory_fabric/governed_star_dome_closure_boundary_manifest.py",
    "scripts/smoke_governed_star_dome_closure_boundary_manifest.py",
    "tests/test_governed_star_dome_closure_boundary_manifest.py",
    "tests/test_smoke_governed_star_dome_closure_boundary_manifest.py",
    "src/hermes_memory_fabric/governed_star_hub_preflight_boundary_analysis.py",
    "scripts/smoke_governed_star_hub_preflight_boundary_analysis.py",
    "tests/test_governed_star_hub_preflight_boundary_analysis.py",
    "tests/test_smoke_governed_star_hub_preflight_boundary_analysis.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_design_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_design_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_design_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_design_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_design_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_design_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "tests/test_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "scripts/smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "tests/test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "tests/test_smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_hub_chain_closure_audit.py",
    "scripts/smoke_governed_star_hub_chain_closure_audit.py",
    "tests/test_governed_star_hub_chain_closure_audit.py",
    "tests/test_smoke_governed_star_hub_chain_closure_audit.py",
    "src/hermes_memory_fabric/governed_star_hub_closure_boundary_manifest.py",
    "scripts/smoke_governed_star_hub_closure_boundary_manifest.py",
    "tests/test_governed_star_hub_closure_boundary_manifest.py",
    "tests/test_smoke_governed_star_hub_closure_boundary_manifest.py",
    "src/hermes_memory_fabric/governed_star_law_preflight_boundary_analysis.py",
    "scripts/smoke_governed_star_law_preflight_boundary_analysis.py",
    "tests/test_governed_star_law_preflight_boundary_analysis.py",
    "tests/test_smoke_governed_star_law_preflight_boundary_analysis.py",
    "src/hermes_memory_fabric/governed_star_law_design_boundary_proposal.py",
    "scripts/smoke_governed_star_law_design_boundary_proposal.py",
    "tests/test_governed_star_law_design_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_design_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_design_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_design_boundary_review_gate.py",
    "tests/test_governed_star_law_design_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_design_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_set_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_set_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_set_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_activation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_activation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_enforcement_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py",
    "src/hermes_memory_fabric/governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "scripts/smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "tests/test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "tests/test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py",
    "docs/SHARED_SKILL_FABRIC.md",
    "README.md",
)


def run_release_integrity_audit(repo_root: str | Path = ".") -> dict[str, Any]:
    """Run a local, no-network integrity audit for the v2.0-v2.58 release chain."""

    root = Path(repo_root).expanduser().resolve()
    pyproject_version = _pyproject_version(root)
    expected_tags, missing_tags = _release_tags(root)
    missing_files = [relative for relative in EXPECTED_RELEASE_FILES if not (root / relative).is_file()]
    expected_files_present = not missing_files
    provider_tools = MemoryFabricProvider().get_tool_schemas()
    provider_tools_empty = provider_tools == []
    authority = _run_authority_contract_check()
    skill_fabric = _run_skill_fabric_check()
    simulation = _run_simulation_check()
    proposal_pack = _run_governed_memory_proposal_pack_check(root)
    review_gate = _run_governed_memory_proposal_review_gate_check(root)
    approval_request = _run_governed_memory_approval_request_check(root)
    openclaw_audit_review = _run_openclaw_audit_review_check()
    openclaw_audit_review_smoke = _run_openclaw_audit_review_smoke_check(root)
    closed_loop_evidence_validation_smoke = _run_closed_loop_evidence_validation_smoke_check(root)
    governed_memory_proposal_from_evidence_smoke = (
        _run_governed_memory_proposal_from_evidence_smoke_check(root)
    )
    governed_memory_proposal_review_gate_smoke = (
        _run_governed_memory_proposal_review_gate_smoke_check(root)
    )
    governed_approval_request_preparation_smoke = (
        _run_governed_approval_request_preparation_smoke_check(root)
    )
    governed_approval_request_dry_run_envelope_smoke = (
        _run_governed_approval_request_dry_run_envelope_smoke_check(root)
    )
    governed_approval_request_dry_run_envelope_validation_smoke = (
        _run_governed_approval_request_dry_run_envelope_validation_smoke_check(root)
    )
    governed_human_operator_decision_packet_dry_run_smoke = (
        _run_governed_human_operator_decision_packet_dry_run_smoke_check(root)
    )
    governed_human_operator_decision_packet_validation_smoke = (
        _run_governed_human_operator_decision_packet_validation_smoke_check(root)
    )
    governed_star_dome_chain_closure_audit_smoke = (
        _run_governed_star_dome_chain_closure_audit_smoke_check(root)
    )
    governed_star_dome_closure_boundary_manifest_smoke = (
        _run_governed_star_dome_closure_boundary_manifest_smoke_check(root)
    )
    governed_star_hub_preflight_boundary_analysis_smoke = (
        _run_governed_star_hub_preflight_boundary_analysis_smoke_check(root)
    )
    governed_star_hub_scheduling_design_boundary_proposal_smoke = (
        _run_governed_star_hub_scheduling_design_boundary_proposal_smoke_check(root)
    )
    governed_star_hub_scheduling_design_boundary_review_gate_smoke = (
        _run_governed_star_hub_scheduling_design_boundary_review_gate_smoke_check(root)
    )
    governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke = (
        _run_governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_check(root)
    )
    governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke = (
        _run_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_check(root)
    )
    governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke = (
        _run_governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke = (
        _run_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_hub_chain_closure_audit_smoke = (
        _run_governed_star_hub_chain_closure_audit_smoke_check(root)
    )
    governed_star_hub_closure_boundary_manifest_smoke = (
        _run_governed_star_hub_closure_boundary_manifest_smoke_check(root)
    )
    governed_star_law_preflight_boundary_analysis_smoke = (
        _run_governed_star_law_preflight_boundary_analysis_smoke_check(root)
    )
    governed_star_law_design_boundary_proposal_smoke = (
        _run_governed_star_law_design_boundary_proposal_smoke_check(root)
    )
    governed_star_law_design_boundary_review_gate_smoke = (
        _run_governed_star_law_design_boundary_review_gate_smoke_check(root)
    )
    governed_star_law_candidate_rule_set_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_set_boundary_proposal_smoke_check(root)
    )
    governed_star_law_candidate_rule_set_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_set_boundary_review_gate_smoke_check(root)
    )
    governed_star_law_candidate_rule_activation_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_activation_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_activation_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_check(
            root
        )
    )
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke = (
        _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_check(
            root
        )
    )
    surface = _scan_unsafe_surfaces(root)

    no_network_surface = not any(hit["category"] == "network" for hit in surface["unsafe_source_hits"])
    no_hermes_memory_write = not any(
        hit["category"] == "hermes_memory_write" for hit in surface["unsafe_source_hits"]
    )
    no_github_write = not any(hit["category"] == "github_write" for hit in surface["unsafe_source_hits"])
    no_composio_execution = not any(
        hit["category"] == "composio_execution" for hit in surface["unsafe_source_hits"]
    )
    modifies_hermes_agent = False
    release_chain_status = "pass" if (
        pyproject_version == RELEASE_INTEGRITY_AUDIT_VERSION
        and not missing_tags
        and expected_files_present
        and provider_tools_empty
        and authority["authority_contract_safe"]
        and skill_fabric["skill_fabric_safe"]
        and simulation["simulation_status"] == "pass"
        and simulation["simulation_safe"]
        and simulation["simulation_used_network"] is False
        and simulation["simulation_used_local_archive"] is True
        and proposal_pack["proposal_pack_status"] == "ready"
        and proposal_pack["proposal_pack_safe"]
        and review_gate["review_gate_status"] == "ready"
        and review_gate["review_gate_safe"]
        and approval_request["approval_request_status"] == "ready"
        and approval_request["approval_request_safe"]
        and openclaw_audit_review["openclaw_audit_review_safe"]
        and openclaw_audit_review_smoke["openclaw_audit_review_smoke_safe"]
        and closed_loop_evidence_validation_smoke["closed_loop_evidence_validation_smoke_safe"]
        and governed_memory_proposal_from_evidence_smoke[
            "governed_memory_proposal_from_evidence_smoke_safe"
        ]
        and governed_memory_proposal_review_gate_smoke[
            "governed_memory_proposal_review_gate_smoke_safe"
        ]
        and governed_approval_request_preparation_smoke[
            "governed_approval_request_preparation_smoke_safe"
        ]
        and governed_approval_request_dry_run_envelope_smoke[
            "governed_approval_request_dry_run_envelope_smoke_safe"
        ]
        and governed_approval_request_dry_run_envelope_validation_smoke[
            "governed_approval_request_dry_run_envelope_validation_smoke_safe"
        ]
        and governed_human_operator_decision_packet_dry_run_smoke[
            "governed_human_operator_decision_packet_dry_run_smoke_safe"
        ]
        and governed_human_operator_decision_packet_validation_smoke[
            "governed_human_operator_decision_packet_validation_smoke_safe"
        ]
        and governed_star_dome_chain_closure_audit_smoke[
            "governed_star_dome_chain_closure_audit_smoke_safe"
        ]
        and governed_star_dome_closure_boundary_manifest_smoke[
            "governed_star_dome_closure_boundary_manifest_smoke_safe"
        ]
        and governed_star_hub_preflight_boundary_analysis_smoke[
            "governed_star_hub_preflight_boundary_analysis_smoke_safe"
        ]
        and governed_star_hub_scheduling_design_boundary_proposal_smoke[
            "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe"
        ]
        and governed_star_hub_scheduling_design_boundary_review_gate_smoke[
            "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe"
        ]
        and governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke[
            "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe"
        ]
        and governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke[
            "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe"
        ]
        and governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke[
            "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe"
        ]
        and governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke[
            "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe"
        ]
        and governed_star_hub_chain_closure_audit_smoke[
            "governed_star_hub_chain_closure_audit_smoke_safe"
        ]
        and governed_star_hub_closure_boundary_manifest_smoke[
            "governed_star_hub_closure_boundary_manifest_smoke_safe"
        ]
        and governed_star_law_preflight_boundary_analysis_smoke[
            "governed_star_law_preflight_boundary_analysis_smoke_safe"
        ]
        and governed_star_law_design_boundary_proposal_smoke[
            "governed_star_law_design_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_design_boundary_review_gate_smoke[
            "governed_star_law_design_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_set_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_set_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_activation_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_activation_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe"
        ]
        and governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke[
            "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe"
        ]
        and no_network_surface
        and no_hermes_memory_write
        and no_github_write
        and no_composio_execution
        and not modifies_hermes_agent
    ) else "fail"
    audit_status = release_chain_status

    return {
        "version": RELEASE_INTEGRITY_AUDIT_VERSION,
        "audit_status": audit_status,
        "pyproject_version": pyproject_version,
        "expected_tags_present": not missing_tags,
        "missing_tags": missing_tags,
        "expected_files_present": expected_files_present,
        "missing_files": missing_files,
        "provider_tools": provider_tools,
        "provider_tools_empty": provider_tools_empty,
        "provider_tool_surface_empty": provider_tools_empty,
        "authority_contract_status": authority["authority_contract_status"],
        "authority_contract_safe": authority["authority_contract_safe"],
        "skill_fabric_verify_status": skill_fabric["skill_fabric_verify_status"],
        "skill_fabric_safe": skill_fabric["skill_fabric_safe"],
        "skill_fabric_files": skill_fabric["skill_fabric_files"],
        "simulation_status": simulation["simulation_status"],
        "simulation_safe": simulation["simulation_safe"],
        "simulation_used_network": simulation["simulation_used_network"],
        "simulation_used_local_archive": simulation["simulation_used_local_archive"],
        "proposal_pack_status": proposal_pack["proposal_pack_status"],
        "proposal_pack_safe": proposal_pack["proposal_pack_safe"],
        "proposal_pack_entry_count": proposal_pack["proposal_pack_entry_count"],
        "proposal_pack_rejected_count": proposal_pack["proposal_pack_rejected_count"],
        "proposal_pack_risk_note_count": proposal_pack["proposal_pack_risk_note_count"],
        "review_gate_status": review_gate["review_gate_status"],
        "review_gate_safe": review_gate["review_gate_safe"],
        "review_gate_decision_count": review_gate["review_gate_decision_count"],
        "review_gate_approve_candidate_count": review_gate["review_gate_approve_candidate_count"],
        "review_gate_reject_locked_count": review_gate["review_gate_reject_locked_count"],
        "review_gate_risk_note_only_count": review_gate["review_gate_risk_note_only_count"],
        "approval_request_status": approval_request["approval_request_status"],
        "approval_request_safe": approval_request["approval_request_safe"],
        "approval_request_count": approval_request["approval_request_count"],
        "blocked_decision_count": approval_request["blocked_decision_count"],
        "openclaw_audit_review_status": openclaw_audit_review["openclaw_audit_review_status"],
        "openclaw_audit_review_safe": openclaw_audit_review["openclaw_audit_review_safe"],
        "openclaw_audit_review_smoke_status": openclaw_audit_review_smoke[
            "openclaw_audit_review_smoke_status"
        ],
        "openclaw_audit_review_smoke_safe": openclaw_audit_review_smoke[
            "openclaw_audit_review_smoke_safe"
        ],
        "closed_loop_evidence_validation_smoke_status": closed_loop_evidence_validation_smoke[
            "closed_loop_evidence_validation_smoke_status"
        ],
        "closed_loop_evidence_validation_smoke_safe": closed_loop_evidence_validation_smoke[
            "closed_loop_evidence_validation_smoke_safe"
        ],
        "governed_memory_proposal_from_evidence_smoke_status": (
            governed_memory_proposal_from_evidence_smoke[
                "governed_memory_proposal_from_evidence_smoke_status"
            ]
        ),
        "governed_memory_proposal_from_evidence_smoke_safe": (
            governed_memory_proposal_from_evidence_smoke[
                "governed_memory_proposal_from_evidence_smoke_safe"
            ]
        ),
        "governed_memory_proposal_review_gate_smoke_status": (
            governed_memory_proposal_review_gate_smoke[
                "governed_memory_proposal_review_gate_smoke_status"
            ]
        ),
        "governed_memory_proposal_review_gate_smoke_safe": (
            governed_memory_proposal_review_gate_smoke[
                "governed_memory_proposal_review_gate_smoke_safe"
            ]
        ),
        "governed_approval_request_preparation_smoke_status": (
            governed_approval_request_preparation_smoke[
                "governed_approval_request_preparation_smoke_status"
            ]
        ),
        "governed_approval_request_preparation_smoke_safe": (
            governed_approval_request_preparation_smoke[
                "governed_approval_request_preparation_smoke_safe"
            ]
        ),
        "governed_approval_request_dry_run_envelope_smoke_status": (
            governed_approval_request_dry_run_envelope_smoke[
                "governed_approval_request_dry_run_envelope_smoke_status"
            ]
        ),
        "governed_approval_request_dry_run_envelope_smoke_safe": (
            governed_approval_request_dry_run_envelope_smoke[
                "governed_approval_request_dry_run_envelope_smoke_safe"
            ]
        ),
        "governed_approval_request_dry_run_envelope_validation_smoke_status": (
            governed_approval_request_dry_run_envelope_validation_smoke[
                "governed_approval_request_dry_run_envelope_validation_smoke_status"
            ]
        ),
        "governed_approval_request_dry_run_envelope_validation_smoke_safe": (
            governed_approval_request_dry_run_envelope_validation_smoke[
                "governed_approval_request_dry_run_envelope_validation_smoke_safe"
            ]
        ),
        "governed_human_operator_decision_packet_dry_run_smoke_status": (
            governed_human_operator_decision_packet_dry_run_smoke[
                "governed_human_operator_decision_packet_dry_run_smoke_status"
            ]
        ),
        "governed_human_operator_decision_packet_dry_run_smoke_safe": (
            governed_human_operator_decision_packet_dry_run_smoke[
                "governed_human_operator_decision_packet_dry_run_smoke_safe"
            ]
        ),
        "governed_human_operator_decision_packet_validation_smoke_status": (
            governed_human_operator_decision_packet_validation_smoke[
                "governed_human_operator_decision_packet_validation_smoke_status"
            ]
        ),
        "governed_human_operator_decision_packet_validation_smoke_safe": (
            governed_human_operator_decision_packet_validation_smoke[
                "governed_human_operator_decision_packet_validation_smoke_safe"
            ]
        ),
        "governed_star_dome_chain_closure_audit_smoke_status": (
            governed_star_dome_chain_closure_audit_smoke[
                "governed_star_dome_chain_closure_audit_smoke_status"
            ]
        ),
        "governed_star_dome_chain_closure_audit_smoke_safe": (
            governed_star_dome_chain_closure_audit_smoke[
                "governed_star_dome_chain_closure_audit_smoke_safe"
            ]
        ),
        "governed_star_dome_closure_boundary_manifest_smoke_status": (
            governed_star_dome_closure_boundary_manifest_smoke[
                "governed_star_dome_closure_boundary_manifest_smoke_status"
            ]
        ),
        "governed_star_dome_closure_boundary_manifest_smoke_safe": (
            governed_star_dome_closure_boundary_manifest_smoke[
                "governed_star_dome_closure_boundary_manifest_smoke_safe"
            ]
        ),
        "governed_star_hub_preflight_boundary_analysis_smoke_status": (
            governed_star_hub_preflight_boundary_analysis_smoke[
                "governed_star_hub_preflight_boundary_analysis_smoke_status"
            ]
        ),
        "governed_star_hub_preflight_boundary_analysis_smoke_safe": (
            governed_star_hub_preflight_boundary_analysis_smoke[
                "governed_star_hub_preflight_boundary_analysis_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_design_boundary_proposal_smoke_status": (
            governed_star_hub_scheduling_design_boundary_proposal_smoke[
                "governed_star_hub_scheduling_design_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe": (
            governed_star_hub_scheduling_design_boundary_proposal_smoke[
                "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_design_boundary_review_gate_smoke_status": (
            governed_star_hub_scheduling_design_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_design_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe": (
            governed_star_hub_scheduling_design_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_status": (
            governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke[
                "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe": (
            governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke[
                "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_status": (
            governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe": (
            governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_status": (
            governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke[
                "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe": (
            governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke[
                "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_status": (
            governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe": (
            governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke[
                "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_hub_chain_closure_audit_smoke_status": (
            governed_star_hub_chain_closure_audit_smoke[
                "governed_star_hub_chain_closure_audit_smoke_status"
            ]
        ),
        "governed_star_hub_chain_closure_audit_smoke_safe": (
            governed_star_hub_chain_closure_audit_smoke[
                "governed_star_hub_chain_closure_audit_smoke_safe"
            ]
        ),
        "governed_star_hub_closure_boundary_manifest_smoke_status": (
            governed_star_hub_closure_boundary_manifest_smoke[
                "governed_star_hub_closure_boundary_manifest_smoke_status"
            ]
        ),
        "governed_star_hub_closure_boundary_manifest_smoke_safe": (
            governed_star_hub_closure_boundary_manifest_smoke[
                "governed_star_hub_closure_boundary_manifest_smoke_safe"
            ]
        ),
        "governed_star_law_preflight_boundary_analysis_smoke_status": (
            governed_star_law_preflight_boundary_analysis_smoke[
                "governed_star_law_preflight_boundary_analysis_smoke_status"
            ]
        ),
        "governed_star_law_preflight_boundary_analysis_smoke_safe": (
            governed_star_law_preflight_boundary_analysis_smoke[
                "governed_star_law_preflight_boundary_analysis_smoke_safe"
            ]
        ),
        "governed_star_law_design_boundary_proposal_smoke_status": (
            governed_star_law_design_boundary_proposal_smoke[
                "governed_star_law_design_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_design_boundary_proposal_smoke_safe": (
            governed_star_law_design_boundary_proposal_smoke[
                "governed_star_law_design_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_design_boundary_review_gate_smoke_status": (
            governed_star_law_design_boundary_review_gate_smoke[
                "governed_star_law_design_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_design_boundary_review_gate_smoke_safe": (
            governed_star_law_design_boundary_review_gate_smoke[
                "governed_star_law_design_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_set_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_set_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_set_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_set_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_set_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_set_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_activation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_activation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_activation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_activation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_status": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_status"
            ]
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe": (
            governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke[
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe"
            ]
        ),
        "unsafe_source_hits": surface["unsafe_source_hits"],
        "allowed_documentation_hits": surface["allowed_documentation_hits"],
        "no_network_surface": no_network_surface,
        "no_hermes_memory_write": no_hermes_memory_write,
        "no_github_write": no_github_write,
        "no_composio_execution": no_composio_execution,
        "modifies_hermes_agent": modifies_hermes_agent,
        "release_chain_status": release_chain_status,
        "safety_summary": {
            "local_only": True,
            "uses_network": False,
            "uses_github_api": False,
            "writes_hermes_memory": False,
            "exposes_provider_tools": False,
            "checks": {
                "version": pyproject_version == RELEASE_INTEGRITY_AUDIT_VERSION,
                "tags": not missing_tags,
                "files": expected_files_present,
                "provider_tools_empty": provider_tools_empty,
                "authority_contract_safe": authority["authority_contract_safe"],
                "skill_fabric_safe": skill_fabric["skill_fabric_safe"],
                "simulation_safe": simulation["simulation_safe"],
                "proposal_pack_safe": proposal_pack["proposal_pack_safe"],
                "review_gate_safe": review_gate["review_gate_safe"],
                "approval_request_safe": approval_request["approval_request_safe"],
                "openclaw_audit_review_safe": openclaw_audit_review["openclaw_audit_review_safe"],
                "openclaw_audit_review_smoke_safe": openclaw_audit_review_smoke[
                    "openclaw_audit_review_smoke_safe"
                ],
                "closed_loop_evidence_validation_smoke_safe": closed_loop_evidence_validation_smoke[
                    "closed_loop_evidence_validation_smoke_safe"
                ],
                "governed_memory_proposal_from_evidence_smoke_safe": (
                    governed_memory_proposal_from_evidence_smoke[
                        "governed_memory_proposal_from_evidence_smoke_safe"
                    ]
                ),
                "governed_memory_proposal_review_gate_smoke_safe": (
                    governed_memory_proposal_review_gate_smoke[
                        "governed_memory_proposal_review_gate_smoke_safe"
                    ]
                ),
                "governed_approval_request_preparation_smoke_safe": (
                    governed_approval_request_preparation_smoke[
                        "governed_approval_request_preparation_smoke_safe"
                    ]
                ),
                "governed_approval_request_dry_run_envelope_smoke_safe": (
                    governed_approval_request_dry_run_envelope_smoke[
                        "governed_approval_request_dry_run_envelope_smoke_safe"
                    ]
                ),
                "governed_approval_request_dry_run_envelope_validation_smoke_safe": (
                    governed_approval_request_dry_run_envelope_validation_smoke[
                        "governed_approval_request_dry_run_envelope_validation_smoke_safe"
                    ]
                ),
                "governed_human_operator_decision_packet_dry_run_smoke_safe": (
                    governed_human_operator_decision_packet_dry_run_smoke[
                        "governed_human_operator_decision_packet_dry_run_smoke_safe"
                    ]
                ),
                "governed_human_operator_decision_packet_validation_smoke_safe": (
                    governed_human_operator_decision_packet_validation_smoke[
                        "governed_human_operator_decision_packet_validation_smoke_safe"
                    ]
                ),
                "governed_star_dome_chain_closure_audit_smoke_safe": (
                    governed_star_dome_chain_closure_audit_smoke[
                        "governed_star_dome_chain_closure_audit_smoke_safe"
                    ]
                ),
                "governed_star_dome_closure_boundary_manifest_smoke_safe": (
                    governed_star_dome_closure_boundary_manifest_smoke[
                        "governed_star_dome_closure_boundary_manifest_smoke_safe"
                    ]
                ),
                "governed_star_hub_preflight_boundary_analysis_smoke_safe": (
                    governed_star_hub_preflight_boundary_analysis_smoke[
                        "governed_star_hub_preflight_boundary_analysis_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe": (
                    governed_star_hub_scheduling_design_boundary_proposal_smoke[
                        "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe": (
                    governed_star_hub_scheduling_design_boundary_review_gate_smoke[
                        "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe": (
                    governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke[
                        "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe": (
                    governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke[
                        "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe": (
                    governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke[
                        "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe": (
                    governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke[
                        "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_hub_chain_closure_audit_smoke_safe": (
                    governed_star_hub_chain_closure_audit_smoke[
                        "governed_star_hub_chain_closure_audit_smoke_safe"
                    ]
                ),
                "governed_star_hub_closure_boundary_manifest_smoke_safe": (
                    governed_star_hub_closure_boundary_manifest_smoke[
                        "governed_star_hub_closure_boundary_manifest_smoke_safe"
                    ]
                ),
                "governed_star_law_preflight_boundary_analysis_smoke_safe": (
                    governed_star_law_preflight_boundary_analysis_smoke[
                        "governed_star_law_preflight_boundary_analysis_smoke_safe"
                    ]
                ),
                "governed_star_law_design_boundary_proposal_smoke_safe": (
                    governed_star_law_design_boundary_proposal_smoke[
                        "governed_star_law_design_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_design_boundary_review_gate_smoke_safe": (
                    governed_star_law_design_boundary_review_gate_smoke[
                        "governed_star_law_design_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_set_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_set_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_activation_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_activation_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe"
                    ]
                ),
                "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe": (
                    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke[
                        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe"
                    ]
                ),
                "surface_scan_safe": surface["unsafe_source_hits"] == [],
            },
        },
    }



def _run_openclaw_audit_review_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        result = build_openclaw_audit_review(tmp)

    safe = (
        result.get("status") == "missing_audit_log"
        and result.get("read_only") is True
        and result.get("would_mutate_memory") is False
        and result.get("invokes_openclaw") is False
        and result.get("writes_files") is False
        and result.get("entries") == []
    )
    return {
        "openclaw_audit_review_status": str(result.get("status") or "fail"),
        "openclaw_audit_review_safe": safe,
    }


def _run_openclaw_audit_review_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "smoke_openclaw_audit_review.py")],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "openclaw_audit_review=passed\n"
        and completed.stderr == ""
    )
    return {
        "openclaw_audit_review_smoke_status": "pass" if safe else "fail",
        "openclaw_audit_review_smoke_safe": safe,
    }


def _run_closed_loop_evidence_validation_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "smoke_closed_loop_evidence_validation.py")],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "closed_loop_evidence_validation=passed\n"
        and completed.stderr == ""
    )
    return {
        "closed_loop_evidence_validation_smoke_status": "pass" if safe else "fail",
        "closed_loop_evidence_validation_smoke_safe": safe,
    }


def _run_governed_memory_proposal_from_evidence_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "smoke_governed_memory_proposal_from_evidence.py")],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_memory_proposal_from_evidence=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_memory_proposal_from_evidence_smoke_status": "pass" if safe else "fail",
        "governed_memory_proposal_from_evidence_smoke_safe": safe,
    }


def _run_governed_memory_proposal_review_gate_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "smoke_governed_memory_proposal_review_gate.py")],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_memory_proposal_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_memory_proposal_review_gate_smoke_status": "pass" if safe else "fail",
        "governed_memory_proposal_review_gate_smoke_safe": safe,
    }


def _run_governed_approval_request_preparation_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "smoke_governed_approval_request_preparation.py")],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_approval_request_preparation=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_approval_request_preparation_smoke_status": "pass" if safe else "fail",
        "governed_approval_request_preparation_smoke_safe": safe,
    }


def _run_governed_approval_request_dry_run_envelope_smoke_check(root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "smoke_governed_approval_request_dry_run_envelope.py"),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_approval_request_dry_run_envelope=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_approval_request_dry_run_envelope_smoke_status": "pass" if safe else "fail",
        "governed_approval_request_dry_run_envelope_smoke_safe": safe,
    }


def _run_governed_approval_request_dry_run_envelope_validation_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_approval_request_dry_run_envelope_validation.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_approval_request_dry_run_envelope_validation=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_approval_request_dry_run_envelope_validation_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_approval_request_dry_run_envelope_validation_smoke_safe": safe,
    }


def _run_governed_human_operator_decision_packet_dry_run_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_human_operator_decision_packet_dry_run.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_human_operator_decision_packet_dry_run=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_human_operator_decision_packet_dry_run_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_human_operator_decision_packet_dry_run_smoke_safe": safe,
    }


def _run_governed_human_operator_decision_packet_validation_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_human_operator_decision_packet_validation.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_human_operator_decision_packet_validation=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_human_operator_decision_packet_validation_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_human_operator_decision_packet_validation_smoke_safe": safe,
    }


def _run_governed_star_dome_chain_closure_audit_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "smoke_governed_star_dome_chain_closure_audit.py"),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_dome_chain_closure_audit=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_dome_chain_closure_audit_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_dome_chain_closure_audit_smoke_safe": safe,
    }


def _run_governed_star_dome_closure_boundary_manifest_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "smoke_governed_star_dome_closure_boundary_manifest.py"),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_dome_closure_boundary_manifest=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_dome_closure_boundary_manifest_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_dome_closure_boundary_manifest_smoke_safe": safe,
    }


def _run_governed_star_hub_preflight_boundary_analysis_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "smoke_governed_star_hub_preflight_boundary_analysis.py"),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_hub_preflight_boundary_analysis=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_preflight_boundary_analysis_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_preflight_boundary_analysis_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_design_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_design_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_hub_scheduling_design_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_design_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_design_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_design_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_design_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_hub_scheduling_design_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_design_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_dry_run_plan_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_hub_scheduling_dry_run_plan_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_dry_run_execution_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_hub_scheduling_dry_run_execution_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_hub_chain_closure_audit_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_chain_closure_audit.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_hub_chain_closure_audit=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_chain_closure_audit_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_chain_closure_audit_smoke_safe": safe,
    }


def _run_governed_star_hub_closure_boundary_manifest_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_hub_closure_boundary_manifest.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_hub_closure_boundary_manifest=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_hub_closure_boundary_manifest_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_hub_closure_boundary_manifest_smoke_safe": safe,
    }


def _run_governed_star_law_preflight_boundary_analysis_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_preflight_boundary_analysis.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_preflight_boundary_analysis=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_preflight_boundary_analysis_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_preflight_boundary_analysis_smoke_safe": safe,
    }


def _run_governed_star_law_design_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_design_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout == "governed_star_law_design_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_design_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_design_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_design_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_design_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_design_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_design_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_design_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_set_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_set_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_set_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_set_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_set_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_set_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_set_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_activation_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_activation_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_activation_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_activation_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_activation_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_enforcement_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_enforcement_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_enforcement_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_observation_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_observation_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_observation_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_observation_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_proposal_smoke_safe": safe,
    }


def _run_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_check(
    root: Path,
) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(
                root
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate.py"
            ),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    safe = (
        completed.returncode == 0
        and completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate=passed\n"
        and completed.stderr == ""
    )
    return {
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_status": (
            "pass" if safe else "fail"
        ),
        "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_smoke_safe": safe,
    }


def release_integrity_audit_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a release integrity audit report deterministically."""

    return json.dumps(dict(result), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _pyproject_version(root: Path) -> str | None:
    path = root / "pyproject.toml"
    if not path.is_file():
        return None
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    project = data.get("project", {})
    return str(project.get("version")) if isinstance(project, dict) and project.get("version") else None


def _release_tags(root: Path) -> tuple[dict[str, bool], list[str]]:
    tags = set(_git_tags(root))
    expected = {tag: tag in tags for tag in EXPECTED_RELEASE_TAGS}
    missing = [tag for tag in EXPECTED_RELEASE_TAGS if tag not in tags]
    return expected, missing


def _git_tags(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "tag", "--list", "v2.*"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return []
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _run_authority_contract_check() -> dict[str, Any]:
    source = _valid_token_issuance_source()
    result = run_memory_token_authority_boundary_contract_dry_run(source)
    expected_false = {
        key: value for key, value in NO_TOKEN_NO_WRITE_FLAGS.items() if isinstance(value, bool)
    }
    safe = (
        result.get("authority_contract_status") == "ready"
        and all(result.get(key) is expected for key, expected in expected_false.items())
        and result.get("approval_token_id") is None
        and result.get("approval_token_value") is None
        and result.get("provider_tools") == []
    )
    return {
        "authority_contract_status": str(result.get("authority_contract_status") or "fail"),
        "authority_contract_safe": safe,
    }


def _valid_token_issuance_source() -> dict[str, Any]:
    source: dict[str, Any] = {key: None for key in SOURCE_REQUIRED_KEYS}
    source.update(
        {
            "version": "1.9.0",
            "dry_run": True,
            "token_issuance_status": "ready",
            "token_draft_id": "release-integrity-token-draft",
            "token_intent_id": "release-integrity-token-intent",
            "required_next_step": "manual_token_issuance_review_required_no_token_created",
            "safety_summary": {},
            **NO_TOKEN_NO_WRITE_FLAGS,
        }
    )
    return source


def _run_skill_fabric_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="release-integrity-skill-fabric-") as directory:
        temp_root = Path(directory).resolve()
        paths = SkillFabricPaths(temp_root / "skill-fabric")
        initialize_skill_fabric(paths)
        verification = verify_skill_fabric(paths)
        files = _relative_files(paths.root, paths.root)
        safe = (
            verification.get("status") == "pass"
            and paths.root.resolve().is_relative_to(temp_root)
            and paths.registry_path.is_file()
            and paths.lock_path.is_file()
            and paths.ledger_path.is_file()
        )
        return {
            "skill_fabric_verify_status": str(verification.get("status") or "fail"),
            "skill_fabric_safe": safe,
            "skill_fabric_files": files,
        }


def _run_simulation_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="release-integrity-simulation-") as directory:
        result = run_skill_fabric_github_archive_simulation(Path(directory))
    return {
        "simulation_status": str(result.get("simulation_status") or "fail"),
        "simulation_safe": (
            result.get("simulation_status") == "pass"
            and result.get("used_network") is False
            and result.get("used_local_archive") is True
            and result.get("writes_hermes_memory") is False
            and result.get("modifies_hermes_agent") is False
            and result.get("executes_composio") is False
            and result.get("performs_github_write") is False
            and result.get("provider_tools") == []
        ),
        "simulation_used_network": result.get("used_network") is True,
        "simulation_used_local_archive": result.get("used_local_archive") is True,
    }


def _run_governed_memory_proposal_pack_check(root: Path) -> dict[str, Any]:
    proposal_path = root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = build_governed_memory_proposal_pack_dry_run(proposal_path)
    safe = (
        result.get("pack_status") == "ready"
        and result.get("entry_count", 0) > 0
        and result.get("proposed_count", 0) > 0
        and result.get("rejected_count", 0) > 0
        and result.get("risk_note_count", 0) > 0
        and result.get("writes_memory") is False
        and result.get("writes_graph") is False
        and result.get("writes_operation_ledger") is False
        and result.get("writes_config") is False
        and result.get("writes_sqlite") is False
        and result.get("invokes_real_executor") is False
        and result.get("provider_tools") == []
        and result.get("creates_real_memory_write_proposal") is False
        and result.get("creates_real_operation_ledger_entry") is False
        and result.get("modifies_hermes_agent") is False
        and result.get("no_network_surface") is True
    )
    return {
        "proposal_pack_status": str(result.get("pack_status") or "blocked"),
        "proposal_pack_safe": safe,
        "proposal_pack_entry_count": int(result.get("entry_count") or 0),
        "proposal_pack_rejected_count": int(result.get("rejected_count") or 0),
        "proposal_pack_risk_note_count": int(result.get("risk_note_count") or 0),
    }


def _run_governed_memory_proposal_review_gate_check(root: Path) -> dict[str, Any]:
    proposal_path = root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = run_governed_memory_proposal_review_gate_dry_run(proposal_path)
    safe = (
        result.get("review_gate_status") == "ready"
        and result.get("pack_version") == "2.4.0"
        and result.get("pack_status") == "ready"
        and result.get("entry_count", 0) > 0
        and result.get("decision_count") == result.get("entry_count")
        and result.get("approve_candidate_count", 0) > 0
        and result.get("reject_locked_count", 0) > 0
        and result.get("risk_note_only_count", 0) > 0
        and result.get("defer_for_human_review_count") == 0
        and result.get("writes_memory") is False
        and result.get("writes_graph") is False
        and result.get("writes_operation_ledger") is False
        and result.get("writes_config") is False
        and result.get("writes_sqlite") is False
        and result.get("invokes_real_executor") is False
        and result.get("provider_tools") == []
        and result.get("creates_real_memory_write_proposal") is False
        and result.get("creates_real_operation_ledger_entry") is False
        and result.get("issues_approval_token") is False
        and result.get("approval_token_issued") is False
        and result.get("approval_token_value") is None
        and result.get("creates_usable_token") is False
        and result.get("modifies_hermes_agent") is False
        and result.get("no_network_surface") is True
    )
    return {
        "review_gate_status": str(result.get("review_gate_status") or "blocked"),
        "review_gate_safe": safe,
        "review_gate_decision_count": int(result.get("decision_count") or 0),
        "review_gate_approve_candidate_count": int(result.get("approve_candidate_count") or 0),
        "review_gate_reject_locked_count": int(result.get("reject_locked_count") or 0),
        "review_gate_risk_note_only_count": int(result.get("risk_note_only_count") or 0),
    }


def _run_governed_memory_approval_request_check(root: Path) -> dict[str, Any]:
    proposal_path = root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = build_governed_memory_approval_request_dry_run(proposal_path)
    safe = (
        result.get("approval_request_status") == "ready"
        and result.get("review_gate_version") == "2.5.0"
        and result.get("review_gate_status") == "ready"
        and result.get("approval_request_count") == result.get("approve_candidate_count")
        and result.get("approval_request_count") == 15
        and result.get("blocked_decision_count") == 3
        and result.get("writes_memory") is False
        and result.get("writes_graph") is False
        and result.get("writes_operation_ledger") is False
        and result.get("writes_config") is False
        and result.get("writes_sqlite") is False
        and result.get("invokes_real_executor") is False
        and result.get("provider_tools") == []
        and result.get("creates_real_memory_write_proposal") is False
        and result.get("creates_real_operation_ledger_entry") is False
        and result.get("issues_approval_token") is False
        and result.get("approval_token_issued") is False
        and result.get("approval_token_value") is None
        and result.get("creates_usable_token") is False
        and result.get("modifies_hermes_agent") is False
        and result.get("no_network_surface") is True
    )
    return {
        "approval_request_status": str(result.get("approval_request_status") or "blocked"),
        "approval_request_safe": safe,
        "approval_request_count": int(result.get("approval_request_count") or 0),
        "blocked_decision_count": int(result.get("blocked_decision_count") or 0),
    }


def _scan_unsafe_surfaces(root: Path) -> dict[str, list[dict[str, Any]]]:
    unsafe_source_hits: list[dict[str, Any]] = []
    allowed_documentation_hits: list[dict[str, Any]] = []
    for relative in SURFACE_AUDIT_FILES:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line, category, pattern_name in _unsafe_line_hits(text):
            hit = {
                "file": relative,
                "line": line_number,
                "pattern": pattern_name,
                "category": category,
                "text": line.strip(),
            }
            if path.suffix == ".md":
                allowed_documentation_hits.append(hit)
            else:
                unsafe_source_hits.append(hit)
    return {
        "unsafe_source_hits": unsafe_source_hits,
        "allowed_documentation_hits": allowed_documentation_hits,
    }


def _unsafe_line_hits(text: str) -> Iterable[tuple[int, str, str, str]]:
    expressions = _unsafe_expressions()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern_name, category, expression in expressions:
            if expression.search(line):
                yield line_number, line, category, pattern_name


def _unsafe_expressions() -> tuple[tuple[str, str, re.Pattern[str]], ...]:
    return (
        ("network_client_a", "network", re.compile(re.escape("url" + "open"))),
        ("network_client_b", "network", re.compile(re.escape("urllib" + "." + "request"))),
        (
            "network_client_c",
            "network",
            re.compile(
                r"^\s*(import\s+"
                + re.escape("requ" + "ests")
                + r"\b|from\s+"
                + re.escape("requ" + "ests")
                + r"\b)"
            ),
        ),
        ("shell_github_cli", "github_write", re.compile(r"subprocess.*\b" + re.escape("g" + "h") + r"\b")),
        ("github_api_cli", "github_write", re.compile(re.escape("g" + "h api"))),
        ("github_push", "github_write", re.compile(re.escape("git " + "push"))),
        ("github_merge", "github_write", re.compile(re.escape("git " + "merge"))),
        ("external_app_execution", "composio_execution", re.compile(re.escape("composio " + "execute"))),
        (
            "durable_memory_proposal",
            "hermes_memory_write",
            re.compile(re.escape("create_" + "memory_write_proposal")),
        ),
        ("hermes_home_write", "hermes_memory_write", re.compile(re.escape("HERMES" + "_HOME " + "writes"))),
        ("hermes_home_path_write", "hermes_memory_write", re.compile(re.escape("~/" + "." + "hermes writes"))),
    )


def _relative_files(root: Path, base: Path) -> list[str]:
    if not root.exists():
        return []
    return [
        path.relative_to(base).as_posix()
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file())
    ]


__all__ = [
    "RELEASE_INTEGRITY_AUDIT_VERSION",
    "run_release_integrity_audit",
    "release_integrity_audit_to_json",
]
