# Contributing

Thanks for your interest in contributing to this skills marketplace!

## Marketplace Scope

This repository distributes plugins developed and maintained by Aviv Sinai. It does not accept third-party plugin listings.

Contributions to an existing plugin should be made in the source repository listed in the [README](README.md). Contributions to this repository's marketplace infrastructure and documentation are welcome.

## Repository Changes

- `registry/plugins.json` is the source of truth.
- Generated files under `.claude-plugin/`, `.agents/plugins/`, and `plugins/` must not be edited by hand.
- Run `python3 scripts/generate-manifests.py` after an approved registry change.
- Test infrastructure and documentation changes before submitting a pull request.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
