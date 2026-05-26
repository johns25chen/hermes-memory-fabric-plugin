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


def test_smoke_suite_still_passes_37_cases():
    report = run_benchmark("smoke")

    assert report["suite"] == "smoke"
    assert report["aggregate"]["case_count"] == 37
    assert report["aggregate"]["passed_count"] == 37
    assert report["aggregate"]["failed_count"] == 0
    assert report["aggregate"]["overall_score"] == 1.0


def test_v02_suite_loads_separately_with_required_dimensions():
    smoke_cases = load_cases("smoke")
    v02_cases = load_cases("v02")
    v02_dimensions = {case["dimension"] for case in v02_cases}

    assert len(smoke_cases) == 37
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
