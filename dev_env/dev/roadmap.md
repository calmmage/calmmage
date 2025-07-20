# Development Environment Roadmap

## Plan

### Right Now (MVP)
1. Basic Nix Configuration
   - [x] Apply current nix configuration
   - [x] Commit initial state
   - [ ] Move core files from dev-env to this repo
   - [ ] Basic shell configuration
     - [x] Custom aliases (.alias)
     - [x] Zsh configuration (.zshrc)

2. Documentation
   - [ ] Setup instructions
   - [ ] Configuration guide
   - [ ] Repository structure documentation

### Later (Committed Features)
1. Enhanced Development Tools
   - Launch daemon configurations (launchd)
   - Docker & MongoDB setup
   - Raycast extensions and custom scripts
   - Python environment
     - Python startup configuration
     - Common development libraries
     - Development tools from devenv repo

2. Automated Setup
   - Complete setup script
     - User settings customization
     - MacOS settings management
     - Nix/nix-darwin installation
     - Automated configuration application

3. Manual Configuration Guide
   - App Store applications
     - Dropover
     - Flow
     - Endel
   - Third-party tools
     - Shottr (settings + license)
     - Bartender (settings + license)
     - Rectangle (shortcuts + settings)

### Maybe (Ideas & Possibilities)
1. Project Management
   - Project creation tools
   - Project discovery features
   - Template system

2. Knowledge Management
   - Task tracking integration
   - Knowledge base system
   - Code management tools

3. Additional Tools
   - Custom utility scripts
   - Additional Raycast extensions
   - More development libraries

## Thoughts


g1
- [x] Apply current nix configuration. 
- generate settings on my personal mac
    - cancelled for now
- [x] commit current state

g2 - try adding more cool settings, aliases etc..
- my Notion guide
- some random guide on the internet
- my custom aliases
    - .alias
    - .zshrc
- gpt suggestions

g3 - more hardcore tools and setups
- launchd (Launch Control)
- Local docker, mongodb etc.
- Raycast - extensions and scripts (my, custom - e.g. the nix command)

## g4 - 
.alias
.zshrc
python_startup.py

- calmlib
- frequent libs
- some tools / utils? 

## g5 - _some_ way to have the features I want
- find projects
- new project
- 

## g6 - mega-functional-requirements
- task tracking
- knowledge tracking
- code tracking / management

# Mega-projects

## complete setup script

How I want the final script to look:

1) update .nix files with local user settings (current username, hostname etc..)
2) capture initial macos settings using the mac-settings tool.py
3) install necessary intermediate things like python and stuff
4) install nix, nix-darwin and whatever else necessary (brew?)
5) apply ...
Extras
6) prompt user to set everythign up to their liking
7) capture update mac settings
8) generate updated nix files based on settings diff

## manual setup readme

d) install manually with ... App Store
- Dropover
- Flow
- Endel
e) Configure manually
- shottr
	- [ ] settings
		- [x] basic settings
		- [ ] iterate
	- [ ] license
- bartender
	- [ ] settings
		- [x] basic settings
		- [ ] iterate
	- [ ] license
- rectangle
	- [x] shortcuts
	- [x] settings (border, auto-start at login)


# Project structure draft

dev-env/
├── nix/                      # Nix configuration
│   ├── flake.nix
│   ├── configuration.nix
│   └── modules/
│       ├── darwin/          # macOS-specific configurations
│       └── home-manager/    # User environment configurations
│
├── tools/                    # CLI tools and utilities
│   ├── mac-settings/        # Tool for tracking macOS settings changes
│   ├── project-manager/     # Project creation and management
│   └── git-hooks/          # Git hooks management
│
├── scripts/                  # Setup and maintenance scripts
│   ├── setup/              # First-time setup scripts
│   │   ├── install-nix.sh
│   │   └── bootstrap.sh
│   └── maintenance/        # Regular maintenance scripts
│       ├── daily.sh
│       └── weekly.sh
│
├── config/                   # Configuration files
│   ├── shell/              # Shell configurations
│   │   ├── aliases.sh
│   │   ├── functions.sh
│   │   └── zshrc
│   ├── git/               # Git configurations
│   └── python/           # Python environment configs
│
├── templates/               # Project templates
│   ├── python/
│   │   ├── app/
│   │   ├── lib/
│   │   └── experiment/
│   └── typescript/
│
├── docs/                    # Documentation
│   ├── setup.md            # Setup guide
│   ├── maintenance.md      # Maintenance guide
│   └── templates/          # Template documentation
│
└── tests/                   # Test suite
    ├── tools/
    ├── scripts/
    └── templates/
