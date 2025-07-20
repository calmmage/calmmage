{ config, lib, pkgs, ... }:

{
  imports = [
    ./new.nix
    ./navigation.nix
    ./better_tools.nix
  ];
} 