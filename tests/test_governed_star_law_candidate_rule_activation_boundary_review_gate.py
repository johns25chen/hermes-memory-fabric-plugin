from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_activation_boundary_review_gate import (
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_PROPOSED_CANDIDATE_RULE_ACTIVATION_BOUNDARY_KEYS,
    build_governed_star_law_candidate_rule_activation_boundary_review_gate,
    governed_star_law_candidate_rule_activation_boundary_review_gate_to_json,
)
from tests.test_governed_star_law_candidate_rule_activation_boundary_proposal import (
    _build as _valid_v2_33_proposal,
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

REVIEW_GATE_FALSE_FLAGS = [
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

UNSAFE_TOP_LEVEL_FIELDS = [
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
    "mature_star_law_claimed",
    "enters_star_soul_layer",
    "enters_star_cosmos_layer",
    "enters_star_source_layer",
    "civilization_core_complete_claimed",
    "star_hub_handoff_authorized",
    "handoff_authorized",
    "handoff_performed",
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

UNSAFE_PROPOSAL_FIELDS = [
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


def _valid_proposal_report() -> dict[str, object]:
    return deepcopy(_valid_v2_33_proposal())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_activation_boundary_review_gate(
        report or _valid_proposal_report()
    )


def test_valid_candidate_rule_activation_boundary_proposal_creates_star_law_candidate_rule_activation_boundary_review_gate_ready():
    result = _build()

    assert result["version"] == "2.34.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_activation_boundary_review_gate_ready"
    )
    assert result["source_proposal_version"] == "2.33.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["review_gate_only"] is True
    assert result["candidate_rule_activation_boundary_review_gate_only"] is True
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate_only"] is True
    )
    assert (
        result["candidate_rule_activation_boundary_reviewed_for_human_review_only"]
        is True
    )
    assert (
        result[
            "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert all(check["passed"] is True for check in result["review_gate_checks"])
    assert result["blocking_reasons"] == []
    review_gate = result["star_law_candidate_rule_activation_boundary_review_gate"]
    assert (
        review_gate["review_status"]
        == "star_law_candidate_rule_activation_boundary_reviewed_for_human_review_only"
    )
    assert (
        review_gate["boundary_type"]
        == "star_law_candidate_rule_activation_boundary_review_gate"
    )
    assert review_gate["source_proposal_version"] == "2.33.0"
    assert review_gate["candidate_rule_activation_boundary_reviewed"] is True
    assert (
        review_gate["candidate_rule_activation_boundary_structurally_review_ready"]
        is True
    )
    assert (
        review_gate[
            "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        review_gate[
            "source_star_law_candidate_rule_activation_boundary_proposal_valid"
        ]
        is True
    )


def test_reviewed_chain_versions_exactly_match_v2_9_0_through_v2_33_0():
    result = _build()

    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert REVIEWED_CHAIN_VERSIONS == [
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
        "v2.33.0",
    ]
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate"][
            "reviewed_chain_versions"
        ]
        == REVIEWED_CHAIN_VERSIONS
    )


def test_reviewed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_33_0():
    result = _build()

    assert (
        result["reviewed_star_hub_chain_versions"]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )
    assert REVIEWED_STAR_HUB_CHAIN_VERSIONS == [
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
        "v2.33.0",
    ]
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate"][
            "reviewed_star_hub_chain_versions"
        ]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )


def test_blocked_candidate_rule_activation_boundary_proposal_blocks_review_gate():
    report = _valid_proposal_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["candidate_rule_activation_boundary_reviewed_for_human_review_only"]
        is False
    )
    assert (
        result[
            "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only"
        ]
        is False
    )
    review_gate = result["star_law_candidate_rule_activation_boundary_review_gate"]
    assert review_gate["candidate_rule_activation_boundary_reviewed"] is False
    assert (
        review_gate["candidate_rule_activation_boundary_structurally_review_ready"]
        is False
    )
    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert (
        result["reviewed_star_hub_chain_versions"]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize("field", UNSAFE_TOP_LEVEL_FIELDS)
def test_unsafe_authorization_or_execution_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["candidate_rule_activation_boundary_reviewed_for_human_review_only"]
        is False
    )
    assert (
        result[
            "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only"
        ]
        is False
    )
    for safe_field in TOP_LEVEL_FALSE_FLAGS:
        assert result[safe_field] is False
    assert result["civilization_core_complete_claimed"] is False
    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


