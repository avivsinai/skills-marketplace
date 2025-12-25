# Contributing

Thanks for your interest in contributing to this skills marketplace!

## Adding a Plugin

1. Ensure your plugin repo has the required structure:
   ```
   .claude/skills/<skill-name>/
   ├── SKILL.md      # Required: YAML frontmatter + instructions
   └── plugin.json   # Optional: plugin metadata
   ```

2. Fork this repository and edit `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "your-skill",
     "source": {
       "source": "github",
       "repo": "your-username/your-repo"
     },
     "description": "What it does and when to use it",
     "version": "1.0.0"
   }
   ```

3. Submit a pull request with:
   - Link to your plugin repository
   - Brief description of what the plugin does
   - Confirmation that it follows the [Agent Skills standard](https://agentskills.io/specification)

## Requirements

- Plugin repos must be public
- Skills must follow the Agent Skills specification
- Include a LICENSE file in your plugin repo
- Test your skill before submitting

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
