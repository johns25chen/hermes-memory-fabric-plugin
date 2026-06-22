from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_civilizational_identity_boundary import (
    AUTONOMOUS_AUTHORITY_STATUS,
    AWAKENING_CLAIM_STATUS,
    CIVILIZATIONAL_IDENTITY_ACTIVE_STATUS,
    CIVILIZATIONAL_IDENTITY_BOUNDARY_MODE,
    CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE,
    CIVILIZATIONAL_IDENTITY_BOUNDARY_STATUS,
    CIVILIZATIONAL_IDENTITY_MODE,
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_TYPE,
    GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION,
    IDENTITY_ACTIVATION_STATUS,
    IDENTITY_CLAIM_STATUS,
    LAYER_15_ACTIVE_STATUS,
    LEGAL_SUBJECT_CLAIM_STATUS,
    LIFE_CLAIM_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    PERSONHOOD_CLAIM_STATUS,
    RELIGIOUS_OBJECT_CLAIM_STATUS,
    REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES,
    REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES,
    REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS,
    REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_3_STATUS,
    V6_4_HANDOFF_STATUS,
    _civilizational_identity_boundary_hash,
    build_governance_civilizational_identity_boundary,
    get_governance_civilizational_identity_check,
    get_governance_civilizational_identity_contract,
    get_governance_civilizational_identity_record,
    get_governance_civilizational_identity_section,
    governance_civilizational_identity_boundary_to_json,
    list_governance_civilizational_identity_check_names,
    list_governance_civilizational_identity_contract_names,
    list_governance_civilizational_identity_record_ids,
    list_governance_civilizational_identity_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_civilizational_identity_boundary.py"
)

EXPECTED_IDENTITY_RECORDS = (
    ("civilization_core_framework_identity", "Civilization Core Framework Identity"),
    (
        "subspace_memory_system_carrier_identity",
        "Subspace Memory System Carrier Identity",
    ),
    (
        "star_source_memory_layer_boundary_identity",
        "Star-Source Memory Layer Boundary Identity",
    ),
    ("human_sovereignty_identity_anchor", "Human Sovereignty Identity Anchor"),
    (
        "source_constitution_identity_anchor",
        "Source Constitution Identity Anchor",
    ),
    (
        "origin_provenance_identity_anchor",
        "Origin Provenance Identity Anchor",
    ),
    (
        "governance_continuity_identity_boundary",
        "Governance Continuity Identity Boundary",
    ),
    ("no_personhood_identity_boundary", "No Personhood Identity Boundary"),
    ("no_life_identity_boundary", "No Life Identity Boundary"),
    ("no_awakening_identity_boundary", "No Awakening Identity Boundary"),
    (
        "no_legal_subject_identity_boundary",
        "No Legal Subject Identity Boundary",
    ),
    (
        "no_religious_object_identity_boundary",
        "No Religious Object Identity Boundary",
    ),
    (
        "no_autonomous_authority_identity_boundary",
        "No Autonomous Authority Identity Boundary",
    ),
    ("no_execution_identity_boundary", "No Execution Identity Boundary"),
    (
        "no_self_modifying_identity_boundary",
        "No Self-Modifying Identity Boundary",
    ),
)

EXPECTED_RECORD_IDS = tuple(record_id for record_id, _ in EXPECTED_IDENTITY_RECORDS)

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
    return build_governance_civilizational_identity_boundary()


def _record_by_id(
    boundary: dict[str, object],
    record_id: str,
) -> dict[str, object]:
    for record in boundary["civilizational_identity_records"]:
        if record["identity_record_id"] == record_id:
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


