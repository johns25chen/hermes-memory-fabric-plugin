"""R8 operator-only security intake and minimized output boundary."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping


SCHEMA_NAME = "GOVERNED-MEMORY-SECURITY-DECISION-ENVELOPE"
CONTRACT_VERSION = "1.3"
LEGACY_OPERATION = "R7_PROJECT_CONTINUITY"
OBSERVATION_OPERATION = "R7_REAL_USE_OBSERVATION_VALIDATION"
OPERATIONS = frozenset({LEGACY_OPERATION, OBSERVATION_OPERATION})
MEASUREMENT_SCOPES = frozenset(
    {
        "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL",
        "NEW-WINDOW-HANDOFF-TO-VERIFIED-TERMINAL-STATE",
    }
)

_REAL_USE_SNAPSHOT_FIELDS = frozenset(
    {
        "task_completed",
        "state_traceable",
        "human_correction_count",
        "recovery_time_seconds",
        "governance_burden_worthwhile",
        "baseline_available",
        "baseline_human_correction_count",
        "baseline_recovery_time_seconds",
    }
)
_ASSESSMENT_FIELDS = frozenset(
    {
        "assessment_status",
        "baseline_available",
        "task_completion",
        "state_traceability",
        "reduced_human_correction",
        "shortened_recovery_time",
        "governance_burden_worthwhile",
        "benefit_inference_allowed",
    }
)
_PROVENANCE_FIELDS = frozenset(
    {
        "task_completed_source",
        "state_traceable_source",
        "human_correction_count_source",
        "recovery_time_seconds_source",
        "governance_burden_worthwhile_source",
        "baseline_source",
        "measurement_scope",
    }
)
_SAFE_R7_STATUS_VALUES = frozenset(
    {"complete-terminal-non-applied-revocation"}
)
_COMMON_BOOLEAN_FIELDS = frozenset(
    {
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
    }
)

_REQUEST_REFERENCE = re.compile(r"^r8-request:[0-9a-f]{32}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_COMMON_FIELDS = frozenset(
    {
        "schema_name",
        "version",
        "operation",
        "request_reference",
        "payload_binding_sha256",
        "project_id",
        "namespace",
        "operator_role",
        "requested_effect",
        "security_classification",
        "security_classification_source",
        "source_trust",
        "source_lineage_class",
        "human_decision",
        "authority_attestation",
    }
)
_ATTESTED_FIELDS = _COMMON_FIELDS - {"authority_attestation"}
_ATTESTATION_FIELDS = _ATTESTED_FIELDS | {
    "attestation_type",
    "attestation_version",
    "attested",
}
_FIXED_VALUES = {
    "schema_name": SCHEMA_NAME,
    "version": CONTRACT_VERSION,
    "project_id": "CIVILIZATION-CORE",
    "namespace": "R7_PROJECT_CONTINUITY",
    "operator_role": "FOUNDER-OPERATOR",
    "requested_effect": "READ_ONLY_NON_PERSISTENT_TERMINAL_ASSESSMENT",
    "security_classification_source": "CALLER_DECLARATION",
}


class R8StructuralError(ValueError):
    """A fixed-code structural rejection for which no receipt is permitted."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class SecurityDecision:
    disposition: str
    code: str
    receipt: dict[str, Any]


def parse_strict_json_object(value: Any, *, field: str) -> dict[str, Any]:
    """Parse a duplicate-free, finite JSON object without numeric coercion."""

    if not isinstance(value, str) or not value.strip():
        raise R8StructuralError(f"{field}_missing_or_blank")

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise R8StructuralError(f"{field}_duplicate_key")
            result[key] = item
        return result

    def reject_constant(_value: str) -> None:
        raise R8StructuralError(f"{field}_non_finite_number")

    try:
        parsed = json.loads(
            value,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except R8StructuralError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError):
        raise R8StructuralError(f"{field}_malformed") from None
    if not isinstance(parsed, dict):
        raise R8StructuralError(f"{field}_not_object")
    return parsed


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError):
        raise R8StructuralError("payload_not_canonicalizable") from None


def canonical_payload_binding_sha256(payload: Mapping[str, Any]) -> str:
    if not isinstance(payload, Mapping):
        raise R8StructuralError("payload_not_object")
    return hashlib.sha256(canonical_json_bytes(dict(payload))).hexdigest()


