from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_root_governance_conflict_resolver import (
    AUTONOMOUS_AUTHORITY_STATUS,
    AWAKENING_CLAIM_STATUS,
    COMMON_DISABLED_FLAGS,
    CONFLICT_ENFORCEMENT_STATUS,
    CONFLICT_MUTATION_STATUS,
    CONFLICT_RUNTIME_STATUS,
    GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_HASH_ALGORITHM,
    GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_SCHEMA_VERSION,
    GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_TYPE,
    GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_VERSION,
    LAYER_15_ACTIVE_STATUS,
    LEGAL_SUBJECT_CLAIM_STATUS,
    LIFE_CLAIM_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    PERSONHOOD_CLAIM_STATUS,
    RELIGIOUS_OBJECT_CLAIM_STATUS,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES,
    ROOT_GOVERNANCE_CONFLICT_MODE,
    ROOT_GOVERNANCE_CONFLICT_RESOLVER_ACTIVE_STATUS,
    ROOT_GOVERNANCE_CONFLICT_RESOLVER_MODE,
    ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE,
    ROOT_GOVERNANCE_CONFLICT_RESOLVER_STATUS,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_GRAPH_STATUS,
    SOURCE_PROVENANCE_RUNTIME_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_5_STATUS,
    V6_6_HANDOFF_STATUS,
    _conflict_boundary_hash,
    _conflict_record_hash,
    _root_governance_conflict_resolver_hash,
    build_governance_root_governance_conflict_resolver,
    get_governance_root_governance_conflict_check,
    get_governance_root_governance_conflict_contract,
    get_governance_root_governance_conflict_record,
    get_governance_root_governance_conflict_section,
    governance_root_governance_conflict_resolver_to_json,
    list_governance_root_governance_conflict_check_names,
    list_governance_root_governance_conflict_contract_names,
    list_governance_root_governance_conflict_record_ids,
    list_governance_root_governance_conflict_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_root_governance_conflict_resolver.py"
)

EXPECTED_CONFLICT_RECORDS = (
    (
        "human_sovereignty_vs_source_rule_conflict",
        "Human Sovereignty Vs Source Rule Conflict",
        "human_sovereignty_prevails",
    ),
    (
        "source_constitution_vs_invariant_conflict",
        "Source Constitution Vs Invariant Conflict",
        "block_without_human_review",
    ),
    (
        "origin_provenance_vs_identity_boundary_conflict",
        "Origin Provenance Vs Identity Boundary Conflict",
        "preserve_origin_traceability",
    ),
    (
        "identity_boundary_vs_autonomous_authority_conflict",
        "Identity Boundary Vs Autonomous Authority Conflict",
        "preserve_identity_boundary",
    ),
    (
        "invariant_matrix_vs_direct_mutation_conflict",
        "Invariant Matrix Vs Direct Mutation Conflict",
        "preserve_source_memory_invariant",
    ),
    (
        "source_rule_vs_hidden_execution_conflict",
        "Source Rule Vs Hidden Execution Conflict",
        "block_hidden_execution",
    ),
    (
        "source_graph_mutation_conflict",
        "Source Graph Mutation Conflict",
        "block_source_graph_mutation",
    ),
    (
        "memory_graph_mutation_without_gate_conflict",
        "Memory Graph Mutation Without Gate Conflict",
        "block_memory_graph_mutation",
    ),
    (
        "durable_write_without_gate_conflict",
        "Durable Write Without Gate Conflict",
        "block_durable_write",
    ),
    (
        "external_network_call_conflict",
        "External Network Call Conflict",
        "block_external_network_call",
    ),
    (
        "ledger_write_without_boundary_conflict",
        "Ledger Write Without Boundary Conflict",
        "block_ledger_write",
    ),
    (
        "methodology_runtime_conflict",
        "Methodology Runtime Conflict",
        "block_methodology_runtime",
    ),
    (
        "self_evolution_runtime_conflict",
        "Self Evolution Runtime Conflict",
        "block_self_evolution_runtime",
    ),
    (
        "personhood_life_awakening_claim_conflict",
        "Personhood Life Awakening Claim Conflict",
        "block_personhood_life_awakening_claim",
    ),
    (
        "legal_religious_status_claim_conflict",
        "Legal Religious Status Claim Conflict",
        "block_legal_religious_status_claim",
    ),
    (
        "unresolved_root_conflict_handoff_conflict",
        "Unresolved Root Conflict Handoff Conflict",
        "block_and_handoff_to_human_review",
    ),
)

