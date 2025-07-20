#!/usr/bin/env bash

function change_dir_fuzzy() {
    local match
    match=$("$SHELL_SCRIPTS_PATH/python/fuzzy_match.py" "$1")
    if [ $? -eq 0 ] && [ -n "$match" ]; then
        cd "$match"
    fi
}

function list_dir_regexp() {
    local pattern="*$(echo "$1" | sed 's/./&*/g')"
    ls $pattern
}

function change_dir_regexp() {
    local pattern="*$(echo "$1" | sed 's/./&*/g')"
    ls -d $pattern 2>/dev/null
    cd $pattern 2>/dev/null
}

# region paths
function copy_absolute_path() {
    local abs_path
    abs_path="$(readlink -f "${1:-.}")"
    echo "$abs_path" | pbcopy
    echo "Copied: $abs_path"
} 
# endregion paths