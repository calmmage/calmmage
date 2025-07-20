# New Nix Setup 2024-11-21 update

- gpg
  - use `gpg --full-generate-key` to generate a new key (4096 bits!)
  - configure pycharm to use gpg (search gpg in settings)
- ssh
  - use `nix run .create-keys` command to generate keys
  - ??? check: do i need to add to ssh agent?
  - ??? add to github manually? 
- secrets
  - create a new private repo in github
  - configure local git to use ssh
    - how to do that wihtout conflicts, with multiple remote profiles? 

--------------------------------

# Setup from scratch

Follow this YouTube video:

[Walkthrough of Nix Install and Setup on MacOS](https://www.youtube.com/watch?v=LE5JR4JcvMg&t=2773s)

...

Install Nix

Install nix-darwin

`darwin-rebuild switch --flake $ACTIVE_DEV_ENV_DIR/nix/.#`

Cachix

nix profile install nixpkgs#cachix

cachix use devenv

After the above runs successfully, use the alias `nixswitch` instead.