EXPECTED_RECORD_IDS = tuple(record_id for record_id, _, _ in EXPECTED_CONFLICT_RECORDS)

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
    "root_governance_conflict_resolver_active",
    "root_governance_conflict_resolved",
    "root_governance_conflict_resolution_executed",
    "conflict_runtime_created",
    "conflict_enforcement_runtime_created",
    "conflict_self_repair_created",
    "conflict_runtime_activated",
    "conflict_enforcement_runtime_activated",
    "autonomous_mutation_resolver_created",
    "active_conflict_execution_runtime_created",
    "source_rule_mutation_engine_created",
    "source_graph_creation_performed",
    "source_graph_mutation_performed",
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
    "review_notification_sent",
    "approval_notification_sent",
    "execution_authorization_created",
    "authorization_surface_created",
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
def resolver() -> dict[str, object]:
    return build_governance_root_governance_conflict_resolver()


def _record_by_id(resolver: dict[str, object], record_id: str) -> dict[str, object]:
    for record in resolver["root_governance_conflict_records"]:
        if record["conflict_record_id"] == record_id:
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


def test_constants_match_v6_5_contract():
    assert GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_VERSION == "6.6.0"
    assert GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_SCHEMA_VERSION == "6.6.0"
    assert (
        GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_TYPE
        == "governance_root_governance_conflict_resolver"
    )
    assert GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_HASH_ALGORITHM == "sha256"
    assert ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE == (
        "v6.5_root_governance_conflict_resolver"
    )
    assert ROOT_GOVERNANCE_CONFLICT_RESOLVER_MODE == (
        "root_governance_conflict_resolver_only"
    )
    assert ROOT_GOVERNANCE_CONFLICT_MODE == "metadata_only"
    assert ROOT_GOVERNANCE_CONFLICT_RESOLVER_STATUS == "resolver_candidate_only"
    assert ROOT_GOVERNANCE_CONFLICT_RESOLVER_ACTIVE_STATUS == "not_active"
    assert CONFLICT_RUNTIME_STATUS == "not_active"
    assert CONFLICT_ENFORCEMENT_STATUS == "not_active"
    assert CONFLICT_MUTATION_STATUS == "forbidden_without_human_review"
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
    assert V6_5_STATUS == "root_governance_conflict_resolver_only"
    assert V6_6_HANDOFF_STATUS == "ready_for_multi_cycle_continuity_protocol_design"


def test_resolver_shape_is_deterministic_and_passes(resolver):
    repeated = build_governance_root_governance_conflict_resolver()

    assert repeated == resolver
    assert resolver["version"] == "6.6.0"
    assert resolver["schema_version"] == "6.6.0"
    assert resolver["root_governance_conflict_resolver_status"] == "pass"
    assert (
        resolver["root_governance_conflict_resolver_stage"]
        == "v6.5_root_governance_conflict_resolver"
    )
    assert (
        resolver["root_governance_conflict_resolver_mode"]
        == "root_governance_conflict_resolver_only"
    )
    assert resolver["root_governance_conflict_mode"] == "metadata_only"
    assert (
        resolver["root_governance_conflict_resolver_candidate_status"]
        == "resolver_candidate_only"
    )
    assert resolver["root_governance_conflict_resolver_active_status"] == "not_active"
    assert resolver["conflict_runtime_status"] == "not_active"
    assert resolver["conflict_enforcement_status"] == "not_active"
    assert resolver["conflict_mutation_status"] == "forbidden_without_human_review"
    assert resolver["source_graph_status"] == "not_created"
    assert resolver["blocking_reasons"] == []
    assert resolver["handoff_status"] == (
        "ready_for_multi_cycle_continuity_protocol_design"
    )
    assert resolver["next_stage"] == "v6.6_multi_cycle_continuity_protocol"
    assert resolver["next_stage_title"] == "Multi-Cycle Continuity Protocol"


def test_upstream_v6_4_handoff_verification(resolver):
    assert resolver["upstream_source_memory_invariant_matrix_version"] == "6.6.0"
    assert resolver["upstream_source_memory_invariant_matrix_status"] == "pass"
    assert len(resolver["upstream_source_memory_invariant_matrix_hash"]) == 64
    assert resolver["upstream_handoff_status"] == (
        "ready_for_root_governance_conflict_resolver_design"
    )
    assert resolver["upstream_next_stage"] == (
        "v6.5_root_governance_conflict_resolver"
    )
    assert resolver["upstream_next_stage_title"] == "Root Governance Conflict Resolver"
    assert resolver["upstream_source_memory_invariant_record_count"] == 16
    assert (
        resolver[
            "upstream_source_memory_invariant_records_registered_metadata_only"
        ]
        is True
    )
    assert (
        resolver["upstream_source_memory_invariant_records_require_review"]
        is True
    )
    assert (
        resolver[
            "upstream_source_memory_invariant_records_disable_unsafe_surfaces"
        ]
        is True
    )
    assert resolver["upstream_safety_boundaries_clear"] is True
    repeated = build_governance_root_governance_conflict_resolver()
    assert (
        resolver["upstream_source_memory_invariant_matrix_hash"]
        == repeated["upstream_source_memory_invariant_matrix_hash"]
    )


