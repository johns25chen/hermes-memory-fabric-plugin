from __future__ import annotations

import hashlib
import json
from copy import deepcopy

import pytest

from hermes_memory_fabric.r8_security_governance import (
    LEGACY_OPERATION,
    MEASUREMENT_SCOPES,
    OBSERVATION_OPERATION,
    R8StructuralError,
    build_legacy_payload,
    canonical_payload_binding_sha256,
    evaluate_security_envelope,
    minimized_operator_projection,
    parse_strict_json_object,
)


def _payload(operation: str = LEGACY_OPERATION) -> dict[str, object]:
    return {"operation": operation, "items": [3, 1, 2], "large": 10**400}


def _envelope(
    payload: dict[str, object],
    *,
    operation: str = LEGACY_OPERATION,
    classification: str = "SYNTHETIC",
    source_trust: str = "LOCAL_CALLER_PROVIDED",
    lineage: str = "CALLER_SUBMISSION",
    human_decision: str = "APPROVE_READ_ONLY_EXECUTION",
    measurement_scope: str | None = None,
    baseline_measurement_scope: str | None = None,
) -> dict[str, object]:
    envelope: dict[str, object] = {
        "schema_name": "GOVERNED-MEMORY-SECURITY-DECISION-ENVELOPE",
        "version": "1.3",
        "operation": operation,
        "request_reference": "r8-request:0123456789abcdef0123456789abcdef",
        "payload_binding_sha256": canonical_payload_binding_sha256(payload),
        "project_id": "CIVILIZATION-CORE",
        "namespace": "R7_PROJECT_CONTINUITY",
        "operator_role": "FOUNDER-OPERATOR",
        "requested_effect": "READ_ONLY_NON_PERSISTENT_TERMINAL_ASSESSMENT",
        "security_classification": classification,
        "security_classification_source": "CALLER_DECLARATION",
        "source_trust": source_trust,
        "source_lineage_class": lineage,
        "human_decision": human_decision,
    }
    if operation == OBSERVATION_OPERATION:
        envelope["measurement_scope"] = measurement_scope
        envelope["baseline_measurement_scope"] = baseline_measurement_scope
    envelope["authority_attestation"] = {
        **envelope,
        "attestation_type": "CALLER_AUTHORITY_ATTESTATION",
        "attestation_version": "1.3",
        "attested": True,
    }
    attestation = envelope["authority_attestation"]
    assert isinstance(attestation, dict)
    attestation.pop("measurement_scope", None)
    attestation.pop("baseline_measurement_scope", None)
    return envelope


@pytest.mark.parametrize(
    ("raw", "code"),
    [
        ("", "payload_missing_or_blank"),
        ("[]", "payload_not_object"),
        ('{"a":1,"a":2}', "payload_duplicate_key"),
        ('{"a":NaN}', "payload_non_finite_number"),
        ('{"a":Infinity}', "payload_non_finite_number"),
        ('{"a":-Infinity}', "payload_non_finite_number"),
    ],
)
def test_strict_json_object_rejects_structural_invalidity(raw: str, code: str):
    with pytest.raises(R8StructuralError) as captured:
        parse_strict_json_object(raw, field="payload")
    assert captured.value.code == code


def test_payload_binding_preserves_large_integer_list_order_and_unicode_form():
    composed = {"operation": LEGACY_OPERATION, "n": 10**400, "v": [1, 2], "u": "é"}
    decomposed = {"operation": LEGACY_OPERATION, "n": 10**400, "v": [2, 1], "u": "e\u0301"}
    expected = hashlib.sha256(
        json.dumps(
            composed,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    assert canonical_payload_binding_sha256(composed) == expected
    assert canonical_payload_binding_sha256(composed) != (
        canonical_payload_binding_sha256(decomposed)
    )
    parsed = parse_strict_json_object(json.dumps(composed), field="payload")
    assert parsed["n"] == 10**400


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("request_reference", "r8-request:ABC", "request_reference_invalid"),
        ("payload_binding_sha256", "0" * 63, "payload_binding_sha256_invalid"),
        ("payload_binding_sha256", "G" * 64, "payload_binding_sha256_invalid"),
    ],
)
def test_reference_and_digest_format_are_structural(field: str, value: str, code: str):
    payload = _payload()
    envelope = _envelope(payload)
    envelope[field] = value
    with pytest.raises(R8StructuralError) as captured:
        evaluate_security_envelope(
            envelope,
            selected_operation=LEGACY_OPERATION,
            payload=payload,
            input_classification="SYNTHETIC",
        )
    assert captured.value.code == code


