{
  username = "";# "petrlavrov";
  full_name = "";# "Petr Lavrov";
  email = "";# "petr.b.lavrov@gmail.com";
  computer_name = "";# "Petr's MacBook Pro 2";
  host_name = "";# "petrs-macbook-pro-2";
  secrets_repo_url = "";# "git+ssh://git@github.com/calmmage/nix-secrets.git";

  system = "aarch64-darwin";  # Apple Silicon Mac
#  system = "x86_64-darwin";  # Intel Mac

  enable_sudo_touch_id = false;

  use_direnv = false;
  use_devenv = false;
  # pick one or the other
   use_nix_homebrew = false;
#  use_nix_homebrew = true;
  use_poetry2nix = false;

  default_browser = "chrome";

#  dock = {
#    settings = {
#      # Visual settings
#      autohide = true;
#      magnification = true;
#      tile_size = 36;
#      large_size = 128;
#      position = "bottom";  # Can be "bottom", "left", or "right"
#      mru_spaces = false; # disable reordering spaces automatically based on recent usage (I hate them chaotically reordering)
#
#      # Behavior settings
#      expose_group_by_app = true;
#      minimize_to_application = true;
#      show_recent_apps = true;
#      show_process_indicators = true;
#    };
#
#    apps = [
#      "/Applications/Raycast.app"
#      "/System/Applications/System Settings.app"
#    ];
#  };

  homebrew = {
    brews = [

      # Development essentials
      "poetry"
      "uv"
      # "ripgrep"
      "python"
      "python@3.9"
      "python@3.11"
      "python@3.12"
      "python@3.13"
      "node"
      "git-lfs"
      "gcc"
      "yarn"
      "pinentry-mac"
      "npm"
      "pnpm"
    ];

    casks = [
      # Development Tools
      # "homebrew/cask/docker"
      # "visual-studio-code"

      # Utility Tools
      # "syncthing"

      # Development
      "docker"  # docker desktop app
      "jetbrains-toolbox"
      "pycharm"
      "sourcetree"
      "github" # github desktop app
      "launchcontrol"
      "warp"
      # - mitmproxy
      "cursor"
      # "zed"
      # "karabiner-elements"
      "sublime-text"

      # Browsers & Communication
      "google-chrome"
      "slack"
      "telegram"

      # Productivity & Utils
      "raycast"
      "rectangle" # window manager
      # "dropbox"
      "obsidian"
      "notion"
      "chatgpt"
      "shottr" # Alternative: CleanShot X - installed through setapp

      # App marketplace
      "setapp"
      # todo: add instructions for user to install apps manually
      # paste
      # cleanshotX
      # bartender
      # popclip
      # hazeover

      # Suggestions from Claude

      # Media Processing & Conversion
      # "ffmpeg"          # Swiss army knife for audio/video processing
      # "imagemagick"     # Powerful image manipulation tool
      # "handbrake"       # Video transcoder
      # "yt-dlp"          # Download videos from YouTube and other sites

      # # Development Tools
      # "neovim"          # Modern, extensible text editor
      # "tmux"            # Terminal multiplexer for multiple sessions
      # "httpie"          # User-friendly HTTP client
      # "mkcert"          # Make locally-trusted development certificates

      # # System Monitoring & Performance
      # "glances"         # System monitoring tool

      # # Network Tools
      # "nmap"            # Network exploration and security scanning
      # "wireshark"       # Network protocol analyzer
      # "netcat"         # Networking utility for reading/writing network connections
      # "mtr"             # Network diagnostic tool

      # # Security & Encryption
      # "gnupg"           # GNU Privacy Guard encryption
      # "bitwarden"       # Password manager
      # "1password"      # Popular password manager alternative
      # "veracrypt"       # Disk encryption software

      # # Productivity
      # "taskwarrior"     # Command-line task management
      # "pandoc"          # Universal document converter
      # "asciinema"       # Terminal session recorder

      # # Database Tools
      # - pgcli           # PostgreSQL CLI with auto-completion
      # - mycli           # MySQL/MariaDB CLI with auto-completion
      # "dbeaver"         # Universal database tool
      # "mongodb-compass" # MongoDB GUI

      # # Cloud & Infrastructure
      # - terraform       # Infrastructure as code
      # - kubernetes-cli  # Kubernetes command-line tool
      # "helm"            # Kubernetes package manager
      # "vagrant"         # Development environment creation

      # # File Management
      # "ranger"          # Console file manager with VI keybindings
      # "fzf"             # Command-line fuzzy finder
      # "rsync"           # Fast file copying tool
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

    masApps = {
      "flow" = 1423210932;
      "dropover" = 1355679052;
      "endel" = 1346247457;
      #  "1password" = 1333542190;
      #  "wireguard" = 1451685025;
    };
  };

  package_names = [
    # General packages for development and system management
    # "alacritty"
    "aspell"
    "aspellDicts_en" # converted to aspellDicts.en later
    "bash-completion"
    "btop"
    #  "coreutils"
    "killall"
    "neofetch"
    "openssh"
    "wget"
    "zip"

    # Encryption and security tools
    "age-plugin-yubikey"
    "gnupg"
    "libfido2"

    # Cloud-related tools and SDKs
    "docker"
    "docker-compose"

    # Media-related packages
#    emacs-all-the-icons-fonts
    "dejavu_fonts"
    "font-awesome"
    "hack-font"
#    "noto-fonts"
#    "noto-fonts-emoji"
    "meslo-lgs-nf"

    # Node.js development tools
    "hunspell"
    "iftop"
    "jetbrains-mono"
    "unrar"
    "unzip"

    # Python packages
    # "python3"
    # "virtualenv"

    # mac-specific
    # "dockutil"

    # CLI Tools
    # utils
    "curl"          # Command line tool for transferring data with URLs
    "less"          # Terminal pager for viewing file contents
    "cmake"           # Cross-platform build system generator
    "dlib"            # C++ toolkit for machine learning
    "tree"            # Directory listing in tree-like format
    "ffmpeg"          # Swiss army knife for audio/video processing

    # custom
    "gh"            # GitHub's official command line tool
    # docker        # CLI interface for Docker containers - conflicts with brew

    # style
    "oh-my-zsh"     # Framework for managing zsh configuration
    "zsh-powerlevel10k"  # Modern, fast zsh theme

    # new
    # new - to explore
    # controlled with a flag instead in user config + programs.nix
    # "direnv"        # Environment switcher for the shell
    # "devenv"        # Development environment manager
    "cachix"        # Binary cache hosting service for Nix
    "postman"       # API development environment

    # new - clear
    "awscli2"           # AWS command line interface v2

    # new - unclear
    "nixfmt-classic"     # Nix code formatter
    "pgbadger"        # PostgreSQL log analyzer
    "inetutils"       # Collection of common network utilities
    "git-remote-codecommit"  # Git remote helper for AWS CodeCommit
    "gitflow"         # Git branching model extension
    "shntool"         # Multi-purpose WAVE data processing tool
    "age"             # Simple, modern file encryption tool

    # via brew
    # "slack" 
    # "poetry"
    "ripgrep" # Fast grep alternative written in Rust

    # Suggestions from Claude
    "jq"              # Command-line JSON processor and manipulator
    "htop"            # Interactive process viewer and system monitor
    "tmux"            # Terminal multiplexer for multiple sessions
    "bat"             # Cat clone with syntax highlighting and git integration
    "eza"             # Modern replacement for ls with git integration (fork of exa)
    # "ncdu"            # NCurses disk usage analyzer
    "duf"             # Disk usage/free utility with better UI
    "tldr"            # Simplified and community-driven man pages

    # Adding from snapshot analysis
    "pkg-config"      # Build tool to help compile applications and libraries
    "openssl"        # SSL/TLS toolkit for secure communication
    "readline"       # Library for command-line editing
    "sqlite"         # Self-contained SQL database engine
    "xz"             # Data compression utility and library
    "zstd"           # Fast real-time compression algorithm
    "SDL2"           # Multimedia library for audio, video, input and more
    "gettext"        # Internationalization and localization system
    "libuv"          # Multi-platform support library with focus on asynchronous I/O
    # gcc is in brew instead
    # python versions are in brew instead

    # Navigation & File Management
    "zoxide"          # Better alternative to z/autojump
    "broot"          # Interactive tree view with fuzzy search
    "fd"             # User-friendly alternative to find
    "fzf"            # Command-line fuzzy finder
    "trash-cli"      # Safer alternative to rm

    # Process & System Monitoring
    "bottom"         # System resource monitor (btop)
    "procs"         # Modern replacement for ps

    # Text Processing & Viewing
    "sd"            # Simpler syntax for sed
    "most"          # More feature-rich pager than less
    "dust"          # More intuitive du
    "gping"         # Ping with graphs
    "mtr"           # Better traceroute

    # File Operations
    "rsync"         # Advanced file copying
    "delta"           # Syntax highlighting pager for git diffs
  ];

  npmPackages = [
    "prettier"
    # Add more global npm packages here
  ];
}