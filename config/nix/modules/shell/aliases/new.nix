{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    # Poetry commands
    bump = "poetry version patch";  # Increment patch version number
    uvup = "uv sync --upgrade --group test --group extras --group dev --group docs";
  };
} 