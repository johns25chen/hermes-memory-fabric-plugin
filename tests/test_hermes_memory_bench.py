from copy import deepcopy

import benchmarks.hermes_memory_bench.core as bench_module
from benchmarks.hermes_memory_bench.core import V02_QUALITY_METRICS, load_cases, run_benchmark


V02_REQUIRED_DIMENSIONS = {
    "recall_fusion_v2_selection_accuracy",
    "recall_fusion_v2_rejection_accuracy",
    "recall_fusion_v2_explanation_quality",
    "subspace_isolation_accuracy",
    "archived_subspace_rejection",
    "high_risk_rejection",
    "high_risk_allowed_when_explicit",
    "temporal_validity_resolution",
    "contradiction_review_routing",
    "memory_active_context_composer",
    "memory_provider_runtime_integration",
    "no_write_policy_safety",
}

V02_REQUIRED_EVIDENCE_FIELDS = {
    "selected_memory_ids",
    "rejected_memory_ids",
    "selected_subspace_ids",
    "rejected_subspace_ids",
    "rejection_reasons",
    "explanation_present",
    "policy",
    "created_real_proposal",
    "created_operation_event",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_token_files",
    "writes_approval_audit",
    "invokes_real_token_write_executor",
    "implements_real_token_write_executor",
    "exposes_provider_tools",
}


def test_smoke_suite_still_passes_39_cases():
    report = run_benchmark("smoke")

    assert report["suite"] == "smoke"
    assert report["aggregate"]["case_count"] == 39
    assert report["aggregate"]["passed_count"] == 39
    assert report["aggregate"]["failed_count"] == 0
    assert report["aggregate"]["overall_score"] == 1.0


def test_v02_suite_loads_separately_with_required_dimensions():
    smoke_cases = load_cases("smoke")
    v02_cases = load_cases("v02")
    v02_dimensions = {case["dimension"] for case in v02_cases}

    assert len(smoke_cases) == 39
    assert len(v02_cases) >= 10
    assert v02_cases != smoke_cases
    assert V02_REQUIRED_DIMENSIONS.issubset(v02_dimensions)


def test_v02_aggregate_includes_quality_metrics_and_scores_one():
    report = run_benchmark("v02")

    assert report["benchmark_type"] == "hermes_memory_bench_v0.2"
    assert report["suite"] == "v02"
    assert report["aggregate"]["case_count"] >= 10
    assert report["aggregate"]["failed_count"] == 0
    for metric in V02_QUALITY_METRICS:
        assert metric in report["aggregate"]
        assert report["aggregate"][metric] == 1.0


def test_benchmark_internal_caller_admission_uses_canonical_scope_and_overwrites_payload_spoofing():
    case = deepcopy(
        next(
            item
            for item in load_cases("v02")
            if item["dimension"] == "memory_provider_runtime_integration"
        )
    )
    candidate = case["memories"][0]
    candidate.update(
        {
            "provider_id": "spoofed-provider",
            "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
            "source_instance": "spoofed-instance",
            "candidate_id": "spoofed-candidate",
            "request_id": "spoofed-request",
            "workspace": "spoofed-workspace",
            "namespace": "spoofed-namespace",
            "provider_federation_identity": {
                "provider_id": "spoofed-provider",
                "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
                "source_instance": "spoofed-instance",
                "candidate_id": "spoofed-candidate",
            },
        }
    )
    original = deepcopy(case)
    registry = bench_module._v02_subspace_registry(case.get("subspaces", []))

    from pytest import MonkeyPatch

    admitted_batches = []
    original_admit = bench_module.MemoryFabricProvider._admit_candidate_sources

    def capture_admit(self, **kwargs):
        admitted = original_admit(self, **kwargs)
        admitted_batches.append(deepcopy(admitted))
        return admitted

    with MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            bench_module.MemoryFabricProvider,
            "_admit_candidate_sources",
            capture_admit,
        )
        passed, evidence = bench_module._run_provider_runtime_integration_case(case, registry)

    assert passed is True
    assert case == original
    selected = evidence["active_context_packet"]["selected_memories"]
    assert [item["id"] for item in selected] == [case["expected_top_selected_memory_id"]]
    assert len(admitted_batches) == 1
    admitted_matches = [
        item for item in admitted_batches[0] if item["id"] == selected[0]["id"]
    ]
    assert len(admitted_matches) == 1
    assert admitted_matches[0]["id"] == candidate["id"]
    identity = admitted_matches[0]["provider_federation_identity"]
    assert identity["provider_id"] == "internal-hermes-memory-bench"
    assert identity["source_class"] == "LOCAL_CALLER"
    assert identity["source_instance"] == "benchmark-runner"
    assert identity["candidate_id"] != "spoofed-candidate"
    assert identity["request_id"] != "spoofed-request"
    runtime_config = evidence["provider_runtime_config"]
    assert runtime_config["admission_scope"] == {
        "project": case["project_scope"],
        "workspace": "/workspace/hermes-memory-bench",
        "namespace": "benchmark-evaluation",
    }
    assert runtime_config["provider_registry_snapshot"] == {
        "internal-hermes-memory-bench": {
            "enabled": True,
            "source_classes": ["LOCAL_CALLER"],
            "capabilities": ["READ_CANDIDATE"],
            "review_only": False,
            "trusted_ingestion": True,
        }
    }


