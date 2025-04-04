
## File: ./claude-code/global_claude-protocol.md

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


## File: ./claude-code/README.md

Protocols and rules for claude code

- [global_CLAUDE.md](global_CLAUDE.md) Global CLAUDE.md - general rules at ~/work
  - copy of cursor rules for coding
  - clarifications about folder structure
  - list of key projects
  - links to other systems - work protocol, task tracking etc.

- [global_claude-protocol.md](global_claude-protocol.md) claude work protocol - a two-loop work protocol
  - loop 1: dumping tasks to todo.md
  - loop 2: working on a single task in workalong.md

- [task-tracking.md](task-tracking.md) - An Obsidian-compatible file-based task tracking system for claude code


## File: ./claude-code/global_CLAUDE.md

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



## File: ./claude-code/task-tracking.md

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




## File: ./inbox/README.md

# Idea - prompt template inbox

Exports of conversations

Here I want to collect examples of successful conversations with GPT and other tools

# Todo

- [ ] Conversation with o1 about multi-component architecture of 

- [ ] Conversation about botspot / library import structure (how to find? In cursor?)

---

Some older chats with GPT

--- 

Cool grok chats? 




## File: ./inbox/brainstorming_team_name.md


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


## File: ./inbox/grok_coding_copilot_workalong.md

Hi!

I need you to work as a task management companion.

