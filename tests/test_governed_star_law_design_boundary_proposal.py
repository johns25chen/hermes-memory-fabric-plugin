from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_hub_chain_closure_audit import (
    build_governed_star_hub_chain_closure_audit,
)
from hermes_memory_fabric.governed_star_hub_closure_boundary_manifest import (
    build_governed_star_hub_closure_boundary_manifest,
)
from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_law_design_boundary_proposal import (
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_law_design_boundary_proposal,
    governed_star_law_design_boundary_proposal_to_json,
)
from hermes_memory_fabric.governed_star_law_preflight_boundary_analysis import (
    build_governed_star_law_preflight_boundary_analysis,
)
from tests.test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    _valid_proposal_report,
)


def _valid_preflight_report() -> dict[str, object]:
    review_gate = build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
        _valid_proposal_report()
    )
    audit = build_governed_star_hub_chain_closure_audit(review_gate)
    manifest = build_governed_star_hub_closure_boundary_manifest(audit)
    return build_governed_star_law_preflight_boundary_analysis(manifest)


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_design_boundary_proposal(
        report or _valid_preflight_report()
    )


def test_valid_preflight_report_creates_star_law_design_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.29.0"
    assert result["status"] == "star_law_design_boundary_proposal_ready"
    assert result["source_preflight_version"] == "2.28.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["proposal_only"] is True
    assert result["design_boundary_proposal_only"] is True
    assert result["star_law_design_boundary_proposal_only"] is True
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposal = result["star_law_design_boundary_proposal"]
    assert (
        proposal["proposal_status"]
        == "star_law_design_boundary_proposed_for_human_review_only"
    )
    assert proposal["boundary_type"] == "star_law_design_boundary_proposal"
    assert proposal["source_star_law_preflight_valid"] is True
    assert proposal["star_law_design_boundary_proposed"] is True
    assert (
        proposal["star_law_design_boundary_review_gate_ready_for_human_review_only"]
        is True
    )


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_28_0():
    result = _build()

    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert (
        result["star_law_design_boundary_proposal"]["proposed_chain_versions"]
        == PROPOSED_CHAIN_VERSIONS
    )


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_28_0():
    result = _build()

    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["star_law_design_boundary_proposal"][
            "proposed_star_hub_chain_versions"
        ]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_preflight_report_blocks_proposal():
    report = _valid_preflight_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["star_law_design_boundary_proposal"][
        "star_law_design_boundary_proposed"
    ] is False
    assert result["star_law_design_boundary_proposal"][
        "star_law_design_boundary_review_gate_ready_for_human_review_only"
    ] is False
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


