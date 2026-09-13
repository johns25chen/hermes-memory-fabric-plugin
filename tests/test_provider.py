from __future__ import annotations

import importlib
from copy import deepcopy

import pytest

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.provider import PROVIDER_RUNTIME_INTEGRATION_POLICY
from hermes_memory_fabric.memory_subspace_index import create_subspace_descriptor, create_subspace_registry


NOW = "2026-05-26T00:00:00Z"
ADMISSION_SCOPE = {
    "project": "hermes-memory-fabric",
    "workspace": "/workspace/hermes-memory-fabric",
    "namespace": "memory",
}
DIRECT_SOURCE = {
    "provider_id": "direct-local-caller",
    "source_class": "LOCAL_CALLER",
    "source_instance": "provider:direct",
}
PROVIDER_REGISTRY = {
    "direct-local-caller": {
        "enabled": True,
        "source_classes": ["LOCAL_CALLER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }
}


def _project_subspace(
    subspace_id: str = "project:hermes-memory-fabric",
    project_scope: str = "hermes-memory-fabric",
    **overrides,
):
    base = {
        "subspace_id": subspace_id,
        "subspace_kind": "project",
        "scope": {"project_scope": project_scope},
        "owner": "memory-fabric-team",
        "access_policy": {
            "read": "allowed",
            "write": "forbidden",
            "proposal_required_for_writes": True,
        },
        "risk_level": "low",
        "lifecycle_status": "active",
        "active_summary": "Hermes Memory Fabric provider runtime project summary.",
        "source_index": {"source_ids": ["test:provider-runtime"]},
        "fact_graph_ref": {"node_id": f"fact-graph:{project_scope}"},
        "memory_blocks_ref": {"block_ids": [f"block:{project_scope}"]},
        "tags": ["memory-fabric", "provider-runtime"],
        "priority": 10,
        "created_at": NOW,
        "updated_at": NOW,
        "last_compacted_at": None,
        "governance_status": "governed",
    }
    base.update(overrides)
    return create_subspace_descriptor(**base)


def _registry():
    return create_subspace_registry(
        [
            _project_subspace(),
            _project_subspace(
                subspace_id="project:lovart",
                project_scope="lovart",
                tags=["lovart"],
                active_summary="Lovart unrelated provider runtime summary.",
            ),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
                active_summary="Archived Hermes Memory Fabric provider runtime summary.",
            ),
        ]
    )


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Provider Runtime Integration v0.1 prepares bounded read-only context packets.",
        "project_id": "hermes-memory-fabric",
        "subspace_id": "project:hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-26T10:00:00Z",
        "source": "design_doc",
        "provenance": f"test:provider-runtime:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def _build_packet(provider: MemoryFabricProvider | None = None, **overrides):
    active_provider = provider or MemoryFabricProvider()
    args = {
        "query": "Hermes Memory Fabric Provider Runtime Integration bounded context",
        "memory_candidates": [
            _candidate("provider-target"),
            _candidate(
                "provider-lovart",
                content="Lovart provider runtime memory belongs to another project.",
                project_id="lovart",
                subspace_id="project:lovart",
                entity_ids=["lovart"],
            ),
            _candidate(
                "provider-archived",
                content="Archived provider runtime memory should stay inactive by default.",
                subspace_id="project:hermes-memory-fabric:archive",
            ),
        ],
        "subspace_registry": _registry(),
        "project_scope": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "now": NOW,
        "admission_scope": ADMISSION_SCOPE,
        "provider_registry_snapshot": PROVIDER_REGISTRY,
        "candidate_source_descriptor": DIRECT_SOURCE,
    }
    args.update(overrides)
    return active_provider.build_active_context(**args)


def test_provider_v0_1_contract_is_read_only():
    provider = MemoryFabricProvider()

    assert provider.name == "memory-fabric"
    assert provider.is_available() is True

    provider.initialize("session-1", hermes_home="/tmp/hermes-test")

    assert provider.session_id == "session-1"
    assert provider.hermes_home == "/tmp/hermes-test"
    assert "read-only" in provider.system_prompt_block()
    assert "active context packets" in provider.system_prompt_block()
    assert provider.prefetch("anything") == ""
    assert provider.get_tool_schemas() == []
    assert provider.get_config_schema() == []
    provider.queue_prefetch("anything")
    provider.sync_turn("user", "assistant")
    provider.save_config({}, "/tmp/hermes-test")
    provider.shutdown()


def test_provider_does_not_handle_tools_in_v0_1():
    provider = MemoryFabricProvider()

    with pytest.raises(NotImplementedError):
        provider.handle_tool_call("memory_fabric_search", {})


def test_build_active_context_returns_valid_packet_with_matching_project_memory():
    provider = MemoryFabricProvider()

    packet = _build_packet(provider)
    validation = provider.validate_active_context(packet)

    assert validation == {"valid": True, "errors": []}
    assert packet["packet_type"] == "active_context_packet"
    assert "Provider Runtime Integration v0.1 prepares bounded read-only context packets" in (
        packet["compact_context_text"]
    )
    assert len(packet["selected_memories"]) == 1
    selected_id = packet["selected_memories"][0]["id"]
    assert selected_id == "provider-target"


def test_provider_rejects_unrelated_project_memory_and_explains_ids():
    provider = MemoryFabricProvider()
    packet = _build_packet(provider)
    explanation = provider.explain_active_context(packet)

    assert explanation["selected_memory_ids"] == ["provider-target"]
    assert set(explanation["rejected_memory_ids"]) == {
        "provider-lovart",
        "provider-archived",
    }
    assert set(explanation["selected_memory_ids"]).isdisjoint(explanation["rejected_memory_ids"])
    assert "project:lovart" in explanation["rejected_subspace_ids"]
    assert "Lovart provider runtime memory" not in packet["compact_context_text"]


def test_provider_summarize_active_context_returns_counts():
    provider = MemoryFabricProvider()
    packet = _build_packet(provider)
    summary = provider.summarize_active_context(packet)

    assert summary["selected_memory_count"] == 1
    assert summary["rejected_memory_count"] == 2
    assert summary["selected_subspace_count"] == 1
    assert summary["rejected_subspace_count"] == 2
    assert summary["context_item_count"] == len(packet["context_items"])


def test_provider_runtime_policy_proves_no_writes_no_executor_no_provider_tools():
    provider = MemoryFabricProvider()
    packet = _build_packet(provider)

    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["read_only"] is True
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["would_write_memory"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["would_modify_config"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["would_write_graph"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["writes_proposal_files"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["writes_operation_ledger"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["writes_token_files"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["writes_approval_audit"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["invokes_real_token_write_executor"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["implements_real_token_write_executor"] is False
    assert PROVIDER_RUNTIME_INTEGRATION_POLICY["exposes_provider_tools"] is False
    assert provider.runtime_integration_policy == PROVIDER_RUNTIME_INTEGRATION_POLICY
    assert packet["policy"]["read_only"] is True
    assert provider.get_tool_schemas() == []


def test_provider_methods_do_not_mutate_inputs_or_runtime_config():
    provider = MemoryFabricProvider()
    config = {"context_budget_chars": 900, "required_tags": ["memory-fabric"]}
    provider.initialize("session-immutability", runtime_config=config)
    candidates = [_candidate("provider-target"), _candidate("provider-archived", lifecycle_status="archived")]
    registry = _registry()
    context = {"project_scope": "hermes-memory-fabric", "query": "provider runtime"}
    original_config = deepcopy(config)
    original_candidates = deepcopy(candidates)
    original_registry = deepcopy(registry)
    original_context = deepcopy(context)
    original_runtime_config = deepcopy(provider.runtime_config)

    packet = provider.build_active_context(
        query="Hermes Memory Fabric Provider Runtime Integration",
        memory_candidates=candidates,
        subspace_registry=registry,
        context=context,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )
    provider.summarize_active_context(packet)
    provider.explain_active_context(packet)
    provider.validate_active_context(packet)

    assert config == original_config
    assert candidates == original_candidates
    assert registry == original_registry
    assert context == original_context
    assert provider.runtime_config == original_runtime_config


def test_provider_runtime_defaults_exclude_archived_and_high_risk_until_allowed():
    provider = MemoryFabricProvider()
    blocked = provider.build_active_context(
        query="Hermes Memory Fabric Provider Runtime Integration risk archive",
        memory_candidates=[
            _candidate("provider-archived", lifecycle_status="archived"),
            _candidate("provider-high-risk", risk_level="high"),
        ],
        project_scope="hermes-memory-fabric",
        now=NOW,
        memory_limit=2,
        admission_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
        candidate_source_descriptor=DIRECT_SOURCE,
    )
    blocked_reasons = {item["id"]: item["reason"] for item in blocked["rejected_memories"]}

    allowed = provider.build_active_context(
        query="Hermes Memory Fabric Provider Runtime Integration risk archive",
        memory_candidates=[
            _candidate("provider-archived", lifecycle_status="archived"),
            _candidate("provider-high-risk", risk_level="high"),
        ],
        project_scope="hermes-memory-fabric",
        now=NOW,
        memory_limit=2,
        include_archived=True,
        allowed_risk_levels=["low", "medium", "high"],
        admission_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
        candidate_source_descriptor=DIRECT_SOURCE,
    )
    allowed_ids = {item["id"] for item in allowed["selected_memories"]}

    assert blocked_reasons["provider-archived"] == "archived_subspace_excluded"
    assert blocked_reasons["provider-high-risk"] == "risk_level_not_allowed:high"
    assert {"provider-archived", "provider-high-risk"}.issubset(allowed_ids)


def test_provider_runtime_config_supplies_active_context_defaults():
    provider = MemoryFabricProvider(memory_limit=1, context_budget_chars=180)

    packet = _build_packet(
        provider,
        memory_candidates=[
            _candidate("provider-target-a", content="Provider Runtime Integration selected memory A."),
            _candidate("provider-target-b", content="Provider Runtime Integration selected memory B."),
        ],
        subspace_registry=None,
    )

    assert len(packet["selected_memories"]) == 1
    assert packet["budget"]["memory_limit"] == 1
    assert packet["budget"]["context_budget_chars"] == 180


def test_direct_candidates_without_admission_configuration_fail_closed():
    provider = MemoryFabricProvider()
    packet = provider.build_active_context(
        query="SECRET DIRECT CANDIDATE",
        memory_candidates=[_candidate("untrusted", content="SECRET DIRECT CANDIDATE")],
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    assert packet["selected_memories"] == []
    assert "SECRET DIRECT CANDIDATE" not in packet["compact_context_text"]


def test_provider_projection_preserves_business_id_and_overwrites_spoofed_security_identity():
    provider = MemoryFabricProvider()
    payload = _candidate(
        "business-memory-id",
        provider_federation_identity={
            "provider_id": "spoofed-provider",
            "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
            "source_instance": "spoofed:instance",
            "candidate_id": "spoofed-candidate",
            "request_id": "spoofed-request",
            "payload_digest": "sha256:" + "0" * 64,
            "request_scope_digest": "sha256:" + "0" * 64,
        },
    )
    original = deepcopy(payload)

    admitted = provider._admit_candidate_sources(
        sources=[(DIRECT_SOURCE, [payload])],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )

    assert payload == original
    assert admitted[0]["id"] == "business-memory-id"
    identity = admitted[0]["provider_federation_identity"]
    assert identity["provider_id"] == "direct-local-caller"
    assert identity["source_class"] == "LOCAL_CALLER"
    assert identity["source_instance"] == "provider:direct"
    assert identity["candidate_id"] != "spoofed-candidate"
    assert identity["request_id"] != "spoofed-request"
    assert identity["payload_digest"] != "sha256:" + "0" * 64
    assert identity["request_scope_digest"] != "sha256:" + "0" * 64


def test_candidate_identity_is_stable_when_source_order_changes_and_payload_updates_digest():
    provider = MemoryFabricProvider()
    first = _candidate("stable-source-key", content="first content")
    second = _candidate("other-source-key", content="other content")

    ordered = provider._admit_candidate_sources(
        sources=[(DIRECT_SOURCE, [first, second])],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )
    reordered = provider._admit_candidate_sources(
        sources=[(DIRECT_SOURCE, [second, first])],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )
    updated = provider._admit_candidate_sources(
        sources=[(DIRECT_SOURCE, [_candidate("stable-source-key", content="updated content")])],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )

    ordered_identity = {item["id"]: item["provider_federation_identity"] for item in ordered}
    reordered_identity = {item["id"]: item["provider_federation_identity"] for item in reordered}
    assert ordered_identity["stable-source-key"]["candidate_id"] == "stable-source-key"
    assert reordered_identity["stable-source-key"]["candidate_id"] == "stable-source-key"
    assert updated[0]["provider_federation_identity"]["candidate_id"] == "stable-source-key"
    assert updated[0]["provider_federation_identity"]["payload_digest"] != ordered_identity["stable-source-key"]["payload_digest"]


def test_missing_or_invalid_candidate_source_key_is_rejected_before_downstream():
    provider = MemoryFabricProvider()
    admitted = provider._admit_candidate_sources(
        sources=[(DIRECT_SOURCE, [_candidate("", content="invalid"), {"content": "missing"}])],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )
    assert admitted == []


def test_same_source_key_with_different_payloads_is_blocked_as_compound_conflict():
    provider = MemoryFabricProvider()
    admitted = provider._admit_candidate_sources(
        sources=[
            (
                DIRECT_SOURCE,
                [
                    _candidate("conflict-key", content="first"),
                    _candidate("conflict-key", content="second"),
                ],
            )
        ],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=PROVIDER_REGISTRY,
    )
    assert admitted == []


def test_explicit_empty_candidate_descriptor_does_not_fall_back_to_runtime_default():
    provider = MemoryFabricProvider(
        runtime_config={
            "admission_scope": ADMISSION_SCOPE,
            "provider_registry_snapshot": PROVIDER_REGISTRY,
            "direct_candidate_source": DIRECT_SOURCE,
        }
    )
    packet = provider.build_active_context(
        query="explicit empty descriptor",
        memory_candidates=[_candidate("empty-descriptor", content="must be rejected")],
        project_scope="hermes-memory-fabric",
        now=NOW,
        candidate_source_descriptor={},
    )
    assert packet["selected_memories"] == []
    assert "must be rejected" not in packet["compact_context_text"]


def test_same_business_id_from_different_authoritative_sources_remains_two_candidates():
    provider = MemoryFabricProvider()
    second_source = {
        "provider_id": "second-local-provider",
        "source_class": "LOCAL_PROVIDER",
        "source_instance": "provider:second",
    }
    registry = deepcopy(PROVIDER_REGISTRY)
    registry["second-local-provider"] = {
        "enabled": True,
        "source_classes": ["LOCAL_PROVIDER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }

    admitted = provider._admit_candidate_sources(
        sources=[
            (DIRECT_SOURCE, [_candidate("shared-business-id", content="first source")]),
            (second_source, [_candidate("shared-business-id", content="second source")]),
        ],
        request_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=registry,
    )

    assert [candidate["id"] for candidate in admitted] == [
        "shared-business-id",
        "shared-business-id",
    ]
    identities = [candidate["provider_federation_identity"] for candidate in admitted]
    assert len({(item["provider_id"], item["source_instance"], item["candidate_id"]) for item in identities}) == 2


def test_external_review_candidate_cannot_reach_direct_context_composition():
    external_registry = {
        "external-review": {
            "enabled": True,
            "source_classes": ["EXTERNAL_FEDERATED_CANDIDATE"],
            "capabilities": ["READ_CANDIDATE"],
            "review_only": True,
            "trusted_ingestion": False,
        }
    }
    packet = MemoryFabricProvider().build_active_context(
        query="SECRET REVIEW CANDIDATE",
        memory_candidates=[_candidate("review", content="SECRET REVIEW CANDIDATE")],
        project_scope="hermes-memory-fabric",
        now=NOW,
        admission_scope=ADMISSION_SCOPE,
        provider_registry_snapshot=external_registry,
        candidate_source_descriptor={
            "provider_id": "external-review",
            "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
            "source_instance": "external:review",
        },
    )

    assert packet["selected_memories"] == []
    assert "SECRET REVIEW CANDIDATE" not in packet["compact_context_text"]


def test_top_level_module_register_adds_memory_provider_without_tools():
    module = importlib.import_module("hermes_memory_fabric")

    class Context:
        def __init__(self) -> None:
            self.providers = []

        def register_memory_provider(self, provider) -> None:
            self.providers.append(provider)

    ctx = Context()

    assert callable(module.register)

    module.register(ctx)

    assert len(ctx.providers) == 1
    assert isinstance(ctx.providers[0], MemoryFabricProvider)
    assert ctx.providers[0].get_tool_schemas() == []
    assert callable(ctx.providers[0].build_active_context)
    assert callable(ctx.providers[0].summarize_active_context)
    assert callable(ctx.providers[0].explain_active_context)
    assert callable(ctx.providers[0].validate_active_context)
    assert callable(ctx.providers[0].prefetch)
    assert callable(ctx.providers[0].queue_prefetch)
    assert callable(ctx.providers[0].sync_turn)
    assert callable(ctx.providers[0].shutdown)
