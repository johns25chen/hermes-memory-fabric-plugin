from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_manifest_dry_run_design import (
    EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION,
    MANIFEST_DRY_RUN_DESIGN_MODE,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_manifest_dry_run_design_hash,
    build_governance_execution_adapter_manifest_dry_run_design,
    get_governance_execution_adapter_manifest_design_check,
    get_governance_execution_adapter_manifest_design_contract,
    get_governance_execution_adapter_manifest_section,
    governance_execution_adapter_manifest_dry_run_design_to_json,
    list_governance_execution_adapter_manifest_design_check_names,
    list_governance_execution_adapter_manifest_design_contract_names,
    list_governance_execution_adapter_manifest_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_manifest_dry_run_design.py"
)

EXPECTED_SECTION_NAMES = [
    "manifest_identity_section",
    "manifest_adapter_reference_section",
    "manifest_capabilities_section",
    "manifest_inputs_section",
    "manifest_outputs_section",
    "manifest_permissions_section",
    "manifest_side_effects_section",
    "manifest_external_dependencies_section",
    "manifest_durable_writes_section",
    "manifest_memory_graph_mutations_section",
    "manifest_operation_ledger_writes_section",
    "manifest_approval_requirements_section",
    "manifest_dry_run_inspection_section",
    "manifest_redaction_policy_section",
    "manifest_safety_boundaries_section",
    "manifest_star_cosmos_candidate_status_section",
]

EXPECTED_CONTRACT_NAMES = [
    "manifest_design_only_contract",
    "declaration_schema_registry_pass_contract",
    "manifest_identity_design_contract",
    "manifest_adapter_reference_design_contract",
    "manifest_capability_design_contract",
    "manifest_input_design_contract",
    "manifest_output_design_contract",
    "manifest_permission_design_contract",
    "manifest_side_effect_design_contract",
    "manifest_external_dependency_design_contract",
    "manifest_durable_write_design_contract",
    "manifest_memory_graph_mutation_design_contract",
    "manifest_operation_ledger_write_design_contract",
    "manifest_approval_requirement_design_contract",
    "manifest_dry_run_inspection_design_contract",
    "manifest_redaction_design_contract",
    "star_cosmos_candidate_only_manifest_contract",
]

EXPECTED_CHECK_NAMES = [
    "declaration_schema_registry_pass_check",
    "manifest_dry_run_design_stage_check",
    "design_only_mode_check",
    "manifest_sections_complete_check",
    "manifest_contracts_complete_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "manifest_not_executed_check",
    "dry_run_plan_not_executed_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
]

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase-4-10",
    "fixture-stdout-tail-4-10",
    "fixture-stdout-4-10",
    "fixture-raw-logs-4-10",
    "fixture-token-4-10",
    "fixture-api-key-4-10",
    "fixture-secret-4-10",
    "fixture-password-4-10",
    "fixture-credential-4-10",
    "fixture-approval-phrase-5-0",
    "fixture-stdout-tail-5-0",
    "fixture-stdout-5-0",
    "fixture-raw-logs-5-0",
    "fixture-token-5-0",
    "fixture-api-key-5-0",
    "fixture-secret-5-0",
    "fixture-password-5-0",
    "fixture-credential-5-0",
    "fixture-approval-phrase-5-1",
    "fixture-stdout-tail-5-1",
    "fixture-stdout-5-1",
    "fixture-raw-logs-5-1",
    "fixture-token-5-1",
    "fixture-api-key-5-1",
    "fixture-secret-5-1",
    "fixture-password-5-1",
    "fixture-credential-5-1",
    "fixture-approval-phrase-5-2",
    "fixture-stdout-tail-5-2",
    "fixture-stdout-5-2",
    "fixture-raw-logs-5-2",
    "fixture-token-5-2",
    "fixture-api-key-5-2",
    "fixture-secret-5-2",
    "fixture-password-5-2",
    "fixture-credential-5-2",
)

