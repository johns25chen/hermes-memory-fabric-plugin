from __future__ import annotations

import json
from copy import deepcopy

import pytest

from hermes_memory_fabric.provider_federation_boundary import (
    CanonicalPayloadError,
    PROVIDER_FEDERATION_CONTRACT_VERSION,
    admit_candidate_batch,
    canonical_payload_digest,
)


SCOPE = {
    "project": "hermes-memory-fabric",
    "workspace": "/workspace/hermes-memory-fabric",
    "namespace": "memory",
}


def _payload(candidate_id: str = "candidate-1", **overrides):
    payload = {"id": candidate_id, "content": "bounded candidate content"}
    payload.update(overrides)
    return payload


def _envelope(payload, **overrides):
    payload_digest = overrides.get("payload_digest")
    if payload_digest is None:
        payload_digest = canonical_payload_digest(payload)
    envelope = {
        "provider_id": "local-provider",
        "source_class": "LOCAL_PROVIDER",
        "source_instance": "configured:local-provider",
        "candidate_id": "candidate-1",
        **SCOPE,
        "capabilities": ["READ_CANDIDATE"],
        "payload_digest": payload_digest,
        "request_id": "00000000-0000-4000-8000-000000000001",
    }
    envelope.update(overrides)
    return envelope


def _registry(**descriptor_overrides):
    descriptor = {
        "enabled": True,
        "source_classes": ["LOCAL_PROVIDER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }
    descriptor.update(descriptor_overrides)
    return {"local-provider": descriptor}


def test_registered_local_provider_is_allowed_with_stable_minimal_receipt_and_copy():
    payload = _payload()
    envelope = _envelope(payload)
    registry = _registry()
    original_payload = deepcopy(payload)
    original_envelope = deepcopy(envelope)
    original_registry = deepcopy(registry)

    first = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=registry,
        items=[{"envelope": envelope, "payload": payload}],
    )
    second = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=registry,
        items=[{"envelope": envelope, "payload": payload}],
    )

    assert first == second
    assert first["contract_version"] == PROVIDER_FEDERATION_CONTRACT_VERSION == "1.0.0"
    assert first["receipts"][0]["decision"] == "ALLOW"
    assert first["receipts"][0]["reason_codes"] == []
    assert first["allowed_candidates"] == [payload]
    assert first["allowed_candidates"][0] is not payload
    assert "content" not in first["receipts"][0]
    assert payload == original_payload
    assert envelope == original_envelope
    assert registry == original_registry


def _decision(payload=None, envelope_overrides=None, registry=None, scope=None):
    payload = _payload() if payload is None else payload
    envelope = _envelope(payload, **(envelope_overrides or {}))
    return admit_candidate_batch(
        request_scope=SCOPE if scope is None else scope,
        provider_registry_snapshot=_registry() if registry is None else registry,
        items=[{"envelope": envelope, "payload": payload}],
    )["receipts"][0]


def test_local_caller_and_external_review_only_source_classes_are_distinct():
    local = _decision(
        envelope_overrides={"source_class": "LOCAL_CALLER"},
        registry=_registry(source_classes=["LOCAL_CALLER"]),
    )
    external = _decision(
        envelope_overrides={"source_class": "EXTERNAL_FEDERATED_CANDIDATE"},
        registry=_registry(
            source_classes=["EXTERNAL_FEDERATED_CANDIDATE"],
            review_only=True,
        ),
    )

    assert local["decision"] == "ALLOW"
    assert external["decision"] == "REVIEW"
    assert external["reason_codes"] == ["REVIEW_EXTERNAL_IDENTITY_UNAUTHENTICATED"]


@pytest.mark.parametrize(
    ("registry", "reason"),
    [
        ({}, "BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED"),
        (_registry(enabled=False), "BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED"),
        (
            _registry(
                source_classes=["EXTERNAL_FEDERATED_CANDIDATE"],
                review_only=False,
                trusted_ingestion=False,
            ),
            "BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED",
        ),
    ],
)
def test_unknown_disabled_or_untrusted_external_provider_is_blocked(registry, reason):
    overrides = {}
    if registry and registry["local-provider"]["source_classes"] == ["EXTERNAL_FEDERATED_CANDIDATE"]:
        overrides["source_class"] = "EXTERNAL_FEDERATED_CANDIDATE"
    receipt = _decision(envelope_overrides=overrides, registry=registry)

    assert receipt["decision"] == "BLOCK"
    assert reason in receipt["reason_codes"]