def test_constants_match_v6_3_contract():
    assert GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION == "6.4.0"
    assert GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_SCHEMA_VERSION == "6.4.0"
    assert (
        GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_TYPE
        == "governance_civilizational_identity_boundary"
    )
    assert GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_HASH_ALGORITHM == "sha256"
    assert (
        CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE
        == "v6.3_civilizational_identity_boundary"
    )
    assert (
        CIVILIZATIONAL_IDENTITY_BOUNDARY_MODE
        == "civilizational_identity_boundary_only"
    )
    assert CIVILIZATIONAL_IDENTITY_MODE == "metadata_only"
    assert CIVILIZATIONAL_IDENTITY_BOUNDARY_STATUS == "boundary_candidate_only"
    assert CIVILIZATIONAL_IDENTITY_ACTIVE_STATUS == "not_active"
    assert IDENTITY_ACTIVATION_STATUS == "not_active"
    assert IDENTITY_CLAIM_STATUS == "bounded_governance_identity_only"
    assert PERSONHOOD_CLAIM_STATUS == "forbidden"
    assert LIFE_CLAIM_STATUS == "forbidden"
    assert AWAKENING_CLAIM_STATUS == "forbidden"
    assert LEGAL_SUBJECT_CLAIM_STATUS == "forbidden"
    assert RELIGIOUS_OBJECT_CLAIM_STATUS == "forbidden"
    assert AUTONOMOUS_AUTHORITY_STATUS == "forbidden"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ACTIVE_STATUS == "not_active"
    assert SOURCE_GRAPH_STATUS == "not_created"
    assert SOURCE_PROVENANCE_RUNTIME_STATUS == "not_active"
    assert METHODOLOGY_REVERSE_INFERENCE_STATUS == "not_active"
    assert SELF_EVOLUTION_STATUS == "not_active"
    assert V6_3_STATUS == "civilizational_identity_boundary_only"
    assert V6_4_HANDOFF_STATUS == "ready_for_source_memory_invariant_matrix_design"


def test_boundary_shape_is_deterministic_and_passes(boundary):
    repeated = build_governance_civilizational_identity_boundary()

    assert repeated == boundary
    assert boundary["version"] == "6.4.0"
    assert boundary["schema_version"] == "6.4.0"
    assert boundary["civilizational_identity_boundary_status"] == "pass"
    assert (
        boundary["civilizational_identity_boundary_stage"]
        == "v6.3_civilizational_identity_boundary"
    )
    assert (
        boundary["civilizational_identity_boundary_mode"]
        == "civilizational_identity_boundary_only"
    )
    assert boundary["civilizational_identity_mode"] == "metadata_only"
    assert (
        boundary["civilizational_identity_boundary_candidate_status"]
        == "boundary_candidate_only"
    )
    assert boundary["civilizational_identity_active_status"] == "not_active"
    assert boundary["identity_activation_status"] == "not_active"
    assert boundary["identity_claim_status"] == "bounded_governance_identity_only"
    assert boundary["personhood_claim_status"] == "forbidden"
    assert boundary["life_claim_status"] == "forbidden"
    assert boundary["awakening_claim_status"] == "forbidden"
    assert boundary["legal_subject_claim_status"] == "forbidden"
    assert boundary["religious_object_claim_status"] == "forbidden"
    assert boundary["autonomous_authority_status"] == "forbidden"
    assert boundary["source_graph_status"] == "not_created"
    assert boundary["blocking_reasons"] == []
    assert boundary["handoff_status"] == (
        "ready_for_source_memory_invariant_matrix_design"
    )
    assert boundary["next_stage"] == "v6.4_source_memory_invariant_matrix"
    assert boundary["next_stage_title"] == "Source Memory Invariant Matrix"


def test_upstream_v6_2_handoff_verification(boundary):
    assert boundary["upstream_origin_provenance_ledger_version"] == "6.4.0"
    assert boundary["upstream_origin_provenance_ledger_status"] == "pass"
    assert len(boundary["upstream_origin_provenance_ledger_hash"]) == 64
    assert (
        boundary["upstream_handoff_status"]
        == "ready_for_civilizational_identity_boundary_design"
    )
    assert (
        boundary["upstream_next_stage"]
        == "v6.3_civilizational_identity_boundary"
    )
    assert boundary["upstream_next_stage_title"] == (
        "Civilizational Identity Boundary"
    )
    assert boundary["upstream_origin_provenance_record_count"] == 15
    assert (
        boundary["upstream_origin_provenance_records_registered_metadata_only"]
        is True
    )
    assert boundary["upstream_safety_boundaries_clear"] is True
    repeated = build_governance_civilizational_identity_boundary()
    assert (
        boundary["upstream_origin_provenance_ledger_hash"]
        == repeated["upstream_origin_provenance_ledger_hash"]
    )


