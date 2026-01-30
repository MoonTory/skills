---
tags: [type/system]
---
# Tags Conventions

Tags use a **namespace/value** format for consistency and easy filtering.

## Tag Namespaces

### type/
The kind of note.
- `type/daily` — Daily journal note
- `type/note` — Atomic or permanent note
- `type/project` — Project brief or tracker
- `type/meeting` — Meeting notes
- `type/rfc` — Request for comments / design doc
- `type/learning` — Learning objectives or study notes
- `type/area` — Area of responsibility
- `type/system` — Internal vault infrastructure

### status/
Lifecycle state.
- `status/active` — Currently being worked on
- `status/on-hold` — Paused
- `status/done` — Completed
- `status/archived` — No longer relevant, kept for reference

### context/
Where or why the note matters.
- `context/work` — Professional
- `context/personal` — Personal life
- `context/studies` — Learning and courses
- `context/1-on-1` — One-on-one meetings

### priority/
Urgency level (optional, mostly for projects and tasks).
- `priority/high`
- `priority/medium`
- `priority/low`

## Guidelines
- Use **frontmatter `tags` field** for primary tags: `tags: [type/note, status/active]`.
- Use **inline `#tag`** sparingly — for ad-hoc labels within the note body.
- Avoid creating one-off tags. If a tag doesn't fit a namespace above, consider whether it's needed.
- Review and prune unused tags during weekly review.
