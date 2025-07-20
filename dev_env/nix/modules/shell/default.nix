{ config, lib, pkgs, userConfig, ... }:

let
  user = userConfig.username;
in
{

  # Use packages from user config
  # todo: user config
#  home.packages = map (name: pkgs.${name}) userConfig.home_manager.packages;

  home.sessionVariables = {
    PAGER = "less";
    CLICOLOR = 1;
    EDITOR = "subl";
    # PATH = "$PATH:$HOME/bin";
    PATH = "$PATH:$HOME/bin:$STABLE_VENV_PATH/bin";  # Add Poetry env to PATH
  };

  imports = [
    ./aliases
    ./scripts
#    ./dotfiles
  ];

  home.file = {
    ".inputrc".source = ./dotfiles/inputrc;
    ".zshrc.custom".source = ./dotfiles/zshrc;  # Add your zshrc file
    ".aliases".source = ./dotfiles/aliases;  # Add your aliases file
    ".zsh-custom-functions" = {
      text = ''
        function my_custom_function() {
          # function code here
        }
      '';
    };
  };

  home.activation = {
    setDefaults = lib.hm.dag.entryAfter ["writeBoundary"] ''
      # Window Manager settings
      /usr/bin/defaults write com.apple.WindowManager EnableTopTilingByEdgeDrag -bool false
      /usr/bin/defaults write com.apple.WindowManager EnableTilingByEdgeDrag -bool false
      /usr/bin/defaults write com.apple.WindowManager EnableTilingOptionAccelerator -bool false
    '';

#    dock = lib.hm.dag.entryAfter ["writeBoundary"] ''
#      # Remove all apps from dock first
#      ${pkgs.dockutil}/bin/dockutil --remove all \
#        --no-restart \
#        "$HOME/Library/Preferences/com.apple.dock.plist"
#
#      # Add apps from our config
#      ${lib.concatMapStringsSep "\n" (app: ''
#        ${pkgs.dockutil}/bin/dockutil --add "${app}" \
#          "$HOME/Library/Preferences/com.apple.dock.plist"
#      '') userConfig.dock.apps}
#
#      # Restart dock to apply changes
#      /usr/bin/killall Dock
#    '';
  };

  # Define help message that was previously in zshrc
  programs.zsh.initExtra = ''
    export HELP="This is a help message by Petr Lavrov, on Jan 2024

    calmlib aliases:
    np, new_project, pm, project_manager
    cdl, cds, cdp - cd to latest, structured and playground
    cd1, 2, 3 - same
    cdr, lsr, cdf - fuzzy match cd and ls

    personal aliases:
    hetzner - ssh to hetzner server

    fp - find project (find dir / file name in ~/work)
    find_ \$text \$path - find text in file (grep all text instances in dir)
    mva - move the dir to new location and leave a symlink instead

    pro cli libs:
    ghc / gh copilot - github copilot cli
    aie - gh copilot explain
    ais - gh copilot suggest

    tree
    awk, grep"
  '';
} 