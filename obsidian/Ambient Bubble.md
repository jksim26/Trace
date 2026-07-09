---
tags: [module]
source: "Trace/bubble.py, Trace/bubble.html"
---

# Ambient Bubble

A tiny web app (Python standard library only), wired live to the engine,
with a project switcher across [[Demo Scenarios]]. Its chat is ONE agent
with ONE memory: a Qwen assistant grounded in every project's decision and
[[Decision Court]] records at once — the switcher just sets the default
context, so you can ask about any project from anywhere. Carries
conversation history across switches, tolerates typos and follow-ups, cites
decision ids, and still abstains on unrecorded decisions. Degrades to
deterministic abstention without a key.

## Related

- Powered by [[Hybrid Recall]].
- Receives events from [[Desktop Watcher]] and [[Workspace Demo]] via
  [[Ambient Trigger]].
- Implements [[Recall Within Budget]].
