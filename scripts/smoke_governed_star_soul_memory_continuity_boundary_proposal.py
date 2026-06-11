#!/usr/bin/env python3
"""Smoke test for the governed Star-Soul continuity boundary proposal."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate import (  # noqa: E402
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_proposal import (  # noqa: E402
    PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    build_governed_star_soul_memory_continuity_boundary_proposal,
)
from smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate import (  # noqa: E402
    _valid_v2_59_finalization_boundary_proposal_report,
)


LABEL = "governed_star_soul_memory_continuity_boundary_proposal"


def _valid_v2_60_star_law_review_gate_report() -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate(
        _valid_v2_59_finalization_boundary_proposal_report()
    )


def main() -> int:
    try:
        result = build_governed_star_soul_memory_continuity_boundary_proposal(
            _valid_v2_60_star_law_review_gate_report()
        )
        if (
            result.get("status")
            != "star_soul_memory_continuity_boundary_proposal_ready"
        ):
            raise AssertionError("status")
        for key, expected in PROPOSAL_FALSE_FLAGS.items():
            if result.get(key) is not expected:
                raise AssertionError(key)
        proposal = result.get(
            "star_soul_memory_continuity_boundary_proposal"
        )
        if not isinstance(proposal, dict):
            raise AssertionError("proposal")
        for key, expected in PROPOSAL_OBJECT_FALSE_FLAGS.items():
            if proposal.get(key) is not expected:
                raise AssertionError(f"proposal_{key}")
        mapping = result.get("civilization_core_layer_mapping")
        if not isinstance(mapping, dict):
            raise AssertionError("layer_mapping")
        if mapping.get("primary_layer") != "星魂记忆":
            raise AssertionError("primary_layer")
        if mapping.get("source_layer") != "星律记忆":
            raise AssertionError("source_layer")
        expected_chain = [
            *[f"v2.{minor}.0" for minor in range(9, 61)],
            "v3.0.0",
        ]
        if (
            PROPOSED_CHAIN_VERSIONS != expected_chain
            or result.get("proposed_chain_versions") != expected_chain
        ):
            raise AssertionError("proposed_chain_versions")
        expected_star_hub_chain = [
            *[f"v2.{minor}.0" for minor in range(19, 61)],
            "v3.0.0",
        ]
        if (
            PROPOSED_STAR_HUB_CHAIN_VERSIONS
            != expected_star_hub_chain
            or result.get("proposed_star_hub_chain_versions")
            != expected_star_hub_chain
        ):
            raise AssertionError("proposed_star_hub_chain_versions")
        if (
            READY_NEXT_ALLOWED_STEP
            != "v3.1.0 Star-Soul Memory continuity boundary review gate"
            or result.get("next_allowed_step") != READY_NEXT_ALLOWED_STEP
        ):
            raise AssertionError("next_allowed_step")
        for key in [
            "enters_star_soul_layer",
            "star_soul_continuity_authorized",
            "persistent_autonomous_identity_created",
            "consciousness_claimed",
            "personhood_claimed",
        ]:
            if result.get(key) is not False:
                raise AssertionError(key)
    except Exception as exc:
        print(f"{LABEL}=failed {exc}", file=sys.stderr)
        return 1

    print(f"{LABEL}=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
