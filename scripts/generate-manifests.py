#!/usr/bin/env python3
"""Generate CC and Codex marketplace manifests from registry/plugins.json.

Phase 0a: CC manifest from registry.
Phase 0b: Codex manifest + local plugin bundles from source repos.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "plugins.json"
CC_OUTPUT = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CODEX_OUTPUT = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

# Plugin-root artifacts to copy into Codex bundles
CODEX_BUNDLE_ARTIFACTS = [
    ".codex-plugin",
    "skills",
    ".mcp.json",
    ".app.json",
    "assets",
]


def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def generate_cc_manifest(registry):
    """Emit .claude-plugin/marketplace.json in CC format."""
    manifest = {
        "name": registry["name"],
        "owner": registry["owner"],
        "metadata": registry["metadata"],
        "plugins": [],
    }
    for plugin in registry["plugins"]:
        entry = {
            "name": plugin["name"],
            "source": {
                "source": "url",
                "url": f"{plugin['repository']}.git",
            },
            "description": plugin["description"],
            "keywords": plugin["keywords"],
        }
        manifest["plugins"].append(entry)
    return manifest


def clone_and_bundle(plugin, dest_dir):
    """Clone a plugin's source repo at pinned ref and extract Codex bundle artifacts."""
    repo_url = plugin["repository"]
    name = plugin["name"]
    ref = plugin.get("ref")
    expected_version = plugin.get("version")
    bundle_dir = dest_dir / name

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = Path(tmpdir) / "repo"

        # Clone at pinned ref if available, otherwise default branch
        clone_cmd = ["git", "clone", "--single-branch", repo_url, str(clone_dir)]
        if not ref:
            clone_cmd.insert(2, "--depth=1")

        result = subprocess.run(clone_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  WARNING: failed to clone {repo_url}: {result.stderr.strip()}")
            return False

        # Checkout pinned ref
        if ref:
            result = subprocess.run(
                ["git", "-C", str(clone_dir), "checkout", ref],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  WARNING: failed to checkout {ref}: {result.stderr.strip()}")
                return False

        # Check for .codex-plugin/plugin.json
        codex_manifest_path = clone_dir / ".codex-plugin" / "plugin.json"
        if not codex_manifest_path.exists():
            print(f"  SKIP: {name} has no .codex-plugin/plugin.json")
            return False

        # Verify version matches registry
        if expected_version:
            with open(codex_manifest_path) as f:
                manifest_data = json.load(f)
            actual_version = manifest_data.get("version")
            if actual_version and actual_version != expected_version:
                print(f"  ERROR: {name} version mismatch — registry: {expected_version}, manifest: {actual_version}")
                return False

        # Copy artifacts
        bundle_dir.mkdir(parents=True, exist_ok=True)
        copied = []
        for artifact in CODEX_BUNDLE_ARTIFACTS:
            src = clone_dir / artifact
            dst = bundle_dir / artifact
            if src.exists():
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst, symlinks=False)
                else:
                    shutil.copy2(src, dst)
                copied.append(artifact)

        print(f"  {name}: bundled [{', '.join(copied)}] @ {ref[:12] if ref else 'HEAD'}")
        return True


def generate_codex_manifest(registry):
    """Emit .agents/plugins/marketplace.json in Codex format + local bundles."""
    # Clean and rebuild plugins dir
    if PLUGINS_DIR.exists():
        shutil.rmtree(PLUGINS_DIR)
    PLUGINS_DIR.mkdir(parents=True)

    manifest = {
        "name": registry["name"],
        "interface": registry.get("interface", {}),
        "plugins": [],
    }

    for plugin in registry["plugins"]:
        print(f"Bundling {plugin['name']}...")
        if clone_and_bundle(plugin, PLUGINS_DIR):
            entry = {
                "name": plugin["name"],
                "source": {
                    "source": "local",
                    "path": f"./plugins/{plugin['name']}",
                },
                "policy": plugin.get("policy", {
                    "installation": "AVAILABLE",
                    "authentication": "ON_FIRST_USE",
                }),
                "category": plugin.get("category", "Developer Tools"),
            }
            manifest["plugins"].append(entry)

    return manifest if manifest["plugins"] else None


class CompactArrayEncoder(json.JSONEncoder):
    """JSON encoder that keeps short arrays on one line."""

    def encode(self, o):
        result = super().encode(o)

        def collapse_array(match):
            inner = match.group(1)
            items = [s.strip() for s in inner.split("\n") if s.strip()]
            if all(s.startswith('"') or s.startswith("]") or s == "" for s in items):
                cleaned = ", ".join(s.rstrip(",") for s in items if s and s != "]")
                return f"[{cleaned}]"
            return match.group(0)

        result = re.sub(
            r'\[\s*\n((?:\s*"[^"]*",?\s*\n)+)\s*\]',
            collapse_array,
            result,
        )
        return result


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(CompactArrayEncoder(indent=2).encode(data))
        f.write("\n")


def main():
    registry = load_registry()

    # CC manifest
    cc = generate_cc_manifest(registry)
    write_json(CC_OUTPUT, cc)
    print(f"Generated CC manifest: {CC_OUTPUT}")

    # Codex manifest + bundles
    print("\n--- Codex bundles ---")
    codex = generate_codex_manifest(registry)
    if codex:
        write_json(CODEX_OUTPUT, codex)
        print(f"\nGenerated Codex manifest: {CODEX_OUTPUT}")
        print(f"Bundled {len(codex['plugins'])} plugins into {PLUGINS_DIR}")
    else:
        # Remove stale Codex manifest if no plugins were bundled
        if CODEX_OUTPUT.exists():
            CODEX_OUTPUT.unlink()
            print(f"\nRemoved stale Codex manifest: {CODEX_OUTPUT}")
        print("No Codex-ready plugins found")

    return 0


if __name__ == "__main__":
    sys.exit(main())
