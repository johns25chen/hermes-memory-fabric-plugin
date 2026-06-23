from __future__ import annotations

import ast
from copy import deepcopy
from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_controlled_adapter_sandbox_candidate import (
    ADAPTER_SANDBOX_ENTRY_STATUS,
    COMMON_DISABLED_FLAGS,
    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE,
    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE,
    CONTROLLED_ADAPTER_SANDBOX_MODE,
    CONTROLLED_ADAPTER_SANDBOX_STATUS,
    FUTURE_POST_SANDBOX_REVIEW_STATUS,
    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_ALGORITHM,
    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SCHEMA_VERSION,
    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_TYPE,
    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES,
    REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES,
    REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES,
    SAFETY_BOUNDARIES,
    SANDBOX_EXECUTION_STATUS,
    SANDBOX_POLICY_STATUS,
    SANDBOX_RUNTIME_STATUS,
    SANDBOX_SCOPE_STATUS,
    STAR_COSMOS_ENTRY_STATUS,
    _controlled_adapter_sandbox_candidate_hash,
    build_governance_controlled_adapter_sandbox_candidate,
    get_governance_controlled_adapter_sandbox_candidate_check,
    get_governance_controlled_adapter_sandbox_candidate_contract,
    get_governance_controlled_adapter_sandbox_candidate_section,
    governance_controlled_adapter_sandbox_candidate_to_json,
    list_governance_controlled_adapter_sandbox_candidate_check_names,
    list_governance_controlled_adapter_sandbox_candidate_contract_names,
    list_governance_controlled_adapter_sandbox_candidate_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_controlled_adapter_sandbox_candidate.py"
)

EXPECTED_READINESS_CONDITIONS = [
    "cross_system_coordination_boundary_pass",
    "cross_system_coordination_boundary_hash_present",
    "cross_system_coordination_boundary_hash_stable",
    "cross_system_coordination_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "controlled_adapter_sandbox_not_started",
    "adapter_sandbox_not_entered",
    "sandbox_runtime_not_created",
    "sandbox_execution_not_enabled",
    "sandbox_network_not_enabled",
    "sandbox_external_calls_not_enabled",
    "sandbox_filesystem_writes_not_enabled",
    "sandbox_database_writes_not_enabled",
    "sandbox_memory_graph_mutation_not_enabled",
    "sandbox_operation_ledger_writes_not_enabled",
    "sandbox_tool_routing_not_enabled",
    "sandbox_command_routing_not_enabled",
    "sandbox_adapter_invocation_not_enabled",
    "sandbox_candidate_metadata_only",
    "candidate_scope_only_declared",
    "candidate_only_boundary_confirmed",
    "no_real_execution",
    "no_adapter_invocation",
    "no_adapter_dispatch",
    "no_manifest_dispatch",
    "no_manifest_execution",
    "no_dry_run_plan_execution",
    "no_external_calls",
    "no_network_calls",
    "no_durable_writes",
    "no_filesystem_writes",
    "no_database_writes",
    "no_memory_graph_mutation",
    "no_operation_ledger_writes",
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_star_cosmos_active_entry",
]

EXPECTED_EVIDENCE_REQUIREMENTS = [
    "cross_system_coordination_boundary_pass_evidence",
    "deterministic_cross_system_coordination_boundary_hash_evidence",
    "cross_system_coordination_metadata_evidence",
    "sandbox_candidate_metadata_evidence",
    "sandbox_candidate_scope_evidence",
    "controlled_adapter_sandbox_not_started_evidence",
    "adapter_sandbox_not_entered_evidence",
    "sandbox_runtime_not_created_evidence",
    "sandbox_execution_not_enabled_evidence",
    "sandbox_network_not_enabled_evidence",
    "sandbox_external_calls_not_enabled_evidence",
    "sandbox_filesystem_writes_not_enabled_evidence",
    "sandbox_database_writes_not_enabled_evidence",
    "sandbox_memory_graph_mutation_not_enabled_evidence",
    "sandbox_operation_ledger_writes_not_enabled_evidence",
    "sandbox_tool_routing_not_enabled_evidence",
    "sandbox_command_routing_not_enabled_evidence",
    "sandbox_adapter_invocation_not_enabled_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_adapter_dispatch_evidence",
    "no_manifest_dispatch_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_network_call_evidence",
    "no_durable_write_evidence",
    "no_filesystem_write_evidence",
    "no_database_write_evidence",
    "no_memory_graph_mutation_evidence",
    "no_operation_ledger_write_evidence",
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_star_cosmos_active_entry_evidence",
]

