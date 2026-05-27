#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
EXPECTED_VERSION="${EXPECTED_VERSION:-0.8.0}"

export HERMES_HOME
export PYTHONPATH="$ROOT_DIR/src:$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export EXPECTED_VERSION

"$PYTHON" - <<'PY'
from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


expected_version = os.environ["EXPECTED_VERSION"]
try:
    version = importlib.metadata.version("hermes-memory-fabric-plugin")
except importlib.metadata.PackageNotFoundError as exc:
    raise SystemExit(
        "FAIL: hermes-memory-fabric-plugin package metadata is not installed; "
        "install it with python -m pip install -e ."
    ) from exc

if version != expected_version:
    fail(f"package version is {version!r}, expected {expected_version!r}")
ok(f"package version {version}")

entry_points = importlib.metadata.entry_points()


def require_entry_point(group: str, name: str, value: str) -> None:
    matches = [
        entry_point
        for entry_point in entry_points.select(group=group)
        if entry_point.name == name and entry_point.value == value
    ]
    if not matches:
        fail(f"missing entry point {group}:{name} = {value}")
    ok(f"entry point {group}:{name} = {value}")


require_entry_point("hermes.memory_providers", "memory-fabric", "hermes_memory_fabric:register")
require_entry_point("hermes_agent.plugins", "memory-fabric", "hermes_memory_fabric")

hermes_home = Path(os.environ["HERMES_HOME"]).expanduser()
shim_dir = hermes_home / "plugins" / "memory-fabric"
init_path = shim_dir / "__init__.py"
yaml_path = shim_dir / "plugin.yaml"
if not init_path.is_file():
    fail(f"shim __init__.py missing at {init_path}")
if not yaml_path.is_file():
    fail(f"shim plugin.yaml missing at {yaml_path}")
ok(f"shim exists at {shim_dir}")

import plugins.memory as memory_plugins

discovered = memory_plugins.discover_memory_providers()
matching = [item for item in discovered if item[0] == "memory-fabric"]
if not matching:
    fail("plugins.memory.discover_memory_providers() did not include memory-fabric")
if matching[0][2] is not True:
    fail("memory-fabric was discovered but is not available")
ok("plugins.memory.discover_memory_providers() includes available memory-fabric")

provider = memory_plugins.load_memory_provider("memory-fabric")
if provider is None:
    fail('plugins.memory.load_memory_provider("memory-fabric") returned None')
ok("plugins.memory.load_memory_provider(\"memory-fabric\") returned a provider")

if getattr(provider, "name", None) != "memory-fabric":
    fail(f"provider.name is {getattr(provider, 'name', None)!r}")
ok('provider.name == "memory-fabric"')

tool_schemas = provider.get_tool_schemas()
if tool_schemas != []:
    fail(f"provider.get_tool_schemas() returned {tool_schemas!r}, expected []")
ok("provider.get_tool_schemas() == []")

if not hasattr(provider, "build_active_context"):
    fail("provider does not have build_active_context")
ok("provider has build_active_context")

ok("no real model call was made")
PY
