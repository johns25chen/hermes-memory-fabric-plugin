from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_hub_chain_closure_audit import (
    build_governed_star_hub_chain_closure_audit,
)
from hermes_memory_fabric.governed_star_hub_closure_boundary_manifest import (
    MANIFESTED_CHAIN_VERSIONS,
    MANIFESTED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_hub_closure_boundary_manifest,
    governed_star_hub_closure_boundary_manifest_to_json,
)
from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
)
from tests.test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    _valid_proposal_report,
)


def _valid_audit_report() -> dict[str, object]:
    review_gate = build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
        _valid_proposal_report()
    )
    return build_governed_star_hub_chain_closure_audit(review_gate)


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_hub_closure_boundary_manifest(
        report or _valid_audit_report()
    )


def test_valid_audit_report_creates_star_hub_closure_boundary_manifest_ready():
    result = _build()

    assert result["version"] == "2.27.0"
    assert result["status"] == "star_hub_closure_boundary_manifest_ready"
    assert result["source_audit_version"] == "2.26.0"
    assert result["star_hub_staged_closure_boundary_ready"] is True
    assert result["star_hub_stage_sealed_for_human_review_only"] is True
    assert all(check["passed"] is True for check in result["manifest_checks"])
    assert result["blocking_reasons"] == []
    manifest = result["star_hub_closure_boundary_manifest"]
    assert (
        manifest["manifest_status"]
        == "star_hub_staged_closure_boundary_manifested_for_human_review_only"
    )
    assert manifest["boundary_type"] == "star_hub_closure_boundary_manifest"


def test_manifested_chain_versions_exactly_match_v2_9_0_through_v2_26_0():
    result = _build()

    assert result["manifested_chain_versions"] == MANIFESTED_CHAIN_VERSIONS
    assert (
        result["star_hub_closure_boundary_manifest"]["manifested_chain_versions"]
        == MANIFESTED_CHAIN_VERSIONS
    )


def test_manifested_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_26_0():
    result = _build()

    assert result["manifested_star_hub_chain_versions"] == MANIFESTED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["star_hub_closure_boundary_manifest"][
            "manifested_star_hub_chain_versions"
        ]
        == MANIFESTED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_audit_report_blocks_manifest():
    report = _valid_audit_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["star_hub_staged_closure_boundary_ready"] is False
    assert result["star_hub_stage_sealed_for_human_review_only"] is False
    assert result["manifested_chain_versions"] == MANIFESTED_CHAIN_VERSIONS
    assert result["manifested_star_hub_chain_versions"] == MANIFESTED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["star_hub_closure_boundary_manifest"][
            "star_hub_staged_closure_boundary_ready"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
        "civilization_core_complete_claimed",
        "star_hub_final_closure_claimed",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "handoff_performed",
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
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
        "approval_request_authorized",
        "human_decision_recorded",
        "star_dome_final_closure_claimed",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ],
)
def test_unsafe_top_level_claim_blocks_manifest(field: str):
    report = _valid_audit_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_hub_final_closure_claimed",
        "star_hub_closure_claimed",
        "closure_manifest_created",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "durable_memory_write_authorized",
        "memory_graph_mutation_authorized",
        "operation_ledger_creation_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "real_human_decision_recorded",
        "civilization_core_complete_claimed",
        "star_dome_final_closure_claimed",
    ],
)
def test_unsafe_audited_boundary_claim_blocks_manifest(field: str):
    report = _valid_audit_report()
    boundary = report["audited_star_hub_chain_boundary"]
    assert isinstance(boundary, dict)
    boundary[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_audited_chain_versions_blocks_manifest():
    report = _valid_audit_report()
    report["audited_chain_versions"] = ["v2.26.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_audited_star_hub_chain_versions_blocks_manifest():
    report = _valid_audit_report()
    report["audited_star_hub_chain_versions"] = ["v2.26.0"]

    assert _build(report)["status"] == "blocked"


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_audit_report()
    report["approval_phrase"] = "approve-the-hidden-manifest"
    report["nested"] = {
        "stdout_tail": "secret terminal tail",
        "api_key": "sk-hidden",
        "password": "hidden-password",
    }

    serialized = governed_star_hub_closure_boundary_manifest_to_json(_build(report))

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
        "approve-the-hidden-manifest",
        "secret terminal tail",
        "sk-hidden",
        "hidden-password",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field",
    [
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "handoff_performed",
        "dry_run_execution_authorized",
        "dry_run_performed",
        "dry_run_executed",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "would_create_approval_request",
        "would_submit_approval_request",
        "would_execute_approval_request",
        "would_record_human_decision",
        "would_grant_approval",
        "would_write_durable_memory",
        "openclaw_execution_authorized",
        "enters_star_law_layer",
    ],
)
def test_manifest_does_not_authorize_perform_or_claim_governed_action(field: str):
    assert _build()[field] is False


def test_nested_manifest_does_not_authorize_or_enter_later_layers():
    manifest = _build()["star_hub_closure_boundary_manifest"]

    for field in [
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
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ]:
        assert manifest[field] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == (
        "Star-Hub staged closure boundary manifest only, not handoff and not execution"
    )
    assert mapping["supporting_layers"] == ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    assert mapping["direction"] == (
        "Star-Hub chain closure audit -> Star-Hub closure boundary manifest"
    )


def test_next_allowed_step_is_v2_28_star_law_preflight_boundary_analysis():
    assert _build()["next_allowed_step"] == (
        "v2.28.0 Star-Law preflight boundary analysis"
    )
