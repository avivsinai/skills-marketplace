# Contributing

Thanks for your interest in contributing to this skills marketplace!

## Adding a Plugin

1. Ensure your plugin repo has the required structure:
   ```
   .claude-plugin/plugin.json   # Claude Code manifest
   .codex-plugin/plugin.json    # Codex manifest (if Codex support is desired)
   skills/<skill-name>/SKILL.md # Skill payload
   ```

2. Fork this repository and edit `registry/plugins.json`.

   The registry entry is the source of truth. Generated marketplace files under `.claude-plugin/`, `.agents/plugins/`, and `plugins/` must not be edited by hand.

   Example entry:
   ```json
   {
     "name": "your-plugin",
     "description": "What it does and when to use it",
     "repository": "https://github.com/your-username/your-repo",
     "version": "1.0.0",
     "ref": "v1.0.0",
     "keywords": ["agents", "automation"],
     "category": "Developer Tools",
     "policy": {
       "installation": "AVAILABLE",
       "authentication": "ON_FIRST_USE"
     },
     "sync": {
       "mode": "manual"
     }
   }
   ```

3. Regenerate derived artifacts:
   ```bash
   python3 scripts/generate-manifests.py
   ```

4. Submit a pull request with:
   - Link to your plugin repository
   - Brief description of what the plugin does
   - Confirmation that it follows the [Agent Skills standard](https://agentskills.io/specification)
   - The updated registry and regenerated artifacts

## Sync Modes

- Use `"sync": {"mode": "release", "prereleases": false}` only if the child repo publishes GitHub release tags that match the plugin manifest version.
- Use `"sync": {"mode": "manual"}` when the registry should stay pinned to a specific commit or when release tags are not aligned yet.

## Requirements

- Plugin repos must be public
- Skills must follow the Agent Skills specification
- Include a LICENSE file in your plugin repo
- Test your skill before submitting
- Do not edit generated marketplace files by hand

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
