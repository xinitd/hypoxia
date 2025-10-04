<div align="center">

  <img src="assets/logo.png" alt="Hypoxia logo" style="height: 256px; width: 256px; object-fit: contain;">

  <h2>HYPOXIA</h2>
  <p>
    <a href="#about">About</a>
    ·
    <a href="#usage">Usage</a>
    ·
    <a href="#options">Options</a>
  </p>
  <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/xinitd/hypoxia/total">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/xinitd/hypoxia">
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/xinitd/hypoxia">
</div>

<div align="center">
  <h3 align="center">Disclaimer</h3>
</div>

> [!WARNING]
> This project can only be used on devices owned by you. You can't use this project for evil intent. Authors and contributors are not responsible for possible consequences.

<div align="center">
  <h3 align="center">About</h3>
</div>

<img src="assets/terminal.png" alt="Terminal">

Hypoxia is a powerful, cross-platform command-line tool for targeted file collection. Written in pure Python, it recursively searches directories to find and copy files based on a rich set of criteria, including file extension and modification date ranges.

Designed for efficiency and portability, Hypoxia is an ideal utility for digital forensics specialists, system administrators, and security researchers who need to quickly gather digital evidence, create specific archives, or recover data from a mounted file system.

Use cases:
- Forensic;
- Backing up data;
- Recovery files from PC with broken operating system.

<div align="center">
    <h3 align="center">Features & Philosophy</h3>
</div>

Hypoxia is built with a focus on simplicity, portability, and reliability.

- **Lightweight & Portable:** Written in pure Python with no external dependencies. If you have Python 3.11+, it just works.

- **Cross-Platform:** Runs seamlessly on Windows, macOS, and Linux.

- **Powerful Filtering:** Collect files with precision by combining filters for:

  - File extensions (e.g., `pdf`, `docx`, `jpg`).

  - Modification date ranges (files created after, before, or within a specific period).

- **Metadata Control:** Choose whether to preserve original file metadata (timestamps, permissions) or discard it for faster copy operations.

- **Standard Library Only:** Built exclusively using Python's robust standard libraries (argparse, pathlib, datetime, shutil), ensuring maximum compatibility and security.

<div align="center">
  <h3 align="center">Usage</h3>
</div>

#### Standalone executable:

- Download [latest release](https://github.com/xinitd/hypoxia/releases)

- Set executable flag:

  ```bash
  chmod +x hypoxia
  ```

- Run:

  ```bash
  ./hypoxia --help
  ```

#### As Python script:

- Install Python

- Clone repo:
  ```bash
  git clone https://github.com/xinitd/hypoxia.git
  ```

- Go to project folder:

  ```bash
  cd hypoxia
  ```

- Set executable flag:

  ```bash
  chmod +x hypoxia.py
  ```

- Run:

  ```bash
  $(which python) hypoxia.py --help
  ```

#### Usage example:

This command will search the `/mnt/data` directory and all its subdirectories for `.jpg`, `.mp4`, and `.mov` files modified between January 1st and March 31st, 2025. It will preserve their metadata (`--keep-metadata` defaults to `yes`) and print every action to the terminal:

```bash
python hypoxia.py -v info -s "/mnt/data" -e "jpg,mp4,mov" --date-from "2025-01-01" --date-to "2025-03-31"
```

<div align="center">
  <h3 align="center">Options</h3>
</div>

All command-line arguments that can be used to control the behavior of Hypoxia are listed below:

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--version` | Displays the current version of Hypoxia and exits. | No | - |
| `-v`, `--verbosity` | Sets the verbosity level. `silent` provides no output, while `info` logs every action to the terminal. | Yes | - |
| `-s`, `--search-path` | The absolute or relative path to the directory to search recursively. | Yes | - |
| `-e`, `--extensions` | A comma-separated list of file extensions to search for (e.g., `pdf`, `docx`, `txt`). Do not include dots. | Yes |  |
| `-m`, `--keep-metadata` | Defines if file metadata (timestamps, permissions) should be preserved. | No | `yes` |
| `--date-from` | Filters for files modified on or after this date. Format: `YYYY-MM-DD`. | No | - |
| `--date-to` | Filters for files modified on or before this date. Format: `YYYY-MM-DD`. | No | - |
