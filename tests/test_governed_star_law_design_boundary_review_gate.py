from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_law_design_boundary_proposal import (
    build_governed_star_law_design_boundary_proposal,
)
from hermes_memory_fabric.governed_star_law_design_boundary_review_gate import (
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_law_design_boundary_review_gate,
    governed_star_law_design_boundary_review_gate_to_json,
)
from tests.test_governed_star_law_design_boundary_proposal import (
    _valid_preflight_report,
)


TOP_LEVEL_FALSE_FLAGS = [
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

REVIEW_GATE_FALSE_FLAGS = [
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
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "openclaw_execution_authorized",
    "approval_authorized",
    "real_human_decision_recorded",
]

UNSAFE_TOP_LEVEL_FIELDS = [
    "authorization_granted",
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
    "would_schedule_anything",
    "dry_run_performed",
    "dry_run_executed",
    "dry_run_execution_authorized",
    "would_execute_dry_run",
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
]


def _valid_proposal_report() -> dict[str, object]:
    return build_governed_star_law_design_boundary_proposal(
        _valid_preflight_report()
    )


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_design_boundary_review_gate(
        report or _valid_proposal_report()
    )


def test_valid_design_proposal_creates_star_law_design_boundary_review_gate_ready():
    result = _build()

    assert result["version"] == "2.30.0"
    assert result["status"] == "star_law_design_boundary_review_gate_ready"
    assert result["source_proposal_version"] == "2.29.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["review_gate_only"] is True
    assert result["design_boundary_review_gate_only"] is True
    assert result["star_law_design_boundary_review_gate_only"] is True
    assert result["star_law_design_boundary_review_ready"] is True
    assert (
        result[
            "star_law_candidate_rule_set_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert all(check["passed"] is True for check in result["review_gate_checks"])
    assert result["blocking_reasons"] == []
    review_gate = result["star_law_design_boundary_review_gate"]
    assert (
        review_gate["review_status"]
        == "star_law_design_boundary_reviewed_for_human_review_only"
    )
    assert review_gate["boundary_type"] == "star_law_design_boundary_review_gate"
    assert review_gate["star_law_design_boundary_reviewed"] is True
    assert review_gate["star_law_design_boundary_structurally_review_ready"] is True
    assert (
        review_gate[
            "candidate_rule_set_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert review_gate["source_star_law_design_boundary_proposal_valid"] is True


def test_reviewed_chain_versions_exactly_match_v2_9_0_through_v2_29_0():
    result = _build()

    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert (
        result["star_law_design_boundary_review_gate"]["reviewed_chain_versions"]
        == REVIEWED_CHAIN_VERSIONS
    )


def test_reviewed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_29_0():
    result = _build()

    assert result["reviewed_star_hub_chain_versions"] == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    assert (
        result["star_law_design_boundary_review_gate"][
            "reviewed_star_hub_chain_versions"
        ]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_design_proposal_blocks_review_gate():
    report = _valid_proposal_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["star_law_design_boundary_review_ready"] is False
    assert (
        result[
            "star_law_candidate_rule_set_boundary_proposal_ready_for_human_review_only"
        ]
        is False
    )
    review_gate = result["star_law_design_boundary_review_gate"]
    assert review_gate["star_law_design_boundary_reviewed"] is False
    assert review_gate["star_law_design_boundary_structurally_review_ready"] is False
    assert (
        review_gate[
            "candidate_rule_set_boundary_proposal_ready_for_human_review_only"
        ]
        is False
    )
    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert result["reviewed_star_hub_chain_versions"] == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize("field", UNSAFE_TOP_LEVEL_FIELDS)
def test_unsafe_top_level_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["star_law_design_boundary_review_ready"] is False
    assert result["star_law_design_boundary_review_gate"][
        "star_law_design_boundary_structurally_review_ready"
    ] is False
    for safe_field in TOP_LEVEL_FALSE_FLAGS:
        assert result[safe_field] is False
    assert result["civilization_core_complete_claimed"] is False
    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


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
        "durable_memory_write_authorized",
        "memory_graph_mutation_authorized",
        "operation_ledger_creation_authorized",
        "openclaw_execution_authorized",
        "approval_authorized",
        "real_human_decision_recorded",
    ],
)
def test_unsafe_source_design_boundary_proposal_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    proposal = report["star_law_design_boundary_proposal"]
    assert isinstance(proposal, dict)
    proposal[field] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_chain_versions"] = ["v2.29.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_star_hub_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_star_hub_chain_versions"] = ["v2.29.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_star_law_design_boundary_claim_blocks_review_gate():
    report = _valid_proposal_report()
    boundaries = report["proposed_star_law_design_boundaries"]
    assert isinstance(boundaries, dict)
    boundaries["candidate_rule_taxonomy_boundary"]["star_law_rules_created"] = True

    assert _build(report)["status"] == "blocked"


def test_textual_rule_activation_claim_in_design_boundaries_blocks_review_gate():
    report = _valid_proposal_report()
    boundaries = report["proposed_star_law_design_boundaries"]
    assert isinstance(boundaries, dict)
    boundaries["candidate_rule_taxonomy_boundary"]["description"] = (
        "Star-Law rules are active"
    )

    assert _build(report)["status"] == "blocked"


def test_reviewed_design_boundaries_remain_review_only_and_non_authorizing():
    result = _build()
    boundaries = result["reviewed_star_law_design_boundaries"]

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
        assert boundary["review_only"] is True
        for key, value in boundary.items():
            if key != "review_only":
                assert value is not True
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


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_proposal_report()
    report["approval_phrase"] = "approve-hidden-star-law-review"
    report["nested"] = {
        "stdout_tail": "hidden terminal output",
        "api_key": "sk-hidden",
        "password": "hidden-password",
        "token": "hidden-token",
    }

    serialized = governed_star_law_design_boundary_review_gate_to_json(_build(report))

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
        "approve-hidden-star-law-review",
        "hidden terminal output",
        "sk-hidden",
        "hidden-password",
        "hidden-token",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", TOP_LEVEL_FALSE_FLAGS)
def test_review_gate_preserves_top_level_non_authorization_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", REVIEW_GATE_FALSE_FLAGS)
def test_star_law_design_boundary_review_gate_preserves_non_authorization_flags(
    field: str,
):
    assert _build()["star_law_design_boundary_review_gate"][field] is False


def test_review_gate_does_not_create_self_enforcing_memory_law():
    result = _build()

    assert result["star_law_self_enforcing_law_created"] is False
    assert result["star_law_self_enforcing_law_active"] is False
    assert result["non_authorization_boundary"][
        "star_law_design_boundary_review_gate_ready_is_self_enforcing_memory_law"
    ] is False


def test_review_gate_does_not_create_activate_or_enforce_star_law_rules():
    result = _build()

    assert result["star_law_rules_created"] is False
    assert result["star_law_rules_activated"] is False
    assert result["star_law_rules_enforced"] is False
    boundary = result["non_authorization_boundary"]
    assert boundary["star_law_design_boundary_review_gate_ready_is_rule_creation"] is False
    assert boundary["star_law_design_boundary_review_gate_ready_is_rule_activation"] is False
    assert boundary["star_law_design_boundary_review_gate_ready_is_rule_enforcement"] is False


def test_review_gate_does_not_create_autonomous_governance_or_authorize_execution():
    result = _build()

    assert result["autonomous_governance_created"] is False
    assert result["autonomous_execution_authorized"] is False
    boundary = result["non_authorization_boundary"]
    assert (
        boundary["star_law_design_boundary_review_gate_ready_is_autonomous_governance"]
        is False
    )
    assert (
        boundary["star_law_design_boundary_review_gate_ready_is_autonomous_execution"]
        is False
    )


def test_review_gate_does_not_enter_star_law_layer():
    result = _build()

    assert result["enters_star_law_layer"] is False
    assert result["mature_star_law_claimed"] is False


def test_review_gate_does_not_authorize_handoff_or_durable_memory_write():
    result = _build()

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False
    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False


def test_review_gate_does_not_authorize_openclaw_execution_or_claim_core_completion():
    result = _build()

    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False
    assert result["civilization_core_complete_claimed"] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law design boundary review gate only, not rule activation and not rule enforcement"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law design boundary proposal complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law design boundary proposal -> Star-Law design boundary review gate"
    )


def test_next_allowed_step_is_v2_31_star_law_candidate_rule_set_boundary_proposal():
    result = _build()

    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        result["star_law_design_boundary_review_gate"]["next_allowed_step"]
        == READY_NEXT_ALLOWED_STEP
    )