def build_legacy_payload(args: Mapping[str, Any], candidate: Mapping[str, Any], real_use: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "operation": LEGACY_OPERATION,
        "project_id": args.get("project_id"),
        "operator": args.get("operator"),
        "query": args.get("query"),
        "candidate": deepcopy(dict(candidate)),
        "real_use_result_snapshot": deepcopy(dict(real_use)) if real_use is not None else None,
        "outcome": args.get("outcome"),
        "rationale": args.get("rationale"),
        "corrected_outcome": args.get("corrected_outcome"),
        "correction_rationale": args.get("correction_rationale"),
        "revocation_rationale": args.get("revocation_rationale"),
        "input_classification": args.get("input_classification"),
        "confirm_human_review": args.get("confirm_human_review"),
        "confirm_scope_check": args.get("confirm_scope_check"),
        "confirm_correction": args.get("confirm_correction"),
        "confirm_revocation": args.get("confirm_revocation"),
        "confirm_no_apply": args.get("confirm_no_apply"),
    }


def build_observation_payload(args: Mapping[str, Any], observation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "operation": OBSERVATION_OPERATION,
        "project_id": args.get("project_id"),
        "operator": args.get("operator"),
        "observation": deepcopy(dict(observation)),
        "confirm_real_use_observation": args.get("confirm_real_use_observation"),
    }


def evaluate_security_envelope(
    envelope: Mapping[str, Any],
    *,
    selected_operation: str,
    payload: Mapping[str, Any],
    input_classification: Any,
    measurement_scope: Any = None,
    baseline_available: Any = None,
) -> SecurityDecision:
    """Validate structure and return one deterministic policy decision."""

    source = _validate_envelope_structure(envelope, selected_operation)
    request_reference = source["request_reference"]
    code = _runtime_policy_code(
        source,
        selected_operation=selected_operation,
        payload=payload,
        input_classification=input_classification,
        measurement_scope=measurement_scope,
        baseline_available=baseline_available,
    )
    disposition, code = _policy_result(source, code)
    receipt = _build_receipt(
        request_reference=request_reference,
        operation=source["operation"],
        disposition=disposition,
        code=code,
    )
    return SecurityDecision(disposition, code, receipt)


def structural_error_output(error: R8StructuralError) -> dict[str, str]:
    return {"code": error.code, "disposition": "BLOCK"}


def policy_error_output(decision: SecurityDecision) -> dict[str, str]:
    return {
        "code": decision.code,
        "disposition": decision.disposition,
        "receipt_id": decision.receipt["receipt_id"],
    }


def minimized_operator_projection(
    decision: SecurityDecision,
    downstream: Mapping[str, Any],
    *,
    selected_operation: str,
    measurement_scope: str | None = None,
    baseline_measurement_scope: str | None = None,
) -> dict[str, Any]:
    result = {
        "security_decision": {
            "code": decision.code,
            "disposition": decision.disposition,
        },
        "sanitized_receipt": deepcopy(decision.receipt),
    }
    status = downstream.get("status")
    if isinstance(status, str) and status in _SAFE_R7_STATUS_VALUES:
        result["status"] = status
    for field in _COMMON_BOOLEAN_FIELDS:
        value = downstream.get(field)
        if type(value) is bool:
            result[field] = value
    if selected_operation == OBSERVATION_OPERATION:
        snapshot = _project_real_use_snapshot(
            downstream.get("real_use_result_snapshot")
        )
        if snapshot is not None:
            result["real_use_snapshot"] = snapshot
        assessment = _project_value_signal_assessment(
            downstream.get("value_signal_assessment")
        )
        if assessment is not None:
            result["assessment"] = assessment
        provenance = _project_observation_provenance(
            downstream.get("observation_provenance")
        )
        if provenance is not None:
            result["provenance"] = provenance
        result["benefit_inference_allowed"] = False
        result["measurement_scope"] = measurement_scope
        result["baseline_measurement_scope"] = baseline_measurement_scope
    return result


