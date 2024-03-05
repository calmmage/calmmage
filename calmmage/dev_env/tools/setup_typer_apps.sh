# let's write a script to set up typer cli apps with auto completion

# also, let's write a script to set up env variables required for calmmage to function

# 1) install typer-cli
pip install typer-cli

# 2) enable typer auto completion
typer --install-completion
# adds the following to .zshrc:
# autoload -Uz compinit
# zstyle ':completion:*' menu select
# fpath+=~/.zfunc
# compinit

# 3) install specific apps?
# get root dir of the repo - this file
root_dir=$(dirname $(realpath $0))
# todo: python $root_dir/project_actions.py --install-completion
# todo: python $root_dir/project_manager.py --install-completion
# todo 1: use the files directly from the ... lib
# todo 2: use the files copied to ~/calmmage by the setup script

# 4) add aliases for all the apps
# to calmmage aliases
# todo: move this to dev_env setup
# typer project_manage:app --install-completion

# alias project_manage
# alias project_actions
# command looks like this:
# typer project_manage:app --install-completion --name project_manage

# this is how alias line should look like:
# alias move_to_github="typer ($root_dir/project_actions.py) move"
