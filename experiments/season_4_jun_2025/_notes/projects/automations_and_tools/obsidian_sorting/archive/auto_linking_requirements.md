# Auto-Linking Requirements - Verbatim User Requirements

## Core Logic
"Go over all of the files (not just daily files) and skip the daily files."

## Date-Based Linking Strategy

### Multiple Date Sources
"Let's not only look at the edit date but also look at the creation date. Let's make this logic somewhat configurable."

### Date Difference Logic
"If the edit date and the creation date are very far apart (more than 3 days), then if it's between 3 days and 20 days,
we do not do anything or throw a warning or ask a separate confirmation. Maybe for each file or for all of the files
together. If it's above 20 days, then I don't know, maybe ask a confirmation for each file (below 20 days ask for all
files together, above 20 days ask for each file individually)."

### Confirmation Strategy
- **0-3 days difference**: Auto-proceed
- **3-20 days difference**: Ask confirmation for all files together
- **Above 20 days difference**: Ask confirmation for each file individually
- **Add flag to auto-cancel/decline**: "Maybe add a flag to auto-cancel that how to decline that. I don't because right
  now for example we're moving all the files and we're going to have a lot of files with that property, so I don't want
  to bother with that."

## Name-Based Date Detection
"Look at the name because I have this pattern I often include the date of something in the name, so it's just
straightforward to link something if it's in the name. You need to adjust your regular expressions to detect the
inclusions."

## Auxiliary Feature - Outlinks Analysis
"The fourth thing I wanted to say is I want you to check the out-links that we already have added because right now we
already obviously added some, and it would be nice to see the stats of the out-links."

### Requested Analytics
- "distribution maybe we can draw a distribution of number of out-links per page"
- "maybe out-links plot out-links over time (x-axis is the date and y-axis is the number of out-links)"
- "For now, just make a note, maybe implement something"

### Priority Note
"Most importantly, capture the intent and write it down verbatim because maybe we'll mess up implementation that's not
important right now. We don't care about that, it's an auxiliary feature, but we care about the main functionality."