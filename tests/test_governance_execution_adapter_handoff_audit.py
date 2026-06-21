from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_handoff_audit import (
    ADAPTER_HANDOFF_AUDIT_MODE,
    EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE,
    FUTURE_ADAPTER_SANDBOX_STATUS,
    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_handoff_audit_hash,
    build_governance_execution_adapter_handoff_audit,
    get_governance_execution_adapter_handoff_audit_check,
    get_governance_execution_adapter_handoff_audit_contract,
    get_governance_execution_adapter_handoff_audit_section,
    governance_execution_adapter_handoff_audit_to_json,
    list_governance_execution_adapter_handoff_audit_check_names,
    list_governance_execution_adapter_handoff_audit_contract_names,
    list_governance_execution_adapter_handoff_audit_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_handoff_audit.py"
)

EXPECTED_READINESS_CONDITION_NAMES = [
    "execution_adapter_boundary_candidate_sealed",
    "adapter_contract_registry_candidate_sealed",
    "adapter_capability_manifest_candidate_sealed",
    "invocation_request_envelope_candidate_sealed",
    "human_approval_boundary_candidate_sealed",
    "adapter_dry_run_simulator_candidate_sealed",
    "side_effect_policy_registry_candidate_sealed",
    "execution_plan_review_matrix_candidate_sealed",
    "manifest_authorization_gate_pass",
    "manifest_authorization_gate_hash_present",
    "manifest_authorization_gate_hash_stable",
    "authorization_metadata_only",
    "approval_metadata_only",
    "candidate_only_boundary_confirmed",
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
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_adapter_sandbox_entry",
    "no_star_cosmos_active_entry",
]

EXPECTED_EVIDENCE_REQUIREMENT_NAMES = [
    "v5_0_boundary_candidate_evidence",
    "v5_1_contract_registry_candidate_evidence",
    "v5_2_capability_manifest_candidate_evidence",
    "v5_3_invocation_request_envelope_candidate_evidence",
    "v5_4_human_approval_boundary_candidate_evidence",
    "v5_5_dry_run_simulator_candidate_evidence",
    "v5_6_side_effect_policy_registry_candidate_evidence",
    "v5_7_execution_plan_review_matrix_candidate_evidence",
    "manifest_authorization_gate_pass_evidence",
    "deterministic_authorization_gate_hash_evidence",
    "authorization_metadata_evidence",
    "approval_metadata_evidence",
    "candidate_only_boundary_evidence",
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
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_adapter_sandbox_entry_evidence",
    "no_star_cosmos_active_entry_evidence",
]

EXPECTED_BLOCKING_CONDITION_NAMES = [
    "manifest_authorization_gate_blocked",
    "missing_manifest_authorization_gate_hash",
    "unstable_manifest_authorization_gate_hash",
    "authorization_metadata_invalid",
    "approval_metadata_invalid",
    "candidate_only_boundary_missing",
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
    "v5_0_execution_adapter_boundary_audit",
    "v5_1_adapter_contract_registry_audit",
    "v5_2_adapter_capability_manifest_audit",
    "v5_3_invocation_request_envelope_audit",
    "v5_4_human_approval_boundary_audit",
    "v5_5_adapter_dry_run_simulator_audit",
    "v5_6_side_effect_policy_registry_audit",
    "v5_7_execution_plan_review_matrix_audit",
    "manifest_authorization_gate_audit",
    "authorization_metadata_audit",
    "approval_metadata_audit",
    "candidate_only_boundary_audit",
    "runtime_disabled_boundary_audit",
    "write_disabled_boundary_audit",
    "external_call_disabled_boundary_audit",
    "adapter_sandbox_not_entered_audit",
    "star_cosmos_candidate_only_audit",
    "future_handoff_readiness_audit",
]

