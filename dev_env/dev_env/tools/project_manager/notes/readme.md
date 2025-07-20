# Project Manager User Scenarios

## Core Scenarios
- [New Project](./scenarios/new_project.md)
- [New Mini Project](./scenarios/new_mini_project.md)
- [New Todo](./scenarios/new_todo.md)
- [New Feature](./scenarios/new_feature.md)
- [Destinations overview](./features/destinations.md)

## Features
- [GitHub Template Name Parsing and Integration](./features/github_template.md)
- [Nix Command Aliases](./features/nix_aliases.md)
- [Project Auto-detection](./features/project_autodetect.md)
- [Timed Confirmation Defaults](./features/timed_confirmation.md)

## Sanity Checks & Auto-jobs
- [Job Timing System](./features/job_timing.md)
- [Project Discovery Cache](./features/project_discovery.md)
- [Seasonal Folder Management](./features/seasonal_folders.md)

## Navigation & Deduplication -> project inspector
(../../project_inspector/notes/README.md)
- [Project Search](./features/project_search.md)
- [Mini-Project Search](./features/mini_project_search.md)
- [Todo Search](./features/todo_search.md)
- [Feature Search](./features/feature_search.md)

## Bonus Jobs
- [Template Auto-update](./jobs/template_update.md)
- [Seasonal Folder Auto-update](./jobs/seasonal_update.md)
- [Project Discovery](./jobs/project_discovery.md)
- [Legacy Migration](./jobs/legacy_migration.md)

# Raw

let's actually start collecting specific user scenarios we want to support
We'll start with the following docs I have in mind

User scenario should be in the format of steps:
User calls new_project command from console
-> ... 'new_project' or 'new_project name' or 'new_project name -t template_name'
-> ...

Suggest a good designation for branching scenarios here.
mermaid?

1) write the instructions above in notes/readme.md @readme.md 

scenarios i have in mind:
4 from before
- new proj
- new mini proj
- new task / todo
- new feature for a proj

features I want to support
- fancy template name parsing
- creating from github template and cloning locally
- aliases for all main commands via nix
- auto-determine which project we're talking about if not specified. 
- timed-out-confirmation with defaults

Navigation / deduplication
- searching projects -> copy abs path, auto-check if duplicate
- search mini-projects -> copy abs path, auto-check if duplicate 
- search in project todos, check if dup
- search features, check if dup

Sanity checks, auto-jobs
Idea: make a tool that 1) has a folder at ~/.smth 2) saves there times when it ran a job 3) can check and NOT run a job if last run is within (delta)
- caching and project discovery
- seasonal folder rename / roll

bonus, jobs
- auto-updating of templates (using fix_repo tool)
- auto-updating of seasonal folders (creating new when too much projects, renaming based on time span)
- discovery and caching of all projects
- bonus bonus - dicsovery and caching of 1) mini-projects, 2) todos 3) features / examples / drafts 4) migration / ingestion of old cool projects and ideas

For each of the above create a separate md doc
