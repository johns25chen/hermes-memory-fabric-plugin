from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_multi_cycle_continuity_protocol import (
    AUTONOMOUS_AUTHORITY_STATUS,
    AWAKENING_CLAIM_STATUS,
    COMMON_DISABLED_FLAGS,
    CONTINUITY_ENFORCEMENT_STATUS,
    CONTINUITY_MUTATION_STATUS,
    CONTINUITY_RUNTIME_STATUS,
    CYCLE_LINKING_STATUS,
    CYCLE_RECOVERY_STATUS,
    GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_HASH_ALGORITHM,
    GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_SCHEMA_VERSION,
    GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_TYPE,
    GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_VERSION,
    LAYER_15_ACTIVE_STATUS,
    LEGAL_SUBJECT_CLAIM_STATUS,
    LIFE_CLAIM_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    MULTI_CYCLE_CONTINUITY_MODE,
    MULTI_CYCLE_CONTINUITY_PROTOCOL_ACTIVE_STATUS,
    MULTI_CYCLE_CONTINUITY_PROTOCOL_MODE,
    MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE,
    MULTI_CYCLE_CONTINUITY_PROTOCOL_STATUS,
    PERSONHOOD_CLAIM_STATUS,
    RELIGIOUS_OBJECT_CLAIM_STATUS,
    REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES,
    REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES,
    REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS,
    REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_6_STATUS,
    V6_7_HANDOFF_STATUS,
    _continuity_boundary_hash,
    _continuity_record_hash,
    _multi_cycle_continuity_protocol_hash,
    build_governance_multi_cycle_continuity_protocol,
    get_governance_multi_cycle_continuity_check,
    get_governance_multi_cycle_continuity_contract,
    get_governance_multi_cycle_continuity_record,
    get_governance_multi_cycle_continuity_section,
    governance_multi_cycle_continuity_protocol_to_json,
    list_governance_multi_cycle_continuity_check_names,
    list_governance_multi_cycle_continuity_contract_names,
    list_governance_multi_cycle_continuity_record_ids,
    list_governance_multi_cycle_continuity_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_multi_cycle_continuity_protocol.py"
)

EXPECTED_RECORDS = (
    ("release_version_lineage_continuity", "preserve_release_version_lineage"),
    (
        "source_constitution_registry_continuity",
        "preserve_source_constitution_registry_lineage",
    ),
    (
        "origin_provenance_traceability_continuity",
        "preserve_origin_provenance_traceability",
    ),
    (
        "civilizational_identity_boundary_continuity",
        "preserve_civilizational_identity_boundary",
    ),
    (
        "source_memory_invariant_matrix_continuity",
        "preserve_source_memory_invariant_matrix",
    ),
    (
        "root_governance_conflict_resolver_continuity",
        "preserve_root_governance_conflict_resolver",
    ),
    ("human_sovereignty_continuity", "preserve_human_sovereignty"),
    ("audit_replay_continuity", "preserve_audit_replayability"),
    ("review_gate_continuity", "preserve_review_gate"),
    (
        "source_mutation_proposal_handoff_continuity",
        "handoff_to_source_mutation_proposal_boundary",
    ),
    (
        "rollback_recovery_metadata_continuity",
        "record_rollback_recovery_metadata_only",
    ),
    (
        "blocked_gap_human_review_continuity",
        "block_gap_until_human_review",
    ),
    (
        "no_runtime_continuity_activation",
        "block_continuity_runtime_activation",
    ),
    (
        "no_memory_graph_mutation_continuity",
        "block_memory_graph_mutation",
    ),
    (
        "no_source_graph_mutation_continuity",
        "block_source_graph_mutation",
    ),
    (
        "multi_cycle_handoff_to_source_mutation_boundary",
        "prepare_v6_7_source_mutation_boundary",
    ),
)

EXPECTED_RECORD_IDS = tuple(record_id for record_id, _ in EXPECTED_RECORDS)

