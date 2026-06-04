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
from hermes_memory_fabric.governed_star_law_preflight_boundary_analysis import (
    ANALYZED_CHAIN_VERSIONS,
    ANALYZED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_law_preflight_boundary_analysis,
    governed_star_law_preflight_boundary_analysis_to_json,
)
from tests.test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    _valid_proposal_report,
)


def _valid_manifest_report() -> dict[str, object]:
    review_gate = build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
        _valid_proposal_report()
    )
    audit = build_governed_star_hub_chain_closure_audit(review_gate)
    return build_governed_star_hub_closure_boundary_manifest(audit)


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_preflight_boundary_analysis(
        report or _valid_manifest_report()
    )


def test_valid_manifest_report_creates_star_law_preflight_boundary_analysis_ready():
    result = _build()

    assert result["version"] == "2.28.0"
    assert result["status"] == "star_law_preflight_boundary_analysis_ready"
    assert result["source_manifest_version"] == "2.27.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["preflight_analysis_only"] is True
    assert result["star_law_preflight_boundary_analysis_only"] is True
    assert all(check["passed"] is True for check in result["preflight_checks"])
    assert result["blocking_reasons"] == []
    boundary = result["star_law_preflight_boundary"]
    assert (
        boundary["preflight_status"]
        == "star_law_preflight_boundary_analyzed_for_human_review_only"
    )
    assert boundary["boundary_type"] == "star_law_preflight_boundary_analysis"
    assert boundary["source_star_hub_boundary_manifest_valid"] is True
    assert (
        boundary["star_law_design_boundary_proposal_ready_for_human_review_only"]
        is True
    )


def test_analyzed_chain_versions_exactly_match_v2_9_0_through_v2_27_0():
    result = _build()

    assert result["analyzed_chain_versions"] == ANALYZED_CHAIN_VERSIONS
    assert (
        result["star_law_preflight_boundary"]["analyzed_chain_versions"]
        == ANALYZED_CHAIN_VERSIONS
    )


def test_analyzed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_27_0():
    result = _build()

    assert result["analyzed_star_hub_chain_versions"] == ANALYZED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["star_law_preflight_boundary"]["analyzed_star_hub_chain_versions"]
        == ANALYZED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_manifest_report_blocks_preflight():
    report = _valid_manifest_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["star_law_preflight_boundary"][
        "star_law_preflight_boundary_analyzed"
    ] is False
    assert result["star_law_preflight_boundary"][
        "star_law_design_boundary_proposal_ready_for_human_review_only"
    ] is False
    assert result["analyzed_chain_versions"] == ANALYZED_CHAIN_VERSIONS
    assert result["analyzed_star_hub_chain_versions"] == ANALYZED_STAR_HUB_CHAIN_VERSIONS
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
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
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "handoff_performed",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "memory_write_authorized",
        "would_write_durable_memory",
        "would_mutate_memory_graph",
        "would_create_operation_ledger_entry",
        "openclaw_execution_authorized",
        "approval_granted",
        "approval_authorized",
        "approval_request_authorized",
        "human_decision_recorded",
        "real_human_decision_recorded",
    ],
)
def test_unsafe_top_level_claim_blocks_preflight(field: str):
    report = _valid_manifest_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_hub_final_closure_claimed",
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "handoff_performed",
        "dry_run_execution_authorized",
        "dry_run_performed",
        "dry_run_executed",
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
        "scheduling_performed",
        "durable_memory_write_authorized",
        "memory_graph_mutation_authorized",
        "operation_ledger_creation_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "real_human_decision_recorded",
        "star_dome_final_closure_claimed",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ],
)
def test_unsafe_manifest_boundary_claim_blocks_preflight(field: str):
    report = _valid_manifest_report()
    manifest = report["star_hub_closure_boundary_manifest"]
    assert isinstance(manifest, dict)
    manifest[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_manifested_chain_versions_blocks_preflight():
    report = _valid_manifest_report()
    report["manifested_chain_versions"] = ["v2.27.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_manifested_star_hub_chain_versions_blocks_preflight():
    report = _valid_manifest_report()
    report["manifested_star_hub_chain_versions"] = ["v2.27.0"]

    assert _build(report)["status"] == "blocked"


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_manifest_report()
    report["approval_phrase"] = "approve-hidden-star-law"
    report["nested"] = {
        "stdout_tail": "hidden terminal output",
        "api_key": "sk-hidden",
        "password": "hidden-password",
    }

    serialized = governed_star_law_preflight_boundary_analysis_to_json(_build(report))

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
        "approve-hidden-star-law",
        "hidden terminal output",
        "sk-hidden",
        "hidden-password",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field",
    [
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "self_executing_policy_created",
        "self_executing_policy_active",
        "enters_star_law_layer",
        "mature_star_law_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "would_write_durable_memory",
        "openclaw_execution_authorized",
        "civilization_core_complete_claimed",
    ],
)
def test_preflight_preserves_non_authorization_flags(field: str):
    result = _build()

    assert result[field] is False
    assert result["star_law_preflight_boundary"].get(field, False) is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law preflight boundary analysis only, not self-enforcing law and not autonomous execution"
    )
    assert mapping["source_layer"] == "星枢记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Hub staged closure boundary manifest complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Hub closure boundary manifest -> Star-Law preflight boundary analysis"
    )


def test_next_allowed_step_is_v2_29_star_law_design_boundary_proposal():
    assert _build()["next_allowed_step"] == "v2.29.0 Star-Law design boundary proposal"
    assert (
        _build()["star_law_preflight_boundary"]["next_allowed_step"]
        == "v2.29.0 Star-Law design boundary proposal"
    )
