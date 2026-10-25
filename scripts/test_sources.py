"""The Claude-only subdirectory source survives generation and main sync."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


def load_script(name):
    path = Path(__file__).with_name(name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate = load_script("generate-manifests")
sync = load_script("sync-releases")


class SourceTests(unittest.TestCase):
    def test_main_sync_keeps_the_claude_plugin_subdirectory(self):
        # AMQ's /board plugin lives below the repository root. The old
        # generator dropped its path and main sync replaced its source kind.
        old_sha, new_sha = "a" * 40, "b" * 40
        source = {
            "source": "git-subdir",
            "url": "https://github.com/example/plugins.git",
            "path": "plugins/board",
            "ref": "main",
            "sha": old_sha,
        }
        plugin = {
            "name": "board",
            "repository": "https://github.com/example/plugins",
            "source": dict(source),
            "version": old_sha[:12],
            "sync": {"mode": "main"},
        }
        self.assertEqual(generate.build_claude_source(plugin), source)
        registry = {"plugins": [plugin]}
        with patch.object(sync, "github_default_branch", return_value="main"), patch.object(
            sync, "github_branch_head_sha", return_value=new_sha
        ), patch.object(sync, "write_registry") as write:
            self.assertTrue(sync.sync_registry(registry))
            write.assert_called_once_with(registry)
            expected = dict(source, sha=new_sha)
            self.assertEqual(plugin["version"], new_sha[:12])
            self.assertEqual(plugin["source"], expected)
            self.assertEqual(generate.build_claude_source(plugin), expected)
            self.assertFalse(sync.sync_registry(registry))


if __name__ == "__main__":
    unittest.main()
