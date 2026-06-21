from __future__ import annotations

from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_operation_ledger_proposal_boundary import (
    COMMON_DISABLED_FLAGS,
    FUTURE_CROSS_SYSTEM_COORDINATION_STATUS,
    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_TYPE,
    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION,
    OPERATION_LEDGER_ENTRY_STATUS,
    OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE,
    OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE,
    OPERATION_LEDGER_PROPOSAL_MODE,
    OPERATION_LEDGER_WRITE_STATUS,
    REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES,
    REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES,
    REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES,
    REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _operation_ledger_proposal_boundary_hash,
    build_governance_operation_ledger_proposal_boundary,
    get_governance_operation_ledger_proposal_boundary_check,
    get_governance_operation_ledger_proposal_boundary_contract,
    get_governance_operation_ledger_proposal_boundary_section,
    governance_operation_ledger_proposal_boundary_to_json,
    list_governance_operation_ledger_proposal_boundary_check_names,
    list_governance_operation_ledger_proposal_boundary_contract_names,
    list_governance_operation_ledger_proposal_boundary_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_operation_ledger_proposal_boundary.py"
)

EXPECTED_READINESS_CONDITIONS = [
    "adapter_handoff_audit_pass",
    "adapter_handoff_audit_hash_present",
    "adapter_handoff_audit_hash_stable",
    "future_adapter_sandbox_not_entered",
    "handoff_metadata_only",
    "candidate_only_boundary_confirmed",
    "approval_metadata_only",
    "authorization_metadata_only",
    "no_real_execution",
    "no_adapter_invocation",
    "no_adapter_dispatch",
    "no_manifest_dispatch",
    "no_manifest_execution",
    "no_dry_run_plan_execution",
    "no_external_calls",
    "no_durable_writes",
    "no_filesystem_writes",
    "no_database_writes",
    "no_memory_graph_mutation",
    "no_operation_ledger_writes",
    "no_operation_ledger_entry_created",
    "no_operation_ledger_entry_written",
    "no_operation_ledger_proposal_persisted",
    "no_operation_ledger_proposal_submitted",
    "no_operation_ledger_proposal_dispatched",
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_adapter_sandbox_entry",
    "no_star_cosmos_active_entry",
]

EXPECTED_EVIDENCE_REQUIREMENTS = [
    "adapter_handoff_audit_pass_evidence",
    "deterministic_handoff_audit_hash_evidence",
    "handoff_metadata_evidence",
    "approval_metadata_evidence",
    "authorization_metadata_evidence",
    "candidate_only_boundary_evidence",
    "future_adapter_sandbox_not_entered_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_adapter_dispatch_evidence",
    "no_manifest_dispatch_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_durable_write_evidence",
    "no_filesystem_write_evidence",
    "no_database_write_evidence",
    "no_memory_graph_mutation_evidence",
    "no_operation_ledger_write_evidence",
    "no_operation_ledger_entry_created_evidence",
    "no_operation_ledger_entry_written_evidence",
    "no_operation_ledger_proposal_persisted_evidence",
    "no_operation_ledger_proposal_submitted_evidence",
    "no_operation_ledger_proposal_dispatched_evidence",
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_adapter_sandbox_entry_evidence",
    "no_star_cosmos_active_entry_evidence",
]

EXPECTED_BLOCKING_CONDITIONS = [
    "adapter_handoff_audit_blocked",
    "missing_adapter_handoff_audit_hash",
    "unstable_adapter_handoff_audit_hash",
    "handoff_metadata_invalid",
    "candidate_only_boundary_missing",
    "future_adapter_sandbox_entered",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "adapter_dispatch_enabled",
    "manifest_dispatch_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "operation_ledger_entry_created",
    "operation_ledger_entry_written",
    "operation_ledger_proposal_persisted",
    "operation_ledger_proposal_submitted",
    "operation_ledger_proposal_dispatched",
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
    "adapter_handoff_audit_input_section",
    "handoff_metadata_section",
    "proposal_metadata_section",
    "candidate_only_boundary_section",
    "runtime_disabled_boundary_section",
    "write_disabled_boundary_section",
    "operation_ledger_entry_not_created_section",
    "operation_ledger_proposal_not_persisted_section",
    "external_call_disabled_boundary_section",
    "adapter_sandbox_not_entered_section",
    "star_cosmos_candidate_only_section",
    "future_cross_system_coordination_readiness_section",
]

