# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.5.1] - 2026-09-17

### Fixed
- Fixed an issue where dating and reverting the dating recursively could incorrectly move files to the base directory.

## [1.5.0] - 2026-09-17

### Added
- `--depth` flag: `organize`, `date`, and `revert --date` operations can now recurse into subfolders, down to a specified depth.
- Detection of missing/empty language or categories in `config.toml`, with a clear warning instead of silently treating the folder as if there was nothing to organize (helps catch an outdated or incompatible config file after an upgrade).

### Fixed
- Extension detection was missing files found only in subfolders, in recursive mode.
- `--depth` now correctly validated as an integer greater than 0.
- Copying or moving a file onto itself — e.g. when recursive mode revisits a category folder `orfi` itself created — is now skipped instead of being silently treated (and reported) as a successful move.

## [1.4.1] - 2026-09-16

### Added

- Translation of the help messages for the `-h`/`--help` and `-V`/`--version` arguments according to the selected language.

### Changed

- CLI arguments renamed to follow more common conventions (`--target`, `--copy`, `--revert`, `--date`, `--yes`, `--dry-run`, `--language`).
- Default configuration keys and categories changed to English.
- `executar()` now guarantees that the process completion and duration are logged, including when the process exits early or an exception occurs.

### Fixed

- Tests and documentation updated to reflect the CLI and `config.toml` changes.

## [1.4.0] - 2026-09-15

### Added
- `__version__` exposed in `orfi/__init__.py` via `importlib.metadata`.
- Atomic config file writes, protecting `config.toml` against corruption from an interrupted write.
- Graceful error handling in `main()`: `Ctrl+C` now exits cleanly with code `130`, and any unexpected exception is caught and shown as a friendly message instead of a raw traceback.
- `podeSubstituir`: shared validation extracted from `copiaFicheiro`/`moveFicheiro`, reducing duplication.
- Dedicated tests for error handling in `main()`, the `-i`/`--idioma` argument, and invalid-language handling not overwriting `config.toml`.

### Changed
- Language and categories are now loaded from `config.toml` in a single read, instead of separately.
- `main()` now returns a proper exit code on failure, instead of always exiting successfully.

### Fixed
- `orfi` no longer requires `tkinter` to run at all — it's now only imported when `-a`/`--alvo` is actually used, with a clear message if it's unavailable.
- Tests no longer abort the entire suite when `tkinter` isn't installed (`test_alvo.py` is skipped instead).
- `criaPastas` no longer crashes if it fails to create a category folder — the error is now handled and reported.
- `configuraLogs` no longer crashes if it can't create the logs folder — it now degrades gracefully without file logging instead.
- `apagaFicheiro` was reporting the wrong exception object in its error message.
- `eliminaPastasVazias` was counting a folder as deleted even when deletion failed.

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