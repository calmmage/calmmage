{ config, lib, pkgs, ... }:

{
  programs.zsh.shellAliases = {
    # Navigation
    ls = "exa";  # Modern ls with git integration and colors
    tree1 = "broot";  # Interactive tree view with fuzzy search

    # Search
    find1 = "fd";  # User-friendly, fast alternative to find
    grep1 = "rg";  # Fast grep with better syntax and git integration
    locate1 = "plocate";  # Much faster locate
    
    # Process Management
    top = "btop";  # Interactive process viewer
    # ps = "procs";  # Modern replacement for ps
    ps1 = "procs";  # Modern replacement for ps
    kill1 = "fkill";  # Interactive process killer    
    # File Operations
    # cp = "rsync -ah --progress";  # Advanced copy with progress
    cp1 = "rsync -ah --progress";  # Advanced copy with progress
    cat1 = "bat";  # Cat with syntax highlighting
    less1 = "most";  # More feature-rich pager
    
    # System Monitoring
    df1 = "duf";  # Disk usage with better UI
    # du = "dust";  # Interactive disk usage analyzer
    free1 = "bottom";  # System resource monitor
    
    # Text Processing
    sed1 = "sd";  # Simpler syntax for sed
    diff1 = "delta";  # Git diff with syntax highlighting
    
    # Network
    ping = "gping";  # Ping with graph
    traceroute1 = "mtr";  # Better network diagnostics
    netstat1 = "ss";  # Modern netstat replacement
    
    # File Management
    rm = "trash";  # Safer alternative that moves to trash
    mkdir = "mkdir -p";  # Create parent directories automatically
  };
} 