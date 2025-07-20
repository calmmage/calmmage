let's focus on project management tool for now

We have 3 folers in play:
a) @project_arranger 

b) lib @__init__.py 
I want to create a folder with shared project management utils
I imagine we will move here 
- destinations
- github? 
- general project discovery?
- general configs? 
-> rework config system:
each app will be able to have a nested config.yaml
with sections for shared lib classes
and sections for its own configs.

c) and a new tool. Project manager
this is the key interactive cli tool
- I want us to create a config.yaml with clear destinations listed
(name, path and description)
also maybe draft up a typer cli tool and main.py file with all the logic
Make sure to NOT include logic in the typer app - only commands with wrappers

Here's what I want feature and destination-wise:
a)
	new project
	(goes into Experiments destination)
- b)
	new mini-project
	goes into 
	- calmmage-private (if private)
	- calmmage (if public)? 
		- custom seasonal dir? 
- c)
	- new todo -> goes into project/dev/todo_date
	- asks which project to use (default - current discovered)
		- if no discovered - assume it's a mini-project?
- d)
	- new feature
	- goes into project/dev/draft/name. asks "what do you want to do"? creates idea.md
	- asks which project to use (default - current discovered)
		- if no discovered - assume it's a mini-project?
- e) other (unused) destinations ?
	- calmmage?
		- cool artifacts for publishing
	- examples
		- finished tech items go there? 
		- examples of how to build stuff
		- Simple dummy tech demos I do
	- calmlib
		- shared utils to be reuse everywhere
	- botspot
		- telegram utils