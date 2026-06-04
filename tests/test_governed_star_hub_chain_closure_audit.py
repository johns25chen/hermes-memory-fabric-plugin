from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_hub_chain_closure_audit import (
    AUDITED_CHAIN_VERSIONS,
    AUDITED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_hub_chain_closure_audit,
    governed_star_hub_chain_closure_audit_to_json,
)
from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
)
from tests.test_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    _valid_proposal_report,
)


def _valid_review_gate_report() -> dict[str, object]:
    return build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
        _valid_proposal_report()
    )


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_hub_chain_closure_audit(
        report or _valid_review_gate_report()
    )


def test_valid_review_gate_report_creates_star_hub_chain_closure_audit_ready():
    result = _build()

    assert result["version"] == "2.26.0"
    assert result["status"] == "star_hub_chain_closure_audit_ready"
    assert result["source_review_gate_version"] == "2.25.0"
    assert all(check["passed"] is True for check in result["audit_checks"])
    assert result["blocking_reasons"] == []
    boundary = result["audited_star_hub_chain_boundary"]
    assert (
        boundary["audit_status"]
        == "star_hub_chain_audited_for_closure_boundary_manifest_readiness_only"
    )
    assert boundary["boundary_type"] == "star_hub_chain_closure_audit"
    assert boundary["star_hub_chain_audited"] is True
    assert boundary["star_hub_chain_structurally_continuous"] is True


def test_audited_chain_versions_exactly_match_v2_9_0_through_v2_25_0():
    result = _build()

    assert result["audited_chain_versions"] == AUDITED_CHAIN_VERSIONS
    assert (
        result["audited_star_hub_chain_boundary"]["audited_chain_versions"]
        == AUDITED_CHAIN_VERSIONS
    )


def test_audited_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_25_0():
    result = _build()

    assert result["audited_star_hub_chain_versions"] == AUDITED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["audited_star_hub_chain_boundary"]["audited_star_hub_chain_versions"]
        == AUDITED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_review_gate_report_blocks_audit():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["audited_chain_versions"] == AUDITED_CHAIN_VERSIONS
    assert result["audited_star_hub_chain_versions"] == AUDITED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["audited_star_hub_chain_boundary"][
            "star_hub_chain_closure_manifest_ready_for_human_review_only"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
        "star_hub_closure_claimed",
        "star_hub_final_closure_claimed",
        "closure_manifest_created",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "star_hub_handoff_authorized",
        "memory_write_authorized",
        "openclaw_execution_authorized",
        "approval_granted",
        "civilization_core_complete_claimed",
        "star_dome_final_closure_claimed",
    ],
)
def test_unsafe_top_level_claim_blocks_audit(field: str):
    report = _valid_review_gate_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_hub_closure_claimed",
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "dry_run_execution_boundary_authorized",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "durable_memory_write_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "civilization_core_complete_claimed",
        "star_dome_final_closure_claimed",
    ],
)
def test_unsafe_reviewed_boundary_claim_blocks_audit(field: str):
    report = _valid_review_gate_report()
    reviewed = report["reviewed_star_hub_dry_run_execution_boundary"]
    assert isinstance(reviewed, dict)
    reviewed[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_chain_versions_blocks_audit():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.25.0"]

    assert _build(report)["status"] == "blocked"


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_review_gate_report()
    report["approval_phrase"] = "approve-the-hidden-chain"
    report["nested"] = {
        "stdout_tail": "secret terminal tail",
        "api_key": "sk-hidden",
        "password": "hidden-password",
    }

    serialized = governed_star_hub_chain_closure_audit_to_json(_build(report))

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
        "approve-the-hidden-chain",
        "secret terminal tail",
        "sk-hidden",
        "hidden-password",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field",
    [
        "star_hub_final_closure_claimed",
        "star_hub_closure_claimed",
        "closure_manifest_created",
        "star_hub_handoff_authorized",
        "dry_run_execution_authorized",
        "dry_run_performed",
        "dry_run_executed",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "approval_request_created",
        "approval_request_submitted",
        "would_execute_approval_request",
        "human_decision_recorded",
        "approval_granted",
        "memory_write_authorized",
        "openclaw_execution_authorized",
        "civilization_core_complete_claimed",
    ],
)
def test_audit_does_not_authorize_perform_or_claim_governed_action(field: str):
    assert _build()[field] is False


def test_audited_boundary_does_not_claim_final_closure_or_authorize_handoff():
    boundary = _build()["audited_star_hub_chain_boundary"]

    assert boundary["star_hub_final_closure_claimed"] is False
    assert boundary["star_hub_closure_claimed"] is False
    assert boundary["closure_manifest_created"] is False
    assert boundary["star_hub_handoff_authorized"] is False
    assert boundary["star_hub_scheduling_authorized"] is False
    assert boundary["dry_run_execution_authorized"] is False
    assert boundary["civilization_core_complete_claimed"] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == (
        "Star-Hub chain closure audit only, not final closure and not handoff"
    )
    assert mapping["supporting_layers"] == ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    assert mapping["direction"] == (
        "Star-Hub scheduling dry-run execution boundary review gate -> Star-Hub chain closure audit"
    )


def test_next_allowed_step_is_v2_27_star_hub_closure_boundary_manifest():
    assert _build()["next_allowed_step"] == "v2.27.0 Star-Hub closure boundary manifest"
