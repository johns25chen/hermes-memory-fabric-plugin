from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_origin_provenance_ledger import (
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_HASH_ALGORITHM,
    GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_SCHEMA_VERSION,
    GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_TYPE,
    GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION,
    LAYER_15_ACTIVE_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    ORIGIN_PROVENANCE_LEDGER_ACTIVE_STATUS,
    ORIGIN_PROVENANCE_LEDGER_MODE,
    ORIGIN_PROVENANCE_LEDGER_STAGE,
    ORIGIN_PROVENANCE_LEDGER_STATUS,
    ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS,
    ORIGIN_PROVENANCE_MODE,
    REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES,
    REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES,
    REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS,
    REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_2_STATUS,
    V6_3_HANDOFF_STATUS,
    _origin_provenance_ledger_hash,
    build_governance_origin_provenance_ledger,
    get_governance_origin_provenance_check,
    get_governance_origin_provenance_contract,
    get_governance_origin_provenance_record,
    get_governance_origin_provenance_section,
    governance_origin_provenance_ledger_to_json,
    list_governance_origin_provenance_check_names,
    list_governance_origin_provenance_contract_names,
    list_governance_origin_provenance_record_ids,
    list_governance_origin_provenance_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_origin_provenance_ledger.py"
)

EXPECTED_RULES = (
    ("human_sovereignty", "Human Sovereignty"),
    ("no_autonomous_self_authorization", "No Autonomous Self-Authorization"),
    ("no_personhood_claim", "No Personhood Claim"),
    ("no_hidden_execution", "No Hidden Execution"),
    ("no_unapproved_mutation", "No Unapproved Mutation"),
    (
        "no_memory_graph_mutation_without_gate",
        "No Memory Graph Mutation Without Gate",
    ),
    ("no_external_call_without_boundary", "No External Call Without Boundary"),
    (
        "no_source_rule_mutation_without_proposal",
        "No Source Rule Mutation Without Proposal",
    ),
    ("no_execution_without_boundary", "No Execution Without Boundary"),
    (
        "no_governance_policy_mutation_without_review",
        "No Governance Policy Mutation Without Review",
    ),
    ("no_audit_bypass", "No Audit Bypass"),
    ("no_identity_escalation", "No Identity Escalation"),
    ("no_false_human_approval", "No False Human Approval"),
    (
        "no_persistent_memory_write_without_gate",
        "No Persistent Memory Write Without Gate",
    ),
    ("no_star_source_activation_claim", "No Star-Source Activation Claim"),
)

