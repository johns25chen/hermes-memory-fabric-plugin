from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
    governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_to_json,
)


SOURCE_CHAIN = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
    "v2.17.0",
    "v2.18.0",
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
]

EXPECTED_CHAIN = [
    *SOURCE_CHAIN,
    "v2.24.0",
]


def _valid_proposal_report() -> dict[str, object]:
    return {
        "version": "2.24.0",
        "status": "star_hub_scheduling_dry_run_execution_boundary_proposal_ready",
        "read_only": True,
        "read_only_memory": True,
        "proposal_only": True,
        "dry_run_execution_boundary_proposal_only": True,
        "scheduling_dry_run_execution_boundary_proposal_only": True,
        "star_hub_dry_run_execution_boundary_only": True,
        "dry_run_performed": False,
        "dry_run_executed": False,
        "scheduling_performed": False,
        "would_schedule_anything": False,
        "would_execute_dry_run": False,
        "would_mutate_memory": False,
        "writes_files": False,
        "invokes_openclaw": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "would_write_durable_memory": False,
        "would_mutate_memory_graph": False,
        "would_create_operation_ledger_entry": False,
        "would_create_approval_request": False,
        "would_submit_approval_request": False,
        "would_execute_approval_request": False,
        "would_record_human_decision": False,
        "would_grant_approval": False,
        "authorization_granted": False,
        "dry_run_execution_boundary_authorized": False,
        "dry_run_execution_authorized": False,
        "scheduling_dry_run_authorized": False,
        "star_hub_scheduling_authorized": False,
        "star_hub_scheduling_executed": False,
        "star_hub_handoff_authorized": False,
        "handoff_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "star_dome_final_closure_claimed": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星枢记忆",
            "primary_layer_status": "scheduling dry-run execution boundary proposal only, not scheduling and not dry-run execution",
            "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
        },
        "proposed_chain_versions": SOURCE_CHAIN,
        "next_allowed_step": "v2.25.0 Star-Hub scheduling dry-run execution boundary review gate",
        "blocking_reasons": [],
        "proposed_star_hub_dry_run_execution_boundary": {
            "proposal_status": "star_hub_scheduling_dry_run_execution_boundary_proposed_for_human_review_only",
            "star_hub_dry_run_execution_boundary_proposed": True,
            "dry_run_execution_boundary_authorized": False,
            "dry_run_execution_authorized": False,
            "dry_run_performed": False,
            "dry_run_executed": False,
            "star_hub_scheduling_authorized": False,
            "star_hub_scheduling_executed": False,
            "scheduling_performed": False,
            "star_hub_handoff_authorized": False,
            "handoff_authorized": False,
            "durable_memory_write_authorized": False,
            "memory_graph_mutation_authorized": False,
            "operation_ledger_creation_authorized": False,
            "openclaw_execution_authorized": False,
            "approval_authorized": False,
            "real_human_decision_recorded": False,
            "civilization_core_complete_claimed": False,
            "star_dome_final_closure_claimed": False,
        },
        "non_authorization_boundary": {
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_star_hub_scheduling": False,
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_dry_run_execution": False,
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_star_hub_handoff": False,
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_authorization": False,
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_civilization_core_completion": False,
        },
    }


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
        report or _valid_proposal_report()
    )


def test_valid_proposal_report_creates_star_hub_scheduling_dry_run_execution_boundary_review_gate_ready():
    result = _build()

    assert result["version"] == "2.25.0"
    assert (
        result["status"]
        == "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready"
    )
    assert result["source_proposal_version"] == "2.24.0"
    assert all(check["passed"] is True for check in result["review_gate_checks"])
    assert result["blocking_reasons"] == []
    reviewed = result["reviewed_star_hub_dry_run_execution_boundary"]
    assert reviewed["review_status"] == (
        "star_hub_scheduling_dry_run_execution_boundary_reviewed_for_human_review_only"
    )
    assert reviewed["boundary_type"] == (
        "star_hub_scheduling_dry_run_execution_boundary_review_gate"
    )
    assert reviewed["star_hub_dry_run_execution_boundary_reviewed"] is True


def test_reviewed_chain_versions_exactly_match_v2_9_0_through_v2_24_0():
    result = _build()

    assert result["reviewed_chain_versions"] == EXPECTED_CHAIN
    assert (
        result["reviewed_star_hub_dry_run_execution_boundary"][
            "reviewed_chain_versions"
        ]
        == EXPECTED_CHAIN
    )


def test_blocked_proposal_report_blocks_review_gate():
    report = _valid_proposal_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["reviewed_chain_versions"] == EXPECTED_CHAIN
    assert (
        result["reviewed_star_hub_dry_run_execution_boundary"][
            "star_hub_dry_run_execution_boundary_reviewed"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "dry_run_execution_boundary_authorized",
        "star_hub_handoff_authorized",
        "memory_write_authorized",
        "openclaw_execution_authorized",
        "approval_granted",
        "civilization_core_complete_claimed",
        "star_hub_closure_claimed",
        "star_dome_final_closure_claimed",
    ],
)
def test_unsafe_top_level_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
        "dry_run_performed",
        "dry_run_executed",
        "dry_run_execution_authorized",
        "dry_run_execution_boundary_authorized",
        "star_hub_handoff_authorized",
        "durable_memory_write_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "civilization_core_complete_claimed",
        "star_dome_final_closure_claimed",
    ],
)
def test_unsafe_proposed_boundary_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    proposed = report["proposed_star_hub_dry_run_execution_boundary"]
    assert isinstance(proposed, dict)
    proposed[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_chain_versions"] = ["v2.24.0"]

    assert _build(report)["status"] == "blocked"


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_proposal_report()
    report["approval_phrase"] = "approve-the-hidden-boundary"
    report["nested"] = {
        "stdout_tail": "secret terminal tail",
        "api_key": "sk-hidden",
        "password": "hidden-password",
    }

    serialized = governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_to_json(
        _build(report)
    )

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
        "approve-the-hidden-boundary",
        "secret terminal tail",
        "sk-hidden",
        "hidden-password",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field",
    [
        "dry_run_execution_boundary_review_authorized",
        "dry_run_execution_boundary_authorized",
        "dry_run_execution_authorized",
        "dry_run_performed",
        "dry_run_executed",
        "star_hub_scheduling_authorized",
        "scheduling_performed",
        "star_hub_handoff_authorized",
        "approval_request_created",
        "approval_request_submitted",
        "would_execute_approval_request",
        "human_decision_recorded",
        "approval_granted",
        "memory_write_authorized",
        "openclaw_execution_authorized",
        "civilization_core_complete_claimed",
        "star_hub_closure_claimed",
    ],
)
def test_review_gate_does_not_authorize_or_perform_any_governed_action(field: str):
    assert _build()[field] is False


def test_review_gate_does_not_claim_star_dome_final_closure():
    assert _build()["star_dome_final_closure_claimed"] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == (
        "scheduling dry-run execution boundary review gate only, not scheduling and not dry-run execution"
    )
    assert mapping["supporting_layers"] == ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]


def test_next_allowed_step_is_v2_26_star_hub_chain_closure_audit():
    assert _build()["next_allowed_step"] == "v2.26.0 Star-Hub chain closure audit"
