from __future__ import annotations

import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_set_boundary_proposal import (
    PROPOSED_CANDIDATE_RULE_SET_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    build_governed_star_law_candidate_rule_set_boundary_proposal,
    governed_star_law_candidate_rule_set_boundary_proposal_to_json,
)
from hermes_memory_fabric.governed_star_law_design_boundary_proposal import (
    build_governed_star_law_design_boundary_proposal,
)
from hermes_memory_fabric.governed_star_law_design_boundary_review_gate import (
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_law_design_boundary_review_gate,
)
from tests.test_governed_star_law_design_boundary_proposal import (
    _valid_preflight_report,
)


TOP_LEVEL_FALSE_FLAGS = [
    "star_law_candidate_rules_created",
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
    "star_law_candidate_rules_created",
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

UNSAFE_TOP_LEVEL_FIELDS = [
    "star_law_candidate_rules_created",
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
    "invokes_openclaw",
    "approval_granted",
    "approval_authorized",
    "approval_request_authorized",
    "approval_request_created",
    "approval_request_submitted",
    "approval_request_executed",
    "would_execute_approval_request",
    "human_decision_recorded",
    "real_human_decision_recorded",
]

UNSAFE_REVIEW_GATE_FIELDS = [
    "star_law_candidate_rules_created",
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


def _valid_review_gate_report() -> dict[str, object]:
    return build_governed_star_law_design_boundary_review_gate(
        build_governed_star_law_design_boundary_proposal(_valid_preflight_report())
    )


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_set_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_review_gate_creates_star_law_candidate_rule_set_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.31.0"
    assert result["status"] == "star_law_candidate_rule_set_boundary_proposal_ready"
    assert result["source_review_gate_version"] == "2.30.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["proposal_only"] is True
    assert result["candidate_rule_set_boundary_proposal_only"] is True
    assert result["star_law_candidate_rule_set_boundary_proposal_only"] is True
    assert result["candidate_rule_set_boundary_proposed_for_human_review_only"] is True
    assert result["candidate_rule_set_review_gate_ready_for_human_review_only"] is True
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposal = result["star_law_candidate_rule_set_boundary_proposal"]
    assert (
        proposal["proposal_status"]
        == "star_law_candidate_rule_set_boundary_proposed_for_human_review_only"
    )
    assert proposal["boundary_type"] == "star_law_candidate_rule_set_boundary_proposal"
    assert proposal["source_review_gate_version"] == "2.30.0"
    assert proposal["candidate_rule_set_boundary_proposed"] is True
    assert (
        proposal["candidate_rule_set_boundary_review_gate_ready_for_human_review_only"]
        is True
    )
    assert proposal["source_star_law_design_boundary_review_gate_valid"] is True


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_30_0():
    result = _build()

    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert PROPOSED_CHAIN_VERSIONS == [*REVIEWED_CHAIN_VERSIONS, "v2.30.0"]
    assert (
        result["star_law_candidate_rule_set_boundary_proposal"][
            "proposed_chain_versions"
        ]
        == PROPOSED_CHAIN_VERSIONS
    )


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_30_0():
    result = _build()

    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    assert PROPOSED_STAR_HUB_CHAIN_VERSIONS == [
        *REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "v2.30.0",
    ]
    assert (
        result["star_law_candidate_rule_set_boundary_proposal"][
            "proposed_star_hub_chain_versions"
        ]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_review_gate_report_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["candidate_rule_set_boundary_proposed_for_human_review_only"] is False
    assert result["candidate_rule_set_review_gate_ready_for_human_review_only"] is False
    proposal = result["star_law_candidate_rule_set_boundary_proposal"]
    assert proposal["candidate_rule_set_boundary_proposed"] is False
    assert (
        proposal["candidate_rule_set_boundary_review_gate_ready_for_human_review_only"]
        is False
    )
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert result["proposed_star_hub_chain_versions"] == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize("field", UNSAFE_TOP_LEVEL_FIELDS)
def test_unsafe_top_level_claim_blocks_proposal(field: str):
    report = _valid_review_gate_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["candidate_rule_set_boundary_proposed_for_human_review_only"] is False
    assert result["candidate_rule_set_review_gate_ready_for_human_review_only"] is False
    for safe_field in TOP_LEVEL_FALSE_FLAGS:
        assert result[safe_field] is False
    assert result["civilization_core_complete_claimed"] is False
    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


@pytest.mark.parametrize("field", UNSAFE_REVIEW_GATE_FIELDS)
def test_unsafe_source_review_gate_claim_blocks_proposal(field: str):
    report = _valid_review_gate_report()
    review_gate = report["star_law_design_boundary_review_gate"]
    assert isinstance(review_gate, dict)
    review_gate[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["star_law_candidate_rule_set_boundary_proposal"][
            "source_star_law_design_boundary_review_gate_valid"
        ]
        is False
    )


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.30.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_star_hub_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_star_hub_chain_versions"] = ["v2.30.0"]

    assert _build(report)["status"] == "blocked"


def test_unsafe_reviewed_design_boundary_claim_blocks_proposal():
    report = _valid_review_gate_report()
    boundaries = report["reviewed_star_law_design_boundaries"]
    assert isinstance(boundaries, dict)
    first = next(iter(boundaries.values()))
    assert isinstance(first, dict)
    first["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_textual_rule_activation_claim_in_source_boundaries_blocks_proposal():
    report = _valid_review_gate_report()
    boundaries = report["reviewed_star_law_design_boundaries"]
    assert isinstance(boundaries, dict)
    first = next(iter(boundaries.values()))
    assert isinstance(first, dict)
    first["summary"] = "Star-Law rules are active"

    assert _build(report)["status"] == "blocked"


def test_proposed_candidate_rule_set_boundaries_are_proposal_only_and_non_authorizing():
    result = _build()
    boundaries = result["proposed_candidate_rule_set_boundaries"]

    assert isinstance(boundaries, dict)
    assert set(boundaries) == PROPOSED_CANDIDATE_RULE_SET_BOUNDARY_KEYS
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        for key, value in boundary.items():
            if key != "proposal_only":
                assert value is not True
    serialized = json.dumps(boundaries, ensure_ascii=True, sort_keys=True).lower()
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
        assert forbidden_claim not in serialized


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_review_gate_report()
    report["approval_phrase"] = "approve-hidden-star-law-candidate-rule-set"
    report["nested"] = {
        "stdout_tail": "hidden terminal output",
        "api_key": "sk-hidden",
        "password": "hidden-password",
        "token": "hidden-token",
    }

    serialized = governed_star_law_candidate_rule_set_boundary_proposal_to_json(
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
        "approve-hidden-star-law-candidate-rule-set",
        "hidden terminal output",
        "sk-hidden",
        "hidden-password",
        "hidden-token",
    ]:
        assert forbidden not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", TOP_LEVEL_FALSE_FLAGS)
def test_proposal_preserves_top_level_non_authorization_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", PROPOSAL_FALSE_FLAGS)
def test_star_law_candidate_rule_set_boundary_proposal_preserves_non_authorization_flags(
    field: str,
):
    assert _build()["star_law_candidate_rule_set_boundary_proposal"][field] is False


def test_proposal_does_not_create_candidate_rules():
    result = _build()

    assert result["star_law_candidate_rules_created"] is False
    assert (
        result["star_law_candidate_rule_set_boundary_proposal"][
            "star_law_candidate_rules_created"
        ]
        is False
    )


def test_proposal_does_not_create_activate_or_enforce_star_law_rules():
    result = _build()

    assert result["star_law_rules_created"] is False
    assert result["star_law_rules_activated"] is False
    assert result["star_law_rules_enforced"] is False
    boundary = result["non_authorization_boundary"]
    assert (
        boundary[
            "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_creation"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_activation"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_enforcement"
        ]
        is False
    )


def test_proposal_does_not_create_autonomous_governance_or_authorize_execution():
    result = _build()

    assert result["autonomous_governance_created"] is False
    assert result["autonomous_execution_authorized"] is False
    boundary = result["non_authorization_boundary"]
    assert (
        boundary[
            "star_law_candidate_rule_set_boundary_proposal_ready_is_autonomous_governance"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_set_boundary_proposal_ready_is_autonomous_execution"
        ]
        is False
    )


def test_proposal_does_not_enter_star_law_layer():
    result = _build()

    assert result["enters_star_law_layer"] is False
    assert result["mature_star_law_claimed"] is False


def test_proposal_does_not_authorize_handoff_or_durable_memory_write():
    result = _build()

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False
    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False


def test_proposal_does_not_authorize_openclaw_execution_or_claim_core_completion():
    result = _build()

    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False
    assert result["civilization_core_complete_claimed"] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law candidate rule-set boundary proposal only, not rule creation, not rule activation, and not rule enforcement"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law design boundary review gate complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law design boundary review gate -> Star-Law candidate rule-set boundary proposal"
    )


def test_next_allowed_step_is_v2_32_star_law_candidate_rule_set_boundary_review_gate():
    result = _build()

    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        result["star_law_candidate_rule_set_boundary_proposal"]["next_allowed_step"]
        == READY_NEXT_ALLOWED_STEP
    )
