# Trace, as an Obsidian vault

This folder is a small [Obsidian](https://obsidian.md) vault: one note per Trace
concept or module, linked to the others with `[[wikilinks]]`. Open it in Obsidian
and switch to **Graph View** to see Trace's architecture as a node graph — the
decision store at the center, the three pillars radiating out, and each module
wired to the concepts it implements.

## Open it

1. In Obsidian: **File → Open folder as vault** → select this `obsidian/` folder.
2. Click the graph icon in the left ribbon (or `Ctrl/Cmd+G`) for **Graph View**.
3. Start from [[Trace]] and follow the links outward.

## Keep it synced with GitHub

Obsidian has no built-in GitHub sync, but the community plugin **Obsidian Git**
does exactly that — it commits and pushes/pulls this vault like any other git
repo, on a timer or on demand:

1. In Obsidian: **Settings → Community plugins → Browse** → search "Obsidian
   Git" → install and enable it.
2. Since this vault already lives inside the `Trace` git repo, no extra
   remote setup is needed — the plugin will pick up this repo's existing
   `origin` remote and your existing GitHub auth (SSH key or credential
   manager) on this machine.
3. Optional: **Settings → Obsidian Git** → turn on "Vault backup interval"
   (autocommit) if you want it to push on a schedule instead of manually via
   the command palette (`Obsidian Git: Commit and sync`).

If you'd rather keep your notes vault as a *separate* repo instead of living
inside `Trace/obsidian/`, that's the more common Obsidian Git setup — see the
plugin's own docs for `git init` + `git remote add origin <your-notes-repo>`
in a standalone vault folder.

## Map of notes

- [[Trace]] — the root node: pitch, the three pillars, links to every module.
- `concepts/` — one note per pillar and cross-cutting idea (golden thread,
  bi-temporal time-travel, decision court).
- Everything else at the top level is one note per code module, named after
  its source file so it's easy to find in `Trace/Trace/`.