EXPECTED_CONTRACT_NAMES = [
    "adapter_handoff_audit_only_contract",
    "future_adapter_sandbox_not_entered_contract",
    "manifest_authorization_gate_pass_contract",
    "manifest_authorization_gate_hash_present_contract",
    "manifest_authorization_gate_hash_stable_contract",
    "handoff_metadata_only_contract",
    "handoff_readiness_conditions_declared_contract",
    "handoff_evidence_requirements_declared_contract",
    "handoff_blocking_conditions_declared_contract",
    "handoff_audit_sections_complete_contract",
    "handoff_audit_sections_pass_contract",
    "authorization_metadata_only_contract",
    "approval_metadata_only_contract",
    "candidate_only_boundary_contract",
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
    "no_real_approval_record_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_issued_contract",
    "no_authorization_token_created_contract",
    "no_authorization_grant_created_contract",
    "no_adapter_sandbox_entry_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "adapter_handoff_audit_stage_check",
    "adapter_handoff_audit_only_mode_check",
    "future_adapter_sandbox_not_entered_check",
    "manifest_authorization_gate_pass_check",
    "manifest_authorization_gate_hash_present_check",
    "manifest_authorization_gate_hash_stable_check",
    "handoff_metadata_only_check",
    "handoff_readiness_conditions_declared_check",
    "handoff_evidence_requirements_declared_check",
    "handoff_blocking_conditions_declared_check",
    "handoff_audit_sections_complete_check",
    "handoff_audit_sections_pass_check",
    "handoff_audit_contracts_pass_check",
    "authorization_metadata_only_check",
    "approval_metadata_only_check",
    "candidate_only_boundary_check",
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
    "no_real_approval_record_check",
    "no_approval_notification_check",
    "no_execution_authorization_issued_check",
    "no_authorization_token_created_check",
    "no_authorization_grant_created_check",
    "no_adapter_sandbox_entry_check",
    "star_cosmos_candidate_only_check",
    "deterministic_handoff_audit_hash_check",
    "handoff_audit_readiness_check",
]

COMMON_FALSE_FIELDS = (
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "adapter_dispatched",
    "manifest_dispatched",
    "manifest_executed",
    "dry_run_plan_executed",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "approval_request_created",
    "approval_notification_sent",
    "real_approval_record_written",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "adapter_sandbox_entered",
    "controlled_adapter_sandbox_started",
)

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_artifact"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
)

FORBIDDEN_HANDOFF_METADATA_TERMS = (
    *SENSITIVE_BLOCKED_TERMS,
    "http://",
    "https://",
    "ssh://",
    "git@",
    "github" + ".com",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call",
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
    "bash -",
    "sh -",
    "python -",
    "$(",
    "send_" + "email",
    "web" + "hook",
    "notification_" + "sender",
    "authorization_" + "token_value",
    "authorization_" + "grant_value",
)

FORBIDDEN_ACTIVE_SOURCE_TERMS = (
    "sub" + "process",
    "socket",
    "requ" + "ests",
    "urllib",
    "url" + "open",
    "open(",
    ".open(",
    "write_text",
    "git " + "push",
    "g" + "h api",
    "Open" + "Claw",
    "Git" + "Hub API",
    "Composio",
    "memory_graph_mutation_" + "api",
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
    "shell commands",
    "operation-ledger write APIs",
    "create_" + "memory_write_proposal",
    "send_" + "email",
    "web" + "hook",
    "notification_" + "sender",
    "notification_" + "routing",
    "create_" + "authorization_" + "token",
    "create_" + "authorization_" + "grant",
    "issue_" + "real_execution_authorization",
)

CONTAMINATION_TERMS = (
    "governance_" + "improvement_planner",
    "governance_" + "improvement_planner_activation",
    "governance_" + "plan_rules",
    "governance_" + "plan_schema",
    "governance_" + "plan_writer",
    "smoke_governance_" + "improvement_planner",
    "smoke_governance_" + "improvement_planner_activation",
    "test_governance_" + "improvement_planner",
    "test_governance_" + "improvement_planner_activation",
    "test_governance_" + "plan_writer",
    "uv" + ".lock",
)


