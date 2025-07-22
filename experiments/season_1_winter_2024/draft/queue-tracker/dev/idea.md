# queue-tracker

a queue tracking module

idea is applying this for some places where bulk work makes sense

1) queue
2) cadence
3) items

- there should be some way to add new items to the queue
    - in bulk?
- there should be some action that auto-extracts items from the queue on specific
  cadence
    - callback
- there should be a notificaiton when queue is close to empty so it's time to fill it up

these are the three main components

and some reporting mechanism for tracking what happened

there are two possible ways to do queue tracking:

1) continuous
2) cli + job

cli + job:

- use cli to populate the queue
- use a job to run the queue


