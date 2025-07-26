{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    # Poetry commands
    bump = "poetry version patch";  # Increment patch version number
    bump-minor = "poetry version minor";  # Increment minor version number
    bump-major = "poetry version major";  # Increment major version number

    uvup = "uv sync --upgrade --group test --group extras --group dev --group docs";
  };
} 