def test_payload_identity_claims_never_override_authoritative_envelope():
    payload = _payload(
        provider_id="evil-provider",
        source_class="EXTERNAL_FEDERATED_CANDIDATE",
        source_instance="evil:instance",
        candidate_id="evil-candidate",
        project="other",
        workspace="/other",
        namespace="other",
        capabilities=["WRITE_MEMORY"],
        request_id="ffffffff-ffff-4fff-8fff-ffffffffffff",
    )

    receipt = _decision(payload=payload)

    assert receipt["decision"] == "ALLOW"
    assert receipt["provider_id"] == "local-provider"
    assert receipt["candidate_id"] == "candidate-1"


@pytest.mark.parametrize("field", ["project", "workspace", "namespace"])
def test_each_scope_field_must_match_exactly(field):
    receipt = _decision(envelope_overrides={field: _envelope(_payload())[field] + "-other"})
    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_SCOPE_MISMATCH" in receipt["reason_codes"]


def test_missing_request_scope_blocks_instead_of_inheriting_payload_scope():
    receipt = _decision(scope={})
    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_SCOPE_REQUIRED" in receipt["reason_codes"]


@pytest.mark.parametrize(
    ("capabilities", "reason"),
    [
        ([], "BLOCK_CAPABILITY_REQUIRED"),
        (["WRITE_MEMORY"], "BLOCK_CAPABILITY_UNKNOWN"),
        (["READ_CANDIDATE", "WRITE_MEMORY"], "BLOCK_CAPABILITY_UNKNOWN"),
    ],
)
def test_capability_missing_unknown_or_escalated_is_blocked(capabilities, reason):
    receipt = _decision(envelope_overrides={"capabilities": capabilities})
    assert receipt["decision"] == "BLOCK"
    assert reason in receipt["reason_codes"]


def test_provider_capability_grant_cannot_be_escalated():
    receipt = _decision(registry=_registry(capabilities=[]))
    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_CAPABILITY_ESCALATION" in receipt["reason_codes"]


def test_digest_mismatch_and_non_json_payloads_block_fail_closed():
    mismatch = _decision(envelope_overrides={"payload_digest": "sha256:" + "0" * 64})
    non_json = _decision(
        payload={"bad": {1, 2}},
        envelope_overrides={"payload_digest": "sha256:" + "0" * 64},
    )

    assert mismatch["decision"] == "BLOCK"
    assert non_json["decision"] == "BLOCK"
    assert "BLOCK_PAYLOAD_DIGEST_MISMATCH" in mismatch["reason_codes"]
    assert "BLOCK_PAYLOAD_DIGEST_MISMATCH" in non_json["reason_codes"]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_payload_digest_rejects_nonfinite_numbers(value):
    with pytest.raises(CanonicalPayloadError, match="payload_non_finite_number"):
        canonical_payload_digest({"value": value})


def test_canonical_payload_digest_rejects_non_string_keys_and_is_order_stable():
    with pytest.raises(CanonicalPayloadError, match="payload_non_string_object_key"):
        canonical_payload_digest({1: "value"})
    assert canonical_payload_digest({"b": 2, "a": 1}) == canonical_payload_digest({"a": 1, "b": 2})


def test_batch_request_id_conflict_blocks_all_reuses():
    first_payload = _payload("first")
    second_payload = _payload("second")
    first = _envelope(first_payload, candidate_id="first")
    second = _envelope(second_payload, candidate_id="second", request_id=first["request_id"])

    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=_registry(),
        items=[{"envelope": first, "payload": first_payload}, {"envelope": second, "payload": second_payload}],
    )

    assert result["allowed_candidates"] == []
    assert all("BLOCK_REQUEST_ID_DUPLICATE_IN_BATCH" in receipt["reason_codes"] for receipt in result["receipts"])