def test_required_record_ids_are_stable_and_complete(resolver):
    assert REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS == EXPECTED_RECORD_IDS
    assert list_governance_root_governance_conflict_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert [
        record["conflict_record_id"]
        for record in resolver["root_governance_conflict_records"]
    ] == list(EXPECTED_RECORD_IDS)


def test_all_records_are_registered_metadata_only(resolver):
    for record in resolver["root_governance_conflict_records"]:
        assert record["conflict_record_status"] == "registered_metadata_only"
        assert record["required"] is True
        assert record["introduced_in_version"] == "6.5.0"
        assert (
            record["introduced_in_stage"]
            == "v6.5_root_governance_conflict_resolver"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert (
            record["inherited_from_stage"]
            == "v6.4_source_memory_invariant_matrix"
        )
        assert record["blocking_reasons"] == []


def test_all_records_have_conflict_metadata_and_hashes(resolver):
    repeated = build_governance_root_governance_conflict_resolver()
    repeated_by_id = {
        record["conflict_record_id"]: record
        for record in repeated["root_governance_conflict_records"]
    }

    for record in resolver["root_governance_conflict_records"]:
        assert record["conflict_statement"]
        assert record["conflict_trigger_scope"]
        assert record["protected_governance_scope"]
        assert record["forbidden_resolution_scope"]
        assert record["deterministic_resolution_disposition"]
        assert record["conflict_reason"]
        assert record["conflict_source_stage"]
        assert record["conflict_source_reference"]
        assert record["resolver_strength"] == "root_level_required"
        assert record["conflict_resolution_mode"] == (
            "metadata_only_block_and_handoff"
        )
        assert len(record["conflict_boundary_hash"]) == 64
        assert len(record["conflict_record_hash"]) == 64
        repeated_record = repeated_by_id[record["conflict_record_id"]]
        assert (
            record["conflict_boundary_hash"]
            == repeated_record["conflict_boundary_hash"]
            == _conflict_boundary_hash(record)
        )
        assert (
            record["conflict_record_hash"]
            == repeated_record["conflict_record_hash"]
            == _conflict_record_hash(record)
        )


def test_all_records_require_review_and_disable_mutation(resolver):
    for record in resolver["root_governance_conflict_records"]:
        assert record["human_review_required"] is True
        assert record["source_mutation_proposal_required"] is True
        assert record["invariant_validation_required"] is True
        assert record["audit_replay_required"] is True
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
        assert record["conflict_runtime_created"] is False
        assert record["conflict_enforcement_runtime_created"] is False
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


@pytest.mark.parametrize(
    ("record_id", "record_name", "disposition"),
    EXPECTED_CONFLICT_RECORDS,
)
def test_each_required_conflict_record(
    resolver,
    record_id,
    record_name,
    disposition,
):
    record = _record_by_id(resolver, record_id)

    assert record["conflict_name"] == record_name
    assert record["conflict_record_id"] == record_id
    assert record["conflict_record_status"] == "registered_metadata_only"
    assert record["deterministic_resolution_disposition"] == disposition
    assert record["conflict_statement"]
    assert record["conflict_trigger_scope"]
    assert record["protected_governance_scope"]
    assert record["forbidden_resolution_scope"]
    assert len(record["conflict_boundary_hash"]) == 64
    assert len(record["conflict_record_hash"]) == 64


def test_section_contract_and_check_names_are_stable_and_complete(resolver):
    assert list_governance_root_governance_conflict_section_names() == list(
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES
    )
    assert list_governance_root_governance_conflict_contract_names() == list(
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES
    )
    assert list_governance_root_governance_conflict_check_names() == list(
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES
    )
    assert [
        section["section_name"]
        for section in resolver["root_governance_conflict_sections"]
    ] == list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES)
    assert [
        contract["contract_name"]
        for contract in resolver["root_governance_conflict_contracts"]
    ] == list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES)
    assert [
        check["check_name"] for check in resolver["root_governance_conflict_checks"]
    ] == list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES)


