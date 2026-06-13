#!/usr/bin/env python3
"""Smoke test for the governed Star-Soul completion attestation review gate."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal import (  # noqa: E402
    build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal,
)
from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate import (  # noqa: E402
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS,
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
    REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate,
)
from smoke_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal import (  # noqa: E402
    _valid_v3_9_star_soul_approval_request_dry_run_execution_review_gate_report,
)


LABEL = (
    "governed_star_soul_memory_continuity_boundary_approval_request_"
    "dry_run_completion_attestation_review_gate"
)


def _valid_v3_10_star_soul_approval_request_dry_run_completion_attestation_proposal_report() -> (
    dict[str, object]
):
    return build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal(
        _valid_v3_9_star_soul_approval_request_dry_run_execution_review_gate_report()
    )


def main() -> int:
    try:
        result = build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate(
            _valid_v3_10_star_soul_approval_request_dry_run_completion_attestation_proposal_report()
        )
        if (
            result.get("status")
            != "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_ready"
        ):
            raise AssertionError("status")
        for key, expected in (
            APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS.items()
        ):
            if result.get(key) is not expected:
                raise AssertionError(key)
        review_gate = result.get(
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate"
        )
        if not isinstance(review_gate, dict):
            raise AssertionError(
                "approval_request_dry_run_completion_attestation_review_gate"
            )
        for key, expected in (
            APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS.items()
        ):
            if review_gate.get(key) is not expected:
                raise AssertionError(
                    f"approval_request_dry_run_completion_attestation_review_gate_{key}"
                )
        for key in [
            "dry_run_executed",
            "dry_run_plan_executed",
            "completion_executed",
            "attestation_executed",
            "finalization_executed",
            "closure_executed",
            "approval_request_created",
            "approval_request_submitted",
            "approval_request_executed",
            "approval_granted",
            "real_human_decision_recorded",
        ]:
            if result.get(key) is not False:
                raise AssertionError(key)
        mapping = result.get("civilization_core_layer_mapping")
        if not isinstance(mapping, dict):
            raise AssertionError("layer_mapping")
        if mapping.get("primary_layer") != "星魂记忆":
            raise AssertionError("primary_layer")
        if mapping.get("source_layer") != "星魂记忆":
            raise AssertionError("source_layer")
        expected_chain = [
            *[f"v2.{minor}.0" for minor in range(9, 61)],
            "v3.0.0",
            "v3.1.0",
            "v3.2.0",
            "v3.4.0",
            "v3.6.0",
            "v3.7.0",
            "v3.8.0",
            "v3.9.0",
            "v3.10.0",
            "v3.11.0",
        ]
        if (
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
            != expected_chain
            or result.get(
                "reviewed_dry_run_completion_attestation_chain_versions"
            )
            != expected_chain
        ):
            raise AssertionError(
                "reviewed_dry_run_completion_attestation_chain_versions"
            )
        expected_star_hub_chain = [
            *[f"v2.{minor}.0" for minor in range(19, 61)],
            "v3.0.0",
            "v3.1.0",
            "v3.2.0",
            "v3.4.0",
            "v3.6.0",
            "v3.7.0",
            "v3.8.0",
            "v3.9.0",
            "v3.10.0",
            "v3.11.0",
        ]
        if (
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
            != expected_star_hub_chain
            or result.get(
                "reviewed_dry_run_completion_attestation_star_hub_chain_versions"
            )
            != expected_star_hub_chain
        ):
            raise AssertionError(
                "reviewed_dry_run_completion_attestation_star_hub_chain_versions"
            )
        if (
            READY_NEXT_ALLOWED_STEP
            != "v3.12.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation approval proposal"
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
