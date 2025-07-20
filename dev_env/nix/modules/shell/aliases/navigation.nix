{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    ll = "ls -la";
    cdr = "nocorrect change_dir_regexp";
    lsr = "nocorrect list_dir_regexp";
    cdf = "nocorrect change_dir_fuzzy";
    cdz = "z";
    cpa = "copy_absolute_path";
  };
} 