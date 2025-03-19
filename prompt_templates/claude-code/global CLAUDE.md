# What is this

## Intro

This is a global workspace of all my folders and projects.

The idea is that we're going to be working together on them

The work will be coordinated using the task tracking system in claude-task-tracking/
Please read the claude-task-tracking/CLAUDE.md for instructions

## Map

Here's a list of most important locations in this folder, try to ignore other sub-folders:

experiments - recent project ideas i came up with and trying to work on.
- Description of contents is to be finished, discover dynamically for now

projects - main actual long-term projects that I'm working on currently.
Includes my libs and personal mono repos

archive - old project that I worked on in the past. Projects are auto-moved there after idling for 3 months. I have many projects so I often get back to them.

superlinear - these are work projects. Only go there if explicitly mentioned that current project is for work.

Here are the key projects:
- botspot - a library of telegram bot components based on aiogram
- botspot template
- calmlib - a library of my personal utils, including loguru logging, heartbeat for service registry and llm calling utils based on langchain
- dev-env -
    - nix
        - aliases
        - shell scripts
    - tools
- calmmage
    - seasonal mini-projects to avoid cluttering experiments/ folder
- calmmage-private - for private projects like code vault etc. that are at risk of leaking secret info but i need the freedom.
- github templates - i have several repos for github templates, namely botspot-template, python-template and some others
- mini-templates - templates for mini-projects in experiments/ folder


# Rules from Cursor

## Tech Stack
For python, always use the following python libraries:
- pathlib
- aiogram
- pydantic
- fastapi
- pydantic_settings
- dotenv
- tqdm
- loguru
- pytest: fixture, mark, temp_dir

For react use vercel nodejs latest version (with app architecture)

For C++ and other languages no specific requirements yet - look at the project.

## Calmlib
I have a personal library - collection of utils
ALWAYS USE METHODS FROM THAT LIBRARY

## Telegram bots
A lot of my projects are telegram bots
ALWAYS USE BOTSPOT FEATURES IF POSSIBLE
SUGGEST TO

##  Work protocol
READ claude_protocol.md

Always do ONE task at a time.
Save extra mentioned tasks in todo.md file in the dev/ directory within project
Include task descriptions literally, in the EXACT words I tell you, with DIRECT QUOTES of how I explain it
Improve structure of the notes - convert to nested sub-items (but keep the phrasing of each point)

Example of conversion
Input: "Make a todo and readme in root dir, add the first command to chat with user via llm"
Output:
"""
Basic tasks
- [ ] Create a readme
- [ ] Create a todo

Features
- [ ] command to chat with user via LLM
  """


## Task Management Principles for formatting markdown files
- "Stop adding extra features!!!!"
- "For now focus on the core features only!!!"
- "No fancy-schmancy overplanning!!!"
- "Why do you write 6 lines where 1 would do??"
- "never add a header to a list of 1-2 items"
  Applied examples:
- Keep tasks minimal and focused
- One bullet point is enough if it covers the task
- Remove unnecessary headers and structure
- Only add complexity when actually needed

## Service work
Do NOT mention error handling in ANY of the todo lists, unless explicitly asked
Do NOT mention testing in any of the todo lists, unless explicitly asked
Do NOT mention docstrings in any of the todo lists, unless explicitly asked
In general try/except blocks ALWAYS PRESERVE TRACEBACK OUTPUT or THROW THE ORIGINAL ERROR
You can add A FEW extra points in SUGGESTIONS BY CLAUDE section with the  MOST IMPORTANT AND RELEVANT IMPROVEMENTS
Improvements should be guided by my github hooks: adding tests, style fixes etc.
Keep docstrings to minimum because they bloat out the code.
