{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    # Git sync tool commands
    git-sync = "uv run typer tools/git_sync_tool/cli.py run";
#    git-sync-all = "uv run typer tools/git_sync_tool/cli.py run sync-all";
#    git-sync-all-dry = "uv run typer tools/git_sync_tool/cli.py run sync-all --dry-run";
#    git-sync-all-verbose = "uv run typer tools/git_sync_tool/cli.py run sync-all --verbose";
#    git-sync-single = "uv run typer tools/git_sync_tool/cli.py run sync";
    
    # Quick shortcuts
    gsync = "uv run typer tools/git_sync_tool/cli.py run sync-all";
    #gsync-dry = "uv run typer tools/git_sync_tool/cli.py run sync-all --dry-run";
    #gsync-v = "uv run typer tools/git_sync_tool/cli.py run sync-all --verbose";
  };
}