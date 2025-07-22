# bash script to reapply nix files
# make sure nix daemon is running
. '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'

# make sure we're in the right dir - root of the repo
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if we're in the dev-env directory
if [ "$PWD" != "$SCRIPT_DIR" ]; then
    echo "Error: This script must be run from the dev-env directory"
    echo "Current directory: $PWD"
    echo "Script directory: $SCRIPT_DIR"
    exit 1
fi


echo "Applying nix files for user $USER"

cd nix

# d) nix update
nix flake update

# e) nix switch
/run/current-system/sw/bin/darwin-rebuild switch --flake .#$USER
