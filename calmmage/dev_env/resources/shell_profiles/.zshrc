export HELP="This is a help message by Petr Lavrov, on Jan 2024

calmlib aliases:
np, new_project, pm, project_manager
cdl, cds, cdp - cd to latest, structured and playground
cd1, 2, 3 - same
# todo: construct this help message dynamically in calmmage_dev_env

personal aliases:
hetzner -

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

# add alias to add alias to ~/.alias
aa() {
    echo "" >> ~/.alias
    echo "# $3" >> ~/.alias
    echo "alias $1=\"$2\"" >> ~/.alias; source ~/.alias
}

move_and_link() {
    mv "$1" "$2" && ln -s "$2/${1##*/}" "$1"
}

find_project() {
    find ~/work -name "*$1*"
}

find_what_where() {
    grep -rnw "$2" -e "$1"
}

help() {
    # HELP=${HELP:-"No help available"}
    if [ -z "$1" ]; then
        echo "$HELP"
    else
        found=0
        for file in ~/.alias ~/.zshrc ~/.calmmage/.zshrc ~/.calmmage/.alias; do
            if [ -f "$file" ]; then
                grep -E "^alias $1=" "$file" > /dev/null && {
                    found=1
                    tac "$file" | sed -n "/^alias $1=/,/^#/{/^#/p}" | head -1
                    break
                }
            fi
        done
        [ "$found" -eq 0 ] && echo "Alias '$1' not found."
    fi
}
