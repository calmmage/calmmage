# Todos

Bugfixes
- Fix query issues
  - 2025-06-05 02:30:23.765 | ERROR    | __main__:main:88 - Failed to write 2024-10-22 - Petr Lavrov's Zoom Meeting to airtable: <HttpError 400 when requesting https://www.googleapis.com/drive/v2/files?q=title+contains+%272024-10-22+-+Petr+Lavrov%27s+Zoom+Meeting.mp4%27+and+trashed%3Dfalse&maxResults=1000&alt=json returned "Invalid query". Details: "[{'message': 'Invalid query', 'domain': 'global', 'reason': 'invalid', 'location': 'q', 'locationType': 'parameter'}]">
- fix 'zoom_0.mp4' file issue: bulk rename files

Misc
- [ ] publish to my calmmage github
- [ ] move to some permanent location
  - [ ] Services? Dev_env/tools?
- [ ] publish articles on substack
  - [ ] part 1 - tech stuffaws s3 as convenient file storage 
  - [ ] 
  - [ ] full pipeline: zoom
    - why? -> data for gpt experiments
    - ai summary / transcript - calmmage_whisper_bot
    - google drive link lookup
    - airtable as convenient human-readable data storage