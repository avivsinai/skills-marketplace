# Skills Marketplace

[![Validate](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/avivsinai/skills-marketplace/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Central plugin marketplace for AI coding assistants. Supports both Claude Code and Codex CLI.

## Installation

### Claude Code

```bash
# Add marketplace (one-time)
/plugin marketplace add avivsinai/skills-marketplace

# Install plugins
/plugin install amq-cli@avivsinai-marketplace
```

### Codex CLI

```bash
# Install from this marketplace
$skill-installer install https://github.com/avivsinai/skills-marketplace/tree/main/skills/amq-cli

# Or install directly from source repo
$skill-installer install https://github.com/avivsinai/agent-message-queue/tree/main/.codex/skills/amq-cli
```

## Available Plugins

| Plugin | Description | Source |
|--------|-------------|--------|
| `amq-cli` | Agent Message Queue - atomic Maildir-style message delivery | [agent-message-queue](https://github.com/avivsinai/agent-message-queue) |

## Adding a Plugin

See [CONTRIBUTING.md](CONTRIBUTING.md) for plugin submission guidelines.

## Structure

```
skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json    # Claude Code marketplace index
├── skills/
│   └── <skill-name>/
│       └── SKILL.md        # Codex-compatible skill files
├── .github/workflows/
│   └── validate.yml        # CI validation
└── README.md
```

## Standards

All skills follow the [Agent Skills specification](https://agentskills.io/specification), ensuring compatibility with:
- Claude Code
- Codex CLI
- GitHub Copilot
- Other Agent Skills-compatible tools

## License

MIT
