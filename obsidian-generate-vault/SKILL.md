---
name: obsidian-generate-vault
description: Generate a complete Obsidian vault structured as a second brain for software engineers. Use when the user asks to create, scaffold, or set up an Obsidian vault, note-taking system, second brain, or personal knowledge management (PKM) workspace. Produces a numbered-folder hierarchy with templates, a dashboard, tagging conventions, and Obsidian configuration — ready to open in Obsidian immediately.
---

# Obsidian Vault Generator

Generate a full Obsidian vault directory using the Write and Bash tools. The vault follows a numbered-folder hierarchy inspired by the Zettelkasten / PARA method, optimised for a software engineer's daily notes, projects, and knowledge base.

**Design rule:** maximum two levels of nesting. Every note reachable in two clicks from the Dashboard.

## Step 1 — Ask the user

Before creating anything, confirm:
1. **Vault path** — where to create it (e.g. `~/Documents/MyVault`).
2. **Vault name** — display name for the dashboard heading (defaults to folder name).
3. **Optional customisations** — extra top-level folders, extra Knowledge sub-topics, or different template fields. Apply reasonable defaults if the user has no preference.

## Step 2 — Create folder structure

Create these directories under the vault root. Folder names MUST start with their number prefix exactly as shown.

```
<vault-root>/
├── 00 - Dashboard/
├── 01 - Personal/
│   ├── Daily/
│   ├── Fleeting/
│   ├── Plans/
│   ├── Reflections/
│   └── Health/
├── 02 - Knowledge/
│   ├── Computing/
│   ├── Philosophy/
│   ├── History/
│   ├── Literature/
│   └── Health/
├── 03 - Projects/
│   ├── Project1/
│   ├── Project2/
│   └── Project3/
├── 04 - References/
│   ├── Articles/
│   ├── Courses/
│   ├── Books/
│   └── Tutorials/
├── 99 - Meta/
│   ├── Templates/
│   └── System/
└── .obsidian/
```

Create every directory with `mkdir -p`.

## Step 3 — Write Obsidian configuration

Create these JSON files inside `.obsidian/`:

**app.json**
```json
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "01 - Personal/Fleeting",
  "attachmentFolderPath": "99 - Meta/System",
  "showLineNumber": true,
  "strictLineBreaks": false,
  "readableLineLength": true
}
```

**daily-notes.json**
```json
{
  "folder": "01 - Personal/Daily",
  "format": "YYYY-MM-DD",
  "template": "99 - Meta/Templates/Daily Note"
}
```

**templates.json**
```json
{
  "folder": "99 - Meta/Templates"
}
```

**core-plugins.json**
```json
["file-explorer","global-search","switcher","graph","backlink","outgoing-link","tag-pane","page-preview","daily-notes","templates","note-composer","command-palette","editor-status","bookmarks","outline","word-count","file-recovery"]
```

**community-plugins.json**
```json
[]
```

## Step 4 — Write template notes

Create each file inside `99 - Meta/Templates/`.

### Daily Note.md
```markdown
---
aliases: []
tags: [type/daily, context/personal]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{date:YYYY-MM-DD}} {{date:dddd}}

## Plan
- [ ]

## Notes


## End of Day
### What went well?

### What could be improved?

### Blockers

```

### Project.md
```markdown
---
aliases: []
tags: [type/project, status/active]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{title}}

## Overview
- **Status:** #status/active
- **Start date:** {{date:YYYY-MM-DD}}
- **Target date:**

## Goals


## Tasks
- [ ]

## Log
### {{date:YYYY-MM-DD}}
-

## References

```

### Meeting.md
```markdown
---
aliases: []
tags: [type/meeting]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{title}}

- **Date:** {{date:YYYY-MM-DD}}
- **Attendees:**

## Agenda


## Notes


## Action Items
- [ ]

```

### 1-on-1.md
```markdown
---
aliases: []
tags: [type/meeting, context/1-on-1]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# 1-on-1 {{date:YYYY-MM-DD}}

- **With:**

## Their Updates


## My Updates


## Discussion Points


## Action Items
- [ ]

```

### Knowledge.md
```markdown
---
aliases: []
tags: [type/study]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{title}}

- **Source:**
- **Topic:**

## Summary


## Key Points


## Code Snippets

```

```

## References

```

### Reference.md
```markdown
---
aliases: []
tags: [type/reference]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{title}}

- **Type:**
- **Source:**
- **Author:**

## Summary


## Key Takeaways


## Quotes / Highlights


## Related

```

### Fleeting Note.md
```markdown
---
aliases: []
tags: [type/fleeting]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# {{title}}

> Quick thought — move to the right folder once it matures.


```

## Step 5 — Write seed notes

### 00 - Dashboard/Home.md
```markdown
---
aliases: [Home, Index]
tags: [type/dashboard]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# <vault-name> Dashboard

> Two clicks to anything.

## Quick Capture
- [[01 - Personal/Fleeting/|Fleeting Notes]]

## Daily
- [[01 - Personal/Daily/|Daily Notes]]

## Projects
| Project | Status |
| ------- | ------ |
|         |        |

## Navigation
| #  | Area | Description |
|----|------|-------------|
| 00 | [[00 - Dashboard/|Dashboard]] | You are here |
| 01 | [[01 - Personal/|Personal]] | Daily notes, plans, reflections |
| 02 | [[02 - Knowledge/|Knowledge]] | Computing, philosophy, history, literature |
| 03 | [[03 - Projects/|Projects]] | Active work & personal projects |
| 04 | [[04 - References/|References]] | Articles, books, courses, tutorials |
| 99 | [[99 - Meta/|Meta]] | Templates & system files |

## Tags Reference
- **Type:** `#type/daily`, `#type/study`, `#type/project`, `#type/meeting`, `#type/reference`, `#type/fleeting`
- **Context:** `#context/work`, `#context/personal`, `#context/studies`, `#context/1-on-1`
- **Status:** `#status/active`, `#status/on-hold`, `#status/done`, `#status/archived`
- **Priority:** `#priority/high`, `#priority/medium`, `#priority/low`
```

Replace `<vault-name>` with the user's chosen vault name.

### 01 - Personal/Fleeting/Scratch.md
```markdown
---
aliases: [Scratch]
tags: [type/fleeting]
date: "{{date:YYYY-MM-DD}}"
last_updated: "{{date:YYYY-MM-DD}}"
---
# Scratch Pad

Quick capture space. Move notes to the right folder when ready.

---

```

## Step 6 — Write .gitignore

```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/
.obsidian/hotkeys.json
.trash/
```

## Step 7 — Report to user

After creating all files, print a summary:
- Vault path
- Number of folders created
- Number of templates created
- Remind the user to open the vault root in Obsidian
- Suggest installing community plugins: **Dataview**, **Calendar**, **Tag Wrangler**
