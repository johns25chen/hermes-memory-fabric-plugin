# Hermes Integration

This package exposes `MemoryFabricProvider` through Python entry points, but
Hermes memory provider runtime also uses a directory-based loader in
`plugins.memory`. The v0.8.0 shim makes those two discovery paths agree without
changing Memory Fabric provider behavior.

## Why The Shim Exists

The installed pip package declares a generic Hermes plugin and a memory provider
entry point. Hermes can discover those entry points, but the runtime path used
by memory status and provider activation loads memory providers from
`$HERMES_HOME/plugins/<provider-name>/`.

The shim installed at `~/.hermes/plugins/memory-fabric/` is a tiny directory
plugin. Its `__init__.py` imports `MemoryFabricProvider` from the installed
package and registers it with `ctx.register_memory_provider(...)`. It does not
store secrets, does not edit `auth.json`, does not change provider tool
exposure, and does not call a model.

## Entry Points Vs Directory Loader

`[project.entry-points."hermes_agent.plugins"]` declares a generic Hermes
plugin package:

```toml
[project.entry-points."hermes_agent.plugins"]
memory-fabric = "hermes_memory_fabric"
```

That entry point is useful for generic plugin discovery. It is not the same as
the directory-based memory provider loader.

Hermes memory provider runtime uses `plugins.memory.discover_memory_providers()`
and `plugins.memory.load_memory_provider("memory-fabric")`. That loader scans
bundled memory provider directories and user-installed directories under
`$HERMES_HOME/plugins/`. The v0.8.0 shim gives this loader a concrete
`memory-fabric` directory provider that delegates to the installed package.

The package also keeps the memory-provider entry point:

```toml
[project.entry-points."hermes.memory_providers"]
memory-fabric = "hermes_memory_fabric:register"
```

This remains declared for compatibility, but the directory shim is required for
the current Hermes `plugins.memory` runtime path.

## Install

From this repository:

```bash
python scripts/install_memory_fabric_shim.py
```

Use a non-default Hermes home for testing:

```bash
python scripts/install_memory_fabric_shim.py --hermes-home /tmp/hermes-memory-fabric-smoke
```

Preview without writing files:

```bash
python scripts/install_memory_fabric_shim.py --dry-run
```

The installer creates or updates:

```text
~/.hermes/plugins/memory-fabric/__init__.py
~/.hermes/plugins/memory-fabric/plugin.yaml
```

## Smoke

Run the local smoke script after installing the package and shim:

```bash
PYTHON=/Users/han/.hermes/hermes-agent/.venv/bin/python bash scripts/smoke_memory_fabric_hermes.sh
```

The smoke checks package version `0.8.0`, both declared entry points, the shim
files, Hermes `plugins.memory` discovery, provider loading, provider name,
empty provider tool schemas, and the `build_active_context` method. It does not
call a real model.

Optional real chat smoke:

```bash
hermes chat -Q -q "Reply exactly and only with this token: MEMORY_FABRIC_CHATQ_OK"
```

## Rollback

Remove the directory shim:

```bash
rm -rf ~/.hermes/plugins/memory-fabric
```

If any manual Hermes configuration changes were made while testing, restore
`~/.hermes/config.yaml` from your backup. The shim installer itself does not
modify `config.yaml` or `auth.json`.

## Current Acceptance Criteria

- `~/.hermes/plugins/memory-fabric/__init__.py` imports
  `MemoryFabricProvider` from `hermes_memory_fabric.provider`.
- `register(ctx)` calls
  `ctx.register_memory_provider(MemoryFabricProvider())`.
- `~/.hermes/plugins/memory-fabric/plugin.yaml` contains:

```yaml
name: memory-fabric
description: Civilization Core / Hermes Memory Fabric read-only provider shim.
```

- The installer is idempotent and supports `--hermes-home`, `--dry-run`, and
  `--force`.
- The installer does not store secrets, modify `~/.hermes/auth.json`, change
  provider tool exposure, or call any real model.
- `plugins.memory.discover_memory_providers()` includes `memory-fabric`.
- `plugins.memory.load_memory_provider("memory-fabric")` returns a provider.
- `provider.name == "memory-fabric"`.
- `provider.get_tool_schemas() == []`.
- The provider has `build_active_context`.
- Optional real chat smoke returns exactly `MEMORY_FABRIC_CHATQ_OK`.
