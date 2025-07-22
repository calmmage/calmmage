{ config, lib, pkgs, ... }:

let
  shellScriptsPath = ./sh;
  pythonScriptsPath = ./python;
in
{
  home.sessionVariables = {
    SHELL_SCRIPTS_PATH = "${shellScriptsPath}";
    PYTHON_SCRIPTS_PATH = "${pythonScriptsPath}";
  };

  home.file = {
    ".local/shell/scripts" = {
      source = shellScriptsPath;
      recursive = true;
    };
    ".local/shell/python" = {
      source = pythonScriptsPath;
      recursive = true;
    };
  };

  programs.zsh.initExtra = ''
    # Source all shell functions
    for f in ~/.local/shell/scripts/*.sh; do
      source "$f"
    done
  '';
}