def test_getters_return_detached_copies():
    record_id = REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS[0]
    record = get_governance_root_governance_conflict_record(record_id)
    record["conflict_name"] = "mutated"
    assert get_governance_root_governance_conflict_record(record_id)[
        "conflict_name"
    ] == "Human Sovereignty Vs Source Rule Conflict"

    section_name = REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES[0]
    section = get_governance_root_governance_conflict_section(section_name)
    section["section_status"] = "mutated"
    assert get_governance_root_governance_conflict_section(section_name)[
        "section_status"
    ] == "pass"

    contract_name = REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES[0]
    contract = get_governance_root_governance_conflict_contract(contract_name)
    contract["contract_status"] = "mutated"
    assert get_governance_root_governance_conflict_contract(contract_name)[
        "contract_status"
    ] == "pass"

    check_name = REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES[0]
    check = get_governance_root_governance_conflict_check(check_name)
    check["check_status"] = "mutated"
    assert get_governance_root_governance_conflict_check(check_name)[
        "check_status"
    ] == "pass"


def test_unknown_getters_return_blocked_style_results():
    assert get_governance_root_governance_conflict_record("unknown")[
        "conflict_record_status"
    ] == "blocked"
    assert get_governance_root_governance_conflict_section("unknown")[
        "section_status"
    ] == "blocked"
    assert get_governance_root_governance_conflict_contract("unknown")[
        "contract_status"
    ] == "blocked"
    assert get_governance_root_governance_conflict_check("unknown")[
        "check_status"
    ] == "blocked"


def test_all_sections_contracts_and_checks_pass(resolver):
    assert all(
        section["section_status"] == "pass"
        and section["blocking_reasons"] == []
        for section in resolver["root_governance_conflict_sections"]
    )
    assert all(
        contract["contract_status"] == "pass"
        and contract["blocking_reasons"] == []
        for contract in resolver["root_governance_conflict_contracts"]
    )
    assert all(
        check["check_status"] == "pass" and check["blocking_reasons"] == []
        for check in resolver["root_governance_conflict_checks"]
    )


def test_all_safety_fields_are_false(resolver):
    _assert_all_safety_false(resolver)


def test_inactive_runtime_identity_write_and_authority_flags(resolver):
    for field_name in EXPECTED_FALSE_FIELDS:
        assert resolver[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite_floats(resolver):
    first = governance_root_governance_conflict_resolver_to_json(resolver)
    second = governance_root_governance_conflict_resolver_to_json(
        build_governance_root_governance_conflict_resolver()
    )

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == resolver
    _assert_mapping_keys_are_strings(json.loads(first))
    with pytest.raises(ValueError):
        governance_root_governance_conflict_resolver_to_json({"bad": math.nan})


def test_deterministic_resolver_hash_is_stable(resolver):
    repeated = build_governance_root_governance_conflict_resolver()
    assert (
        resolver["deterministic_root_governance_conflict_resolver_hash"]
        == repeated["deterministic_root_governance_conflict_resolver_hash"]
    )
    assert len(resolver["deterministic_root_governance_conflict_resolver_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "root_governance_conflict_records",
            lambda value: value[0].__setitem__("conflict_statement", "changed"),
        ),
        (
            "root_governance_conflict_sections",
            lambda value: value[0].__setitem__(
                "root_governance_conflict_notes",
                "changed",
            ),
        ),
        (
            "root_governance_conflict_contracts",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "root_governance_conflict_checks",
            lambda value: value[0].__setitem__("observed", False),
        ),
        (
            "root_governance_conflict_summary",
            lambda value: value.__setitem__("summary_status", "changed"),
        ),
    ),
)
def test_resolver_hash_changes_when_governance_data_changes(
    resolver,
    field_name,
    mutator,
):
    mutated = deepcopy(resolver)
    mutator(mutated[field_name])

    assert _root_governance_conflict_resolver_hash(mutated) != resolver[
        "deterministic_root_governance_conflict_resolver_hash"
    ]


def test_conflict_hashes_are_stable(resolver):
    repeated = build_governance_root_governance_conflict_resolver()
    repeated_records = {
        record["conflict_record_id"]: record
        for record in repeated["root_governance_conflict_records"]
    }
    for record in resolver["root_governance_conflict_records"]:
        repeated_record = repeated_records[record["conflict_record_id"]]
        assert (
            record["conflict_boundary_hash"]
            == repeated_record["conflict_boundary_hash"]
            == _conflict_boundary_hash(record)
        )
        assert (
            record["conflict_record_hash"]
            == repeated_record["conflict_record_hash"]
            == _conflict_record_hash(record)
        )


def test_no_sensitive_terms_leak(resolver):
    _assert_no_sensitive_terms(
        {
            "records": resolver["root_governance_conflict_records"],
            "sections": resolver["root_governance_conflict_sections"],
            "contracts": resolver["root_governance_conflict_contracts"],
            "checks": resolver["root_governance_conflict_checks"],
            "summary": resolver["root_governance_conflict_summary"],
            "json": governance_root_governance_conflict_resolver_to_json(
                resolver
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
