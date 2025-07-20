- [x] move name processing to cli
  - [x] validate with ai
  - [ ] check if name is already taken on github
    - [ ] bonus: check if already have this idea somewhere


What the fuck am I trying to do?

- create a new project.
Very simple.
np name -t template

Why the fuck haven't I written this yet?!

- extra name processing - later
  - [ ] ask user for name if missing
  - [ ] validate with ai
  - [ ] check if name is already taken on github
  - [ ] bonus: check if already have this idea somewhere (use project discoverer embeddings search)
- [x] fuzzy match template name
- [x] create github repo from template
  - [x] if template is None - default
- [x] clone it locally
  - [x] to an experiments destination
  - [x] check if exists? and not empty?



So. What the fuck am I doing?

- follow along the flow of the code, entry points etc.
- delete all the garbage code?
- test the current version, make sure it works - dry run mode
- add alias
- add the 'new mini project' command as well
- search / open project / mini-project. 



----
What the fuck am I doing?
Just make the new_project command work...

what's stopping me?
it's so simple...
a) create github repo
b) clone it.
what i need:
- name
- template
- destination.

is this working? test. then add alias. 
- commit
- rerun nix

Then move on to new ideas:
- ai validate name
  - add github and openai tokens to ~/.env
- put description of the projects into ...

----
What do i want to do next?
- add mini project
- find project

find project:
1) seaches project + mini-projects destinations
   1) not found
   2) user menu - list all projects + "search more" button
2) greps file names
   1) ...
3) embedding search
   1) show results, let user choose.

add mini project:
- locate seasonal dir
  - check if time to roll
  - sanity check name
- create dir
  - put idea there
  - print & copy path / open it.

new idea:
"move to examples" - moves the file / dir to examples destination command