EXPECTED_CONTRACT_NAMES = [
    "operation_ledger_proposal_boundary_only_contract",
    "operation_ledger_proposal_metadata_only_contract",
    "adapter_handoff_audit_pass_contract",
    "adapter_handoff_audit_hash_present_contract",
    "adapter_handoff_audit_hash_stable_contract",
    "proposal_readiness_conditions_declared_contract",
    "proposal_evidence_requirements_declared_contract",
    "proposal_blocking_conditions_declared_contract",
    "proposal_boundary_sections_complete_contract",
    "proposal_boundary_sections_pass_contract",
    "candidate_only_boundary_contract",
    "future_cross_system_coordination_not_entered_contract",
    "no_real_execution_contract",
    "no_adapter_invocation_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_manifest_execution_contract",
    "no_dry_run_plan_execution_contract",
    "no_external_call_contract",
    "no_durable_write_contract",
    "no_filesystem_write_contract",
    "no_database_write_contract",
    "no_memory_graph_mutation_contract",
    "no_operation_ledger_write_contract",
    "no_operation_ledger_entry_created_contract",
    "no_operation_ledger_entry_written_contract",
    "no_operation_ledger_proposal_persisted_contract",
    "no_operation_ledger_proposal_submitted_contract",
    "no_operation_ledger_proposal_dispatched_contract",
    "no_real_approval_record_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_issued_contract",
    "no_authorization_token_created_contract",
    "no_authorization_grant_created_contract",
    "no_adapter_sandbox_entry_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "operation_ledger_proposal_boundary_stage_check",
    "operation_ledger_proposal_boundary_only_mode_check",
    "operation_ledger_proposal_metadata_only_check",
    "operation_ledger_entry_not_created_check",
    "operation_ledger_write_not_written_check",
    "adapter_handoff_audit_pass_check",
    "adapter_handoff_audit_hash_present_check",
    "adapter_handoff_audit_hash_stable_check",
    "proposal_readiness_conditions_declared_check",
    "proposal_evidence_requirements_declared_check",
    "proposal_blocking_conditions_declared_check",
    "proposal_boundary_sections_complete_check",
    "proposal_boundary_sections_pass_check",
    "proposal_boundary_contracts_pass_check",
    "candidate_only_boundary_check",
    "future_cross_system_coordination_not_entered_check",
    "no_real_execution_check",
    "no_adapter_invocation_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_manifest_execution_check",
    "no_dry_run_plan_execution_check",
    "no_external_call_check",
    "no_durable_write_check",
    "no_filesystem_write_check",
    "no_database_write_check",
    "no_memory_graph_mutation_check",
    "no_operation_ledger_write_check",
    "no_operation_ledger_entry_created_check",
    "no_operation_ledger_entry_written_check",
    "no_operation_ledger_proposal_persisted_check",
    "no_operation_ledger_proposal_submitted_check",
    "no_operation_ledger_proposal_dispatched_check",
    "no_real_approval_record_check",
    "no_approval_notification_check",
    "no_execution_authorization_issued_check",
    "no_authorization_token_created_check",
    "no_authorization_grant_created_check",
    "no_adapter_sandbox_entry_check",
    "star_cosmos_candidate_only_check",
    "deterministic_operation_ledger_proposal_boundary_hash_check",
    "proposal_boundary_readiness_check",
]


