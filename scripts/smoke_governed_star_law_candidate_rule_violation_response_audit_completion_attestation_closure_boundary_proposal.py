#!/usr/bin/env python3
"""Smoke test for the governed audit completion attestation closure proposal."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate import (  # noqa: E402
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal import (  # noqa: E402
    PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal,
)
from smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate import (  # noqa: E402
    _valid_audit_completion_attestation_boundary_proposal_report,
)


LABEL = "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal"


def _valid_audit_completion_attestation_boundary_review_gate_report() -> dict[
    str, object
]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate(
        _valid_audit_completion_attestation_boundary_proposal_report()
    )


def main() -> int:
    try:
        result = build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal(
            _valid_audit_completion_attestation_boundary_review_gate_report()
        )
        if (
            result.get("status")
            != "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_ready"
        ):
            print(f"{LABEL}=failed status", file=sys.stderr)
            return 1
        for key in (
            "read_only",
            "read_only_memory",
            "proposal_only",
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_only",
            "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_only",
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposed_for_human_review_only",
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_ready_for_human_review_only",
        ):
            if result.get(key) is not True:
                print(f"{LABEL}=failed {key}", file=sys.stderr)
                return 1
        for key, expected in PROPOSAL_FALSE_FLAGS.items():
            if result.get(key) is not expected:
                print(f"{LABEL}=failed {key}", file=sys.stderr)
                return 1
        proposal = result.get(
            "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal",
            {},
        )
        if not isinstance(proposal, dict):
            print(f"{LABEL}=failed proposal", file=sys.stderr)
            return 1
        for key, expected in PROPOSAL_OBJECT_FALSE_FLAGS.items():
            if proposal.get(key) is not expected:
                print(f"{LABEL}=failed proposal_{key}", file=sys.stderr)
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if not isinstance(mapping, dict) or mapping.get("primary_layer") != "星律记忆":
            print(f"{LABEL}=failed primary_layer", file=sys.stderr)
            return 1
        if result.get("proposed_chain_versions") != PROPOSED_CHAIN_VERSIONS:
            print(f"{LABEL}=failed proposed_chain_versions", file=sys.stderr)
            return 1
        if (
            result.get("proposed_star_hub_chain_versions")
            != PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ):
            print(f"{LABEL}=failed proposed_star_hub_chain_versions", file=sys.stderr)
            return 1
        if result.get("next_allowed_step") != READY_NEXT_ALLOWED_STEP:
            print(f"{LABEL}=failed next_allowed_step", file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"{LABEL}=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print(f"{LABEL}=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