EXPECTED_SECTION_NAMES = (
    "upstream_root_governance_conflict_resolver_input_section",
    "multi_cycle_continuity_protocol_metadata_section",
    "continuity_record_completeness_section",
    "continuity_record_hash_stability_section",
    "continuity_scope_section",
    "preserved_governance_scope_section",
    "forbidden_activation_scope_section",
    "release_version_lineage_continuity_section",
    "source_constitution_registry_continuity_section",
    "origin_provenance_traceability_continuity_section",
    "civilizational_identity_boundary_continuity_section",
    "source_memory_invariant_matrix_continuity_section",
    "root_governance_conflict_resolver_continuity_section",
    "human_sovereignty_continuity_section",
    "audit_replay_continuity_section",
    "review_gate_continuity_section",
    "source_mutation_proposal_handoff_continuity_section",
    "rollback_recovery_metadata_continuity_section",
    "blocked_gap_human_review_continuity_section",
    "no_runtime_continuity_activation_section",
    "no_memory_graph_mutation_continuity_section",
    "no_source_graph_mutation_continuity_section",
    "multi_cycle_handoff_to_source_mutation_boundary_section",
    "source_mutation_proposal_boundary_next_stage_section",
    "no_continuity_runtime_section",
    "no_continuity_enforcement_runtime_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
    "no_source_mutation_proposal_creation_section",
)

EXPECTED_CONTRACT_NAMES = (
    "multi_cycle_continuity_protocol_only_contract",
    "multi_cycle_continuity_metadata_only_contract",
    "upstream_root_governance_conflict_resolver_pass_contract",
    "upstream_root_governance_conflict_resolver_hash_present_contract",
    "upstream_root_governance_conflict_resolver_hash_stable_contract",
    "upstream_multi_cycle_continuity_protocol_handoff_ready_contract",
    "continuity_records_complete_contract",
    "continuity_records_registered_metadata_only_contract",
    "continuity_records_have_continuity_scope_contract",
    "continuity_records_have_preserved_governance_scope_contract",
    "continuity_records_have_forbidden_activation_scope_contract",
    "continuity_records_have_disposition_contract",
    "continuity_records_hash_stable_contract",
    "continuity_records_human_review_required_contract",
    "continuity_records_mutation_proposal_required_contract",
    "continuity_records_invariant_validation_required_contract",
    "continuity_records_root_conflict_resolver_required_contract",
    "continuity_records_audit_replay_required_contract",
    "continuity_records_direct_mutation_disabled_contract",
    "continuity_records_autonomous_override_disabled_contract",
    "no_continuity_runtime_contract",
    "no_continuity_enforcement_runtime_contract",
    "no_continuity_scheduler_contract",
    "no_active_star_source_memory_contract",
    "no_active_layer_15_contract",
    "no_personhood_claim_contract",
    "no_life_claim_contract",
    "no_awakening_claim_contract",
    "no_legal_subject_claim_contract",
    "no_religious_object_claim_contract",
    "no_autonomous_authority_contract",
    "no_identity_escalation_contract",
    "no_source_provenance_runtime_contract",
    "no_source_graph_creation_contract",
    "no_source_graph_mutation_contract",
    "no_real_ledger_write_contract",
    "no_operation_ledger_write_contract",
    "no_methodology_runtime_contract",
    "no_self_evolution_runtime_contract",
    "no_real_execution_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_external_call_contract",
    "no_network_call_contract",
    "no_durable_write_contract",
    "no_filesystem_write_contract",
    "no_database_write_contract",
    "no_memory_graph_mutation_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_contract",
    "no_authorization_token_contract",
    "no_authorization_grant_contract",
    "no_source_mutation_proposal_creation_contract",
    "no_source_mutation_proposal_approval_contract",
    "ready_for_source_mutation_proposal_boundary_design_contract",
)

