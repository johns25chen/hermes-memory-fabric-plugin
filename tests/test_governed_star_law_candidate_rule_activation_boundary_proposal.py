from __future__ import annotations

from copy import deepcopy
import json

from hermes_memory_fabric.governed_star_law_candidate_rule_activation_boundary_proposal import (
    PROPOSED_CANDIDATE_RULE_ACTIVATION_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    build_governed_star_law_candidate_rule_activation_boundary_proposal,
    governed_star_law_candidate_rule_activation_boundary_proposal_to_json,
)
from tests.test_governed_star_law_candidate_rule_set_boundary_review_gate import (
    _build as _valid_v2_32_review_gate,
)


TOP_LEVEL_FALSE_FLAGS = [
    "candidate_rule_activation_performed",
    "candidate_rule_activation_authorized",
    "star_law_candidate_rules_created",
    "star_law_candidate_rules_activated",
    "star_law_rules_created",
    "star_law_rules_activated",
    "star_law_rules_enforced",
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
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
    "handoff_performed",
    "dry_run_performed",
    "dry_run_executed",
    "scheduling_performed",
    "would_schedule_anything",
    "would_execute_dry_run",
    "would_mutate_memory",
    "writes_files",
    "invokes_openclaw",
    "would_call_github_api",
    "would_merge_pr",
    "would_create_tag",
    "would_write_durable_memory",
    "would_mutate_memory_graph",
    "would_create_operation_ledger_entry",
    "would_create_approval_request",
    "would_submit_approval_request",
    "would_execute_approval_request",
    "would_record_human_decision",
    "would_grant_approval",
    "authorization_granted",
    "approval_request_created",
    "approval_request_submitted",
    "approval_request_authorized",
    "approval_granted",
    "human_decision_recorded",
    "memory_write_authorized",
    "openclaw_execution_authorized",
    "star_dome_final_closure_claimed",
]

PROPOSAL_FALSE_FLAGS = [
    "candidate_rule_activation_performed",
    "candidate_rule_activation_authorized",
    "star_law_candidate_rules_created",
    "star_law_candidate_rules_activated",
    "star_law_rules_created",
    "star_law_rules_activated",
    "star_law_rules_enforced",
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
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
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "openclaw_execution_authorized",
    "approval_authorized",
    "real_human_decision_recorded",
]

UNSAFE_SOURCE_FLAGS = [
    "authorization_granted",
    "candidate_rule_activation_performed",
    "candidate_rule_activation_authorized",
    "star_law_candidate_rules_created",
    "star_law_candidate_rules_activated",
    "star_law_rules_created",
    "star_law_rules_activated",
    "star_law_rules_enforced",
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
    "autonomous_governance_created",
    "autonomous_execution_authorized",
    "self_executing_policy_created",
    "self_executing_policy_active",
    "enters_star_law_layer",
    "enters_star_soul_layer",
    "enters_star_cosmos_layer",
    "enters_star_source_layer",
    "civilization_core_complete_claimed",
    "star_hub_handoff_authorized",
    "scheduling_authorized",
    "scheduling_performed",
    "dry_run_performed",
    "dry_run_executed",
    "dry_run_execution_authorized",
    "memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "openclaw_execution_authorized",
    "approval_granted",
    "real_human_decision_recorded",
]

SENSITIVE_KEYS = [
    "approval_phrase",
    "stdout_tail",
    "stdout",
    "raw_logs",
    "token",
    "api_key",
    "secret",
    "password",
    "credential",
]


