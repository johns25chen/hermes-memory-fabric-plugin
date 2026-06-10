#!/usr/bin/env python3
"""Smoke test for the final v2.x governed Star-Law boundary review gate."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal import (  # noqa: E402
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal,
)
from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate import (  # noqa: E402
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate,
)
from smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal import (  # noqa: E402
    _valid_audit_completion_attestation_completion_closure_boundary_review_gate_report,
)


LABEL = "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"


def _valid_v2_59_finalization_boundary_proposal_report() -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal(
        _valid_audit_completion_attestation_completion_closure_boundary_review_gate_report()
    )


def main() -> int:
    try:
        result = build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate(
            _valid_v2_59_finalization_boundary_proposal_report()
        )
        if (
            result.get("status")
            != "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready"
        ):
            raise AssertionError("status")
        for key, expected in REVIEW_GATE_FALSE_FLAGS.items():
            if result.get(key) is not expected:
                raise AssertionError(key)
        review_gate = result.get(
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"
        )
        if not isinstance(review_gate, dict):
            raise AssertionError("review_gate")
        for key, expected in REVIEW_OBJECT_FALSE_FLAGS.items():
            if review_gate.get(key) is not expected:
                raise AssertionError(f"review_gate_{key}")
        mapping = result.get("civilization_core_layer_mapping")
        if not isinstance(mapping, dict) or mapping.get("primary_layer") != "星律记忆":
            raise AssertionError("primary_layer")
        expected_chain = [f"v2.{minor}.0" for minor in range(9, 60)]
        if REVIEWED_CHAIN_VERSIONS != expected_chain:
            raise AssertionError("reviewed_chain_versions_constant")
        if result.get("reviewed_chain_versions") != expected_chain:
            raise AssertionError("reviewed_chain_versions")
        expected_star_hub_chain = [f"v2.{minor}.0" for minor in range(19, 60)]
        if REVIEWED_STAR_HUB_CHAIN_VERSIONS != expected_star_hub_chain:
            raise AssertionError("reviewed_star_hub_chain_versions_constant")
        if result.get("reviewed_star_hub_chain_versions") != expected_star_hub_chain:
            raise AssertionError("reviewed_star_hub_chain_versions")
        if (
            READY_NEXT_ALLOWED_STEP
            != "v3.0.0 Star-Soul Memory continuity boundary proposal"
            or result.get("next_allowed_step") != READY_NEXT_ALLOWED_STEP
        ):
            raise AssertionError("next_allowed_step")
        if result.get("enters_star_soul_layer") is not False:
            raise AssertionError("enters_star_soul_layer")
        if result.get("star_soul_transition_authorized") is not False:
            raise AssertionError("star_soul_transition_authorized")
        if result.get("v3_created") is not False:
            raise AssertionError("v3_created")
    except Exception as exc:
        print(f"{LABEL}=failed {exc}", file=sys.stderr)
        return 1

    print(f"{LABEL}=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
