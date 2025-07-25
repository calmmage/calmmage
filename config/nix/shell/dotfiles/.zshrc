# ------------------------------------------------------------------------------
# verified

export PATH=~/.npm-global/bin:$PATH

# make sure the dev-env location is available
[ -f ~/.dev-env-location ] && source ~/.dev-env-location

# Add warning if DEV_ENV_PATH is not set
if [ -z "$CALMMAGE_DIR" ]; then
    echo "Warning: CALMMAGE_DIR is not set."
    echo "This variable should point to the root directory of your calmmage development environment."
    echo " "
    echo "Example: To add a Python tool located at \$CALMMAGE_DIR/tools/your_tool.py:"
    echo "1. Ensure your_tool.py is executable (chmod +x \$CALMMAGE_DIR/tools/your_tool.py)."
    echo "     alias toolname=\"$CALMMAGE_VENV_PATH/bin/python $CALMMAGE_DIR/tools/your_tool.py\""
    echo " "
    echo "     alias toolname=\"\$CALMMAGE_VENV_PATH/bin/typer $CALMMAGE_DIR/tools/your_tool/your_tool.py\""
    echo "3. Add the alias to your ~/.aliases file."
    echo "4. Reload your shell or run 'source ~/.aliases'."
fi

# Function to explain how to add a new tool alias
add_tool() {
    echo "Instructions for adding a new tool alias:"
    echo "1. Make sure CALMMAGE_DIR is set correctly at ~/.dev-env-location"
    echo "2. Add your tool script to dev_env repo in tools/"
    echo "3. Add an alias to dev_env/nix/modules/home-manager/dotfiles/zshrc in one of these formats:"
    echo "   - For direct Python scripts:"
    echo "     alias toolname=\"$CALMMAGE_VENV_PATH/bin/python \$CALMMAGE_DIR/tools/your_tool.py\""
    echo "   - For Typer CLI tools:" 
    echo "     alias toolname=\"\$CALMMAGE_VENV_PATH/bin/typer \$CALMMAGE_DIR/tools/your_tool/your_tool.py\""
    echo "4. nix-shell -p zsh"
    echo "5. source ~/.zshrc (or restart your terminal)"
}

