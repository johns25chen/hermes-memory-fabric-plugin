"""Deterministic manifest dry-run design metadata for future adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_declaration_schema_registry import (
    build_governance_execution_adapter_declaration_schema_registry,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION = "6.7.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_SCHEMA_VERSION = "6.7.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_TYPE = (
    "governance_execution_adapter_manifest_dry_run_design"
)
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE = (
    "v5.2_execution_adapter_manifest_dry_run_design_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
MANIFEST_DRY_RUN_DESIGN_MODE = "design_only"

READY_HANDOFF_STATUS = "ready_for_future_manifest_fixture_pack_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_MANIFEST_SECTION_NAMES = (
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
)

REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES = (
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
)

REQUIRED_MANIFEST_DESIGN_CHECK_NAMES = (
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
)

_MANIFEST_DRY_RUN_DESIGN_HASH_FIELDS = (
    "version",
    "schema_version",
    "manifest_dry_run_design_type",
    "manifest_dry_run_design_status",
    "manifest_dry_run_design_stage",
    "manifest_dry_run_design_mode",
    "star_cosmos_entry_status",
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "manifest_executed",
    "dry_run_plan_executed",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "declaration_schema_registry_version",
    "declaration_schema_registry_status",
    "declaration_schema_registry_hash",
    "manifest_sections",
    "manifest_design_contracts",
    "manifest_design_checks",
    "manifest_design_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MANIFEST_DRY_RUN_DESIGN_HASH_FIELDS),
    "input_shape": "sanitized future execution adapter manifest dry-run design projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_SENSITIVE_BLOCKED_TERMS = (
    '"approval_' + 'phrase"',
    '"std' + 'out_tail"',
    '"std' + 'out"',
    '"raw_' + 'logs"',
    '"to' + 'ken"',
    '"api_' + 'key"',
    '"sec' + 'ret"',
    '"pass' + 'word"',
    '"creden' + 'tial"',
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


def build_governance_execution_adapter_manifest_dry_run_design() -> dict[str, Any]:
    """Build deterministic design-only manifest metadata."""

    registry = _detached_json_value(
        build_governance_execution_adapter_declaration_schema_registry()
    )
    sections = _build_manifest_sections()
    contracts = _build_manifest_design_contracts(registry, sections)
    checks = _build_manifest_design_checks(registry, sections, contracts)

    registry_passes = (
        registry.get("declaration_schema_registry_status") == "pass"
        and registry.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
    )
    sections_pass = all(
        section["design_status"] == "pass" for section in sections
    )
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    manifest_status = (
        "pass"
        if registry_passes and sections_pass and contracts_pass and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["declaration schema registry must pass at version 6.7.0"]
                if not registry_passes
                else []
            ),
            *(
                reason
                for section in sections
                for reason in section["blocking_reasons"]
            ),
            *(
                reason
                for contract in contracts
                for reason in contract["blocking_reasons"]
            ),
            *(
                reason
                for check in checks
                for reason in check["blocking_reasons"]
            ),
        ]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    manifest: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_SCHEMA_VERSION
        ),
        "manifest_dry_run_design_type": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_TYPE
        ),
        "manifest_dry_run_design_status": manifest_status,
        "manifest_dry_run_design_stage": (
            EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE
        ),
        "manifest_dry_run_design_mode": MANIFEST_DRY_RUN_DESIGN_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "star_cosmos_memory_active": False,
        "execution_adapter_implemented": False,
        "execution_adapter_invoked": False,
        "manifest_executed": False,
        "dry_run_plan_executed": False,
        "real_execution_enabled": False,
        "external_calls_enabled": False,
        "durable_writes_enabled": False,
        "memory_graph_mutation_enabled": False,
        "operation_ledger_writes_enabled": False,
        "autonomous_execution_enabled": False,
        "declaration_schema_registry_version": _string_or_none(
            registry.get("version")
        ),
        "declaration_schema_registry_status": _string_or_none(
            registry.get("declaration_schema_registry_status")
        ),
        "declaration_schema_registry_hash": _string_or_none(
            registry.get("deterministic_declaration_schema_registry_hash")
        ),
        "manifest_sections": sections,
        "manifest_design_contracts": contracts,
        "manifest_design_checks": checks,
        "manifest_design_summary": _manifest_design_summary(
            sections, contracts, checks
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if manifest_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    manifest["deterministic_manifest_dry_run_design_hash"] = (
        _execution_adapter_manifest_dry_run_design_hash(manifest)
    )
    return _detached_json_value(manifest)


def get_governance_execution_adapter_manifest_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest design section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    for section in _build_manifest_sections():
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_execution_adapter_manifest_design_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest design contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    registry = _detached_json_value(
        build_governance_execution_adapter_declaration_schema_registry()
    )
    sections = _build_manifest_sections()
    for contract in _build_manifest_design_contracts(registry, sections):
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_manifest_design_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest design check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    registry = _detached_json_value(
        build_governance_execution_adapter_declaration_schema_registry()
    )
    sections = _build_manifest_sections()
    contracts = _build_manifest_design_contracts(registry, sections)
    for check in _build_manifest_design_checks(registry, sections, contracts):
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_manifest_section_names() -> list[str]:
    """Return stable manifest design section names."""

    return list(REQUIRED_MANIFEST_SECTION_NAMES)


def list_governance_execution_adapter_manifest_design_contract_names() -> list[str]:
    """Return stable manifest design contract names."""

    return list(REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES)


def list_governance_execution_adapter_manifest_design_check_names() -> list[str]:
    """Return stable manifest design check names."""

    return list(REQUIRED_MANIFEST_DESIGN_CHECK_NAMES)


def governance_execution_adapter_manifest_dry_run_design_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize manifest dry-run design metadata deterministically."""

    return (
        json.dumps(
            _detached_json_value(dict(result)),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _build_manifest_sections() -> list[dict[str, Any]]:
    return [
        _section(
            "manifest_identity_section",
            section_type="manifest_identity_metadata",
            schema_field_refs=[
                "adapter_id",
                "adapter_name",
                "adapter_kind",
                "adapter_version",
                "adapter_owner",
                "adapter_description",
            ],
        ),
        _section(
            "manifest_adapter_reference_section",
            section_type="adapter_reference_metadata",
            schema_field_refs=[
                "adapter_id",
                "adapter_kind",
                "adapter_version",
            ],
        ),
        _section(
            "manifest_capabilities_section",
            section_type="capability_metadata",
            schema_field_refs=["declared_capabilities"],
        ),
        _section(
            "manifest_inputs_section",
            section_type="input_metadata",
            schema_field_refs=["declared_inputs"],
        ),
        _section(
            "manifest_outputs_section",
            section_type="output_metadata",
            schema_field_refs=["declared_outputs"],
        ),
        _section(
            "manifest_permissions_section",
            section_type="permission_metadata",
            schema_field_refs=["declared_permissions"],
        ),
        _section(
            "manifest_side_effects_section",
            section_type="side_effect_metadata",
            schema_field_refs=["declared_side_effects"],
        ),
        _section(
            "manifest_external_dependencies_section",
            section_type="external_dependency_metadata",
            schema_field_refs=["declared_external_dependencies"],
        ),
        _section(
            "manifest_durable_writes_section",
            section_type="durable_write_metadata",
            schema_field_refs=["declared_durable_writes"],
        ),
        _section(
            "manifest_memory_graph_mutations_section",
            section_type="memory_graph_mutation_metadata",
            schema_field_refs=["declared_memory_graph_mutations"],
        ),
        _section(
            "manifest_operation_ledger_writes_section",
            section_type="operation_ledger_write_metadata",
            schema_field_refs=["declared_operation_ledger_writes"],
        ),
        _section(
            "manifest_approval_requirements_section",
            section_type="approval_requirement_metadata",
            schema_field_refs=["declared_approval_requirements"],
        ),
        _section(
            "manifest_dry_run_inspection_section",
            section_type="dry_run_inspection_metadata",
            schema_field_refs=["declared_dry_run_inspection"],
        ),
        _section(
            "manifest_redaction_policy_section",
            section_type="redaction_policy_metadata",
            schema_field_refs=["declared_redaction_policy"],
        ),
        _section(
            "manifest_safety_boundaries_section",
            section_type="safety_boundary_metadata",
            schema_field_refs=["declared_safety_boundaries"],
        ),
        _section(
            "manifest_star_cosmos_candidate_status_section",
            section_type="candidate_status_metadata",
            schema_field_refs=["declared_star_cosmos_entry_status"],
        ),
    ]


def _build_manifest_design_contracts(
    registry: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    section_names = [
        _string_or_none(section.get("section_name")) or ""
        for section in sections
    ]
    return [
        _contract(
            "manifest_design_only_contract",
            contract_type="manifest_design_contract",
            expected={
                "manifest_dry_run_design_mode": MANIFEST_DRY_RUN_DESIGN_MODE,
                "manifest_executed": False,
                "execution_adapter_invoked": False,
            },
            observed={
                "manifest_dry_run_design_mode": MANIFEST_DRY_RUN_DESIGN_MODE,
                "manifest_executed": False,
                "execution_adapter_invoked": False,
            },
        ),
        _contract(
            "declaration_schema_registry_pass_contract",
            contract_type="upstream_registry_contract",
            expected={
                "declaration_schema_registry_status": "pass",
                "declaration_schema_registry_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
                ),
            },
            observed={
                "declaration_schema_registry_status": _string_or_none(
                    registry.get("declaration_schema_registry_status")
                ),
                "declaration_schema_registry_version": _string_or_none(
                    registry.get("version")
                ),
                "declaration_schema_registry_hash_present": _is_sha256(
                    _string_or_none(
                        registry.get(
                            "deterministic_declaration_schema_registry_hash"
                        )
                    )
                ),
            },
            blocking_reasons=_deduplicate(
                [
                    *(
                        ["declaration schema registry status must pass"]
                        if registry.get("declaration_schema_registry_status")
                        != "pass"
                        else []
                    ),
                    *(
                        ["declaration schema registry version must equal 6.7.0"]
                        if registry.get("version")
                        != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
                        else []
                    ),
                ]
            ),
        ),
        _section_presence_contract(
            "manifest_identity_design_contract",
            "manifest_identity_section",
        ),
        _section_presence_contract(
            "manifest_adapter_reference_design_contract",
            "manifest_adapter_reference_section",
        ),
        _section_presence_contract(
            "manifest_capability_design_contract",
            "manifest_capabilities_section",
        ),
        _section_presence_contract(
            "manifest_input_design_contract",
            "manifest_inputs_section",
        ),
        _section_presence_contract(
            "manifest_output_design_contract",
            "manifest_outputs_section",
        ),
        _section_presence_contract(
            "manifest_permission_design_contract",
            "manifest_permissions_section",
        ),
        _section_presence_contract(
            "manifest_side_effect_design_contract",
            "manifest_side_effects_section",
        ),
        _section_presence_contract(
            "manifest_external_dependency_design_contract",
            "manifest_external_dependencies_section",
        ),
        _section_presence_contract(
            "manifest_durable_write_design_contract",
            "manifest_durable_writes_section",
        ),
        _section_presence_contract(
            "manifest_memory_graph_mutation_design_contract",
            "manifest_memory_graph_mutations_section",
        ),
        _section_presence_contract(
            "manifest_operation_ledger_write_design_contract",
            "manifest_operation_ledger_writes_section",
        ),
        _section_presence_contract(
            "manifest_approval_requirement_design_contract",
            "manifest_approval_requirements_section",
        ),
        _section_presence_contract(
            "manifest_dry_run_inspection_design_contract",
            "manifest_dry_run_inspection_section",
        ),
        _section_presence_contract(
            "manifest_redaction_design_contract",
            "manifest_redaction_policy_section",
        ),
        _contract(
            "star_cosmos_candidate_only_manifest_contract",
            contract_type="candidate_manifest_contract",
            expected={
                "manifest_star_cosmos_candidate_status_section_present": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
            observed={
                "manifest_star_cosmos_candidate_status_section_present": (
                    "manifest_star_cosmos_candidate_status_section"
                    in section_names
                ),
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
        ),
    ]


def _build_manifest_design_checks(
    registry: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    registry_hash = _string_or_none(
        registry.get("deterministic_declaration_schema_registry_hash")
    )
    return [
        _check(
            "declaration_schema_registry_pass_check",
            expected={
                "declaration_schema_registry_status": "pass",
                "declaration_schema_registry_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
                ),
                "declaration_schema_registry_hash_present": True,
            },
            observed={
                "declaration_schema_registry_status": _string_or_none(
                    registry.get("declaration_schema_registry_status")
                ),
                "declaration_schema_registry_version": _string_or_none(
                    registry.get("version")
                ),
                "declaration_schema_registry_hash_present": (
                    _is_sha256(registry_hash)
                ),
            },
            blocking_reasons=_deduplicate(
                [
                    *(
                        ["declaration schema registry status must pass"]
                        if registry.get("declaration_schema_registry_status")
                        != "pass"
                        else []
                    ),
                    *(
                        ["declaration schema registry version must equal 6.7.0"]
                        if registry.get("version")
                        != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION
                        else []
                    ),
                    *(
                        ["declaration schema registry hash must be sha256"]
                        if not _is_sha256(registry_hash)
                        else []
                    ),
                ]
            ),
        ),
        _simple_flag_check(
            "manifest_dry_run_design_stage_check",
            expected=EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE,
            observed=EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE,
        ),
        _simple_flag_check(
            "design_only_mode_check",
            expected=MANIFEST_DRY_RUN_DESIGN_MODE,
            observed=MANIFEST_DRY_RUN_DESIGN_MODE,
        ),
        _sections_complete_check(sections),
        _contracts_complete_check(contracts),
        _simple_flag_check("adapter_not_implemented_check", False, False),
        _simple_flag_check("adapter_not_invoked_check", False, False),
        _simple_flag_check("manifest_not_executed_check", False, False),
        _simple_flag_check("dry_run_plan_not_executed_check", False, False),
        _simple_flag_check("real_execution_disabled_check", False, False),
        _simple_flag_check("external_calls_disabled_check", False, False),
        _simple_flag_check("durable_writes_disabled_check", False, False),
        _simple_flag_check("memory_graph_mutation_disabled_check", False, False),
        _simple_flag_check(
            "operation_ledger_writes_disabled_check", False, False
        ),
        _simple_flag_check("autonomous_execution_disabled_check", False, False),
        _check(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            blocking_reasons=[],
        ),
        _deterministic_hash_check(registry, sections, contracts),
        _redaction_boundary_check(sections, contracts),
    ]


def _section(
    section_name: str,
    *,
    section_type: str,
    schema_field_refs: Sequence[str],
    required: bool = True,
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    section: dict[str, Any] = {
        "section_name": section_name,
        "section_type": section_type,
        "required": required,
        "schema_field_refs": list(schema_field_refs),
        "design_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(section)


def _contract(
    contract_name: str,
    *,
    contract_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    contract: dict[str, Any] = {
        "contract_name": contract_name,
        "contract_type": contract_type,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "contract_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(contract)


def _check(
    check_name: str,
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    check: dict[str, Any] = {
        "check_name": check_name,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "check_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(check)


def _section_presence_contract(
    contract_name: str,
    section_name: str,
) -> dict[str, Any]:
    section_names = list_governance_execution_adapter_manifest_section_names()
    return _contract(
        contract_name,
        contract_type="manifest_section_design_contract",
        expected={
            "manifest_section_present": True,
            "section_name": section_name,
            "metadata_only": True,
            "manifest_executed": False,
        },
        observed={
            "manifest_section_present": section_name in section_names,
            "section_name": section_name,
            "metadata_only": True,
            "manifest_executed": False,
        },
        blocking_reasons=[] if section_name in section_names else [
            f"{section_name} missing"
        ],
    )


def _simple_flag_check(
    check_name: str,
    expected: bool | str,
    observed: bool | str,
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _sections_complete_check(
    sections: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    section_names = [
        _string_or_none(section.get("section_name")) or ""
        for section in sections
    ]
    missing_names = [
        name for name in REQUIRED_MANIFEST_SECTION_NAMES if name not in section_names
    ]
    extra_names = [
        name for name in section_names if name not in REQUIRED_MANIFEST_SECTION_NAMES
    ]
    return _check(
        "manifest_sections_complete_check",
        expected={
            "section_names": list(REQUIRED_MANIFEST_SECTION_NAMES),
            "section_count": len(REQUIRED_MANIFEST_SECTION_NAMES),
        },
        observed={
            "section_names": section_names,
            "section_count": len(section_names),
            "missing_section_names": missing_names,
            "extra_section_names": extra_names,
        },
        blocking_reasons=_deduplicate(
            [
                *(["manifest sections missing"] if missing_names else []),
                *(["unexpected manifest sections present"] if extra_names else []),
                *(
                    ["manifest section order must be stable"]
                    if section_names != list(REQUIRED_MANIFEST_SECTION_NAMES)
                    else []
                ),
            ]
        ),
    )


def _contracts_complete_check(
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    contract_names = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
    ]
    missing_names = [
        name
        for name in REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES
        if name not in contract_names
    ]
    extra_names = [
        name
        for name in contract_names
        if name not in REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES
    ]
    return _check(
        "manifest_contracts_complete_check",
        expected={
            "contract_names": list(REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES),
            "contract_count": len(REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES),
        },
        observed={
            "contract_names": contract_names,
            "contract_count": len(contract_names),
            "missing_contract_names": missing_names,
            "extra_contract_names": extra_names,
        },
        blocking_reasons=_deduplicate(
            [
                *(["manifest design contracts missing"] if missing_names else []),
                *(
                    ["unexpected manifest design contracts present"]
                    if extra_names
                    else []
                ),
                *(
                    ["manifest design contract order must be stable"]
                    if contract_names
                    != list(REQUIRED_MANIFEST_DESIGN_CONTRACT_NAMES)
                    else []
                ),
            ]
        ),
    )


def _deterministic_hash_check(
    registry: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    registry_repeat = _detached_json_value(
        build_governance_execution_adapter_declaration_schema_registry()
    )
    registry_hash = _string_or_none(
        registry.get("deterministic_declaration_schema_registry_hash")
    )
    registry_repeat_hash = _string_or_none(
        registry_repeat.get("deterministic_declaration_schema_registry_hash")
    )
    sections_hash = _hash_json_value(list(sections))
    sections_repeat_hash = _hash_json_value(_build_manifest_sections())
    contracts_hash = _hash_json_value(list(contracts))
    contracts_repeat_hash = _hash_json_value(
        _build_manifest_design_contracts(registry, _build_manifest_sections())
    )
    return _check(
        "deterministic_hash_check",
        expected={
            "declaration_schema_registry_hash_stable": True,
            "manifest_section_hash_stable": True,
            "manifest_contract_hash_stable": True,
            "hash_algorithm": (
                GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM
            ),
        },
        observed={
            "declaration_schema_registry_hash_stable": (
                registry == registry_repeat
                and registry_hash == registry_repeat_hash
            ),
            "declaration_schema_registry_hash_present": _is_sha256(
                registry_hash
            ),
            "manifest_section_hash_stable": (
                sections_hash == sections_repeat_hash
            ),
            "manifest_section_hash_present": _is_sha256(sections_hash),
            "manifest_contract_hash_stable": (
                contracts_hash == contracts_repeat_hash
            ),
            "manifest_contract_hash_present": _is_sha256(contracts_hash),
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["declaration schema registry hash must be stable"]
                    if registry != registry_repeat
                    or registry_hash != registry_repeat_hash
                    else []
                ),
                *(
                    ["declaration schema registry hash must be sha256"]
                    if not _is_sha256(registry_hash)
                    else []
                ),
                *(
                    ["manifest section hash must be stable"]
                    if sections_hash != sections_repeat_hash
                    else []
                ),
                *(
                    ["manifest section hash must be sha256"]
                    if not _is_sha256(sections_hash)
                    else []
                ),
                *(
                    ["manifest design contract hash must be stable"]
                    if contracts_hash != contracts_repeat_hash
                    else []
                ),
                *(
                    ["manifest design contract hash must be sha256"]
                    if not _is_sha256(contracts_hash)
                    else []
                ),
            ]
        ),
    )


def _redaction_boundary_check(
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    protected = {
        "section_names": [
            _string_or_none(section.get("section_name")) or ""
            for section in sections
        ],
        "section_statuses": [
            _string_or_none(section.get("design_status")) or ""
            for section in sections
        ],
        "contract_names": [
            _string_or_none(contract.get("contract_name")) or ""
            for contract in contracts
        ],
        "contract_statuses": [
            _string_or_none(contract.get("contract_status")) or ""
            for contract in contracts
        ],
        "manifest_design_summary": _manifest_design_summary(
            sections, contracts, ()
        ),
        "section_hash": _hash_json_value(list(sections)),
        "contract_hash": _hash_json_value(list(contracts)),
    }
    serialized = json.dumps(
        _detached_json_value(protected),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    leaked_terms = [
        term for term in _SENSITIVE_BLOCKED_TERMS if term in serialized
    ]
    return _check(
        "redaction_boundary_check",
        expected={
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
        },
        observed={
            "raw_fixture_events_included": False,
            "sensitive_term_hit_count": len(leaked_terms),
            "sensitive_terms_leaked": bool(leaked_terms),
        },
        blocking_reasons=[
            "manifest dry-run design metadata must not expose sensitive fields or values"
        ]
        if leaked_terms
        else [],
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _section(
        name,
        section_type="unknown_section",
        schema_field_refs=[],
        required=False,
        blocking_reasons=[
            "execution adapter manifest section name is not recognized"
        ],
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _contract(
        name,
        contract_type="unknown_contract",
        expected={"known_contract_name": True},
        observed={
            "known_contract_name": False,
            "requested_contract_name": name,
        },
        blocking_reasons=[
            "execution adapter manifest design contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter manifest design check name is not recognized"
        ],
    )


def _manifest_design_summary(
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_sections = [
        _string_or_none(section.get("section_name")) or ""
        for section in sections
        if section.get("design_status") != "pass"
    ]
    blocked_contracts = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
        if contract.get("contract_status") != "pass"
    ]
    blocked_checks = [
        _string_or_none(check.get("check_name")) or ""
        for check in checks
        if check.get("check_status") != "pass"
    ]
    return _detached_json_value(
        {
            "section_count": len(sections),
            "section_pass_count": len(sections) - len(blocked_sections),
            "section_blocked_count": len(blocked_sections),
            "blocked_section_names": blocked_sections,
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "manifest_dry_run_design_mode": MANIFEST_DRY_RUN_DESIGN_MODE,
            "manifest_dry_run_design_stage": (
                EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
            "execution_adapter_implemented": False,
            "execution_adapter_invoked": False,
            "manifest_executed": False,
            "dry_run_plan_executed": False,
            "real_execution_enabled": False,
            "external_calls_enabled": False,
            "durable_writes_enabled": False,
            "memory_graph_mutation_enabled": False,
            "operation_ledger_writes_enabled": False,
            "autonomous_execution_enabled": False,
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "manifest_design_status": (
                "safe"
                if not blocked_sections
                and not blocked_contracts
                and not blocked_checks
                else "blocked"
            ),
        }
    )


def _execution_adapter_manifest_dry_run_design_hash(
    manifest: Mapping[str, Any],
) -> str:
    hash_input = {
        field: manifest[field]
        for field in _MANIFEST_DRY_RUN_DESIGN_HASH_FIELDS
    }
    return _hash_json_value(hash_input)


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        _detached_json_value(value),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            _reject_non_finite(value),
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _reject_non_finite(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError("mapping keys must be strings")
        return {key: _reject_non_finite(value[key]) for key in value}
    if isinstance(value, list):
        return [_reject_non_finite(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("floats must be finite")
        return value
    raise ValueError("value must be deterministic JSON-compatible")


def _is_sha256(value: str | None) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _deduplicate(values: Sequence[str] | Any) -> list[str]:
    return list(dict.fromkeys(list(values)))


__all__ = [
    "EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_DRY_RUN_DESIGN_VERSION",
    "MANIFEST_DRY_RUN_DESIGN_MODE",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_manifest_dry_run_design",
    "get_governance_execution_adapter_manifest_design_check",
    "get_governance_execution_adapter_manifest_design_contract",
    "get_governance_execution_adapter_manifest_section",
    "governance_execution_adapter_manifest_dry_run_design_to_json",
    "list_governance_execution_adapter_manifest_design_check_names",
    "list_governance_execution_adapter_manifest_design_contract_names",
    "list_governance_execution_adapter_manifest_section_names",
]
