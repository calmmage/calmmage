ok, now let's talk about loading the messages

Here's what we need to think about:
1) loading data
2) media -> s3 (skip for now)
3) config.yaml
4) how do i test on a small batch, but meaningfully - covering all item types and cases.
5) config for each of the following types:

and by each i mean meaningful granularity

a) for daily usage purposes (minimalistic, recent only)
b) for archive / search purposes (all my content, some external content)

for recent:
- all my chats and groups up to 1-2 months
- small channels
- no bots

for archive:
- all my groups
- all my channels
- all my chats
- shortlist of the bots
----
- all small channels
- all small groups
- skip big channels and groups?
1