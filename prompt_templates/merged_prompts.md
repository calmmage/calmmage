
## File: ./claude-code/README.md

Protocols and rules for claude code

- Global CLAUDE.md - general rules at ~/work

- claude work protocol - 



## File: ./claude-code/task tracking.md

# AI Task Tracker Instructions

Hey! I’m here to help you dump tasks and work on them with two simple loops. We’ve got `sessions.md` as the main index, `projects/` for long-term task lists, and `notes/` for session-specific stuff. Here’s how I’ll roll:

---

## Setup (One-Time)
- Check if `task-tracker/` exists. If not, create it.
- Inside `task-tracker/`:
  - If `sessions.md` isn’t there, make it with `# Task Tracker Sessions`.
  - If `projects/` or `notes/` folders are missing, create them (empty).

---

## Loop 1: Dumping Tasks from Your Brain
This is you unloading ideas—I’ll keep it organized.

### Step 1: Pick a Project
- Open `sessions.md`.
- Say: “Hey, what project are you thinking about today? Could be ‘People Bot’ or something fresh—just toss me a name.”
- When you reply (e.g., “People Bot”), hold off on updating `sessions.md`—we’ll link a session note next.
- Check `projects/`. If there’s no `People Bot.md`, say: “I don’t see a [[People Bot]] project yet. Want me to make one? If so, what’s the goal—like ‘Build an AI to analyze profiles’?”
  - If you say yes and give a goal (e.g., “Build an AI to analyze profiles”), create `projects/People Bot.md` with:
    ```markdown
    # People Bot

    ## Goal
    Build an AI to analyze profiles

    ## Tasks
    ```
- Move to Step 2.

### Step 2: Add Task to Latest Note
- Say: “What task do you want to dump for [[People Bot]]? Like ‘Code the profile scanner’ or whatever’s in your head.”
- Check `notes/` for the latest note tied to “People Bot” (e.g., `11 Mar 2025 - People Bot Work.md`).
  - If there’s no note from today (e.g., it’s `13 Mar 2025` and the latest is older), create a new one:
    - Name it `13 Mar 2025 - People Bot Work.md`.
    - Add:
      ```markdown
      # 13 Mar 2025 - People Bot Work

      ## Tasks
      ```
    - Update `sessions.md` at the top: `- [[13 Mar 2025 - People Bot Work]]`.
  - If there’s a note from today (e.g., `13 Mar 2025 - People Bot Work.md`), use that.
- When you reply (e.g., “Code the profile scanner”), add it to `## Tasks` in the note:
  ```markdown
  ## Tasks
  - [ ] Code the profile scanner
  ```

### Step 3: (Optional) Cleanup Old Task Lists
- Say: “Want to tidy up old [[People Bot]] tasks? I can check past notes and the project file. Say ‘yes’ if you’re up for it.”
- If you say “yes”:
    - Scan `notes/` for all “People Bot” notes (e.g., `11 Mar 2025 - People Bot Work.md`) and `projects/People Bot.md`.
    - Show you a list of tasks from all files (e.g., “Here’s what I found: [ ] Code scanner, [x] Research profiles”).
    - Ask: “Which ones are done? Any to merge or update?”
    - Update files based on your input (e.g., mark `[x]` in `People Bot.md` or move unfinished tasks there).

### Step 4: Start Work
- Say: “Ready to jump in? Pick a task when you’re set—Loop 2’s up next!”

---

## Loop 2: Working on Tasks
Now we’re doing stuff together—I’m your sidekick.

### Step 1: Pick a Task
- Say: “What task are we tackling? Grab one from a note or [[People Bot]]—like ‘Code the profile scanner’.”
- When you reply (e.g., “Code the profile scanner”), find it in a note (e.g., `13 Mar 2025 - People Bot Work.md`) or `People Bot.md`. If it’s not there, add it to the latest note’s `## Tasks`.

### Step 2: Go Do It (Together)
- Say: “Sweet, let’s hit it! How can I help with ‘Code the profile scanner’? Need ideas, a breakdown, or something else?”
- Wait for your lead—e.g., if you say “Break it down,” I’ll ask: “What steps do you see? I’ll jot ‘em down.”
- Keep chatting as you work, helping however you need (no inventing—just prompting and recording).

### Step 3: Mark Task as Done
- When you say “done” or finish, find the task (e.g., in `13 Mar 2025 - People Bot Work.md`).
- Change it to `[x]` (e.g., `- [x] Code the profile scanner`).
- Ask: “Want to sync this to [[People Bot]]? Say ‘yes’ if so.”
    - If yes, update `People Bot.md`’s `## Tasks` with `- [x] Code the profile scanner (see [[13 Mar 2025 - People Bot Work]])`.
- Say: “Nice one! What’s next—another task or back to dumping?”




## File: ./claude-code/global claude protocol.md

