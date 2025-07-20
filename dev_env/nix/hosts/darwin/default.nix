{ agenix, config, pkgs, lib, poetry2nix, userConfig, ... }:

let
  inherit (lib) mkEnableOption mkOption types;
  # Add an overlay to disable tests for problematic Python packages
in
{
  imports = [
  # todo: re-enable secrets
#    ../../modules/darwin/secrets.nix
    ../../modules/darwin/home-manager.nix
     agenix.darwinModules.default
  ];

  # Auto upgrade nix package and the daemon service.
  services.nix-daemon.enable = true;

  networking = {
    computerName = userConfig.computer_name;
    hostName = userConfig.host_name;
    localHostName = userConfig.host_name;
  };

  # fonts.fontDir.enable = true; # DANGER
  fonts.packages = [ (pkgs.nerdfonts.override { fonts = [ "Meslo" ]; }) ];

  documentation.enable = false;

  # Setup user, packages, programs
  nix = {
    package = pkgs.nix;
    settings = {
      trusted-users = [ "root" "@admin" "${userConfig.username}" ];
      substituters = [ "https://nix-community.cachix.org" "https://cache.nixos.org" ];
      trusted-public-keys = [ "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=" ];
    };

    gc = {
      user = "root";
      automatic = true;
      interval = { Weekday = 0; Hour = 2; Minute = 0; };
      options = "--delete-older-than 30d";
    };

    extraOptions = ''
      experimental-features = nix-command flakes
    '';
  };

  # Turn off NIX_PATH warnings now that we're using flakes
  system.checks.verifyNixPath = false;

  # Load configuration that is shared across systems
  environment = {
    shells = [ pkgs.bash pkgs.zsh ];
    systemPackages = with pkgs; [
      agenix.packages."${pkgs.system}".default
      coreutils
      defaultbrowser] ++ 
      (lib.optional userConfig.use_devenv devenv) ++
      (lib.optionals userConfig.use_poetry2nix [(pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../..;
        preferWheels = true;
        python = python311;
        # Add overrides to handle git dependencies
        overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
          calmlib = prev.calmlib.overridePythonAttrs (old: {
            buildInputs = (old.buildInputs or [ ]) ++ [
              pkgs.poetry
              final.poetry-core
            ];
          });
        });
        # Add extra packages that might be needed for building
        extraPackages = ps: with ps; [
          pip
          setuptools
          wheel
          poetry
          poetry-core
        ];
      })]) ++ pkgs.userPackages;

    systemPath = [
      "/opt/homebrew/bin"
      # "$STABLE_DEV_ENV_DIR/tools/" - remove for now - can't get it to work
    ];
    pathsToLink = [ "/Applications" ];
  };

