from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_source_mutation_proposal_boundary import (
    AUTONOMOUS_AUTHORITY_STATUS,
    AWAKENING_CLAIM_STATUS,
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_TYPE,
    GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_VERSION,
    LAYER_15_ACTIVE_STATUS,
    LEGAL_SUBJECT_CLAIM_STATUS,
    LIFE_CLAIM_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    PERSONHOOD_CLAIM_STATUS,
    RELIGIOUS_OBJECT_CLAIM_STATUS,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CHECK_NAMES,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_MUTATION_EXECUTION_STATUS,
    SOURCE_MUTATION_PROPOSAL_APPROVAL_STATUS,
    SOURCE_MUTATION_PROPOSAL_BOUNDARY_ACTIVE_STATUS,
    SOURCE_MUTATION_PROPOSAL_BOUNDARY_MODE,
    SOURCE_MUTATION_PROPOSAL_BOUNDARY_STAGE,
    SOURCE_MUTATION_PROPOSAL_BOUNDARY_STATUS,
    SOURCE_MUTATION_PROPOSAL_CREATION_STATUS,
    SOURCE_MUTATION_PROPOSAL_MODE,
    SOURCE_MUTATION_REVIEW_GATE_STATUS,
    SOURCE_MUTATION_REVIEW_STATUS,
    SOURCE_MUTATION_RUNTIME_STATUS,
    SOURCE_MUTATION_STATUS,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_7_STATUS,
    V6_8_HANDOFF_STATUS,
    _proposal_boundary_hash,
    _proposal_boundary_record_hash,
    _source_mutation_proposal_boundary_hash,
    build_governance_source_mutation_proposal_boundary,
    get_governance_source_mutation_proposal_boundary_check,
    get_governance_source_mutation_proposal_boundary_contract,
    get_governance_source_mutation_proposal_boundary_record,
    get_governance_source_mutation_proposal_boundary_section,
    governance_source_mutation_proposal_boundary_to_json,
    list_governance_source_mutation_proposal_boundary_check_names,
    list_governance_source_mutation_proposal_boundary_contract_names,
    list_governance_source_mutation_proposal_boundary_record_ids,
    list_governance_source_mutation_proposal_boundary_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_source_mutation_proposal_boundary.py"
)

EXPECTED_RECORDS = (
    (
        "source_mutation_intake_metadata_boundary",
        "record_source_mutation_intake_metadata_only",
    ),
    ("human_sovereignty_proposal_gate", "require_human_sovereignty_gate"),
    (
        "source_constitution_alignment_requirement",
        "require_source_constitution_alignment",
    ),
    (
        "origin_provenance_preservation_requirement",
        "preserve_origin_provenance",
    ),
    (
        "civilizational_identity_non_escalation_requirement",
        "preserve_civilizational_identity_boundary",
    ),
    (
        "source_memory_invariant_validation_requirement",
        "require_source_memory_invariant_validation",
    ),
    (
        "root_governance_conflict_resolution_requirement",
        "require_root_governance_conflict_resolution",
    ),
    ("multi_cycle_continuity_requirement", "require_multi_cycle_continuity"),
    ("audit_replay_requirement", "require_audit_replay"),
    (
        "proposal_scope_definition_boundary",
        "define_proposal_scope_metadata_only",
    ),
    (
        "proposal_risk_classification_boundary",
        "classify_proposal_risk_metadata_only",
    ),
    (
        "proposal_review_readiness_boundary",
        "prepare_review_readiness_metadata_only",
    ),
    ("no_auto_proposal_creation_boundary", "block_auto_proposal_creation"),
    ("no_auto_proposal_approval_boundary", "block_auto_proposal_approval"),
    (
        "no_source_or_memory_graph_mutation_boundary",
        "block_source_and_memory_graph_mutation",
    ),
    (
        "source_mutation_review_gate_handoff_boundary",
        "handoff_to_source_mutation_review_gate",
    ),
)

