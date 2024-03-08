#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Generate Calmmage Dev Env
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🧙🏻‍
# @raycast.packageName generate-calmmage-dev-env

# Documentation:
# @raycast.author petr_lavrov
# @raycast.authorURL https://raycast.com/petr_lavrov

# - 'Regenerate calmmage dev env
#     - cd ...
#     - checkout main
#     - git pull
#     - run main.py

# todo: move path to env vars?
cd /Users/calm/work/code/structured/tools/calmmage/calmmage/dev_env
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" != "main" ]; then
    git checkout main
else
    echo "Already on main branch"
fi

git pull

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
# todo: move path to env vars?
__conda_setu p="$('/Users/calm/miniforge3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/calm/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/Users/calm/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/calm/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate calmmage

python main.py
```