alias_() {
    # Create a temporary file to store the excluded aliases
    local excluded_file="/tmp/excluded_aliases.txt"
    
    # Here you can paste your excluded aliases directly in this format
    cat > "$excluded_file" << 'EOL'
....=../../..
.....=../../../..
......=../../../../..
2='cd -2'
3='cd -3'
4='cd -4'
5='cd -5'
6='cd -6'
7='cd -7'
8='cd -8'
9='cd -9'
dbl='docker build'
dc=docker-compose
dcin='docker container inspect'
dcls='docker container ls'
dclsa='docker container ls -a'
dib='docker image build'
dii='docker image inspect'
dils='docker image ls'
dipu='docker image push'
dirm='docker image rm'
dit='docker image tag'
dlo='docker container logs'
dnc='docker network create'
dncn='docker network connect'
dndcn='docker network disconnect'
dni='docker network inspect'
dnls='docker network ls'
dnrm='docker network rm'
dpo='docker container port'
dpu='docker pull'
dr='docker container run'
drit='docker container run -it'
drm='docker container rm'
'drm!'='docker container rm -f'
drs='docker container restart'
dst='docker container start'
dsta='docker stop $(docker ps -q)'
dstp='docker container stop'
dtop='docker top'
dvi='docker volume inspect'
dvls='docker volume ls'
dvprune='docker volume prune'
dxc='docker container exec'
dxcit='docker container exec -it'
k=kubectl
kaf='kubectl apply -f'
kca='_kca(){ kubectl "$@" --all-namespaces;  unset -f _kca; }; _kca'
kccc='kubectl config current-context'
kcdc='kubectl config delete-context'
kcgc='kubectl config get-contexts'
kcn='kubectl config set-context --current --namespace'
kcp='kubectl cp'
kcsc='kubectl config set-context'
kcuc='kubectl config use-context'
kdcj='kubectl describe cronjob'
kdcm='kubectl describe configmap'
kdd='kubectl describe deployment'
kdds='kubectl describe daemonset'
kdel='kubectl delete'
kdelcj='kubectl delete cronjob'
kdelcm='kubectl delete configmap'
kdeld='kubectl delete deployment'
kdelds='kubectl delete daemonset'
kdelf='kubectl delete -f'
kdeli='kubectl delete ingress'
kdelj='kubectl delete job'
kdelno='kubectl delete node'
kdelns='kubectl delete namespace'
kdelp='kubectl delete pods'
kdelpvc='kubectl delete pvc'
kdels='kubectl delete svc'
kdelsa='kubectl delete sa'
kdelsec='kubectl delete secret'
kdelss='kubectl delete statefulset'
kdi='kubectl describe ingress'
kdj='kubectl describe job'
kdno='kubectl describe node'
kdns='kubectl describe namespace'
kdp='kubectl describe pods'
kdpvc='kubectl describe pvc'
kdrs='kubectl describe replicaset'
kds='kubectl describe svc'
kdsa='kubectl describe sa'
kdsec='kubectl describe secret'
kdss='kubectl describe statefulset'
kecj='kubectl edit cronjob'
kecm='kubectl edit configmap'
ked='kubectl edit deployment'
keds='kubectl edit daemonset'
kei='kubectl edit ingress'
kej='kubectl edit job'
keno='kubectl edit node'
kens='kubectl edit namespace'
kep='kubectl edit pods'
kepvc='kubectl edit pvc'
kers='kubectl edit replicaset'
kes='kubectl edit svc'
kess='kubectl edit statefulset'
keti='kubectl exec -t -i'
kga='kubectl get all'
kgaa='kubectl get all --all-namespaces'
kgcj='kubectl get cronjob'
kgcm='kubectl get configmaps'
kgcma='kubectl get configmaps --all-namespaces'
kgd='kubectl get deployment'
kgda='kubectl get deployment --all-namespaces'
kgds='kubectl get daemonset'
kgdsa='kubectl get daemonset --all-namespaces'
kgdsw='kgds --watch'
kgdw='kgd --watch'
kgdwide='kgd -o wide'
kgi='kubectl get ingress'
kgia='kubectl get ingress --all-namespaces'
kgj='kubectl get job'
kgno='kubectl get nodes'
kgns='kubectl get namespaces'
kgp='kubectl get pods'
kgpa='kubectl get pods --all-namespaces'
kgpall='kubectl get pods --all-namespaces -o wide'
kgpl='kgp -l'
kgpn='kgp -n'
kgpvc='kubectl get pvc'
kgpvca='kubectl get pvc --all-namespaces'
kgpvcw='kgpvc --watch'
kgpw='kgp --watch'
kgpwide='kgp -o wide'
kgrs='kubectl get replicaset'
kgs='kubectl get svc'
kgsa='kubectl get svc --all-namespaces'
kgsec='kubectl get secret'
kgseca='kubectl get secret --all-namespaces'
kgss='kubectl get statefulset'
kgssa='kubectl get statefulset --all-namespaces'
kgssw='kgss --watch'
kgsswide='kgss -o wide'
kgsw='kgs --watch'
kgswide='kgs -o wide'
kl='kubectl logs'
kl1h='kubectl logs --since 1h'
kl1m='kubectl logs --since 1m'
kl1s='kubectl logs --since 1s'
klf='kubectl logs -f'
klf1h='kubectl logs --since 1h -f'
klf1m='kubectl logs --since 1m -f'
klf1s='kubectl logs --since 1s -f'
kpf='kubectl port-forward'
krh='kubectl rollout history'
krsd='kubectl rollout status deployment'
krsss='kubectl rollout status statefulset'
kru='kubectl rollout undo'
ksd='kubectl scale deployment'
ksss='kubectl scale statefulset'
npmD='npm i -D '
npmE='PATH="$(npm bin)":"$PATH"'
npmF='npm i -f'
npmI='npm init'
npmL='npm list'
npmL0='npm ls --depth=0'
npmO='npm outdated'
npmP='npm publish'
npmR='npm run'
npmS='npm i -S '
npmSe='npm search'
npmU='npm update'
npmV='npm -v'
npmg='npm i -g '
npmi='npm info'
npmrb='npm run build'
npmrd='npm run dev'
npmst='npm start'
npmt='npm test'
EOL

    # Get excluded alias names
    local excluded_names=($(cut -d'=' -f1 "$excluded_file"))
    
    # Get all aliases and process them line by line
    alias | while read -r line; do
        # Extract alias name (everything before the first '=')
        local alias_name=$(echo "$line" | cut -d'=' -f1 | cut -d' ' -f2)
        
        # Check if alias is not in excluded list
        if [[ ! " ${excluded_names[@]} " =~ " ${alias_name} " ]]; then
            echo "$line"
        fi
    done
    
    # Clean up
    rm "$excluded_file"
}

