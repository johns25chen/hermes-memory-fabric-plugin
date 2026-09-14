# Hermes Integration

This package exposes `MemoryFabricProvider` through Python entry points, but
Hermes memory provider runtime also uses a directory-based loader in
`plugins.memory`. The shim, first introduced with an older package release,
makes those two discovery paths agree without changing Memory Fabric provider
behavior. The shim has no independent runtime version: `6.16.0` below is the
`hermes-memory-fabric-plugin` distribution version, not a Hermes version.

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
`$HERMES_HOME/plugins/`. The shim gives this loader a concrete
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

For the current `6.16.0` repository state, use a normally built wheel installed
in an isolated environment. The interpreter must also resolve a real local
Hermes `plugins.memory` loader and its already-installed dependencies. Keep the
isolated environment's site-packages ahead of any reused dependency path, and
verify module origins before running:

```bash
r9_hermes_home="/exclusive/evidence/directory/hermes-home"
r9_python="/exclusive/evidence/directory/hermes-isolated-venv/bin/python"
PYTHONDONTWRITEBYTECODE=1 "$r9_python" \
  scripts/install_memory_fabric_shim.py --hermes-home "$r9_hermes_home"
HERMES_HOME="$r9_hermes_home" EXPECTED_VERSION=6.16.0 \
  PYTHON="$r9_python" PYTHONPATH= \
  bash scripts/smoke_memory_fabric_hermes.sh
```

The smoke checks package version `6.16.0`, both declared entry points, the shim
files, Hermes `plugins.memory` discovery, provider loading, provider name,
empty provider tool schemas, and the `build_active_context` method. It does not
call a real model. A successful isolated run on 2026-09-14 loaded package
metadata and `hermes_memory_fabric` from the isolated installation while
loading `plugins.memory` from the existing local Hermes checkout. That Hermes
runtime reported `hermes-agent==0.18.2`; it is distinct from the plugin package
version `6.16.0`. Importing the Hermes loader also created its default
`SOUL.md` under the fresh `HERMES_HOME`; no default Hermes home was used.

The following optional real-chat check is outside isolated/no-model validation
and requires separate model and network authorization:

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
