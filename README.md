# Skills Marketplace

Central plugin marketplace for AI coding assistants.

## Installation

### Claude Code

```bash
# Add marketplace (one-time)
/plugin marketplace add avivsinai/skills-marketplace

# List available plugins
/plugin list avivsinai-marketplace

# Install plugins
/plugin install amq-cli@avivsinai-marketplace
```

## Available Plugins

| Plugin | Description | Source |
|--------|-------------|--------|
| `amq-cli` | Agent Message Queue - atomic Maildir-style message delivery | [agent-message-queue](https://github.com/avivsinai/agent-message-queue) |

## Adding New Plugins

Edit `.claude-plugin/marketplace.json` to add new plugins:

```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "avivsinai/my-project"
  },
  "description": "What this plugin does",
  "version": "1.0.0"
}
```

Each referenced project must have a valid plugin structure with `.claude/skills/` or plugin.json.

## License

MIT
