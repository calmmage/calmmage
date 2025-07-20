# Todos from 28 Dec

- [x] fix the issue in new project - something's wrong with
  cloning.. [note.md](../dev_env/tools/project_manager/issues/note.md)

# Todos from 11 Dec

- [ ] make sure our project picker for todo sees the mini-projects.. (now it goes to repo root)
- [ ] bugfix the ordering of todo files in todo rollup

- [ ] convert all headers in the todos to one level deeper (# -> ##)

# Todos from 09 Dec

- [x] fix ipython alias
	- make it the same as typer
	- delete old symlink
	- who creates it? 
- [x] make it so 'python' works?
	- option 1: add shell script that creates softlink
	- o2: try to link trhough brew?
	- No, this was explicitly removed to emphasise python3 - not python 2 - usage and avoid confusion. Just make a habit of using python3 from now on. and pip3 for that matter

# Todos from 05 Dec

- [ ] Fix issue in fix_repo - repo_fixer.py:fix_repo:646 - Error during Operation.RUN_ALL: [Errno 2] No such file or directory: 'pre-commit'

- [ ] install ~/.dev_env on nix setup / bootstrap
	- poetry install (packages and proejct)

- [ ] add alias "add todo" and maybe others in addition to "new todo" / nt

- [ ] auto-roll old todo file into a single document with proper header? (#todo {date} ... )

# Todos from 27 Nov

- [ ] merge branches properly

## make nix configure new things
- homebrew vs nix-homebrew
- (poetry2nix) or (configure proper poetry env somewhere)
- x86 vs aarch
- devenv enable / disable
- direnv enable / disable
- custom shell scripts enable / disable

## fix nix issues
- [x] what makes my trackpad gestures misconfigured? - fix that
    - [x] dump
    - [x] change
    - [x] dump again

## fix_repo
- discover project  name in poetry or something
- ask project name
- add vulture config to pyproject
- fix vulture config
- fix test job on github (rename to tests)

## project_manager
- better project auto-sorting
- add project
- add mini-project
- work on an existing project (asks for name / feature)
- add task / todo / idea (writes to a dev/todo_{date}.md file)

# Past

- [x] 1) Move home-manager home.packages = with pkgs; [
 to ... config user.yaml

2) 
   - setup user config
   - delete my apps
   - apply nix 

- [x] 3) Move brew packages list to user.yaml


4) Invent a better structure for specific configs:
   - user-specific aliases?
   - user-specific bashrc / zshrc values - e.g. local? 

5) create a private personal.nix file with local settings, aliases etc.. 
   
6) learning tools
- create aliases for useful tools
- make a list of common actions and tools for them (accompanied by aliases)
- a tool for used /aliased and unused / unaliased tools (three categories: used, unused, ingored)


- [x] deduplicate brew and home-manager packages with preference to home-manager
- [x] add brew tools from brew dump
- [x] add tools from claude suggested tools (and aliases)
- [ ] figure out how to better store aliases: in nix-file or in .aliases file?
- [ ] add aliases for better tool replacements:
  - [ ] alias cd -> z/zoxide
  - [ ] alias ls -> exa
  - [ ] alias find -> fd
  - [ ] alias grep -> rg
  - [ ] alias cat -> bat
  - [ ] alias top -> btop/htop
  - [ ] alias du -> dust/ncdu
  - [ ] alias diff -> delta
  - [ ] alias rm -> trash-cli
  - [ ] alias ping -> gping
  - [ ] alias traceroute -> mtr