#  launchd.user.agents.emacs.path = [ config.environment.systemPath ];
#  launchd.user.agents.emacs.serviceConfig = {
#    KeepAlive = true;
#    ProgramArguments = [
#      "/bin/sh"
#      "-c"
#      "/bin/wait4path ${pkgs.emacs}/bin/emacs && exec ${pkgs.emacs}/bin/emacs --fg-daemon"
#    ];
#    StandardErrorPath = "/tmp/emacs.err.log";
#    StandardOutPath = "/tmp/emacs.out.log";
#  };

  # Enable TouchID for sudo if configured in user config
  security.pam.enableSudoTouchIdAuth = userConfig.enable_sudo_touch_id;

  system = {
    keyboard.enableKeyMapping = true;
    keyboard.remapCapsLockToEscape = false;
    stateVersion = 4;
    activationScripts.postActivation.text = ''
      # Allow Karabiner-Elements to receive keyboard events
      /usr/bin/sudo /usr/bin/security authorizationdb write system.privilege.taskport allow
    '';

    defaults = {
      NSGlobalDomain = {
        AppleShowAllExtensions = true;
        ApplePressAndHoldEnabled = false;

        # 120, 90, 60, 30, 12, 6, 2
        KeyRepeat = 2;

        # 120, 94, 68, 35, 25, 15
        InitialKeyRepeat = 15;

        "com.apple.mouse.tapBehavior" = 1;
        "com.apple.sound.beep.volume" = 0.0;
        "com.apple.sound.beep.feedback" = 0;

        AppleInterfaceStyle = "Dark";
        AppleInterfaceStyleSwitchesAutomatically = false;
        AppleShowAllFiles = true;
        NSNavPanelExpandedStateForSaveMode = true;
      };
      # todo: re-enable later when issues are fixed
#       dock = {
#         autohide = true;
#         show-recents = true;
#         launchanim = true;
#         orientation = "bottom";
#         tilesize = 36;
#         largesize = 128;

#         magnification = true;
#         # expose-group-apps = userConfig.dock.settings.expose_group_by_app;
#         mru-spaces = false; # disable reordering spaces
#         minimize-to-application = true;
#         show-process-indicators = true;

# #        autohide = userConfig.dock.settings.autohide;
# #        largesize = userConfig.dock.settings.large_size;
# #        magnification = userConfig.dock.settings.magnification;
# #        tilesize = userConfig.dock.settings.tile_size;
# #        # orientation = userConfig.dock.settings.position;
# #        # expose-group-apps = userConfig.dock.settings.expose_group_by_app;
# #        mru-spaces = userConfig.dock.settings.mru_spaces;
# #        minimize-to-application = userConfig.dock.settings.minimize_to_application;
# #        show-recents = userConfig.dock.settings.show_recent_apps;
# #        show-process-indicators = userConfig.dock.settings.show_process_indicators;
#       };

      finder = {
        AppleShowAllExtensions = false;
        _FXShowPosixPathInTitle = false;
        FXPreferredViewStyle = "Nlsv";
  #     defaults write com.apple.finder ShowPathbar -bool true
  #     defaults write com.apple.finder ShowStatusBar -bool true
      };

      # todo: move to user config?

      trackpad = {
        Clicking = true;

        # --------------------------------------
        # region Broken - these setting are not supported by nix-darwin yet :(
        # --------------------------------------
        # https://support.apple.com/en-us/102341
        # TrackpadThreeFingerDrag = false;

        # 2 = Mission Control
        # TrackpadThreeFingerVertSwipeGesture = 2;

        # 0 = Disabled
        # TrackpadFourFingerVertSwipeGesture = 0;

        # 2 = Application Windows
        # TrackpadThreeFingerHorizSwipeGesture = 2;

        # 0 = Disabled
        # TrackpadFourFingerHorizSwipeGesture = 0;
        
        # 0 = Disabled
        # 3 = Notifications Center
        # TrackpadTwoFingerFromRightEdgeSwipeGesture = 0;

        # --------------------------------------
        # endregion Broken - these setting are not supported by nix-darwin yet :(
        # --------------------------------------

        # "com.apple.AppleMultitouchTrackpad": {
        #   "TrackpadFourFingerHorizSwipeGesture": 2,
        #   "TrackpadPinch": 1,
        #   "TrackpadFourFingerVertSwipeGesture": 2,
        #   "USBMouseStopsTrackpad": 0,
        #   "ActuateDetents": 1,
        #   "TrackpadRotate": 1,
        #   "SecondClickThreshold": 1,
        #   "TrackpadHorizScroll": 1,
        #   "TrackpadTwoFingerDoubleTapGesture": 1,
        #   "UserPreferences": true,
        #   "TrackpadThreeFingerTapGesture": 0,
        #   "TrackpadThreeFingerHorizSwipeGesture": 2,
        #   "Clicking": true,
        #   "FirstClickThreshold": 1,
        #   "TrackpadFourFingerPinchGesture": 2,
        #   "TrackpadMomentumScroll": true,
        #   "DragLock": 0,
        #   "TrackpadFiveFingerPinchGesture": 2,
        #   "ForceSuppressed": false,
        #   "TrackpadThreeFingerVertSwipeGesture": 2,
        #   "TrackpadTwoFingerFromRightEdgeSwipeGesture": 3,
        #   "TrackpadScroll": true,
        #   "version": 12,
        #   "Dragging": 0,
        #   "TrackpadCornerSecondaryClick": 0,
        #   "TrackpadRightClick": true,
        #   "TrackpadHandResting": true,
        #   "TrackpadThreeFingerDrag": true
        # },
      };
    };
  };
}
