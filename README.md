# Skills Marketplace

[![Validate](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Central plugin marketplace for **Claude Code**. This is a **registry** that points to plugins in their source repos - no duplication.

> **Cross-platform?** These skills are also published to [skild.sh](https://skills.sh) for use with Claude, Codex, Copilot, Cursor, Windsurf, and more:
> ```bash
> npx skild install amq-cli
> npx skild install langfuse
> npx skild install sabx
> npx skild install bkt
> npx skild install jk
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

All plugins use the default branch (`main` or `master`) - you always get the latest version from the source repo.

## Architecture

This marketplace is a **registry/index** - plugins live in their source repos:

```
skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json    # Registry pointing to source repos
└── README.md

# Plugins live in their own repos:
agent-message-queue/
├── .claude-plugin/
│   └── plugin.json         # Plugin manifest
├── skills/
│   └── amq-cli/SKILL.md    # Plugin skills (for Claude Code)
├── .claude/skills/         # Project-scoped skills
└── .codex/skills/          # Codex-compatible skills
```

When you install a plugin via the marketplace, it fetches from the source repo.

## Adding a Plugin

To add your plugin to this marketplace:

1. Ensure your repo has `.claude-plugin/plugin.json` (for Claude Code)
2. Add skills to `skills/<name>/SKILL.md` (for plugin distribution)
3. Submit a PR adding your plugin to `.claude-plugin/marketplace.json`

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Standards

All plugins follow the [Agent Skills specification](https://agentskills.io/specification), ensuring compatibility with:
- Claude Code
- Codex CLI
- Other Agent Skills-compatible tools

## License

MIT
