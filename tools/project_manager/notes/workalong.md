# Project Manager Implementation Checklist

## Progress Tracking
- [x] Initial Project Setup
  - [x] Basic file structure
  - [x] Core configuration files
  - [x] Destination concept defined

- [ ] Code Migration from Project Arranger
  - [x] Move Destination concept to shared utils
  - [x] Create central destinations registry
  - [x] Create shared destinations config
  - [ ] Port GitHub integration utils
  - [ ] Port project discovery logic
  - [ ] Adapt project sorting algorithms
  - [ ] Update project arranger to use shared code

## Core Scenarios
- [ ] New Project
  - [x] Config Integration
    - [x] Create shared destinations config
    - [x] Create destinations registry
    - [x] Create project manager config
  - [ ] Project Creation
  - [ ] Name Processing
    - [ ] Prompt if no name provided implement prompt_project_name()
    - [ ]  Validate with AI (query_gpt) implement validate_name_with_ai()
    - [ ] Check GitHub conflicts implement check_github_conflicts()
    - [ ] Generate concise name if needed implement generate_name_from_description()
  - [ ] Template Selection
    - [ ] Fuzzy-match template name
    - [ ] Use default if none provided

  - [ ] GitHub Integration
    - [ ] Create GitHub repo from template
    - [ ] Clone to experiments destination
    - [ ] Copy path to clipboard implement copy_path_to_clipboard()
    - [ ] Print confirmation

- [ ] New Mini Project
  - [ ] init: list all points from the user scenario file
- [ ] New Todo
  - [ ] init: list all points from the user scenario file
- [ ] New Feature
  - [ ] init: list all points from the user scenario file
- [ ] Destinations:
  - [ ] list all points from the user scenario file

## Features
- [ ] GitHub Template Name Parsing and Integration
  - [ ] init: list all points from the user scenario file
- [ ] Nix Command Aliases
  - [ ] init: list all points from the user scenario file
- [ ] Project Auto-detection
  - [ ] init: list all points from the user scenario file
- [ ] Timed Confirmation Defaults
  - [ ] init: list all points from the user scenario file
- [ ] Project Search
  - [ ] init: list all points from the user scenario file

## Sanity Checks & Auto-jobs
- [ ] Job Timing System
  - [ ] init: list all points from the user scenario file
- [ ] Project Discovery Cache
  - [ ] init: list all points from the user scenario file
- [ ] Seasonal Folder Management
  - [ ] init: list all points from the user scenario file
