from __future__ import annotations

import ast
from copy import deepcopy
from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_cross_system_coordination_boundary import (
    CODEX_COORDINATION_STATUS,
    COMMAND_ROUTING_STATUS,
    COMMON_DISABLED_FLAGS,
    CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE,
    CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE,
    CROSS_SYSTEM_COORDINATION_MODE,
    CROSS_SYSTEM_COORDINATION_STATUS,
    FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS,
    GITHUB_COORDINATION_STATUS,
    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_TYPE,
    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION,
    HERMES_COORDINATION_STATUS,
    OPENCLAW_COORDINATION_STATUS,
    REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES,
    REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_COORDINATION_READINESS_CONDITION_NAMES,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    SYSTEM_HANDOFF_STATUS,
    TOOL_ROUTING_STATUS,
    _cross_system_coordination_boundary_hash,
    build_governance_cross_system_coordination_boundary,
    get_governance_cross_system_coordination_boundary_check,
    get_governance_cross_system_coordination_boundary_contract,
    get_governance_cross_system_coordination_boundary_section,
    governance_cross_system_coordination_boundary_to_json,
    list_governance_cross_system_coordination_boundary_check_names,
    list_governance_cross_system_coordination_boundary_contract_names,
    list_governance_cross_system_coordination_boundary_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_cross_system_coordination_boundary.py"
)

EXPECTED_READINESS_CONDITIONS = [
    "operation_ledger_proposal_boundary_pass",
    "operation_ledger_proposal_boundary_hash_present",
    "operation_ledger_proposal_boundary_hash_stable",
    "operation_ledger_entry_not_created",
    "operation_ledger_write_not_written",
    "operation_ledger_proposal_not_persisted",
    "operation_ledger_proposal_not_submitted",
    "operation_ledger_proposal_not_dispatched",
    "cross_system_coordination_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "metadata_only_boundary_confirmed",
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
    "no_adapter_sandbox_entry",
    "no_star_cosmos_active_entry",
]

EXPECTED_EVIDENCE_REQUIREMENTS = [
    "operation_ledger_proposal_boundary_pass_evidence",
    "deterministic_operation_ledger_proposal_boundary_hash_evidence",
    "operation_ledger_proposal_metadata_evidence",
    "coordination_metadata_evidence",
    "hermes_not_connected_evidence",
    "codex_not_connected_evidence",
    "openclaw_not_connected_evidence",
    "github_not_connected_evidence",
    "tool_routing_not_configured_evidence",
    "command_routing_not_configured_evidence",
    "system_handoff_not_completed_evidence",
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
    "no_adapter_sandbox_entry_evidence",
    "no_star_cosmos_active_entry_evidence",
]

EXPECTED_BLOCKING_CONDITIONS = [
    "operation_ledger_proposal_boundary_blocked",
    "missing_operation_ledger_proposal_boundary_hash",
    "unstable_operation_ledger_proposal_boundary_hash",
    "coordination_metadata_invalid",
    "candidate_only_boundary_missing",
    "cross_system_coordination_started",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "tool_routing_configured",
    "command_routing_configured",
    "system_handoff_completed",
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
    "adapter_sandbox_entered",
    "controlled_adapter_sandbox_started",
    "star_cosmos_active_entry_claimed",
]

EXPECTED_SECTION_NAMES = [
    "operation_ledger_proposal_boundary_input_section",
    "coordination_metadata_section",
    "hermes_boundary_section",
    "codex_boundary_section",
    "openclaw_boundary_section",
    "github_boundary_section",
    "tool_routing_disabled_section",
    "command_routing_disabled_section",
    "runtime_disabled_boundary_section",
    "write_disabled_boundary_section",
    "external_call_disabled_boundary_section",
    "network_call_disabled_boundary_section",
    "operation_ledger_write_disabled_section",
    "adapter_sandbox_not_entered_section",
    "star_cosmos_candidate_only_section",
    "future_controlled_adapter_sandbox_readiness_section",
]