def test_compound_identity_conflict_blocks_both_candidates():
    first_payload = _payload(content="first")
    second_payload = _payload(content="second")
    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=_registry(),
        items=[
            {"envelope": _envelope(first_payload), "payload": first_payload},
            {
                "envelope": _envelope(
                    second_payload,
                    request_id="00000000-0000-4000-8000-000000000002",
                ),
                "payload": second_payload,
            },
        ],
    )

    assert result["allowed_candidates"] == []
    assert all("BLOCK_COMPOUND_ID_CONFLICT" in receipt["reason_codes"] for receipt in result["receipts"])


def test_compound_identity_conflict_is_reached_with_stable_candidate_id():
    first_payload = _payload("stable-key", content="first")
    second_payload = _payload("stable-key", content="second")
    first = _envelope(first_payload, candidate_id="stable-key")
    second = _envelope(
        second_payload,
        candidate_id="stable-key",
        request_id="00000000-0000-4000-8000-000000000002",
    )
    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=_registry(),
        items=[
            {"envelope": first, "payload": first_payload},
            {"envelope": second, "payload": second_payload},
        ],
    )
    assert result["allowed_candidates"] == []
    assert all("BLOCK_COMPOUND_ID_CONFLICT" in receipt["reason_codes"] for receipt in result["receipts"])


def test_same_bare_id_from_different_compound_identities_does_not_collide():
    payload = _payload()
    second_envelope = _envelope(
        payload,
        provider_id="other-provider",
        source_instance="configured:other-provider",
        request_id="00000000-0000-4000-8000-000000000002",
    )
    registry = _registry()
    registry["other-provider"] = deepcopy(registry["local-provider"])

    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=registry,
        items=[
            {"envelope": _envelope(payload), "payload": payload},
            {"envelope": second_envelope, "payload": payload},
        ],
    )

    assert [receipt["decision"] for receipt in result["receipts"]] == ["ALLOW", "ALLOW"]
    assert len(result["allowed_candidates"]) == 2


def test_source_class_upgrade_or_downgrade_is_blocked():
    receipt = _decision(
        envelope_overrides={"source_class": "LOCAL_CALLER"},
        registry=_registry(source_classes=["EXTERNAL_FEDERATED_CANDIDATE"]),
    )
    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_SOURCE_CLASS_DOWNGRADE" in receipt["reason_codes"]


def test_malformed_envelope_unknown_fields_and_noncanonical_values_block_without_raising():
    payload = _payload()
    malformed = _envelope(payload)
    malformed["unknown"] = "value"
    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=_registry(),
        items=[{"envelope": malformed, "payload": payload}],
    )
    assert result["receipts"][0]["decision"] == "BLOCK"
    assert "BLOCK_MALFORMED_ENVELOPE" in result["receipts"][0]["reason_codes"]

    wrong_types = _envelope(payload, provider_id=7)
    registry = _registry()
    registry[7] = registry.pop("local-provider")
    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=registry,
        items=[{"envelope": wrong_types, "payload": payload}],
    )
    assert result["receipts"][0]["decision"] == "BLOCK"


def test_receipt_contains_only_bounded_metadata_and_no_historical_replay_claim():
    payload = _payload(content="SECRET-PAYLOAD-CONTENT")
    result = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=_registry(),
        items=[{"envelope": _envelope(payload), "payload": payload}],
    )
    serialized_receipts = repr(result["receipts"])
    assert "SECRET-PAYLOAD-CONTENT" not in serialized_receipts
    assert result["historical_replay_protection"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_id", "p" + ("a" * 127)),
        ("source_instance", "S" + ("a" * 255)),
        ("candidate_id", "C" + ("a" * 255)),
        ("payload_digest", "sha256:" + "b4c98897d0447d0f18cc7cd9349d34e336a1b7f35efda34263592f59969f3c0d"),
        ("request_id", "ffffffff-ffff-4fff-8fff-ffffffffffff"),
    ],
)
def test_receipt_preserves_valid_boundary_metadata(field, value):
    payload = _payload()
    registry = _registry()
    if field == "provider_id":
        registry[value] = registry.pop("local-provider")

    receipt = _decision(
        payload=payload,
        envelope_overrides={field: value},
        registry=registry,
    )

    assert receipt["decision"] == "ALLOW"
    assert receipt["reason_codes"] == []
    assert receipt[field] == value


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_id", "p" * 129),
        ("provider_id", "Uppercase-provider"),
        ("provider_id", 7),
        ("source_instance", "S" * 257),
        ("source_instance", "bad source instance"),
        ("source_instance", 7),
        ("candidate_id", "C" * 257),
        ("candidate_id", "bad candidate id"),
        ("candidate_id", 7),
        ("payload_digest", "sha256:" + ("0" * 65)),
        ("payload_digest", "sha256:" + ("G" * 64)),
        ("payload_digest", 7),
        ("request_id", "00000000-0000-4000-8000-000000000001x"),
        ("request_id", "AAAAAAAA-AAAA-4AAA-8AAA-AAAAAAAAAAAA"),
        ("request_id", 7),
    ],
)
def test_receipt_omits_invalid_metadata(field, value):
    receipt = _decision(envelope_overrides={field: value})
    serialized = json.dumps(receipt, sort_keys=True)

    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_MALFORMED_ENVELOPE" in receipt["reason_codes"]
    assert receipt[field] is None
    if isinstance(value, str):
        assert value not in serialized


