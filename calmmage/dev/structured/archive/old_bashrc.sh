
# ----------------------------------------
# alias and help

ai, ai4 - cli copilot
alias ai="python ~/home/tools/command-ai/main.py --prompt "
alias ai4="python ~/home/tools/command-ai/main.py --model gpt-4 --prompt "


# ----------------------------------------

source ~/.alias
# HELP="This is a help message by Petr Lavrov, on Apr 2022
# use 'help' command to see this message
#
# use 'ai' for inline CLI copilot
# use 'ai4' for gpt-4 copilot
#
# use 'gcu' alias to connect to the Google Compute Unit of Jarvis project
# use 'gcj' alias to connect to the Google Compute Unit of Jarvis project - as a service account
# gcn - google compute neuro
# gcns - google compute neuro, service account
# use 'alias' to see all other aliases"
# alias help="echo \"$HELP\""
# alias subl="/Applications/Sublime\ Text.app/Contents/MacOS/sublime_text"
#
# alias ai="python ~/home/tools/command-ai/main.py --prompt "
# alias ai4="python ~/home/tools/command-ai/main.py --model gpt-4 --prompt "
#
# alias gpt="cd /Users/calm/home/projects/2022_12_Dec/chatgpt_enhancer_bot/chatgpt_enhancer_bot"
#
# #alias gcn="(gcloud compute ssh --zone europe-central2-c instance-1 --project neuro-376122)"
# #alias gcns="(gcloud compute ssh --zone europe-central2-c neuro@instance-1 --project neuro-376122)"
# alias gcu1="(gcloud compute ssh --zone "europe-west6-a" "instance-1"  --project "jarvis-mar-2022-pub")"
# alias gcu="(gcloud compute ssh --zone "europe-west1-b" "instance-default-mar-2023"  --project "jarvis-mar-2022-pub")"
# alias gcj="(gcloud compute ssh --zone "europe-west6-a" "jarvis-service-account@instance-1"  --project "jarvis-mar-2022-pub")"


echo ""
help
echo ""

# ----------------------------------------
# copy files to/from GCP
function scpj() {
  gcloud compute scp --recurse jarvis-service-account@instance-1:$1 $2 --zone europe-west6-a --project jarvis-mar-2022-pub
}

function scps() {
gcloud compute scp --recurse $1 calm@instance-default-mar-2023:$2 --zone europe-west1-b --project jarvis-mar-2022-pub
}

# ----------------------------------------
# my MAC OS home dir
# ----------------------------------------

function add_to_path() {
    for dir in "$@"; do
        if ! echo "$PATH" | grep -q "$dir"; then
            export PATH="$dir:$PATH"
        fi
    done
}

add_to_path "/opt/homebrew/opt/python@3.11/libexec/bin"
add_to_path "/usr/local/opt/llvm/bin"  # clang, llvm
add_to_path "/Users/calm/.local/bin"  # poetry





# ----------------------------------------
# my MAC OS home dir
# ----------------------------------------

# go to default home location for this Mac (~/ is cluttered with MacOS system folders..)
# cd ~/home
echo "cd ~/home"
echo ""


alias git='nocorrect git'













# ----------------------------------------
# default zsh settings - auto-generated
# ----------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Below this line - default zsh settings

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
# plugins=(
# git
# )
plugins=(
	poetry
	# git
    aws
    gcloud
    npm
    python
    zsh-syntax-highlighting
    zsh-autosuggestions
    macos
	)
source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/calm/code/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/calm/code/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/calm/code/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/calm/code/google-cloud-sdk/completion.zsh.inc'; fi



# JINA_CLI_BEGIN

## autocomplete
if [[ ! -o interactive ]]; then
    return
fi

compctl -K _jina jina

_jina() {
  local words completions
  read -cA words

  if [ "${#words}" -eq 2 ]; then
    completions="$(jina commands)"
  else
    completions="$(jina completions ${words[2,-2]})"
  fi

  reply=(${(ps:
:)completions})
}

# session-wise fix
ulimit -n 4096
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# JINA_CLI_END









# ----------------------------------------
# DISABLED
# ----------------------------------------

