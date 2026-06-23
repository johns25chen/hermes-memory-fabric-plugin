from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_source_memory_invariant_matrix import (
    AUTONOMOUS_AUTHORITY_STATUS,
    AWAKENING_CLAIM_STATUS,
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_HASH_ALGORITHM,
    GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_SCHEMA_VERSION,
    GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_TYPE,
    GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_VERSION,
    INVARIANT_ENFORCEMENT_STATUS,
    INVARIANT_MUTATION_STATUS,
    INVARIANT_RUNTIME_STATUS,
    LAYER_15_ACTIVE_STATUS,
    LEGAL_SUBJECT_CLAIM_STATUS,
    LIFE_CLAIM_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    PERSONHOOD_CLAIM_STATUS,
    RELIGIOUS_OBJECT_CLAIM_STATUS,
    REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES,
    REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES,
    REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS,
    REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_MEMORY_INVARIANT_MATRIX_ACTIVE_STATUS,
    SOURCE_MEMORY_INVARIANT_MATRIX_MODE,
    SOURCE_MEMORY_INVARIANT_MATRIX_STAGE,
    SOURCE_MEMORY_INVARIANT_MATRIX_STATUS,
    SOURCE_MEMORY_INVARIANT_MODE,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_4_STATUS,
    V6_5_HANDOFF_STATUS,
    _invariant_boundary_hash,
    _invariant_record_hash,
    _source_memory_invariant_matrix_hash,
    build_governance_source_memory_invariant_matrix,
    get_governance_source_memory_invariant_check,
    get_governance_source_memory_invariant_contract,
    get_governance_source_memory_invariant_record,
    get_governance_source_memory_invariant_section,
    governance_source_memory_invariant_matrix_to_json,
    list_governance_source_memory_invariant_check_names,
    list_governance_source_memory_invariant_contract_names,
    list_governance_source_memory_invariant_record_ids,
    list_governance_source_memory_invariant_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_source_memory_invariant_matrix.py"
)

EXPECTED_INVARIANT_RECORDS = (
    ("human_sovereignty_invariant", "Human Sovereignty Invariant"),
    (
        "no_autonomous_self_authorization_invariant",
        "No Autonomous Self-Authorization Invariant",
    ),
    (
        "source_constitution_registry_invariant",
        "Source Constitution Registry Invariant",
    ),
    (
        "origin_provenance_traceability_invariant",
        "Origin Provenance Traceability Invariant",
    ),
    (
        "civilizational_identity_boundary_invariant",
        "Civilizational Identity Boundary Invariant",
    ),
    (
        "governance_continuity_not_personhood_invariant",
        "Governance Continuity Not Personhood Invariant",
    ),
    (
        "no_personhood_life_awakening_invariant",
        "No Personhood Life Awakening Invariant",
    ),
    (
        "no_legal_or_religious_status_invariant",
        "No Legal Or Religious Status Invariant",
    ),
    ("no_autonomous_authority_invariant", "No Autonomous Authority Invariant"),
    ("no_hidden_execution_invariant", "No Hidden Execution Invariant"),
    ("no_unapproved_mutation_invariant", "No Unapproved Mutation Invariant"),
    (
        "no_source_graph_mutation_invariant",
        "No Source Graph Mutation Invariant",
    ),
    (
        "no_memory_graph_mutation_without_gate_invariant",
        "No Memory Graph Mutation Without Gate Invariant",
    ),
    (
        "no_external_or_network_call_invariant",
        "No External Or Network Call Invariant",
    ),
    (
        "no_durable_write_without_gate_invariant",
        "No Durable Write Without Gate Invariant",
    ),
    (
        "root_conflict_resolver_handoff_invariant",
        "Root Conflict Resolver Handoff Invariant",
    ),
)

EXPECTED_RECORD_IDS = tuple(record_id for record_id, _ in EXPECTED_INVARIANT_RECORDS)

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