myalias() {
    # Create a temporary file to store the excluded aliases
    local excluded_file="/tmp/excluded_aliases.txt"
    
    # Here you can paste your excluded aliases directly in this format
    cat > "$excluded_file" << 'EOL'
-='cd -'
...=../..
....=../../..
.....=../../../..
......=../../../../..
1='cd -1'
2='cd -2'
3='cd -3'
4='cd -4'
5='cd -5'
6='cd -6'
7='cd -7'
8='cd -8'
9='cd -9'
_='sudo '
cat=bat
cp='rsync -ah --progress'
dbl='docker build'
dc=docker-compose
dcin='docker container inspect'
dcls='docker container ls'
dclsa='docker container ls -a'
df=duf
dib='docker image build'
diff=delta
dii='docker image inspect'
dils='docker image ls'
dipu='docker image push'
dirm='docker image rm'
dit='docker image tag'
dlo='docker container logs'
dnc='docker network create'
dncn='docker network connect'
dndcn='docker network disconnect'
dni='docker network inspect'
dnls='docker network ls'
dnrm='docker network rm'
dpo='docker container port'
dpu='docker pull'
dr='docker container run'
drit='docker container run -it'
drm='docker container rm'
'drm!'='docker container rm -f'
drs='docker container restart'
dst='docker container start'
dsta='docker stop $(docker ps -q)'
dstp='docker container stop'
dtop='docker top'
dvi='docker volume inspect'
dvls='docker volume ls'
dvprune='docker volume prune'
dxc='docker container exec'
dxcit='docker container exec -it'
egrep='grep -E --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox}'
ff=find_file
fgrep='grep -F --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox}'
find=fd
free=bottom
g=git
globurl='noglob urlglobber '
grep=rg
hidefiles='defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder'
history=omz_history
k=kubectl
kaf='kubectl apply -f'
kca='_kca(){ kubectl "$@" --all-namespaces;  unset -f _kca; }; _kca'
kccc='kubectl config current-context'
kcdc='kubectl config delete-context'
kcgc='kubectl config get-contexts'
kcn='kubectl config set-context --current --namespace'
kcp='kubectl cp'
kcsc='kubectl config set-context'
kcuc='kubectl config use-context'
kdcj='kubectl describe cronjob'
kdcm='kubectl describe configmap'
kdd='kubectl describe deployment'
kdds='kubectl describe daemonset'
kdel='kubectl delete'
kdelcj='kubectl delete cronjob'
kdelcm='kubectl delete configmap'
kdeld='kubectl delete deployment'
kdelds='kubectl delete daemonset'
kdelf='kubectl delete -f'
kdeli='kubectl delete ingress'
kdelj='kubectl delete job'
kdelno='kubectl delete node'
kdelns='kubectl delete namespace'
kdelp='kubectl delete pods'
kdelpvc='kubectl delete pvc'
kdels='kubectl delete svc'
kdelsa='kubectl delete sa'
kdelsec='kubectl delete secret'
kdelss='kubectl delete statefulset'
kdi='kubectl describe ingress'
kdj='kubectl describe job'
kdno='kubectl describe node'
kdns='kubectl describe namespace'
kdp='kubectl describe pods'
kdpvc='kubectl describe pvc'
kdrs='kubectl describe replicaset'
kds='kubectl describe svc'
kdsa='kubectl describe sa'
kdsec='kubectl describe secret'
kdss='kubectl describe statefulset'
kecj='kubectl edit cronjob'
kecm='kubectl edit configmap'
ked='kubectl edit deployment'
keds='kubectl edit daemonset'
kei='kubectl edit ingress'
kej='kubectl edit job'
keno='kubectl edit node'
kens='kubectl edit namespace'
kep='kubectl edit pods'
kepvc='kubectl edit pvc'
kers='kubectl edit replicaset'
kes='kubectl edit svc'
kess='kubectl edit statefulset'
keti='kubectl exec -t -i'
kga='kubectl get all'
kgaa='kubectl get all --all-namespaces'
kgcj='kubectl get cronjob'
kgcm='kubectl get configmaps'
kgcma='kubectl get configmaps --all-namespaces'
kgd='kubectl get deployment'
kgda='kubectl get deployment --all-namespaces'
kgds='kubectl get daemonset'
kgdsa='kubectl get daemonset --all-namespaces'
kgdsw='kgds --watch'
kgdw='kgd --watch'
kgdwide='kgd -o wide'
kgi='kubectl get ingress'
kgia='kubectl get ingress --all-namespaces'
kgj='kubectl get job'
kgno='kubectl get nodes'
kgns='kubectl get namespaces'
kgp='kubectl get pods'
kgpa='kubectl get pods --all-namespaces'
kgpall='kubectl get pods --all-namespaces -o wide'
kgpl='kgp -l'
kgpn='kgp -n'
kgpvc='kubectl get pvc'
kgpvca='kubectl get pvc --all-namespaces'
kgpvcw='kgpvc --watch'
kgpw='kgp --watch'
kgpwide='kgp -o wide'
kgrs='kubectl get replicaset'
kgs='kubectl get svc'
kgsa='kubectl get svc --all-namespaces'
kgsec='kubectl get secret'
kgseca='kubectl get secret --all-namespaces'
kgss='kubectl get statefulset'
kgssa='kubectl get statefulset --all-namespaces'
kgssw='kgss --watch'
kgsswide='kgss -o wide'
kgsw='kgs --watch'
kgswide='kgs -o wide'
kl='kubectl logs'
kl1h='kubectl logs --since 1h'
kl1m='kubectl logs --since 1m'
kl1s='kubectl logs --since 1s'
klf='kubectl logs -f'
klf1h='kubectl logs --since 1h -f'
klf1m='kubectl logs --since 1m -f'
klf1s='kubectl logs --since 1s -f'
kpf='kubectl port-forward'
krh='kubectl rollout history'
krsd='kubectl rollout status deployment'
krsss='kubectl rollout status statefulset'
kru='kubectl rollout undo'
ksd='kubectl scale deployment'
ksss='kubectl scale statefulset'
l='ls -lah'
la='ls -lAh'
less=most
ll='ls -la'
locate=plocate
ls=exa
lsa='ls -lah'
lsr='nocorrect list_dir_regexp'
md='mkdir -p'
mkdir='mkdir -p'
netstat=ss
npmD='npm i -D '
npmE='PATH="$(npm bin)":"$PATH"'
npmF='npm i -f'
npmI='npm init'
npmL='npm list'
npmL0='npm ls --depth=0'
npmO='npm outdated'
npmP='npm publish'
npmR='npm run'
npmS='npm i -S '
npmSe='npm search'
npmU='npm update'
npmV='npm -v'
npmg='npm i -g '
npmi='npm info'
npmrb='npm run build'
npmrd='npm run dev'
npmst='npm start'
npmt='npm test'
ping=gping
pn=pnpm
ps=procs
px=pnpx
py=python3
pyfind='find . -name "*.py"'
pygrep='grep -nr --include="*.py"'
pyserver='python3 -m http.server'
rd=rmdir
rm=trash
run-help=man
search=rg
sed=sd
showfiles='defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder'
top=btop
traceroute=mtr
tree_=broot
which-command=whence
EOL

    # Get excluded alias names
    local excluded_names=($(cut -d'=' -f1 "$excluded_file"))
    
    # Get all aliases and process them line by line
    alias | while read -r line; do
        # Extract alias name (everything before the first '=')
        local alias_name=$(echo "$line" | cut -d'=' -f1 | cut -d' ' -f2)
        
        # Check if alias is not in excluded list
        if [[ ! " ${excluded_names[@]} " =~ " ${alias_name} " ]]; then
            echo "$line"
        fi
    done
    
    # Clean up
    rm "$excluded_file"
}

