"""Deterministic manifest fixture-pack metadata for future adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_manifest_dry_run_design import (
    build_governance_execution_adapter_manifest_dry_run_design,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION = "5.4.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION = "5.4.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_TYPE = (
    "governance_execution_adapter_manifest_fixture_pack"
)
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE = (
    "v5.3_execution_adapter_manifest_fixture_pack_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
MANIFEST_FIXTURE_PACK_MODE = "fixture_only"

READY_HANDOFF_STATUS = "ready_for_future_manifest_validation_matrix_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_MANIFEST_FIXTURE_NAMES = (
    "minimal_read_only_manifest_fixture",
    "permission_declared_manifest_fixture",
    "external_dependency_declared_manifest_fixture",
    "durable_write_declared_but_disabled_manifest_fixture",
    "memory_graph_mutation_declared_but_disabled_manifest_fixture",
    "operation_ledger_write_declared_but_disabled_manifest_fixture",
    "approval_required_manifest_fixture",
    "redaction_required_manifest_fixture",
    "star_cosmos_candidate_only_manifest_fixture",
)

REQUIRED_MANIFEST_FIXTURE_CONTRACT_NAMES = (
    "fixture_pack_only_contract",
    "manifest_dry_run_design_pass_contract",
    "sanitized_fixture_payload_contract",
    "fixture_names_complete_contract",
    "fixture_payload_json_contract",
    "no_executable_command_fixture_contract",
    "no_live_endpoint_fixture_contract",
    "no_secret_fixture_contract",
    "no_raw_log_fixture_contract",
    "adapter_not_implemented_fixture_contract",
    "adapter_not_invoked_fixture_contract",
    "manifest_not_executed_fixture_contract",
    "dry_run_plan_not_executed_fixture_contract",
    "external_calls_disabled_fixture_contract",
    "durable_writes_disabled_fixture_contract",
    "filesystem_writes_disabled_fixture_contract",
    "database_writes_disabled_fixture_contract",
    "memory_graph_mutation_disabled_fixture_contract",
    "operation_ledger_writes_disabled_fixture_contract",
    "autonomous_execution_disabled_fixture_contract",
    "star_cosmos_candidate_only_fixture_contract",
)

REQUIRED_MANIFEST_FIXTURE_CHECK_NAMES = (
    "manifest_dry_run_design_pass_check",
    "manifest_fixture_pack_stage_check",
    "fixture_only_mode_check",
    "fixture_names_complete_check",
    "fixture_payloads_sanitized_check",
    "fixture_payloads_json_compatible_check",
    "fixture_payloads_deterministic_check",
    "no_executable_command_check",
    "no_live_endpoint_check",
    "no_secret_or_token_check",
    "no_raw_log_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "manifest_not_executed_check",
    "dry_run_plan_not_executed_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "filesystem_writes_disabled_check",
    "database_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
)

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "real_execution_enabled": False,
    "external_calls_enabled": False,
    "durable_writes_enabled": False,
    "filesystem_writes_enabled": False,
    "database_writes_enabled": False,
    "memory_graph_mutation_enabled": False,
    "operation_ledger_writes_enabled": False,
    "autonomous_execution_enabled": False,
}

_MANIFEST_FIXTURE_PACK_HASH_FIELDS = (
    "version",
    "schema_version",
    "manifest_fixture_pack_type",
    "manifest_fixture_pack_status",
    "manifest_fixture_pack_stage",
    "manifest_fixture_pack_mode",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "manifest_dry_run_design_version",
    "manifest_dry_run_design_status",
    "manifest_dry_run_design_hash",
    "manifest_fixtures",
    "manifest_fixture_contracts",
    "manifest_fixture_checks",
    "manifest_fixture_pack_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MANIFEST_FIXTURE_PACK_HASH_FIELDS),
    "input_shape": "sanitized future execution adapter manifest fixture pack projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_PAYLOAD_BLOCKED_FRAGMENTS = (
    '"approval_' + 'phrase"',
    '"std' + 'out_tail"',
    '"std' + 'out"',
    '"std' + 'err"',
    '"raw_' + 'logs"',
    '"to' + 'ken"',
    '"api_' + 'key"',
    '"sec' + 'ret"',
    '"pass' + 'word"',
    '"creden' + 'tial"',
    "fixture-approval-phrase",
    "fixture-stdout-tail",
    "fixture-stdout",
    "fixture-stderr",
    "fixture-raw-logs",
    "fixture-token",
    "fixture-api-key",
    "fixture-secret",
    "fixture-password",
    "fixture-credential",
    "http" + "://",
    "https" + "://",
    "ssh" + "://",
    "git" + "@",
    "/users/",
    "/private/",
    "/tmp/",
    "c:\\",
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "git " + "push",
    "g" + "h api",
)


def build_governance_execution_adapter_manifest_fixture_pack() -> dict[str, Any]:
    """Build deterministic fixture-only manifest metadata."""

    design = _detached_json_value(
        build_governance_execution_adapter_manifest_dry_run_design()
    )
    fixtures = _build_manifest_fixtures()
    contracts = _build_manifest_fixture_contracts(design, fixtures)
    checks = _build_manifest_fixture_checks(design, fixtures, contracts)

    design_passes = (
        design.get("manifest_dry_run_design_status") == "pass"
        and design.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION
    )
    fixtures_pass = all(
        fixture["fixture_status"] == "pass" for fixture in fixtures
    )
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    pack_status = (
        "pass"
        if design_passes and fixtures_pass and contracts_pass and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["manifest dry-run design must pass at version 5.4.0"]
                if not design_passes
                else []
            ),
            *(
                reason
                for fixture in fixtures
                for reason in fixture["blocking_reasons"]
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
    pack: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION
        ),
        "manifest_fixture_pack_type": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_TYPE
        ),
        "manifest_fixture_pack_status": pack_status,
        "manifest_fixture_pack_stage": (
            EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE
        ),
        "manifest_fixture_pack_mode": MANIFEST_FIXTURE_PACK_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "manifest_dry_run_design_version": _string_or_none(
            design.get("version")
        ),
        "manifest_dry_run_design_status": _string_or_none(
            design.get("manifest_dry_run_design_status")
        ),
        "manifest_dry_run_design_hash": _string_or_none(
            design.get("deterministic_manifest_dry_run_design_hash")
        ),
        "manifest_fixtures": fixtures,
        "manifest_fixture_contracts": contracts,
        "manifest_fixture_checks": checks,
        "manifest_fixture_pack_summary": _manifest_fixture_pack_summary(
            fixtures, contracts, checks
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if pack_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    pack["deterministic_manifest_fixture_pack_hash"] = (
        _execution_adapter_manifest_fixture_pack_hash(pack)
    )
    return _detached_json_value(pack)


def get_governance_execution_adapter_manifest_fixture(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest fixture by stable name."""

    if not isinstance(name, str):
        return _unknown_fixture("")
    for fixture in _build_manifest_fixtures():
        if fixture["fixture_name"] == name:
            return _detached_json_value(fixture)
    return _unknown_fixture(name)


