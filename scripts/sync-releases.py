#!/usr/bin/env python3
"""Sync registry/plugins.json against GitHub default-branch HEADs for main-mode plugins."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "plugins.json"
USER_AGENT = "skills-marketplace-sync/1.0"
SHORT_SHA_LEN = 12


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


def plugin_repo_slug(plugin):
    source = plugin.get("source", {})
    if isinstance(source, dict) and source.get("source") == "github" and source.get("repo"):
        return source["repo"]

    owner, repo = github_repo_slug(plugin["repository"])
    return f"{owner}/{repo}"


def split_repo_slug(repo_slug):
    owner, repo = repo_slug.split("/", 1)
    return owner, repo


def github_default_branch(owner, repo):
    repo_data = github_request_json(f"/repos/{owner}/{repo}")
    default_branch = repo_data.get("default_branch")
    if not default_branch:
        raise ValueError(f"missing default branch for {owner}/{repo}")
    return default_branch


def github_branch_head_sha(owner, repo, branch):
    encoded_branch = urllib.parse.quote(branch, safe="")
    commit = github_request_json(f"/repos/{owner}/{repo}/commits/{encoded_branch}")
    sha = commit.get("sha")
    if not sha:
        raise ValueError(f"missing HEAD sha for {owner}/{repo}@{branch}")
    return sha


def short_sha(sha):
    return sha[:SHORT_SHA_LEN]


def sync_registry(data, target_repo=None, dry_run=False):
    changed = False
    matched_target = False

    for plugin in data.get("plugins", []):
        repo_slug = plugin_repo_slug(plugin)
        if target_repo and repo_slug != target_repo:
            continue
        if target_repo:
            matched_target = True

        sync = plugin.get("sync", {})
        mode = sync.get("mode", "manual")
        if mode != "main":
            print(f"skip {plugin['name']}: sync.mode={mode}")
            continue

        owner, repo = split_repo_slug(repo_slug)
        default_branch = github_default_branch(owner, repo)
        sha = github_branch_head_sha(owner, repo, default_branch)
        version = short_sha(sha)

        current_version = plugin.get("version", "")
        current_source = plugin.get("source", {}) if isinstance(plugin.get("source"), dict) else {}
        current_ref = current_source.get("ref", "")
        current_sha = current_source.get("sha", "")
        desired_source = {
            "source": "github",
            "repo": repo_slug,
            "ref": default_branch,
            "sha": sha,
        }

        if current_version == version and current_source == desired_source and plugin.get("ref") is None:
            print(f"ok {plugin['name']}: already at {default_branch}@{version}")
            continue

        print(
            f"update {plugin['name']}: "
            f"{current_version}@{current_ref or '<none>'}:{current_sha[:SHORT_SHA_LEN] or '<none>'} "
            f"-> {default_branch}@{version}"
        )
        plugin["version"] = version
        plugin["source"] = desired_source
        plugin.pop("ref", None)
        changed = True

    if target_repo and not matched_target:
        raise ValueError(f"no registry entry matched repo {target_repo}")

    if changed and not dry_run:
        write_registry(data)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Sync main-mode plugins in registry/plugins.json")
    parser.add_argument("--dry-run", action="store_true", help="Show planned updates without writing files")
    parser.add_argument(
        "--repo",
        help="Only sync the plugin whose GitHub source repo matches this owner/name slug",
    )
    args = parser.parse_args()

    registry = load_registry()
    changed = sync_registry(registry, target_repo=args.repo, dry_run=args.dry_run)
    if args.dry_run:
        print("dry-run complete")
    elif changed:
        print(f"updated {REGISTRY}")
    else:
        print("no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
