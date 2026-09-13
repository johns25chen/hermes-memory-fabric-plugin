"""Deterministic, read-only provider candidate admission boundary."""

from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from copy import deepcopy
from typing import Any, Iterable, Mapping


PROVIDER_FEDERATION_CONTRACT_VERSION = "1.0.0"
CANONICAL_JSON_VERSION = "canonical-json-v1"
READ_CANDIDATE = "READ_CANDIDATE"
SOURCE_CLASSES = frozenset(
    {"LOCAL_CALLER", "LOCAL_PROVIDER", "EXTERNAL_FEDERATED_CANDIDATE"}
)
ENVELOPE_FIELDS = frozenset(
    {
        "provider_id",
        "source_class",
        "source_instance",
        "candidate_id",
        "project",
        "workspace",
        "namespace",
        "capabilities",
        "payload_digest",
        "request_id",
    }
)
SCOPE_FIELDS = ("project", "workspace", "namespace")
REASON_ORDER = (
    "BLOCK_MALFORMED_ENVELOPE",
    "BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED",
    "BLOCK_SCOPE_REQUIRED",
    "BLOCK_SCOPE_MISMATCH",
    "BLOCK_CAPABILITY_REQUIRED",
    "BLOCK_CAPABILITY_UNKNOWN",
    "BLOCK_CAPABILITY_ESCALATION",
    "BLOCK_PAYLOAD_DIGEST_MISMATCH",
    "BLOCK_COMPOUND_ID_CONFLICT",
    "BLOCK_SOURCE_CLASS_DOWNGRADE",
    "BLOCK_REQUEST_ID_DUPLICATE_IN_BATCH",
    "BLOCK_INTERNAL_INVARIANT",
    "REVIEW_EXTERNAL_IDENTITY_UNAUTHENTICATED",
)

_PROVIDER_ID_RE = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}\Z")
_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}\Z")
_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")


class CanonicalPayloadError(ValueError):
    """The payload cannot be represented by the contract canonical JSON form."""


