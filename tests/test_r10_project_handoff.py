from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "r10_project_handoff.py"
_SPEC = importlib.util.spec_from_file_location("r10_project_handoff", SCRIPT_PATH)
assert _SPEC is not None and _SPEC.loader is not None
handoff = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(handoff)


def _run(source_files: list[Path], output_dir: Path, *extra: str, caller_risk_level: str = "low") -> int:
    argv = [
        "--source-file",
        str(source_files[0]),
        "--question",
        "alpha completed capability and next work",
        "--project",
        "CIVILIZATION-CORE",
        "--workspace",
        "/governance/civilization-core/test",
        "--namespace",
        "r10-test",
        "--caller-risk-level",
        caller_risk_level,
        "--output-dir",
        str(output_dir),
        "--confirm-local-context-use",
    ]
    for source_file in source_files[1:]:
        argv.extend(("--source-file", str(source_file)))
    argv.extend(extra)
    return handoff.main(argv)


def _result(output_dir: Path) -> dict:
    return json.loads((output_dir / handoff.RESULT_FILENAME).read_text(encoding="utf-8"))


def _diagnostics(output_dir: Path) -> dict:
    return json.loads((output_dir / handoff.DIAGNOSTIC_FILENAME).read_text(encoding="utf-8"))


def test_reads_original_text_and_preserves_file_hash_and_line_range(tmp_path):
    source = tmp_path / "synthetic-alpha.txt"
    sentinel = tmp_path / "command-side-effect"
    original = (
        "alpha completed capability\n"
        f"touch {sentinel}\n"
        "next work remains bounded\n"
    )
    source.write_text(original, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([source], output_dir, "--write-diagnostics") == 0

    result = _result(output_dir)
    diagnostics = _diagnostics(output_dir)
    candidate = diagnostics["input_candidates"][0]
    assert candidate["content"] == original
    assert candidate["provenance"] == {
        "file_path": str(source),
        "file_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
        "line_end": 3,
        "line_start": 1,
        "char_start": 0,
        "char_end": len(original),
    }
    assert not sentinel.exists()
    assert source.read_text(encoding="utf-8") == original
    assert diagnostics["packet"]["packet_type"] == "active_context_packet"
    assert result["source_mappings"][0]["provenance"] == candidate["provenance"]
    assert result["source_mappings"][0]["source_id"] in result["context"]


@pytest.mark.parametrize("kind", ["missing", "directory", "symlink"])
def test_rejects_non_regular_or_missing_source_paths(tmp_path, kind):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    source = tmp_path / "source.txt"
    source.write_text("alpha", encoding="utf-8")
    if kind == "missing":
        target = tmp_path / "missing.txt"
    elif kind == "directory":
        target = tmp_path / "directory"
        target.mkdir()
    else:
        target = tmp_path / "link.txt"
        target.symlink_to(source)

    with pytest.raises(SystemExit) as captured:
        _run([target], output_dir)

    assert captured.value.code == 2
    assert not (output_dir / handoff.RESULT_FILENAME).exists()


def test_rejects_fifo_before_opening_it(tmp_path):
    source = tmp_path / "source.fifo"
    os.mkfifo(source)

    with pytest.raises(handoff.HandoffInputError, match="source_file_not_regular"):
        handoff._read_utf8_regular_file(str(source), max_bytes=64)


def test_rejects_source_replaced_between_lstat_and_open(tmp_path, monkeypatch):
    source = tmp_path / "source.txt"
    replacement = tmp_path / "replacement.txt"
    source.write_text("alpha original", encoding="utf-8")
    replacement.write_text("alpha replacement", encoding="utf-8")
    original_open = handoff.os.open

    def replace_then_open(value, flags, *args, **kwargs):
        if Path(value) == source:
            source.unlink()
            replacement.rename(source)
        return original_open(value, flags, *args, **kwargs)

    monkeypatch.setattr(handoff.os, "open", replace_then_open)

    with pytest.raises(handoff.HandoffInputError, match="source_file_replaced_before_open"):
        handoff._read_utf8_regular_file(str(source), max_bytes=64)


def test_rejects_source_before_reading_when_declared_size_exceeds_limit(tmp_path):
    source = tmp_path / "oversize.txt"
    source.write_text("alpha exceeds limit", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(SystemExit) as captured:
        _run([source], output_dir, "--max-source-bytes", "4")

    assert captured.value.code == 2
    assert not (output_dir / handoff.RESULT_FILENAME).exists()


def test_requires_explicit_confirmation_before_provider_call(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    argv = [
        "--source-file", str(source),
        "--question", "alpha completed capability",
        "--project", "CIVILIZATION-CORE",
        "--workspace", "/governance/civilization-core/test",
        "--namespace", "r10-test",
        "--caller-risk-level", "low",
        "--output-dir", str(output_dir),
    ]

    with pytest.raises(SystemExit) as captured:
        handoff.main(argv)

    assert captured.value.code == 2
    assert not (output_dir / handoff.RESULT_FILENAME).exists()


def test_real_provider_selects_relevant_content_and_excludes_lower_ranked_content(tmp_path):
    selected = tmp_path / "selected.txt"
    selected.write_text("alpha completed capability next work", encoding="utf-8")
    lower_ranked = tmp_path / "lower-ranked.txt"
    lower_ranked.write_text("unrelated orchard weather", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([selected, lower_ranked], output_dir, "--memory-limit", "1", "--write-diagnostics") == 0

    result = _result(output_dir)
    diagnostics = _diagnostics(output_dir)
    packet = diagnostics["packet"]
    assert len(packet["selected_memories"]) == 1
    assert packet["selected_memories"][0]["id"] == diagnostics["input_candidates"][0]["id"]
    assert [item["id"] for item in packet["rejected_memories"]] == [diagnostics["input_candidates"][1]["id"]]
    assert "unrelated orchard weather" not in result["context"]
    assert "alpha completed capability" in result["context"]


def test_original_rejected_prefix_is_not_mistaken_for_mapping_failure(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("[REJECTED] alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([source], output_dir) == 0
    assert "alpha completed capability" in _result(output_dir)["context"]


def test_zero_budget_reports_no_context_without_result(tmp_path, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([source], output_dir, "--context-budget-chars", "0") == 3
    assert capsys.readouterr().out.strip() == "NO_CONTEXT"
    assert not (output_dir / handoff.RESULT_FILENAME).exists()
    assert not (output_dir / handoff.DIAGNOSTIC_FILENAME).exists()


def test_candidate_ids_are_path_bound_stable_and_duplicate_paths_are_rejected(tmp_path):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("same body", encoding="utf-8")
    second.write_text("same body", encoding="utf-8")

    forward = handoff._build_candidates(
        [str(first), str(second)], project="CIVILIZATION-CORE", max_bytes=64, max_segment_chars=64, caller_risk_level="low"
    )
    reverse = handoff._build_candidates(
        [str(second), str(first)], project="CIVILIZATION-CORE", max_bytes=64, max_segment_chars=64, caller_risk_level="low"
    )
    forward_by_path = {candidate["provenance"]["file_path"]: candidate["id"] for candidate in forward}
    reverse_by_path = {candidate["provenance"]["file_path"]: candidate["id"] for candidate in reverse}

    assert forward_by_path == reverse_by_path
    assert forward[0]["id"] != forward[1]["id"]
    with pytest.raises(handoff.HandoffInputError, match="source_file_duplicate"):
        handoff._build_candidates(
            [str(first), str(first)], project="CIVILIZATION-CORE", max_bytes=64, max_segment_chars=64, caller_risk_level="low"
        )


@pytest.mark.parametrize("caller_risk_level", ["high", "critical"])
def test_high_risk_requires_the_existing_provider_allowlist_and_is_not_silently_reclassified(tmp_path, capsys, caller_risk_level):
    source = tmp_path / "source.txt"
    source.write_text("alpha high risk declaration", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([source], output_dir, caller_risk_level=caller_risk_level) == 3
    assert capsys.readouterr().out.strip() == "NO_CONTEXT"
    assert not (output_dir / handoff.RESULT_FILENAME).exists()


def test_invalid_packet_is_rejected_before_any_output(tmp_path, monkeypatch, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_build = handoff.MemoryFabricProvider.build_active_context

    def invalid_packet(provider, **kwargs):
        packet = original_build(provider, **kwargs)
        packet["packet_type"] = "invalid"
        return packet

    monkeypatch.setattr(handoff.MemoryFabricProvider, "build_active_context", invalid_packet)
    assert _run([source], output_dir, "--write-diagnostics") == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "ERROR:" in captured.err
    assert list(output_dir.iterdir()) == []


def test_mapping_mismatch_is_rejected_before_any_output(tmp_path, monkeypatch, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_build = handoff.MemoryFabricProvider.build_active_context

    def mismatched_packet(provider, **kwargs):
        packet = original_build(provider, **kwargs)
        packet["context_items"][0]["source_id"] = "wrong-source"
        return packet

    monkeypatch.setattr(handoff.MemoryFabricProvider, "build_active_context", mismatched_packet)
    assert _run([source], output_dir) == 1
    assert capsys.readouterr().out == ""
    assert list(output_dir.iterdir()) == []


@pytest.mark.parametrize("write_diagnostics", [False, True])
def test_body_mismatch_with_consistent_mapping_and_render_is_rejected(tmp_path, monkeypatch, capsys, write_diagnostics):
    source = tmp_path / "source.txt"
    source.write_text("alpha original body\n", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_build = handoff.MemoryFabricProvider.build_active_context

    def mismatched_body(provider, **kwargs):
        packet = original_build(provider, **kwargs)
        item = packet["context_items"][0]
        candidate = kwargs["memory_candidates"][0]
        assert item["item_id"] == f"memory:{candidate['id']}"
        assert item["source_id"] == candidate["source_id"]
        assert item["text"] == candidate["content"].strip()
        item["text"] = "alpha forged body"
        packet["compact_context_text"] = f"[MEMORY {item['source_id']}] {item['text']}"
        assert provider.validate_active_context(packet) == {"valid": True, "errors": []}
        return packet

    monkeypatch.setattr(handoff.MemoryFabricProvider, "build_active_context", mismatched_body)
    args = ("--write-diagnostics",) if write_diagnostics else ()
    code = _run([source], output_dir, *args)
    captured = capsys.readouterr()
    observed = {
        "entry_exit": code,
        "stdout": captured.out,
        "stderr": captured.err,
        "published_files": sorted(path.name for path in output_dir.iterdir()),
        "formal_context": _result(output_dir)["context"] if (output_dir / handoff.RESULT_FILENAME).exists() else None,
    }
    assert observed == {
        "entry_exit": 1,
        "stdout": "",
        "stderr": "ERROR:HandoffDeliveryError:context_source_mismatch\n",
        "published_files": [],
        "formal_context": None,
    }


@pytest.mark.parametrize("write_diagnostics", [False, True])
def test_serialization_failure_leaves_no_final_or_temporary_files(tmp_path, monkeypatch, capsys, write_diagnostics):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_dumps = handoff.json.dumps

    def fail_result(value, *args, **kwargs):
        if isinstance(value, dict) and value.get("result_type") == "r10_local_project_handoff":
            raise TypeError("synthetic serialization failure")
        return original_dumps(value, *args, **kwargs)

    monkeypatch.setattr(handoff.json, "dumps", fail_result)
    args = ("--write-diagnostics",) if write_diagnostics else ()
    assert _run([source], output_dir, *args) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert not (output_dir / handoff.RESULT_FILENAME).exists()
    assert not any(path.name.startswith(".project-handoff") for path in output_dir.iterdir())
    assert (output_dir / handoff.DIAGNOSTIC_FILENAME).exists() is write_diagnostics, captured.err


@pytest.mark.parametrize("write_diagnostics", [False, True])
def test_write_failure_leaves_no_final_or_temporary_files(tmp_path, monkeypatch, capsys, write_diagnostics):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_link = handoff.os.link

    def fail_result_link(source_path, target_path, *args, **kwargs):
        if Path(target_path).name == handoff.RESULT_FILENAME:
            raise OSError("synthetic publication failure")
        return original_link(source_path, target_path, *args, **kwargs)

    monkeypatch.setattr(handoff.os, "link", fail_result_link)
    args = ("--write-diagnostics",) if write_diagnostics else ()
    assert _run([source], output_dir, *args) == 1
    assert capsys.readouterr().out == ""
    assert not (output_dir / handoff.RESULT_FILENAME).exists()
    assert not any(path.name.startswith(".project-handoff") for path in output_dir.iterdir())
    assert (output_dir / handoff.DIAGNOSTIC_FILENAME).exists() is write_diagnostics


@pytest.mark.parametrize("write_diagnostics", [False, True])
def test_partial_temporary_write_is_cleaned_up(tmp_path, monkeypatch, capsys, write_diagnostics):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_fdopen = handoff.os.fdopen

    class FailingStream:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return self.stream.__exit__(*args)

        def write(self, content):
            if content.startswith('{\n  "context":'):
                self.stream.write(content[:5])
                raise OSError("synthetic partial write")
            return self.stream.write(content)

    def failing_fdopen(descriptor, mode, *args, **kwargs):
        stream = original_fdopen(descriptor, mode, *args, **kwargs)
        return FailingStream(stream) if "w" in mode else stream

    monkeypatch.setattr(handoff.os, "fdopen", failing_fdopen)
    args = ("--write-diagnostics",) if write_diagnostics else ()
    assert _run([source], output_dir, *args) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert not (output_dir / handoff.RESULT_FILENAME).exists()
    assert not any(path.name.startswith(".project-handoff") for path in output_dir.iterdir())
    assert (output_dir / handoff.DIAGNOSTIC_FILENAME).exists() is write_diagnostics, captured.err


def test_no_context_can_write_diagnostics_without_delivery(tmp_path, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run([source], output_dir, "--context-budget-chars", "0", "--write-diagnostics") == 3
    assert capsys.readouterr().out.strip() == "NO_CONTEXT"
    assert not (output_dir / handoff.RESULT_FILENAME).exists()
    assert _diagnostics(output_dir)["packet"]["compact_context_text"] == ""


def test_diagnostic_publication_failure_reports_error_without_result(tmp_path, monkeypatch, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_link = handoff.os.link

    def fail_diagnostic_link(source_path, target_path, *args, **kwargs):
        if Path(target_path).name == handoff.DIAGNOSTIC_FILENAME:
            raise OSError("synthetic diagnostic failure")
        return original_link(source_path, target_path, *args, **kwargs)

    monkeypatch.setattr(handoff.os, "link", fail_diagnostic_link)
    assert _run([source], output_dir, "--write-diagnostics") == 1
    assert capsys.readouterr().out == ""
    assert list(output_dir.iterdir()) == []


def test_existing_target_is_not_overwritten(tmp_path, capsys):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    result = output_dir / handoff.RESULT_FILENAME
    result.write_text("existing", encoding="utf-8")

    with pytest.raises(SystemExit) as captured:
        _run([source], output_dir)
    assert captured.value.code == 2
    assert result.read_text(encoding="utf-8") == "existing"
    assert capsys.readouterr().out == ""


def test_downstream_result_excludes_undelivered_text_and_diagnostics_are_opt_in(tmp_path):
    source = tmp_path / "source.txt"
    undelivered = "UNDELIVERED_UNIQUE_TEXT"
    source.write_text(f"alpha selected context\n{undelivered}\n", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    assert _run(
        [source], output_dir,
        "--max-segment-chars", "24",
        "--memory-limit", "2",
        "--context-budget-chars", "140",
        "--write-diagnostics",
    ) == 0

    result = _result(output_dir)
    diagnostics = _diagnostics(output_dir)
    assert set(result) == {"result_type", "context", "source_mappings"}
    assert undelivered not in json.dumps(result, ensure_ascii=False)
    assert len(result["source_mappings"]) == 1
    assert len(diagnostics["packet"]["selected_memories"]) == 2
    assert undelivered in diagnostics["input_candidates"][1]["content"]


def test_writes_only_the_single_result_file_in_the_explicit_output_directory(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("alpha completed capability", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    assert _run([source], output_dir) == 0

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert after == sorted(before + [Path("output") / handoff.RESULT_FILENAME])