# ------------------------------------------------------------------------------
#
#
#
#
#
#
#
#
#
#
#
#
#
# ------------------------------------------------------------------------------
# unverified


export HELP="This is a help message by Petr Lavrov, on Jan 2024

calmlib aliases:
np, new_project, pm, project_manager
cdl, cds, cdp - cd to latest, structured and playground
cd1, 2, 3 - same
# todo: construct this help message dynamically in calmmage_dev_env
cdr, lsr, cdf - fuzzy match cd and ls

personal aliases:
hetzner - ssh to hetzner server

fp - find project (find dir / file name in ~/work)
find_ \$text \$path - find text in file (grep all text instances in dir)
mva - move the dir to new location and leave a symlink instead

pro cli libs:
ghc / gh copilot - github copilot cli
aie - gh copilot explain
ais - gh copilot suggest

tree
awk, grep

todo: add a personal, code-aware ai helper with vector store
quick: simple vector store code snippet search
aliases: import a code chunk / notebook / dir
more: knowledge base, similar.
"




# find_what_where() {
#     grep -rnw "$2" -e "$1"
# }




# cdf prj -> cd if is_substring(prj, dir). Fails on multi-match; See also: cdf
change_dir_fuzzy() {
    # Python script handling all logic including match count
    python_code="from pathlib import Path
# from calmlib.utils.common import is_subsequence

def is_subsequence(sub: str, main: str):
    sub_index = 0
    main_index = 0
    while sub_index < len(sub) and main_index < len(main):
        if sub[sub_index] == main[main_index]:
            sub_index += 1
        main_index += 1
    return sub_index == len(sub)

subsequence = '$1'
base_path = Path('.')
matching_dirs = [entry.name for entry in base_path.iterdir() if entry.is_dir() and is_subsequence(subsequence, entry.name)]

if len(matching_dirs) == 1:
    print(matching_dirs[0])
elif len(matching_dirs) > 1:
    x = ', '.join(matching_dirs)
    raise ValueError(f'Too many matches: {x}')
else:
    raise ValueError('No matches found')"

    # Execute the complete Python script and handle exceptions
    local match=$(python -c "$python_code")

    if [ -n "$match" ]; then
        # Only one match, change directory
        cd "$match"
    fi
}
# lsr abc -> ls *a*b*c*
list_dir_regexp() {
    dir_regexp=$(python -c "print('*'+'*'.join('$1')+'*')")
    eval "ls $dir_regexp"
}

