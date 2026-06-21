from __future__ import annotations

from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_post_sandbox_review_boundary import (
    AUDIT_EVIDENCE_STATUS,
    COMMON_DISABLED_FLAGS,
    FAILURE_HANDLING_STATUS,
    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_TYPE,
    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION,
    INCIDENT_STATUS,
    LAYER_14_CLOSURE_READINESS_STATUS,
    POST_SANDBOX_REVIEW_BOUNDARY_MODE,
    POST_SANDBOX_REVIEW_BOUNDARY_STAGE,
    POST_SANDBOX_REVIEW_MODE,
    POST_SANDBOX_REVIEW_STATUS,
    QUARANTINE_STATUS,
    REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES,
    ROLLBACK_STATUS,
    SAFETY_BOUNDARIES,
    SANDBOX_RESULT_STATUS,
    SANDBOX_REVIEW_STATUS,
    STAR_COSMOS_ENTRY_STATUS,
    _post_sandbox_review_boundary_hash,
    build_governance_post_sandbox_review_boundary,
    get_governance_post_sandbox_review_boundary_check,
    get_governance_post_sandbox_review_boundary_contract,
    get_governance_post_sandbox_review_boundary_section,
    governance_post_sandbox_review_boundary_to_json,
    list_governance_post_sandbox_review_boundary_check_names,
    list_governance_post_sandbox_review_boundary_contract_names,
    list_governance_post_sandbox_review_boundary_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_post_sandbox_review_boundary.py"
)

EXPECTED_READINESS_CONDITIONS = (
    "controlled_adapter_sandbox_candidate_pass",
    "controlled_adapter_sandbox_candidate_hash_present",
    "controlled_adapter_sandbox_candidate_hash_stable",
    "controlled_adapter_sandbox_not_started",
    "adapter_sandbox_not_entered",
    "sandbox_runtime_not_created",
    "sandbox_execution_not_enabled",
    "sandbox_result_not_available",
    "actual_post_sandbox_review_not_performed",
    "rollback_not_triggered",
    "quarantine_not_triggered",
    "incident_not_triggered",
    "audit_log_not_written",
    "audit_evidence_not_persisted",
    "failure_handling_not_executed",
    "remediation_not_executed",
    "closure_audit_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "post_sandbox_review_metadata_only",
    "layer_14_closure_candidate_only_declared",
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
)

EXPECTED_EVIDENCE_REQUIREMENTS = (
    "controlled_adapter_sandbox_candidate_pass_evidence",
    "deterministic_controlled_adapter_sandbox_candidate_hash_evidence",
    "sandbox_candidate_metadata_evidence",
    "post_sandbox_review_metadata_evidence",
    "post_sandbox_review_scope_evidence",
    "controlled_adapter_sandbox_not_started_evidence",
    "adapter_sandbox_not_entered_evidence",
    "sandbox_runtime_not_created_evidence",
    "sandbox_execution_not_enabled_evidence",
    "sandbox_result_not_available_evidence",
    "actual_post_sandbox_review_not_performed_evidence",
    "rollback_not_triggered_evidence",
    "quarantine_not_triggered_evidence",
    "incident_not_triggered_evidence",
    "audit_log_not_written_evidence",
    "audit_evidence_not_persisted_evidence",
    "failure_handling_not_executed_evidence",
    "remediation_not_executed_evidence",
    "closure_audit_not_started_evidence",
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
)

EXPECTED_BLOCKING_CONDITIONS = (
    "controlled_adapter_sandbox_candidate_blocked",
    "missing_controlled_adapter_sandbox_candidate_hash",
    "unstable_controlled_adapter_sandbox_candidate_hash",
    "post_sandbox_review_metadata_invalid",
    "candidate_only_boundary_missing",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_result_available",
    "actual_post_sandbox_review_performed",
    "sandbox_failure_observed",
    "sandbox_success_observed",
    "rollback_triggered",
    "quarantine_triggered",
    "incident_triggered",
    "audit_log_written",
    "audit_evidence_persisted",
    "failure_handling_executed",
    "remediation_executed",
    "closure_audit_started",
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
    "star_cosmos_active_entry_claimed",
)

EXPECTED_SECTION_NAMES = (
    "controlled_adapter_sandbox_candidate_input_section",
    "post_sandbox_review_metadata_section",
    "review_scope_section",
    "sandbox_result_unavailable_section",
    "actual_review_disabled_section",
    "rollback_disabled_section",
    "quarantine_disabled_section",
    "incident_disabled_section",
    "audit_log_write_disabled_section",
    "failure_handling_disabled_section",
    "sandbox_entry_disabled_section",
    "sandbox_runtime_disabled_section",
    "sandbox_execution_disabled_section",
    "external_network_write_disabled_section",
    "tool_command_routing_disabled_section",
    "adapter_manifest_execution_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_cosmos_candidate_only_section",
    "layer_14_closure_readiness_section",
)

