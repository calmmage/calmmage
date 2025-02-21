# download-telegram-messages

What I want to do here is:

- donwload all telegram messages from my account
    - personal chats history limit (default - forever)
    - group chats config
    - channels config
- make a yaml config for configuring my stuff
- add support for multimedia
    - use s3 storage?

Bonus features:

- make a telegram bot
    - make it a botspot bot
- add a feature for this telegram bot to search / chat / process my messages (option 1:
  just chat with all recent (personal) messages. option 2: use embeddings to search
  relevant snippets)
- mongo db support
    - messages collection
    - user config (e.g. telegram api keys etc.)
- authenticate to pyrogram via telegram bot
