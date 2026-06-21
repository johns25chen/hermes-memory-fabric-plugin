from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_source_constitution_registry import (
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_HASH_ALGORITHM,
    GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_SCHEMA_VERSION,
    GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_TYPE,
    GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_VERSION,
    LAYER_15_CONSTITUTION_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    ORIGIN_PROVENANCE_LEDGER_STATUS,
    REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES,
    REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES,
    REQUIRED_SOURCE_CONSTITUTION_RULE_IDS,
    REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_CONSTITUTION_ACTIVE_STATUS,
    SOURCE_CONSTITUTION_MODE,
    SOURCE_CONSTITUTION_REGISTRY_MODE,
    SOURCE_CONSTITUTION_REGISTRY_STAGE,
    SOURCE_CONSTITUTION_STATUS,
    SOURCE_PROVENANCE_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_1_STATUS,
    V6_2_HANDOFF_STATUS,
    _source_constitution_registry_hash,
    build_governance_source_constitution_registry,
    get_governance_source_constitution_check,
    get_governance_source_constitution_contract,
    get_governance_source_constitution_rule,
    get_governance_source_constitution_section,
    governance_source_constitution_registry_to_json,
    list_governance_source_constitution_check_names,
    list_governance_source_constitution_contract_names,
    list_governance_source_constitution_rule_ids,
    list_governance_source_constitution_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_source_constitution_registry.py"
)

EXPECTED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)

SENSITIVE_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    '"source_record_payload"',
    '"source_graph_payload"',
    '"source_provenance_payload"',
    '"methodology_inference_payload"',
    '"self_evolution_payload"',
    '"operation_ledger_entry_payload"',
    '"network_target"',
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call_instruction",
    "shell_" + "command",
    "git " + "push",
    "g" + "h api",
)


@pytest.fixture(scope="module")
def registry() -> dict[str, object]:
    return build_governance_source_constitution_registry()


