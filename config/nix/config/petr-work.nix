let
  shared = import ./shared.nix;
in
{
  username = "petr";
  full_name = "Petr Lavrov";
  email = "petr@superlinear.com";
  computer_name = "Petr's MacBook Pro";
  host_name = "petrs-macbook-pro";
  secrets_repo_url = "git+ssh://git@github.com/petrlavrov-sl/nix-secrets.git";
  
  system = "aarch64-darwin";  # Apple Silicon Mac

  enable_sudo_touch_id = true;

  use_direnv = true;
  use_devenv = false;
  # pick one or the other
  # use_nix_homebrew = false;
  use_nix_homebrew = true;
  use_poetry2nix = false;

  homebrew = {
    brews = shared.homebrew.brews ++ [
      "sonar-scanner"
    ];

    casks = shared.homebrew.casks ++ [
      # Communication
#      "microsoft-teams"
      "ollama"
      "zed"
      "windsurf"
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
      # Add work-specific Mac App Store apps here
    };
  };

  package_names = shared.package_names ++ [
    # Add work-specific packages here

    "teams"           # Microsoft Teams client
  ];

  npmPackages = shared.npmPackages ++ [
    # Add work-specific npm packages here
  ];
}
