# Idea

We're building local automation jobs

There are three key modalities
- cronicle job (this is a standalone run of a serious tool with configurable env variables etc.)
-

# Key components and locations
- we put tools at ~/calmmage/tools/...
    - import everything by abs path - so from tools.tool_name.file ...
- we put shared code - enums, reusable classes, data models etc. at ~/calmmage/src/lib
    - import by abs path too
- we put the automated job to a corresponding place
    - scripts/cronicle/{job_name}/run.py - if that's for cronicle
    - scripts/scheduled_jobs/ .. - if that's for local scheduler
    - cli.py - if we're developing an interactive cli tool - in the tool dir
- Surfacing information to the user
  Implemented
    - ping / status to the cronitor
        - todo: add util to calmlib that gets cronitor id (for url) from .env
          todo: add a calmmage setup script that makes sure
        - todo: use ai to generate proper cronitor key (for now, just a script name would do)
    - job status to local_scheduler
        - local scheduler parses two main keywords from the script output: FINAL_STATUS and FINAL_NOTES
        - Format: `🎯 FINAL STATUS: <status> - <optional description>`
        - Valid status values: success, fail, no_change, hanging, requires_attention
        - Format: `📝 FINAL NOTES: <descriptive text>`
        - Example: `echo "🎯 FINAL STATUS: success - Updated 15 files"`
          Planned
    - calmlib -> ask_user with multiple backend engines (telegram, ui, botspot, typer cli, input() - for jupyter and
      shell)

- wiring things together (what )
    -
        1) for local_scheduler automation jobs - just put it in the proper folder is enough (~
           /calmmage/scripts/scheduled_tasks)
    -
        2) for cronicle - I have to add a job. We can do this ...
           todo: add a 'cwd' parameter for the job (useful for some obsidian tools and running claude-experiments runner
           from its repo root)
           todo: add 'report result to cronitor' parameter
           move local_scheduler output parsing code to ...
    -
        3) 