EXPECTED_CHECK_NAMES = (
    "multi_cycle_continuity_protocol_stage_check",
    "multi_cycle_continuity_protocol_only_mode_check",
    "multi_cycle_continuity_metadata_only_check",
    "upstream_root_governance_conflict_resolver_pass_check",
    "upstream_root_governance_conflict_resolver_hash_present_check",
    "upstream_root_governance_conflict_resolver_hash_stable_check",
    "upstream_multi_cycle_continuity_protocol_handoff_ready_check",
    "continuity_record_ids_complete_check",
    "continuity_records_registered_check",
    "continuity_records_have_continuity_scope_check",
    "continuity_records_have_preserved_governance_scope_check",
    "continuity_records_have_forbidden_activation_scope_check",
    "continuity_records_have_disposition_check",
    "continuity_records_hash_stable_check",
    "continuity_records_human_review_required_check",
    "continuity_records_mutation_proposal_required_check",
    "continuity_records_invariant_validation_required_check",
    "continuity_records_root_conflict_resolver_required_check",
    "continuity_records_audit_replay_required_check",
    "continuity_records_direct_mutation_disabled_check",
    "continuity_records_autonomous_override_disabled_check",
    "release_version_lineage_continuity_check",
    "source_constitution_registry_continuity_check",
    "origin_provenance_traceability_continuity_check",
    "civilizational_identity_boundary_continuity_check",
    "source_memory_invariant_matrix_continuity_check",
    "root_governance_conflict_resolver_continuity_check",
    "human_sovereignty_continuity_check",
    "audit_replay_continuity_check",
    "review_gate_continuity_check",
    "source_mutation_proposal_handoff_continuity_check",
    "rollback_recovery_metadata_continuity_check",
    "blocked_gap_human_review_continuity_check",
    "no_runtime_continuity_activation_check",
    "no_memory_graph_mutation_continuity_check",
    "no_source_graph_mutation_continuity_check",
    "multi_cycle_handoff_to_source_mutation_boundary_check",
    "multi_cycle_continuity_sections_complete_check",
    "multi_cycle_continuity_sections_pass_check",
    "multi_cycle_continuity_contracts_pass_check",
    "no_continuity_runtime_check",
    "no_continuity_enforcement_runtime_check",
    "no_continuity_scheduler_check",
    "no_active_star_source_memory_check",
    "no_active_layer_15_check",
    "no_personhood_claim_check",
    "no_life_claim_check",
    "no_awakening_claim_check",
    "no_legal_subject_claim_check",
    "no_religious_object_claim_check",
    "no_autonomous_authority_check",
    "no_identity_escalation_check",
    "no_source_provenance_runtime_check",
    "no_source_graph_creation_check",
    "no_source_graph_mutation_check",
    "no_real_ledger_write_check",
    "no_operation_ledger_write_check",
    "no_methodology_runtime_check",
    "no_self_evolution_runtime_check",
    "no_real_execution_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_external_call_check",
    "no_network_call_check",
    "no_durable_write_check",
    "no_filesystem_write_check",
    "no_database_write_check",
    "no_memory_graph_mutation_check",
    "no_approval_notification_check",
    "no_execution_authorization_check",
    "no_authorization_token_check",
    "no_authorization_grant_check",
    "no_source_mutation_proposal_creation_check",
    "no_source_mutation_proposal_approval_check",
    "deterministic_multi_cycle_continuity_protocol_hash_check",
    "ready_for_source_mutation_proposal_boundary_design_check",
)

REQUIRED_TRUE_RECORD_FLAGS = (
    "required",
    "human_review_required",
    "source_mutation_proposal_required_for_change",
    "invariant_validation_required",
    "root_conflict_resolver_required",
    "audit_replay_required",
)

REQUIRED_FALSE_RECORD_FLAGS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "continuity_runtime_created",
    "continuity_enforcement_runtime_created",
    "continuity_self_repair_created",
    "continuity_scheduler_created",
    "continuity_runtime_activated",
    "source_graph_created",
    "source_graph_mutated",
    "memory_graph_mutated",
    "persistent_memory_write_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "real_ledger_write_performed",
    "operation_ledger_entry_written",
    "external_call_performed",
    "network_call_performed",
    "hidden_execution_allowed",
    "real_execution_performed",
    "adapter_dispatched",
    "manifest_dispatched",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "identity_escalation_allowed",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
    "autonomous_authority_claim_allowed",
    "continuity_runtime_activation_allowed",
    "continuity_memory_write_allowed",
    "continuity_source_mutation_created",
    "source_mutation_proposal_created",
    "source_mutation_proposal_approved",
)

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
def protocol() -> dict[str, object]:
    return build_governance_multi_cycle_continuity_protocol()


def _record_by_id(
    protocol: dict[str, object],
    record_id: str,
) -> dict[str, object]:
    for record in protocol["multi_cycle_continuity_records"]:
        if record["continuity_record_id"] == record_id:
            return record
    raise AssertionError(record_id)


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