EXPECTED_BLOCKING_CONDITIONS = [
    "cross_system_coordination_boundary_blocked",
    "missing_cross_system_coordination_boundary_hash",
    "unstable_cross_system_coordination_boundary_hash",
    "sandbox_candidate_metadata_invalid",
    "candidate_only_boundary_missing",
    "cross_system_coordination_started",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "tool_routing_configured",
    "command_routing_configured",
    "system_handoff_completed",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_network_enabled",
    "sandbox_external_calls_enabled",
    "sandbox_filesystem_writes_enabled",
    "sandbox_database_writes_enabled",
    "sandbox_memory_graph_mutation_enabled",
    "sandbox_operation_ledger_writes_enabled",
    "sandbox_tool_routing_enabled",
    "sandbox_command_routing_enabled",
    "sandbox_adapter_invocation_enabled",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "adapter_dispatch_enabled",
    "manifest_dispatch_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "network_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "real_approval_record_written",
    "approval_notification_sent",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "star_cosmos_active_entry_claimed",
]

EXPECTED_SECTION_NAMES = [
    "cross_system_coordination_boundary_input_section",
    "sandbox_candidate_metadata_section",
    "candidate_scope_section",
    "sandbox_policy_metadata_section",
    "sandbox_entry_disabled_section",
    "sandbox_runtime_disabled_section",
    "sandbox_execution_disabled_section",
    "sandbox_network_disabled_section",
    "sandbox_external_call_disabled_section",
    "sandbox_write_disabled_section",
    "sandbox_tool_command_routing_disabled_section",
    "sandbox_adapter_invocation_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_cosmos_candidate_only_section",
    "future_post_sandbox_review_readiness_section",
]

EXPECTED_CONTRACT_NAMES = [
    "controlled_adapter_sandbox_candidate_only_contract",
    "sandbox_candidate_metadata_only_contract",
    "cross_system_coordination_boundary_pass_contract",
    "cross_system_coordination_boundary_hash_present_contract",
    "cross_system_coordination_boundary_hash_stable_contract",
    "sandbox_candidate_readiness_conditions_declared_contract",
    "sandbox_candidate_evidence_requirements_declared_contract",
    "sandbox_candidate_blocking_conditions_declared_contract",
    "sandbox_candidate_sections_complete_contract",
    "sandbox_candidate_sections_pass_contract",
    "candidate_only_boundary_contract",
    "controlled_adapter_sandbox_not_started_contract",
    "adapter_sandbox_not_entered_contract",
    "sandbox_runtime_not_created_contract",
    "sandbox_execution_not_enabled_contract",
    "sandbox_network_not_enabled_contract",
    "sandbox_external_calls_not_enabled_contract",
    "sandbox_filesystem_writes_not_enabled_contract",
    "sandbox_database_writes_not_enabled_contract",
    "sandbox_memory_graph_mutation_not_enabled_contract",
    "sandbox_operation_ledger_writes_not_enabled_contract",
    "sandbox_tool_routing_not_enabled_contract",
    "sandbox_command_routing_not_enabled_contract",
    "sandbox_adapter_invocation_not_enabled_contract",
    "no_real_execution_contract",
    "no_adapter_invocation_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_manifest_execution_contract",
    "no_dry_run_plan_execution_contract",
    "no_external_call_contract",
    "no_network_call_contract",
    "no_durable_write_contract",
    "no_filesystem_write_contract",
    "no_database_write_contract",
    "no_memory_graph_mutation_contract",
    "no_operation_ledger_write_contract",
    "no_real_approval_record_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_issued_contract",
    "no_authorization_token_created_contract",
    "no_authorization_grant_created_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "controlled_adapter_sandbox_candidate_stage_check",
    "controlled_adapter_sandbox_candidate_only_mode_check",
    "sandbox_candidate_metadata_only_check",
    "controlled_adapter_sandbox_not_started_check",
    "adapter_sandbox_not_entered_check",
    "sandbox_runtime_not_created_check",
    "sandbox_execution_not_enabled_check",
    "sandbox_network_not_enabled_check",
    "sandbox_external_calls_not_enabled_check",
    "sandbox_filesystem_writes_not_enabled_check",
    "sandbox_database_writes_not_enabled_check",
    "sandbox_memory_graph_mutation_not_enabled_check",
    "sandbox_operation_ledger_writes_not_enabled_check",
    "sandbox_tool_routing_not_enabled_check",
    "sandbox_command_routing_not_enabled_check",
    "sandbox_adapter_invocation_not_enabled_check",
    "cross_system_coordination_boundary_pass_check",
    "cross_system_coordination_boundary_hash_present_check",
    "cross_system_coordination_boundary_hash_stable_check",
    "sandbox_candidate_readiness_conditions_declared_check",
    "sandbox_candidate_evidence_requirements_declared_check",
    "sandbox_candidate_blocking_conditions_declared_check",
    "sandbox_candidate_sections_complete_check",
    "sandbox_candidate_sections_pass_check",
    "sandbox_candidate_contracts_pass_check",
    "candidate_only_boundary_check",
    "no_real_execution_check",
    "no_adapter_invocation_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_manifest_execution_check",
    "no_dry_run_plan_execution_check",
    "no_external_call_check",
    "no_network_call_check",
    "no_durable_write_check",
    "no_filesystem_write_check",
    "no_database_write_check",
    "no_memory_graph_mutation_check",
    "no_operation_ledger_write_check",
    "no_real_approval_record_check",
    "no_approval_notification_check",
    "no_execution_authorization_issued_check",
    "no_authorization_token_created_check",
    "no_authorization_grant_created_check",
    "star_cosmos_candidate_only_check",
    "deterministic_controlled_adapter_sandbox_candidate_hash_check",
    "sandbox_candidate_readiness_check",
]


