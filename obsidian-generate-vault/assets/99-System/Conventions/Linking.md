---
tags: [type/system]
---
# Linking Conventions

Links are the backbone of a Zettelkasten. Every note should link to at least one other note.

## Link Types

| Syntax | Use |
|--------|-----|
| `[[Note Name]]` | Standard wikilink |
| `[[Note Name\|Display Text]]` | Aliased wikilink |
| `[[Note Name#Heading]]` | Link to a specific heading |
| `![[Note Name]]` | Embed (transclude) a note |
| `![[image.png]]` | Embed an image |

## Guidelines

1. **Link liberally** — when you mention a concept that has its own note, link it.
2. **Use aliases** for readability: `[[Project Brief\|the project]]` reads better in prose.
3. **Avoid deep paths** — Obsidian resolves note names globally, so `[[Daily Note]]` is enough; you don't need `[[03-Daily/2025-01-15]]`.
4. **Backlinks matter** — check the backlinks pane to discover connections you didn't plan.
5. **Embed sparingly** — transclusion is powerful but can make notes hard to read if overused.

## Orphan Notes
A note with zero backlinks and zero outgoing links is an orphan. During weekly review, check the Graph View for disconnected nodes and link or delete them.
