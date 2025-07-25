# Obsidian Auto-Sorting User Requirements

## Original Problem Statement
"basic idea of obsidian sorting 1) we'll start simple. There's a small issue with obsidian note creation approach - it
creates them either in static /Inbox dir, or 'in the same dir as current'. There's no way to program which notes get
created where depending on its contents. I have a few already established note types that I'm using all the time - let's
start with just supporting that."

## Key Requirements

### Paths and Structure
- obsidian root: `/Users/petrlavrov/work/projects/taskzilla-cm/main/root`
- tool location: `calmmage/tools` (typer CLI)
- automated job: `scripts/scheduled_jobs` using the tool's main features
- output parsing: uses `tools/local_job_runner` format with `FINAL_STATUS` and `FINAL_NOTE`

### Configuration and Detection
- "there are other page types and established templates / locations already, so I want to be able to a) auto-detect
  those from for example templates / tags / existing db fields b) configure that - e.g. desired folder structure and
  what page types should be sorted where - so I want a config.yaml and a correspoding pydantic ObsidianSorterConfig
  class"

### Future Vision - On-Disk Database
- "for my future projects, I want to start establishing the obsidian as on-filesystem database (which there are plugins
  in obsidian for supporting)"
- database utils needed in `src/` or `calmlib/` for general obsidian tooling
- "maybe for parsing db values from obsidian annotations, maybe something else.. but just keep that in mind, we will
  need our obsidian db class for other projects and tools as well"

### Output Format Clarification
- "about final status thing - my original plan was that status message will containt STATUS ONLY, and all extra info -
  like how many jobs completed - specified in the FINAL_NOTE only"
- Status format: `🎯 FINAL STATUS: <status>` (no extra description)
- Details format: `📝 FINAL NOTES: <all details here>`

## Implementation Notes
- Start simple with established note types
- Auto-detection from templates/tags/existing fields
- Configurable folder structure and sorting rules
- Future extensibility for obsidian-as-database workflows