@lru_cache(maxsize=1)
def _audit_payload() -> str:
    return governance_execution_adapter_handoff_audit_to_json(
        build_governance_execution_adapter_handoff_audit()
    )


def _audit() -> dict[str, object]:
    return json.loads(_audit_payload())


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_FALSE_FIELDS:
            if key in value:
                assert value[key] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert value[key] is False
                assert boundaries[key] is False
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_string_keys_and_finite_values(value: object) -> None:
    if isinstance(value, dict):
        assert all(isinstance(key, str) for key in value)
        for nested_value in value.values():
            _assert_string_keys_and_finite_values(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_string_keys_and_finite_values(item)
    elif isinstance(value, float):
        assert math.isfinite(value)


def test_public_constants():
    assert GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION == "6.3.0"
    assert GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_SCHEMA_VERSION == "6.3.0"
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_TYPE
        == "governance_execution_adapter_handoff_audit"
    )
    assert GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM == "sha256"
    assert EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE == "v5.8_adapter_handoff_audit"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"
    assert ADAPTER_HANDOFF_AUDIT_MODE == "adapter_handoff_audit_only"
    assert FUTURE_ADAPTER_SANDBOX_STATUS == "not_entered"


def test_adapter_handoff_audit_shape_is_deterministic():
    first = _audit()
    second = _audit()

    assert first == second
    assert first["version"] == "6.3.0"
    assert first["schema_version"] == "6.3.0"
    assert (
        first["adapter_handoff_audit_type"]
        == "governance_execution_adapter_handoff_audit"
    )
    assert first["adapter_handoff_audit_status"] == "pass"
    assert first["adapter_handoff_audit_stage"] == "v5.8_adapter_handoff_audit"
    assert first["adapter_handoff_audit_mode"] == "adapter_handoff_audit_only"
    assert first["future_adapter_sandbox_status"] == "not_entered"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["manifest_authorization_gate_version"] == "6.3.0"
    assert first["manifest_authorization_gate_status"] == "pass"
    assert isinstance(first["manifest_authorization_gate_hash"], str)
    assert len(first["manifest_authorization_gate_hash"]) == 64
    assert (
        first["handoff_status"]
        == "ready_for_operation_ledger_proposal_boundary_design"
    )
    assert first["blocking_reasons"] == []
    assert len(first["deterministic_adapter_handoff_audit_hash"]) == 64
    for key in COMMON_FALSE_FIELDS:
        assert first[key] is False
    _assert_string_keys_and_finite_values(first)


def test_handoff_metadata_is_deterministic_and_metadata_only():
    metadata = _audit()["adapter_handoff_audit_metadata"]
    repeated_metadata = _audit()["adapter_handoff_audit_metadata"]

    assert metadata == repeated_metadata
    assert metadata["handoff_audit_metadata_type"] == (
        "future_controlled_adapter_sandbox_entry_readiness_metadata"
    )
    assert metadata["handoff_audit_metadata_mode"] == "metadata_only"
    assert metadata["handoff_audit_status"] == "not_handed_off"
    assert metadata["future_adapter_sandbox_status"] == "not_entered"
    assert metadata["handoff_required"] is True
    assert metadata["handoff_approved"] is False
    assert metadata["candidate_only"] is True
    assert metadata["authorization_gate_pass_required"] is True
    assert metadata["authorization_gate_hash_required"] is True
    assert metadata["handoff_audit_next_stage"] == (
        "operation_ledger_proposal_boundary"
    )
    assert metadata["handoff_audit_handoff_status"] == (
        "ready_for_operation_ledger_proposal_boundary_design"
    )
    for key in COMMON_FALSE_FIELDS:
        if key in metadata:
            assert metadata[key] is False
    _assert_safety(metadata)


def test_handoff_readiness_condition_names_are_stable_and_complete():
    assert (
        _audit()["adapter_handoff_audit_metadata"][
            "handoff_audit_readiness_conditions"
        ]
        == EXPECTED_READINESS_CONDITION_NAMES
    )