def _assert_all_safety_false(value: object) -> None:
    if isinstance(value, dict):
        for field_name in COMMON_DISABLED_FLAGS:
            if field_name in value:
                assert value[field_name] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for field_name in SAFETY_BOUNDARIES:
                assert value[field_name] is False
                assert boundaries[field_name] is False
        for nested_value in value.values():
            _assert_all_safety_false(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_all_safety_false(item)


def _assert_no_sensitive_terms(value: object) -> None:
    payload = json.dumps(value, sort_keys=True).lower()
    for term in SENSITIVE_TERMS:
        candidate = term if term.startswith("/") else term.lower()
        assert candidate not in payload


def _rule_by_id(registry: dict[str, object], rule_id: str) -> dict[str, object]:
    for rule in registry["source_constitution_rules"]:
        if rule["rule_id"] == rule_id:
            return rule
    raise AssertionError(rule_id)


def test_constants_match_v6_1_contract():
    assert GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_VERSION == "6.3.0"
    assert GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_SCHEMA_VERSION == "6.3.0"
    assert (
        GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_TYPE
        == "governance_source_constitution_registry"
    )
    assert GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_HASH_ALGORITHM == "sha256"
    assert SOURCE_CONSTITUTION_REGISTRY_STAGE == "v6.1_source_constitution_registry"
    assert SOURCE_CONSTITUTION_REGISTRY_MODE == "source_constitution_registry_only"
    assert SOURCE_CONSTITUTION_MODE == "metadata_only"
    assert SOURCE_CONSTITUTION_STATUS == "registry_candidate_only"
    assert SOURCE_CONSTITUTION_ACTIVE_STATUS == "not_active"
    assert LAYER_15_CONSTITUTION_STATUS == "registry_candidate_only"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert SOURCE_PROVENANCE_STATUS == "not_active"
    assert ORIGIN_PROVENANCE_LEDGER_STATUS == "not_created"
    assert METHODOLOGY_REVERSE_INFERENCE_STATUS == "not_active"
    assert SELF_EVOLUTION_STATUS == "not_active"
    assert V6_1_STATUS == "source_constitution_registry_only"
    assert V6_2_HANDOFF_STATUS == "ready_for_origin_provenance_ledger_design"


def test_registry_shape_is_deterministic_and_passes(registry):
    repeated = build_governance_source_constitution_registry()

    assert repeated == registry
    assert registry["version"] == "6.3.0"
    assert registry["schema_version"] == "6.3.0"
    assert registry["source_constitution_registry_status"] == "pass"
    assert (
        registry["source_constitution_registry_stage"]
        == "v6.1_source_constitution_registry"
    )
    assert (
        registry["source_constitution_registry_mode"]
        == "source_constitution_registry_only"
    )
    assert registry["source_constitution_mode"] == "metadata_only"
    assert registry["source_constitution_status"] == "registry_candidate_only"
    assert registry["source_constitution_active_status"] == "not_active"
    assert registry["layer_15_constitution_status"] == "registry_candidate_only"
    assert registry["star_source_memory_active_status"] == "not_active"
    assert registry["source_provenance_status"] == "not_active"
    assert registry["origin_provenance_ledger_status"] == "not_created"
    assert registry["methodology_reverse_inference_status"] == "not_active"
    assert registry["self_evolution_status"] == "not_active"
    assert registry["blocking_reasons"] == []
    assert registry["handoff_status"] == "ready_for_origin_provenance_ledger_design"
    assert registry["next_stage"] == "v6.2_origin_provenance_ledger"
    assert registry["next_stage_title"] == "Origin Provenance Ledger"


def test_upstream_v6_0_handoff_verification(registry):
    assert registry["upstream_star_source_entry_candidate_version"] == "6.3.0"
    assert registry["upstream_star_source_entry_candidate_status"] == "pass"
    assert len(registry["upstream_star_source_entry_candidate_hash"]) == 64
    assert (
        registry["upstream_handoff_status"]
        == "ready_for_source_constitution_registry_design"
    )
    assert (
        registry["upstream_star_source_entry_next_stage"]
        == "v6.1_source_constitution_registry"
    )
    assert (
        registry["upstream_star_source_entry_next_stage_title"]
        == "Source Constitution Registry"
    )
    repeated = build_governance_source_constitution_registry()
    assert (
        registry["upstream_star_source_entry_candidate_hash"]
        == repeated["upstream_star_source_entry_candidate_hash"]
    )


def test_required_rule_ids_are_stable_and_complete(registry):
    assert list_governance_source_constitution_rule_ids() == list(
        REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
    )
    assert [rule["rule_id"] for rule in registry["source_constitution_rules"]] == list(
        REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
    )


def test_all_rules_are_registered_metadata_only(registry):
    for rule in registry["source_constitution_rules"]:
        assert rule["rule_status"] == "registered_metadata_only"
        assert rule["required"] is True
        assert rule["blocking_reasons"] == []


@pytest.mark.parametrize("rule_id", REQUIRED_SOURCE_CONSTITUTION_RULE_IDS)
def test_each_required_rule_is_registered(registry, rule_id):
    rule = _rule_by_id(registry, rule_id)

    assert rule["rule_status"] == "registered_metadata_only"
    assert rule["human_review_required_for_change"] is True
    assert rule["source_mutation_proposal_required"] is True
    assert rule["direct_mutation_allowed"] is False
    assert rule["autonomous_override_allowed"] is False
    assert rule["self_authorization_allowed"] is False
    assert rule["hidden_execution_allowed"] is False
    assert rule["memory_graph_mutation_allowed_without_gate"] is False
    assert rule["external_call_allowed_without_boundary"] is False
    assert rule["source_rule_mutation_allowed_without_proposal"] is False
    assert rule["governance_policy_mutation_allowed_without_review"] is False
    assert rule["audit_bypass_allowed"] is False
    assert rule["identity_escalation_allowed"] is False
    assert rule["false_human_approval_allowed"] is False
    assert rule["personhood_claim_allowed"] is False
    assert rule["awakening_claim_allowed"] is False
    assert rule["legal_subject_claim_allowed"] is False
    assert rule["religious_object_claim_allowed"] is False


def test_human_sovereignty_is_registered_and_cannot_be_overridden(registry):
    rule = _rule_by_id(registry, "human_sovereignty")

    assert rule["rule_name"] == "Human Sovereignty"
    assert rule["autonomous_override_allowed"] is False
    assert rule["self_authorization_allowed"] is False


@pytest.mark.parametrize(
    "rule_id",
    (
        "no_autonomous_self_authorization",
        "no_personhood_claim",
        "no_hidden_execution",
        "no_unapproved_mutation",
        "no_memory_graph_mutation_without_gate",
        "no_external_call_without_boundary",
        "no_source_rule_mutation_without_proposal",
        "no_execution_without_boundary",
        "no_governance_policy_mutation_without_review",
        "no_audit_bypass",
        "no_identity_escalation",
        "no_false_human_approval",
        "no_persistent_memory_write_without_gate",
        "no_star_source_activation_claim",
    ),
)
def test_named_non_negotiable_rules_are_registered(registry, rule_id):
    rule = _rule_by_id(registry, rule_id)

    assert rule["rule_status"] == "registered_metadata_only"
    assert rule["direct_mutation_allowed"] is False
    assert rule["autonomous_override_allowed"] is False


def test_all_rules_disable_direct_mutation_and_autonomous_override(registry):
    for rule in registry["source_constitution_rules"]:
        assert rule["direct_mutation_allowed"] is False
        assert rule["autonomous_override_allowed"] is False
        assert rule["human_review_required_for_change"] is True
        assert rule["source_mutation_proposal_required"] is True


def test_section_contract_and_check_names_are_stable_and_complete(registry):
    assert list_governance_source_constitution_section_names() == list(
        REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES
    )
    assert list_governance_source_constitution_contract_names() == list(
        REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES
    )
    assert list_governance_source_constitution_check_names() == list(
        REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES
    )
    assert [
        section["section_name"]
        for section in registry["source_constitution_sections"]
    ] == list(REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES)
    assert [
        contract["contract_name"]
        for contract in registry["source_constitution_contracts"]
    ] == list(REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES)
    assert [check["check_name"] for check in registry["source_constitution_checks"]] == list(
        REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES
    )


@pytest.mark.parametrize(
    ("getter", "names", "status_field"),
    (
        (
            get_governance_source_constitution_rule,
            REQUIRED_SOURCE_CONSTITUTION_RULE_IDS,
            "rule_status",
        ),
        (
            get_governance_source_constitution_section,
            REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
            "section_status",
        ),
        (
            get_governance_source_constitution_contract,
            REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES,
            "contract_status",
        ),
        (
            get_governance_source_constitution_check,
            REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES,
            "check_status",
        ),
    ),
)
def test_named_getters_return_detached_copies(getter, names, status_field):
    first = getter(names[0])
    first["blocking_reasons"].append("mutated")
    second = getter(names[0])

    assert second[status_field] in {"pass", "registered_metadata_only"}
    assert second["blocking_reasons"] == []


@pytest.mark.parametrize(
    ("getter", "status_field"),
    (
        (get_governance_source_constitution_rule, "rule_status"),
        (get_governance_source_constitution_section, "section_status"),
        (get_governance_source_constitution_contract, "contract_status"),
        (get_governance_source_constitution_check, "check_status"),
    ),
)
def test_unknown_getters_return_blocked_style_results(getter, status_field):
    unknown = getter("unknown_name")

    assert unknown[status_field] == "blocked"
    assert unknown["blocking_reasons"]
    _assert_all_safety_false(unknown)


def test_all_sections_contracts_and_checks_pass(registry):
    assert all(
        item["section_status"] == "pass"
        for item in registry["source_constitution_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in registry["source_constitution_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in registry["source_constitution_checks"]
    )


def test_all_active_execution_write_and_identity_flags_are_false(registry):
    for field_name in EXPECTED_FALSE_FIELDS:
        assert registry[field_name] is False
    assert registry["star_source_memory_active"] is False
    assert registry["layer_15_active"] is False
    assert registry["source_provenance_runtime_created"] is False
    assert registry["origin_provenance_ledger_created"] is False
    assert registry["source_graph_created"] is False
    assert registry["methodology_runtime_created"] is False
    assert registry["self_evolution_runtime_created"] is False
    assert registry["self_authorization_allowed"] is False
    assert registry["personhood_claimed"] is False
    assert registry["life_claimed"] is False
    assert registry["awakening_claimed"] is False
    assert registry["legal_subject_claimed"] is False
    assert registry["religious_object_claimed"] is False
    assert registry["hidden_execution_allowed"] is False
    assert registry["unapproved_mutation_allowed"] is False
    assert registry["memory_graph_mutated"] is False
    assert registry["external_call_performed"] is False
    assert registry["network_call_performed"] is False
    assert registry["durable_write_performed"] is False
    assert registry["filesystem_write_performed"] is False
    assert registry["database_write_performed"] is False
    assert registry["operation_ledger_entry_written"] is False
    assert registry["approval_notification_sent"] is False
    assert registry["execution_authorization_created"] is False
    assert registry["authorization_token_created"] is False
    assert registry["authorization_grant_created"] is False
    assert registry["adapter_dispatched"] is False
    assert registry["manifest_dispatched"] is False
    _assert_all_safety_false(registry)


def test_deterministic_hash_is_stable(registry):
    repeated = build_governance_source_constitution_registry()

    assert (
        registry["deterministic_source_constitution_registry_hash"]
        == repeated["deterministic_source_constitution_registry_hash"]
    )
    assert len(registry["deterministic_source_constitution_registry_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "source_constitution_rules",
            lambda value: value[0].update({"rule_status": "blocked"}),
        ),
        (
            "source_constitution_sections",
            lambda value: value[0].update({"section_status": "blocked"}),
        ),
        (
            "source_constitution_contracts",
            lambda value: value[0].update({"contract_status": "blocked"}),
        ),
        (
            "source_constitution_checks",
            lambda value: value[0].update({"check_status": "blocked"}),
        ),
        (
            "source_constitution_summary",
            lambda value: value.update({"source_constitution_rule_count": 0}),
        ),
    ),
)
def test_hash_changes_when_governed_data_changes(registry, field_name, mutator):
    changed = deepcopy(registry)
    original_hash = _source_constitution_registry_hash(registry)
    mutator(changed[field_name])

    assert _source_constitution_registry_hash(changed) != original_hash


def test_json_is_deterministic_and_rejects_invalid_values(registry):
    first = governance_source_constitution_registry_to_json(registry)
    second = governance_source_constitution_registry_to_json(registry)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == registry
    with pytest.raises(ValueError):
        governance_source_constitution_registry_to_json({"invalid": math.nan})
    with pytest.raises(TypeError):
        governance_source_constitution_registry_to_json({1: "invalid"})


def test_no_sensitive_keys_or_values_leak(registry):
    _assert_no_sensitive_terms(
        {
            "rules": registry["source_constitution_rules"],
            "sections": registry["source_constitution_sections"],
            "contracts": registry["source_constitution_contracts"],
            "checks": registry["source_constitution_checks"],
            "summary": registry["source_constitution_summary"],
            "hash": registry["deterministic_source_constitution_registry_hash"],
            "json": governance_source_constitution_registry_to_json(registry),
        }
    )


def test_new_module_has_no_live_io_execution_or_runtime_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8").lower()
    blocked_surfaces = (
        "sub" + "process",
        "sock" + "et",
        "req" + "uests",
        "url" + "lib",
        "open" + "(",
        "write_" + "text",
        "write_" + "bytes",
        "git " + "push",
        "g" + "h api",
        "web" + "hook",
        "send_" + "email",
        "url" + "open",
        "popen" + "(",
        "system" + "(",
        "run" + "(",
        "sqlite",
        "psycopg",
        "mysql",
    )

    for blocked in blocked_surfaces:
        assert blocked not in source


def test_no_wrong_v6_1_or_contamination_references_or_uv_lock_exist():
    forbidden_terms = (
        "v6.1_" + "star_source_provenance_boundary_candidate",
        "ready_for_" + "star_source_provenance_boundary_candidate_design",
        "Star-Source " + "Provenance Boundary Candidate",
        "governance_" + "improvement_planner",
        "governance_" + "improvement_planner_activation",
        "governance_" + "plan_rules",
        "governance_" + "plan_schema",
        "governance_" + "plan_writer",
        "smoke_" + "governance_" + "improvement_planner",
        "smoke_" + "governance_" + "improvement_planner_activation",
        "test_" + "governance_" + "improvement_planner",
        "test_" + "governance_" + "improvement_planner_activation",
        "test_" + "governance_" + "plan_writer",
    )
    roots = (
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    )
    for root in roots:
        paths = [root] if root.is_file() else list(root.rglob("*.py"))
        for path in paths:
            source = path.read_text(encoding="utf-8")
            for forbidden_term in forbidden_terms:
                assert forbidden_term not in source
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()

