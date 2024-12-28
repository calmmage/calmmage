# TODO
- [x] 1. Save telethon user session to somewhere persistently 
- [ ] 2. add a new botspot component for telethon client
- [x] 3. Modify ask_user to handle message cleanup
- [x] 4. Add proper session initialization and verification
- [ ] 5. Save telethon session to a database as a conn str
- [ ] 6. Add ALL the utils for working with deps items.
  - [ ] get_bot
  - [ ] get_scheduler
  - [ ] get_telethon_client
  - [ ] get_mongo / get_db ?
  - [ ] something else? what's there? pyrogram? 
  - [ ] bot info? 
  - [ ] ... all the other components that store stuff in deps. Notion client. GPT client / token. 
  - [ ] other calmmage services - notification service, service registry, ... 

Suggestions by Claude:
- [ ] 1. Add similar callback mechanism for handling verification codes
- [ ] 2. Add error handling for invalid phone numbers
- [ ] 3. Add support for bot tokens in the same callback system
- [ ] 4. Add method to list all active sessions
- [ ] 5. Add command to disconnect specific session