def test_unsafe_authorization_flag_blocks_proposal():
    report = _valid_preflight_report()
    report["authorization_granted"] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "self_executing_policy_created",
        "self_executing_policy_active",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "mature_star_law_claimed",
        "civilization_core_complete_claimed",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "handoff_performed",
        "star_hub_scheduling_authorized",
        "scheduling_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "memory_write_authorized",
        "durable_memory_write_authorized",
        "would_write_durable_memory",
        "memory_graph_mutation_authorized",
        "would_mutate_memory_graph",
        "operation_ledger_creation_authorized",
        "would_create_operation_ledger_entry",
        "openclaw_execution_authorized",
        "approval_granted",
        "approval_authorized",
        "approval_request_authorized",
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
        "human_decision_recorded",
        "real_human_decision_recorded",
    ],
)
def test_unsafe_top_level_claim_blocks_proposal(field: str):
    report = _valid_preflight_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "self_executing_policy_created",
        "self_executing_policy_active",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "mature_star_law_claimed",
        "civilization_core_complete_claimed",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "handoff_performed",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "durable_memory_write_authorized",
        "memory_graph_mutation_authorized",
        "operation_ledger_creation_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "approval_granted",
        "real_human_decision_recorded",
    ],
)
def test_unsafe_preflight_boundary_claim_blocks_proposal(field: str):
    report = _valid_preflight_report()
    boundary = report["star_law_preflight_boundary"]
    assert isinstance(boundary, dict)
    boundary[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_analyzed_chain_versions_blocks_proposal():
    report = _valid_preflight_report()
    report["analyzed_chain_versions"] = ["v2.28.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_analyzed_star_hub_chain_versions_blocks_proposal():
    report = _valid_preflight_report()
    report["analyzed_star_hub_chain_versions"] = ["v2.28.0"]

    assert _build(report)["status"] == "blocked"


def test_proposed_design_boundaries_are_proposal_only_and_non_authorizing():
    result = _build()
    boundaries = result["proposed_star_law_design_boundaries"]

    assert isinstance(boundaries, dict)
    assert set(boundaries) == {
        "candidate_rule_taxonomy_boundary",
        "human_operator_control_boundary",
        "non_authorization_boundary",
        "evidence_lineage_boundary",
        "memory_write_boundary",
        "memory_graph_boundary",
        "operation_ledger_boundary",
        "openclaw_boundary",
        "approval_boundary",
        "auditability_boundary",
        "future_review_gate_boundary",
    }
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
    serialized = json.dumps(boundaries, ensure_ascii=True, sort_keys=True)
    for forbidden_claim in [
        "rules are created",
        "rules are active",
        "rules are enforced",
        "self-executing policy active",
        "autonomous governance is created",
        "autonomous execution is authorized",
        "durable memory writing is allowed",
        "memory graph mutation is allowed",
        "operation-ledger creation is allowed",
        "openclaw execution is allowed",
        "approval is granted",
        "real human decision has been recorded",
        "civilization core is complete",
    ]:
        assert forbidden_claim not in serialized.lower()
    for boundary in boundaries.values():
        for key, value in boundary.items():
            if key not in {"proposal_only", "review_gate_ready_for_human_review_only"}:
                assert value is not True


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_preflight_report()
    report["approval_phrase"] = "approve-hidden-star-law-design"
    report["nested"] = {
        "stdout_tail": "hidden terminal output",
        "api_key": "sk-hidden",
        "password": "hidden-password",
        "token": "hidden-token",
    }

    serialized = governed_star_law_design_boundary_proposal_to_json(_build(report))

    assert "Sensitive fields were omitted" in serialized
    for forbidden in [
        "approval_phrase",
        "stdout_tail",
        "stdout",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
        "approve-hidden-star-law-design",
        "hidden terminal output",
        "sk-hidden",
        "hidden-password",
        "hidden-token",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field",
    [
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "self_executing_policy_created",
        "self_executing_policy_active",
        "enters_star_law_layer",
        "mature_star_law_claimed",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "dry_run_performed",
        "dry_run_executed",
        "scheduling_performed",
        "would_write_durable_memory",
        "openclaw_execution_authorized",
        "approval_granted",
        "human_decision_recorded",
    ],
)
def test_proposal_preserves_top_level_non_authorization_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize(
    "field",
    [
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "enters_star_law_layer",
        "civilization_core_complete_claimed",
        "durable_memory_write_authorized",
        "memory_graph_mutation_authorized",
        "operation_ledger_creation_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "real_human_decision_recorded",
    ],
)
def test_star_law_design_boundary_proposal_preserves_non_authorization_flags(
    field: str,
):
    assert _build()["star_law_design_boundary_proposal"][field] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law design boundary proposal only, not rule activation and not rule enforcement"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law preflight boundary analysis complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law preflight boundary analysis -> Star-Law design boundary proposal"
    )


def test_next_allowed_step_is_v2_30_star_law_design_boundary_review_gate():
    assert _build()["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        _build()["star_law_design_boundary_proposal"]["next_allowed_step"]
        == READY_NEXT_ALLOWED_STEP
    )


READY_NEXT_ALLOWED_STEP = "v2.30.0 Star-Law design boundary review gate"
