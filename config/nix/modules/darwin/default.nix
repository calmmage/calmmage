{ config, pkgs, ... }:

let
  # todo: remove, replace with my editor - cursor or something
  emacsOverlaySha256 = "06413w510jmld20i4lik9b36cfafm501864yq8k4vxl5r4hn0j0h";
in
{

  nixpkgs = {
    overlays =
      # Apply each overlay found in the /overlays directory
      let path = ../../overlays; in with builtins;
      map (n: import (path + ("/" + n)))
          (filter (n: match ".*\\.nix" n != null ||
                      pathExists (path + ("/" + n + "/default.nix")))
                  (attrNames (readDir path)))
      # Base configuration overlays
      ++ [
        (final: prev: {
          unstable = nixpkgs-unstable.legacyPackages.${prev.system};
        })
      ];

#      ++ [(import (builtins.fetchTarball {
#               url = "https://github.com/dustinlyons/emacs-overlay/archive/refs/heads/master.tar.gz";
#               sha256 = emacsOverlaySha256;
#           }))];
  };
}
