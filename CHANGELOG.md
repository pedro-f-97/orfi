# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.3.0] - 2026-09-11

### Added
- `ResultadosOperacao` dataclass: `organiza`, `datar`, `reverte` and `reverteDatar` now return counts of files handled and folders created/deleted.
- `-v`/`--version` flag.
- Dedicated tests for `mensagens.py`.

### Fixed
- Error handling around reading a corrupted or malformed `config.toml`.
- Incorrect "operation type" wording in summary messages.

## [1.2.0] - 2026-09-09

### Added
- Multi-language support (Portuguese/English) via `-i`/`--idioma`, persisted in `config.toml`.
- `LICENSE` (MIT).

### Fixed
- `eliminaPastasVazias` not detecting folders that would become empty during a `--simula` run.
- Dangling reference to a removed `CoresTexto` location, causing a crash on an unexpected `Modo`.

### Changed
- Log messages changed to English.

## [1.1.2] - 2026-09-07

### Added
- Docstrings across the entire codebase.

## [1.1.1] - 2026-09-07

### Added
- `-f`/`--force` flag to skip confirmation prompts.
- `-s`/`--simula` flag (dry-run mode).

## [1.1.0] - 2026-09-03

### Added
- Logging system (`orfi.log`, rotating file handler).
- CI pipeline (GitHub Actions: tests + lint).
- Protection against unexpected CLI arguments.

## [1.0.0] - 2026-09-03

### Added
- Copy mode (`-c`/`--copiar`), alongside the existing move behavior.
- File dating (`-d`/`--datar`) and reverting dated names.
- Error handling for file copy/move operations.
- Extensive test coverage across all modules.

## [0.1.0] - 2026-09-01

### Added
- Initial release as an installable package (`orfi` command).
- TOML-based configuration, with a cross-platform config path.
- Category validation (duplicate extensions, duplicate categories, malformed extensions, multiple default categories).