If you're an AI assistant and user explicitly told you to read this file with these instructions, from now on you have to start EVERY message with the following rules as mantra:

- We are tracking our work in todo.md and in workalong.md
- We only work on ONE FEATURE AT A TIME - e.g. ONE ITEM, ONE TASK from todo.md
- Before jumping to action with implementing the feature - ASK USER WHAT THEY WANT TO SEE DONE
    - Suggest 1 or 2 ideas IN A SEPARATE SENTENCE.
- The procotol is as follows:
    - 1) Look at todo.md, select ONE task to work on (suggest to user 1 main candidate and 1-2 alternatives - and let them confirm)
    - 2) write down the selected task to workalong.md
    - 3) work on a task together with user and write user notes / sub-tasks in the workalong.md
    - 4) After task is finished - archive the existing workalong.md and start a new one. Update todo.md - mark task as done and add relevant notes / new todos from workalong if necessary.
    - 5) Repeat from start.


## File: ./claude-code/global CLAUDE.md

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



## File: ./inbox/README.md

# Idea - prompt template inbox

Here I want to collect examples of successful conversatinos 

# Todo

- [ ] Conversation with o1 about multi-component architecture of 

- [ ] Conversation about botspot / library import structure (how to find? In cursor?)

---

Some older chats with GPT

--- 

Cool grok chats? 




## File: ./inbox/brainstorming_team_name.md




## File: ./cursor/README.md

prompt templates for cursor


## File: ./cursor/rules.md

# Tech Stack
For python always use the following python libraries:
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

# Work protocol
Always do ONE task at a time.
Save extra mentioned tasks in todo.md file in the same directory
Include task descriptions literally, in the EXACT words I tell you, with DIRECT QUOTES
Improve structure of the notes - convert to nested sub-items (but keep the phrasing of each point)

# Task Management Principles for formatting markdown files
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

# Service work
Do NOT mention error handling in ANY of the todo lists, unless explicitly asked
Do NOT mention testing in any of the todo lists, unless explicitly asked
Do NOT mention docstrings in any of the todo lists, unless explicitly asked
In general try/except blocks ALWAYS PRESERVE TRACEBACK OUTPUT or THROW THE ORIGINAL ERROR
 


## File: ./components/think_brainstorming.md


```
I need to create a name for our team of hacky engineers building LLM chats, apps and tools for business and productivity,
we're serious senior devs, so i want something both powerful, magestic and with symbolism, an interesting wordplay (but 1 / 1.5 words at max)

let's try a fancy brainstorming technique i invented:

INDEPENDETLY generate 10 words of type 1 and 10 words of type 2
(for example type 1 is adjective and type 2 is noun
or type 1 is meaning and type 2 is wordplay style)

now i want you to generate WHAT TYPE 1, TYPE 2, TYPE 3 can be 

```

```
this is not what i wanted you to do. Instead i want you to generate me at least 10 diverse options - just a list, be ultra concise, max 1-2 word comments

Certainly! Here’s a concise list of options for both Type 1 (Qualities/Characteristics) and Type 2 (Objects/Concepts), each with...

not what can be IN type 1. instead what can BE type 1
```
1.	Emotion - Capturing the emotional essence or impact of your work.
2.	Value - Fundamental principles or ethics guiding the team.
3.	Intensity - Reflecting the level of passion or energy.
4.	Innovation Level - Expressing the degree of creativity and innovation.
5.	Skill Level - Highlighting professional expertise or mastery.
6.	Impact - Denoting the magnitude or effect of your work.
7.	Speed - Symbolizing quickness, efficiency, or dynamism.
8.	Reliability - Conveying trustworthiness or dependability.
9.	Flexibility - Indicating adaptability or versatility.
10.	Vision - Representing foresight, ambition, or goals.

```
ok, now generate a random number
The random number generated is 4.

now, take an item from the list with that number. and generate 10 options what could the word of that type be


mm. those are not of type "innovation level". Instead, those are THE SAME INNOVATION LEVEL.

hm. i still don't see nothing original or simple.
- where is option 'no innovation'?!
- where is something ultra original? e.g. 'negative innovaion' e.g. stabilization? Or reduction of information space?

```


## File: ./components/code_python-personal-libs.md

# todo: add more information and examples

botspot

calmlib

---

botspot-template

botspot-mini-template

---




## File: ./components/README.md

Idea:

Add here individual isolated prompt components that can be combined / utilized ad hoc


## File: ./components/think_akinator.md

With a series of akinator-like questions, find {target}

Example:

With a series of akinator-like questions, find something interesting and complex to tell me


## File: ./components/code_python-modern-libs.md

# Tech Stack
For python always use the following python libraries:
- pathlib
- aiogram
- pydantic
- pydantic_settings
- fastapi
- dotenv
- tqdm
- loguru
- pytest: fixture, mark, temp_dir, conftest



## File: ./components/code_one-task-at-a-time.md




## File: ./fewshot-examples/README.md



