from __future__ import annotations

import importlib
import importlib.metadata
import sys
import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _project_entry_points() -> dict[str, dict[str, str]]:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["entry-points"]


def _write_dist_info_with_entry_points(tmp_path: Path, entry_points: dict[str, dict[str, str]]) -> Path:
    site_packages = tmp_path / "site-packages"
    dist_info = site_packages / "hermes_memory_fabric_plugin-0.6.0.dist-info"
    dist_info.mkdir(parents=True)
    (dist_info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: hermes-memory-fabric-plugin\nVersion: 0.6.0\n",
        encoding="utf-8",
    )
    entry_points_text = "\n".join(
        f"[{group}]\n"
        + "\n".join(f"{name} = {value}" for name, value in sorted(entries.items()))
        for group, entries in sorted(entry_points.items())
    )
    (dist_info / "entry_points.txt").write_text(entry_points_text + "\n", encoding="utf-8")
    return site_packages


def _matching_entry_point(group: str, name: str, value: str) -> importlib.metadata.EntryPoint:
    for entry_point in importlib.metadata.entry_points().select(group=group):
        if entry_point.name == name and entry_point.value == value:
            return entry_point
    raise AssertionError(f"missing entry point {group}:{name} = {value}")


def test_pyproject_declares_memory_provider_and_generic_plugin_entry_points():
    entry_points = _project_entry_points()

    assert entry_points["hermes.memory_providers"]["memory-fabric"] == "hermes_memory_fabric:register"
    assert entry_points["hermes_agent.plugins"]["memory-fabric"] == "hermes_memory_fabric"


def test_importlib_metadata_discovers_declared_entry_point_groups(tmp_path, monkeypatch):
    site_packages = _write_dist_info_with_entry_points(tmp_path, _project_entry_points())
    monkeypatch.syspath_prepend(str(site_packages))
    sys.path_importer_cache.pop(str(site_packages), None)
    importlib.invalidate_caches()

    provider_entry_point = _matching_entry_point(
        "hermes.memory_providers",
        "memory-fabric",
        "hermes_memory_fabric:register",
    )
    plugin_entry_point = _matching_entry_point(
        "hermes_agent.plugins",
        "memory-fabric",
        "hermes_memory_fabric",
    )

    assert provider_entry_point.load() is importlib.import_module("hermes_memory_fabric").register
    assert plugin_entry_point.load() is importlib.import_module("hermes_memory_fabric")