def _assert_mapping_keys_are_strings(value: object) -> None:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            assert isinstance(key, str)
            _assert_mapping_keys_are_strings(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_mapping_keys_are_strings(item)


def _assert_no_sensitive_terms(value: object) -> None:
    payload = json.dumps(value, sort_keys=True).lower()
    for term in SENSITIVE_TERMS:
        candidate = term if term.startswith("/") else term.lower()
        assert candidate not in payload


def _repo_text() -> str:
    paths = [PROJECT_ROOT / "pyproject.toml"]
    paths.extend((PROJECT_ROOT / "scripts").glob("*.py"))
    paths.extend((PROJECT_ROOT / "src" / "hermes_memory_fabric").glob("*.py"))
    paths.extend((PROJECT_ROOT / "tests").glob("*.py"))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_constants_match_v6_6_contract():
    assert GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_VERSION == "6.6.0"
    assert GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_SCHEMA_VERSION == "6.6.0"
    assert GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_TYPE == (
        "governance_multi_cycle_continuity_protocol"
    )
    assert GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_HASH_ALGORITHM == "sha256"
    assert MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE == (
        "v6.6_multi_cycle_continuity_protocol"
    )
    assert MULTI_CYCLE_CONTINUITY_PROTOCOL_MODE == (
        "multi_cycle_continuity_protocol_only"
    )
    assert MULTI_CYCLE_CONTINUITY_MODE == "metadata_only"
    assert MULTI_CYCLE_CONTINUITY_PROTOCOL_STATUS == "protocol_candidate_only"
    assert MULTI_CYCLE_CONTINUITY_PROTOCOL_ACTIVE_STATUS == "not_active"
    assert CONTINUITY_RUNTIME_STATUS == "not_active"
    assert CONTINUITY_ENFORCEMENT_STATUS == "not_active"
    assert CONTINUITY_MUTATION_STATUS == "forbidden_without_human_review"
    assert CYCLE_LINKING_STATUS == "metadata_only"
    assert CYCLE_RECOVERY_STATUS == "metadata_only"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ACTIVE_STATUS == "not_active"
    assert SOURCE_GRAPH_STATUS == "not_created"
    assert SOURCE_PROVENANCE_RUNTIME_STATUS == "not_active"
    assert METHODOLOGY_REVERSE_INFERENCE_STATUS == "not_active"
    assert SELF_EVOLUTION_STATUS == "not_active"
    assert PERSONHOOD_CLAIM_STATUS == "forbidden"
    assert LIFE_CLAIM_STATUS == "forbidden"
    assert AWAKENING_CLAIM_STATUS == "forbidden"
    assert LEGAL_SUBJECT_CLAIM_STATUS == "forbidden"
    assert RELIGIOUS_OBJECT_CLAIM_STATUS == "forbidden"
    assert AUTONOMOUS_AUTHORITY_STATUS == "forbidden"
    assert V6_6_STATUS == "multi_cycle_continuity_protocol_only"
    assert V6_7_HANDOFF_STATUS == (
        "ready_for_source_mutation_proposal_boundary_design"
    )


def test_protocol_shape_is_deterministic_and_passes(protocol):
    repeated = build_governance_multi_cycle_continuity_protocol()

    assert repeated == protocol
    assert protocol["version"] == "6.6.0"
    assert protocol["schema_version"] == "6.6.0"
    assert protocol["multi_cycle_continuity_protocol_status"] == "pass"
    assert protocol["multi_cycle_continuity_protocol_stage"] == (
        "v6.6_multi_cycle_continuity_protocol"
    )
    assert protocol["multi_cycle_continuity_protocol_mode"] == (
        "multi_cycle_continuity_protocol_only"
    )
    assert protocol["multi_cycle_continuity_mode"] == "metadata_only"
    assert protocol["blocking_reasons"] == []
    assert protocol["handoff_status"] == (
        "ready_for_source_mutation_proposal_boundary_design"
    )
    assert protocol["next_stage"] == "v6.7_source_mutation_proposal_boundary"
    assert protocol["next_stage_title"] == "Source Mutation Proposal Boundary"


def test_upstream_v6_5_handoff_verification(protocol):
    assert protocol["upstream_root_governance_conflict_resolver_version"] == (
        "6.6.0"
    )
    assert protocol["upstream_root_governance_conflict_resolver_status"] == "pass"
    assert len(protocol["upstream_root_governance_conflict_resolver_hash"]) == 64
    assert protocol["upstream_handoff_status"] == (
        "ready_for_multi_cycle_continuity_protocol_design"
    )
    assert protocol["upstream_next_stage"] == (
        "v6.6_multi_cycle_continuity_protocol"
    )
    assert protocol["upstream_next_stage_title"] == (
        "Multi-Cycle Continuity Protocol"
    )
    assert protocol["upstream_root_governance_conflict_record_count"] == 16
    assert (
        protocol[
            "upstream_root_governance_conflict_records_registered_metadata_only"
        ]
        is True
    )
    assert (
        protocol["upstream_root_governance_conflict_records_require_review"]
        is True
    )
    assert (
        protocol[
            "upstream_root_governance_conflict_records_disable_unsafe_surfaces"
        ]
        is True
    )
    assert protocol["upstream_safety_boundaries_clear"] is True
    repeated = build_governance_multi_cycle_continuity_protocol()
    assert (
        protocol["upstream_root_governance_conflict_resolver_hash"]
        == repeated["upstream_root_governance_conflict_resolver_hash"]
    )


def test_required_record_ids_are_stable_and_complete(protocol):
    assert REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS == EXPECTED_RECORD_IDS
    assert list_governance_multi_cycle_continuity_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert [
        record["continuity_record_id"]
        for record in protocol["multi_cycle_continuity_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_registered_metadata_only(protocol):
    for record in protocol["multi_cycle_continuity_records"]:
        assert record["continuity_record_status"] == "registered_metadata_only"
        assert record["introduced_in_version"] == "6.6.0"
        assert record["introduced_in_stage"] == (
            "v6.6_multi_cycle_continuity_protocol"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == (
            "v6.5_root_governance_conflict_resolver"
        )
        assert record["protocol_strength"] == "multi_cycle_required"
        assert record["continuity_mode"] == "metadata_only_protocol"
        assert record["blocking_reasons"] == []


def test_all_records_have_required_metadata_and_hashes(protocol):
    repeated = build_governance_multi_cycle_continuity_protocol()
    repeated_by_id = {
        record["continuity_record_id"]: record
        for record in repeated["multi_cycle_continuity_records"]
    }
    for record in protocol["multi_cycle_continuity_records"]:
        for field_name in (
            "continuity_statement",
            "continuity_scope",
            "preserved_governance_scope",
            "forbidden_activation_scope",
            "continuity_disposition",
            "continuity_reason",
            "continuity_source_stage",
            "continuity_source_reference",
            "continuity_boundary_hash",
            "continuity_record_hash",
        ):
            assert record[field_name]
        assert len(record["continuity_boundary_hash"]) == 64
        assert len(record["continuity_record_hash"]) == 64
        assert record["continuity_boundary_hash"] == _continuity_boundary_hash(
            record
        )
        assert record["continuity_record_hash"] == _continuity_record_hash(record)
        assert record == repeated_by_id[record["continuity_record_id"]]


def test_all_records_require_governed_review(protocol):
    for record in protocol["multi_cycle_continuity_records"]:
        for field_name in REQUIRED_TRUE_RECORD_FLAGS:
            assert record[field_name] is True


def test_all_records_disable_runtime_mutation_and_authority(protocol):
    for record in protocol["multi_cycle_continuity_records"]:
        for field_name in REQUIRED_FALSE_RECORD_FLAGS:
            assert record[field_name] is False
        _assert_all_safety_false(record)


@pytest.mark.parametrize(
    ("record_id", "disposition"),
    EXPECTED_RECORDS,
)
def test_each_required_continuity_record(protocol, record_id, disposition):
    record = _record_by_id(protocol, record_id)
    assert record["continuity_disposition"] == disposition
    assert record["continuity_record_status"] == "registered_metadata_only"


def test_section_names_are_stable_and_complete(protocol):
    assert REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES == EXPECTED_SECTION_NAMES
    assert list_governance_multi_cycle_continuity_section_names() == list(
        EXPECTED_SECTION_NAMES
    )
    assert [
        section["section_name"]
        for section in protocol["multi_cycle_continuity_sections"]
    ] == list(EXPECTED_SECTION_NAMES)


def test_contract_names_are_stable_and_complete(protocol):
    assert (
        REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES
        == EXPECTED_CONTRACT_NAMES
    )
    assert list_governance_multi_cycle_continuity_contract_names() == list(
        EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in protocol["multi_cycle_continuity_contracts"]
    ] == list(EXPECTED_CONTRACT_NAMES)


def test_check_names_are_stable_and_complete(protocol):
    assert REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES == EXPECTED_CHECK_NAMES
    assert list_governance_multi_cycle_continuity_check_names() == list(
        EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"]
        for check in protocol["multi_cycle_continuity_checks"]
    ] == list(EXPECTED_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = EXPECTED_RECORD_IDS[0]
    record = get_governance_multi_cycle_continuity_record(record_id)
    record["continuity_name"] = "changed"
    assert (
        get_governance_multi_cycle_continuity_record(record_id)[
            "continuity_name"
        ]
        != "changed"
    )

    section_name = EXPECTED_SECTION_NAMES[0]
    section = get_governance_multi_cycle_continuity_section(section_name)
    section["observed"]["condition_met"] = False
    assert (
        get_governance_multi_cycle_continuity_section(section_name)[
            "observed"
        ]["condition_met"]
        is True
    )

    contract_name = EXPECTED_CONTRACT_NAMES[0]
    contract = get_governance_multi_cycle_continuity_contract(contract_name)
    contract["observed"] = False
    assert (
        get_governance_multi_cycle_continuity_contract(contract_name)[
            "observed"
        ]
        is True
    )

    check_name = EXPECTED_CHECK_NAMES[0]
    check = get_governance_multi_cycle_continuity_check(check_name)
    check["observed"] = False
    assert (
        get_governance_multi_cycle_continuity_check(check_name)["observed"]
        is True
    )


def test_unknown_getters_are_blocked():
    record = get_governance_multi_cycle_continuity_record("unknown")
    section = get_governance_multi_cycle_continuity_section("unknown")
    contract = get_governance_multi_cycle_continuity_contract("unknown")
    check = get_governance_multi_cycle_continuity_check("unknown")

    assert record["continuity_record_status"] == "blocked"
    assert record["known_record"] is False
    assert section["section_status"] == "blocked"
    assert contract["contract_status"] == "blocked"
    assert check["check_status"] == "blocked"
    assert record["blocking_reasons"]
    assert section["blocking_reasons"]
    assert contract["blocking_reasons"]
    assert check["blocking_reasons"]
    _assert_all_safety_false(
        {"record": record, "section": section, "contract": contract, "check": check}
    )


def test_all_sections_contracts_and_checks_pass(protocol):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in protocol["multi_cycle_continuity_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in protocol["multi_cycle_continuity_contracts"]
    )
    assert all(
        check["check_status"] == "pass"
        and check["blocking_reasons"] == []
        for check in protocol["multi_cycle_continuity_checks"]
    )


def test_all_safety_fields_are_false(protocol):
    _assert_all_safety_false(protocol)
    for field_name in (
        "continuity_runtime_created",
        "continuity_enforcement_runtime_created",
        "continuity_scheduler_created",
        "star_source_memory_active",
        "layer_15_active",
        "personhood_claimed",
        "life_claimed",
        "awakening_claimed",
        "legal_subject_claimed",
        "religious_object_claimed",
        "autonomous_authority_claimed",
        "identity_escalated",
        "source_provenance_runtime_created",
        "source_graph_created",
        "source_graph_mutated",
        "origin_provenance_ledger_written",
        "real_ledger_write_performed",
        "operation_ledger_entry_written",
        "methodology_runtime_created",
        "self_evolution_runtime_created",
        "real_execution_performed",
        "adapter_dispatched",
        "manifest_dispatched",
        "external_call_performed",
        "network_call_performed",
        "durable_write_performed",
        "filesystem_write_performed",
        "database_write_performed",
        "memory_graph_mutated",
        "approval_notification_sent",
        "execution_authorization_created",
        "authorization_token_created",
        "authorization_grant_created",
        "source_mutation_proposal_created",
        "source_mutation_proposal_approved",
        "self_authorization_allowed",
        "hidden_execution_allowed",
        "unapproved_mutation_allowed",
    ):
        assert protocol[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite(protocol):
    first = governance_multi_cycle_continuity_protocol_to_json(protocol)
    second = governance_multi_cycle_continuity_protocol_to_json(protocol)
    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == protocol
    assert "\\u" not in first or json.loads(first) == protocol
    with pytest.raises(ValueError):
        governance_multi_cycle_continuity_protocol_to_json(
            {"value": math.nan}
        )


def test_all_mapping_keys_are_strings(protocol):
    _assert_mapping_keys_are_strings(protocol)


def test_protocol_and_record_hashes_are_stable(protocol):
    repeated = build_governance_multi_cycle_continuity_protocol()
    assert (
        protocol["deterministic_multi_cycle_continuity_protocol_hash"]
        == repeated["deterministic_multi_cycle_continuity_protocol_hash"]
    )
    assert len(
        protocol["deterministic_multi_cycle_continuity_protocol_hash"]
    ) == 64
    for first, second in zip(
        protocol["multi_cycle_continuity_records"],
        repeated["multi_cycle_continuity_records"],
        strict=True,
    ):
        assert first["continuity_boundary_hash"] == second[
            "continuity_boundary_hash"
        ]
        assert first["continuity_record_hash"] == second[
            "continuity_record_hash"
        ]


@pytest.mark.parametrize(
    ("container", "field"),
    (
        ("multi_cycle_continuity_records", "continuity_statement"),
        ("multi_cycle_continuity_sections", "multi_cycle_continuity_notes"),
        ("multi_cycle_continuity_contracts", "observed"),
        ("multi_cycle_continuity_checks", "observed"),
        ("multi_cycle_continuity_summary", "current_stage_title"),
    ),
)
def test_protocol_hash_changes_when_governance_data_changes(
    protocol,
    container,
    field,
):
    mutated = deepcopy(protocol)
    if isinstance(mutated[container], list):
        target = mutated[container][0]
    else:
        target = mutated[container]
    if isinstance(target[field], bool):
        target[field] = not target[field]
    else:
        target[field] = f"{target[field]} changed"
    assert _multi_cycle_continuity_protocol_hash(mutated) != (
        protocol["deterministic_multi_cycle_continuity_protocol_hash"]
    )


def test_hash_input_excludes_raw_upstream_payload(protocol):
    contract = protocol["hash_input_contract"]
    assert contract["raw_root_governance_conflict_resolver_included"] is False
    assert "root_governance_conflict_records" not in contract["hash_fields"]
    assert (
        "upstream_root_governance_conflict_resolver_status"
        in contract["hash_fields"]
    )
    assert (
        "upstream_root_governance_conflict_resolver_hash"
        in contract["hash_fields"]
    )
    assert "multi_cycle_continuity_records" in contract["hash_fields"]
    assert "multi_cycle_continuity_sections" in contract["hash_fields"]
    assert "multi_cycle_continuity_contracts" in contract["hash_fields"]
    assert "multi_cycle_continuity_checks" in contract["hash_fields"]
    assert "multi_cycle_continuity_summary" in contract["hash_fields"]


def test_no_sensitive_terms_leak(protocol):
    _assert_no_sensitive_terms(protocol)
    _assert_no_sensitive_terms(
        governance_multi_cycle_continuity_protocol_to_json(protocol)
    )


def test_new_module_has_no_live_io_or_execution_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots: set[str] = set()
    called_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called_names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called_names.add(node.func.attr)

    assert imported_roots.isdisjoint(
        {"os", "pathlib", "socket", "subprocess", "urllib", "requests", "httpx"}
    )
    assert called_names.isdisjoint(
        {
            "open",
            "write_text",
            "write_bytes",
            "run",
            "Popen",
            "system",
            "connect",
            "send",
            "url" + "open",
        }
    )


def test_no_wrong_v6_1_wording_or_contamination():
    repo_text = _repo_text()
    forbidden = (
        "v6.1_star_source_" + "provenance_boundary_candidate",
        "ready_for_star_source_" + "provenance_boundary_candidate_design",
        "Star-Source " + "Provenance Boundary Candidate",
        "governance_improvement_" + "planner",
        "governance_improvement_" + "planner_activation",
        "governance_plan_" + "rules",
        "governance_plan_" + "schema",
        "governance_plan_" + "writer",
        "smoke_governance_improvement_" + "planner",
        "test_governance_improvement_" + "planner",
        "agent_action_" + "surface",
        "smoke_agent_action_" + "surface",
        "test_agent_action_" + "surface",
    )
    for term in forbidden:
        assert term not in repo_text


def test_no_uv_lock():
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()