def test_handoff_evidence_requirement_names_are_stable_and_complete():
    assert (
        _audit()["adapter_handoff_audit_metadata"]["required_handoff_evidence"]
        == EXPECTED_EVIDENCE_REQUIREMENT_NAMES
    )


def test_handoff_blocking_condition_names_are_stable_and_complete():
    assert (
        _audit()["adapter_handoff_audit_metadata"][
            "handoff_audit_blocking_conditions"
        ]
        == EXPECTED_BLOCKING_CONDITION_NAMES
    )


def test_handoff_audit_section_names_are_stable_and_complete():
    audit = _audit()

    assert list_governance_execution_adapter_handoff_audit_section_names() == (
        EXPECTED_SECTION_NAMES
    )
    assert [
        section["section_name"] for section in audit["adapter_handoff_audit_sections"]
    ] == EXPECTED_SECTION_NAMES


def test_handoff_audit_contract_names_are_stable_and_complete():
    audit = _audit()

    assert list_governance_execution_adapter_handoff_audit_contract_names() == (
        EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in audit["adapter_handoff_audit_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_handoff_audit_check_names_are_stable_and_complete():
    audit = _audit()

    assert list_governance_execution_adapter_handoff_audit_check_names() == (
        EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in audit["adapter_handoff_audit_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_section_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_handoff_audit_section(
        "manifest_authorization_gate_audit"
    )
    original = deepcopy(first)
    first["observed"]["manifest_authorization_gate_status"] = "blocked"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_handoff_audit_section(
        "manifest_authorization_gate_audit"
    )

    assert second == original
    assert second["observed"]["manifest_authorization_gate_status"] == "pass"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_handoff_audit_contract(
        "adapter_handoff_audit_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["handoff_approved"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_handoff_audit_contract(
        "adapter_handoff_audit_only_contract"
    )

    assert second == original
    assert second["observed"]["handoff_approved"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_handoff_audit_check(
        "adapter_handoff_audit_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["adapter_handoff_audit_mode"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_handoff_audit_check(
        "adapter_handoff_audit_only_mode_check"
    )

    assert second == original
    assert second["observed"]["adapter_handoff_audit_mode"] == (  # type: ignore[index]
        "adapter_handoff_audit_only"
    )
    assert second["blocking_reasons"] == []


def test_unknown_section_contract_and_check_return_blocked_style_results():
    section = get_governance_execution_adapter_handoff_audit_section(
        "missing_section"
    )
    contract = get_governance_execution_adapter_handoff_audit_contract(
        "missing_contract"
    )
    check = get_governance_execution_adapter_handoff_audit_check("missing_check")

    assert section["section_status"] == "blocked"
    assert section["section_type"] == "unknown_adapter_handoff_audit_section"
    assert section["observed"] == {
        "known_section_name": False,
        "requested_section_name": "missing_section",
    }
    assert contract["contract_status"] == "blocked"
    assert contract["contract_type"] == "unknown_adapter_handoff_audit_contract"
    assert contract["observed"] == {
        "known_contract_name": False,
        "requested_contract_name": "missing_contract",
    }
    assert check["check_status"] == "blocked"
    assert check["observed"] == {
        "known_check_name": False,
        "requested_check_name": "missing_check",
    }


def test_all_sections_contracts_and_checks_pass_without_blocking_reasons():
    audit = _audit()

    assert audit["adapter_handoff_audit_status"] == "pass"
    assert audit["blocking_reasons"] == []
    for section in audit["adapter_handoff_audit_sections"]:
        assert section["section_status"] == "pass"
        assert section["blocking_reasons"] == []
    for contract in audit["adapter_handoff_audit_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in audit["adapter_handoff_audit_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_all_execution_write_external_approval_authorization_and_sandbox_flags_are_false():
    audit = _audit()

    for key in COMMON_FALSE_FIELDS:
        assert audit[key] is False
    _assert_safety(audit)


def test_deterministic_adapter_handoff_audit_hash_is_stable_and_sensitive_to_metadata():
    audit = _audit()
    repeated = _audit()
    mutated = deepcopy(audit)
    mutated["adapter_handoff_audit_metadata"][  # type: ignore[index]
        "handoff_audit_metadata_mode"
    ] = "mutated"

    assert audit["deterministic_adapter_handoff_audit_hash"] == repeated[
        "deterministic_adapter_handoff_audit_hash"
    ]
    assert _execution_adapter_handoff_audit_hash(audit) == audit[
        "deterministic_adapter_handoff_audit_hash"
    ]
    assert _execution_adapter_handoff_audit_hash(mutated) != audit[
        "deterministic_adapter_handoff_audit_hash"
    ]


def test_adapter_handoff_audit_hash_is_sensitive_to_section_contract_and_check_data():
    audit = _audit()
    section_mutated = deepcopy(audit)
    contract_mutated = deepcopy(audit)
    check_mutated = deepcopy(audit)
    section_mutated["adapter_handoff_audit_sections"][0]["observed"][  # type: ignore[index]
        "candidate_only"
    ] = False
    contract_mutated["adapter_handoff_audit_contracts"][0]["observed"][  # type: ignore[index]
        "handoff_approved"
    ] = True
    check_mutated["adapter_handoff_audit_checks"][0]["observed"][  # type: ignore[index]
        "adapter_handoff_audit_stage"
    ] = "mutated"

    assert _execution_adapter_handoff_audit_hash(section_mutated) != audit[
        "deterministic_adapter_handoff_audit_hash"
    ]
    assert _execution_adapter_handoff_audit_hash(contract_mutated) != audit[
        "deterministic_adapter_handoff_audit_hash"
    ]
    assert _execution_adapter_handoff_audit_hash(check_mutated) != audit[
        "deterministic_adapter_handoff_audit_hash"
    ]


def test_adapter_handoff_audit_json_is_deterministic():
    audit = _audit()
    payload = governance_execution_adapter_handoff_audit_to_json(audit)
    repeated_payload = governance_execution_adapter_handoff_audit_to_json(_audit())

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == audit
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_adapter_handoff_audit_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_handoff_audit_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_handoff_audit_to_json({"bad": math.inf})


def test_no_sensitive_keys_or_values_leak():
    audit = _audit()
    protected = {
        "metadata": audit["adapter_handoff_audit_metadata"],
        "sections": audit["adapter_handoff_audit_sections"],
        "contracts": audit["adapter_handoff_audit_contracts"],
        "checks": audit["adapter_handoff_audit_checks"],
        "summary": audit["adapter_handoff_audit_summary"],
        "hashes": {
            "handoff_audit": audit["deterministic_adapter_handoff_audit_hash"],
            "manifest_authorization_gate": audit["manifest_authorization_gate_hash"],
        },
        "json": governance_execution_adapter_handoff_audit_to_json(audit),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_handoff_metadata_and_sections_do_not_expose_live_or_sensitive_surfaces():
    audit = _audit()
    serialized = json.dumps(
        {
            "metadata": audit["adapter_handoff_audit_metadata"],
            "sections": audit["adapter_handoff_audit_sections"],
        },
        sort_keys=True,
    )

    for blocked in FORBIDDEN_HANDOFF_METADATA_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_audit())


def test_adapter_handoff_audit_module_has_no_active_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source


def test_no_unrelated_planner_or_lock_references_exist():
    search_roots = [
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    ]
    files: list[Path] = []
    for root in search_roots:
        if root.is_file():
            files.append(root)
        else:
            files.extend(
                path
                for path in sorted(root.rglob("*"))
                if path.is_file() and path.suffix in {".py", ".toml"}
            )

    for path in files:
        text = path.read_text(encoding="utf-8")
        for forbidden in CONTAMINATION_TERMS:
            assert forbidden not in text, path