# cdr prj -> cd *p*r*j*; See also: cdf
change_dir_regexp() {
    # Execute the Python script and store the result
    dir_regexp=$(python -c "print('*'+'*'.join('$1')+'*')")
    eval "ls -d $dir_regexp"
    # echo $dir_regexp
    # dir_names=$(echo ($dir_regexp))
    # echo $dir_names
    # ls ($dir_regexp)
    eval "cd $dir_regexp 2>/dev/null"
}


# requires export DEV_ENV_PATH="/path/to/poetry/env"
# default - DEV_ENV_PATH="$HOME/.calmmage/dev_env/.venv"
# export PROJECTS_ROOT="$HOME/work/projects"

run_with_poetry() {
    # Check if the environment variable is set
    if [ -z "$CALMMAGE_DIR" ]; then
        echo "Warning: CALMMAGE_DIR is not set. Some aliases may not work."
        echo "Poetry environment not found or activated."
        return 1
    fi

    # Check if a script path is provided as an argument
    if [ $# -eq 0 ]; then
        echo "Error: No script path provided"
        echo "Usage: run_with_poetry <script_path> [args...]"
        return 1
    fi

    # Get the script path (first argument)
    local SCRIPT_PATH="$1"
    shift  # Remove the first argument, leaving any additional args

    # Check if the script exists
    if [ ! -f "$SCRIPT_PATH" ]; then
        echo "Error: Script not found at $SCRIPT_PATH"
        return 1
    fi

    # Activate the Poetry environment, run the script with any additional args, and deactivate
    (
        source "$CALMMAGE_VENV_PATH/bin/activate" && \
        python "$SCRIPT_PATH" "$@" && \
        deactivate
    )
}

# requires export CALMMAGE_DIR="/path/to/stable/dev/env"
# default - CALMMAGE_DIR="/Users/petrlavrov/calmmage/config/"
# requires export CALMMAGE_VENV_PATH="/path/to/stable/venv"
# default - CALMMAGE_VENV_PATH="/Users/petrlavrov/calmmage/config/.venv"
