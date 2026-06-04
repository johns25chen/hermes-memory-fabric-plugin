from __future__ import annotations

import json

from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_proposal import (
    build_governed_star_hub_scheduling_dry_run_execution_boundary_proposal,
    governed_star_hub_scheduling_dry_run_execution_boundary_proposal_to_json,
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
]

EXPECTED_CHAIN = [
    *SOURCE_CHAIN,
    "v2.23.0",
]


def _valid_review_gate_report() -> dict[str, object]:
    return {
        "version": "2.23.0",
        "status": "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready",
        "read_only": True,
        "read_only_memory": True,
        "review_gate_only": True,
        "dry_run_plan_boundary_review_gate_only": True,
        "scheduling_dry_run_plan_boundary_review_gate_only": True,
        "star_hub_dry_run_plan_review_gate_only": True,
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
        "dry_run_plan_review_authorized": False,
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
            "primary_layer_status": "scheduling dry-run plan boundary review gate only, not scheduling and not dry-run execution",
            "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
        },
        "reviewed_chain_versions": SOURCE_CHAIN,
        "next_allowed_step": "v2.24.0 Star-Hub scheduling dry-run execution boundary proposal",
        "blocking_reasons": [],
        "reviewed_star_hub_dry_run_plan_boundary": {
            "review_status": "star_hub_scheduling_dry_run_plan_boundary_reviewed_for_human_review_only",
            "star_hub_dry_run_plan_boundary_reviewed": True,
            "dry_run_plan_review_authorized": False,
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
            "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready_is_star_hub_scheduling": False,
            "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready_is_dry_run_execution": False,
            "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready_is_star_hub_handoff": False,
            "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready_is_authorization": False,
            "star_hub_scheduling_dry_run_plan_boundary_review_gate_ready_is_civilization_core_completion": False,
        },
    }


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_hub_scheduling_dry_run_execution_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_review_gate_report_creates_star_hub_scheduling_dry_run_execution_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.24.0"
    assert (
        result["status"]
        == "star_hub_scheduling_dry_run_execution_boundary_proposal_ready"
    )
    assert result["source_review_gate_version"] == "2.23.0"
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposed = result["proposed_star_hub_dry_run_execution_boundary"]
    assert proposed["proposal_status"] == (
        "star_hub_scheduling_dry_run_execution_boundary_proposed_for_human_review_only"
    )
    assert proposed["boundary_type"] == (
        "star_hub_scheduling_dry_run_execution_boundary_proposal"
    )
    assert proposed["star_hub_dry_run_execution_boundary_proposed"] is True


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_23_0():
    result = _build()

    assert result["proposed_chain_versions"] == EXPECTED_CHAIN
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"][
            "proposed_chain_versions"
        ]
        == EXPECTED_CHAIN
    )


def test_blocked_review_gate_report_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == EXPECTED_CHAIN
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"][
            "star_hub_dry_run_execution_boundary_proposed"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


def test_unsafe_authorization_flag_blocks_proposal():
    report = _valid_review_gate_report()
    report["authorization_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_star_hub_scheduling_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_hub_scheduling_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_star_hub_scheduling_performed_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["scheduling_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_performed_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["dry_run_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_executed_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["dry_run_executed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_execution_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["dry_run_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_star_hub_handoff_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_hub_handoff_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_memory_write_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["memory_write_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_openclaw_execution_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["openclaw_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_approval_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_civilization_core_completion_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["civilization_core_complete_claimed"] = True

    assert _build(report)["status"] == "blocked"


def test_star_dome_final_closure_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_dome_final_closure_claimed"] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.9.0", "v2.22.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == EXPECTED_CHAIN


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_review_gate_report()
    report["approval_phrase"] = "approve-secret-material"
    report["nested"] = {
        "stdout_tail": "hidden-tail",
        "stdout": "hidden-stdout",
        "raw_logs": "hidden-logs",
        "token": "hidden-token",
        "api_key": "hidden-api-key",
        "secret": "hidden-secret",
        "credential": "hidden-credential",
        "safe": [{"password": "hidden-password"}],
    }

    result = _build(report)
    payload = governed_star_hub_scheduling_dry_run_execution_boundary_proposal_to_json(
        result
    )

    assert result["sensitive_fields_omitted"] is True
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
        "approve-secret-material",
        "hidden-tail",
        "hidden-stdout",
        "hidden-logs",
        "hidden-token",
        "hidden-api-key",
        "hidden-secret",
        "hidden-password",
        "hidden-credential",
    ]:
        assert forbidden not in payload
    json.loads(payload)


def test_proposal_does_not_authorize_dry_run_execution_boundary():
    result = _build()

    assert result["dry_run_execution_boundary_authorized"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"][
            "dry_run_execution_boundary_authorized"
        ]
        is False
    )


def test_proposal_does_not_authorize_dry_run_execution():
    result = _build()

    assert result["dry_run_execution_authorized"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"][
            "dry_run_execution_authorized"
        ]
        is False
    )


def test_proposal_does_not_perform_dry_run():
    result = _build()

    assert result["dry_run_performed"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"]["dry_run_performed"]
        is False
    )


def test_proposal_does_not_execute_dry_run():
    result = _build()

    assert result["dry_run_executed"] is False
    assert result["would_execute_dry_run"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"]["dry_run_executed"]
        is False
    )


def test_proposal_does_not_authorize_star_hub_scheduling():
    result = _build()

    assert result["star_hub_scheduling_authorized"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"][
            "star_hub_scheduling_authorized"
        ]
        is False
    )


def test_proposal_does_not_perform_scheduling():
    result = _build()

    assert result["scheduling_performed"] is False
    assert result["would_schedule_anything"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"]["scheduling_performed"]
        is False
    )


def test_proposal_does_not_authorize_handoff():
    result = _build()

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False


def test_proposal_does_not_create_approval_request():
    result = _build()

    assert result["approval_request_created"] is False
    assert result["would_create_approval_request"] is False


def test_proposal_does_not_submit_approval_request():
    result = _build()

    assert result["approval_request_submitted"] is False
    assert result["would_submit_approval_request"] is False


def test_proposal_does_not_execute_approval_request():
    result = _build()

    assert result["would_execute_approval_request"] is False


def test_proposal_does_not_record_human_decision():
    result = _build()

    assert result["human_decision_recorded"] is False
    assert result["would_record_human_decision"] is False


def test_proposal_does_not_authorize_approval():
    result = _build()

    assert result["approval_granted"] is False
    assert result["would_grant_approval"] is False
    assert (
        result["proposed_star_hub_dry_run_execution_boundary"]["approval_authorized"]
        is False
    )


def test_proposal_does_not_authorize_memory_write():
    result = _build()

    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False


def test_proposal_does_not_authorize_openclaw_execution():
    result = _build()

    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False


def test_layer_mapping_is_correct():
    result = _build()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == (
        "scheduling dry-run execution boundary proposal only, not scheduling and not dry-run execution"
    )
    assert "星穹记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert "星辰记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == (
        "Star-Hub scheduling dry-run plan boundary review gate -> Star-Hub scheduling dry-run execution boundary proposal"
    )


def test_next_allowed_step_is_v2_25_star_hub_scheduling_dry_run_execution_boundary_review_gate():
    result = _build()

    assert result["next_allowed_step"] == (
        "v2.25.0 Star-Hub scheduling dry-run execution boundary review gate"
    )
    assert result["proposed_star_hub_dry_run_execution_boundary"][
        "next_allowed_step"
    ] == "v2.25.0 Star-Hub scheduling dry-run execution boundary review gate"