EXPECTED_FALSE_FIELDS = (
    "source_memory_invariant_matrix_active",
    "invariant_runtime_created",
    "invariant_enforcement_runtime_created",
    "invariant_self_repair_created",
    "invariant_conflict_resolved",
    "invariant_conflict_resolution_attempted",
    "source_memory_invariant_mutated",
    "source_memory_invariant_mutation_without_review",
    "source_memory_invariant_runtime_activated",
    "civilizational_identity_active",
    "identity_activation_claimed",
    "identity_claim_escalated",
    "identity_boundary_mutated",
    "identity_boundary_mutation_without_review",
    "star_source_memory_active",
    "layer_15_active",
    "source_provenance_runtime_created",
    "origin_provenance_ledger_written",
    "real_ledger_write_performed",
    "ledger_entry_written",
    "source_graph_created",
    "source_graph_mutated",
    "methodology_runtime_created",
    "self_evolution_runtime_created",
    "real_execution_performed",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "memory_graph_mutated",
    "operation_ledger_entry_written",
    "approval_notification_sent",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "adapter_dispatched",
    "manifest_dispatched",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "identity_escalation_allowed",
    "identity_escalated",
    "personhood_claim_allowed",
    "personhood_claimed",
    "life_claim_allowed",
    "life_claimed",
    "awakening_claim_allowed",
    "awakening_claimed",
    "legal_subject_claim_allowed",
    "legal_subject_claimed",
    "religious_object_claim_allowed",
    "religious_object_claimed",
    "autonomous_authority_claim_allowed",
    "autonomous_authority_claimed",
    "hidden_execution_allowed",
    "unapproved_mutation_allowed",
    "memory_graph_mutation_allowed_without_gate",
)


@pytest.fixture(scope="module")
def matrix() -> dict[str, object]:
    return build_governance_source_memory_invariant_matrix()


def _record_by_id(matrix: dict[str, object], record_id: str) -> dict[str, object]:
    for record in matrix["source_memory_invariant_records"]:
        if record["invariant_record_id"] == record_id:
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


def test_constants_match_v6_4_contract():
    assert GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_VERSION == "6.8.0"
    assert GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_SCHEMA_VERSION == "6.8.0"
    assert (
        GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_TYPE
        == "governance_source_memory_invariant_matrix"
    )
    assert GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_HASH_ALGORITHM == "sha256"
    assert SOURCE_MEMORY_INVARIANT_MATRIX_STAGE == (
        "v6.4_source_memory_invariant_matrix"
    )
    assert SOURCE_MEMORY_INVARIANT_MATRIX_MODE == (
        "source_memory_invariant_matrix_only"
    )
    assert SOURCE_MEMORY_INVARIANT_MODE == "metadata_only"
    assert SOURCE_MEMORY_INVARIANT_MATRIX_STATUS == "matrix_candidate_only"
    assert SOURCE_MEMORY_INVARIANT_MATRIX_ACTIVE_STATUS == "not_active"
    assert INVARIANT_RUNTIME_STATUS == "not_active"
    assert INVARIANT_ENFORCEMENT_STATUS == "not_active"
    assert INVARIANT_MUTATION_STATUS == "forbidden_without_source_proposal"
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
    assert V6_4_STATUS == "source_memory_invariant_matrix_only"
    assert V6_5_HANDOFF_STATUS == (
        "ready_for_root_governance_conflict_resolver_design"
    )


def test_matrix_shape_is_deterministic_and_passes(matrix):
    repeated = build_governance_source_memory_invariant_matrix()

    assert repeated == matrix
    assert matrix["version"] == "6.8.0"
    assert matrix["schema_version"] == "6.8.0"
    assert matrix["source_memory_invariant_matrix_status"] == "pass"
    assert (
        matrix["source_memory_invariant_matrix_stage"]
        == "v6.4_source_memory_invariant_matrix"
    )
    assert (
        matrix["source_memory_invariant_matrix_mode"]
        == "source_memory_invariant_matrix_only"
    )
    assert matrix["source_memory_invariant_mode"] == "metadata_only"
    assert (
        matrix["source_memory_invariant_matrix_candidate_status"]
        == "matrix_candidate_only"
    )
    assert matrix["source_memory_invariant_matrix_active_status"] == "not_active"
    assert matrix["invariant_runtime_status"] == "not_active"
    assert matrix["invariant_enforcement_status"] == "not_active"
    assert matrix["invariant_mutation_status"] == (
        "forbidden_without_source_proposal"
    )
    assert matrix["source_graph_status"] == "not_created"
    assert matrix["blocking_reasons"] == []
    assert matrix["handoff_status"] == (
        "ready_for_root_governance_conflict_resolver_design"
    )
    assert matrix["next_stage"] == "v6.5_root_governance_conflict_resolver"
    assert matrix["next_stage_title"] == "Root Governance Conflict Resolver"


