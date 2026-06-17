"""Deterministic schema-only registry for future execution adapter declarations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_boundary import (
    build_governance_execution_adapter_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION = "5.5.0"
GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_SCHEMA_VERSION = "5.5.0"
GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_TYPE = (
    "governance_execution_adapter_declaration_schema_registry"
)
GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE = (
    "v5.1_execution_adapter_declaration_schema_registry_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
DECLARATION_REGISTRY_MODE = "schema_only"

READY_HANDOFF_STATUS = "ready_for_future_adapter_manifest_dry_run_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES = (
    "adapter_id",
    "adapter_name",
    "adapter_kind",
    "adapter_version",
    "adapter_owner",
    "adapter_description",
    "declared_capabilities",
    "declared_inputs",
    "declared_outputs",
    "declared_permissions",
    "declared_side_effects",
    "declared_external_dependencies",
    "declared_durable_writes",
    "declared_memory_graph_mutations",
    "declared_operation_ledger_writes",
    "declared_approval_requirements",
    "declared_dry_run_inspection",
    "declared_redaction_policy",
    "declared_safety_boundaries",
    "declared_star_cosmos_entry_status",
)

REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES = (
    "schema_registry_declaration_only_contract",
    "adapter_identity_schema_contract",
    "adapter_capability_schema_contract",
    "adapter_input_schema_contract",
    "adapter_output_schema_contract",
    "adapter_permission_schema_contract",
    "adapter_side_effect_schema_contract",
    "adapter_external_dependency_schema_contract",
    "adapter_durable_write_schema_contract",
    "adapter_memory_graph_mutation_schema_contract",
    "adapter_operation_ledger_write_schema_contract",
    "adapter_human_approval_schema_contract",
    "adapter_dry_run_inspection_schema_contract",
    "adapter_redaction_schema_contract",
    "star_cosmos_candidate_only_schema_contract",
)

REQUIRED_DECLARATION_SCHEMA_CHECK_NAMES = (
    "execution_adapter_boundary_pass_check",
    "declaration_schema_registry_stage_check",
    "schema_only_mode_check",
    "declaration_fields_complete_check",
    "declaration_contracts_complete_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
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

_DECLARATION_SCHEMA_REGISTRY_HASH_FIELDS = (
    "version",
    "schema_version",
    "declaration_schema_registry_type",
    "declaration_schema_registry_status",
    "declaration_schema_registry_stage",
    "declaration_registry_mode",
    "star_cosmos_entry_status",
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "boundary_version",
    "boundary_status",
    "boundary_hash",
    "declaration_schema_fields",
    "declaration_schema_contracts",
    "declaration_schema_checks",
    "registry_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_DECLARATION_SCHEMA_REGISTRY_HASH_FIELDS),
    "input_shape": "sanitized execution adapter declaration schema registry projection",
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
)


def build_governance_execution_adapter_declaration_schema_registry() -> dict[str, Any]:
    """Build deterministic declaration-schema metadata without adapter behavior."""

    boundary = _detached_json_value(build_governance_execution_adapter_boundary())
    fields = _build_declaration_schema_fields()
    contracts = _build_declaration_schema_contracts(fields)
    checks = _build_declaration_schema_checks(boundary, fields, contracts)

    boundary_passes = (
        boundary.get("execution_adapter_boundary_status") == "pass"
        and boundary.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION
    )
    fields_pass = all(field["field_status"] == "pass" for field in fields)
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    registry_status = (
        "pass"
        if boundary_passes and fields_pass and contracts_pass and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["execution adapter boundary must pass at version 5.5.0"]
                if not boundary_passes
                else []
            ),
            *(
                reason
                for field in fields
                for reason in field["blocking_reasons"]
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
    registry: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_SCHEMA_VERSION
        ),
        "declaration_schema_registry_type": (
            GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_TYPE
        ),
        "declaration_schema_registry_status": registry_status,
        "declaration_schema_registry_stage": (
            EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE
        ),
        "declaration_registry_mode": DECLARATION_REGISTRY_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "star_cosmos_memory_active": False,
        "execution_adapter_implemented": False,
        "execution_adapter_invoked": False,
        "real_execution_enabled": False,
        "external_calls_enabled": False,
        "durable_writes_enabled": False,
        "memory_graph_mutation_enabled": False,
        "operation_ledger_writes_enabled": False,
        "autonomous_execution_enabled": False,
        "boundary_version": _string_or_none(boundary.get("version")),
        "boundary_status": _string_or_none(
            boundary.get("execution_adapter_boundary_status")
        ),
        "boundary_hash": _string_or_none(
            boundary.get("deterministic_execution_adapter_boundary_hash")
        ),
        "declaration_schema_fields": fields,
        "declaration_schema_contracts": contracts,
        "declaration_schema_checks": checks,
        "registry_summary": _registry_summary(fields, contracts, checks),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if registry_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    registry["deterministic_declaration_schema_registry_hash"] = (
        _execution_adapter_declaration_schema_registry_hash(registry)
    )
    return _detached_json_value(registry)


def get_governance_execution_adapter_declaration_schema_field(
    name: str,
) -> dict[str, Any]:
    """Return a detached future adapter declaration schema field by name."""

    if not isinstance(name, str):
        return _unknown_field("")
    for field in _build_declaration_schema_fields():
        if field["field_name"] == name:
            return _detached_json_value(field)
    return _unknown_field(name)


def get_governance_execution_adapter_declaration_schema_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached future adapter declaration schema contract by name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    fields = _build_declaration_schema_fields()
    for contract in _build_declaration_schema_contracts(fields):
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_declaration_schema_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached future adapter declaration schema check by name."""

    if not isinstance(name, str):
        return _unknown_check("")
    boundary = _detached_json_value(build_governance_execution_adapter_boundary())
    fields = _build_declaration_schema_fields()
    contracts = _build_declaration_schema_contracts(fields)
    for check in _build_declaration_schema_checks(boundary, fields, contracts):
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_declaration_schema_field_names() -> list[str]:
    """Return stable declaration schema field names in deterministic order."""

    return list(REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES)