FORBIDDEN_ACTIVE_SOURCE_TERMS = (
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "open(",
    ".open(",
    "write_text",
    "git " + "push",
    "g" + "h api",
    "OpenClaw",
    "GitHub API",
    "Composio",
    "create_" + "memory_write_proposal",
    "memory_graph_write",
    "memory_graph_mutate",
    "memory_graph_mutation_api",
    "adapter_dispatch",
    "manifest_dispatch",
)


def _design() -> dict[str, object]:
    return build_governance_execution_adapter_manifest_dry_run_design()


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
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
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
        == "6.7.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_SCHEMA_VERSION
        == "6.7.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_TYPE
        == "governance_execution_adapter_manifest_dry_run_design"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE
        == "v5.2_execution_adapter_manifest_dry_run_design_candidate"
    )
    assert MANIFEST_DRY_RUN_DESIGN_MODE == "design_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_manifest_dry_run_design_shape_is_deterministic():
    first = _design()
    second = _design()

    assert first == second
    assert first["version"] == "6.7.0"
    assert first["schema_version"] == "6.7.0"
    assert (
        first["manifest_dry_run_design_type"]
        == "governance_execution_adapter_manifest_dry_run_design"
    )
    assert first["manifest_dry_run_design_status"] == "pass"
    assert (
        first["manifest_dry_run_design_stage"]
        == "v5.2_execution_adapter_manifest_dry_run_design_candidate"
    )
    assert first["manifest_dry_run_design_mode"] == "design_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["star_cosmos_memory_active"] is False
    assert first["execution_adapter_implemented"] is False
    assert first["execution_adapter_invoked"] is False
    assert first["manifest_executed"] is False
    assert first["dry_run_plan_executed"] is False
    assert first["real_execution_enabled"] is False
    assert first["external_calls_enabled"] is False
    assert first["durable_writes_enabled"] is False
    assert first["memory_graph_mutation_enabled"] is False
    assert first["operation_ledger_writes_enabled"] is False
    assert first["autonomous_execution_enabled"] is False
    assert (
        first["handoff_status"]
        == "ready_for_future_manifest_fixture_pack_design"
    )
    assert first["blocking_reasons"] == []
    assert first["declaration_schema_registry_version"] == "6.7.0"
    assert first["declaration_schema_registry_status"] == "pass"
    assert isinstance(first["declaration_schema_registry_hash"], str)
    assert len(first["declaration_schema_registry_hash"]) == 64
    assert len(first["deterministic_manifest_dry_run_design_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_section_names_are_stable_and_complete():
    design = _design()

    assert (
        list_governance_execution_adapter_manifest_section_names()
        == EXPECTED_SECTION_NAMES
    )
    assert [
        section["section_name"] for section in design["manifest_sections"]
    ] == EXPECTED_SECTION_NAMES


def test_contract_names_are_stable_and_complete():
    design = _design()

    assert (
        list_governance_execution_adapter_manifest_design_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in design["manifest_design_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_check_names_are_stable_and_complete():
    design = _design()

    assert (
        list_governance_execution_adapter_manifest_design_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in design["manifest_design_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_section_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_section(
        "manifest_identity_section"
    )
    original = deepcopy(first)
    first["schema_field_refs"].append("mutated")  # type: ignore[union-attr]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_section(
        "manifest_identity_section"
    )

    assert second == original
    assert "mutated" not in second["schema_field_refs"]  # type: ignore[operator]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_design_contract(
        "manifest_design_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["manifest_executed"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_design_contract(
        "manifest_design_only_contract"
    )

    assert second == original
    assert second["observed"]["manifest_executed"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_design_check(
        "design_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_design_check(
        "design_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "design_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_section_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_section(
        "missing_section"
    )
    second = get_governance_execution_adapter_manifest_section(
        "missing_section"
    )

    assert result == second
    assert result["section_name"] == "missing_section"
    assert result["section_type"] == "unknown_section"
    assert result["design_status"] == "blocked"
    assert result["schema_field_refs"] == []
    assert result["blocking_reasons"] == [
        "execution adapter manifest section name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_design_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_manifest_design_contract(
        "missing_contract"
    )

    assert result == second
    assert result["contract_name"] == "missing_contract"
    assert result["contract_type"] == "unknown_contract"
    assert result["contract_status"] == "blocked"
    assert result["expected"] == {"known_contract_name": True}
    assert result["observed"] == {
        "known_contract_name": False,
        "requested_contract_name": "missing_contract",
    }
    assert result["blocking_reasons"] == [
        "execution adapter manifest design contract name is not recognized"
    ]


def test_unknown_check_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_design_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_manifest_design_check(
        "missing_check"
    )

    assert result == second
    assert result["check_name"] == "missing_check"
    assert result["check_status"] == "blocked"
    assert result["expected"] == {"known_check_name": True}
    assert result["observed"] == {
        "known_check_name": False,
        "requested_check_name": "missing_check",
    }
    assert result["blocking_reasons"] == [
        "execution adapter manifest design check name is not recognized"
    ]


def test_all_sections_contracts_and_checks_pass_without_blocking_reasons():
    design = _design()

    assert design["manifest_dry_run_design_status"] == "pass"
    assert design["blocking_reasons"] == []
    for section in design["manifest_sections"]:
        assert section["design_status"] == "pass"
        assert section["blocking_reasons"] == []
    for contract in design["manifest_design_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in design["manifest_design_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_deterministic_manifest_hash_is_stable_and_sensitive_to_section_data():
    design = _design()
    repeated = _design()
    mutated = deepcopy(design)
    mutated["manifest_sections"][0]["section_type"] = "mutated"  # type: ignore[index]

    assert (
        design["deterministic_manifest_dry_run_design_hash"]
        == repeated["deterministic_manifest_dry_run_design_hash"]
    )
    assert _execution_adapter_manifest_dry_run_design_hash(design) == design[
        "deterministic_manifest_dry_run_design_hash"
    ]
    assert _execution_adapter_manifest_dry_run_design_hash(mutated) != design[
        "deterministic_manifest_dry_run_design_hash"
    ]


def test_deterministic_manifest_hash_is_sensitive_to_contract_and_check_data():
    design = _design()
    contract_mutated = deepcopy(design)
    check_mutated = deepcopy(design)
    contract_mutated["manifest_design_contracts"][0]["observed"][  # type: ignore[index]
        "manifest_executed"
    ] = True
    check_mutated["manifest_design_checks"][0]["observed"][  # type: ignore[index]
        "declaration_schema_registry_status"
    ] = "blocked"

    assert _execution_adapter_manifest_dry_run_design_hash(
        contract_mutated
    ) != design["deterministic_manifest_dry_run_design_hash"]
    assert _execution_adapter_manifest_dry_run_design_hash(check_mutated) != design[
        "deterministic_manifest_dry_run_design_hash"
    ]


def test_manifest_json_is_deterministic():
    design = _design()
    payload = governance_execution_adapter_manifest_dry_run_design_to_json(
        design
    )
    repeated_payload = governance_execution_adapter_manifest_dry_run_design_to_json(
        _design()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == design
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_manifest_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_manifest_dry_run_design_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_manifest_dry_run_design_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    design = _design()
    protected = {
        "sections": design["manifest_sections"],
        "contracts": design["manifest_design_contracts"],
        "checks": design["manifest_design_checks"],
        "summary": design["manifest_design_summary"],
        "hashes": {
            "manifest": design["deterministic_manifest_dry_run_design_hash"],
            "registry": design["declaration_schema_registry_hash"],
        },
        "json": governance_execution_adapter_manifest_dry_run_design_to_json(
            design
        ),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_design())


def test_manifest_design_module_has_no_active_execution_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source