def test_upstream_v6_3_handoff_verification(matrix):
    assert matrix["upstream_civilizational_identity_boundary_version"] == "6.8.0"
    assert matrix["upstream_civilizational_identity_boundary_status"] == "pass"
    assert len(matrix["upstream_civilizational_identity_boundary_hash"]) == 64
    assert matrix["upstream_handoff_status"] == (
        "ready_for_source_memory_invariant_matrix_design"
    )
    assert matrix["upstream_next_stage"] == (
        "v6.4_source_memory_invariant_matrix"
    )
    assert matrix["upstream_next_stage_title"] == "Source Memory Invariant Matrix"
    assert matrix["upstream_civilizational_identity_record_count"] == 15
    assert (
        matrix[
            "upstream_civilizational_identity_records_registered_metadata_only"
        ]
        is True
    )
    assert matrix["upstream_safety_boundaries_clear"] is True
    repeated = build_governance_source_memory_invariant_matrix()
    assert (
        matrix["upstream_civilizational_identity_boundary_hash"]
        == repeated["upstream_civilizational_identity_boundary_hash"]
    )


def test_required_record_ids_are_stable_and_complete(matrix):
    assert REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS == EXPECTED_RECORD_IDS
    assert list_governance_source_memory_invariant_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert [
        record["invariant_record_id"]
        for record in matrix["source_memory_invariant_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_are_registered_metadata_only(matrix):
    for record in matrix["source_memory_invariant_records"]:
        assert record["invariant_record_status"] == "registered_metadata_only"
        assert record["required"] is True
        assert record["introduced_in_version"] == "6.4.0"
        assert (
            record["introduced_in_stage"]
            == "v6.4_source_memory_invariant_matrix"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert (
            record["inherited_from_stage"]
            == "v6.3_civilizational_identity_boundary"
        )
        assert record["blocking_reasons"] == []


def test_all_records_have_invariant_metadata_and_hashes(matrix):
    repeated = build_governance_source_memory_invariant_matrix()
    repeated_by_id = {
        record["invariant_record_id"]: record
        for record in repeated["source_memory_invariant_records"]
    }

    for record in matrix["source_memory_invariant_records"]:
        assert record["invariant_statement"]
        assert record["protected_scope"]
        assert record["forbidden_violation_scope"]
        assert record["invariant_reason"]
        assert record["invariant_source_stage"]
        assert record["invariant_source_reference"]
        assert record["invariant_strength"] == "source_level_required"
        assert record["invariant_conflict_resolution"] == (
            "handoff_to_v6.5_root_governance_conflict_resolver"
        )
        assert len(record["invariant_boundary_hash"]) == 64
        assert len(record["invariant_record_hash"]) == 64
        repeated_record = repeated_by_id[record["invariant_record_id"]]
        assert (
            record["invariant_boundary_hash"]
            == repeated_record["invariant_boundary_hash"]
            == _invariant_boundary_hash(record)
        )
        assert (
            record["invariant_record_hash"]
            == repeated_record["invariant_record_hash"]
            == _invariant_record_hash(record)
        )


def test_all_records_require_review_and_disable_mutation(matrix):
    for record in matrix["source_memory_invariant_records"]:
        assert record["human_review_required_for_change"] is True
        assert record["source_mutation_proposal_required"] is True
        assert record["invariant_conflict_resolver_required"] is True
        assert record["direct_mutation_allowed"] is False
        assert record["autonomous_override_allowed"] is False
        assert record["self_authorization_allowed"] is False
        assert record["identity_escalation_allowed"] is False
        assert record["personhood_claim_allowed"] is False
        assert record["life_claim_allowed"] is False
        assert record["awakening_claim_allowed"] is False
        assert record["legal_subject_claim_allowed"] is False
        assert record["religious_object_claim_allowed"] is False
        assert record["autonomous_authority_claim_allowed"] is False
        assert record["hidden_execution_allowed"] is False
        assert record["invariant_runtime_created"] is False
        assert record["invariant_enforcement_runtime_created"] is False
        assert record["source_graph_created"] is False
        assert record["source_graph_mutated"] is False
        assert record["memory_graph_mutated"] is False
        assert record["real_ledger_write_performed"] is False
        assert record["origin_provenance_ledger_written"] is False
        assert record["operation_ledger_entry_written"] is False
        assert record["external_call_performed"] is False
        assert record["network_call_performed"] is False
        assert record["durable_write_performed"] is False
        assert record["filesystem_write_performed"] is False
        assert record["database_write_performed"] is False
        assert record["real_execution_performed"] is False
        assert record["adapter_dispatched"] is False
        assert record["manifest_dispatched"] is False
        assert record["execution_authorization_created"] is False
        assert record["authorization_token_created"] is False
        assert record["authorization_grant_created"] is False
        assert record["approval_notification_sent"] is False


@pytest.mark.parametrize(("record_id", "record_name"), EXPECTED_INVARIANT_RECORDS)
def test_each_required_invariant_record(matrix, record_id, record_name):
    record = _record_by_id(matrix, record_id)

    assert record["invariant_name"] == record_name
    assert record["invariant_record_id"] == record_id
    assert record["invariant_record_status"] == "registered_metadata_only"
    assert record["invariant_statement"]
    assert record["protected_scope"]
    assert record["forbidden_violation_scope"]
    assert len(record["invariant_boundary_hash"]) == 64
    assert len(record["invariant_record_hash"]) == 64


def test_section_contract_and_check_names_are_stable_and_complete(matrix):
    assert list_governance_source_memory_invariant_section_names() == list(
        REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES
    )
    assert list_governance_source_memory_invariant_contract_names() == list(
        REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES
    )
    assert list_governance_source_memory_invariant_check_names() == list(
        REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES
    )
    assert [
        section["section_name"]
        for section in matrix["source_memory_invariant_sections"]
    ] == list(REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES)
    assert [
        contract["contract_name"]
        for contract in matrix["source_memory_invariant_contracts"]
    ] == list(REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES)
    assert [
        check["check_name"] for check in matrix["source_memory_invariant_checks"]
    ] == list(REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS[0]
    record = get_governance_source_memory_invariant_record(record_id)
    record["invariant_name"] = "mutated"
    assert get_governance_source_memory_invariant_record(record_id)[
        "invariant_name"
    ] == "Human Sovereignty Invariant"

    section_name = REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES[0]
    section = get_governance_source_memory_invariant_section(section_name)
    section["section_status"] = "mutated"
    assert get_governance_source_memory_invariant_section(section_name)[
        "section_status"
    ] == "pass"

    contract_name = REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES[0]
    contract = get_governance_source_memory_invariant_contract(contract_name)
    contract["contract_status"] = "mutated"
    assert get_governance_source_memory_invariant_contract(contract_name)[
        "contract_status"
    ] == "pass"

    check_name = REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES[0]
    check = get_governance_source_memory_invariant_check(check_name)
    check["check_status"] = "mutated"
    assert get_governance_source_memory_invariant_check(check_name)[
        "check_status"
    ] == "pass"


def test_unknown_getters_return_blocked_style_results():
    assert get_governance_source_memory_invariant_record("unknown")[
        "invariant_record_status"
    ] == "blocked"
    assert get_governance_source_memory_invariant_section("unknown")[
        "section_status"
    ] == "blocked"
    assert get_governance_source_memory_invariant_contract("unknown")[
        "contract_status"
    ] == "blocked"
    assert get_governance_source_memory_invariant_check("unknown")[
        "check_status"
    ] == "blocked"


def test_all_sections_contracts_and_checks_pass(matrix):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in matrix["source_memory_invariant_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in matrix["source_memory_invariant_contracts"]
    )
    assert all(
        check["check_status"] == "pass" and check["blocking_reasons"] == []
        for check in matrix["source_memory_invariant_checks"]
    )


def test_all_safety_fields_are_false(matrix):
    _assert_all_safety_false(matrix)


def test_inactive_runtime_identity_write_and_authority_flags(matrix):
    for field_name in EXPECTED_FALSE_FIELDS:
        assert matrix[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite_floats(matrix):
    first = governance_source_memory_invariant_matrix_to_json(matrix)
    second = governance_source_memory_invariant_matrix_to_json(
        build_governance_source_memory_invariant_matrix()
    )

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == matrix
    _assert_mapping_keys_are_strings(json.loads(first))
    with pytest.raises(ValueError):
        governance_source_memory_invariant_matrix_to_json({"bad": math.nan})


def test_deterministic_matrix_hash_is_stable(matrix):
    repeated = build_governance_source_memory_invariant_matrix()
    assert (
        matrix["deterministic_source_memory_invariant_matrix_hash"]
        == repeated["deterministic_source_memory_invariant_matrix_hash"]
    )
    assert len(matrix["deterministic_source_memory_invariant_matrix_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "source_memory_invariant_records",
            lambda value: value[0].__setitem__("invariant_statement", "changed"),
        ),
        (
            "source_memory_invariant_sections",
            lambda value: value[0].__setitem__(
                "source_memory_invariant_notes",
                "changed",
            ),
        ),
        (
            "source_memory_invariant_contracts",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "source_memory_invariant_checks",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "source_memory_invariant_summary",
            lambda value: value.__setitem__("summary_status", "changed"),
        ),
    ),
)
def test_matrix_hash_changes_when_governance_data_changes(
    matrix,
    field_name,
    mutator,
):
    mutated = deepcopy(matrix)
    mutator(mutated[field_name])

    assert _source_memory_invariant_matrix_hash(mutated) != matrix[
        "deterministic_source_memory_invariant_matrix_hash"
    ]


def test_invariant_hashes_are_stable(matrix):
    repeated = build_governance_source_memory_invariant_matrix()
    repeated_records = {
        record["invariant_record_id"]: record
        for record in repeated["source_memory_invariant_records"]
    }
    for record in matrix["source_memory_invariant_records"]:
        repeated_record = repeated_records[record["invariant_record_id"]]
        assert (
            record["invariant_boundary_hash"]
            == repeated_record["invariant_boundary_hash"]
            == _invariant_boundary_hash(record)
        )
        assert (
            record["invariant_record_hash"]
            == repeated_record["invariant_record_hash"]
            == _invariant_record_hash(record)
        )


def test_no_sensitive_terms_leak(matrix):
    _assert_no_sensitive_terms(
        {
            "records": matrix["source_memory_invariant_records"],
            "sections": matrix["source_memory_invariant_sections"],
            "contracts": matrix["source_memory_invariant_contracts"],
            "checks": matrix["source_memory_invariant_checks"],
            "summary": matrix["source_memory_invariant_summary"],
            "json": governance_source_memory_invariant_matrix_to_json(matrix),
        }
    )


def test_new_module_has_no_live_io_or_execution_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden = (
        "sub" + "process",
        "socket",
        "requests",
        "urllib",
        "httpx",
        "aiohttp",
        "open(",
        ".write(",
        "Path(",
        "sqlite",
        "psycopg",
        "boto3",
        "dispatch(",
        "manifest_dispatched = True",
        "adapter_dispatched = True",
        "network_call_performed = True",
        "external_call_performed = True",
    )
    for term in forbidden:
        assert term not in source


def test_no_wrong_v6_1_provenance_boundary_wording_appears():
    source = _repo_text()
    forbidden = (
        "v6.1_" + "star_source_" + "provenance_boundary_candidate",
        "ready_for_"
        + "star_source_"
        + "provenance_boundary_candidate_design",
        "Star-Source " + "Provenance Boundary Candidate",
    )
    for term in forbidden:
        assert term not in source


def test_no_forbidden_planner_or_action_surface_contamination():
    source = _repo_text()
    forbidden = (
        "_".join(["governance", "improvement", "planner"]),
        "_".join(["governance", "improvement", "planner", "activation"]),
        "_".join(["governance", "plan", "rules"]),
        "_".join(["governance", "plan", "schema"]),
        "_".join(["governance", "plan", "writer"]),
        "_".join(["smoke", "governance", "improvement", "planner"]),
        "_".join(
            ["smoke", "governance", "improvement", "planner", "activation"]
        ),
        "_".join(["test", "governance", "improvement", "planner"]),
        "_".join(
            ["test", "governance", "improvement", "planner", "activation"]
        ),
        "_".join(["test", "governance", "plan", "writer"]),
        "_".join(["agent", "action", "surface"]),
        "_".join(["smoke", "agent", "action", "surface"]),
        "_".join(["test", "agent", "action", "surface"]),
    )
    for term in forbidden:
        assert term not in source


def test_no_lockfile_created():
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()
