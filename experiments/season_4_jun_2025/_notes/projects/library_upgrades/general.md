# Idea

This is a project about long overdue refactorings and library upgrades
There's a bunch of features I want to add / move around in my libraries

- Idea 1: refactor calmlib
    - Idea 2: we will remove a lot of legacy components, but then let's capture some of the featured libraries and
      imports
    - let's save tech_stack.md somewhere in a reasonable and prominent location (maybe in dev/ or docs/ or somewhere
      else. But we need to make sure there's no other / old / irrelevant garbage in that dir then)
    - This will be useful for another tool I have in mind which will help me to update CLAUDE.md, .gemini and
      .cursorrules

- Idea 3: add new basic components inspired by what was there before
    - Logging
- Idea 4: move over telegram_downloader - make it a tool, but make the core functionality a shared lib within calmlib
- Idea 5: add new 'ask_user' component that would allow me to universally ask for external user feedback within any of
  my tools or utils using the appropriate channel
    - I've dumped notes about this somewhere already - ask me to find it, before starting work. (reference this comment)
- Idea 6: Move stuff from experiments to main calmlib
    - aws s3
    - airtable
    - zoom?
    - gdrive?
- Idea 7: env discoverer
    - a simple tool that finds the necessary env variables across my system (basically just use ~/.env if a key is not
      present)
    - Interactively (using ask_user) ask user for a key if such key is missing - and put it to the appropriate place
    - This will work nicely in tandem with another planned setup tool - env_setup_script. I think I also want some cli
      tool 'setup_env' or something that i can then alias like 'setup zoom' or 'setup s3' and it will walk me through
      adding / enabling necessary components.. Specific to my env arrangement.
    - For this env_discoverer tool let's also add a security / backup / privacy mode which bascially doesn't search
      anything (and actually kills unsecure env variables if it finds them in ~/.env) - for my eventual transition to a
      proper secure mode of operations (because obviously storing global env keys is a no-go.. )

