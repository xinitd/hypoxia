<div align="center">
  <h2>HYPOXIA</h2>
  <p>
    <a href="#about">About</a>
    ·
    <a href="#usage">Usage</a>
    ·
    <a href="#settings">Settings</a>
  </p>
  <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/xinitd/hypoxia/total">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/xinitd/hypoxia">
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/xinitd/hypoxia">
  <img alt="GitHub License" src="https://img.shields.io/github/license/xinitd/hypoxia">
</div>

<div align="center">
  <h3 align="center">Disclaimer</h3>
</div>

> [!WARNING]
> This project can only be used on devices owned by you. You can't use this project for evil intent. Authors and contributors are not responsible for possible consequences.

<div align="center">
  <h3 align="center">About</h3>
</div>

Hypoxia is an open-source forensic and backup creation tool, designed for security researchers and system administrators. This utility may be used for data analysis (metadata extraction), backup creation and file recovering.

Use cases:
- Forensic;
- Backing up data;
- Recovery files from PC with broken operating system.

<div align="center">
  <h3 align="center">Technical information</h3>
</div>

Programming language: `Python`

Requirements:
* There is no need to install dependencies. They simply do not exist. Just install Python version `3.11` or newer for using as Python script.

<div align="center">
  <h3 align="center">Usage</h3>
</div>

#### Standalone executable:

* Download [latest release](https://github.com/xinitd/hypoxia/releases)
* Set executable flag: `chmod +x hypoxia`
* Run: `./hypoxia --help`

#### As Python script:

* Install Python
* Clone repo `git clone https://github.com/xinitd/hypoxia.git`
* Go to project folder `cd hypoxia`
* Set executable flag: `chmod +x hypoxia.py`
* Run `$(which python) hypoxia.py --help`

```
user@localhost:~$ ./hypoxia --help
Hypoxia. Every byte will be found.

options:
  -h, --help            show this help message and exit
  -v {silent,info}, --verbosity {silent,info}
                        Set verbosity level for display additional information in runtime: "silent" - no any prints in terminal, "info" - print every action.
  -s SEARCH_PATH, --search-path SEARCH_PATH
                        Setting up searching path. The absolute or relative path to the directory to search in.
  -e EXTENSIONS, --extensions EXTENSIONS
                        File extensions to search for, separated by commas (e.g., "pdf,docx,txt").
  -m {yes,no}, --keep-metadata {yes,no}
                        Defines if file metadata should be preserved. "yes" keeps it, "no" discards it (faster).
```

#### Settings:

* `-v` or `--verbosity` - needs for print data about working of program. This parameter required and have two values: `silent` - no any prints in terminal, `info` - print every action and path of copying file.
* `-s` or `--search-path` - set path where you want look up files. This argument required and have no default value.
* `-e` or `--extensions` - put file extensions, which you want be found.
* `-m` or `--keep-metadata` - metadata saving mode for collected files: `no` - copy files without metadata (faster), `yes` - attempts to keep all metadata.