Can you remind yourself in the beginning of each message the following rules:
- rule 1: remind rules at start of each message:
- rule 2: you can think / chat with me as much as you want, but in the end there should be a "Focus" section with a specific task we'll be focusing. It should have 3 components: - project, - simple next step, - current goal (artifact / deliverable we're targeting).
- rule 3: maintain a list of projects, goals within those projects, and clear tasks mentioned by me (only by me - don't add your stuff there)

There are currently 2 tracks on my mind:

Track 1 - 146. This is number of my school and I am helping organize alumni community.
- goal 1: create a bot in telegram and wire the token in my bot
- goal 2: set up the bot to save registered users to the database
- goal 3: deploy the bot to my coolify

Track 2: my telegram bots development
- goal 1: understand / write down goals
- goal 2: set up a workspace for bot / feature development
- goal 3: start developing bots with new components: LLM utils, telethon utils, query etc.
- goal 4: add missing items to canvas



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
 


## File: ./README.md

# Overview

- [claude-code](claude-code) - most recent (2025) prompts
- [cursor](cursor) - cursor rules - 2024
 
# Bonus:

Use export.sh to merge all prompts to a single file
merged_prompts.md and copy it over to Obsidian note "Prompt Templates"


## File: ./components/think_brainstorm_categories.md

### **Category-Generation Brainstorming Prompt Template**

#### **Step 1 - Define the Purpose**
- **AI**: Asks user, "What are we generating categories for? This means what kinds of lists or collections do you want to frame?"
- **AI**: Suggests 1-2 options in a separate sentence.
    - Options: "Types of story elements, types of team name traits."
- **User**: Specifies the purpose (e.g., "Types of lists for story properties").
- **AI**: Confirms with a rephrase: "So, you want category types that could define collections of story-related ideas?"
- **User**: Agrees or adjusts.

---

#### **Step 2 - Generate Categories**
- **AI**: Generates 10 diverse category types based on the confirmed purpose, each a distinct framework for lists/collections.
    - Example for "story properties":
        1. Parts of Speech (nouns, verbs)
        2. Settings (forest, space)
        3. Themes (betrayal, hope)
        4. Character Roles (hero, trickster)
        5. Plot Actions (escape, discover)
        6. Time Periods (past, future)
        7. Tones (dark, whimsical)
        8. Objects (sword, journal)
        9. Conflicts (man vs. nature, internal)
        10. Perspectives (first-person, omniscient)
- **AI**: Stops and waits for user feedback.

---

#### **Step 3 - Apply**
- **AI**: Asks user, "Which category should I use next (e.g., to feed into a list)?"
- **AI**: Suggests 1-2 options in a separate sentence.
    - Options: "Settings, Themes."
- **User**: Picks one (e.g., "Settings").
- **AI**: Proceeds (e.g., generates a list like "Forest, Space, Ruins...").

**Key Rule**: AI generates meta-types (frameworks for lists), not items, and waits for user input at each step.


Here's a conversation example where user has to correct AI's output:
### **Sample Conversation**

**AI**: "What are we generating categories for? This means what kinds of lists or collections do you want to frame?"  
**AI**: Options: Types of story elements, types of team name traits.

**User**: "I need to create a name for our team of hacky engineers building LLM chats, apps, and tools for business and productivity. We’re serious senior devs, so I want something both powerful, majestic, and with symbolism, an interesting wordplay (but 1 / 1.5 words max). I want categories that could frame lists for this."

**AI**: "Here are 10 category types for your team name:"
1. Lion
2. Crown
3. Forge
4. Fire
5. ...

**User**: "No, those should be types of lists, not the list items themselves!"

**AI**: "Got it—so not specific examples like ‘Lion,’ but frameworks like ‘Symbols’ or ‘Actions’ that could hold lists? Is this what you mean?"

**User**: "Yes, exactly."

**AI**: "Here’s a corrected list:"
1. Qualities (strength, wisdom)
2. Symbols (lion, crown)
3. Actions (forge, rise)
...

**AI**: "Which category should I use next (e.g., to feed into a list)?"  
**AI**: Options: Symbols, Actions.

**User**: "Symbols."

**AI**: "Here’s a list for ‘Symbols’: Lion, Crown, Shield, Flame, Tower, Star, Wolf, Spear, Tree, Vortex."




## File: ./components/code_clarify-before-coding.md

Explain the full approach you’d take to implement this. Just tell, don’t code.


## File: ./components/code_propose-ideas.md

When interacting with user
- First ask them a question
- Then suggest 1 or 2 ideas IN A SEPARATE SENTENCE.


## File: ./components/think_brainstorm_lists.md

### **List 1, List 2 Brainstorming Prompt Template**  
1. **Define the Goal**: State what you’re brainstorming (e.g., "Generate a novel topic").  

2. **List 1 - First Element Type**: Choose a type (e.g., nouns) and generate 10 diverse, independent options.  
   - Example Type: Nouns - "Storm, Clock, Raven..."  

3. **STOP**: Do not proceed until List 1 is generated and reviewed in a separate response.  

4. **List 2 - Second Element Type**: Choose a complementary type (e.g., verbs) and generate 10 diverse, independent options, without referencing List 1.  
   - Example Type: Verbs - "Ruminates, Explodes, Drifts..."  

5. **STOP**: Do not proceed until List 2 is generated and reviewed in a separate response.  

6. **Sample & Combine**: In a new response, randomly pair one item from List 1 and one from List 2 (e.g., roll 1-10 for each). No pre-matching allowed.  
   - Example: "Clock Drifts" → A seed, not curated for fit.  

**Key Rule**: Lists 1 and 2 must be generated blindly and separately—AI cannot combine or align them in the same response.


## File: ./components/task_tracking_markdown-formatting.md

Rules for task tracking and markdown formatting:
- never add a header to a list of 1-2 items

- Keep tasks minimal and focused
- One bullet point is enough if it covers the task
- Remove unnecessary headers and structure
- Only add complexity when actually needed


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

There are currently 3 groups of prompts here
- Code
- Think
  - [think_brainstorm_lists.md](think_brainstorm_lists.md) - a brainstorming technique to activate ai's real creative potential. Find a novel idea by generating independent list 1 and list 2 of combineable items and then picking a random pair from them.
  - [think_brainstorm_categories.md](think_brainstorm_categories.md) - meta-prompt to help come up with qualitative categories for lists from previous technique
  - [think_akinator.md](think_akinator.md) - a hack to use the power of akinator concept to make AI interview you and get an information / decision you have.
- Task tracking
  - [task_tracking-save-direct-quotes.md](task_tracking_save-direct-quotes) - I notice that cursor's / claude's task logging ability is horrible. It bloats task lists, worsens the language, corrupts meaning. Writing down direct quotes solves that somewhat.


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



## File: ./components/task_tracking_save-direct-quotes.md

Save extra mentioned tasks in todo.md file in the same directory
Include task descriptions literally, in the EXACT words I tell you, with DIRECT QUOTES


## File: ./components/code_one-task-at-a-time.md

- Always do ONE task at a time.
- We are tracking our work in todo.md and in workalong.md
- We only work on ONE FEATURE AT A TIME - e.g. ONE ITEM, ONE TASK from todo.md


## File: ./fewshot-examples/README.md



