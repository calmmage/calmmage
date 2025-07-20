let
  shared = import ./shared.nix;
in
{
  username = "petrlavrov";
  full_name = "Petr Lavrov";
  email = "petr.b.lavrov@gmail.com";
  computer_name = "Petr's MacBook Pro 2";
  host_name = "petrs-macbook-pro-2";
  secrets_repo_url = "git+ssh://git@github.com/calmmage/nix-secrets.git";
  
  system = "aarch64-darwin";  # Apple Silicon Mac

  enable_sudo_touch_id = true;

  # use_direnv = true;
  use_direnv = false;
  use_devenv = true;
  # pick one or the other
  use_nix_homebrew = false;
  # use_nix_homebrew = true;

  use_poetry2nix = false;
  
  homebrew = {
    brews = shared.homebrew.brews ++ [
      # "sonar-scanner" is commented out
    ];

    casks = shared.homebrew.casks ++ [
        # Personal & Entertainment
        "discord"           # Gaming chat and communities
        "steam"            # Gaming platform
        "epic-games"       # Epic Games store
        "obs"              # Streaming and recording
        "kindle"           # Amazon's e-book reader
        "whatsapp"         # Messaging app
        "zoom"             # Video conferencing

        # Gaming & Creative
        "blender"          # 3D creation suite
        "unity-hub"        # Game development platform
        "minecraft"        # Gaming
        # "adobe-creative-cloud"

        # System & Utilities
        "grandperspective" # Disk space visualization
        "lastpass"         # Password manager

        # installing via setapp
        # "dropover"         # Drag and drop enhancement 
        # "hand-mirror"      # Quick camera check
        # "aldente"          # Battery management

        # Media & Entertainment
        "vlc"              # Media player
        "iina"            # Modern media player for macOS
    ];

    # These app IDs are from using the mas CLI app
    # mas = mac app store
    # https://github.com/mas-cli/mas
    #
    # $ nix shell nixpkgs#mas
    # $ mas search <app name>
    #
    # If you have previously added these apps to your Mac App Store profile (but not installed them on this system),
    # you may receive an error message "Redownload Unavailable with This Apple ID".
    # This message is safe to ignore. (https://github.com/dustinlyons/nixos-config/issues/83)

    masApps = shared.homebrew.masApps // {
      "hp-smart" = 1474276998;
      "amphetamine" = 937984704;
    };
  };

  package_names = shared.package_names ++ [
    # Add personal-specific packages here as strings
  ];

  npmPackages = shared.npmPackages ++ [
    # Add personal-specific npm packages here
  ];
}