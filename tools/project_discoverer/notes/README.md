# Project Inspector

1) well this actually more relates to another tool I had in mind - interactive research tool
And to have related components in the shared lib - for reuse.
2) here, in the context of project manager the goal is twofold:
- for new project and miniproject creation - avoid duplicates or include references to old projects - for useful context
- for todos and features - discover to which project to add them (/suggest) quickly

Let's talk about discovery / ingestion as well
- i already have basic cached globbing for git repo detection
- there will need to be some way to discover past projects from folder tree
- but that's way too advanced. A more direct way is just to have conflict.yaml with direct paths 

then, when tool is launched - 
1) if files are not in valid destinations - grab the old files from ... their location and ingest into a proper place
2) save metadata somewhere handy (in a destination explicitly or just in a folder structure) 
3) so in the future if we have paths in config.yaml that are missing - we could check if they are already ingested
- I want to write / generate the project / idea description 

For quick lookup, during daily operations:
- i want a combo of plain text search + embedding search on my projects / mini-projects / drafts from the past
- I want background detection and suggestion under the hood when i'm creating stuff - sanity checking me

Separate above into sections:
- for project manager
- for project discovery
- old todo / examples discovery (no content yet)