EXPECTED_CONTRACT_NAMES = (
    "post_sandbox_review_boundary_only_contract",
    "post_sandbox_review_metadata_only_contract",
    "controlled_adapter_sandbox_candidate_pass_contract",
    "controlled_adapter_sandbox_candidate_hash_present_contract",
    "controlled_adapter_sandbox_candidate_hash_stable_contract",
    "post_sandbox_review_readiness_conditions_declared_contract",
    "post_sandbox_review_evidence_requirements_declared_contract",
    "post_sandbox_review_blocking_conditions_declared_contract",
    "post_sandbox_review_sections_complete_contract",
    "post_sandbox_review_sections_pass_contract",
    "candidate_only_boundary_contract",
    "controlled_adapter_sandbox_not_started_contract",
    "adapter_sandbox_not_entered_contract",
    "sandbox_runtime_not_created_contract",
    "sandbox_execution_not_enabled_contract",
    "sandbox_result_not_available_contract",
    "actual_post_sandbox_review_not_performed_contract",
    "rollback_not_triggered_contract",
    "quarantine_not_triggered_contract",
    "incident_not_triggered_contract",
    "audit_log_not_written_contract",
    "audit_evidence_not_persisted_contract",
    "failure_handling_not_executed_contract",
    "remediation_not_executed_contract",
    "closure_audit_not_started_contract",
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
)

EXPECTED_CHECK_NAMES = (
    "post_sandbox_review_boundary_stage_check",
    "post_sandbox_review_boundary_only_mode_check",
    "post_sandbox_review_metadata_only_check",
    "controlled_adapter_sandbox_candidate_pass_check",
    "controlled_adapter_sandbox_candidate_hash_present_check",
    "controlled_adapter_sandbox_candidate_hash_stable_check",
    "post_sandbox_review_readiness_conditions_declared_check",
    "post_sandbox_review_evidence_requirements_declared_check",
    "post_sandbox_review_blocking_conditions_declared_check",
    "post_sandbox_review_sections_complete_check",
    "post_sandbox_review_sections_pass_check",
    "post_sandbox_review_contracts_pass_check",
    "candidate_only_boundary_check",
    "controlled_adapter_sandbox_not_started_check",
    "adapter_sandbox_not_entered_check",
    "sandbox_runtime_not_created_check",
    "sandbox_execution_not_enabled_check",
    "sandbox_result_not_available_check",
    "actual_post_sandbox_review_not_performed_check",
    "rollback_not_triggered_check",
    "quarantine_not_triggered_check",
    "incident_not_triggered_check",
    "audit_log_not_written_check",
    "audit_evidence_not_persisted_check",
    "failure_handling_not_executed_check",
    "remediation_not_executed_check",
    "closure_audit_not_started_check",
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
    "deterministic_post_sandbox_review_boundary_hash_check",
    "layer_14_closure_readiness_check",
)


@lru_cache(maxsize=1)
def _boundary_payload() -> str:
    return governance_post_sandbox_review_boundary_to_json(
        build_governance_post_sandbox_review_boundary()
    )


def _boundary() -> dict[str, object]:
    return json.loads(_boundary_payload())