def test_both_operations_allow_and_route_mismatch_blocks_with_receipt():
    legacy = _payload()
    assert evaluate_security_envelope(
        _envelope(legacy),
        selected_operation=LEGACY_OPERATION,
        payload=legacy,
        input_classification="SYNTHETIC",
    ).disposition == "ALLOW"

    observation = _payload(OBSERVATION_OPERATION)
    scope = "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
    decision = evaluate_security_envelope(
        _envelope(
            observation,
            operation=OBSERVATION_OPERATION,
            measurement_scope=scope,
            baseline_measurement_scope=scope,
        ),
        selected_operation=OBSERVATION_OPERATION,
        payload=observation,
        input_classification="SYNTHETIC",
        measurement_scope=scope,
        baseline_available=True,
    )
    assert decision.disposition == "ALLOW"

    mismatch = _envelope(legacy)
    mismatch["operation"] = OBSERVATION_OPERATION
    decision = evaluate_security_envelope(
        mismatch,
        selected_operation=LEGACY_OPERATION,
        payload=legacy,
        input_classification="SYNTHETIC",
    )
    assert (decision.disposition, decision.code) == (
        "BLOCK",
        "operation_route_mismatch",
    )
    assert decision.receipt["receipt_id"].startswith("r8-receipt:89abcdef:")