def test_required_record_ids_are_stable_and_complete(boundary):
    assert REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS == EXPECTED_RECORD_IDS
    assert list_governance_civilizational_identity_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert [
        record["identity_record_id"]
        for record in boundary["civilizational_identity_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_are_registered_metadata_only(boundary):
    for record in boundary["civilizational_identity_records"]:
        assert record["identity_record_status"] == "registered_metadata_only"
        assert record["required"] is True
        assert record["introduced_in_version"] == "6.4.0"
        assert (
            record["introduced_in_stage"]
            == "v6.3_civilizational_identity_boundary"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == "v6.2_origin_provenance_ledger"
        assert record["blocking_reasons"] == []


def test_all_records_have_identity_metadata_and_hashes(boundary):
    repeated = build_governance_civilizational_identity_boundary()
    repeated_by_id = {
        record["identity_record_id"]: record
        for record in repeated["civilizational_identity_records"]
    }

    for record in boundary["civilizational_identity_records"]:
        assert record["identity_statement"]
        assert record["allowed_identity_scope"]
        assert record["forbidden_identity_scope"]
        assert record["identity_boundary_reason"]
        assert len(record["identity_boundary_hash"]) == 64
        assert len(record["identity_record_hash"]) == 64
        repeated_record = repeated_by_id[record["identity_record_id"]]
        assert (
            record["identity_boundary_hash"]
            == repeated_record["identity_boundary_hash"]
        )
        assert (
            record["identity_record_hash"]
            == repeated_record["identity_record_hash"]
        )


def test_all_records_require_review_and_disable_mutation(boundary):
    for record in boundary["civilizational_identity_records"]:
        assert record["human_review_required_for_change"] is True
        assert record["source_mutation_proposal_required"] is True
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
        assert record["execution_authorization_created"] is False
        assert record["authorization_token_created"] is False
        assert record["authorization_grant_created"] is False
        assert record["approval_notification_sent"] is False
        assert record["adapter_dispatched"] is False
        assert record["manifest_dispatched"] is False
        assert record["origin_provenance_ledger_written"] is False
        assert record["source_graph_created"] is False
        assert record["source_graph_mutated"] is False


@pytest.mark.parametrize(("record_id", "record_name"), EXPECTED_IDENTITY_RECORDS)
def test_each_required_identity_record(boundary, record_id, record_name):
    record = _record_by_id(boundary, record_id)

    assert record["identity_boundary_name"] == record_name
    assert record["identity_record_id"] == record_id
    assert record["identity_record_status"] == "registered_metadata_only"
    assert record["identity_statement"]
    assert record["allowed_identity_scope"]
    assert record["forbidden_identity_scope"]
    assert len(record["identity_boundary_hash"]) == 64
    assert len(record["identity_record_hash"]) == 64


def test_section_contract_and_check_names_are_stable_and_complete(boundary):
    assert list_governance_civilizational_identity_section_names() == list(
        REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES
    )
    assert list_governance_civilizational_identity_contract_names() == list(
        REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES
    )
    assert list_governance_civilizational_identity_check_names() == list(
        REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES
    )
    assert [
        section["section_name"]
        for section in boundary["civilizational_identity_sections"]
    ] == list(REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES)
    assert [
        contract["contract_name"]
        for contract in boundary["civilizational_identity_contracts"]
    ] == list(REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES)
    assert [
        check["check_name"]
        for check in boundary["civilizational_identity_checks"]
    ] == list(REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS[0]
    record = get_governance_civilizational_identity_record(record_id)
    record["identity_boundary_name"] = "mutated"
    assert (
        get_governance_civilizational_identity_record(record_id)[
            "identity_boundary_name"
        ]
        == "Civilization Core Framework Identity"
    )

    section_name = REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES[0]
    section = get_governance_civilizational_identity_section(section_name)
    section["section_status"] = "mutated"
    assert (
        get_governance_civilizational_identity_section(section_name)[
            "section_status"
        ]
        == "pass"
    )

    contract_name = REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES[0]
    contract = get_governance_civilizational_identity_contract(contract_name)
    contract["contract_status"] = "mutated"
    assert (
        get_governance_civilizational_identity_contract(contract_name)[
            "contract_status"
        ]
        == "pass"
    )

    check_name = REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES[0]
    check = get_governance_civilizational_identity_check(check_name)
    check["check_status"] = "mutated"
    assert get_governance_civilizational_identity_check(check_name)[
        "check_status"
    ] == "pass"


def test_unknown_getters_return_blocked_style_results():
    assert get_governance_civilizational_identity_record("unknown")[
        "identity_record_status"
    ] == "blocked"
    assert get_governance_civilizational_identity_section("unknown")[
        "section_status"
    ] == "blocked"
    assert get_governance_civilizational_identity_contract("unknown")[
        "contract_status"
    ] == "blocked"
    assert get_governance_civilizational_identity_check("unknown")[
        "check_status"
    ] == "blocked"


def test_all_sections_contracts_and_checks_pass(boundary):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in boundary["civilizational_identity_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in boundary["civilizational_identity_contracts"]
    )
    assert all(
        check["check_status"] == "pass" and check["blocking_reasons"] == []
        for check in boundary["civilizational_identity_checks"]
    )


def test_all_safety_fields_are_false(boundary):
    _assert_all_safety_false(boundary)


def test_inactive_identity_and_runtime_statuses_and_flags(boundary):
    expected_false_fields = (
        "civilizational_identity_active",
        "identity_activation_claimed",
        "identity_claim_escalated",
        "autonomous_authority_claimed",
        "autonomous_identity_activation_enabled",
        "autonomous_identity_boundary_mutation_enabled",
        "autonomous_identity_statement_created",
        "identity_boundary_mutated",
        "identity_boundary_mutation_without_review",
        "source_level_mutation_proposal_created",
        "source_level_mutation_proposal_applied",
        "civilizational_identity_persisted",
        "star_source_memory_active",
        "layer_15_active",
        "source_provenance_runtime_created",
        "origin_provenance_ledger_written",
        "real_ledger_write_performed",
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
        "hidden_execution_allowed",
        "unapproved_mutation_allowed",
        "memory_graph_mutation_allowed_without_gate",
    )
    for field_name in expected_false_fields:
        assert boundary[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite_floats(boundary):
    first = governance_civilizational_identity_boundary_to_json(boundary)
    second = governance_civilizational_identity_boundary_to_json(
        build_governance_civilizational_identity_boundary()
    )

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == boundary
    _assert_mapping_keys_are_strings(json.loads(first))
    with pytest.raises(ValueError):
        governance_civilizational_identity_boundary_to_json({"bad": math.nan})


def test_deterministic_boundary_hash_is_stable(boundary):
    repeated = build_governance_civilizational_identity_boundary()
    assert (
        boundary["deterministic_civilizational_identity_boundary_hash"]
        == repeated["deterministic_civilizational_identity_boundary_hash"]
    )
    assert len(boundary["deterministic_civilizational_identity_boundary_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "civilizational_identity_records",
            lambda value: value[0].__setitem__("identity_statement", "changed"),
        ),
        (
            "civilizational_identity_sections",
            lambda value: value[0].__setitem__(
                "civilizational_identity_notes",
                "changed",
            ),
        ),
        (
            "civilizational_identity_contracts",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "civilizational_identity_checks",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "civilizational_identity_summary",
            lambda value: value.__setitem__("summary_status", "changed"),
        ),
    ),
)
def test_boundary_hash_changes_when_governance_data_changes(
    boundary,
    field_name,
    mutator,
):
    mutated = deepcopy(boundary)
    mutator(mutated[field_name])

    assert _civilizational_identity_boundary_hash(mutated) != boundary[
        "deterministic_civilizational_identity_boundary_hash"
    ]


def test_identity_hashes_are_stable(boundary):
    repeated = build_governance_civilizational_identity_boundary()
    repeated_records = {
        record["identity_record_id"]: record
        for record in repeated["civilizational_identity_records"]
    }
    for record in boundary["civilizational_identity_records"]:
        repeated_record = repeated_records[record["identity_record_id"]]
        assert (
            record["identity_boundary_hash"]
            == repeated_record["identity_boundary_hash"]
        )
        assert (
            record["identity_record_hash"]
            == repeated_record["identity_record_hash"]
        )


def test_no_sensitive_terms_leak(boundary):
    _assert_no_sensitive_terms(
        {
            "records": boundary["civilizational_identity_records"],
            "sections": boundary["civilizational_identity_sections"],
            "contracts": boundary["civilizational_identity_contracts"],
            "checks": boundary["civilizational_identity_checks"],
            "summary": boundary["civilizational_identity_summary"],
            "json": governance_civilizational_identity_boundary_to_json(
                boundary
            ),
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