@pytest.mark.parametrize("field", UNSAFE_PROPOSAL_FIELDS)
def test_unsafe_source_proposal_nested_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    proposal = report["star_law_candidate_rule_activation_boundary_proposal"]
    assert isinstance(proposal, dict)
    proposal[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate"][
            "source_star_law_candidate_rule_activation_boundary_proposal_valid"
        ]
        is False
    )


def test_unsafe_authorization_flag_blocks_review_gate():
    report = _valid_proposal_report()
    report["authorization_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_candidate_rule_activation_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["candidate_rule_activation_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_candidate_rule_activation_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["candidate_rule_activation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_candidate_rule_creation_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_candidate_rules_created"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_candidate_rule_activation_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_candidate_rules_activated"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_creation_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_rules_created"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_activation_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_rules_activated"] = True

    assert _build(report)["status"] == "blocked"


def test_star_law_rule_enforcement_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_rules_enforced"] = True

    assert _build(report)["status"] == "blocked"


def test_self_enforcing_law_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_law_self_enforcing_law_created"] = True

    assert _build(report)["status"] == "blocked"


def test_autonomous_governance_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["autonomous_governance_created"] = True

    assert _build(report)["status"] == "blocked"


def test_autonomous_execution_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["autonomous_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_self_executing_policy_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["self_executing_policy_active"] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ],
)
def test_entering_star_law_star_soul_star_cosmos_or_star_source_claim_blocks_review_gate(
    field: str,
):
    report = _valid_proposal_report()
    report[field] = True

    assert _build(report)["status"] == "blocked"


def test_civilization_core_completion_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["civilization_core_complete_claimed"] = True

    assert _build(report)["status"] == "blocked"


def test_star_hub_handoff_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["star_hub_handoff_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_scheduling_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["scheduling_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_scheduling_performed_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["scheduling_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_performed_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["dry_run_performed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_executed_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["dry_run_executed"] = True

    assert _build(report)["status"] == "blocked"


def test_dry_run_execution_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["dry_run_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_memory_write_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["memory_write_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_memory_graph_mutation_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["memory_graph_mutation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_operation_ledger_creation_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["operation_ledger_creation_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_openclaw_execution_authorization_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["openclaw_execution_authorized"] = True

    assert _build(report)["status"] == "blocked"


def test_approval_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_real_human_decision_claim_blocks_review_gate():
    report = _valid_proposal_report()
    report["real_human_decision_recorded"] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_chain_versions"] = ["v2.9.0", "v2.33.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS


def test_malformed_proposed_star_hub_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_star_hub_chain_versions"] = ["v2.19.0", "v2.33.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["reviewed_star_hub_chain_versions"] == REVIEWED_STAR_HUB_CHAIN_VERSIONS


def test_reviewed_candidate_rule_activation_boundaries_are_review_only_and_non_authorizing():
    result = _build()
    boundaries = result["reviewed_candidate_rule_activation_boundaries"]

    assert isinstance(boundaries, dict)
    assert set(boundaries) == SOURCE_PROPOSED_CANDIDATE_RULE_ACTIVATION_BOUNDARY_KEYS
    for boundary in boundaries.values():
        assert boundary["review_only"] is True
        for key, value in boundary.items():
            if key != "review_only":
                assert value is not True
    serialized = json.dumps(boundaries, ensure_ascii=True, sort_keys=True).lower()
    for forbidden_claim in [
        "candidate rules are activated",
        "candidate rules are created",
        "star-law rules are created",
        "star-law rules are active",
        "star-law rules are enforced",
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
    report = _valid_proposal_report()
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
    serialized = governed_star_law_candidate_rule_activation_boundary_review_gate_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    assert "Sensitive fields were omitted" in serialized
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", TOP_LEVEL_FALSE_FLAGS)
def test_review_gate_preserves_top_level_non_authorization_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", REVIEW_GATE_FALSE_FLAGS)
def test_star_law_candidate_rule_activation_boundary_review_gate_preserves_non_authorization_flags(
    field: str,
):
    assert (
        _build()["star_law_candidate_rule_activation_boundary_review_gate"][field]
        is False
    )


def test_review_gate_does_not_activate_candidate_rules():
    result = _build()

    assert result["candidate_rule_activation_performed"] is False
    assert result["candidate_rule_activation_authorized"] is False
    review_gate = result["star_law_candidate_rule_activation_boundary_review_gate"]
    assert review_gate["candidate_rule_activation_performed"] is False
    assert review_gate["candidate_rule_activation_authorized"] is False


def test_review_gate_does_not_authorize_candidate_rule_activation():
    result = _build()

    assert result["candidate_rule_activation_authorized"] is False
    assert (
        result["non_authorization_boundary"][
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_candidate_rule_activation"
        ]
        is False
    )


def test_review_gate_does_not_create_candidate_rules():
    result = _build()

    assert result["star_law_candidate_rules_created"] is False
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate"][
            "star_law_candidate_rules_created"
        ]
        is False
    )


def test_review_gate_does_not_create_activate_or_enforce_star_law_rules():
    result = _build()

    assert result["star_law_rules_created"] is False
    assert result["star_law_rules_activated"] is False
    assert result["star_law_rules_enforced"] is False
    boundary = result["non_authorization_boundary"]
    assert (
        boundary[
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_rule_creation"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_rule_activation"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_rule_enforcement"
        ]
        is False
    )


def test_review_gate_does_not_create_autonomous_governance_or_authorize_execution():
    result = _build()

    assert result["autonomous_governance_created"] is False
    assert result["autonomous_execution_authorized"] is False
    boundary = result["non_authorization_boundary"]
    assert (
        boundary[
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_autonomous_governance"
        ]
        is False
    )
    assert (
        boundary[
            "star_law_candidate_rule_activation_boundary_review_gate_ready_is_autonomous_execution"
        ]
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
    assert mapping["primary_layer_status"] == (
        "Star-Law candidate rule activation boundary review gate only, not candidate rule activation, not rule activation, and not rule enforcement"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law candidate rule activation boundary proposal complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law candidate rule activation boundary proposal -> Star-Law candidate rule activation boundary review gate"
    )


def test_next_allowed_step_is_v2_35_0_star_law_candidate_rule_enforcement_boundary_proposal():
    result = _build()

    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        result["star_law_candidate_rule_activation_boundary_review_gate"][
            "next_allowed_step"
        ]
        == READY_NEXT_ALLOWED_STEP
    )


def test_review_components_match_required_activation_boundary_review_components():
    components = _build()["star_law_candidate_rule_activation_boundary_review_gate"][
        "star_law_candidate_rule_activation_boundary_review_components"
    ]

    assert set(components) == {
        "source_candidate_rule_activation_boundary_proposal_review",
        "candidate_rule_activation_eligibility_boundary_review",
        "candidate_rule_activation_precondition_boundary_review",
        "candidate_rule_non_activation_boundary_review",
        "candidate_rule_non_enforcement_boundary_review",
        "activation_human_operator_control_boundary_review",
        "activation_evidence_lineage_boundary_review",
        "activation_auditability_boundary_review",
        "activation_rollback_boundary_review",
        "activation_suspension_boundary_review",
        "self_enforcing_law_non_activation_boundary_review",
        "autonomous_governance_non_creation_boundary_review",
        "autonomous_execution_non_authorization_boundary_review",
        "memory_write_non_authorization_boundary_review",
        "memory_graph_mutation_non_authorization_boundary_review",
        "operation_ledger_non_creation_boundary_review",
        "openclaw_execution_non_authorization_boundary_review",
        "approval_non_authorization_boundary_review",
        "human_operator_final_authority_boundary_review",
        "fifteen_memory_layers_boundary_review",
    }
    assert set(components.values()) == {"reviewed_for_human_review_only"}


def test_report_is_json_serializable():
    result = _build()
    payload = governed_star_law_candidate_rule_activation_boundary_review_gate_to_json(
        result
    )
    decoded = json.loads(payload)

    assert (
        decoded["status"]
        == "star_law_candidate_rule_activation_boundary_review_gate_ready"
    )