EXPECTED_CONTRACT_NAMES = [
    "cross_system_coordination_boundary_only_contract",
    "cross_system_coordination_metadata_only_contract",
    "operation_ledger_proposal_boundary_pass_contract",
    "operation_ledger_proposal_boundary_hash_present_contract",
    "operation_ledger_proposal_boundary_hash_stable_contract",
    "coordination_readiness_conditions_declared_contract",
    "coordination_evidence_requirements_declared_contract",
    "coordination_blocking_conditions_declared_contract",
    "coordination_boundary_sections_complete_contract",
    "coordination_boundary_sections_pass_contract",
    "candidate_only_boundary_contract",
    "hermes_not_connected_contract",
    "codex_not_connected_contract",
    "openclaw_not_connected_contract",
    "github_not_connected_contract",
    "tool_routing_not_configured_contract",
    "command_routing_not_configured_contract",
    "system_handoff_not_completed_contract",
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
    "no_adapter_sandbox_entry_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "cross_system_coordination_boundary_stage_check",
    "cross_system_coordination_boundary_only_mode_check",
    "cross_system_coordination_metadata_only_check",
    "cross_system_coordination_not_started_check",
    "hermes_not_connected_check",
    "codex_not_connected_check",
    "openclaw_not_connected_check",
    "github_not_connected_check",
    "tool_routing_not_configured_check",
    "command_routing_not_configured_check",
    "system_handoff_not_completed_check",
    "operation_ledger_proposal_boundary_pass_check",
    "operation_ledger_proposal_boundary_hash_present_check",
    "operation_ledger_proposal_boundary_hash_stable_check",
    "coordination_readiness_conditions_declared_check",
    "coordination_evidence_requirements_declared_check",
    "coordination_blocking_conditions_declared_check",
    "coordination_boundary_sections_complete_check",
    "coordination_boundary_sections_pass_check",
    "coordination_boundary_contracts_pass_check",
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
    "no_adapter_sandbox_entry_check",
    "star_cosmos_candidate_only_check",
    "deterministic_cross_system_coordination_boundary_hash_check",
    "coordination_boundary_readiness_check",
]


@lru_cache(maxsize=1)
def _boundary_json() -> str:
    return governance_cross_system_coordination_boundary_to_json(
        build_governance_cross_system_coordination_boundary()
    )


def _boundary() -> dict[str, object]:
    return json.loads(_boundary_json())


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


def test_cross_system_coordination_boundary_shape_is_deterministic():
    first = _boundary()
    second = build_governance_cross_system_coordination_boundary()

    assert first == second
    assert first["version"] == GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION
    assert (
        first["schema_version"]
        == GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_SCHEMA_VERSION
    )
    assert (
        first["cross_system_coordination_boundary_type"]
        == GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_TYPE
    )
    assert first["cross_system_coordination_boundary_status"] == "pass"
    assert (
        first["cross_system_coordination_boundary_stage"]
        == CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE
    )
    assert (
        first["cross_system_coordination_boundary_mode"]
        == CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
    )
    assert (
        first["deterministic_cross_system_coordination_boundary_hash"]
        == second["deterministic_cross_system_coordination_boundary_hash"]
    )
    assert first["blocking_reasons"] == []


def test_coordination_metadata_is_deterministic_and_metadata_only():
    result = _boundary()
    metadata = result["cross_system_coordination_metadata"]

    assert metadata["coordination_metadata_type"] == (
        "future_cross_system_coordination_boundary_metadata"
    )
    assert metadata["coordination_metadata_mode"] == CROSS_SYSTEM_COORDINATION_MODE
    assert metadata["coordination_status"] == "metadata_only_boundary"
    assert metadata["coordination_metadata_available"] is True
    assert metadata["coordination_established"] is False
    assert metadata["coordination_persisted"] is False
    assert metadata["coordination_submitted"] is False
    assert metadata["coordination_dispatched"] is False
    assert metadata["coordination_boundary_handoff_status"] == (
        "ready_for_controlled_adapter_sandbox_candidate_design"
    )


@pytest.mark.parametrize(
    ("actual", "expected"),
    (
        (
            REQUIRED_COORDINATION_READINESS_CONDITION_NAMES,
            EXPECTED_READINESS_CONDITIONS,
        ),
        (
            REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES,
            EXPECTED_EVIDENCE_REQUIREMENTS,
        ),
        (
            REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES,
            EXPECTED_BLOCKING_CONDITIONS,
        ),
        (
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES,
            EXPECTED_SECTION_NAMES,
        ),
        (
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES,
            EXPECTED_CONTRACT_NAMES,
        ),
        (
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES,
            EXPECTED_CHECK_NAMES,
        ),
    ),
)
def test_required_name_sets_are_stable_and_complete(actual, expected):
    assert list(actual) == expected