def _valid_review_gate_report() -> dict[str, object]:
    return deepcopy(_valid_v2_32_review_gate())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_activation_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_candidate_rule_set_boundary_review_gate_creates_star_law_candidate_rule_activation_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.33.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_activation_boundary_proposal_ready"
    )
    assert result["source_review_gate_version"] == "2.32.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["proposal_only"] is True
    assert result["candidate_rule_activation_boundary_proposal_only"] is True
    assert (
        result["star_law_candidate_rule_activation_boundary_proposal_only"] is True
    )
    assert (
        result["candidate_rule_activation_boundary_proposed_for_human_review_only"]
        is True
    )
    assert (
        result[
            "candidate_rule_activation_boundary_review_gate_ready_for_human_review_only"
        ]
        is True
    )
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposal = result["star_law_candidate_rule_activation_boundary_proposal"]
    assert (
        proposal["proposal_status"]
        == "star_law_candidate_rule_activation_boundary_proposed_for_human_review_only"
    )
    assert proposal["boundary_type"] == "star_law_candidate_rule_activation_boundary_proposal"
    assert proposal["source_review_gate_version"] == "2.32.0"
    assert proposal["candidate_rule_activation_boundary_proposed"] is True
    assert (
        proposal[
            "candidate_rule_activation_boundary_review_gate_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        proposal["source_star_law_candidate_rule_set_boundary_review_gate_valid"]
        is True
    )


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_32_0():
    result = _build()

    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert PROPOSED_CHAIN_VERSIONS == [
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
        "v2.24.0",
        "v2.25.0",
        "v2.26.0",
        "v2.27.0",
        "v2.28.0",
        "v2.29.0",
        "v2.30.0",
        "v2.31.0",
        "v2.32.0",
    ]


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_32_0():
    result = _build()

    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    assert PROPOSED_STAR_HUB_CHAIN_VERSIONS == [
        "v2.19.0",
        "v2.20.0",
        "v2.21.0",
        "v2.22.0",
        "v2.23.0",
        "v2.24.0",
        "v2.25.0",
        "v2.26.0",
        "v2.27.0",
        "v2.28.0",
        "v2.29.0",
        "v2.30.0",
        "v2.31.0",
        "v2.32.0",
    ]


def test_blocked_candidate_rule_set_boundary_review_gate_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_not_ready"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["candidate_rule_activation_boundary_proposed_for_human_review_only"]
        is False
    )
    proposal = result["star_law_candidate_rule_activation_boundary_proposal"]
    assert proposal["candidate_rule_activation_boundary_proposed"] is False
    assert (
        proposal[
            "candidate_rule_activation_boundary_review_gate_ready_for_human_review_only"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


def test_unsafe_authorization_flag_blocks_proposal():
    report = _valid_review_gate_report()
    report["authorization_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_candidate_rule_activation_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["candidate_rule_activation_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_candidate_rule_activation_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["candidate_rule_activation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_candidate_rule_creation_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_candidate_rules_created"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_candidate_rule_activation_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_candidate_rules_activated"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_creation_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_rules_created"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_activation_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_rules_activated"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_enforcement_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_rules_enforced"] = True

    assert _build(report)["status"] == "blocked"


def test_self_enforcing_law_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_law_self_enforcing_law_active"] = True

    assert _build(report)["status"] == "blocked"


def test_autonomous_governance_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["autonomous_governance_created"] = True

    assert _build(report)["status"] == "blocked"


def test_autonomous_execution_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["autonomous_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_self_executing_policy_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["self_executing_policy_active"] = True

    assert _build(report)["status"] == "blocked"


def test_entering_star_law_star_soul_star_cosmos_or_star_source_claim_blocks_proposal():
    for field in [
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ]:
        report = _valid_review_gate_report()
        report[field] = True

        assert _build(report)["status"] == "blocked"


def test_civilization_core_completion_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["civilization_core_complete_claimed"] = True

    assert _build(report)["status"] == "blocked"


def test_star_hub_handoff_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["star_hub_handoff_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_scheduling_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["scheduling_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_scheduling_performed_claim_blocks_proposal():
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


def test_memory_write_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["memory_write_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_memory_graph_mutation_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["memory_graph_mutation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_operation_ledger_creation_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["operation_ledger_creation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_openclaw_execution_authorization_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["openclaw_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_approval_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_real_human_decision_claim_blocks_proposal():
    report = _valid_review_gate_report()
    report["real_human_decision_recorded"] = True

    assert _build(report)["status"] == "blocked"


def test_all_unsafe_source_flags_block_proposal():
    for field in UNSAFE_SOURCE_FLAGS:
        report = _valid_review_gate_report()
        report[field] = True

        assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.9.0", "v2.32.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS


def test_malformed_reviewed_star_hub_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_star_hub_chain_versions"] = ["v2.19.0", "v2.32.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS


def test_proposed_candidate_rule_activation_boundaries_are_proposal_only_and_non_authorizing():
    result = _build()
    boundaries = result["proposed_candidate_rule_activation_boundaries"]

    assert set(boundaries) == PROPOSED_CANDIDATE_RULE_ACTIVATION_BOUNDARY_KEYS
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        for key, value in boundary.items():
            if isinstance(value, bool) and key != "proposal_only":
                assert value is False


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_review_gate_report()
    report["nested_sensitive"] = {
        "approval_phrase": "do-not-leak-approval-phrase",
        "stdout_tail": "do-not-leak-stdout-tail",
        "stdout": "do-not-leak-stdout",
        "raw_logs": "do-not-leak-raw-logs",
        "token": "do-not-leak-token",
        "api_key": "do-not-leak-api-key",
        "secret": "do-not-leak-secret",
        "password": "do-not-leak-password",
        "credential": "do-not-leak-credential",
    }

    result = _build(report)
    serialized = governed_star_law_candidate_rule_activation_boundary_proposal_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized


def test_proposal_does_not_activate_create_enforce_authorize_or_claim_completion():
    result = _build()
    proposal = result["star_law_candidate_rule_activation_boundary_proposal"]

    for flag in TOP_LEVEL_FALSE_FLAGS:
        assert result[flag] is False
    for flag in PROPOSAL_FALSE_FLAGS:
        assert proposal[flag] is False
    assert result["candidate_rule_activation_boundary_proposal_only"] is True
    assert result["star_law_candidate_rule_activation_boundary_proposal_only"] is True


def test_layer_mapping_is_correct():
    result = _build()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert mapping["primary_layer_status"] == (
        "Star-Law candidate rule activation boundary proposal only, not candidate rule activation, not rule activation, and not rule enforcement"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law candidate rule-set boundary review gate complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law candidate rule-set boundary review gate -> Star-Law candidate rule activation boundary proposal"
    )


def test_next_allowed_step_is_v2_34_0_star_law_candidate_rule_activation_boundary_review_gate():
    result = _build()

    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        result["star_law_candidate_rule_activation_boundary_proposal"][
            "next_allowed_step"
        ]
        == READY_NEXT_ALLOWED_STEP
    )


def test_report_is_json_serializable():
    result = _build()
    payload = governed_star_law_candidate_rule_activation_boundary_proposal_to_json(
        result
    )
    decoded = json.loads(payload)

    assert (
        decoded["status"]
        == "star_law_candidate_rule_activation_boundary_proposal_ready"
    )