def _assert_all_safety_false(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_DISABLED_FLAGS:
            if key in value:
                assert value[key] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert value[key] is False
                assert boundaries[key] is False
        for nested in value.values():
            _assert_all_safety_false(nested)
    elif isinstance(value, list):
        for item in value:
            _assert_all_safety_false(item)


def _assert_string_keys(value: object) -> None:
    if isinstance(value, dict):
        assert all(isinstance(key, str) for key in value)
        for nested in value.values():
            _assert_string_keys(nested)
    elif isinstance(value, list):
        for item in value:
            _assert_string_keys(item)


def test_post_sandbox_review_boundary_shape_is_deterministic():
    first = _boundary()
    second = build_governance_post_sandbox_review_boundary()

    assert first == second
    assert first["version"] == GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION
    assert (
        first["schema_version"]
        == GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_SCHEMA_VERSION
    )
    assert (
        first["post_sandbox_review_boundary_type"]
        == GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_TYPE
    )
    assert first["post_sandbox_review_boundary_status"] == "pass"
    assert first["blocking_reasons"] == []
    assert (
        first["deterministic_post_sandbox_review_boundary_hash"]
        == second["deterministic_post_sandbox_review_boundary_hash"]
    )
    _assert_string_keys(first)


def test_post_sandbox_review_metadata_is_metadata_only_and_deterministic():
    result = _boundary()
    metadata = result["post_sandbox_review_metadata"]

    assert metadata["post_sandbox_review_metadata_type"] == (
        "future_post_sandbox_review_boundary_metadata"
    )
    assert metadata["post_sandbox_review_metadata_mode"] == "metadata_only"
    assert metadata["post_sandbox_review_status"] == "not_started"
    assert metadata["post_sandbox_review_metadata_available"] is True
    assert metadata["post_sandbox_review_declared"] is True
    assert metadata["post_sandbox_review_handoff_status"] == (
        "ready_for_star_cosmos_closure_handoff_audit_design"
    )


def test_required_name_inventories_are_stable_and_complete():
    assert REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES == (
        EXPECTED_READINESS_CONDITIONS
    )
    assert REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES == (
        EXPECTED_EVIDENCE_REQUIREMENTS
    )
    assert REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES == (
        EXPECTED_BLOCKING_CONDITIONS
    )
    assert REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES == (
        EXPECTED_SECTION_NAMES
    )
    assert REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES == (
        EXPECTED_CONTRACT_NAMES
    )
    assert REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES == (
        EXPECTED_CHECK_NAMES
    )
    assert list_governance_post_sandbox_review_boundary_section_names() == list(
        EXPECTED_SECTION_NAMES
    )
    assert list_governance_post_sandbox_review_boundary_contract_names() == list(
        EXPECTED_CONTRACT_NAMES
    )
    assert list_governance_post_sandbox_review_boundary_check_names() == list(
        EXPECTED_CHECK_NAMES
    )


@pytest.mark.parametrize(
    ("getter", "name", "status_key"),
    (
        (
            get_governance_post_sandbox_review_boundary_section,
            EXPECTED_SECTION_NAMES[0],
            "section_status",
        ),
        (
            get_governance_post_sandbox_review_boundary_contract,
            EXPECTED_CONTRACT_NAMES[0],
            "contract_status",
        ),
        (
            get_governance_post_sandbox_review_boundary_check,
            EXPECTED_CHECK_NAMES[0],
            "check_status",
        ),
    ),
)
def test_named_getters_return_detached_copies(getter, name, status_key):
    first = getter(name)
    second = getter(name)

    assert first == second
    assert first is not second
    assert first[status_key] == "pass"
    first["blocking_reasons"].append("mutation")
    assert getter(name)["blocking_reasons"] == []


@pytest.mark.parametrize(
    ("getter", "status_key"),
    (
        (get_governance_post_sandbox_review_boundary_section, "section_status"),
        (get_governance_post_sandbox_review_boundary_contract, "contract_status"),
        (get_governance_post_sandbox_review_boundary_check, "check_status"),
    ),
)
def test_unknown_getters_return_deterministic_blocked_results(getter, status_key):
    first = getter("unknown_name")
    second = getter("unknown_name")

    assert first == second
    assert first[status_key] == "blocked"
    assert first["blocking_reasons"]
    _assert_all_safety_false(first)


def test_top_level_statuses_and_upstream_candidate_are_aligned():
    result = _boundary()
    expected = {
        "post_sandbox_review_boundary_stage": POST_SANDBOX_REVIEW_BOUNDARY_STAGE,
        "post_sandbox_review_boundary_mode": POST_SANDBOX_REVIEW_BOUNDARY_MODE,
        "post_sandbox_review_mode": POST_SANDBOX_REVIEW_MODE,
        "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
        "sandbox_result_status": SANDBOX_RESULT_STATUS,
        "sandbox_review_status": SANDBOX_REVIEW_STATUS,
        "rollback_status": ROLLBACK_STATUS,
        "quarantine_status": QUARANTINE_STATUS,
        "incident_status": INCIDENT_STATUS,
        "audit_evidence_status": AUDIT_EVIDENCE_STATUS,
        "failure_handling_status": FAILURE_HANDLING_STATUS,
        "layer_14_closure_readiness_status": (
            LAYER_14_CLOSURE_READINESS_STATUS
        ),
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "controlled_adapter_sandbox_candidate_version": "6.2.0",
        "controlled_adapter_sandbox_candidate_status": "pass",
    }
    for key, value in expected.items():
        assert result[key] == value
    assert len(result["controlled_adapter_sandbox_candidate_hash"]) == 64
    assert result["handoff_status"] == (
        "ready_for_star_cosmos_closure_handoff_audit_design"
    )


def test_all_disabled_and_safety_fields_remain_false_everywhere():
    _assert_all_safety_false(_boundary())


def test_all_sections_contracts_and_checks_pass():
    result = _boundary()
    assert [item["section_name"] for item in result["post_sandbox_review_sections"]] == (
        list(EXPECTED_SECTION_NAMES)
    )
    assert all(
        item["section_status"] == "pass"
        for item in result["post_sandbox_review_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in result["post_sandbox_review_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in result["post_sandbox_review_checks"]
    )


@pytest.mark.parametrize(
    ("collection_key", "field_name"),
    (
        ("post_sandbox_review_metadata", "post_sandbox_review_status"),
        ("post_sandbox_review_sections", "observed"),
        ("post_sandbox_review_contracts", "observed"),
        ("post_sandbox_review_checks", "observed"),
    ),
)
def test_hash_changes_when_review_boundary_data_changes(
    collection_key,
    field_name,
):
    result = _boundary()
    changed = json.loads(json.dumps(result))

    if collection_key == "post_sandbox_review_metadata":
        changed[collection_key][field_name] = "changed"
    else:
        changed[collection_key][0][field_name] = {"changed": True}

    assert _post_sandbox_review_boundary_hash(changed) != (
        result["deterministic_post_sandbox_review_boundary_hash"]
    )


def test_post_sandbox_review_boundary_json_is_deterministic_and_strict():
    result = _boundary()
    first = governance_post_sandbox_review_boundary_to_json(result)
    second = governance_post_sandbox_review_boundary_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == result
    with pytest.raises(ValueError):
        governance_post_sandbox_review_boundary_to_json({"value": math.nan})
    with pytest.raises(TypeError):
        governance_post_sandbox_review_boundary_to_json({1: "invalid"})


def test_no_sensitive_values_or_runtime_payloads_leak():
    result = _boundary()
    inspected = {
        "metadata": result["post_sandbox_review_metadata"],
        "sections": result["post_sandbox_review_sections"],
        "contracts": result["post_sandbox_review_contracts"],
        "checks": result["post_sandbox_review_checks"],
        "summary": result["post_sandbox_review_summary"],
        "hash": result["deterministic_post_sandbox_review_boundary_hash"],
        "json": governance_post_sandbox_review_boundary_to_json(result),
    }
    lowered = json.dumps(inspected, sort_keys=True).lower()
    blocked = (
        '"approval_phrase"',
        '"authorization_value"',
        '"authorization_token_value"',
        '"authorization_grant_value"',
        '"raw_logs"',
        '"stdout"',
        '"stderr"',
        '"api_key"',
        '"secret"',
        '"password"',
        '"credential"',
        '"sandbox_runtime_payload"',
        '"sandbox_result_payload"',
        '"rollback_payload"',
        '"quarantine_payload"',
        '"incident_payload"',
        '"audit_log_payload"',
        '"operation_ledger_entry_payload"',
        "http://",
        "https://",
        "ssh://",
        "git@",
        "/users/",
        "/private/",
        "/tmp/",
        "@example" + ".com",
        "tool_" + "call_instruction",
        "shell_" + "command",
        "adapter_" + "dispatch_call",
        "manifest_" + "dispatch_call",
    )
    for value in blocked:
        assert value not in lowered


def test_new_module_has_no_live_execution_or_mutation_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8").lower()
    blocked = (
        "sub" + "process",
        "sock" + "et",
        "url" + "lib.request",
        "url" + "open",
        "import " + "requests",
        "from " + "requests",
        ".write_" + "text(",
        ".write_" + "bytes(",
        "os." + "system(",
        "popen" + "(",
        "git " + "push",
        "g" + "h api",
        "composio " + "execute",
        "adapter_" + "dispatch_call(",
        "manifest_" + "dispatch_call(",
        "send_" + "notification(",
        "create_" + "authorization_token(",
        "create_" + "authorization_grant(",
        "enter_" + "adapter_sandbox(",
        "start_" + "controlled_adapter_sandbox(",
        "create_" + "sandbox_runtime(",
        "perform_" + "post_sandbox_review(",
        "execute_" + "rollback(",
        "execute_" + "quarantine(",
        "execute_" + "incident(",
        "write_" + "audit_log(",
        "write_" + "operation_ledger_entry(",
        "persist_" + "operation_ledger_proposal(",
        "submit_" + "operation_ledger_proposal(",
        "route_" + "command(",
        "route_" + "tool(",
    )
    for value in blocked:
        assert value not in source


def test_no_governance_planner_contamination_and_no_uv_lock():
    blocked = (
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
    paths = [PROJECT_ROOT / "pyproject.toml"]
    for base in (
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    ):
        paths.extend(sorted(base.rglob("*.py")))

    for path in paths:
        source = path.read_text(encoding="utf-8")
        for value in blocked:
            assert value not in source
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()


def test_hash_contract_is_sha256_and_declares_review_data():
    result = _boundary()
    contract = result["hash_input_contract"]

    assert (
        contract["algorithm"]
        == GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_HASH_ALGORITHM
    )
    assert contract["json_allow_nan"] is False
    assert contract["json_ensure_ascii"] is True
    assert contract["json_sort_keys"] is True
    assert "post_sandbox_review_metadata" in contract["hash_fields"]
    assert "post_sandbox_review_sections" in contract["hash_fields"]
    assert "post_sandbox_review_contracts" in contract["hash_fields"]
    assert "post_sandbox_review_checks" in contract["hash_fields"]