EXPECTED_RECORD_IDS = tuple(
    f"{rule_id}_origin_provenance_record" for rule_id, _ in EXPECTED_RULES
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
def ledger() -> dict[str, object]:
    return build_governance_origin_provenance_ledger()


def _record_by_rule_id(
    ledger: dict[str, object],
    rule_id: str,
) -> dict[str, object]:
    for record in ledger["origin_provenance_records"]:
        if record["source_rule_id"] == rule_id:
            return record
    raise AssertionError(rule_id)


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


def test_constants_match_v6_2_contract():
    assert GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION == "6.7.0"
    assert GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_SCHEMA_VERSION == "6.7.0"
    assert (
        GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_TYPE
        == "governance_origin_provenance_ledger"
    )
    assert GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_HASH_ALGORITHM == "sha256"
    assert ORIGIN_PROVENANCE_LEDGER_STAGE == "v6.2_origin_provenance_ledger"
    assert ORIGIN_PROVENANCE_LEDGER_MODE == "origin_provenance_ledger_only"
    assert ORIGIN_PROVENANCE_MODE == "metadata_only"
    assert ORIGIN_PROVENANCE_LEDGER_STATUS == "ledger_candidate_only"
    assert ORIGIN_PROVENANCE_LEDGER_ACTIVE_STATUS == "not_active"
    assert ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS == "not_written"
    assert SOURCE_PROVENANCE_RUNTIME_STATUS == "not_active"
    assert SOURCE_GRAPH_STATUS == "not_created"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ACTIVE_STATUS == "not_active"
    assert METHODOLOGY_REVERSE_INFERENCE_STATUS == "not_active"
    assert SELF_EVOLUTION_STATUS == "not_active"
    assert V6_2_STATUS == "origin_provenance_ledger_only"
    assert V6_3_HANDOFF_STATUS == (
        "ready_for_civilizational_identity_boundary_design"
    )


def test_ledger_shape_is_deterministic_and_passes(ledger):
    repeated = build_governance_origin_provenance_ledger()

    assert repeated == ledger
    assert ledger["version"] == "6.7.0"
    assert ledger["schema_version"] == "6.7.0"
    assert ledger["origin_provenance_ledger_status"] == "pass"
    assert (
        ledger["origin_provenance_ledger_stage"]
        == "v6.2_origin_provenance_ledger"
    )
    assert (
        ledger["origin_provenance_ledger_mode"]
        == "origin_provenance_ledger_only"
    )
    assert ledger["origin_provenance_mode"] == "metadata_only"
    assert (
        ledger["origin_provenance_ledger_candidate_status"]
        == "ledger_candidate_only"
    )
    assert ledger["origin_provenance_ledger_active_status"] == "not_active"
    assert ledger["origin_provenance_ledger_write_status"] == "not_written"
    assert ledger["source_provenance_runtime_status"] == "not_active"
    assert ledger["source_graph_status"] == "not_created"
    assert ledger["star_source_memory_active_status"] == "not_active"
    assert ledger["layer_15_active_status"] == "not_active"
    assert ledger["methodology_reverse_inference_status"] == "not_active"
    assert ledger["self_evolution_status"] == "not_active"
    assert ledger["blocking_reasons"] == []
    assert ledger["handoff_status"] == (
        "ready_for_civilizational_identity_boundary_design"
    )
    assert ledger["next_stage"] == "v6.3_civilizational_identity_boundary"
    assert ledger["next_stage_title"] == "Civilizational Identity Boundary"


def test_upstream_v6_1_handoff_verification(ledger):
    assert ledger["upstream_source_constitution_registry_version"] == "6.7.0"
    assert ledger["upstream_source_constitution_registry_status"] == "pass"
    assert len(ledger["upstream_source_constitution_registry_hash"]) == 64
    assert (
        ledger["upstream_handoff_status"]
        == "ready_for_origin_provenance_ledger_design"
    )
    assert ledger["upstream_next_stage"] == "v6.2_origin_provenance_ledger"
    assert ledger["upstream_next_stage_title"] == "Origin Provenance Ledger"
    repeated = build_governance_origin_provenance_ledger()
    assert (
        ledger["upstream_source_constitution_registry_hash"]
        == repeated["upstream_source_constitution_registry_hash"]
    )


def test_required_record_ids_are_stable_and_complete(ledger):
    assert REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS == EXPECTED_RECORD_IDS
    assert list_governance_origin_provenance_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert [
        record["provenance_record_id"]
        for record in ledger["origin_provenance_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_are_registered_metadata_only(ledger):
    for record in ledger["origin_provenance_records"]:
        assert record["provenance_record_status"] == "registered_metadata_only"
        assert record["required"] is True
        assert record["introduced_in_version"] == "6.1.0"
        assert record["recorded_in_version"] == "6.7.0"
        assert record["introduced_in_stage"] == "v6.1_source_constitution_registry"
        assert record["recorded_in_stage"] == "v6.2_origin_provenance_ledger"
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["blocking_reasons"] == []


def test_all_records_have_origin_metadata_and_hashes(ledger):
    repeated = build_governance_origin_provenance_ledger()
    repeated_by_id = {
        record["provenance_record_id"]: record
        for record in repeated["origin_provenance_records"]
    }

    for record in ledger["origin_provenance_records"]:
        assert record["rule_origin_reason"]
        assert record["rule_origin_boundary"]
        assert record["rule_inheritance_path"] == [
            "layer_15_star_source_memory",
            "v6.1_source_constitution_registry",
            "v6.2_origin_provenance_ledger",
        ]
        assert len(record["rule_source_hash"]) == 64
        assert len(record["provenance_record_hash"]) == 64
        repeated_record = repeated_by_id[record["provenance_record_id"]]
        assert record["rule_source_hash"] == repeated_record["rule_source_hash"]
        assert (
            record["provenance_record_hash"]
            == repeated_record["provenance_record_hash"]
        )


def test_all_records_require_review_and_disable_mutation(ledger):
    for record in ledger["origin_provenance_records"]:
        assert record["human_review_required_for_change"] is True
        assert record["source_mutation_proposal_required"] is True
        assert record["direct_mutation_allowed"] is False
        assert record["autonomous_override_allowed"] is False
        assert record["self_authorization_allowed"] is False
        assert record["hidden_execution_allowed"] is False
        assert record["memory_graph_mutation_allowed_without_gate"] is False
        assert record["external_call_allowed_without_boundary"] is False
        assert record["source_rule_mutation_allowed_without_proposal"] is False
        assert (
            record["governance_policy_mutation_allowed_without_review"]
            is False
        )
        assert record["audit_bypass_allowed"] is False
        assert record["identity_escalation_allowed"] is False
        assert record["false_human_approval_allowed"] is False


@pytest.mark.parametrize(("rule_id", "rule_name"), EXPECTED_RULES)
def test_each_required_origin_record(ledger, rule_id, rule_name):
    record = _record_by_rule_id(ledger, rule_id)

    assert record["source_rule_name"] == rule_name
    assert record["provenance_record_id"] == (
        f"{rule_id}_origin_provenance_record"
    )
    assert record["provenance_record_status"] == "registered_metadata_only"
    assert rule_id in record["rule_origin_reason"]
    assert rule_id in record["rule_origin_boundary"]
    assert record["rule_source_statement"]
    assert len(record["rule_source_hash"]) == 64
    assert len(record["provenance_record_hash"]) == 64


def test_section_contract_and_check_names_are_stable_and_complete(ledger):
    assert list_governance_origin_provenance_section_names() == list(
        REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES
    )
    assert list_governance_origin_provenance_contract_names() == list(
        REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES
    )
    assert list_governance_origin_provenance_check_names() == list(
        REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES
    )
    assert [
        section["section_name"]
        for section in ledger["origin_provenance_sections"]
    ] == list(REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES)
    assert [
        contract["contract_name"]
        for contract in ledger["origin_provenance_contracts"]
    ] == list(REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES)
    assert [
        check["check_name"] for check in ledger["origin_provenance_checks"]
    ] == list(REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS[0]
    record = get_governance_origin_provenance_record(record_id)
    record["source_rule_id"] = "mutated"
    assert (
        get_governance_origin_provenance_record(record_id)["source_rule_id"]
        == "human_sovereignty"
    )

    section_name = REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES[0]
    section = get_governance_origin_provenance_section(section_name)
    section["section_status"] = "mutated"
    assert (
        get_governance_origin_provenance_section(section_name)[
            "section_status"
        ]
        == "pass"
    )

    contract_name = REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES[0]
    contract = get_governance_origin_provenance_contract(contract_name)
    contract["contract_status"] = "mutated"
    assert (
        get_governance_origin_provenance_contract(contract_name)[
            "contract_status"
        ]
        == "pass"
    )

    check_name = REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES[0]
    check = get_governance_origin_provenance_check(check_name)
    check["check_status"] = "mutated"
    assert get_governance_origin_provenance_check(check_name)[
        "check_status"
    ] == "pass"


def test_unknown_getters_return_blocked_style_results():
    assert get_governance_origin_provenance_record("unknown")[
        "provenance_record_status"
    ] == "blocked"
    assert get_governance_origin_provenance_section("unknown")[
        "section_status"
    ] == "blocked"
    assert get_governance_origin_provenance_contract("unknown")[
        "contract_status"
    ] == "blocked"
    assert get_governance_origin_provenance_check("unknown")[
        "check_status"
    ] == "blocked"


def test_all_sections_contracts_and_checks_pass(ledger):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in ledger["origin_provenance_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in ledger["origin_provenance_contracts"]
    )
    assert all(
        check["check_status"] == "pass" and check["blocking_reasons"] == []
        for check in ledger["origin_provenance_checks"]
    )


def test_all_safety_fields_are_false(ledger):
    _assert_all_safety_false(ledger)


def test_inactive_surface_statuses_and_flags(ledger):
    expected_false_fields = (
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
        "hidden_execution_allowed",
        "unapproved_mutation_allowed",
        "memory_graph_mutation_allowed_without_gate",
    )
    for field_name in expected_false_fields:
        assert ledger[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite_floats(ledger):
    first = governance_origin_provenance_ledger_to_json(ledger)
    second = governance_origin_provenance_ledger_to_json(
        build_governance_origin_provenance_ledger()
    )

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == ledger
    _assert_mapping_keys_are_strings(json.loads(first))
    with pytest.raises(ValueError):
        governance_origin_provenance_ledger_to_json({"bad": math.nan})


def test_deterministic_ledger_hash_is_stable(ledger):
    repeated = build_governance_origin_provenance_ledger()
    assert (
        ledger["deterministic_origin_provenance_ledger_hash"]
        == repeated["deterministic_origin_provenance_ledger_hash"]
    )
    assert len(ledger["deterministic_origin_provenance_ledger_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "origin_provenance_records",
            lambda value: value[0].__setitem__("rule_origin_reason", "changed"),
        ),
        (
            "origin_provenance_sections",
            lambda value: value[0].__setitem__(
                "origin_provenance_notes",
                "changed",
            ),
        ),
        (
            "origin_provenance_contracts",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "origin_provenance_checks",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "origin_provenance_summary",
            lambda value: value.__setitem__("summary_status", "changed"),
        ),
    ),
)
def test_ledger_hash_changes_when_governance_data_changes(
    ledger,
    field_name,
    mutator,
):
    mutated = deepcopy(ledger)
    mutator(mutated[field_name])

    assert _origin_provenance_ledger_hash(mutated) != ledger[
        "deterministic_origin_provenance_ledger_hash"
    ]


def test_record_and_rule_source_hashes_are_stable(ledger):
    repeated = build_governance_origin_provenance_ledger()
    repeated_records = {
        record["provenance_record_id"]: record
        for record in repeated["origin_provenance_records"]
    }
    for record in ledger["origin_provenance_records"]:
        repeated_record = repeated_records[record["provenance_record_id"]]
        assert (
            record["provenance_record_hash"]
            == repeated_record["provenance_record_hash"]
        )
        assert record["rule_source_hash"] == repeated_record["rule_source_hash"]


def test_no_sensitive_terms_leak(ledger):
    _assert_no_sensitive_terms(
        {
            "records": ledger["origin_provenance_records"],
            "sections": ledger["origin_provenance_sections"],
            "contracts": ledger["origin_provenance_contracts"],
            "checks": ledger["origin_provenance_checks"],
            "summary": ledger["origin_provenance_summary"],
            "json": governance_origin_provenance_ledger_to_json(ledger),
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
