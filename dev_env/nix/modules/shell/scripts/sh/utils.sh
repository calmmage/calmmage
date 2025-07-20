#!/usr/bin/env bash

# region softlinks
function move_and_link() {
    if [ $# -ne 2 ]; then
        echo "Usage: move_and_link <source> <destination>"
        return 1
    fi
    local source source_base destination destination_base
    source=$(realpath "$1")
    source_base=$(basename "$1")
    mv "$1" "$2"
    destination=$(realpath "$2")
    destination_base=$(basename "$2")
    echo "Moved $source to $destination"
    
    if [ "$destination_base" = "$source_base" ]; then
        ln -s "$destination" "$source"
        echo "Linked $source to $destination"
    else
        ln -s "$destination/$source_base" "$source"
        echo "Linked $source to $destination/$source_base"
    fi
}
# endregion softlinks


# todo: replace this with a fancy ai help that queries chatgpt? 
function help() {
    if [ -z "$1" ]; then
        echo "$HELP"
    else
        local found=0
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