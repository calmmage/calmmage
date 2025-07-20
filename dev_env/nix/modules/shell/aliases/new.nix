{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    # Poetry commands
    bump = "poetry version patch";  # Increment patch version number
  };
} 