from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = PROJECT_ROOT / "scripts" / "install_memory_fabric_shim.py"


def _load_installer():
    spec = importlib.util.spec_from_file_location("install_memory_fabric_shim", INSTALLER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_installer_writes_expected_files_and_summary(tmp_path, capsys):
    installer = _load_installer()

    assert installer.main(["--hermes-home", str(tmp_path)]) == 0

    output = capsys.readouterr().out
    assert "Hermes Memory Fabric shim installer" in output
    assert f"Hermes home: {tmp_path}" in output
    assert "auth.json: not touched" in output
    assert "provider tool exposure: unchanged" in output
    assert "real model calls: none" in output

    shim_dir = tmp_path / "plugins" / "memory-fabric"
    assert (shim_dir / "__init__.py").read_text(encoding="utf-8") == installer.INIT_PY_CONTENT
    assert (shim_dir / "plugin.yaml").read_text(encoding="utf-8") == installer.PLUGIN_YAML_CONTENT


def test_installer_is_idempotent(tmp_path):
    installer = _load_installer()

    first = installer.install_shim(tmp_path)
    second = installer.install_shim(tmp_path)

    assert [item.action for item in first.files] == ["created", "created"]
    assert [item.action for item in second.files] == ["unchanged", "unchanged"]

    shim_dir = tmp_path / "plugins" / "memory-fabric"
    assert (shim_dir / "__init__.py").read_text(encoding="utf-8") == installer.INIT_PY_CONTENT
    assert (shim_dir / "plugin.yaml").read_text(encoding="utf-8") == installer.PLUGIN_YAML_CONTENT


def test_dry_run_does_not_write_files(tmp_path, capsys):
    installer = _load_installer()

    assert installer.main(["--hermes-home", str(tmp_path), "--dry-run"]) == 0

    output = capsys.readouterr().out
    assert "Mode: dry-run" in output
    assert "would create" in output
    assert not (tmp_path / "plugins").exists()


def test_shim_init_content_registers_memory_provider():
    installer = _load_installer()

    assert "from hermes_memory_fabric.provider import MemoryFabricProvider" in installer.INIT_PY_CONTENT
    assert "def register(ctx):" in installer.INIT_PY_CONTENT
    assert "ctx.register_memory_provider(MemoryFabricProvider())" in installer.INIT_PY_CONTENT


def test_plugin_yaml_content():
    installer = _load_installer()

    assert installer.PLUGIN_YAML_CONTENT == (
        "name: memory-fabric\n"
        "description: Civilization Core / Hermes Memory Fabric read-only provider shim.\n"
    )
