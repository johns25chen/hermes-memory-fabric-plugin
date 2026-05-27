from __future__ import annotations

import json

from hermes_memory_fabric.candidate_jsonl_source import load_candidate_jsonl_source


def _jsonl_line(**payload) -> str:
    return json.dumps(payload, sort_keys=True) + "\n"


def test_loads_valid_jsonl_candidates(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(id="one", content="Hermes JSONL candidate one.")
        + _jsonl_line(id="two", content="Hermes JSONL candidate two."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path)

    assert [candidate["id"] for candidate in candidates] == ["one", "two"]
    assert candidates[0]["content"] == "Hermes JSONL candidate one."


def test_ignores_blank_lines(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        "\n"
        + _jsonl_line(id="one", content="Hermes JSONL candidate one.")
        + "   \n"
        + _jsonl_line(id="two", content="Hermes JSONL candidate two."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path)

    assert [candidate["id"] for candidate in candidates] == ["one", "two"]


def test_ignores_invalid_lines_by_default(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(id="valid", content="Hermes valid JSONL candidate.")
        + "not-json\n"
        + "[1, 2, 3]\n"
        + _jsonl_line(id="also-valid", content="Hermes also valid JSONL candidate."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path)

    assert [candidate["id"] for candidate in candidates] == ["valid", "also-valid"]


def test_strict_invalid_lines_return_no_candidates(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(id="valid", content="Hermes valid JSONL candidate.")
        + "not-json\n"
        + _jsonl_line(id="also-valid", content="Hermes also valid JSONL candidate."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path, ignore_invalid_lines=False)

    assert candidates == []


def test_required_fields_filter_invalid_objects_by_default(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(id="missing-content")
        + _jsonl_line(id="complete", content="Hermes complete JSONL candidate."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path, required_fields=["id", "content"])

    assert [candidate["id"] for candidate in candidates] == ["complete"]


def test_caps_max_lines(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(id="one", content="Hermes JSONL candidate one.")
        + _jsonl_line(id="two", content="Hermes JSONL candidate two.")
        + _jsonl_line(id="three", content="Hermes JSONL candidate three."),
        encoding="utf-8",
    )

    candidates = load_candidate_jsonl_source(path, max_lines=2)

    assert [candidate["id"] for candidate in candidates] == ["one", "two"]


def test_caps_max_bytes(tmp_path):
    path = tmp_path / "candidates.jsonl"
    first_line = _jsonl_line(id="one", content="Hermes JSONL candidate one.")
    second_line = _jsonl_line(id="two", content="Hermes JSONL candidate two.")
    path.write_text(first_line + second_line, encoding="utf-8")

    candidates = load_candidate_jsonl_source(path, max_bytes=len(first_line.encode("utf-8")))

    assert [candidate["id"] for candidate in candidates] == ["one"]


def test_missing_file_returns_no_candidates(tmp_path):
    path = tmp_path / "missing.jsonl"

    assert load_candidate_jsonl_source(path) == []


def test_directory_path_returns_no_candidates(tmp_path):
    directory = tmp_path / "candidate-dir"
    directory.mkdir()

    assert load_candidate_jsonl_source(directory) == []


def test_no_files_are_created_for_missing_or_remote_sources(tmp_path):
    missing = tmp_path / "missing.jsonl"
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    assert load_candidate_jsonl_source(missing) == []
    assert load_candidate_jsonl_source("https://example.test/candidates.jsonl") == []

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert after == before == []


def test_loaded_candidates_are_defensively_copied(tmp_path):
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        _jsonl_line(
            id="selected",
            content="Hermes defensive copy JSONL candidate.",
            governance={"read_only": True, "nested": {"safe": True}},
        ),
        encoding="utf-8",
    )

    first = load_candidate_jsonl_source(path)
    first[0]["governance"]["nested"]["safe"] = False
    second = load_candidate_jsonl_source(path)

    assert second[0]["governance"]["nested"]["safe"] is True
