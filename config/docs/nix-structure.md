# Nix Configuration Structure

## Core Nix Files

### 1. flake.nix - Entry Point
- Defines dependencies (inputs) like nixpkgs, home-manager, darwin
- Sets up the system configuration
- Connects all other modules together
- Essential for reproducible builds

### 2. configuration.nix - Global System Configuration
- Sets up system-wide settings
- Configures home-manager for the user
- Contains user-specific packages and settings

### 3. modules/darwin/default.nix - macOS Configuration
- System preferences and defaults
- Environment setup
- Homebrew configuration
- System packages
- Security settings

### 4. modules/home-manager/default.nix - User Environment
- User packages
- Shell configuration (zsh)
- Git settings
- Program configurations
- Dock settings
- User environment variables

### 5. personal.nix - Private Settings
- Store sensitive configurations
- Personal preferences
- Private keys/tokens

## Shell Configuration Files

### 1. dotfiles/aliases - Custom Shell Aliases
- Command shortcuts
- Tool replacements
- Helper functions aliases

### 2. dotfiles/zshrc - ZSH Shell Configuration
- Shell functions
- Environment setup
- Utility functions
- Path configurations

## Why Separate Files?

### 1. Modularity
- Each file handles specific aspects of configuration
- Easier to maintain and update
- Can be reused across different systems

### 2. Organization
- System settings (darwin/default.nix)
- User settings (home-manager/default.nix)
- Shell customization (aliases, zshrc)
- Private settings (personal.nix)

### 3. Flexibility
- Can enable/disable modules easily
- Different configurations for different machines
- Easy to share non-sensitive parts

### 4. Security
- Sensitive information can be kept separate
- Personal configurations isolated from shared ones 