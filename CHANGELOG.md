# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Issue templates for plugin requests and bug reports

## 2026-02-07

### Added

- yoetz plugin

## 2026-01-29

### Fixed

- Remove invalid `owner.url` field from marketplace schema
- Use correct source type `url` instead of `git` in schema

## 2026-01-27

### Fixed

- Use HTTPS URLs to avoid SSH auth issues

## 2026-01-23

### Added

- jk (jenkins-cli) plugin
- sabx plugin
- skild.sh and skills.sh installation methods in docs

### Fixed

- Correct branch ref for bkt skill

### Changed

- Updated langfuse skill description with datasets info

## 2026-01-19

### Added

- langfuse skill plugin
- skild.sh cross-platform install docs

## 2026-01-17

### Added

- gitleaks secret scanning and pre-commit hooks

## 2025-12-27

### Changed

- Use `ref:main` for always-latest plugin versions

## 2025-12-25

### Added

- Initial marketplace with amq-cli plugin
- OSS files and Codex support

### Fixed

- Remove invalid `category` key from plugin entry

### Changed

- Restructured as registry (removed local skill stubs)
- Clarified marketplace is for Claude Code only
