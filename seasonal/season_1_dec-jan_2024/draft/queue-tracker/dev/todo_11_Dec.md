Plans for next steps:
- [ ] make sure custom callbacks work correctly - hybrid init - load data from storage but init queues in runtime with proper callbacks
- [ ] extras - custom extensions for default queue tracker to make it usable in real life out of the box
	- telegram notifs / messages with the bot
- [ ] save info about past items

- wire the service together so that it works.. 
  - runner that launches the job from time to time..
  - ~/.env with all necessary details:
   - telegram bot token
   - personal user chat id to use
   etc
  - persistent data storage path? 


Bonus
- [ ] add support for the database