🇵🇹 [Ler em português](README.pt.md)

# Orfi

**Or**ganize **fi**les, straight from the command line.

[![CI](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml/badge.svg)](https://github.com/pedro-f-97/orfi/actions/workflows/ci.yml)

## Features

- Automatic file organization by extension
- Default folder for unrecognized files
- Support for moving or copying files
- Reversal of the organization
- Configurable file categories
- Per-user configuration
- File dating with creation date
- Reversal of dating
- Logging
- Configurable language

## Installation

Requires Python 3.11 or higher.
From the project folder:

```bash
python -m pip install .
```

After installation, the program can be run with the command:

```bash
orfi
```

## Options

| Option             | Description                              |
|--------------------|-------------------------------------------|
| `-t`, `--target`     | Allows selecting the target folder (requires 'tkinter') |
| `-c`, `--copy`   | Copies files instead of moving them       |
| `-r`, `--revert` | Reverts the organization                  |
| `-d`, `--date`    | Adds the creation date to file names      |
| `-y`, `--yes`    | Automatically accepts required confirmations |
| `-n`, `--dry-run`   | Simulates the process without making any real changes |
| `-l`, `--language`   | Changes the language to the one specified |
| `-V`, `--version`  | Displays the installed version |

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

Revert the organization by categories:

```bash
orfi -r
```

Add the creation date to file names:

```bash
orfi -d
```

Simulate organizing a specific folder:

```bash
orfi -t -n
```

For example:

```text
relatorio.pdf → 260903_relatorio.pdf
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

## Tests

Tests can be run with:

```bash
pytest
```

The project uses `pytest` to test Orfi's different features.
