from pathlib import Path
import sys


def is_subsequence(sub: str, main: str):
    sub_index = 0
    main_index = 0
    while sub_index < len(sub) and main_index < len(main):
        if sub[sub_index] == main[main_index]:
            sub_index += 1
        main_index += 1
    return sub_index == len(sub)


def find_matching_dir(subsequence: str):
    base_path = Path(".")
    matching_dirs = [
        entry.name
        for entry in base_path.iterdir()
        if entry.is_dir() and is_subsequence(subsequence, entry.name)
    ]

    if len(matching_dirs) == 1:
        print(matching_dirs[0])
    elif len(matching_dirs) > 1:
        x = ", ".join(matching_dirs)
        raise ValueError(f"Too many matches: {x}")
    else:
        raise ValueError("No matches found")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: fuzzy_match.py <pattern>")
        sys.exit(1)
    try:
        find_matching_dir(sys.argv[1])
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