# # >>> conda initialize >>>
# # !! Contents within this block are managed by 'conda init' !!
# __conda_setup="$('/Users/calm/code/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/Users/calm/code/anaconda3/etc/profile.d/conda.sh" ]; then
#         . "/Users/calm/code/anaconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/Users/calm/code/anaconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# # <<< conda initialize <<<


# # CUSTOM
# # Check if the current Python executable is from a conda environment
# if [[ $(which -a python) == *"conda"* ]]; then
#     if [[ $(which -a python) == *"env"* ]]; then
#         # The current Python executable is from a conda environment, do nothing
# #         echo "True: $(which -a python) == *'env'* "
#         echo "Warning: Detected conda env using 'which -a python'"
#         echo "This is currently not used to take any action"
#         echo "can be used to stop 'conda activate env'"
#         echo ""
# #     else
# #         echo "False: $(which -a python) == *'env'* "
#     fi
# fi
# if [[ $- == *i* ]]; then
#     # Interactive shell, try to activate conda env unless running in PyCharm
#     echo "Interactive shell, trying to activate conda env."
#     if [ -z "${IS_PYCHARM+x}" ]; then
#         # PYCHARM variable is unset, check if a conda environment is already activated
#         if [[ -n "$CONDA_DEFAULT_ENV" && "$CONDA_DEFAULT_ENV" != "base" ]]; then
#             # A non-base conda environment is already activated, log the environment name and skip activating the default environment
#             echo "Detected conda environment '$CONDA_DEFAULT_ENV', skipping activate conda env."
#             echo ""
#         else
#             # No conda environment is activated or only the 'base' environment is activated, log the default environment name and activate it
#             echo "No active conda env found, activating py311"
#             conda activate py311
#             python /Users/calm/home/lib/calmlib/calmlib/tools/startup_setup/startup.py
#         fi
#     else
#         # Running in PyCharm, skip activating conda env
#         echo "Running in PyCharm, activating $CONDA_DEFAULT_ENV"
#         echo ""
#     fi
# else
#     # Non-interactive shell, do nothing
#     echo "Non-interactive shell, skipping activate conda env."
#     echo ""
# fi

# this is some fucking garbage.
# I want a very simple logic:
# if not pycharm - activate 311
# if pycharm - activate whatever is set by env variables

# if [ -z "${IS_PYCHARM+x}" ]; then
#     echo ""
#     conda activate $PYCHARM_CONDA_ENV
# # else
# export MAIN_CONDA_ENV=py311
#
#
# if [ -z "${IS_PYCHARM+x}" ]; then
#     # Not running in PyCharm
#     if [[ $- == *i* ]]; then
#         # Interactive shell, try to activate conda env
#         echo "Interactive shell, trying to activate conda env."
#         if [[ -n "$CONDA_DEFAULT_ENV" && "$CONDA_DEFAULT_ENV" != "base" ]]; then
#             # A non-base conda environment is already activated, log the environment name and skip activating the default environment
#             echo "Detected conda environment '$CONDA_DEFAULT_ENV', skipping activate conda env."
#             echo ""
#         else
#             # No conda environment is activated or only the 'base' environment is activated, log the default environment name and activate it
#             echo "No active conda env found, activating $MAIN_CONDA_ENV"
#             conda activate $MAIN_CONDA_ENV
#         fi
#     else
#         # Non-interactive shell, skip activating conda env
#         echo "Non-interactive shell, skipping activate conda env."
#         echo ""
#     fi
# else
#     # Running in PyCharm, activate environment set by environment variables if PYCHARM_CONDA_ENV is set
#     if [ -z "${PYCHARM_CONDA_ENV+x}" ]; then
#         # PYCHARM_CONDA_ENV is unset, activate base environment or print error message
#         echo "Error: PYCHARM_CONDA_ENV environment variable is not set.
#         activating MAIN_CONDA_ENV: $MAIN_CONDA_ENV"
#         # Uncomment the following line to activate the base environment instead
#         conda activate $MAIN_CONDA_ENV
#     else
#         # PYCHARM_CONDA_ENV is set, activate the specified environment
#         echo "Running in PyCharm, activating $PYCHARM_CONDA_ENV environment"
#         conda activate $PYCHARM_CONDA_ENV
#     fi
# fi

alias .git='nocorrect .git'

