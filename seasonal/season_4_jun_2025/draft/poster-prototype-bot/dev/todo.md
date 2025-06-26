
- [x] Queue component
  - [x] enable botspot mongodb
  - [x] enable botspot queue
  - [x] import botspot queue
  - [x] create botspot queue
  - [x] add item to botspot queue
  - [x] override botspot queue item type - pydantic whatever
    - [x] import
    - [x] inherit
    - [x] pass to constructor

- [ ] receive message from user handler
  - [ ] implementation 1: forward
  - [ ] implementation 2: manual sender - use 
  - [ ] bonus: use Mark's features - picture and title generation

- [ ] send message to channel handler

- [ ] Add title generation flow and picture generation flow
- [ ] Add formatting niceities
  - [ ] @author in the end?
  - [ ] Visual separators / highlights / pleasantries? 


## Phase 1 - save message to db

Seems done
Test? 

## Phase 2 - post message on a schedule
- post on a schedule
- 1) scheduler
- [ ] enable scheduler
- [ ] get scheduler
- [ ] ... scheduler mode - app config
- [ ] ... dev -> on period
- [ ] ... non-dev - on cron / ... regularly

## Phase 3 - reminders when queue is close to empty
