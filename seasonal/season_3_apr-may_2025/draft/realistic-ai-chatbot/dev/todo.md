- [x] basic chat
- [x] media support
- [ ] add main feature: splitting the ai response into parts
    - [ ] add (randomized?) delay between messages
    - [ ] add custom formatting instructions for system prompt - e.g. split formatting mode

- a - just split in the end 
- b - streaming 
- c - streaming + send as you go
- [x] d - 'reply safe / answer safe'

- [ ] add model selection command / menu
  - [x] use model for querying
  - [ ] add a command - model picker (with ask_user_choice util)
- [ ] add history - accumulate messages for user
  - [ ] improve - rotate out extra context on timeout
  - [ ] option 1: in-memory
  - [ ] option 2: mongodb
  - [ ] option 3:
  - [ ] bonus: add and use mongodb vector storage for RAG


- [ ] split messages simple
  - [ ] Just wire it - so that it at least works at all.. (None mode)
- [ ] split messages streaming
  - [ ] Just wire it - so that it at least works at all.. (None mode
- [ ] delay messages (e.g. send_out_messages) feature
  - [ ] Just wire it - so that it at least works at all.. (None mode

Next main improvement idea:
- support the interaction where user writes to the chatbot also in multiple messages - potentially writing in the middle of next message without waiting for response to finish...
- [ ] idea 1: maintain a shared message -> response (chat) history and use it across processes
- [ ] idea 2: stop responding to a previous message (interrupt) when new one arrives
- [ ] automatically activate 'reply' mode when this happens - otherwise, use 'answer' by default


# Settings
- [ ] Implement a web-app settings with slider (e.g. for 'delay between messages' variable
- [ ] Implement a basic 'settings' component for botspot, that gets a list of variables, setters, and gives user a nice menu / ui for setting them all (e.g. commands, ask_user_choice etc.)