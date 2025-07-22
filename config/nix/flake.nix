{
  description = "Darwin System Configuration with secrets for MacOS";

  nixConfig = {
    extra-substituters = [
      "https://nixpkgs-python.cachix.org"
      "https://devenv.cachix.org"
      "https://cache.nixos.org"
      "https://nix-community.cachix.org"
    ];
    extra-trusted-public-keys = [
      "nixpkgs-python.cachix.org-1:hxjI7pFxTyuTHn2NkvWCrAUcNZLNS3ZAvfYNuYifcEU="
      "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw="
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
    ];
  };

  inputs = {
#    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    agenix.url = "github:ryantm/agenix";
#    home-manager.url = "github:nix-community/home-manager";
    home-manager = {
      url = "github:nix-community/home-manager/release-24.11";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    darwin = {
      url = "github:nix-darwin/nix-darwin/nix-darwin-24.11";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix-homebrew = {
      url = "github:zhaofengli-wip/nix-homebrew";
    };
    homebrew-bundle = {
      url = "github:homebrew/homebrew-bundle";
      flake = false;
    };
    homebrew-core = {
      url = "github:homebrew/homebrew-core";
      flake = false;
    };
    homebrew-cask = {
      url = "github:homebrew/homebrew-cask";
      flake = false;
    }; 
    disko = {
      url = "github:nix-community/disko";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    # todo: add secrets back
#    secrets = {
#      url = "git+ssh://git@github.com/petrlavrov-sl/nix-secrets.git";
#      flake = false;
#    };
  };
  outputs = { self, darwin, nix-homebrew, homebrew-bundle, homebrew-core, homebrew-cask, home-manager, nixpkgs, nixpkgs-unstable, disko, poetry2nix, agenix, ... } @inputs: # , secrets # todo: add secrets back
  let
    lib = nixpkgs.lib;
    # Remove the hardcoded system
    # system = "aarch64-darwin";
    
    # Load user configs
    userConfigs = (import ./config/default.nix {}).userconfigs;

    # Define pythonOverlay here so it's available during initial pkgs setup
    pythonOverlay = final: prev: {
      ghostscript = prev.ghostscript.overrideAttrs (old: {
        doCheck = false;
      });
      
      python311 = prev.python311.override {
        packageOverrides = pyFinal: pyPrev: {
          dnspython = pyPrev.dnspython.overridePythonAttrs (old: {
            doCheck = false;
          });
          cherrypy = pyPrev.cherrypy.overridePythonAttrs (old: {
            doCheck = false;
          });
          matplotlib = pyPrev.matplotlib.overridePythonAttrs (old: {
            doCheck = false;
            buildInputs = builtins.filter (p: p.pname or "" != "ghostscript") (old.buildInputs or []);
          });
        };
      };
    };

    # Function to convert package strings to actual packages
    mkPackageSet = pkgs: packageNames: 
      map (name: 
        if builtins.isString name
        then 
          if name == "aspellDicts_en" then pkgs.aspellDicts.en
          else if name == "nodePackages_npm" then pkgs.nodePackages.npm
          else if name == "nodePackages_prettier" then pkgs.nodePackages.prettier
          else if name == "nodePackages_pnpm" then pkgs.nodePackages.pnpm
          else pkgs.${name}
        else name
      ) packageNames;

    # Initialize pkgs with overlays
    mkPkgs = userConfig: import nixpkgs {
      system = userConfig.system;  # Use system from config instead of system_arch
      overlays = [
        pythonOverlay
        # Conditionally include poetry2nix overlay
        (final: prev: 
          if userConfig.use_poetry2nix 
          then poetry2nix.overlays.default final prev
          else {})
        (final: prev: {
          # Convert string package names to actual packages
          userPackages = mkPackageSet prev userConfig.package_names;
        })
      ];
      config = {
        allowUnfree = true;
        allowBroken = true;
      };
    };

    # Update devShell to use system from config
    mkDevShell = system: let pkgs = nixpkgs.legacyPackages.${system}; in {
      default = with pkgs; mkShell {
        nativeBuildInputs = [ bashInteractive git age age-plugin-yubikey ];
        shellHook = ''
          export EDITOR=vim
        '';
      };
    };

    # Update mkApp to use system from config
    mkApp = system: scriptName: {
      type = "app";
      program = "${(nixpkgs.legacyPackages.${system}.writeScriptBin scriptName ''
        #!/usr/bin/env bash
        PATH=${nixpkgs.legacyPackages.${system}.git}/bin:$PATH
        echo "Running ${scriptName} for ${system}"
        exec ${self}/apps/aarch64-darwin/${scriptName}
      '')}/bin/${scriptName}";
    };
  in
  {
    darwinConfigurations = lib.mapAttrs (user: userConfig:
      let
        pkgs = mkPkgs userConfig;
      in
      darwin.lib.darwinSystem {
        system = userConfig.system;  # Use system from config instead of system_arch
        specialArgs = inputs // {
          inherit userConfig;
          pkgs = pkgs // {
            userPackages = pkgs.userPackages;
          };
        };
        modules = [
          {
            nixpkgs.config = {
              allowUnfree = true;
              allowBroken = true;
              allowInsecure = false;
              allowUnsupportedSystem = false;
            };
          }
          home-manager.darwinModules.home-manager
          nix-homebrew.darwinModules.nix-homebrew
          {
            nix-homebrew = {
              inherit user;
              enable = userConfig.use_nix_homebrew;
              taps = {
                "homebrew/homebrew-core" = homebrew-core;
                "homebrew/homebrew-cask" = homebrew-cask;
                "homebrew/homebrew-bundle" = homebrew-bundle;
              };
              mutableTaps = false;
              autoMigrate = true;
            };
          }
          ./hosts/darwin
        ];
      }
    ) userConfigs;

    # Create devShells for both architectures
    devShells = {
      "aarch64-darwin" = mkDevShell "aarch64-darwin";
      "x86_64-darwin" = mkDevShell "x86_64-darwin";
    };

    # Create apps for both architectures
    apps = {
      "aarch64-darwin" = {
        "apply" = mkApp "aarch64-darwin" "apply";
        "build" = mkApp "aarch64-darwin" "build";
        "build-switch" = mkApp "aarch64-darwin" "build-switch";
        "copy-keys" = mkApp "aarch64-darwin" "copy-keys";
        "create-keys" = mkApp "aarch64-darwin" "create-keys";
        "check-keys" = mkApp "aarch64-darwin" "check-keys";
        "rollback" = mkApp "aarch64-darwin" "rollback";
      };
      "x86_64-darwin" = {
        "apply" = mkApp "x86_64-darwin" "apply";
        "build" = mkApp "x86_64-darwin" "build";
        "build-switch" = mkApp "x86_64-darwin" "build-switch";
        "copy-keys" = mkApp "x86_64-darwin" "copy-keys";
        "create-keys" = mkApp "x86_64-darwin" "create-keys";
        "check-keys" = mkApp "x86_64-darwin" "check-keys";
        "rollback" = mkApp "x86_64-darwin" "rollback";
      };
    };
  };
}