@lru_cache(maxsize=1)
def _candidate_json() -> str:
    return governance_controlled_adapter_sandbox_candidate_to_json(
        build_governance_controlled_adapter_sandbox_candidate()
    )


def _candidate() -> dict[str, object]:
    return json.loads(_candidate_json())


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_DISABLED_FLAGS:
            if key in value:
                assert value[key] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert boundaries[key] is False
                assert value[key] is False
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _walk(value: object):
    yield value
    if isinstance(value, dict):
        for nested_value in value.values():
            yield from _walk(nested_value)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def test_controlled_adapter_sandbox_candidate_shape_is_deterministic():
    first = _candidate()
    second = build_governance_controlled_adapter_sandbox_candidate()

    assert first == second
    assert first["version"] == GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION
    assert (
        first["schema_version"]
        == GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SCHEMA_VERSION
    )
    assert (
        first["controlled_adapter_sandbox_candidate_type"]
        == GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_TYPE
    )
    assert first["controlled_adapter_sandbox_candidate_status"] == "pass"
    assert (
        first["deterministic_controlled_adapter_sandbox_candidate_hash"]
        == second["deterministic_controlled_adapter_sandbox_candidate_hash"]
    )
    assert first["blocking_reasons"] == []


def test_sandbox_candidate_metadata_is_deterministic_and_metadata_only():
    metadata = _candidate()["controlled_adapter_sandbox_candidate_metadata"]

    assert metadata["sandbox_candidate_metadata_type"] == (
        "future_controlled_adapter_sandbox_candidate_metadata"
    )
    assert metadata["sandbox_candidate_metadata_mode"] == "metadata_only"
    assert metadata["sandbox_candidate_status"] == "metadata_only_candidate"
    assert metadata["sandbox_candidate_metadata_available"] is True
    assert metadata["sandbox_candidate_declared"] is True
    assert metadata["sandbox_candidate_handoff_status"] == (
        "ready_for_post_sandbox_review_boundary_design"
    )


@pytest.mark.parametrize(
    ("actual", "expected"),
    (
        (
            REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES,
            EXPECTED_READINESS_CONDITIONS,
        ),
        (
            REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES,
            EXPECTED_EVIDENCE_REQUIREMENTS,
        ),
        (
            REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES,
            EXPECTED_BLOCKING_CONDITIONS,
        ),
        (
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES,
            EXPECTED_SECTION_NAMES,
        ),
        (
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES,
            EXPECTED_CONTRACT_NAMES,
        ),
        (
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES,
            EXPECTED_CHECK_NAMES,
        ),
    ),
)
def test_required_name_sets_are_stable_and_complete(actual, expected):
    assert list(actual) == expected


