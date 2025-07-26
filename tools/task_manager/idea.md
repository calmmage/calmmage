# Task Management Tool

Look at experiments / season 4 / notes / outstanding items and other ideas -> make a list of outstanding projects ideas -> then go read the code and evaluate for each project / goal / feature / task - if it is properly implemented already (for most it will be no, but for some / yes). Then, let's start working on a new tool for the tasks / outstanding items management. Let's start simple: 1) write a fuzzy parser script that builds a list of items and their status based on 
(I want the logic to look something like that:
- new item

-[x] done item

Header
- a cluster
  - of items and subitems
  - subitems 2
)

So, generally first split by double newlines
(Or sometimes I use --- to emphasize a strong split)
Then look for top level - single dash item points / or other markdown lists.

Attach sub-items to the item.


The main trick here is that in our memory, I want to maintain a backward mapping from a (item) to (it's place in text) - so that we could know about all items but also work with them somewhat meaningfully.
Maybe that will be a basis for MCP or something.

In general, I just want a natural item / task editing flow that works based on common sense assumptions, not explicit metadata annotations (because they clutter the space on screen and are usually could be intuitively derived). Also, save the project description in the idea.md in the new tool dir (use exact text I wrote above).

So, have a config.yaml specifying "item source locations" (for now, just outstanding_items.md - existing in _notes dir). Then source the items from that file. And for now - just show the parsed items and info about them (include sub-items as parts of the item they are children to, not as separate items)