# Skills Marketplace

[![Validate](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Central plugin marketplace for **Claude Code** and **Codex**. This repo is a registry plus generated distribution artifacts. Plugin source stays in the child repos.

> **Cross-platform?** These skills work with Claude Code, Codex CLI, Copilot, Cursor, Windsurf, and more.
>
> **Via [skild.sh](https://skild.sh)** (registry-based):
> ```bash
> npx skild install @avivsinai/amq-cli
> npx skild install @avivsinai/langfuse
> npx skild install @avivsinai/sabx
> npx skild install @avivsinai/bkt
> npx skild install @avivsinai/jk
> ```
>
> **Via [skills.sh](https://skills.sh)** (GitHub-based):
> ```bash
> npx skills add avivsinai/agent-message-queue
> npx skills add avivsinai/langfuse-mcp
> npx skills add avivsinai/sabx
> npx skills add avivsinai/bitbucket-cli
> npx skills add avivsinai/jenkins-cli
> ```

## Installation (Claude Code)

```bash
# Add marketplace (one-time)
/plugin marketplace add avivsinai/skills-marketplace

# Install plugins
/plugin install amq-cli@avivsinai-marketplace
/plugin install langfuse@avivsinai-marketplace
/plugin install sabx@avivsinai-marketplace
/plugin install bkt@avivsinai-marketplace
/plugin install jk@avivsinai-marketplace
```

## Available Plugins

| Plugin | Description | Source |
|--------|-------------|--------|
| `amq-cli` | Agent Message Queue - atomic Maildir-style message delivery with co-op mode | [agent-message-queue](https://github.com/avivsinai/agent-message-queue) |
| `langfuse` | Langfuse observability - query traces, debug exceptions, analyze sessions, manage prompts | [langfuse-mcp](https://github.com/avivsinai/langfuse-mcp) |
| `sabx` | SABnzbd CLI - control downloads, queues, RSS feeds, and automation | [sabx](https://github.com/avivsinai/sabx) |
| `bkt` | Bitbucket CLI - manage repos, PRs, branches, issues, webhooks, pipelines (DC & Cloud) | [bitbucket-cli](https://github.com/avivsinai/bitbucket-cli) |
| `jk` | Jenkins CLI - manage jobs, pipelines, runs, logs, artifacts, credentials, nodes | [jenkins-cli](https://github.com/avivsinai/jenkins-cli) |

Plugins are pinned by the registry to either a release tag or a commit SHA. Claude Code and Codex artifacts are generated from those pinned refs so installs are reproducible.

## Architecture

This marketplace is **registry-first**. `registry/plugins.json` is the only file you edit by hand; everything else is generated from it.

```
skills-marketplace/
├── registry/
│   └── plugins.json              # Source of truth: plugin metadata, pins, sync policy
├── .claude-plugin/
│   └── marketplace.json          # Generated Claude Code marketplace catalog
├── .agents/plugins/
│   └── marketplace.json          # Generated Codex marketplace catalog
├── plugins/
│   └── <plugin>/...              # Generated Codex plugin bundles pinned to registry refs
└── scripts/
    ├── generate-manifests.py     # Regenerates all derived artifacts
    └── sync-releases.py          # Updates release-mode plugins from GitHub releases/tags

# Plugins live in their own repos:
agent-message-queue/
├── .claude-plugin/
│   └── plugin.json               # Claude Code plugin manifest
├── .codex-plugin/
│   └── plugin.json               # Codex plugin manifest
└── skills/
    └── ...                       # Shared skill payload
```

For Claude Code, the generated marketplace catalog points directly at pinned GitHub refs. For Codex, the repo also carries generated local bundles under `plugins/`.

## Auto-Sync

- Release-mode plugins in `registry/plugins.json` are checked by `.github/workflows/sync-releases.yml`.
- The workflow runs every 4 hours, can be triggered manually, and also accepts `repository_dispatch`.
- When a newer release tag is found, it updates `registry/plugins.json`, regenerates manifests, and opens or updates a PR instead of pushing directly to `main`.
- Plugins with `sync.mode: "manual"` stay pinned until someone updates the registry explicitly.

Today only plugins whose published release tags line up with their plugin manifest versions should use `sync.mode: "release"`.

## Adding a Plugin

To add your plugin to this marketplace:

1. Ensure your repo has `.claude-plugin/plugin.json` and, for Codex support, `.codex-plugin/plugin.json`
2. Add your plugin entry to `registry/plugins.json`
3. Run `python3 scripts/generate-manifests.py`
4. Submit a PR with the updated registry plus regenerated artifacts

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Standards

All plugins follow the [Agent Skills specification](https://agentskills.io/specification), ensuring compatibility with:
- Claude Code
- Codex CLI
- Other Agent Skills-compatible tools

## License

MIT