def _project_real_use_snapshot(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    result: dict[str, Any] = {}
    for field in _REAL_USE_SNAPSHOT_FIELDS:
        if field not in value:
            continue
        item = value.get(field)
        if field in {
            "task_completed",
            "state_traceable",
            "governance_burden_worthwhile",
            "baseline_available",
        }:
            if type(item) is bool:
                result[field] = item
        elif field in {
            "human_correction_count",
            "baseline_human_correction_count",
        }:
            if type(item) is int and item >= 0:
                result[field] = item
        elif (
            type(item) in {int, float}
            and item >= 0
            and not isinstance(item, bool)
            and item not in {float("inf"), float("-inf")}
            and item == item
        ):
            result[field] = item
    return result


def _project_value_signal_assessment(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    result: dict[str, Any] = {}
    for field in _ASSESSMENT_FIELDS:
        if field not in value:
            continue
        item = value.get(field)
        if field == "assessment_status":
            if isinstance(item, str) and item in {
                "validated",
                "baseline-unavailable",
            }:
                result[field] = item
        elif field in {"reduced_human_correction", "shortened_recovery_time"}:
            if item is None or type(item) is bool:
                result[field] = item
        elif field == "benefit_inference_allowed":
            if item is False:
                result[field] = False
        elif type(item) is bool:
            result[field] = item
    return result


def _project_observation_provenance(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    allowed_values = {
        "task_completed_source": frozenset({"terminal-workflow-result"}),
        "state_traceable_source": frozenset({"validated-workflow-lineage"}),
        "human_correction_count_source": frozenset(
            {"caller-observed-measurement"}
        ),
        "recovery_time_seconds_source": frozenset(
            {"caller-observed-measurement"}
        ),
        "governance_burden_worthwhile_source": frozenset(
            {"human-owner-explicit"}
        ),
        "baseline_source": frozenset(
            {"caller-provided-real-use-data", "unavailable"}
        ),
        "measurement_scope": MEASUREMENT_SCOPES,
    }
    result: dict[str, Any] = {}
    for field in _PROVENANCE_FIELDS:
        if field not in value:
            continue
        item = value.get(field)
        if isinstance(item, str) and item in allowed_values[field]:
            result[field] = item
    return result


def _validate_envelope_structure(
    envelope: Mapping[str, Any], selected_operation: str
) -> dict[str, Any]:
    if not isinstance(envelope, Mapping):
        raise R8StructuralError("security_envelope_not_object")
    source = dict(envelope)
    allowed = set(_COMMON_FIELDS)
    if selected_operation == OBSERVATION_OPERATION:
        allowed.update({"measurement_scope", "baseline_measurement_scope"})
    missing = allowed - set(source)
    if missing:
        raise R8StructuralError("security_envelope_missing_fields")
    for field in _COMMON_FIELDS - {"authority_attestation"}:
        value = source.get(field)
        if not isinstance(value, str) or not value.strip():
            raise R8StructuralError("security_envelope_field_invalid")
    if not _REQUEST_REFERENCE.fullmatch(source["request_reference"]):
        raise R8StructuralError("request_reference_invalid")
    if not _DIGEST.fullmatch(source["payload_binding_sha256"]):
        raise R8StructuralError("payload_binding_sha256_invalid")
    if selected_operation == OBSERVATION_OPERATION:
        if not isinstance(source.get("measurement_scope"), str) or not source[
            "measurement_scope"
        ].strip():
            raise R8StructuralError("measurement_scope_invalid")
        baseline_scope = source.get("baseline_measurement_scope")
        if baseline_scope is not None and (
            not isinstance(baseline_scope, str) or not baseline_scope.strip()
        ):
            raise R8StructuralError("baseline_measurement_scope_invalid")
    attestation = source.get("authority_attestation")
    if not isinstance(attestation, dict):
        raise R8StructuralError("authority_attestation_invalid")
    if set(attestation) != set(_ATTESTATION_FIELDS):
        raise R8StructuralError("authority_attestation_field_set_invalid")
    for field in _ATTESTED_FIELDS | {"attestation_type", "attestation_version"}:
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise R8StructuralError("authority_attestation_field_invalid")
    if type(attestation.get("attested")) is not bool:
        raise R8StructuralError("authority_attestation_attested_invalid")
    return source


def _runtime_policy_code(
    source: Mapping[str, Any],
    *,
    selected_operation: str,
    payload: Mapping[str, Any],
    input_classification: Any,
    measurement_scope: Any,
    baseline_available: Any,
) -> str:
    if set(source) != set(_COMMON_FIELDS) | (
        {"measurement_scope", "baseline_measurement_scope"}
        if selected_operation == OBSERVATION_OPERATION
        else set()
    ):
        return "route_field_set_mismatch"
    if source.get("operation") != selected_operation:
        return "operation_route_mismatch"
    for field, expected in _FIXED_VALUES.items():
        if source.get(field) != expected:
            return f"{field}_mismatch"
    attestation = source["authority_attestation"]
    if (
        attestation.get("attestation_type") != "CALLER_AUTHORITY_ATTESTATION"
        or attestation.get("attestation_version") != CONTRACT_VERSION
        or attestation.get("attested") is not True
        or any(attestation.get(field) != source.get(field) for field in _ATTESTED_FIELDS)
    ):
        return "authority_attestation_mismatch"
    if source.get("payload_binding_sha256") != canonical_payload_binding_sha256(payload):
        return "payload_binding_mismatch"
    if source.get("security_classification") != input_classification:
        return "security_classification_binding_mismatch"
    if selected_operation == OBSERVATION_OPERATION:
        scope = source.get("measurement_scope")
        baseline_scope = source.get("baseline_measurement_scope")
        if scope not in MEASUREMENT_SCOPES or scope != measurement_scope:
            return "measurement_scope_binding_mismatch"
        if baseline_available is True:
            if baseline_scope not in MEASUREMENT_SCOPES or baseline_scope != scope:
                return "baseline_measurement_scope_binding_mismatch"
        elif baseline_available is False:
            if baseline_scope is not None:
                return "baseline_measurement_scope_binding_mismatch"
        else:
            return "baseline_available_invalid"
    return "security_policy_evaluated"


def _policy_result(source: Mapping[str, Any], code: str) -> tuple[str, str]:
    if code != "security_policy_evaluated":
        return "BLOCK", code
    classification = source.get("security_classification")
    if classification == "SENSITIVE":
        return "BLOCK", "sensitive_classification_blocked"
    human = source.get("human_decision")
    if human == "DENY_EXECUTION":
        return "BLOCK", "human_execution_denied"
    if classification not in {"SYNTHETIC", "NON_SENSITIVE"}:
        return "BLOCK", "unsupported_security_classification"
    source_pair = (source.get("source_trust"), source.get("source_lineage_class"))
    if source_pair == ("UNKNOWN", "UNKNOWN"):
        return "BLOCK", "unknown_source_blocked"
    if source_pair not in {
        ("LOCAL_CALLER_PROVIDED", "CALLER_SUBMISSION"),
        ("LOCAL_PROVIDER_DERIVED", "LOCAL_PROVIDER_OUTPUT"),
        ("EXTERNAL_FEDERATED", "EXTERNAL_FEDERATED_INPUT"),
    }:
        return "BLOCK", "source_pair_mismatch"
    if human == "REQUEST_REVIEW":
        return "REVIEW", "human_review_required"
    if human != "APPROVE_READ_ONLY_EXECUTION":
        return "BLOCK", "unsupported_human_decision"
    if source_pair == ("LOCAL_PROVIDER_DERIVED", "LOCAL_PROVIDER_OUTPUT"):
        return "REVIEW", "provider_source_review_required"
    if source_pair == ("EXTERNAL_FEDERATED", "EXTERNAL_FEDERATED_INPUT"):
        return "REVIEW", "federated_source_review_required"
    return "ALLOW", "security_policy_allowed"


def _build_receipt(
    *, request_reference: str, operation: Any, disposition: str, code: str
) -> dict[str, Any]:
    safe_operation = operation if operation in OPERATIONS else "UNSUPPORTED"
    safe_code = code if code in _STABLE_POLICY_CODES else "unsupported_policy_value"
    body = {
        "schema_name": "R8-SANITIZED-SECURITY-RECEIPT",
        "version": CONTRACT_VERSION,
        "operation": safe_operation,
        "disposition": disposition,
        "code": safe_code,
    }
    receipt_hash = hashlib.sha256(canonical_json_bytes(body)).hexdigest()
    return {
        **body,
        "receipt_id": f"r8-receipt:{request_reference[-8:]}:{receipt_hash[:24]}",
        "authenticated": False,
        "encrypted": False,
        "replay_protected": False,
        "tamper_protected": False,
    }


_STABLE_POLICY_CODES = frozenset(
    {
        "security_policy_evaluated",
        "route_field_set_mismatch",
        "operation_route_mismatch",
        "schema_name_mismatch",
        "version_mismatch",
        "project_id_mismatch",
        "namespace_mismatch",
        "operator_role_mismatch",
        "requested_effect_mismatch",
        "security_classification_source_mismatch",
        "authority_attestation_mismatch",
        "payload_binding_mismatch",
        "security_classification_binding_mismatch",
        "measurement_scope_binding_mismatch",
        "baseline_measurement_scope_binding_mismatch",
        "baseline_available_invalid",
        "sensitive_classification_blocked",
        "unsupported_security_classification",
        "provider_source_review_required",
        "federated_source_review_required",
        "unknown_source_blocked",
        "source_pair_mismatch",
        "human_review_required",
        "human_execution_denied",
        "unsupported_human_decision",
        "security_policy_allowed",
    }
)


__all__ = [
    "CONTRACT_VERSION",
    "LEGACY_OPERATION",
    "MEASUREMENT_SCOPES",
    "OBSERVATION_OPERATION",
    "R8StructuralError",
    "SCHEMA_NAME",
    "SecurityDecision",
    "build_legacy_payload",
    "build_observation_payload",
    "canonical_json_bytes",
    "canonical_payload_binding_sha256",
    "evaluate_security_envelope",
    "minimized_operator_projection",
    "parse_strict_json_object",
    "policy_error_output",
    "structural_error_output",
]
