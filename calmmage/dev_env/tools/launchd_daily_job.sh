#!/bin/bash

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


# Execute your Python script
/Users/calm/miniforge3/envs/calmmage/bin/python /Users/calm/work/code/structured/tools/calmmage/calmmage/dev_env/tools/daily_job.py
