
# todo: move path to env vars?
cd /Users/calm/work/code/structured/tools/calmmage
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" != "main" ]; then
    git checkout main
else
    echo "Already on main branch"
fi

git fetch origin main

if [ -z "$(git diff origin/main)" ]; then
    echo "Local repository is up-to-date with remote repository. Proceeding..."
else
    echo "Local repository is not up-to-date with remote repository. Please update."
    git pull
fi

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
# todo: move path to env vars?
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

export PYTHONPATH="$PYTHONPATH:/Users/calm/work/code/structured/tools/calmmage:/Users/calm/work/code/structured/lib/calmlib"