def test_v02_includes_recall_fusion_selection_and_rejection_cases():
    cases = {case["dimension"]: case for case in load_cases("v02")}

    assert "recall_fusion_v2_selection_accuracy" in cases
    assert "recall_fusion_v2_rejection_accuracy" in cases
    assert cases["recall_fusion_v2_selection_accuracy"]["expected_top_selected_memory_id"] == "rfv2-target"
    assert "rfv2-unsafe" in cases["recall_fusion_v2_rejection_accuracy"]["expected_rejected_memory_ids"]


def test_v02_includes_subspace_archived_and_high_risk_gating_cases():
    dimensions = {case["dimension"] for case in load_cases("v02")}

    assert "subspace_isolation_accuracy" in dimensions
    assert "archived_subspace_rejection" in dimensions
    assert "high_risk_rejection" in dimensions
    assert "high_risk_allowed_when_explicit" in dimensions


def test_v02_includes_temporal_and_contradiction_cases():
    cases = {case["dimension"]: case for case in load_cases("v02")}

    assert cases["temporal_validity_resolution"]["expected_selected_memory_ids"] == ["temporal-current"]
    assert cases["contradiction_review_routing"]["expected_review_action"] == "review_contradiction"


def test_v02_includes_active_context_composer_case():
    cases = {case["dimension"]: case for case in load_cases("v02")}

    assert "memory_active_context_composer" in cases
    assert cases["memory_active_context_composer"]["expected_top_selected_memory_id"] == "active-context-target"
    assert "active-context-unrelated" in cases["memory_active_context_composer"]["expected_rejected_memory_ids"]


def test_benchmarks_include_provider_runtime_integration_cases():
    smoke_cases = {case["dimension"]: case for case in load_cases("smoke")}
    v02_cases = {case["dimension"]: case for case in load_cases("v02")}

    assert "memory_provider_runtime_integration" in smoke_cases
    assert "memory_provider_runtime_integration" in v02_cases
    assert smoke_cases["memory_provider_runtime_integration"]["expected_top_selected_memory_id"] == (
        "provider-runtime-target"
    )
    assert v02_cases["memory_provider_runtime_integration"]["expected_top_selected_memory_id"] == (
        "provider-runtime-v02-target"
    )


def test_v02_policy_safety_evidence_proves_no_writes_or_executor_or_provider_tools():
    report = run_benchmark("v02")

    for case in report["cases"]:
        evidence = case["evidence"]
        assert V02_REQUIRED_EVIDENCE_FIELDS.issubset(evidence)
        assert evidence["created_real_proposal"] is False
        assert evidence["created_operation_event"] is False
        assert evidence["writes_proposal_files"] is False
        assert evidence["writes_operation_ledger"] is False
        assert evidence["writes_token_files"] is False
        assert evidence["writes_approval_audit"] is False
        assert evidence["invokes_real_token_write_executor"] is False
        assert evidence["implements_real_token_write_executor"] is False
        assert evidence["exposes_provider_tools"] is False
        assert evidence["policy"]["read_only"] is True
        assert evidence["policy"]["would_write_memory"] is False
        assert evidence["policy"]["would_modify_config"] is False
        assert evidence["policy"]["would_write_graph"] is False
        assert evidence["policy"]["exposes_provider_tools"] is False
