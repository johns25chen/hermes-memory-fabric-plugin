#!/usr/bin/env python3
"""Smoke test for the governed audit completion attestation closure boundary review gate."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal import (  # noqa: E402
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal,
)
from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate import (  # noqa: E402
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate,
)
from smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal import (  # noqa: E402
    _valid_audit_completion_attestation_boundary_review_gate_report,
)


def _valid_audit_completion_attestation_closure_boundary_proposal_report() -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal(
        _valid_audit_completion_attestation_boundary_review_gate_report()
    )


def main() -> int:
    label = "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    try:
        result = build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate(
            _valid_audit_completion_attestation_closure_boundary_proposal_report()
        )
        if (
            result.get("status")
            != "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_ready"
        ):
            print(f"{label}=failed status", file=sys.stderr)
            return 1
        for key, expected in REVIEW_GATE_FALSE_FLAGS.items():
            if result.get(key) is not expected:
                print(f"{label}=failed {key}", file=sys.stderr)
                return 1
        review_gate = result.get(
            "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate",
            {},
        )
        if not isinstance(review_gate, dict):
            print(f"{label}=failed review_gate", file=sys.stderr)
            return 1
        for key, expected in REVIEW_OBJECT_FALSE_FLAGS.items():
            if review_gate.get(key) is not expected:
                print(f"{label}=failed review_gate_{key}", file=sys.stderr)
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if not isinstance(mapping, dict) or mapping.get("primary_layer") != "星律记忆":
            print(f"{label}=failed primary_layer", file=sys.stderr)
            return 1
        if result.get("reviewed_chain_versions") != REVIEWED_CHAIN_VERSIONS:
            print(f"{label}=failed reviewed_chain_versions", file=sys.stderr)
            return 1
        if (
            result.get("reviewed_star_hub_chain_versions")
            != REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ):
            print(f"{label}=failed reviewed_star_hub_chain_versions", file=sys.stderr)
            return 1
        if result.get("next_allowed_step") != READY_NEXT_ALLOWED_STEP:
            print(f"{label}=failed next_allowed_step", file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"{label}=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print(f"{label}=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