EXPECTED_RECORD_IDS = tuple(record_id for record_id, _ in EXPECTED_RECORDS)

EXPECTED_SECTION_NAMES = (
    "upstream_multi_cycle_continuity_protocol_input_section",
    "source_mutation_proposal_boundary_metadata_section",
    "proposal_boundary_record_completeness_section",
    "proposal_boundary_record_hash_stability_section",
    "proposal_boundary_scope_section",
    "required_proposal_metadata_scope_section",
    "forbidden_proposal_activation_scope_section",
    "source_mutation_intake_metadata_boundary_section",
    "human_sovereignty_proposal_gate_section",
    "source_constitution_alignment_requirement_section",
    "origin_provenance_preservation_requirement_section",
    "civilizational_identity_non_escalation_requirement_section",
    "source_memory_invariant_validation_requirement_section",
    "root_governance_conflict_resolution_requirement_section",
    "multi_cycle_continuity_requirement_section",
    "audit_replay_requirement_section",
    "proposal_scope_definition_boundary_section",
    "proposal_risk_classification_boundary_section",
    "proposal_review_readiness_boundary_section",
    "no_auto_proposal_creation_boundary_section",
    "no_auto_proposal_approval_boundary_section",
    "no_source_or_memory_graph_mutation_boundary_section",
    "source_mutation_review_gate_handoff_boundary_section",
    "source_mutation_review_gate_next_stage_section",
    "no_source_mutation_runtime_section",
    "no_source_mutation_execution_section",
    "no_source_mutation_proposal_creation_section",
    "no_source_mutation_proposal_approval_section",
    "no_source_mutation_review_gate_activation_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

EXPECTED_CONTRACT_NAMES = (
    "source_mutation_proposal_boundary_only_contract",
    "source_mutation_proposal_metadata_only_contract",
    "upstream_multi_cycle_continuity_protocol_pass_contract",
    "upstream_multi_cycle_continuity_protocol_hash_present_contract",
    "upstream_multi_cycle_continuity_protocol_hash_stable_contract",
    "upstream_source_mutation_proposal_boundary_handoff_ready_contract",
    "proposal_boundary_records_complete_contract",
    "proposal_boundary_records_registered_metadata_only_contract",
    "proposal_boundary_records_have_boundary_scope_contract",
    "proposal_boundary_records_have_required_metadata_scope_contract",
    "proposal_boundary_records_have_forbidden_activation_scope_contract",
    "proposal_boundary_records_have_disposition_contract",
    "proposal_boundary_records_hash_stable_contract",
    "proposal_boundary_records_human_review_required_contract",
    "proposal_boundary_records_review_gate_required_contract",
    "proposal_boundary_records_constitution_alignment_required_contract",
    "proposal_boundary_records_origin_provenance_required_contract",
    "proposal_boundary_records_identity_boundary_required_contract",
    "proposal_boundary_records_invariant_validation_required_contract",
    "proposal_boundary_records_root_conflict_resolver_required_contract",
    "proposal_boundary_records_multi_cycle_continuity_required_contract",
    "proposal_boundary_records_audit_replay_required_contract",
    "proposal_boundary_records_direct_mutation_disabled_contract",
    "proposal_boundary_records_autonomous_override_disabled_contract",
    "no_source_mutation_runtime_contract",
    "no_source_mutation_execution_contract",
    "no_source_mutation_performed_contract",
    "no_source_mutation_proposal_creation_contract",
    "no_source_mutation_proposal_approval_contract",
    "no_source_mutation_review_contract",
    "no_source_mutation_review_gate_activation_contract",
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
    "no_proposal_auto_creation_contract",
    "no_proposal_auto_approval_contract",
    "ready_for_source_mutation_review_gate_design_contract",
)

EXPECTED_CHECK_NAMES = (
    "source_mutation_proposal_boundary_stage_check",
    "source_mutation_proposal_boundary_only_mode_check",
    "source_mutation_proposal_metadata_only_check",
    "upstream_multi_cycle_continuity_protocol_pass_check",
    "upstream_multi_cycle_continuity_protocol_hash_present_check",
    "upstream_multi_cycle_continuity_protocol_hash_stable_check",
    "upstream_source_mutation_proposal_boundary_handoff_ready_check",
    "proposal_boundary_record_ids_complete_check",
    "proposal_boundary_records_registered_check",
    "proposal_boundary_records_have_boundary_scope_check",
    "proposal_boundary_records_have_required_metadata_scope_check",
    "proposal_boundary_records_have_forbidden_activation_scope_check",
    "proposal_boundary_records_have_disposition_check",
    "proposal_boundary_records_hash_stable_check",
    "proposal_boundary_records_human_review_required_check",
    "proposal_boundary_records_review_gate_required_check",
    "proposal_boundary_records_constitution_alignment_required_check",
    "proposal_boundary_records_origin_provenance_required_check",
    "proposal_boundary_records_identity_boundary_required_check",
    "proposal_boundary_records_invariant_validation_required_check",
    "proposal_boundary_records_root_conflict_resolver_required_check",
    "proposal_boundary_records_multi_cycle_continuity_required_check",
    "proposal_boundary_records_audit_replay_required_check",
    "proposal_boundary_records_direct_mutation_disabled_check",
    "proposal_boundary_records_autonomous_override_disabled_check",
    "source_mutation_intake_metadata_boundary_check",
    "human_sovereignty_proposal_gate_check",
    "source_constitution_alignment_requirement_check",
    "origin_provenance_preservation_requirement_check",
    "civilizational_identity_non_escalation_requirement_check",
    "source_memory_invariant_validation_requirement_check",
    "root_governance_conflict_resolution_requirement_check",
    "multi_cycle_continuity_requirement_check",
    "audit_replay_requirement_check",
    "proposal_scope_definition_boundary_check",
    "proposal_risk_classification_boundary_check",
    "proposal_review_readiness_boundary_check",
    "no_auto_proposal_creation_boundary_check",
    "no_auto_proposal_approval_boundary_check",
    "no_source_or_memory_graph_mutation_boundary_check",
    "source_mutation_review_gate_handoff_boundary_check",
    "source_mutation_proposal_boundary_sections_complete_check",
    "source_mutation_proposal_boundary_sections_pass_check",
    "source_mutation_proposal_boundary_contracts_pass_check",
    "no_source_mutation_runtime_check",
    "no_source_mutation_execution_check",
    "no_source_mutation_performed_check",
    "no_source_mutation_proposal_creation_check",
    "no_source_mutation_proposal_approval_check",
    "no_source_mutation_review_check",
    "no_source_mutation_review_gate_activation_check",
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
    "no_proposal_auto_creation_check",
    "no_proposal_auto_approval_check",
    "deterministic_source_mutation_proposal_boundary_hash_check",
    "ready_for_source_mutation_review_gate_design_check",
)

REQUIRED_TRUE_RECORD_FLAGS = (
    "required",
    "human_review_required",
    "source_mutation_review_gate_required",
    "source_constitution_alignment_required",
    "origin_provenance_preservation_required",
    "civilizational_identity_boundary_required",
    "source_memory_invariant_validation_required",
    "root_governance_conflict_resolution_required",
    "multi_cycle_continuity_required",
    "audit_replay_required",
    "proposal_metadata_only",
)

REQUIRED_FALSE_RECORD_FLAGS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "source_mutation_runtime_created",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_mutation_proposal_created",
    "source_mutation_proposal_approved",
    "source_mutation_proposal_rejected",
    "source_mutation_review_performed",
    "source_mutation_review_gate_created",
    "source_mutation_review_gate_activated",
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
    "proposal_auto_creation_allowed",
    "proposal_auto_approval_allowed",
    "proposal_runtime_activation_allowed",
    "proposal_memory_write_allowed",
    "proposal_source_graph_mutation_allowed",
    "proposal_memory_graph_mutation_allowed",
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
def boundary() -> dict[str, object]:
    return build_governance_source_mutation_proposal_boundary()


def _record_by_id(
    boundary: dict[str, object],
    record_id: str,
) -> dict[str, object]:
    for record in boundary["source_mutation_proposal_boundary_records"]:
        if record["proposal_boundary_record_id"] == record_id:
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


def test_constants_match_v6_7_contract():
    assert GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_VERSION == "6.9.0"
    assert GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SCHEMA_VERSION == "6.9.0"
    assert GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_TYPE == (
        "governance_source_mutation_proposal_boundary"
    )
    assert GOVERNANCE_SOURCE_MUTATION_PROPOSAL_BOUNDARY_HASH_ALGORITHM == "sha256"
    assert SOURCE_MUTATION_PROPOSAL_BOUNDARY_STAGE == (
        "v6.7_source_mutation_proposal_boundary"
    )
    assert SOURCE_MUTATION_PROPOSAL_BOUNDARY_MODE == (
        "source_mutation_proposal_boundary_only"
    )
    assert SOURCE_MUTATION_PROPOSAL_MODE == "metadata_only"
    assert SOURCE_MUTATION_PROPOSAL_BOUNDARY_STATUS == (
        "proposal_boundary_candidate_only"
    )
    assert SOURCE_MUTATION_PROPOSAL_BOUNDARY_ACTIVE_STATUS == "not_active"
    assert SOURCE_MUTATION_RUNTIME_STATUS == "not_active"
    assert SOURCE_MUTATION_EXECUTION_STATUS == "not_active"
    assert SOURCE_MUTATION_PROPOSAL_CREATION_STATUS == "not_active"
    assert SOURCE_MUTATION_PROPOSAL_APPROVAL_STATUS == "not_active"
    assert SOURCE_MUTATION_REVIEW_STATUS == "not_active"
    assert SOURCE_MUTATION_REVIEW_GATE_STATUS == "not_active"
    assert SOURCE_MUTATION_STATUS == "not_performed"
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
    assert V6_7_STATUS == "source_mutation_proposal_boundary_only"
    assert V6_8_HANDOFF_STATUS == "ready_for_source_mutation_review_gate_design"


def test_public_shape_is_deterministic_and_passes(boundary):
    repeated = build_governance_source_mutation_proposal_boundary()
    assert repeated == boundary
    assert boundary["version"] == "6.9.0"
    assert boundary["schema_version"] == "6.9.0"
    assert boundary["source_mutation_proposal_boundary_status"] == "pass"
    assert boundary["source_mutation_proposal_boundary_stage"] == (
        "v6.7_source_mutation_proposal_boundary"
    )
    assert boundary["source_mutation_proposal_boundary_mode"] == (
        "source_mutation_proposal_boundary_only"
    )
    assert boundary["source_mutation_proposal_mode"] == "metadata_only"
    assert boundary["blocking_reasons"] == []
    assert boundary["handoff_status"] == (
        "ready_for_source_mutation_review_gate_design"
    )
    assert boundary["next_stage"] == "v6.8_source_mutation_review_gate"
    assert boundary["next_stage_title"] == "Source Mutation Review Gate"


def test_upstream_v6_6_handoff_verification(boundary):
    assert boundary["upstream_multi_cycle_continuity_protocol_version"] == "6.9.0"
    assert boundary["upstream_multi_cycle_continuity_protocol_status"] == "pass"
    assert len(boundary["upstream_multi_cycle_continuity_protocol_hash"]) == 64
    assert boundary["upstream_handoff_status"] == (
        "ready_for_source_mutation_proposal_boundary_design"
    )
    assert boundary["upstream_next_stage"] == (
        "v6.7_source_mutation_proposal_boundary"
    )
    assert boundary["upstream_next_stage_title"] == (
        "Source Mutation Proposal Boundary"
    )
    assert boundary["upstream_multi_cycle_continuity_record_count"] == 16
    assert (
        boundary[
            "upstream_multi_cycle_continuity_records_registered_metadata_only"
        ]
        is True
    )
    assert (
        boundary["upstream_multi_cycle_continuity_records_require_review"]
        is True
    )
    assert (
        boundary[
            "upstream_multi_cycle_continuity_records_disable_unsafe_surfaces"
        ]
        is True
    )
    assert boundary["upstream_safety_boundaries_clear"] is True


def test_required_record_ids_are_stable_and_complete(boundary):
    assert REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS == (
        EXPECTED_RECORD_IDS
    )
    assert list_governance_source_mutation_proposal_boundary_record_ids() == (
        list(EXPECTED_RECORD_IDS)
    )
    assert [
        record["proposal_boundary_record_id"]
        for record in boundary["source_mutation_proposal_boundary_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_registered_metadata_only(boundary):
    for record in boundary["source_mutation_proposal_boundary_records"]:
        assert record["proposal_boundary_record_status"] == (
            "registered_metadata_only"
        )
        assert record["introduced_in_version"] == "6.9.0"
        assert record["introduced_in_stage"] == (
            "v6.7_source_mutation_proposal_boundary"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == (
            "v6.6_multi_cycle_continuity_protocol"
        )
        assert record["boundary_strength"] == (
            "source_mutation_proposal_required"
        )
        assert record["proposal_boundary_mode"] == "metadata_only_boundary"
        assert record["blocking_reasons"] == []


def test_all_records_have_required_metadata_and_hashes(boundary):
    repeated = build_governance_source_mutation_proposal_boundary()
    repeated_by_id = {
        record["proposal_boundary_record_id"]: record
        for record in repeated["source_mutation_proposal_boundary_records"]
    }
    for record in boundary["source_mutation_proposal_boundary_records"]:
        for field_name in (
            "proposal_boundary_statement",
            "proposal_boundary_scope",
            "required_proposal_metadata_scope",
            "forbidden_proposal_activation_scope",
            "proposal_boundary_disposition",
            "proposal_boundary_reason",
            "proposal_boundary_source_stage",
            "proposal_boundary_source_reference",
            "proposal_boundary_hash",
            "proposal_boundary_record_hash",
        ):
            assert record[field_name]
        assert len(record["proposal_boundary_hash"]) == 64
        assert len(record["proposal_boundary_record_hash"]) == 64
        assert record["proposal_boundary_hash"] == _proposal_boundary_hash(
            record
        )
        assert record["proposal_boundary_record_hash"] == (
            _proposal_boundary_record_hash(record)
        )
        assert record == repeated_by_id[record["proposal_boundary_record_id"]]


def test_all_records_require_governed_review(boundary):
    for record in boundary["source_mutation_proposal_boundary_records"]:
        for field_name in REQUIRED_TRUE_RECORD_FLAGS:
            assert record[field_name] is True


def test_all_records_disable_runtime_mutation_review_and_authority(boundary):
    for record in boundary["source_mutation_proposal_boundary_records"]:
        for field_name in REQUIRED_FALSE_RECORD_FLAGS:
            assert record[field_name] is False
        _assert_all_safety_false(record)


@pytest.mark.parametrize(("record_id", "disposition"), EXPECTED_RECORDS)
def test_each_required_proposal_boundary_record(
    boundary,
    record_id,
    disposition,
):
    record = _record_by_id(boundary, record_id)
    assert record["proposal_boundary_disposition"] == disposition
    assert record["proposal_boundary_record_status"] == (
        "registered_metadata_only"
    )


def test_section_names_are_stable_and_complete(boundary):
    assert REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SECTION_NAMES == (
        EXPECTED_SECTION_NAMES
    )
    assert list_governance_source_mutation_proposal_boundary_section_names() == (
        list(EXPECTED_SECTION_NAMES)
    )
    assert [
        section["section_name"]
        for section in boundary["source_mutation_proposal_boundary_sections"]
    ] == list(EXPECTED_SECTION_NAMES)


def test_contract_names_are_stable_and_complete(boundary):
    assert REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CONTRACT_NAMES == (
        EXPECTED_CONTRACT_NAMES
    )
    assert (
        list_governance_source_mutation_proposal_boundary_contract_names()
        == list(EXPECTED_CONTRACT_NAMES)
    )
    assert [
        contract["contract_name"]
        for contract in boundary["source_mutation_proposal_boundary_contracts"]
    ] == list(EXPECTED_CONTRACT_NAMES)


def test_check_names_are_stable_and_complete(boundary):
    assert REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CHECK_NAMES == (
        EXPECTED_CHECK_NAMES
    )
    assert list_governance_source_mutation_proposal_boundary_check_names() == (
        list(EXPECTED_CHECK_NAMES)
    )
    assert [
        check["check_name"]
        for check in boundary["source_mutation_proposal_boundary_checks"]
    ] == list(EXPECTED_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = EXPECTED_RECORD_IDS[0]
    record = get_governance_source_mutation_proposal_boundary_record(record_id)
    record["proposal_boundary_name"] = "changed"
    assert (
        get_governance_source_mutation_proposal_boundary_record(record_id)[
            "proposal_boundary_name"
        ]
        != "changed"
    )

    section_name = EXPECTED_SECTION_NAMES[0]
    section = get_governance_source_mutation_proposal_boundary_section(
        section_name
    )
    section["observed"]["condition_met"] = False
    assert (
        get_governance_source_mutation_proposal_boundary_section(section_name)[
            "observed"
        ]["condition_met"]
        is True
    )

    contract_name = EXPECTED_CONTRACT_NAMES[0]
    contract = get_governance_source_mutation_proposal_boundary_contract(
        contract_name
    )
    contract["observed"] = False
    assert (
        get_governance_source_mutation_proposal_boundary_contract(
            contract_name
        )["observed"]
        is True
    )

    check_name = EXPECTED_CHECK_NAMES[0]
    check = get_governance_source_mutation_proposal_boundary_check(check_name)
    check["observed"] = False
    assert (
        get_governance_source_mutation_proposal_boundary_check(check_name)[
            "observed"
        ]
        is True
    )


def test_unknown_getters_are_blocked():
    record = get_governance_source_mutation_proposal_boundary_record("unknown")
    section = get_governance_source_mutation_proposal_boundary_section("unknown")
    contract = get_governance_source_mutation_proposal_boundary_contract(
        "unknown"
    )
    check = get_governance_source_mutation_proposal_boundary_check("unknown")
    assert record["proposal_boundary_record_status"] == "blocked"
    assert record["known_record"] is False
    assert section["section_status"] == "blocked"
    assert contract["contract_status"] == "blocked"
    assert check["check_status"] == "blocked"
    for item in (record, section, contract, check):
        assert item["blocking_reasons"]
    _assert_all_safety_false(
        {"record": record, "section": section, "contract": contract, "check": check}
    )


def test_all_sections_contracts_and_checks_pass(boundary):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in boundary["source_mutation_proposal_boundary_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in boundary["source_mutation_proposal_boundary_contracts"]
    )
    assert all(
        check["check_status"] == "pass" and check["blocking_reasons"] == []
        for check in boundary["source_mutation_proposal_boundary_checks"]
    )


def test_all_safety_fields_are_false(boundary):
    _assert_all_safety_false(boundary)
    for field_name in (
        "source_mutation_runtime_created",
        "source_mutation_execution_created",
        "source_mutation_performed",
        "source_mutation_proposal_created",
        "source_mutation_proposal_approved",
        "source_mutation_proposal_rejected",
        "source_mutation_review_performed",
        "source_mutation_review_gate_created",
        "source_mutation_review_gate_activated",
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
        "proposal_auto_creation_allowed",
        "proposal_auto_approval_allowed",
        "self_authorization_allowed",
        "hidden_execution_allowed",
        "unapproved_mutation_allowed",
    ):
        assert boundary[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite(boundary):
    first = governance_source_mutation_proposal_boundary_to_json(boundary)
    second = governance_source_mutation_proposal_boundary_to_json(boundary)
    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == boundary
    with pytest.raises(ValueError):
        governance_source_mutation_proposal_boundary_to_json(
            {"value": math.nan}
        )


def test_all_mapping_keys_are_strings(boundary):
    _assert_mapping_keys_are_strings(boundary)


def test_boundary_and_record_hashes_are_stable(boundary):
    repeated = build_governance_source_mutation_proposal_boundary()
    assert (
        boundary["deterministic_source_mutation_proposal_boundary_hash"]
        == repeated["deterministic_source_mutation_proposal_boundary_hash"]
    )
    assert len(
        boundary["deterministic_source_mutation_proposal_boundary_hash"]
    ) == 64
    for first, second in zip(
        boundary["source_mutation_proposal_boundary_records"],
        repeated["source_mutation_proposal_boundary_records"],
        strict=True,
    ):
        assert first["proposal_boundary_hash"] == second[
            "proposal_boundary_hash"
        ]
        assert first["proposal_boundary_record_hash"] == second[
            "proposal_boundary_record_hash"
        ]


@pytest.mark.parametrize(
    ("container", "field"),
    (
        (
            "source_mutation_proposal_boundary_records",
            "proposal_boundary_statement",
        ),
        (
            "source_mutation_proposal_boundary_sections",
            "source_mutation_proposal_boundary_notes",
        ),
        ("source_mutation_proposal_boundary_contracts", "observed"),
        ("source_mutation_proposal_boundary_checks", "observed"),
        ("source_mutation_proposal_boundary_summary", "current_stage_title"),
    ),
)
def test_boundary_hash_changes_when_governance_data_changes(
    boundary,
    container,
    field,
):
    mutated = deepcopy(boundary)
    target = mutated[container][0] if isinstance(mutated[container], list) else (
        mutated[container]
    )
    target[field] = (
        not target[field]
        if isinstance(target[field], bool)
        else f"{target[field]} changed"
    )
    assert _source_mutation_proposal_boundary_hash(mutated) != (
        boundary["deterministic_source_mutation_proposal_boundary_hash"]
    )


def test_hash_input_excludes_raw_upstream_payload(boundary):
    contract = boundary["hash_input_contract"]
    assert contract["raw_multi_cycle_continuity_protocol_included"] is False
    assert "multi_cycle_continuity_records" not in contract["hash_fields"]
    assert (
        "upstream_multi_cycle_continuity_protocol_status"
        in contract["hash_fields"]
    )
    assert (
        "upstream_multi_cycle_continuity_protocol_hash"
        in contract["hash_fields"]
    )
    for field_name in (
        "source_mutation_proposal_boundary_records",
        "source_mutation_proposal_boundary_sections",
        "source_mutation_proposal_boundary_contracts",
        "source_mutation_proposal_boundary_checks",
        "source_mutation_proposal_boundary_summary",
    ):
        assert field_name in contract["hash_fields"]


def test_no_sensitive_terms_leak(boundary):
    _assert_no_sensitive_terms(boundary)
    _assert_no_sensitive_terms(
        governance_source_mutation_proposal_boundary_to_json(boundary)
    )


def test_new_module_has_no_live_io_or_execution_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots: set[str] = set()
    called_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(
                alias.name.split(".", 1)[0] for alias in node.names
            )
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
