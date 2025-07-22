# Shell Configuration

This directory contains shell-related configurations and customizations for the development environment.

## Structure

- `aliases/` - Shell aliases organized by category
  - `git.nix` - Git-related aliases
  - `navigation.nix` - Directory navigation aliases
  - `python.nix` - Python development aliases
  - `tools.nix` - General tool aliases

- `functions/` - Custom shell functions
  - `utils.nix` - Utility functions
  - `search.nix` - Search-related functions
  - `path.nix` - Path manipulation functions

- `config/` - Shell configuration files
  - `zsh.nix` - ZSH specific configuration
  - `inputrc.nix` - Readline configuration
  - `env.nix` - Environment variables

## Usage

The shell configurations are automatically loaded through the home-manager module system. Individual components can be enabled/disabled in your `user.yaml` configuration.

## Adding New Configurations

1. Create a new .nix file in the appropriate subdirectory
2. Add the configuration to the relevant category
3. Import the new file in the category's default.nix
4. Update this README with any new components 