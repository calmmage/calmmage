# Dev Env

Development environment setup and configuration management.

## Quick Start

First-time setup:
```bash
./bootstrap.sh  # First-time system setup
```

Daily usage:
```bash
# Quick rebuild of current config
nixswitch

# Full update (git + flake) and rebuild
nixup

```

## Core Scripts

- `bootstrap.sh` - First-time system setup (Xcode tools, Nix, Homebrew)
- `build-nix.sh` - Core build script with options:
  - No flags: Just rebuild current config
  - `--flake` (`-f`): Update flake inputs and rebuild
  - `--git` (`-g`): Pull latest changes and rebuild
  - `--update` (`-u`): Full update (git + flake) and rebuild

## Directory Structure

```
.
├── bootstrap.sh     # First-time setup
├── build-nix.sh     # Core build script
├── nix/            # Nix configuration
│   ├── modules/    # System modules
│   └── flake.nix   # Main flake
└── tools/          # Helper tools and scripts
```

## Additional Documentation

- [Nix Configuration](nix/README.md)
- [Python Tools Usage](docs/python-tools.md)
- [Project Management](docs/project-management.md)


# Old instructions - to migrate
----------------------------------------

# Usage
## How to run python scripts with my dev env
- interactively: runp alias
- in scripts: 
  - option 1: direct path to python executable
    - e.g. ~/.calmmage/dev_env/.venv/bin/python3 (should match the value of DEV_ENV_PATH)
  - option 2: source ~/.zshrc and use runp alias
  - todo: option 3 - add env vars to ~/.env and load them from there, then use DEV_ENV_PATH path

## project management
- np (new project) alias - create a new project
- asd
- 
## Refresh dev env
## How to set up launchd jobs
## How to set up raycast extensions
## How to set up raycast scripts

# Setup

## setup dev env
## Setup project folders
## Set up launchd jobs
- daily job to commit / push / pull all repos
- daily job to update all repos
- monthly job to process all repos, compile a list of all drafts

## Set up raycast extensions
- open dir
- create dir link

## Set up raycast scripts

- refresh dev env

## How to setup env, shell and aliases
- clone repo, create poetry env, using that env run `run.py` script
What it does:
1) clones dev_env repo to ~/.calmmage/dev_env
2) sets up zshrc and aliases (add source to ~/.zshrc)
3) sets up env variables STABLE_DEV_ENV_DIR, STABLE_VENV_PATH, ACTIVE_DEV_ENV_DIR and ACTIVE_VENV_PATH

- STABLE_DEV_ENV_DIR  - "~/.calmmage/dev_env"
- STABLE_VENV_PATH - "~/.calmmage/dev_env/.venv"
- ACTIVE_DEV_ENV_DIR - this repo
- ACTIVE_VENV_PATH - this_repo/.venv

# Dev

## Links
Notion page
https://www.notion.so/Troubleshoot-throwaway-11fbc5d57f7c80a993eff1ccaa7c253e?pvs=4

## Plan
1. How to run python scripts with my dev env
    - clone dev_env to
        - Decide: to ~/work/projects or a separate location (e.g. ~/.calmmage)
        - Decided. Clone to ~/.calmmage
    - asd
    - Option 1: just use direct path to python executable
        - e.g. ~/.calmmage/dev_env/.venv/bin/python3
    - Option 2: use my custom alias `runp`
        - It requires env variable $DEV_ENV_PATH to be set
2. How to set up a new dev env from scratch - or refresh it
    - a) clone dev_env repo somewhere
    - b) run setup.py script using
3. How to look up/remember what I did in the past
    - look at aliases and zshrc
    - look at dev_env aliases and zshrc
    - there's alias `help` and `aliases`

## Update 2024-10-14
- Нужен скрипт, который все разворачивает
    - Изначально этот скрипт на питоне - как его запустить?
    - Вариант 1 - пайчармом
    - Вариант 2 - poetry install, poetry run
    - dev_env/run.py
    
    ---
    
    - Что делает скрипт?
        1. Скачивает dev_env в ~/.calmmage/dev_env
            1. Обновляет
        2. Кладет все нужное в ~/.zshrc если его там нет
            1. путь до dev_env
            2. путь до poetry env
            3. source dev_env/resources/shell_profiles/.zshrc
            4. source dev_env/resources/shell_profiles/aliases
    1. Привязать скрипт к raycast setup_calmmage_dev_env
        1. Инструкция как настраивать raycast (может я ее уже писал? где-то…)
            1. extensions
            2. scripts
    2. Привязать к launchd чтобы daily гонялся-обновлялся
        1. Какой-то самодостаточный скрипт который может прогнаться даже если все сломано?

## New dev env

- [ ] install brew
- [x] setup ssh keys  
  [setup_ssh.sh](../try-nix/dev/unsorted/basic_setup/setup_ssh.sh)
- [x] setup github cli  
  [setup_gh.sh](../try-nix/dev/unsorted/basic_setup/setup_gh.sh)
- [ ] install python environments
- [ ] clone all projects
- idea: daily job to commit / push / pull all repos

## old dev env

- create project structure
- setup zshrc and aliases
- raycast extensions
- launchd jobs

## one-off todos:

- add all utils to calmlib - to a beta section
- add all code snippets to calmapp / bot-lib - to a beta section
- add all code snippets to examples repo
- resolve 'migration' branches
- resolve leaked telegram token to a notion assistant repo
- resolve github tests failing - fix

## Calmmage Dev Env.
Includes:

- Development Folder Structure
- .zshrc and aliases
- custom tools for manual and ad-hoc jobs

## Setup

- Run main.py
- Add daily and monthly jobs to the automation tool of your choice (I use
  LaunchControl based on launchd for MacOs and n8n for Windows)
- to access github templates, add the GITHUB_API_TOKEN to the env variables or `.env` file

## Usage

- Folder structure includes seasonal and structured folder,
    - `cd_1`, `cd_2`, `cd_3` - You can access key folders using shortcut aliases
    - cd_1, cdl - ~/work/code/seasonal/latest
    - cd_2, cdp - ~/work/playground
    - cd_3, cds - ~/work/code/structured
- `help` - You can see key features in the $HELP env variable
- project management
    - `np` - create a new project
    - `lt` - list available project templates
    -

## Aliases

### Key Aliases
