
# New

- [x] improve main auto sorting
- [x] apply groups. sort
  - if same group - skip
  - if not cloned - clone
  - if ignore - move to 'to_remove'
  - all the rest - move
  - first - make a list of actions - and verify
# important
- [ ] add periodic jobs
- [ ] add mini-project concept
- [ ] add alias or something? Regular job?
# boost
- [x] if no changes - all skip - don't ask confirmation
- [ ] idea: simple local cache with rocksdb? to make things faster
- [ ] move run.py to cli.py

# Old
Main things I'm trying to do:
- display relevant info about projects
  - [x] add github tech - old clone_all_projects script
  - [x] github name, if different
  - [x] github org, if not personal
  - [x] date, if interesting
- improve project sorting algorithms / rules
  - based on date
  - hardcode more rules
- do actual sorting (move and clone projects)
  - arrive at a state where I'm happy with the result (key projects not removed)
  - move dirs around (with confirmation?)

something else?
- (auto)-commit code before moving stuff around.
- merge with clone_all_projects script

# Tools
- tool to compare local and github projects
- tool to clone all projects from github

# Focus
- 1) Now, that we added github client
  - make github project lists
  - merge / compare with local

- [ ] Get project metadata for github-only projects as well
  - create a separate Github project class?
- [x] Show project owner at least
- [x] add config for which github orgs to use. Debug / info about the ones not used.

- [ ] load_github_projects in the project arranger, not in typer app..
- [x] sort by org, before date.
Bonus
- [ ] handle "project present twice" corner case

- 2) improve project sorting algos
- 3) Start thinking about
  - new project creation 
  - miniproject
  - project location abstraction? (Destination class?)

Refactoings
- [ ] return the reason for group selection together with ... group
- [ ] change everything to return instance of Group
- [ ] Add a new 'destination' class or something
  - dict? group_name -> dir? configurable somehow? 
- [ ] Resolve python config warnings about types of fields (config.py, BaseSettings)

- [ ] Add a flag to show 1) date or 2) reason for group selection 
  - in brackets to the right of the project
- [ ] Sort projects by recency within groups.

- [ ] add a simple clone_all_projects script based on our tool
  - specify target root? create main and secondary groups folders in there?
  - make sure to just add the ability to clone repos to our script
- make things work faster
  - [ ] add cache or something - like what ]

Legacy
- 
-----

 - [ ] Old projects go into projects, not experiments, if edited recently
   - Experiments: Added: + [    16,400] forwarder-bot    (Edited 6 days ago, Created 8 months ago)



- add new tech - github info
  - [ ] merge with clone_all_projects script
  - [x] init github client
  - [x] see github remote for the repo
  - [x] if remote project name 
  - [x] see all remote projects
    - [x] configure which remote sources (orgs) to use
  - [x] merge remote and local lists 
    - [ ] handle "a project that is cloned several times" scenario
    - [ ] handle "a project that is cloned under a different name" scenario. Ask user:
      - rename local
      - rename remote? 
      - keep as is

Plan:




- [ ] handle 'clone from start' scenario
  - [ ] use old 'clone_all_projects' script - deduplicate and reuse
    - copy code to project arranger
    - use in the script to reproduce behavior
    - merge old and new code to remove duplicate functionality

- [ ] handle 'already cloned, now sort'
  - [ ] non-dry-run
    -  [ ] move projects
    -  [ ] projects that are to be deleted (ignored but present on disk) - move to 'to_remove' folder
  - debug / research tools
    - a) view project sizes
      - notice big ignored projects
      - notice small non-ignored projects (except recent) 
    - b) view project dates


- [ ] Better project sorting
  - [ ] Anomaly decetion - analysis / research tools
  - [ ] make it so secondary projects can't be ignored (if ignored -> move to archive instead?)
    - or not? 1) templates - yes 2) cool - no (will distract me?)
  - [ ] automatic sorting: 
    - sticky groups (don't change groups for no reason)
      - if recently modified -> stays in 'actual' even if not hardcoded
    - by date -> 
      - if created this month - stays in experiments
      - if before
        - if modified this month -> actual
        - if before
          - if big -> archive
          - if not -> ignore (to_remove)
  - [ ] auto-commit? warn? Block? 
    - [ ] 1) before removing
    - [ ] 2) before moving? 


- [ ] ai features
  - ai categorization (to which primary / secondary to move?)
  - ai summary of the project
  - ai ... 








# Done
- [x] fix 'ignore' and 'ignored' issue
- [ ] handle 'already cloned, now sort'
  - [x] determine current group based on path
  - [x] add two view options:
    - show only changes
    - show all

- [x] primary and secondary groups - sort, print
- [x] print group size (in brackets?)
  - [x] make cached?
  - [x] make cached all properties - last modified


- [x] print project date info
  - if edited > 1 month ago -> print that
  - if edited recently but created long ago -> print both
  - if edited recently and created recently -> print only when edited