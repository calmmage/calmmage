
# region search
find_project() {
    /usr/bin/find ${2:-~/work} -type d -name "*$1*"
}

find_file() {
    rg -g "*$1*" --files ${2:-.}
}

# endregion search