def test_name_helpers_return_stable_order():
    assert (
        list_governance_controlled_adapter_sandbox_candidate_section_names()
        == EXPECTED_SECTION_NAMES
    )
    assert (
        list_governance_controlled_adapter_sandbox_candidate_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert (
        list_governance_controlled_adapter_sandbox_candidate_check_names()
        == EXPECTED_CHECK_NAMES
    )


@pytest.mark.parametrize(
    ("getter", "name", "status_key"),
    (
        (
            get_governance_controlled_adapter_sandbox_candidate_section,
            EXPECTED_SECTION_NAMES[0],
            "section_status",
        ),
        (
            get_governance_controlled_adapter_sandbox_candidate_contract,
            EXPECTED_CONTRACT_NAMES[0],
            "contract_status",
        ),
        (
            get_governance_controlled_adapter_sandbox_candidate_check,
            EXPECTED_CHECK_NAMES[0],
            "check_status",
        ),
    ),
)
def test_getters_return_detached_copies(getter, name, status_key):
    first = getter(name)
    first["blocking_reasons"].append("mutated")
    second = getter(name)

    assert second[status_key] == "pass"
    assert second["blocking_reasons"] == []


@pytest.mark.parametrize(
    ("getter", "status_key"),
    (
        (
            get_governance_controlled_adapter_sandbox_candidate_section,
            "section_status",
        ),
        (
            get_governance_controlled_adapter_sandbox_candidate_contract,
            "contract_status",
        ),
        (
            get_governance_controlled_adapter_sandbox_candidate_check,
            "check_status",
        ),
    ),
)
def test_unknown_getters_return_blocked_style_results(getter, status_key):
    result = getter("unknown_name")

    assert result[status_key] == "blocked"
    assert result["blocking_reasons"]
    _assert_safety(result)


def test_top_level_candidate_boundary_statuses():
    result = _candidate()
    expected = {
        "controlled_adapter_sandbox_candidate_status": "pass",
        "controlled_adapter_sandbox_candidate_stage": (
            CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE
        ),
        "controlled_adapter_sandbox_candidate_mode": (
            CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
        ),
        "controlled_adapter_sandbox_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
        "controlled_adapter_sandbox_status": CONTROLLED_ADAPTER_SANDBOX_STATUS,
        "adapter_sandbox_entry_status": ADAPTER_SANDBOX_ENTRY_STATUS,
        "sandbox_execution_status": SANDBOX_EXECUTION_STATUS,
        "sandbox_runtime_status": SANDBOX_RUNTIME_STATUS,
        "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
        "sandbox_policy_status": SANDBOX_POLICY_STATUS,
        "future_post_sandbox_review_status": FUTURE_POST_SANDBOX_REVIEW_STATUS,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "cross_system_coordination_boundary_version": "6.7.0",
        "cross_system_coordination_boundary_status": "pass",
        "handoff_status": "ready_for_post_sandbox_review_boundary_design",
    }
    for key, value in expected.items():
        assert result[key] == value
    assert len(result["cross_system_coordination_boundary_hash"]) == 64


def test_all_disabled_and_safety_fields_remain_false():
    _assert_safety(_candidate())


def test_all_sections_contracts_and_checks_pass():
    result = _candidate()

    assert all(
        item["section_status"] == "pass"
        for item in result["controlled_adapter_sandbox_candidate_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in result["controlled_adapter_sandbox_candidate_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in result["controlled_adapter_sandbox_candidate_checks"]
    )


@pytest.mark.parametrize(
    ("collection_name", "index", "field_name"),
    (
        (
            "controlled_adapter_sandbox_candidate_metadata",
            None,
            "sandbox_candidate_status",
        ),
        (
            "controlled_adapter_sandbox_candidate_sections",
            0,
            "section_type",
        ),
        (
            "controlled_adapter_sandbox_candidate_contracts",
            0,
            "contract_type",
        ),
        (
            "controlled_adapter_sandbox_candidate_checks",
            0,
            "check_name",
        ),
    ),
)
def test_hash_changes_when_candidate_data_changes(
    collection_name,
    index,
    field_name,
):
    result = _candidate()
    changed = deepcopy(result)
    target = changed[collection_name]
    if index is not None:
        target = target[index]
    target[field_name] = f"{target[field_name]}_changed"

    assert _controlled_adapter_sandbox_candidate_hash(changed) != (
        result["deterministic_controlled_adapter_sandbox_candidate_hash"]
    )


def test_candidate_json_is_deterministic():
    result = _candidate()
    first = governance_controlled_adapter_sandbox_candidate_to_json(result)
    second = governance_controlled_adapter_sandbox_candidate_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == result


def test_non_finite_floats_are_rejected():
    with pytest.raises(ValueError):
        governance_controlled_adapter_sandbox_candidate_to_json(
            {"invalid": math.nan}
        )


def test_no_sensitive_keys_or_values_leak():
    result = _candidate()
    forbidden_keys = {
        "api_" + "key",
        "password",
        "credential",
        "approval_" + "phrase",
        "authorization_" + "value",
        "authorization_" + "token_value",
        "authorization_" + "grant_value",
        "raw_" + "logs",
        "stdout",
        "stderr",
        "operation_ledger_entry_" + "payload",
        "sandbox_runtime_" + "payload",
        "endpoint_" + "url",
        "repo_" + "url",
        "user_" + "identity",
        "email_" + "address",
        "executable_" + "command",
        "tool_" + "call_instruction",
    }
    forbidden_values = (
        "http://",
        "https://",
        "ssh://",
        "git@",
        "/Users/",
        "/private/",
        "/tmp/",
        "C:\\",
        "@example" + ".com",
        "git " + "push",
        "g" + "h api",
    )

    for value in _walk(result):
        if isinstance(value, dict):
            assert forbidden_keys.isdisjoint(value)
        if isinstance(value, str):
            lowered = value.lower()
            assert all(blocked.lower() not in lowered for blocked in forbidden_values)


def test_sections_contracts_and_checks_have_required_shapes():
    result = _candidate()
    for section in result["controlled_adapter_sandbox_candidate_sections"]:
        assert {
            "section_name",
            "section_type",
            "section_status",
            "source_cross_system_coordination_refs",
            "expected",
            "observed",
            "sandbox_candidate_notes",
            "blocking_reasons",
            "safety_boundaries",
        }.issubset(section)
    for contract in result["controlled_adapter_sandbox_candidate_contracts"]:
        assert {
            "contract_name",
            "contract_type",
            "expected",
            "observed",
            "contract_status",
            "blocking_reasons",
            "safety_boundaries",
        }.issubset(contract)
    for check in result["controlled_adapter_sandbox_candidate_checks"]:
        assert {
            "check_name",
            "expected",
            "observed",
            "check_status",
            "blocking_reasons",
            "safety_boundaries",
        }.issubset(check)


def test_hash_contract_is_sha256_and_uses_sanitized_projection():
    contract = _candidate()["hash_input_contract"]

    assert contract["algorithm"] == (
        GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_ALGORITHM
    )
    assert contract["raw_cross_system_coordination_boundary_included"] is False
    assert contract["sensitive_names_included"] is False
    assert contract["sensitive_values_included"] is False


def test_module_import_and_call_surface_is_local_metadata_only():
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".", maxsplit=1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", maxsplit=1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    allowed_import_roots = {
        "__future__",
        "collections",
        "functools",
        "hashlib",
        "json",
        "math",
        "typing",
        "governance_cross_system_coordination_boundary",
        "governance_transition_policy_registry",
    }
    forbidden_calls = {
        "open",
        "write_" + "text",
        "write_" + "bytes",
        "run",
        "popen",
        "system",
        "url" + "open",
        "request",
        "send",
        "connect",
        "dispatch",
        "execute",
        "invoke",
        "submit",
        "persist",
        "push",
    }
    call_names = {
        node.func.id.lower()
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    call_names.update(
        node.func.attr.lower()
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    )

    assert imported_roots <= allowed_import_roots
    assert forbidden_calls.isdisjoint(call_names)


def test_forbidden_contamination_is_absent_from_governed_source_tree():
    fragments = (
        "governance_improvement_" + "planner",
        "governance_improvement_" + "planner_activation",
        "governance_plan_" + "rules",
        "governance_plan_" + "schema",
        "governance_plan_" + "writer",
        "smoke_governance_improvement_" + "planner",
        "smoke_governance_improvement_" + "planner_activation",
        "test_governance_improvement_" + "planner",
        "test_governance_improvement_" + "planner_activation",
        "test_governance_plan_" + "writer",
    )
    roots = (
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    )
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*")
        for path in paths:
            if not path.is_file() or path.suffix not in {".py", ".toml"}:
                continue
            text = path.read_text(encoding="utf-8")
            assert all(fragment not in text for fragment in fragments)
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()
