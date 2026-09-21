🇵🇹 [Ler em português](README.pt.md)

# Orfi

**Or**ganize **fi**les, straight from the command line.

[![CI](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml/badge.svg)](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml)
[![Changelog](https://img.shields.io/badge/changelog-keep_a_changelog-orange)](CHANGELOG.md)

## Features

- Automatic file organization by extension
- Default folder for unrecognized files
- Support for moving or copying files
- Reversal of the organization
- Configurable file categories
- Per-user configuration
- File dating with creation timestamps
- Reversal of dating
- Logging
- Configurable language

## Installation

Requires Python 3.12 or higher (needed for reliable file creation timestamps on Windows).
From the project folder:

```bash
python -m pip install .
```

After installation, the program can be run with the command:

```bash
orfi
```

## Options

| Option              | Description                                            | Default     |
|---------------------|--------------------------------------------------------|-------------|
| `-t`, `--target`    | Allows selecting the target folder (requires `tkinter`)| No          |
| `-c`, `--copy`      | Copies files instead of moving them                    | Move        |
| `-r`, `--revert`    | Reverts the organization                               | No          |
| `-d`, `--date`      | Adds the creation date to file names                   | No          |
| `-y`, `--yes`       | Automatically accepts required confirmations           | No          |
| `-n`, `--dry-run`   | Simulates the process without making any real changes  | No          |
| `-l`, `--language`  | Changes the language to the one specified              | from config |
| `-V`, `--version`   | Displays the installed version                         | —           |
| `--depth N`         | Recurse into subfolders, down to depth `N`             | 1           |
| `-v`, `--verbose`   | Display more details about the operation               | No          |

## Usage

To see all available options:

```bash
orfi --help
```

Organize the current folder:

```bash
orfi
```

Organize the current folder, automatically accepting all confirmations:

```bash
orfi -y
```

Change the language to Portuguese:

```bash
orfi -l pt
```

Select a specific folder:

```bash
orfi -t
```

Copy files instead of moving them:

```bash
orfi -c
```

Simulate organizing a specific folder:

```bash
orfi -t -n
```

Organize the current folder, including subfolders up to 2 levels deep:

```bash
orfi --depth 2
```

Revert the organization by categories:

```bash
orfi -r
```

Add the creation date to file names:

```bash
orfi -d
```
For example:

```text
report.pdf → 260903_report.pdf
```

Copy and date the files:

```bash
orfi -d -c
```

Revert the dating:

```bash
orfi -d -r
```

Copy files while reverting the dating:

```bash
orfi -d -r -c
```

Options can be combined. For example, to select a folder and simulate reverting the file dating, by copying, while automatically accepting all required confirmations:

```bash
orfi -t -r -c -d -y -n
```

## Configuration

Categories and their respective extensions are defined through the `config.toml` file.

Orfi ships with a default configuration that is automatically copied to the user's configuration location on first run.

### Location

On Windows:

```text
%APPDATA%\orfi\config.toml
```

On Linux:

```text
~/.config/orfi/config.toml
```

The user's configuration file is not overwritten when Orfi is updated or reinstalled.

### Logs

Orfi logs the operations it performs to an `orfi.log` file, located next to the configuration file.

### Language

The interface language is set through the `language` key in `config.toml`:

```toml
language = "en"
```

It can also be changed with the `-l`/`--language` flag, which updates the value in `config.toml` for future runs.

### Categories

Each category can define a set of extensions:

```toml
[[categories]]
name = "Images"
extensions = [".jpg", ".png", ".gif"]
```

A category can be set as the default category:

```toml
[[categories]]
name = "Misc"
extensions = []
default = true
```

Files whose extension doesn't match any category are routed to the default category.

The configuration allows creating, changing, or removing categories and extensions according to the user's needs.

## Known limitations

- Reverting infers state from category folders. Files moved manually into them will be reverted too.
- No transaction log; a mid-operation failure can leave partial state.

## Tests

Tests can be run with:

```bash
pytest
```

The project uses `pytest` to test Orfi's different features.

## Contributing

Issues and PRs are welcome. Run tests with `pytest` before submitting.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE).