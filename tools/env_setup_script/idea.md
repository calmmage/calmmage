# Idea

Extra notes here: [general.md](../../experiments/season_4_jun_2025/_notes/projects/library_upgrades/general.md)

I want to add a simple script / cli tool (i guess, typer cli) that guides me through setting up all relevant ... env
variables and

1) loop over services + keys for each service
    - llm tools
        - openai
        - gemini
          ...
    - github
    - aws
    - google
    - cronitor

2) config.yaml for all relevant env keys?
3) for each key / service, possible actions:
    - check if key is already present in ~/.env
    - instructions to get the key
    - skip key
    - skip service

4) Add this to general calmmage/Makefile as a command
5) as always, use proper python env / uv command to run this (e.g. uv run typer run (path-to-script))