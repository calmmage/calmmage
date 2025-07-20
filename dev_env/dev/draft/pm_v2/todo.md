# Project Management System Roadmap

THIS PLAN SHOULD NOT BE CHANGED BY AI, ONLY EDITED
Allowed actions:
- mark items as checked 
- adding specific sub-items with clear actions
Prohibited actions:
- adding new sections
- adding long abstract explanations or words

## 0. Ideas from Petr
### a) Four things:
- shared lib / code
- project 1: project management. 
role: cli tools for project management. Actions
- project 2: project discovery
role: Running interactively, research. Information extraction
- project 3: project organization
role: Automatic scripts, configured with yaml rules.

### b) old project links
From dev-env:
- tools/project_arrangement/ (all files)
- tools/count_repos/repo_stats.py
From dev-env-experiments:
- old_dev_env/tools/project_manager.py
- old_dev_env/core/dev_env.py
  - project structure (project management - cli)
  - monthly job (project organization - scripts)
- dev/draft/mvp/project_manager.py
- dev/examples/clone_all_projects/clone_all_projects.py
- dev_env/core/repo_discovery.py

## Initial plan

Sort out past projects - map into new

project_arrangement -> continue. project organization
repo_stats
old_project_manager -> 
dev_env -> 




## 1. Save References
- [x] Create branch `dev-pm-v2`
  - [ ] Add `roadmap.md` with file links
  - [ ] Add `references.md` with code snippets
- [ ] Create `dev/draft/project_system_v2`
  - [ ] Symlink relevant files from old code
  - [ ] Copy key code snippets

## 2. Project Core Library
- [ ] Project class (from ProjectArranger)
  - [ ] Basic attributes
  - [ ] Metadata handling
  - [ ] GitHub integration
- [ ] Settings (from repo_discovery.py Settings)
  - [ ] Project paths
  - [ ] GitHub config
  - [ ] Cache settings
- [ ] Cache system (from RepoCache)
  - [ ] Project cache
  - [ ] Metadata cache
  - [ ] GitHub cache

## 3. Project Discovery Service
- [ ] Local scanner (from discover_local_projects)
  - [ ] Path scanning
  - [ ] Git repo detection
  - [ ] Metadata extraction
- [ ] GitHub scanner (from clone_all_projects)
  - [ ] Repo listing
  - [ ] Team filtering
  - [ ] Sync status
- [ ] Cache manager (from RepoCache)
  - [ ] Load/save
  - [ ] TTL handling
  - [ ] Cache invalidation

## 4. Project Organization Service
- [ ] Categorizer (from ProjectArranger._sort_*)
  - [ ] Auto rules
  - [ ] Manual rules
  - [ ] Tag system
- [ ] Status tracker
  - [ ] Activity metrics
  - [ ] Size tracking
  - [ ] Git stats
- [ ] Cleanup recommendations
  - [ ] Archive candidates
  - [ ] Delete candidates
  - [ ] Merge candidates

## 5. Project CLI
- [ ] New project (from project_manager.py)
  - [ ] Mini project
  - [ ] Full project
  - [ ] Template handling
- [ ] Convert project
  - [ ] Mini to full
  - [ ] Move to experiments
- [ ] Find/List projects
  - [ ] Search by name
  - [ ] Filter by status
  - [ ] Group by category
- [ ] Organize projects
  - [ ] Run cleanup
  - [ ] Apply recommendations
  - [ ] Batch operations

## 6. Shell Aliases
using `add_tool` command instructions from shell
- [ ] Project Creation
  - [ ] `np` (new project) with flags:
    - mini: local experiment
    - full: GitHub project
    
- [ ] Project Discovery
  - [ ] `fp` (find project) - search by name
  - [ ] `lp` (list projects) - show active/recent
  
- [ ] Project Organization
  - [ ] `sp` (show project) - status & recommendations
  - [ ] `op` (organize projects) - cleanup workspace