@lru_cache(maxsize=1)
def _boundary_json() -> str:
    return governance_operation_ledger_proposal_boundary_to_json(
        build_governance_operation_ledger_proposal_boundary()
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


def test_operation_ledger_proposal_boundary_constants():
    assert GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION == "6.4.0"
    assert GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SCHEMA_VERSION == "6.4.0"
    assert GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_TYPE == (
        "governance_operation_ledger_proposal_boundary"
    )
    assert GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM == "sha256"
    assert OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE == (
        "v5.9_operation_ledger_proposal_boundary"
    )
    assert OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE == (
        "operation_ledger_proposal_boundary_only"
    )
    assert OPERATION_LEDGER_PROPOSAL_MODE == "metadata_only"
    assert OPERATION_LEDGER_ENTRY_STATUS == "not_created"
    assert OPERATION_LEDGER_WRITE_STATUS == "not_written"
    assert FUTURE_CROSS_SYSTEM_COORDINATION_STATUS == "not_entered"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_operation_ledger_proposal_boundary_shape_is_deterministic():
    first = build_governance_operation_ledger_proposal_boundary()
    second = build_governance_operation_ledger_proposal_boundary()

    assert first == second
    assert first["version"] == "6.4.0"
    assert first["schema_version"] == "6.4.0"
    assert first["operation_ledger_proposal_boundary_type"] == (
        "governance_operation_ledger_proposal_boundary"
    )
    assert first["operation_ledger_proposal_boundary_status"] == "pass"
    assert first["operation_ledger_proposal_boundary_stage"] == (
        "v5.9_operation_ledger_proposal_boundary"
    )
    assert first["operation_ledger_proposal_boundary_mode"] == (
        "operation_ledger_proposal_boundary_only"
    )
    assert first["operation_ledger_proposal_mode"] == "metadata_only"
    assert first["operation_ledger_entry_status"] == "not_created"
    assert first["operation_ledger_write_status"] == "not_written"
    assert first["future_cross_system_coordination_status"] == "not_entered"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["adapter_handoff_audit_version"] == "6.4.0"
    assert first["adapter_handoff_audit_status"] == "pass"
    assert len(first["adapter_handoff_audit_hash"]) == 64
    assert first["blocking_reasons"] == []
    assert first["handoff_status"] == (
        "ready_for_cross_system_coordination_boundary_design"
    )


def test_proposal_metadata_is_deterministic_and_metadata_only():
    metadata = _boundary()["operation_ledger_proposal_metadata"]

    assert metadata["proposal_metadata_type"] == (
        "future_operation_ledger_proposal_boundary_metadata"
    )
    assert metadata["proposal_metadata_mode"] == "metadata_only"
    assert metadata["proposal_status"] == "metadata_only_proposal"
    assert metadata["proposal_required"] is True
    assert metadata["proposal_metadata_available"] is True
    assert metadata["proposal_persisted"] is False
    assert metadata["proposal_submitted"] is False
    assert metadata["proposal_dispatched"] is False
    assert metadata["operation_ledger_entry_status"] == "not_created"
    assert metadata["operation_ledger_write_status"] == "not_written"
    assert metadata["proposal_boundary_handoff_status"] == (
        "ready_for_cross_system_coordination_boundary_design"
    )


def test_proposal_requirement_names_are_stable_and_complete():
    metadata = _boundary()["operation_ledger_proposal_metadata"]

    assert list(REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES) == (
        EXPECTED_READINESS_CONDITIONS
    )
    assert list(REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES) == (
        EXPECTED_EVIDENCE_REQUIREMENTS
    )
    assert list(REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES) == (
        EXPECTED_BLOCKING_CONDITIONS
    )
    assert metadata["proposal_boundary_readiness_conditions"] == (
        EXPECTED_READINESS_CONDITIONS
    )
    assert metadata["required_proposal_evidence"] == EXPECTED_EVIDENCE_REQUIREMENTS
    assert metadata["proposal_boundary_blocking_conditions"] == (
        EXPECTED_BLOCKING_CONDITIONS
    )


def test_boundary_names_are_stable_and_complete():
    boundary = _boundary()

    assert list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES) == (
        EXPECTED_SECTION_NAMES
    )
    assert list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES) == (
        EXPECTED_CONTRACT_NAMES
    )
    assert list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES) == (
        EXPECTED_CHECK_NAMES
    )
    assert (
        list_governance_operation_ledger_proposal_boundary_section_names()
        == EXPECTED_SECTION_NAMES
    )
    assert (
        list_governance_operation_ledger_proposal_boundary_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert (
        list_governance_operation_ledger_proposal_boundary_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        item["section_name"]
        for item in boundary["operation_ledger_proposal_boundary_sections"]
    ] == EXPECTED_SECTION_NAMES
    assert [
        item["contract_name"]
        for item in boundary["operation_ledger_proposal_boundary_contracts"]
    ] == EXPECTED_CONTRACT_NAMES
    assert [
        item["check_name"]
        for item in boundary["operation_ledger_proposal_boundary_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_getters_return_detached_copies():
    section = get_governance_operation_ledger_proposal_boundary_section(
        EXPECTED_SECTION_NAMES[0]
    )
    contract = get_governance_operation_ledger_proposal_boundary_contract(
        EXPECTED_CONTRACT_NAMES[0]
    )
    check = get_governance_operation_ledger_proposal_boundary_check(
        EXPECTED_CHECK_NAMES[0]
    )

    section["observed"]["mutated"] = True
    contract["observed"]["mutated"] = True
    check["observed"]["mutated"] = True

    assert "mutated" not in get_governance_operation_ledger_proposal_boundary_section(
        EXPECTED_SECTION_NAMES[0]
    )["observed"]
    assert "mutated" not in get_governance_operation_ledger_proposal_boundary_contract(
        EXPECTED_CONTRACT_NAMES[0]
    )["observed"]
    assert "mutated" not in get_governance_operation_ledger_proposal_boundary_check(
        EXPECTED_CHECK_NAMES[0]
    )["observed"]


def test_unknown_getters_return_blocked_style_results():
    section = get_governance_operation_ledger_proposal_boundary_section("missing")
    contract = get_governance_operation_ledger_proposal_boundary_contract("missing")
    check = get_governance_operation_ledger_proposal_boundary_check("missing")

    assert section["section_status"] == "blocked"
    assert section["section_type"] == (
        "unknown_operation_ledger_proposal_boundary_section"
    )
    assert contract["contract_status"] == "blocked"
    assert contract["contract_type"] == (
        "unknown_operation_ledger_proposal_boundary_contract"
    )
    assert check["check_status"] == "blocked"
    assert section["blocking_reasons"]
    assert contract["blocking_reasons"]
    assert check["blocking_reasons"]
    _assert_safety(section)
    _assert_safety(contract)
    _assert_safety(check)


def test_all_sections_contracts_checks_and_safety_fields_pass():
    boundary = _boundary()

    assert all(
        item["section_status"] == "pass"
        for item in boundary["operation_ledger_proposal_boundary_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in boundary["operation_ledger_proposal_boundary_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in boundary["operation_ledger_proposal_boundary_checks"]
    )
    for key in COMMON_DISABLED_FLAGS:
        assert boundary[key] is False
    _assert_safety(boundary)


def test_deterministic_boundary_hash_is_stable_and_sensitive():
    boundary = _boundary()
    repeated = _boundary()
    mutations = []
    for collection_name, nested_name in (
        ("operation_ledger_proposal_metadata", "proposal_status"),
        ("operation_ledger_proposal_boundary_sections", "section_status"),
        ("operation_ledger_proposal_boundary_contracts", "contract_status"),
        ("operation_ledger_proposal_boundary_checks", "check_status"),
    ):
        mutated = json.loads(json.dumps(boundary))
        if isinstance(mutated[collection_name], list):
            mutated[collection_name][0][nested_name] = "changed"
        else:
            mutated[collection_name][nested_name] = "changed"
        mutations.append(mutated)

    assert boundary["deterministic_operation_ledger_proposal_boundary_hash"] == (
        repeated["deterministic_operation_ledger_proposal_boundary_hash"]
    )
    assert _operation_ledger_proposal_boundary_hash(boundary) == (
        boundary["deterministic_operation_ledger_proposal_boundary_hash"]
    )
    for mutated in mutations:
        assert _operation_ledger_proposal_boundary_hash(mutated) != (
            boundary["deterministic_operation_ledger_proposal_boundary_hash"]
        )


def test_boundary_json_is_deterministic_and_strict():
    boundary = _boundary()
    payload = governance_operation_ledger_proposal_boundary_to_json(boundary)

    assert payload == governance_operation_ledger_proposal_boundary_to_json(boundary)
    assert payload.endswith("\n")
    assert json.loads(payload) == boundary
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_operation_ledger_proposal_boundary_to_json({1: "bad"})
    with pytest.raises(ValueError, match="floats must be finite"):
        governance_operation_ledger_proposal_boundary_to_json({"bad": math.inf})


def test_no_sensitive_keys_or_values_leak():
    boundary = _boundary()
    payload = json.dumps(
        {
            "metadata": boundary["operation_ledger_proposal_metadata"],
            "sections": boundary["operation_ledger_proposal_boundary_sections"],
            "contracts": boundary["operation_ledger_proposal_boundary_contracts"],
            "checks": boundary["operation_ledger_proposal_boundary_checks"],
            "summary": boundary["operation_ledger_proposal_boundary_summary"],
            "hashes": {
                "proposal": boundary[
                    "deterministic_operation_ledger_proposal_boundary_hash"
                ],
                "handoff": boundary["adapter_handoff_audit_hash"],
            },
        },
        sort_keys=True,
    ).lower()
    blocked = (
        '"approval_' + 'phrase"',
        '"authorization_' + 'value"',
        '"authorization_token_' + 'value"',
        '"authorization_grant_' + 'value"',
        '"raw_' + 'logs"',
        '"std' + 'out"',
        '"std' + 'err"',
        '"api_' + 'key"',
        '"sec' + 'ret"',
        '"pass' + 'word"',
        '"cred' + 'ential"',
        '"operation_ledger_entry_' + 'payload"',
        "http" + "://",
        "https" + "://",
        "ssh" + "://",
        "git" + "@",
        "/Users" + "/",
        "/private" + "/",
        "/tmp" + "/",
        "@example" + ".com",
        "tool_" + "call",
    )

    assert all(item.lower() not in payload for item in blocked)


def test_new_module_has_no_live_mutation_or_execution_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8").lower()
    blocked = (
        "sub" + "process",
        "sock" + "et",
        "req" + "uests",
        "url" + "lib",
        "open" + "(",
        "write_" + "text",
        "write_" + "bytes",
        "os." + "system",
        "po" + "pen",
        "git " + "push",
        "g" + "h api",
        "open" + "claw",
        "github " + "api",
        "composio " + "execute",
        "memory_graph_" + "write",
        "adapter_" + "dispatch(",
        "manifest_" + "dispatch(",
        "send_" + "email",
        "web" + "hook",
        "persist_" + "approval",
        "create_authorization_" + "token",
        "create_authorization_" + "grant",
        "issue_execution_" + "authorization",
        "enter_adapter_" + "sandbox",
        "start_controlled_adapter_" + "sandbox",
        "write_operation_" + "ledger",
        "persist_operation_ledger_" + "proposal",
        "submit_operation_ledger_" + "proposal",
    )

    assert all(item not in source for item in blocked)


def test_no_unrelated_governance_contamination_or_lock_file():
    contamination_names = (
        "governance_improvement_" + "planner",
        "governance_improvement_" + "planner_" + "activation",
        "governance_plan_" + "rules",
        "governance_plan_" + "schema",
        "governance_plan_" + "writer",
        "smoke_governance_improvement_" + "planner",
        "smoke_governance_improvement_" + "planner_" + "activation",
        "test_governance_improvement_" + "planner",
        "test_governance_improvement_" + "planner_" + "activation",
        "test_governance_plan_" + "writer",
    )
    paths = [PROJECT_ROOT / "pyproject.toml"]
    for relative in ("scripts", "src/hermes_memory_fabric", "tests"):
        paths.extend(
            path
            for path in (PROJECT_ROOT / relative).rglob("*")
            if path.is_file() and path.suffix in {".py", ".toml"}
        )

    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert all(name not in source for name in contamination_names)
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()
