#!/usr/bin/env python3
"""Generate CC and Codex marketplace manifests from registry/plugins.json.

Phase 0a: CC output only. Codex generation stubbed (enabled in Phase 0b).
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "plugins.json"
CC_OUTPUT = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CODEX_OUTPUT = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


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


def generate_codex_manifest(registry):
    """Emit .agents/plugins/marketplace.json in Codex format.

    Phase 0b: Currently stubbed. Will be enabled after repo 1 (jenkins-cli)
    has .codex-plugin/plugin.json committed.
    """
    # TODO: Phase 0b — enable after first plugin repo is migrated
    return None


class CompactArrayEncoder(json.JSONEncoder):
    """JSON encoder that keeps short arrays on one line."""

    def encode(self, o):
        result = super().encode(o)
        # Collapse arrays of strings onto single lines
        import re

        def collapse_array(match):
            inner = match.group(1)
            # Only collapse if all elements are simple strings
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

    # Phase 0a: CC manifest
    cc = generate_cc_manifest(registry)
    write_json(CC_OUTPUT, cc)
    print(f"Generated CC manifest: {CC_OUTPUT}")

    # Phase 0b: Codex manifest (stubbed)
    codex = generate_codex_manifest(registry)
    if codex:
        write_json(CODEX_OUTPUT, codex)
        print(f"Generated Codex manifest: {CODEX_OUTPUT}")
    else:
        print("Codex manifest: stubbed (Phase 0b)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