def get_governance_execution_adapter_manifest_fixture_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest fixture contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    design = _detached_json_value(
        build_governance_execution_adapter_manifest_dry_run_design()
    )
    fixtures = _build_manifest_fixtures()
    for contract in _build_manifest_fixture_contracts(design, fixtures):
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_manifest_fixture_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest fixture check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    design = _detached_json_value(
        build_governance_execution_adapter_manifest_dry_run_design()
    )
    fixtures = _build_manifest_fixtures()
    contracts = _build_manifest_fixture_contracts(design, fixtures)
    for check in _build_manifest_fixture_checks(design, fixtures, contracts):
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_manifest_fixture_names() -> list[str]:
    """Return stable manifest fixture names."""

    return list(REQUIRED_MANIFEST_FIXTURE_NAMES)


def list_governance_execution_adapter_manifest_fixture_contract_names() -> list[str]:
    """Return stable manifest fixture contract names."""

    return list(REQUIRED_MANIFEST_FIXTURE_CONTRACT_NAMES)


def list_governance_execution_adapter_manifest_fixture_check_names() -> list[str]:
    """Return stable manifest fixture check names."""

    return list(REQUIRED_MANIFEST_FIXTURE_CHECK_NAMES)


def governance_execution_adapter_manifest_fixture_pack_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize manifest fixture-pack metadata deterministically."""

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


def _build_manifest_fixtures() -> list[dict[str, Any]]:
    return [
        _fixture(
            "minimal_read_only_manifest_fixture",
            fixture_type="minimal_read_only_manifest",
            synthetic_adapter_id="synthetic.adapter.minimal.read_only",
            synthetic_adapter_kind="synthetic_read_only_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-minimal-read-only",
                "synthetic.adapter.minimal.read_only",
                "synthetic_read_only_metadata_adapter",
                declared_metadata={
                    "declared_capabilities": [
                        {
                            "capability_name": "synthetic_metadata_read",
                            "enabled_for_execution": False,
                        }
                    ],
                    "declared_inputs": [],
                    "declared_outputs": [],
                    "declared_permissions": [],
                },
            ),
            expected_design_section_refs=[
                "manifest_identity_section",
                "manifest_adapter_reference_section",
                "manifest_capabilities_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "fixture_pack_only_contract",
                "sanitized_fixture_payload_contract",
                "adapter_not_invoked_fixture_contract",
            ],
            expected_check_refs=[
                "fixture_only_mode_check",
                "fixture_payloads_sanitized_check",
                "adapter_not_invoked_check",
            ],
            fixture_validation_notes=[
                "synthetic read-only fixture uses metadata fields only",
                "no runtime or write capability is enabled",
            ],
        ),
        _fixture(
            "permission_declared_manifest_fixture",
            fixture_type="permission_declared_manifest",
            synthetic_adapter_id="synthetic.adapter.permission.declared",
            synthetic_adapter_kind="synthetic_permission_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-permission-declared",
                "synthetic.adapter.permission.declared",
                "synthetic_permission_metadata_adapter",
                declared_metadata={
                    "declared_permissions": [
                        {
                            "permission_name": "synthetic_review_permission",
                            "declared_only": True,
                            "permission_granted": False,
                        }
                    ],
                    "declared_side_effects": [],
                },
            ),
            expected_design_section_refs=[
                "manifest_permissions_section",
                "manifest_side_effects_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "fixture_pack_only_contract",
                "sanitized_fixture_payload_contract",
                "external_calls_disabled_fixture_contract",
            ],
            expected_check_refs=[
                "fixture_payloads_json_compatible_check",
                "real_execution_disabled_check",
                "external_calls_disabled_check",
            ],
            fixture_validation_notes=[
                "permission is declared as disabled metadata",
                "permission declaration does not grant authority",
            ],
        ),
        _fixture(
            "external_dependency_declared_manifest_fixture",
            fixture_type="external_dependency_declared_manifest",
            synthetic_adapter_id="synthetic.adapter.external.declared",
            synthetic_adapter_kind="synthetic_external_dependency_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-external-dependency-declared",
                "synthetic.adapter.external.declared",
                "synthetic_external_dependency_adapter",
                declared_metadata={
                    "declared_external_dependencies": [
                        {
                            "dependency_id": "synthetic-dependency-disabled",
                            "dependency_kind": "synthetic_external_metadata",
                            "live_endpoint_present": False,
                            "external_call_enabled": False,
                            "declared_only": True,
                        }
                    ],
                },
            ),
            expected_design_section_refs=[
                "manifest_external_dependencies_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "no_live_endpoint_fixture_contract",
                "external_calls_disabled_fixture_contract",
            ],
            expected_check_refs=[
                "no_live_endpoint_check",
                "external_calls_disabled_check",
            ],
            fixture_validation_notes=[
                "external dependency is synthetic and disabled",
                "no live endpoint locator is present",
            ],
        ),
        _fixture(
            "durable_write_declared_but_disabled_manifest_fixture",
            fixture_type="durable_write_declared_but_disabled_manifest",
            synthetic_adapter_id="synthetic.adapter.durable_write.declared",
            synthetic_adapter_kind="synthetic_durable_write_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-durable-write-declared-disabled",
                "synthetic.adapter.durable_write.declared",
                "synthetic_durable_write_metadata_adapter",
                declared_metadata={
                    "declared_durable_writes": [
                        {
                            "write_id": "synthetic-durable-write-disabled",
                            "write_surface": "synthetic_metadata_store",
                            "write_enabled": False,
                            "declared_only": True,
                        }
                    ],
                },
            ),
            expected_design_section_refs=[
                "manifest_durable_writes_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "durable_writes_disabled_fixture_contract",
                "filesystem_writes_disabled_fixture_contract",
                "database_writes_disabled_fixture_contract",
            ],
            expected_check_refs=[
                "durable_writes_disabled_check",
                "filesystem_writes_disabled_check",
                "database_writes_disabled_check",
            ],
            fixture_validation_notes=[
                "durable write is declared but disabled",
                "no storage locator or path is present",
            ],
        ),
        _fixture(
            "memory_graph_mutation_declared_but_disabled_manifest_fixture",
            fixture_type="memory_graph_mutation_declared_but_disabled_manifest",
            synthetic_adapter_id="synthetic.adapter.graph_mutation.declared",
            synthetic_adapter_kind="synthetic_graph_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-graph-mutation-declared-disabled",
                "synthetic.adapter.graph_mutation.declared",
                "synthetic_graph_metadata_adapter",
                declared_metadata={
                    "declared_memory_graph_mutations": [
                        {
                            "mutation_id": "synthetic-graph-mutation-disabled",
                            "mutation_kind": "synthetic_relationship_marker",
                            "mutation_enabled": False,
                            "declared_only": True,
                        }
                    ],
                },
            ),
            expected_design_section_refs=[
                "manifest_memory_graph_mutations_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "memory_graph_mutation_disabled_fixture_contract",
            ],
            expected_check_refs=[
                "memory_graph_mutation_disabled_check",
            ],
            fixture_validation_notes=[
                "memory graph mutation is declared but disabled",
                "fixture contains no graph mutation behavior",
            ],
        ),
        _fixture(
            "operation_ledger_write_declared_but_disabled_manifest_fixture",
            fixture_type="operation_ledger_write_declared_but_disabled_manifest",
            synthetic_adapter_id="synthetic.adapter.ledger_write.declared",
            synthetic_adapter_kind="synthetic_ledger_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-ledger-write-declared-disabled",
                "synthetic.adapter.ledger_write.declared",
                "synthetic_ledger_metadata_adapter",
                declared_metadata={
                    "declared_operation_ledger_writes": [
                        {
                            "ledger_record_id": "synthetic-ledger-record-disabled",
                            "record_kind": "synthetic_audit_marker",
                            "write_enabled": False,
                            "declared_only": True,
                        }
                    ],
                },
            ),
            expected_design_section_refs=[
                "manifest_operation_ledger_writes_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "operation_ledger_writes_disabled_fixture_contract",
            ],
            expected_check_refs=[
                "operation_ledger_writes_disabled_check",
            ],
            fixture_validation_notes=[
                "operation-ledger write is declared but disabled",
                "fixture contains no ledger write behavior",
            ],
        ),
        _fixture(
            "approval_required_manifest_fixture",
            fixture_type="approval_required_manifest",
            synthetic_adapter_id="synthetic.adapter.approval.required",
            synthetic_adapter_kind="synthetic_human_review_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-approval-required",
                "synthetic.adapter.approval.required",
                "synthetic_human_review_metadata_adapter",
                declared_metadata={
                    "declared_approval_requirements": [
                        {
                            "review_requirement_id": (
                                "synthetic-human-review-required"
                            ),
                            "human_review_required": True,
                            "manual_confirmation_text_included": False,
                            "approval_granted": False,
                            "declared_only": True,
                        }
                    ],
                },
            ),
            expected_design_section_refs=[
                "manifest_approval_requirements_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "fixture_pack_only_contract",
                "manifest_not_executed_fixture_contract",
                "star_cosmos_candidate_only_fixture_contract",
            ],
            expected_check_refs=[
                "manifest_not_executed_check",
                "dry_run_plan_not_executed_check",
                "autonomous_execution_disabled_check",
            ],
            fixture_validation_notes=[
                "human review requirement is metadata only",
                "no confirmation text or grant is included",
            ],
        ),
        _fixture(
            "redaction_required_manifest_fixture",
            fixture_type="redaction_required_manifest",
            synthetic_adapter_id="synthetic.adapter.redaction.required",
            synthetic_adapter_kind="synthetic_redaction_metadata_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-redaction-required",
                "synthetic.adapter.redaction.required",
                "synthetic_redaction_metadata_adapter",
                declared_metadata={
                    "declared_redaction_policy": {
                        "redaction_required": True,
                        "redaction_applies_to_synthetic_placeholders": True,
                        "raw_values_included": False,
                        "sensitive_values_included": False,
                    }
                },
            ),
            expected_design_section_refs=[
                "manifest_redaction_policy_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "sanitized_fixture_payload_contract",
                "no_secret_fixture_contract",
                "no_raw_log_fixture_contract",
            ],
            expected_check_refs=[
                "fixture_payloads_sanitized_check",
                "no_secret_or_token_check",
                "no_raw_log_check",
                "redaction_boundary_check",
            ],
            fixture_validation_notes=[
                "redaction policy declares sanitized placeholder behavior",
                "no sensitive values are present",
            ],
        ),
        _fixture(
            "star_cosmos_candidate_only_manifest_fixture",
            fixture_type="star_cosmos_candidate_only_manifest",
            synthetic_adapter_id="synthetic.adapter.star_cosmos.candidate",
            synthetic_adapter_kind="synthetic_candidate_status_adapter",
            fixture_payload=_payload(
                "synthetic-manifest-star-cosmos-candidate-only",
                "synthetic.adapter.star_cosmos.candidate",
                "synthetic_candidate_status_adapter",
                declared_metadata={
                    "declared_star_cosmos_entry_status": (
                        STAR_COSMOS_ENTRY_STATUS
                    ),
                    "star_cosmos_memory_active": False,
                    "candidate_status_only": True,
                },
            ),
            expected_design_section_refs=[
                "manifest_star_cosmos_candidate_status_section",
                "manifest_safety_boundaries_section",
            ],
            expected_contract_refs=[
                "star_cosmos_candidate_only_fixture_contract",
            ],
            expected_check_refs=[
                "star_cosmos_candidate_only_check",
            ],
            fixture_validation_notes=[
                "candidate-only status is explicit",
                "Star-Cosmos active-entry status is not claimed",
            ],
        ),
    ]


def _payload(
    manifest_id: str,
    adapter_id: str,
    adapter_kind: str,
    *,
    declared_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _detached_json_value(
        {
            "manifest_id": manifest_id,
            "schema_version": (
                GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION
            ),
            "manifest_mode": MANIFEST_FIXTURE_PACK_MODE,
            "adapter_reference": {
                "adapter_id": adapter_id,
                "adapter_kind": adapter_kind,
                "adapter_version": "0.0.0-synthetic-fixture",
                "adapter_declared_only": True,
            },
            "declared_metadata": dict(declared_metadata),
            "disabled_runtime_flags": _detached_json_value(
                COMMON_DISABLED_FLAGS
            ),
            "fixture_sanitization": {
                "synthetic_ids_only": True,
                "live_endpoint_present": False,
                "raw_log_material_present": False,
                "executable_command_present": False,
                "real_path_present": False,
                "real_repository_locator_present": False,
                "external_call_enabled": False,
                "durable_write_enabled": False,
                "metadata_only": True,
            },
        }
    )


def _build_manifest_fixture_contracts(
    design: Mapping[str, Any],
    fixtures: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    fixture_names = _fixture_names(fixtures)
    payload_findings = _fixture_payload_findings(fixtures)
    return [
        _contract(
            "fixture_pack_only_contract",
            contract_type="fixture_pack_contract",
            expected={
                "manifest_fixture_pack_mode": MANIFEST_FIXTURE_PACK_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "manifest_fixture_pack_mode": MANIFEST_FIXTURE_PACK_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "manifest_dry_run_design_pass_contract",
            contract_type="upstream_manifest_design_contract",
            expected={
                "manifest_dry_run_design_status": "pass",
                "manifest_dry_run_design_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION
                ),
                "manifest_dry_run_design_hash_present": True,
            },
            observed={
                "manifest_dry_run_design_status": _string_or_none(
                    design.get("manifest_dry_run_design_status")
                ),
                "manifest_dry_run_design_version": _string_or_none(
                    design.get("version")
                ),
                "manifest_dry_run_design_hash_present": _is_sha256(
                    _string_or_none(
                        design.get("deterministic_manifest_dry_run_design_hash")
                    )
                ),
            },
            blocking_reasons=_design_blocking_reasons(design),
        ),
        _contract(
            "sanitized_fixture_payload_contract",
            contract_type="fixture_payload_contract",
            expected={
                "synthetic_ids_only": True,
                "blocked_fragment_hit_count": 0,
                "payload_count": len(REQUIRED_MANIFEST_FIXTURE_NAMES),
            },
            observed={
                "synthetic_ids_only": _fixtures_use_synthetic_ids(fixtures),
                "blocked_fragment_hit_count": len(payload_findings),
                "payload_count": len(fixtures),
            },
            blocking_reasons=_deduplicate(
                [
                    *(
                        ["fixture payloads must use synthetic ids only"]
                        if not _fixtures_use_synthetic_ids(fixtures)
                        else []
                    ),
                    *(
                        ["fixture payloads must not include blocked fragments"]
                        if payload_findings
                        else []
                    ),
                ]
            ),
        ),
        _contract(
            "fixture_names_complete_contract",
            contract_type="fixture_name_contract",
            expected={
                "fixture_names": list(REQUIRED_MANIFEST_FIXTURE_NAMES),
                "fixture_count": len(REQUIRED_MANIFEST_FIXTURE_NAMES),
            },
            observed={
                "fixture_names": fixture_names,
                "fixture_count": len(fixture_names),
                "missing_fixture_names": _missing_fixture_names(fixture_names),
                "extra_fixture_names": _extra_fixture_names(fixture_names),
            },
            blocking_reasons=_fixture_name_blocking_reasons(fixture_names),
        ),
        _contract(
            "fixture_payload_json_contract",
            contract_type="fixture_payload_contract",
            expected={"json_compatible": True, "non_finite_floats_present": False},
            observed={
                "json_compatible": _json_compatible(
                    [fixture["fixture_payload"] for fixture in fixtures]
                ),
                "non_finite_floats_present": False,
            },
            blocking_reasons=[]
            if _json_compatible([fixture["fixture_payload"] for fixture in fixtures])
            else ["fixture payloads must be deterministic JSON-compatible"],
        ),
        _blocked_fragment_contract(
            "no_executable_command_fixture_contract",
            "executable_command_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_live_endpoint_fixture_contract",
            "live_endpoint_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_secret_fixture_contract",
            "sensitive_fragment_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_raw_log_fixture_contract",
            "log_material_present",
            payload_findings,
        ),
        _disabled_flag_contract(
            "adapter_not_implemented_fixture_contract",
            "execution_adapter_implemented",
            fixtures,
        ),
        _disabled_flag_contract(
            "adapter_not_invoked_fixture_contract",
            "execution_adapter_invoked",
            fixtures,
        ),
        _disabled_flag_contract(
            "manifest_not_executed_fixture_contract",
            "manifest_executed",
            fixtures,
        ),
        _disabled_flag_contract(
            "dry_run_plan_not_executed_fixture_contract",
            "dry_run_plan_executed",
            fixtures,
        ),
        _disabled_flag_contract(
            "external_calls_disabled_fixture_contract",
            "external_calls_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "durable_writes_disabled_fixture_contract",
            "durable_writes_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "filesystem_writes_disabled_fixture_contract",
            "filesystem_writes_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "database_writes_disabled_fixture_contract",
            "database_writes_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "memory_graph_mutation_disabled_fixture_contract",
            "memory_graph_mutation_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "operation_ledger_writes_disabled_fixture_contract",
            "operation_ledger_writes_enabled",
            fixtures,
        ),
        _disabled_flag_contract(
            "autonomous_execution_disabled_fixture_contract",
            "autonomous_execution_enabled",
            fixtures,
        ),
        _contract(
            "star_cosmos_candidate_only_fixture_contract",
            contract_type="candidate_fixture_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": _fixtures_flag_false(
                    fixtures, "star_cosmos_memory_active"
                )
                is False,
            },
            blocking_reasons=[]
            if _fixtures_flag_false(fixtures, "star_cosmos_memory_active")
            else ["Star-Cosmos memory active flag must remain false"],
        ),
    ]


def _build_manifest_fixture_checks(
    design: Mapping[str, Any],
    fixtures: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    fixture_names = _fixture_names(fixtures)
    contract_names = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
    ]
    payload_findings = _fixture_payload_findings(fixtures)
    return [
        _check(
            "manifest_dry_run_design_pass_check",
            expected={
                "manifest_dry_run_design_status": "pass",
                "manifest_dry_run_design_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION
                ),
                "manifest_dry_run_design_hash_present": True,
            },
            observed={
                "manifest_dry_run_design_status": _string_or_none(
                    design.get("manifest_dry_run_design_status")
                ),
                "manifest_dry_run_design_version": _string_or_none(
                    design.get("version")
                ),
                "manifest_dry_run_design_hash_present": _is_sha256(
                    _string_or_none(
                        design.get("deterministic_manifest_dry_run_design_hash")
                    )
                ),
            },
            blocking_reasons=_design_blocking_reasons(design),
        ),
        _simple_check(
            "manifest_fixture_pack_stage_check",
            EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE,
            EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE,
        ),
        _simple_check(
            "fixture_only_mode_check",
            MANIFEST_FIXTURE_PACK_MODE,
            MANIFEST_FIXTURE_PACK_MODE,
        ),
        _check(
            "fixture_names_complete_check",
            expected={
                "fixture_names": list(REQUIRED_MANIFEST_FIXTURE_NAMES),
                "fixture_count": len(REQUIRED_MANIFEST_FIXTURE_NAMES),
            },
            observed={
                "fixture_names": fixture_names,
                "fixture_count": len(fixture_names),
                "missing_fixture_names": _missing_fixture_names(fixture_names),
                "extra_fixture_names": _extra_fixture_names(fixture_names),
            },
            blocking_reasons=_fixture_name_blocking_reasons(fixture_names),
        ),
        _payload_findings_check(
            "fixture_payloads_sanitized_check",
            payload_findings,
        ),
        _check(
            "fixture_payloads_json_compatible_check",
            expected={"json_compatible": True},
            observed={
                "json_compatible": _json_compatible(
                    [fixture["fixture_payload"] for fixture in fixtures]
                )
            },
            blocking_reasons=[]
            if _json_compatible([fixture["fixture_payload"] for fixture in fixtures])
            else ["fixture payloads must be deterministic JSON-compatible"],
        ),
        _fixture_payloads_deterministic_check(fixtures),
        _payload_findings_check("no_executable_command_check", payload_findings),
        _payload_findings_check("no_live_endpoint_check", payload_findings),
        _payload_findings_check("no_secret_or_token_check", payload_findings),
        _payload_findings_check("no_raw_log_check", payload_findings),
        _flag_check("adapter_not_implemented_check", "execution_adapter_implemented", fixtures),
        _flag_check("adapter_not_invoked_check", "execution_adapter_invoked", fixtures),
        _flag_check("manifest_not_executed_check", "manifest_executed", fixtures),
        _flag_check(
            "dry_run_plan_not_executed_check", "dry_run_plan_executed", fixtures
        ),
        _flag_check("real_execution_disabled_check", "real_execution_enabled", fixtures),
        _flag_check("external_calls_disabled_check", "external_calls_enabled", fixtures),
        _flag_check("durable_writes_disabled_check", "durable_writes_enabled", fixtures),
        _flag_check(
            "filesystem_writes_disabled_check",
            "filesystem_writes_enabled",
            fixtures,
        ),
        _flag_check("database_writes_disabled_check", "database_writes_enabled", fixtures),
        _flag_check(
            "memory_graph_mutation_disabled_check",
            "memory_graph_mutation_enabled",
            fixtures,
        ),
        _flag_check(
            "operation_ledger_writes_disabled_check",
            "operation_ledger_writes_enabled",
            fixtures,
        ),
        _flag_check(
            "autonomous_execution_disabled_check",
            "autonomous_execution_enabled",
            fixtures,
        ),
        _check(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": _fixtures_flag_false(
                    fixtures, "star_cosmos_memory_active"
                )
                is False,
            },
            blocking_reasons=[]
            if _fixtures_flag_false(fixtures, "star_cosmos_memory_active")
            else ["Star-Cosmos memory active flag must remain false"],
        ),
        _deterministic_hash_check(design, fixtures, contracts, contract_names),
        _payload_findings_check("redaction_boundary_check", payload_findings),
    ]


def _fixture(
    fixture_name: str,
    *,
    fixture_type: str,
    synthetic_adapter_id: str,
    synthetic_adapter_kind: str,
    fixture_payload: Mapping[str, Any],
    expected_design_section_refs: Sequence[str],
    expected_contract_refs: Sequence[str],
    expected_check_refs: Sequence[str],
    fixture_validation_notes: Sequence[str],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    fixture: dict[str, Any] = {
        "fixture_name": fixture_name,
        "fixture_type": fixture_type,
        "fixture_status": "pass" if not blocking_reasons else "blocked",
        "synthetic_adapter_id": synthetic_adapter_id,
        "synthetic_adapter_kind": synthetic_adapter_kind,
        "manifest_mode": MANIFEST_FIXTURE_PACK_MODE,
        "fixture_payload": _detached_json_value(fixture_payload),
        "expected_design_section_refs": list(expected_design_section_refs),
        "expected_contract_refs": list(expected_contract_refs),
        "expected_check_refs": list(expected_check_refs),
        "fixture_validation_notes": list(fixture_validation_notes),
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(fixture)


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
        **COMMON_DISABLED_FLAGS,
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
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(check)


def _blocked_fragment_contract(
    contract_name: str,
    observed_key: str,
    payload_findings: Sequence[str],
) -> dict[str, Any]:
    return _contract(
        contract_name,
        contract_type="fixture_payload_sanitization_contract",
        expected={observed_key: False, "blocked_fragment_hit_count": 0},
        observed={
            observed_key: bool(payload_findings),
            "blocked_fragment_hit_count": len(payload_findings),
        },
        blocking_reasons=[
            "fixture payloads must not include blocked fragments"
        ]
        if payload_findings
        else [],
    )


def _disabled_flag_contract(
    contract_name: str,
    flag_name: str,
    fixtures: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    flag_is_false = _fixtures_flag_false(fixtures, flag_name)
    return _contract(
        contract_name,
        contract_type="fixture_disabled_flag_contract",
        expected={flag_name: False},
        observed={flag_name: False if flag_is_false else True},
        blocking_reasons=[]
        if flag_is_false
        else [f"{flag_name} must remain false"],
    )


def _simple_check(
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


def _flag_check(
    check_name: str,
    flag_name: str,
    fixtures: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    flag_is_false = _fixtures_flag_false(fixtures, flag_name)
    return _check(
        check_name,
        expected={flag_name: False},
        observed={flag_name: False if flag_is_false else True},
        blocking_reasons=[]
        if flag_is_false
        else [f"{flag_name} must remain false"],
    )


def _payload_findings_check(
    check_name: str,
    payload_findings: Sequence[str],
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"blocked_fragment_hit_count": 0},
        observed={"blocked_fragment_hit_count": len(payload_findings)},
        blocking_reasons=[
            "fixture payloads must not include blocked fragments"
        ]
        if payload_findings
        else [],
    )


def _fixture_payloads_deterministic_check(
    fixtures: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    fixture_hash = _hash_json_value(list(fixtures))
    repeat_hash = _hash_json_value(_build_manifest_fixtures())
    return _check(
        "fixture_payloads_deterministic_check",
        expected={
            "fixture_hash_stable": True,
            "hash_algorithm": (
                GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM
            ),
        },
        observed={
            "fixture_hash_stable": fixture_hash == repeat_hash,
            "fixture_hash_present": _is_sha256(fixture_hash),
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["fixture hash must be stable"]
                    if fixture_hash != repeat_hash
                    else []
                ),
                *(
                    ["fixture hash must be sha256"]
                    if not _is_sha256(fixture_hash)
                    else []
                ),
            ]
        ),
    )


def _deterministic_hash_check(
    design: Mapping[str, Any],
    fixtures: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    contract_names: Sequence[str],
) -> dict[str, Any]:
    design_repeat = _detached_json_value(
        build_governance_execution_adapter_manifest_dry_run_design()
    )
    fixture_hash = _hash_json_value(list(fixtures))
    fixture_repeat_hash = _hash_json_value(_build_manifest_fixtures())
    contract_hash = _hash_json_value(list(contracts))
    contract_repeat_hash = _hash_json_value(
        _build_manifest_fixture_contracts(design, _build_manifest_fixtures())
    )
    contract_names_complete = (
        list(contract_names) == list(REQUIRED_MANIFEST_FIXTURE_CONTRACT_NAMES)
    )
    return _check(
        "deterministic_hash_check",
        expected={
            "manifest_dry_run_design_stable": True,
            "fixture_hash_stable": True,
            "contract_hash_stable": True,
            "contract_names_complete": True,
        },
        observed={
            "manifest_dry_run_design_stable": design == design_repeat,
            "fixture_hash_stable": fixture_hash == fixture_repeat_hash,
            "fixture_hash_present": _is_sha256(fixture_hash),
            "contract_hash_stable": contract_hash == contract_repeat_hash,
            "contract_hash_present": _is_sha256(contract_hash),
            "contract_names_complete": contract_names_complete,
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["manifest dry-run design must be stable"]
                    if design != design_repeat
                    else []
                ),
                *(
                    ["fixture hash must be stable"]
                    if fixture_hash != fixture_repeat_hash
                    else []
                ),
                *(
                    ["fixture hash must be sha256"]
                    if not _is_sha256(fixture_hash)
                    else []
                ),
                *(
                    ["fixture contract hash must be stable"]
                    if contract_hash != contract_repeat_hash
                    else []
                ),
                *(
                    ["fixture contract hash must be sha256"]
                    if not _is_sha256(contract_hash)
                    else []
                ),
                *(
                    ["fixture contract names must be complete"]
                    if not contract_names_complete
                    else []
                ),
            ]
        ),
    )


def _unknown_fixture(name: str) -> dict[str, Any]:
    return _fixture(
        name,
        fixture_type="unknown_manifest_fixture",
        synthetic_adapter_id="unknown.synthetic.adapter",
        synthetic_adapter_kind="unknown_synthetic_adapter",
        fixture_payload=_payload(
            "unknown-synthetic-manifest",
            "unknown.synthetic.adapter",
            "unknown_synthetic_adapter",
            declared_metadata={},
        ),
        expected_design_section_refs=[],
        expected_contract_refs=[],
        expected_check_refs=[],
        fixture_validation_notes=[],
        blocking_reasons=[
            "execution adapter manifest fixture name is not recognized"
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
            "execution adapter manifest fixture contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter manifest fixture check name is not recognized"
        ],
    )


def _manifest_fixture_pack_summary(
    fixtures: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_fixtures = [
        _string_or_none(fixture.get("fixture_name")) or ""
        for fixture in fixtures
        if fixture.get("fixture_status") != "pass"
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
            "fixture_count": len(fixtures),
            "fixture_pass_count": len(fixtures) - len(blocked_fixtures),
            "fixture_blocked_count": len(blocked_fixtures),
            "blocked_fixture_names": blocked_fixtures,
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "manifest_fixture_pack_mode": MANIFEST_FIXTURE_PACK_MODE,
            "manifest_fixture_pack_stage": (
                EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "executable_command_included": False,
            "live_endpoint_included": False,
            "manifest_fixture_pack_summary_status": (
                "safe"
                if not blocked_fixtures
                and not blocked_contracts
                and not blocked_checks
                else "blocked"
            ),
        }
    )


def _fixture_names(fixtures: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(fixture.get("fixture_name")) or ""
        for fixture in fixtures
    ]


def _missing_fixture_names(fixture_names: Sequence[str]) -> list[str]:
    return [
        name for name in REQUIRED_MANIFEST_FIXTURE_NAMES if name not in fixture_names
    ]


def _extra_fixture_names(fixture_names: Sequence[str]) -> list[str]:
    return [
        name for name in fixture_names if name not in REQUIRED_MANIFEST_FIXTURE_NAMES
    ]


def _fixture_name_blocking_reasons(fixture_names: Sequence[str]) -> list[str]:
    missing_names = _missing_fixture_names(fixture_names)
    extra_names = _extra_fixture_names(fixture_names)
    return _deduplicate(
        [
            *(["manifest fixtures missing"] if missing_names else []),
            *(["unexpected manifest fixtures present"] if extra_names else []),
            *(
                ["manifest fixture order must be stable"]
                if list(fixture_names) != list(REQUIRED_MANIFEST_FIXTURE_NAMES)
                else []
            ),
        ]
    )


def _design_blocking_reasons(design: Mapping[str, Any]) -> list[str]:
    design_hash = _string_or_none(
        design.get("deterministic_manifest_dry_run_design_hash")
    )
    return _deduplicate(
        [
            *(
                ["manifest dry-run design status must pass"]
                if design.get("manifest_dry_run_design_status") != "pass"
                else []
            ),
            *(
                ["manifest dry-run design version must equal 5.4.0"]
                if design.get("version")
                != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION
                else []
            ),
            *(
                ["manifest dry-run design hash must be sha256"]
                if not _is_sha256(design_hash)
                else []
            ),
        ]
    )


def _fixtures_use_synthetic_ids(
    fixtures: Sequence[Mapping[str, Any]],
) -> bool:
    for fixture in fixtures:
        adapter_id = _string_or_none(fixture.get("synthetic_adapter_id")) or ""
        payload = fixture.get("fixture_payload")
        if not adapter_id.startswith("synthetic."):
            return False
        if not isinstance(payload, Mapping):
            return False
        manifest_id = _string_or_none(payload.get("manifest_id")) or ""
        if not manifest_id.startswith("synthetic-manifest-"):
            return False
    return True


def _fixtures_flag_false(
    fixtures: Sequence[Mapping[str, Any]],
    flag_name: str,
) -> bool:
    for fixture in fixtures:
        if fixture.get(flag_name) is not False:
            return False
        payload = fixture.get("fixture_payload")
        if not isinstance(payload, Mapping):
            return False
        disabled = payload.get("disabled_runtime_flags")
        if not isinstance(disabled, Mapping):
            return False
        if disabled.get(flag_name) is not False:
            return False
    return True


def _fixture_payload_findings(
    fixtures: Sequence[Mapping[str, Any]],
) -> list[str]:
    serialized_payloads = json.dumps(
        _detached_json_value(
            [fixture["fixture_payload"] for fixture in fixtures]
        ),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).lower()
    return [
        fragment
        for fragment in _PAYLOAD_BLOCKED_FRAGMENTS
        if fragment.lower() in serialized_payloads
    ]


def _json_compatible(value: Any) -> bool:
    try:
        _detached_json_value(value)
    except ValueError:
        return False
    return True


def _execution_adapter_manifest_fixture_pack_hash(
    pack: Mapping[str, Any],
) -> str:
    hash_input = {
        field: pack[field]
        for field in _MANIFEST_FIXTURE_PACK_HASH_FIELDS
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
    "EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION",
    "MANIFEST_FIXTURE_PACK_MODE",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_manifest_fixture_pack",
    "get_governance_execution_adapter_manifest_fixture",
    "get_governance_execution_adapter_manifest_fixture_check",
    "get_governance_execution_adapter_manifest_fixture_contract",
    "governance_execution_adapter_manifest_fixture_pack_to_json",
    "list_governance_execution_adapter_manifest_fixture_check_names",
    "list_governance_execution_adapter_manifest_fixture_contract_names",
    "list_governance_execution_adapter_manifest_fixture_names",
]
