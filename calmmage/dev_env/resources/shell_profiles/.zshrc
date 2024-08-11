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

# add alias to add alias to ~/.alias
add_alias() {
    echo "" >> ~/.alias
    echo "# $3" >> ~/.alias
    echo "alias $1=\"$2\"" >> ~/.alias; source ~/.alias
}

move_and_link() {
    # Ensure both arguments are provided
    if [ $# -ne 2 ]; then
        echo "Usage: move_and_link <source> <destination>"
        return 1
    fi
    # Get the absolute paths
    source=$(realpath "$1")
    source_base=$(basename "$1")
    # Move the source to the destination
    mv "$1" "$2"
    destination=$(realpath "$2")
    destination_base=$(basename "$2")
    echo "Moved $source to $destination"
    # Create a symlink at the original source location pointing to the new location
    if [ "$destination_base" = "$source_base" ]; then
        ln -s "$destination" "$source"
        echo "Linked $source to $destination"
    else
        ln -s "$destination/$source_base" "$source"
        echo "Linked $source to $destination/$source_base"
    fi
}

find_project() {
    find ~/work -name "*$1*"
}

find_what_where() {
    grep -rnw "$2" -e "$1"
}

# todo: replace this with a fancy ai help that queries chatgpt
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

copy_absolute_path() {
    local abs_path="$(readlink -f "$1")"
    echo "$abs_path" | pbcopy
    echo "Copied: $abs_path"
}