def test_name_helpers_return_stable_order():
    assert (
        list_governance_cross_system_coordination_boundary_section_names()
        == EXPECTED_SECTION_NAMES
    )
    assert (
        list_governance_cross_system_coordination_boundary_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert (
        list_governance_cross_system_coordination_boundary_check_names()
        == EXPECTED_CHECK_NAMES
    )


@pytest.mark.parametrize(
    ("getter", "name", "status_key"),
    (
        (
            get_governance_cross_system_coordination_boundary_section,
            EXPECTED_SECTION_NAMES[0],
            "section_status",
        ),
        (
            get_governance_cross_system_coordination_boundary_contract,
            EXPECTED_CONTRACT_NAMES[0],
            "contract_status",
        ),
        (
            get_governance_cross_system_coordination_boundary_check,
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
            get_governance_cross_system_coordination_boundary_section,
            "section_status",
        ),
        (
            get_governance_cross_system_coordination_boundary_contract,
            "contract_status",
        ),
        (
            get_governance_cross_system_coordination_boundary_check,
            "check_status",
        ),
    ),
)
def test_unknown_getters_return_blocked_style_results(getter, status_key):
    result = getter("unknown_name")

    assert result[status_key] == "blocked"
    assert result["blocking_reasons"]
    _assert_safety(result)


def test_top_level_status_and_coordination_boundaries():
    result = _boundary()

    expected = {
        "cross_system_coordination_boundary_status": "pass",
        "cross_system_coordination_boundary_stage": (
            CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE
        ),
        "cross_system_coordination_boundary_mode": (
            CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
        ),
        "cross_system_coordination_mode": CROSS_SYSTEM_COORDINATION_MODE,
        "cross_system_coordination_status": CROSS_SYSTEM_COORDINATION_STATUS,
        "hermes_coordination_status": HERMES_COORDINATION_STATUS,
        "codex_coordination_status": CODEX_COORDINATION_STATUS,
        "openclaw_coordination_status": OPENCLAW_COORDINATION_STATUS,
        "github_coordination_status": GITHUB_COORDINATION_STATUS,
        "tool_routing_status": TOOL_ROUTING_STATUS,
        "command_routing_status": COMMAND_ROUTING_STATUS,
        "system_handoff_status": SYSTEM_HANDOFF_STATUS,
        "future_controlled_adapter_sandbox_status": (
            FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
        ),
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "operation_ledger_proposal_boundary_version": "6.9.0",
        "operation_ledger_proposal_boundary_status": "pass",
    }
    for key, value in expected.items():
        assert result[key] == value
    assert len(result["operation_ledger_proposal_boundary_hash"]) == 64
    assert result["handoff_status"] == (
        "ready_for_controlled_adapter_sandbox_candidate_design"
    )


def test_all_disabled_and_safety_fields_remain_false():
    _assert_safety(_boundary())


def test_all_sections_contracts_and_checks_pass():
    result = _boundary()

    assert all(
        item["section_status"] == "pass"
        for item in result["cross_system_coordination_boundary_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in result["cross_system_coordination_boundary_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in result["cross_system_coordination_boundary_checks"]
    )


@pytest.mark.parametrize(
    ("collection_name", "index", "field_name"),
    (
        ("cross_system_coordination_metadata", None, "coordination_status"),
        (
            "cross_system_coordination_boundary_sections",
            0,
            "section_type",
        ),
        (
            "cross_system_coordination_boundary_contracts",
            0,
            "contract_type",
        ),
        (
            "cross_system_coordination_boundary_checks",
            0,
            "check_name",
        ),
    ),
)
def test_hash_changes_when_governed_boundary_data_changes(
    collection_name,
    index,
    field_name,
):
    result = _boundary()
    changed = deepcopy(result)
    target = changed[collection_name]
    if index is not None:
        target = target[index]
    target[field_name] = f"{target[field_name]}_changed"

    assert _cross_system_coordination_boundary_hash(changed) != (
        result["deterministic_cross_system_coordination_boundary_hash"]
    )


def test_cross_system_coordination_boundary_json_is_deterministic():
    result = _boundary()
    first = governance_cross_system_coordination_boundary_to_json(result)
    second = governance_cross_system_coordination_boundary_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == result


def test_non_finite_floats_are_rejected():
    with pytest.raises(ValueError):
        governance_cross_system_coordination_boundary_to_json(
            {"invalid": math.nan}
        )


def test_no_sensitive_keys_or_values_leak():
    result = _boundary()
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


def test_sections_have_required_shape_and_detached_upstream_refs():
    for section in _boundary()["cross_system_coordination_boundary_sections"]:
        assert set(
            (
                "section_name",
                "section_type",
                "section_status",
                "source_operation_ledger_proposal_refs",
                "expected",
                "observed",
                "coordination_notes",
                "blocking_reasons",
                "safety_boundaries",
            )
        ).issubset(section)
        assert section["source_operation_ledger_proposal_refs"] == [
            "operation_ledger_proposal_boundary_status",
            "deterministic_operation_ledger_proposal_boundary_hash",
            "operation_ledger_proposal_metadata",
        ]


def test_contracts_and_checks_have_required_shapes():
    result = _boundary()
    for contract in result["cross_system_coordination_boundary_contracts"]:
        assert set(
            (
                "contract_name",
                "contract_type",
                "expected",
                "observed",
                "contract_status",
                "blocking_reasons",
                "safety_boundaries",
            )
        ).issubset(contract)
    for check in result["cross_system_coordination_boundary_checks"]:
        assert set(
            (
                "check_name",
                "expected",
                "observed",
                "check_status",
                "blocking_reasons",
                "safety_boundaries",
            )
        ).issubset(check)


def test_hash_contract_is_sha256_and_uses_sanitized_projection():
    result = _boundary()
    contract = result["hash_input_contract"]

    assert contract["algorithm"] == (
        GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM
    )
    assert contract["raw_operation_ledger_proposal_boundary_included"] is False
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
        "governance_operation_ledger_proposal_boundary",
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
