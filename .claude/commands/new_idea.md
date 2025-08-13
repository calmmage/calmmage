# New Idea Command

Write the essence of an idea immediately to a file.
If the idea is long, use Secretary instruction to format it properly.

## Determining where to save:

### For coding ideas:
1. Check if there's an existing project repo at ~/work/projects/
    - If yes and it's a long note → save to `{repo}/dev/notes/{date}_{idea_name}.md`
    - If yes and it's short todos → append to `{repo}/dev/todo.md`
2. If this is a new idea without existing project:
    - Create in `~/calmmage/experiments/season_{latest}/_notes/projects/{idea_name}/`
3. If these are quick tasks or short todos:
    - Consider creating in obsidian quick tasks folder for easy linking

### For non-coding ideas:
1. Check current and last weekly notes for existing related projects
    - If found → add to that project page or create linked note
2. If this is completely new topic:
    - Create new page in `~/calmmage/obsidian/Inbox/{idea_name}.md`

## After saving:
Add link to central navigation map:
- Coding → Add to `~/calmmage/experiments/season_5_jul_2025/coding_map.md` under today's date
- Non-coding → Add to current weekly note under today's date header
- Use [[note_name]] for Obsidian notes, /full/path for external files

Check maps first to avoid duplication.

Wait for user to tell you the idea first.