def test_classification_binding_attestation_and_digest_mismatch_block():
    payload = _payload()
    for mutate, code in (
        (
            lambda value: (
                value.update(security_classification="NON_SENSITIVE"),
                value["authority_attestation"].update(
                    security_classification="NON_SENSITIVE"
                ),
            ),
            "security_classification_binding_mismatch",
        ),
        (lambda value: value["authority_attestation"].update(attested=False), "authority_attestation_mismatch"),
        (lambda value: value.update(payload_binding_sha256="f" * 64), "authority_attestation_mismatch"),
    ):
        envelope = _envelope(payload)
        mutate(envelope)
        decision = evaluate_security_envelope(
            envelope,
            selected_operation=LEGACY_OPERATION,
            payload=payload,
            input_classification="SYNTHETIC",
        )
        assert decision.disposition == "BLOCK"
        assert decision.code == code

    envelope = _envelope(payload)
    envelope["payload_binding_sha256"] = "f" * 64
    envelope["authority_attestation"]["payload_binding_sha256"] = "f" * 64
    decision = evaluate_security_envelope(
        envelope,
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    assert decision.code == "payload_binding_mismatch"


def test_matching_sensitive_classification_is_policy_block_with_sanitized_receipt():
    payload = _payload()
    envelope = _envelope(payload, classification="SENSITIVE")
    decision = evaluate_security_envelope(
        envelope,
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SENSITIVE",
    )

    assert (decision.disposition, decision.code) == (
        "BLOCK",
        "sensitive_classification_blocked",
    )
    assert decision.receipt["receipt_id"].startswith("r8-receipt:89abcdef:")
    rendered = json.dumps(decision.receipt, sort_keys=True)
    for forbidden in ("payload", "digest", "candidate", "query", "rationale", envelope["payload_binding_sha256"]):
        assert str(forbidden) not in rendered


@pytest.mark.parametrize(
    ("trust", "lineage", "disposition"),
    [
        ("LOCAL_CALLER_PROVIDED", "CALLER_SUBMISSION", "ALLOW"),
        ("LOCAL_PROVIDER_DERIVED", "LOCAL_PROVIDER_OUTPUT", "REVIEW"),
        ("EXTERNAL_FEDERATED", "EXTERNAL_FEDERATED_INPUT", "REVIEW"),
        ("UNKNOWN", "UNKNOWN", "BLOCK"),
        ("LOCAL_CALLER_PROVIDED", "LOCAL_PROVIDER_OUTPUT", "BLOCK"),
    ],
)
def test_all_source_pairs(trust: str, lineage: str, disposition: str):
    payload = _payload()
    decision = evaluate_security_envelope(
        _envelope(payload, source_trust=trust, lineage=lineage),
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    assert decision.disposition == disposition


@pytest.mark.parametrize(
    ("human", "disposition"),
    [
        ("APPROVE_READ_ONLY_EXECUTION", "ALLOW"),
        ("REQUEST_REVIEW", "REVIEW"),
        ("DENY_EXECUTION", "BLOCK"),
        ("UNSUPPORTED", "BLOCK"),
    ],
)
def test_human_decision_mapping(human: str, disposition: str):
    payload = _payload()
    decision = evaluate_security_envelope(
        _envelope(payload, human_decision=human),
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    assert decision.disposition == disposition


@pytest.mark.parametrize(
    ("human", "trust", "lineage", "expected"),
    [
        (
            "DENY_EXECUTION",
            "LOCAL_CALLER_PROVIDED",
            "CALLER_SUBMISSION",
            ("BLOCK", "human_execution_denied"),
        ),
        (
            "DENY_EXECUTION",
            "LOCAL_PROVIDER_DERIVED",
            "LOCAL_PROVIDER_OUTPUT",
            ("BLOCK", "human_execution_denied"),
        ),
        (
            "DENY_EXECUTION",
            "EXTERNAL_FEDERATED",
            "EXTERNAL_FEDERATED_INPUT",
            ("BLOCK", "human_execution_denied"),
        ),
        (
            "REQUEST_REVIEW",
            "LOCAL_CALLER_PROVIDED",
            "CALLER_SUBMISSION",
            ("REVIEW", "human_review_required"),
        ),
        (
            "REQUEST_REVIEW",
            "LOCAL_PROVIDER_DERIVED",
            "LOCAL_PROVIDER_OUTPUT",
            ("REVIEW", "human_review_required"),
        ),
        (
            "REQUEST_REVIEW",
            "EXTERNAL_FEDERATED",
            "EXTERNAL_FEDERATED_INPUT",
            ("REVIEW", "human_review_required"),
        ),
        (
            "APPROVE_READ_ONLY_EXECUTION",
            "LOCAL_PROVIDER_DERIVED",
            "LOCAL_PROVIDER_OUTPUT",
            ("REVIEW", "provider_source_review_required"),
        ),
        (
            "APPROVE_READ_ONLY_EXECUTION",
            "EXTERNAL_FEDERATED",
            "EXTERNAL_FEDERATED_INPUT",
            ("REVIEW", "federated_source_review_required"),
        ),
        (
            "APPROVE_READ_ONLY_EXECUTION",
            "UNKNOWN",
            "UNKNOWN",
            ("BLOCK", "unknown_source_blocked"),
        ),
        (
            "APPROVE_READ_ONLY_EXECUTION",
            "LOCAL_CALLER_PROVIDED",
            "LOCAL_PROVIDER_OUTPUT",
            ("BLOCK", "source_pair_mismatch"),
        ),
    ],
)
def test_human_decision_and_source_precedence(
    human: str,
    trust: str,
    lineage: str,
    expected: tuple[str, str],
):
    payload = _payload()
    decision = evaluate_security_envelope(
        _envelope(
            payload,
            human_decision=human,
            source_trust=trust,
            lineage=lineage,
        ),
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    assert (decision.disposition, decision.code) == expected


@pytest.mark.parametrize("scope", sorted(MEASUREMENT_SCOPES))
@pytest.mark.parametrize("baseline_available", [True, False])
def test_measurement_scope_and_baseline_binding(scope: str, baseline_available: bool):
    payload = _payload(OBSERVATION_OPERATION)
    baseline_scope = scope if baseline_available else None
    decision = evaluate_security_envelope(
        _envelope(
            payload,
            operation=OBSERVATION_OPERATION,
            measurement_scope=scope,
            baseline_measurement_scope=baseline_scope,
        ),
        selected_operation=OBSERVATION_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
        measurement_scope=scope,
        baseline_available=baseline_available,
    )
    assert decision.disposition == "ALLOW"


def test_legacy_scope_fields_are_policy_block_with_receipt():
    payload = _payload()
    envelope = _envelope(payload)
    envelope["measurement_scope"] = next(iter(MEASUREMENT_SCOPES))
    decision = evaluate_security_envelope(
        envelope,
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    assert decision.code == "route_field_set_mismatch"
    assert decision.receipt


def test_receipt_is_deterministic_sanitized_and_projection_is_minimized():
    payload = _payload()
    envelope = _envelope(payload)
    first = evaluate_security_envelope(
        envelope,
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )
    second = evaluate_security_envelope(
        deepcopy(envelope),
        selected_operation=LEGACY_OPERATION,
        payload=deepcopy(payload),
        input_classification="SYNTHETIC",
    )
    assert first.receipt == second.receipt
    rendered = json.dumps(first.receipt, sort_keys=True)
    for forbidden in ("candidate", "query", "rationale", envelope["payload_binding_sha256"]):
        assert str(forbidden) not in rendered
    projection = minimized_operator_projection(
        first,
        {
            "status": "complete-terminal-non-applied-revocation",
            "terminal": True,
            "non_applied": True,
            "non_persisted": True,
            "continuation_authorized": False,
            "candidate_snapshot": {"secret": "candidate"},
        },
        selected_operation=LEGACY_OPERATION,
    )
    assert projection["terminal"] is True
    assert "candidate_snapshot" not in projection
    assert "payload_binding_sha256" not in json.dumps(projection)


def test_observation_projection_uses_fixed_recursive_safe_allowlists():
    payload = _payload(OBSERVATION_OPERATION)
    scope = "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
    decision = evaluate_security_envelope(
        _envelope(
            payload,
            operation=OBSERVATION_OPERATION,
            measurement_scope=scope,
            baseline_measurement_scope=None,
        ),
        selected_operation=OBSERVATION_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
        measurement_scope=scope,
        baseline_available=False,
    )
    injected = {
        "candidate": "candidate-secret-value",
        "query": "query-secret-value",
        "rationale": "rationale-secret-value",
        "payload_binding_sha256": "digest-secret-value",
        "secret": "plain-secret-value",
        "unknown_future_field": "future-secret-value",
        "nested_attack": {
            "candidate": "nested-candidate-secret",
            "query": "nested-query-secret",
            "rationale": "nested-rationale-secret",
            "payload_binding_sha256": "nested-digest-secret",
            "secret": "nested-plain-secret",
            "unknown_future_field": "nested-future-secret",
        },
    }
    downstream = {
        "real_use_result_snapshot": {
            "task_completed": True,
            "state_traceable": True,
            "human_correction_count": 0,
            "recovery_time_seconds": 10,
            "governance_burden_worthwhile": True,
            "baseline_available": False,
            **injected,
        },
        "value_signal_assessment": {
            "assessment_status": "baseline-unavailable",
            "baseline_available": False,
            "task_completion": True,
            "state_traceability": True,
            "reduced_human_correction": None,
            "shortened_recovery_time": None,
            "governance_burden_worthwhile": True,
            "benefit_inference_allowed": False,
            **injected,
        },
        "observation_provenance": {
            "task_completed_source": "terminal-workflow-result",
            "state_traceable_source": "validated-workflow-lineage",
            "human_correction_count_source": "caller-observed-measurement",
            "recovery_time_seconds_source": "caller-observed-measurement",
            "governance_burden_worthwhile_source": "human-owner-explicit",
            "baseline_source": "unavailable",
            "measurement_scope": scope,
            **injected,
        },
    }
    projection = minimized_operator_projection(
        decision,
        downstream,
        selected_operation=OBSERVATION_OPERATION,
        measurement_scope=scope,
        baseline_measurement_scope=None,
    )
    assert projection["real_use_snapshot"] == {
        "task_completed": True,
        "state_traceable": True,
        "human_correction_count": 0,
        "recovery_time_seconds": 10,
        "governance_burden_worthwhile": True,
        "baseline_available": False,
    }
    assert projection["assessment"] == {
        "assessment_status": "baseline-unavailable",
        "baseline_available": False,
        "task_completion": True,
        "state_traceability": True,
        "reduced_human_correction": None,
        "shortened_recovery_time": None,
        "governance_burden_worthwhile": True,
        "benefit_inference_allowed": False,
    }
    assert projection["provenance"] == {
        "task_completed_source": "terminal-workflow-result",
        "state_traceable_source": "validated-workflow-lineage",
        "human_correction_count_source": "caller-observed-measurement",
        "recovery_time_seconds_source": "caller-observed-measurement",
        "governance_burden_worthwhile_source": "human-owner-explicit",
        "baseline_source": "unavailable",
        "measurement_scope": scope,
    }
    rendered = json.dumps(projection, sort_keys=True)
    for key, value in injected.items():
        assert key not in rendered
        if isinstance(value, str):
            assert value not in rendered
        else:
            for nested_key, nested_value in value.items():
                assert nested_key not in rendered
                assert nested_value not in rendered


@pytest.mark.parametrize(
    "wrong_status",
    [
        "",
        "secret",
        {"candidate": "secret"},
        {"query": "secret"},
        {"rationale": "secret"},
        {"payload_binding_sha256": "secret"},
        {"unknown_future_field": "secret"},
        ["secret"],
        1,
        0,
        True,
        False,
        None,
    ],
)
def test_common_projection_status_uses_fixed_allowlist(wrong_status):
    payload = _payload()
    decision = evaluate_security_envelope(
        _envelope(payload),
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )

    rejected = minimized_operator_projection(
        decision,
        {"status": wrong_status},
        selected_operation=LEGACY_OPERATION,
    )
    accepted = minimized_operator_projection(
        decision,
        {"status": "complete-terminal-non-applied-revocation"},
        selected_operation=LEGACY_OPERATION,
    )

    assert "status" not in rejected
    assert accepted["status"] == "complete-terminal-non-applied-revocation"
    rendered = json.dumps(rejected, sort_keys=True)
    for forbidden in (
        "candidate",
        "query",
        "rationale",
        "payload_binding_sha256",
        "secret",
        "unknown_future_field",
    ):
        assert forbidden not in rendered


@pytest.mark.parametrize(
    "field",
    [
        "terminal",
        "non_authoritative",
        "non_applied",
        "non_persisted",
        "continuation_authorized",
        "automatic_collection",
        "automatic_write",
        "automatic_approval",
        "automatic_adoption",
        "automatic_execution",
        "automatic_continuation",
    ],
)
@pytest.mark.parametrize(
    "wrong_value",
    [
        {"candidate": "secret"},
        {"query": "secret"},
        {"rationale": "secret"},
        {"payload_binding_sha256": "secret"},
        {"unknown_future_field": "secret"},
        ["secret"],
        "secret",
        1,
        0,
        None,
    ],
)
def test_common_projection_boolean_fields_require_exact_bool(field, wrong_value):
    payload = _payload()
    decision = evaluate_security_envelope(
        _envelope(payload),
        selected_operation=LEGACY_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
    )

    rejected = minimized_operator_projection(
        decision,
        {field: wrong_value},
        selected_operation=LEGACY_OPERATION,
    )
    accepted_true = minimized_operator_projection(
        decision,
        {field: True},
        selected_operation=LEGACY_OPERATION,
    )
    accepted_false = minimized_operator_projection(
        decision,
        {field: False},
        selected_operation=LEGACY_OPERATION,
    )

    assert field not in rejected
    assert accepted_true[field] is True
    assert accepted_false[field] is False
    rendered = json.dumps(rejected, sort_keys=True)
    for forbidden in (
        "candidate",
        "query",
        "rationale",
        "payload_binding_sha256",
        "secret",
        "unknown_future_field",
    ):
        assert forbidden not in rendered


def test_observation_projection_omits_wrong_types_instead_of_passing_them_through():
    payload = _payload(OBSERVATION_OPERATION)
    scope = "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
    decision = evaluate_security_envelope(
        _envelope(
            payload,
            operation=OBSERVATION_OPERATION,
            measurement_scope=scope,
            baseline_measurement_scope=None,
        ),
        selected_operation=OBSERVATION_OPERATION,
        payload=payload,
        input_classification="SYNTHETIC",
        measurement_scope=scope,
        baseline_available=False,
    )
    projection = minimized_operator_projection(
        decision,
        {
            "real_use_result_snapshot": {"task_completed": {"secret": "x"}},
            "value_signal_assessment": {
                "assessment_status": {"secret": "y"},
                "benefit_inference_allowed": {"secret": "z"},
            },
            "observation_provenance": {
                "measurement_scope": {"secret": "scope"}
            },
        },
        selected_operation=OBSERVATION_OPERATION,
        measurement_scope=scope,
        baseline_measurement_scope=None,
    )
    assert projection["real_use_snapshot"] == {}
    assert projection["assessment"] == {}
    assert projection["provenance"] == {}
    assert projection["benefit_inference_allowed"] is False
    assert "secret" not in json.dumps(projection)


def test_structural_failure_has_no_receipt():
    payload = _payload()
    envelope = _envelope(payload)
    del envelope["request_reference"]
    with pytest.raises(R8StructuralError) as captured:
        evaluate_security_envelope(
            envelope,
            selected_operation=LEGACY_OPERATION,
            payload=payload,
            input_classification="SYNTHETIC",
        )
    assert "receipt" not in str(captured.value)


def test_build_legacy_payload_contains_exact_operation_literal():
    payload = build_legacy_payload({}, {}, None)
    assert payload["operation"] == LEGACY_OPERATION
    assert len(canonical_payload_binding_sha256(payload)) == 64
