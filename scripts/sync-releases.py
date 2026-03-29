#!/usr/bin/env python3
"""Sync registry/plugins.json against GitHub releases for release-mode plugins."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "plugins.json"
USER_AGENT = "skills-marketplace-sync/1.0"
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")


def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def write_registry(data):
    with open(REGISTRY, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def github_request_json(path):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.load(response)


def github_repo_slug(repo_url):
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != "github.com":
        raise ValueError(f"unsupported repository URL: {repo_url}")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"invalid GitHub repository URL: {repo_url}")
    owner, repo = parts[:2]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def normalize_version(tag_name):
    return tag_name[1:] if tag_name.startswith("v") else tag_name


def parse_semver(value):
    match = SEMVER_RE.match((value or "").strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def latest_release_tag(owner, repo, include_prereleases):
    if include_prereleases:
        releases = github_request_json(f"/repos/{owner}/{repo}/releases?per_page=20")
        for release in releases:
            if release.get("draft"):
                continue
            tag_name = release.get("tag_name")
            if tag_name:
                return tag_name
        return None

    try:
        release = github_request_json(f"/repos/{owner}/{repo}/releases/latest")
    except urllib.error.HTTPError as err:
        if err.code != 404:
            raise
        return None
    return release.get("tag_name")


def latest_tag(owner, repo, include_prereleases):
    tags = github_request_json(f"/repos/{owner}/{repo}/tags?per_page=100")
    candidates = []
    for tag in tags:
        name = tag.get("name")
        version = parse_semver(name)
        if version is None:
            continue
        if not include_prereleases and "-" in normalize_version(name):
            continue
        candidates.append((version, name))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][1]


def latest_sync_target(owner, repo, include_prereleases):
    tag_name = latest_release_tag(owner, repo, include_prereleases)
    if tag_name:
        return tag_name
    return latest_tag(owner, repo, include_prereleases)


def should_update(current_version, target_version):
    current_semver = parse_semver(current_version)
    target_semver = parse_semver(target_version)
    if current_semver and target_semver:
        return target_semver >= current_semver
    return current_version != target_version


def sync_registry(data, dry_run=False):
    changed = False
    for plugin in data.get("plugins", []):
        sync = plugin.get("sync", {})
        mode = sync.get("mode", "manual")
        if mode != "release":
            print(f"skip {plugin['name']}: sync.mode={mode}")
            continue

        include_prereleases = bool(sync.get("prereleases", False))
        owner, repo = github_repo_slug(plugin["repository"])
        tag_name = latest_sync_target(owner, repo, include_prereleases)
        if not tag_name:
            print(f"warn {plugin['name']}: no release/tag found")
            continue

        version = normalize_version(tag_name)
        current_version = plugin.get("version", "")
        current_ref = plugin.get("ref", "")
        if not should_update(current_version, version):
            print(
                f"warn {plugin['name']}: registry version {current_version} is newer than discovered {version}; leaving unchanged"
            )
            continue
        if current_version == version and current_ref == tag_name:
            print(f"ok {plugin['name']}: already at {tag_name}")
            continue

        print(f"update {plugin['name']}: {current_version}@{current_ref} -> {version}@{tag_name}")
        plugin["version"] = version
        plugin["ref"] = tag_name
        changed = True

    if changed and not dry_run:
        write_registry(data)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Sync release-mode plugins in registry/plugins.json")
    parser.add_argument("--dry-run", action="store_true", help="Show planned updates without writing files")
    args = parser.parse_args()

    registry = load_registry()
    changed = sync_registry(registry, dry_run=args.dry_run)
    if args.dry_run:
        print("dry-run complete")
    elif changed:
        print(f"updated {REGISTRY}")
    else:
        print("no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
