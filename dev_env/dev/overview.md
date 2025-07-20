

For nix / dev setup - two main entry points:
- 1) bootstrap.sh
Is responsible for full setup from scratch
- 2) apply.sh
Is responsible for applying the latest changes to the already set up system

Beyond that, there are two main components of the dev-env:
- Automated jobs
- Tools

Below - an overview in more details

------------

# Entry points overview - how to install / set up

##  Bootstrap
- assume this repo is cloned
- assume basic python is installed
-> using shell and python scripts in this repoto install everything else
Installs: 
- brew, nix
- necessary nix pre-installs: nix-darwin, home-manager
- pulls this repo to a persistent location
- saves location to env variable
- configures nix files with username and machine name
- runs first nix build & applies configuration

### Bonus 1
Off-nix setup:
A script for setting up systems beyond nix.

### Bonus 2
Provide user with instructions / checklist of what to configure manually outside of nix
- authenticate into services
- configure settings in those services
- install more apps with setapp
 
------------

## Apply
- find persistent location of dev-env
- pull latest changes
- update flake inputs
- build & apply configuration

------------

# Systems overview - what nix installs / sets up

## Basic components
- brew apps (all the necessary apps, tweak to your preference)
- macos settings (dock, spaces, etc - capture your preferences with mac_settings tool and add to nix)
- nixpkgs (some packages are available through nix and allow for automated configuration)
- home-manager (all the dotfiles - tweak to your preference in resources/shell_profiles)


## Custom components
A list of components that required custom code to set up
Might be unexpected and unintuitive, not a default nix system.


------------

## Automated jobs

------------

## Tools

- lnsafe. Idea: upgrade of ln command. Resolves source path. If target is missing just link to cwd.
- mac_settings. Idea: Track macos settings to use for generating nix files.