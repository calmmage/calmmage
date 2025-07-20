#!/bin/bash
# bootstrap.sh - Full System Setup Script
# This script performs a complete setup of the development environment on a fresh macOS system.

echo "This script will:"
echo "1. Install Command Line Tools for Xcode"
echo "2. Install Nix package manager"
echo "3. Install Homebrew"
echo "4. Clone/update the dev-env repository"
echo "5. Set up initial configuration files"
echo "6. Apply the full nix configuration"
echo "7. Install additional tools and applications"

# TODO: Implement the following steps:
# - Check if running on macOS
# - Install Command Line Tools
# - Install Nix using determinate installer
# - Install Homebrew
# - Clone dev-env repository
# - Set up initial configuration
# - Run first nix build
# - Apply configuration
# - Set up additional tools
# - Verify installation

set -e

setup_persistent_location() {
    local location_file="$HOME/.dev-env-location"
    if [ ! -f "$location_file" ]; then
        echo "Please enter target dev-env location (default: $HOME/.calmmage/dev-env):"
        read -r user_location
        STABLE_DEV_ENV_DIR=${user_location:-$HOME/.calmmage/dev-env}
        ACTIVE_DEV_ENV_DIR="$HOME/work/projects/dev-env"
        STABLE_VENV_PATH="$STABLE_DEV_ENV_DIR/.venv"
        ACTIVE_VENV_PATH="$ACTIVE_DEV_ENV_DIR/.venv"
        echo "export STABLE_DEV_ENV_DIR=\"$STABLE_DEV_ENV_DIR\"" > "$location_file"
        echo "export ACTIVE_DEV_ENV_DIR=\"$ACTIVE_DEV_ENV_DIR\"" >> "$location_file"
        echo "export STABLE_VENV_PATH=\"$STABLE_VENV_PATH\"" >> "$location_file"
        echo "export ACTIVE_VENV_PATH=\"$ACTIVE_VENV_PATH\"" >> "$location_file"
    fi
    source "$location_file"
}

# Install core dependencies
install_dependencies() {
    # Install Xcode Command Line Tools if not already installed
    if ! xcode-select -p &>/dev/null; then
        echo "Installing Xcode Command Line Tools..."
        xcode-select --install || true
    else
        echo "Xcode Command Line Tools already installed"
    fi
    
    # Install Nix if not already installed
    if ! command -v nix &>/dev/null; then
        echo "Installing Nix..."
        # Add experimental features to nix config
        mkdir -p ~/.config/nix
        echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
        # curl -L https://nixos.org/nix/install | sh
        # todo: if ... we follow this path - need to also enable more things.
        curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
        # Wait for nix installation to complete
        sleep 5
        
        # Source nix into current shell
        if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
            . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
        fi
    else
        echo "Nix already installed"
    fi
    
    # Install Homebrew if not already installed
    if ! command -v brew &>/dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew already installed"
    fi
    
    # Install nix-darwin if not already installed
    if ! command -v darwin-rebuild &>/dev/null; then
        echo "Installing nix-darwin..."
        
        # Backup existing configuration files if they exist
        for file in /etc/nix/nix.conf /etc/bashrc /etc/zshrc; do
            if [ -f "$file" ]; then
                echo "Backing up $file to ${file}.before-nix-darwin"
                sudo mv "$file" "${file}.before-nix-darwin"
            fi
        done
        
        nix-build https://github.com/LnL7/nix-darwin/archive/master.tar.gz -A installer
        ./result/bin/darwin-installer
    else
        echo "nix-darwin already installed"
    fi
}

ensure_dev_env_repo() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local updater_script="$script_dir/tools/dev_env_updater.py"
    
    if [ ! -f "$updater_script" ]; then
        echo "Error: Could not find dev_env_updater.py at $updater_script"
        exit 1
    fi
    
    echo "Ensuring dev-env repository is present and up to date..."
    python3 "$updater_script"
    
    if [ ! -d "$STABLE_DEV_ENV_DIR" ]; then
        echo "Error: Failed to setup dev-env repository at $STABLE_DEV_ENV_DIR"
        exit 1
    fi
}

setup_nix_configuration() {
    echo "Setting up Nix configuration..."
    cd "$STABLE_DEV_ENV_DIR/nix"
    
    # TODO: guide the user through setting up user.yaml config file
    # # Run configuration script
    # python3 tools/configure.py
    
    # echo "Please review and edit config/user.yaml before continuing"
    # echo "Press Enter when ready to continue, or Ctrl+C to abort"
    # read -r
    
    # Initial build
    nix flake update
    darwin-rebuild switch --flake .#default
}

# Main execution
setup_persistent_location
install_dependencies
ensure_dev_env_repo
setup_nix_configuration