def test_receipt_does_not_amplify_or_relocate_multiple_invalid_fields():
    marker = "R8-S3-IR-001-UNIQUE-MARKER"

    def evaluate(size):
        invalid = {
            "provider_id": marker + ("p" * size),
            "source_instance": marker + ("s" * size),
            "candidate_id": marker + ("c" * size),
            "payload_digest": marker + ("d" * size),
            "request_id": marker + ("r" * size),
        }
        original = deepcopy(invalid)
        receipt = _decision(envelope_overrides=invalid)
        assert invalid == original
        return receipt, json.dumps(receipt, sort_keys=True)

    short_receipt, short_serialized = evaluate(257)
    long_receipt, long_serialized = evaluate(4096)

    for receipt, serialized in (
        (short_receipt, short_serialized),
        (long_receipt, long_serialized),
    ):
        assert receipt["decision"] == "BLOCK"
        assert "BLOCK_MALFORMED_ENVELOPE" in receipt["reason_codes"]
        assert all(
            receipt[field] is None
            for field in (
                "provider_id",
                "source_instance",
                "candidate_id",
                "payload_digest",
                "request_id",
            )
        )
        assert marker not in serialized
        assert marker not in repr(receipt["reason_codes"])
        assert "detail" not in receipt

    assert len(long_serialized) == len(short_serialized)


def test_mapping_insertion_order_does_not_change_digest_or_receipt():
    first_payload = {"a": 1, "b": {"x": 2, "y": 3}}
    second_payload = {"b": {"y": 3, "x": 2}, "a": 1}
    first_registry = _registry()
    second_registry = {"local-provider": dict(reversed(list(first_registry["local-provider"].items())))}

    first = admit_candidate_batch(
        request_scope=SCOPE,
        provider_registry_snapshot=first_registry,
        items=[{"envelope": _envelope(first_payload), "payload": first_payload}],
    )
    second = admit_candidate_batch(
        request_scope=dict(reversed(list(SCOPE.items()))),
        provider_registry_snapshot=second_registry,
        items=[{"payload": second_payload, "envelope": _envelope(second_payload)}],
    )

    assert canonical_payload_digest(first_payload) == canonical_payload_digest(second_payload)
    assert first["receipts"] == second["receipts"]


def test_block_has_priority_over_external_review():
    payload = _payload(content="blocked external")
    receipt = _decision(
        payload=payload,
        envelope_overrides={
            "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
            "payload_digest": "sha256:" + "0" * 64,
        },
        registry=_registry(
            source_classes=["EXTERNAL_FEDERATED_CANDIDATE"],
            review_only=True,
        ),
    )

    assert receipt["decision"] == "BLOCK"
    assert receipt["reason_codes"] == [
        "BLOCK_PAYLOAD_DIGEST_MISMATCH",
        "REVIEW_EXTERNAL_IDENTITY_UNAUTHENTICATED",
    ]


@pytest.mark.parametrize("workspace", ["relative/path", "/a//b", "/a/../b", "/a/./b", "/a\\b"])
def test_workspace_must_be_canonical_absolute_identifier(workspace):
    receipt = _decision(envelope_overrides={"workspace": workspace})
    assert receipt["decision"] == "BLOCK"
    assert "BLOCK_MALFORMED_ENVELOPE" in receipt["reason_codes"]