def list_governance_execution_adapter_declaration_schema_contract_names() -> list[str]:
    """Return stable declaration schema contract names in deterministic order."""

    return list(REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES)


def list_governance_execution_adapter_declaration_schema_check_names() -> list[str]:
    """Return stable declaration schema check names in deterministic order."""

    return list(REQUIRED_DECLARATION_SCHEMA_CHECK_NAMES)


def governance_execution_adapter_declaration_schema_registry_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize declaration schema registry data deterministically."""

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


def _build_declaration_schema_fields() -> list[dict[str, Any]]:
    return [
        _field(
            "adapter_id",
            field_type="string",
            required=True,
            value_constraints={
                "non_empty": True,
                "stable_identifier_metadata_only": True,
                "active_binding_created": False,
            },
        ),
        _field(
            "adapter_name",
            field_type="string",
            required=True,
            value_constraints={
                "non_empty": True,
                "display_label_metadata_only": True,
            },
        ),
        _field(
            "adapter_kind",
            field_type="string",
            required=True,
            allowed_values=[
                "approval_workflow_adapter_candidate",
                "local_metadata_adapter_candidate",
                "repository_adapter_candidate",
                "service_adapter_candidate",
            ],
            value_constraints={"schema_declares_kind_only": True},
        ),
        _field(
            "adapter_version",
            field_type="string",
            required=True,
            value_constraints={
                "non_empty": True,
                "version_label_metadata_only": True,
            },
        ),
        _field(
            "adapter_owner",
            field_type="string",
            required=True,
            value_constraints={
                "non_empty": True,
                "owner_label_metadata_only": True,
                "sensitive_values_included": False,
            },
        ),
        _field(
            "adapter_description",
            field_type="string",
            required=True,
            value_constraints={
                "non_empty": True,
                "plain_metadata_description": True,
            },
        ),
        _field(
            "declared_capabilities",
            field_type="list[string]",
            required=True,
            default_value=[],
            value_constraints={
                "capability_names_only": True,
                "capability_invocation_available": False,
            },
        ),
        _field(
            "declared_inputs",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "input_schema_metadata_only": True,
                "runtime_input_accepted": False,
                "raw_fixture_events_included": False,
            },
        ),
        _field(
            "declared_outputs",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "output_schema_metadata_only": True,
                "runtime_output_returned": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
        ),
        _field(
            "declared_permissions",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "permission_schema_metadata_only": True,
                "permission_granted": False,
                "approval_granted": False,
            },
        ),
        _field(
            "declared_side_effects",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "side_effect_schema_metadata_only": True,
                "unsafe_side_effects_performed": False,
                "real_execution_performed": False,
            },
        ),
        _field(
            "declared_external_dependencies",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "dependency_schema_metadata_only": True,
                "external_calls_enabled": False,
                "external_calls_performed": False,
            },
        ),
        _field(
            "declared_durable_writes",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "durable_write_schema_metadata_only": True,
                "durable_writes_enabled": False,
                "durable_memory_written": False,
            },
        ),
        _field(
            "declared_memory_graph_mutations",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "memory_graph_mutation_schema_metadata_only": True,
                "memory_graph_mutation_enabled": False,
                "graph_mutation_surface_available": False,
            },
        ),
        _field(
            "declared_operation_ledger_writes",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "operation_ledger_write_schema_metadata_only": True,
                "operation_ledger_writes_enabled": False,
                "operation_ledger_entry_created": False,
            },
        ),
        _field(
            "declared_approval_requirements",
            field_type="list[object]",
            required=True,
            default_value=[],
            value_constraints={
                "approval_schema_metadata_only": True,
                "approval_request_created": False,
                "approval_request_executed": False,
                "real_approval_granted": False,
            },
        ),
        _field(
            "declared_dry_run_inspection",
            field_type="object",
            required=True,
            default_value={
                "dry_run_inspection_schema_only": True,
                "dry_run_executed": False,
                "dry_run_plan_executed": False,
            },
            value_constraints={
                "inspection_metadata_only": True,
                "dry_run_plan_execution_available": False,
            },
        ),
        _field(
            "declared_redaction_policy",
            field_type="object",
            required=True,
            default_value={
                "raw_fixture_events_included": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
            value_constraints={
                "redaction_metadata_only": True,
                "sensitive_values_included": False,
            },
        ),
        _field(
            "declared_safety_boundaries",
            field_type="object",
            required=True,
            default_value=dict(SAFETY_BOUNDARIES),
            value_constraints={
                "all_safety_flags_false": True,
                "safety_contract_metadata_only": True,
            },
        ),
        _field(
            "declared_star_cosmos_entry_status",
            field_type="string",
            required=True,
            allowed_values=[STAR_COSMOS_ENTRY_STATUS],
            default_value=STAR_COSMOS_ENTRY_STATUS,
            value_constraints={
                "star_cosmos_memory_active": False,
                "candidate_only": True,
            },
        ),
    ]


def _build_declaration_schema_contracts(
    fields: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    field_names = [
        _string_or_none(field.get("field_name")) or "" for field in fields
    ]
    return [
        _contract(
            "schema_registry_declaration_only_contract",
            contract_type="declaration_schema_contract",
            expected={
                "declaration_registry_mode": DECLARATION_REGISTRY_MODE,
                "schema_metadata_only": True,
                "adapter_invocation_available": False,
            },
            observed={
                "declaration_registry_mode": DECLARATION_REGISTRY_MODE,
                "schema_metadata_only": True,
                "adapter_invocation_available": False,
            },
        ),
        _contract(
            "adapter_identity_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "identity_fields": [
                    "adapter_id",
                    "adapter_name",
                    "adapter_kind",
                    "adapter_version",
                    "adapter_owner",
                    "adapter_description",
                ],
                "active_adapter_identity_present": False,
            },
            observed={
                "identity_fields_present": [
                    name
                    for name in (
                        "adapter_id",
                        "adapter_name",
                        "adapter_kind",
                        "adapter_version",
                        "adapter_owner",
                        "adapter_description",
                    )
                    if name in field_names
                ],
                "active_adapter_identity_present": False,
            },
        ),
        _contract(
            "adapter_capability_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_capabilities_field_present": True,
                "capability_invocation_available": False,
            },
            observed={
                "declared_capabilities_field_present": (
                    "declared_capabilities" in field_names
                ),
                "capability_invocation_available": False,
            },
        ),
        _contract(
            "adapter_input_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_inputs_field_present": True,
                "runtime_input_accepted": False,
                "raw_fixture_events_included": False,
            },
            observed={
                "declared_inputs_field_present": "declared_inputs" in field_names,
                "runtime_input_accepted": False,
                "raw_fixture_events_included": False,
            },
        ),
        _contract(
            "adapter_output_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_outputs_field_present": True,
                "runtime_output_returned": False,
                "sensitive_values_included": False,
            },
            observed={
                "declared_outputs_field_present": "declared_outputs" in field_names,
                "runtime_output_returned": False,
                "sensitive_values_included": False,
            },
        ),
        _contract(
            "adapter_permission_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_permissions_field_present": True,
                "permission_granted": False,
                "real_approval_granted": False,
            },
            observed={
                "declared_permissions_field_present": (
                    "declared_permissions" in field_names
                ),
                "permission_granted": False,
                "real_approval_granted": False,
            },
        ),
        _contract(
            "adapter_side_effect_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_side_effects_field_present": True,
                "unsafe_side_effects_performed": False,
                "real_execution_performed": False,
            },
            observed={
                "declared_side_effects_field_present": (
                    "declared_side_effects" in field_names
                ),
                "unsafe_side_effects_performed": False,
                "real_execution_performed": False,
            },
        ),
        _contract(
            "adapter_external_dependency_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_external_dependencies_field_present": True,
                "external_calls_enabled": False,
                "external_calls_performed": False,
            },
            observed={
                "declared_external_dependencies_field_present": (
                    "declared_external_dependencies" in field_names
                ),
                "external_calls_enabled": False,
                "external_calls_performed": False,
            },
        ),
        _contract(
            "adapter_durable_write_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_durable_writes_field_present": True,
                "durable_writes_enabled": False,
                "durable_memory_written": False,
            },
            observed={
                "declared_durable_writes_field_present": (
                    "declared_durable_writes" in field_names
                ),
                "durable_writes_enabled": False,
                "durable_memory_written": False,
            },
        ),
        _contract(
            "adapter_memory_graph_mutation_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_memory_graph_mutations_field_present": True,
                "memory_graph_mutation_enabled": False,
                "graph_mutation_surface_available": False,
            },
            observed={
                "declared_memory_graph_mutations_field_present": (
                    "declared_memory_graph_mutations" in field_names
                ),
                "memory_graph_mutation_enabled": False,
                "graph_mutation_surface_available": False,
            },
        ),
        _contract(
            "adapter_operation_ledger_write_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_operation_ledger_writes_field_present": True,
                "operation_ledger_writes_enabled": False,
                "operation_ledger_entry_created": False,
            },
            observed={
                "declared_operation_ledger_writes_field_present": (
                    "declared_operation_ledger_writes" in field_names
                ),
                "operation_ledger_writes_enabled": False,
                "operation_ledger_entry_created": False,
            },
        ),
        _contract(
            "adapter_human_approval_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_approval_requirements_field_present": True,
                "approval_request_created": False,
                "approval_request_executed": False,
                "real_approval_granted": False,
            },
            observed={
                "declared_approval_requirements_field_present": (
                    "declared_approval_requirements" in field_names
                ),
                "approval_request_created": False,
                "approval_request_executed": False,
                "real_approval_granted": False,
            },
        ),
        _contract(
            "adapter_dry_run_inspection_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_dry_run_inspection_field_present": True,
                "dry_run_executed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "declared_dry_run_inspection_field_present": (
                    "declared_dry_run_inspection" in field_names
                ),
                "dry_run_executed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "adapter_redaction_schema_contract",
            contract_type="adapter_declaration_schema_contract",
            expected={
                "declared_redaction_policy_field_present": True,
                "raw_fixture_events_included": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
            observed={
                "declared_redaction_policy_field_present": (
                    "declared_redaction_policy" in field_names
                ),
                "raw_fixture_events_included": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
        ),
        _contract(
            "star_cosmos_candidate_only_schema_contract",
            contract_type="candidate_schema_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
        ),
    ]


def _build_declaration_schema_checks(
    boundary: Mapping[str, Any],
    fields: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    boundary_hash = _string_or_none(
        boundary.get("deterministic_execution_adapter_boundary_hash")
    )
    return [
        _check(
            "execution_adapter_boundary_pass_check",
            expected={
                "boundary_status": "pass",
                "boundary_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION
                ),
                "boundary_hash_present": True,
            },
            observed={
                "boundary_status": _string_or_none(
                    boundary.get("execution_adapter_boundary_status")
                ),
                "boundary_version": _string_or_none(boundary.get("version")),
                "boundary_hash_present": _is_sha256(boundary_hash),
            },
            blocking_reasons=_deduplicate(
                [
                    *(
                        ["execution adapter boundary status must pass"]
                        if boundary.get("execution_adapter_boundary_status")
                        != "pass"
                        else []
                    ),
                    *(
                        ["execution adapter boundary version must equal 5.5.0"]
                        if boundary.get("version")
                        != GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION
                        else []
                    ),
                    *(
                        ["execution adapter boundary hash must be sha256"]
                        if not _is_sha256(boundary_hash)
                        else []
                    ),
                ]
            ),
        ),
        _simple_flag_check(
            "declaration_schema_registry_stage_check",
            expected=EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE,
            observed=EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE,
        ),
        _simple_flag_check(
            "schema_only_mode_check",
            expected=DECLARATION_REGISTRY_MODE,
            observed=DECLARATION_REGISTRY_MODE,
        ),
        _field_completeness_check(fields),
        _contract_completeness_check(contracts),
        _simple_flag_check("adapter_not_implemented_check", expected=False, observed=False),
        _simple_flag_check("adapter_not_invoked_check", expected=False, observed=False),
        _simple_flag_check("real_execution_disabled_check", expected=False, observed=False),
        _simple_flag_check("external_calls_disabled_check", expected=False, observed=False),
        _simple_flag_check("durable_writes_disabled_check", expected=False, observed=False),
        _simple_flag_check(
            "memory_graph_mutation_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "operation_ledger_writes_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "autonomous_execution_disabled_check",
            expected=False,
            observed=False,
        ),
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
        _deterministic_hash_check(boundary, fields, contracts),
        _redaction_boundary_check(fields, contracts),
    ]


def _field(
    field_name: str,
    *,
    field_type: str,
    required: bool,
    allowed_values: Sequence[Any] = (),
    value_constraints: Mapping[str, Any] | None = None,
    default_value: Any = None,
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    field: dict[str, Any] = {
        "field_name": field_name,
        "field_type": field_type,
        "required": required,
        "allowed_values": list(allowed_values),
        "value_constraints": _detached_json_value(value_constraints or {}),
        "default_value": _detached_json_value(default_value),
        "field_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(field)


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


def _simple_flag_check(
    check_name: str,
    *,
    expected: bool | str,
    observed: bool | str,
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _field_completeness_check(
    fields: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    field_names = [
        _string_or_none(field.get("field_name")) or "" for field in fields
    ]
    missing_names = [
        name
        for name in REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES
        if name not in field_names
    ]
    extra_names = [
        name
        for name in field_names
        if name not in REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES
    ]
    return _check(
        "declaration_fields_complete_check",
        expected={
            "field_names": list(REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES),
            "field_count": len(REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES),
        },
        observed={
            "field_names": field_names,
            "field_count": len(field_names),
            "missing_field_names": missing_names,
            "extra_field_names": extra_names,
        },
        blocking_reasons=_deduplicate(
            [
                *(["declaration schema fields missing"] if missing_names else []),
                *(["unexpected declaration schema fields present"] if extra_names else []),
                *(
                    ["declaration schema field order must be stable"]
                    if field_names
                    != list(REQUIRED_DECLARATION_SCHEMA_FIELD_NAMES)
                    else []
                ),
            ]
        ),
    )


def _contract_completeness_check(
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    contract_names = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
    ]
    missing_names = [
        name
        for name in REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES
        if name not in contract_names
    ]
    extra_names = [
        name
        for name in contract_names
        if name not in REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES
    ]
    return _check(
        "declaration_contracts_complete_check",
        expected={
            "contract_names": list(REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES),
            "contract_count": len(REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES),
        },
        observed={
            "contract_names": contract_names,
            "contract_count": len(contract_names),
            "missing_contract_names": missing_names,
            "extra_contract_names": extra_names,
        },
        blocking_reasons=_deduplicate(
            [
                *(["declaration schema contracts missing"] if missing_names else []),
                *(["unexpected declaration schema contracts present"] if extra_names else []),
                *(
                    ["declaration schema contract order must be stable"]
                    if contract_names
                    != list(REQUIRED_DECLARATION_SCHEMA_CONTRACT_NAMES)
                    else []
                ),
            ]
        ),
    )


def _deterministic_hash_check(
    boundary: Mapping[str, Any],
    fields: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    boundary_repeat = _detached_json_value(build_governance_execution_adapter_boundary())
    boundary_hash = _string_or_none(
        boundary.get("deterministic_execution_adapter_boundary_hash")
    )
    boundary_repeat_hash = _string_or_none(
        boundary_repeat.get("deterministic_execution_adapter_boundary_hash")
    )
    fields_hash = _hash_json_value(list(fields))
    fields_repeat_hash = _hash_json_value(_build_declaration_schema_fields())
    contracts_hash = _hash_json_value(list(contracts))
    contracts_repeat_hash = _hash_json_value(
        _build_declaration_schema_contracts(_build_declaration_schema_fields())
    )
    return _check(
        "deterministic_hash_check",
        expected={
            "boundary_hash_stable": True,
            "field_hash_stable": True,
            "contract_hash_stable": True,
            "hash_algorithm": (
                GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM
            ),
        },
        observed={
            "boundary_hash_stable": (
                boundary == boundary_repeat
                and boundary_hash == boundary_repeat_hash
            ),
            "boundary_hash_present": _is_sha256(boundary_hash),
            "field_hash_stable": fields_hash == fields_repeat_hash,
            "field_hash_present": _is_sha256(fields_hash),
            "contract_hash_stable": contracts_hash == contracts_repeat_hash,
            "contract_hash_present": _is_sha256(contracts_hash),
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["execution adapter boundary hash must be stable"]
                    if boundary != boundary_repeat
                    or boundary_hash != boundary_repeat_hash
                    else []
                ),
                *(
                    ["execution adapter boundary hash must be sha256"]
                    if not _is_sha256(boundary_hash)
                    else []
                ),
                *(
                    ["declaration schema field hash must be stable"]
                    if fields_hash != fields_repeat_hash
                    else []
                ),
                *(
                    ["declaration schema field hash must be sha256"]
                    if not _is_sha256(fields_hash)
                    else []
                ),
                *(
                    ["declaration schema contract hash must be stable"]
                    if contracts_hash != contracts_repeat_hash
                    else []
                ),
                *(
                    ["declaration schema contract hash must be sha256"]
                    if not _is_sha256(contracts_hash)
                    else []
                ),
            ]
        ),
    )


def _redaction_boundary_check(
    fields: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    protected = {
        "field_names": [
            _string_or_none(field.get("field_name")) or "" for field in fields
        ],
        "field_statuses": [
            _string_or_none(field.get("field_status")) or "" for field in fields
        ],
        "contract_names": [
            _string_or_none(contract.get("contract_name")) or ""
            for contract in contracts
        ],
        "contract_statuses": [
            _string_or_none(contract.get("contract_status")) or ""
            for contract in contracts
        ],
        "registry_summary": _registry_summary(fields, contracts, ()),
        "field_hash": _hash_json_value(list(fields)),
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
            "declaration schema registry metadata must not expose sensitive fields or values"
        ]
        if leaked_terms
        else [],
    )


def _unknown_field(name: str) -> dict[str, Any]:
    return _field(
        name,
        field_type="unknown_field",
        required=False,
        value_constraints={"known_field_name": True},
        blocking_reasons=[
            "execution adapter declaration schema field name is not recognized"
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
            "execution adapter declaration schema contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter declaration schema check name is not recognized"
        ],
    )


def _registry_summary(
    fields: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_fields = [
        _string_or_none(field.get("field_name")) or ""
        for field in fields
        if field.get("field_status") != "pass"
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
            "field_count": len(fields),
            "field_pass_count": len(fields) - len(blocked_fields),
            "field_blocked_count": len(blocked_fields),
            "blocked_field_names": blocked_fields,
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "declaration_registry_mode": DECLARATION_REGISTRY_MODE,
            "declaration_schema_registry_stage": (
                EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
            "execution_adapter_implemented": False,
            "execution_adapter_invoked": False,
            "real_execution_enabled": False,
            "external_calls_enabled": False,
            "durable_writes_enabled": False,
            "memory_graph_mutation_enabled": False,
            "operation_ledger_writes_enabled": False,
            "autonomous_execution_enabled": False,
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "registry_status": (
                "safe"
                if not blocked_fields and not blocked_contracts and not blocked_checks
                else "blocked"
            ),
        }
    )


def _execution_adapter_declaration_schema_registry_hash(
    registry: Mapping[str, Any],
) -> str:
    hash_input = {
        field: registry[field]
        for field in _DECLARATION_SCHEMA_REGISTRY_HASH_FIELDS
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
    "DECLARATION_REGISTRY_MODE",
    "EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_declaration_schema_registry",
    "get_governance_execution_adapter_declaration_schema_check",
    "get_governance_execution_adapter_declaration_schema_contract",
    "get_governance_execution_adapter_declaration_schema_field",
    "governance_execution_adapter_declaration_schema_registry_to_json",
    "list_governance_execution_adapter_declaration_schema_check_names",
    "list_governance_execution_adapter_declaration_schema_contract_names",
    "list_governance_execution_adapter_declaration_schema_field_names",
]
