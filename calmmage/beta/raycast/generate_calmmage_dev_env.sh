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

cd /Users/calm/work/code/structured/dev/calmmage-dev/calmmage/dev_env

git checkout main

git pull

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/calm/miniforge3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
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