def canonical_payload_digest(payload: Any) -> str:
    encoded = _canonical_json_bytes(payload)
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def admit_candidate_batch(
    *,
    request_scope: Mapping[str, Any],
    provider_registry_snapshot: Mapping[str, Any],
    items: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Admit one immutable batch without network, persistence, or global state."""

    scope = deepcopy(dict(request_scope)) if isinstance(request_scope, Mapping) else {}
    registry = (
        deepcopy(dict(provider_registry_snapshot))
        if isinstance(provider_registry_snapshot, Mapping)
        else {}
    )
    try:
        copied_items = deepcopy(list(items))
    except (TypeError, ValueError):
        copied_items = []
    scope_valid = _valid_scope(scope)
    scope_digest = _safe_digest(scope)
    registry_digest = _safe_digest(registry)
    evaluations = [
        _evaluate_item(
            item,
            scope=scope,
            scope_valid=scope_valid,
            registry=registry,
            scope_digest=scope_digest,
            registry_digest=registry_digest,
        )
        for item in copied_items
    ]
    _apply_batch_conflicts(evaluations)

    receipts: list[dict[str, Any]] = []
    allowed: list[dict[str, Any]] = []
    for evaluation in evaluations:
        reasons = _ordered_reasons(evaluation["reasons"])
        decision = "BLOCK" if any(reason.startswith("BLOCK_") for reason in reasons) else (
            "REVIEW" if any(reason.startswith("REVIEW_") for reason in reasons) else "ALLOW"
        )
        receipt = dict(evaluation["receipt"])
        receipt["decision"] = decision
        receipt["reason_codes"] = reasons
        receipts.append(receipt)
        if decision == "ALLOW":
            allowed.append(deepcopy(evaluation["payload"]))

    return {
        "contract_version": PROVIDER_FEDERATION_CONTRACT_VERSION,
        "canonical_json_version": CANONICAL_JSON_VERSION,
        "receipts": receipts,
        "allowed_candidates": allowed,
        "historical_replay_protection": False,
    }


def _evaluate_item(
    item: Any,
    *,
    scope: Mapping[str, Any],
    scope_valid: bool,
    registry: Mapping[str, Any],
    scope_digest: str,
    registry_digest: str,
) -> dict[str, Any]:
    reasons: set[str] = set()
    envelope: Mapping[str, Any] = {}
    payload: Any = None
    if not isinstance(item, Mapping) or set(item) != {"envelope", "payload"}:
        reasons.add("BLOCK_MALFORMED_ENVELOPE")
    else:
        raw_envelope = item.get("envelope")
        if isinstance(raw_envelope, Mapping):
            envelope = raw_envelope
        else:
            reasons.add("BLOCK_MALFORMED_ENVELOPE")
        payload = item.get("payload")

    if not _valid_envelope(envelope):
        reasons.add("BLOCK_MALFORMED_ENVELOPE")
    if not scope_valid:
        reasons.add("BLOCK_SCOPE_REQUIRED")
    elif any(envelope.get(field) != scope[field] for field in SCOPE_FIELDS):
        reasons.add("BLOCK_SCOPE_MISMATCH")

    provider_id = envelope.get("provider_id")
    descriptor = registry.get(provider_id) if isinstance(provider_id, str) else None
    if not _valid_descriptor(descriptor) or not descriptor.get("enabled"):
        reasons.add("BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED")
    else:
        source_class = envelope.get("source_class")
        if source_class not in descriptor["source_classes"]:
            reasons.add("BLOCK_SOURCE_CLASS_DOWNGRADE")
        capabilities = envelope.get("capabilities")
        if capabilities != [READ_CANDIDATE]:
            if not capabilities or READ_CANDIDATE not in capabilities:
                reasons.add("BLOCK_CAPABILITY_REQUIRED")
            if isinstance(capabilities, list) and any(
                capability != READ_CANDIDATE for capability in capabilities
            ):
                reasons.add("BLOCK_CAPABILITY_UNKNOWN")
        if isinstance(capabilities, list) and any(
            capability not in descriptor["capabilities"] for capability in capabilities
        ):
            reasons.add("BLOCK_CAPABILITY_ESCALATION")

        if source_class == "EXTERNAL_FEDERATED_CANDIDATE":
            if descriptor["trusted_ingestion"] or descriptor["review_only"]:
                reasons.add("REVIEW_EXTERNAL_IDENTITY_UNAUTHENTICATED")
            else:
                reasons.add("BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED")
        elif descriptor["review_only"]:
            reasons.add("BLOCK_SOURCE_CLASS_DOWNGRADE")

    try:
        actual_digest = canonical_payload_digest(payload)
    except (CanonicalPayloadError, TypeError, ValueError):
        actual_digest = ""
        reasons.add("BLOCK_PAYLOAD_DIGEST_MISMATCH")
    if envelope.get("payload_digest") != actual_digest:
        reasons.add("BLOCK_PAYLOAD_DIGEST_MISMATCH")

    receipt = {
        "contract_version": PROVIDER_FEDERATION_CONTRACT_VERSION,
        "canonical_json_version": CANONICAL_JSON_VERSION,
        "provider_id": envelope.get("provider_id") if _valid_provider_id(envelope.get("provider_id")) else None,
        "source_class": envelope.get("source_class") if _valid_source_class(envelope.get("source_class")) else None,
        "source_instance": envelope.get("source_instance") if _valid_identifier(envelope.get("source_instance")) else None,
        "candidate_id": envelope.get("candidate_id") if _valid_identifier(envelope.get("candidate_id")) else None,
        "payload_digest": envelope.get("payload_digest") if _valid_payload_digest(envelope.get("payload_digest")) else None,
        "request_id": envelope.get("request_id") if _valid_request_id(envelope.get("request_id")) else None,
        "request_scope_digest": scope_digest,
        "provider_registry_digest": registry_digest,
    }
    return {
        "envelope": envelope,
        "payload": payload,
        "actual_digest": actual_digest,
        "reasons": reasons,
        "receipt": receipt,
    }


def _apply_batch_conflicts(evaluations: list[dict[str, Any]]) -> None:
    request_positions: dict[str, list[int]] = {}
    identity_positions: dict[tuple[str, str, str], list[int]] = {}
    for index, evaluation in enumerate(evaluations):
        envelope = evaluation["envelope"]
        request_id = envelope.get("request_id")
        if isinstance(request_id, str):
            request_positions.setdefault(request_id, []).append(index)
        identity = _compound_identity(envelope)
        if identity is not None:
            identity_positions.setdefault(identity, []).append(index)

    for positions in request_positions.values():
        if len(positions) > 1:
            for index in positions:
                evaluations[index]["reasons"].add("BLOCK_REQUEST_ID_DUPLICATE_IN_BATCH")
    for positions in identity_positions.values():
        bindings = {
            _identity_binding(evaluations[index]["envelope"], evaluations[index]["actual_digest"])
            for index in positions
        }
        if len(bindings) > 1:
            for index in positions:
                evaluations[index]["reasons"].add("BLOCK_COMPOUND_ID_CONFLICT")


def _valid_envelope(envelope: Mapping[str, Any]) -> bool:
    if set(envelope) != ENVELOPE_FIELDS:
        return False
    if not _valid_provider_id(envelope.get("provider_id")):
        return False
    if not _valid_source_class(envelope.get("source_class")):
        return False
    if not _valid_identifier(envelope.get("source_instance")):
        return False
    if not _valid_identifier(envelope.get("candidate_id")):
        return False
    if not _valid_scope(envelope):
        return False
    capabilities = envelope.get("capabilities")
    if (
        not isinstance(capabilities, list)
        or any(not isinstance(value, str) for value in capabilities)
        or capabilities != sorted(set(capabilities))
    ):
        return False
    if not _valid_payload_digest(envelope.get("payload_digest")):
        return False
    return _valid_request_id(envelope.get("request_id"))


def _valid_provider_id(value: Any) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 128 and _PROVIDER_ID_RE.fullmatch(value) is not None


def _valid_source_class(value: Any) -> bool:
    return isinstance(value, str) and value in SOURCE_CLASSES


def _valid_identifier(value: Any) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 256 and _IDENTIFIER_RE.fullmatch(value) is not None


def _valid_payload_digest(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and _DIGEST_RE.fullmatch(value) is not None


def _valid_request_id(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 36:
        return False
    try:
        return str(uuid.UUID(value)) == value
    except ValueError:
        return False


def _valid_scope(scope: Mapping[str, Any]) -> bool:
    if not isinstance(scope, Mapping) or any(field not in scope for field in SCOPE_FIELDS):
        return False
    project, workspace, namespace = (scope.get(field) for field in SCOPE_FIELDS)
    return (
        _canonical_text(project, 256)
        and _canonical_text(workspace, 1024)
        and _canonical_workspace(workspace)
        and _canonical_text(namespace, 256)
    )


def _canonical_text(value: Any, maximum: int) -> bool:
    return isinstance(value, str) and 0 < len(value) <= maximum and value == value.strip()


def _canonical_workspace(value: str) -> bool:
    if not value.startswith("/") or "//" in value or "\\" in value or "\x00" in value:
        return False
    return all(segment not in {".", ".."} for segment in value.split("/"))


def _valid_descriptor(descriptor: Any) -> bool:
    if not isinstance(descriptor, Mapping):
        return False
    source_classes = descriptor.get("source_classes")
    capabilities = descriptor.get("capabilities")
    return (
        set(descriptor)
        == {"enabled", "source_classes", "capabilities", "review_only", "trusted_ingestion"}
        and isinstance(descriptor.get("enabled"), bool)
        and isinstance(descriptor.get("review_only"), bool)
        and isinstance(descriptor.get("trusted_ingestion"), bool)
        and isinstance(source_classes, list)
        and all(isinstance(value, str) for value in source_classes)
        and source_classes == sorted(set(source_classes))
        and all(value in SOURCE_CLASSES for value in source_classes)
        and isinstance(capabilities, list)
        and all(isinstance(value, str) for value in capabilities)
        and capabilities == sorted(set(capabilities))
    )


def _compound_identity(envelope: Mapping[str, Any]) -> tuple[str, str, str] | None:
    values = tuple(envelope.get(field) for field in ("provider_id", "source_instance", "candidate_id"))
    return values if all(isinstance(value, str) for value in values) else None


def _identity_binding(envelope: Mapping[str, Any], actual_digest: str) -> tuple[Any, ...]:
    return (
        actual_digest,
        envelope.get("source_class"),
        *(envelope.get(field) for field in SCOPE_FIELDS),
        tuple(envelope.get("capabilities", [])) if isinstance(envelope.get("capabilities"), list) else (),
    )


def _ordered_reasons(reasons: set[str]) -> list[str]:
    return [reason for reason in REASON_ORDER if reason in reasons]


def _safe_digest(value: Any) -> str:
    try:
        return canonical_payload_digest(value)
    except (CanonicalPayloadError, TypeError, ValueError):
        return "sha256:" + ("0" * 64)


def _canonical_json_bytes(value: Any) -> bytes:
    _validate_json_value(value)
    try:
        serialized = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalPayloadError("payload_not_canonical_json") from exc
    return serialized.encode("utf-8")


def _validate_json_value(value: Any) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalPayloadError("payload_non_finite_number")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item)
        return
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise CanonicalPayloadError("payload_non_string_object_key")
        for item in value.values():
            _validate_json_value(item)
        return
    raise CanonicalPayloadError("payload_non_json_type")


__all__ = [
    "CANONICAL_JSON_VERSION",
    "CanonicalPayloadError",
    "PROVIDER_FEDERATION_CONTRACT_VERSION",
    "admit_candidate_batch",
    "canonical_payload_digest",
]
