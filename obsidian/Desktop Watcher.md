---
tags: [module]
source: Trace/watcher.py
---

# Desktop Watcher

The Windows desktop watcher: polls the foreground window title (title bar
only, no screen capture) and, on an allowlist match via [[Ambient Trigger]],
pushes the document-open event to the bubble — open the Level 1 fire plan in
Acrobat or Revit and Trace nudges you, unprompted.

## Related

- Uses [[Ambient Trigger]].
- Pushes events to [[Ambient Bubble]].
