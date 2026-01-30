---
tags: [type/system]
---
# Frontmatter Conventions

Every note should include YAML frontmatter between `---` fences at the top of the file.

## Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `tags` | List of tags categorizing the note | `[type/note, status/active]` |

## Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `aliases` | Alternative names for linking | `[API Gateway, APIGW]` |
| `date` | Creation date | `2025-01-15` |
| `last_updated` | Last modification date | `2025-01-20` |
| `source` | URL or reference for the original material | `https://example.com` |
| `author` | Author of the source material | `Jane Doe` |
| `project` | Related project link | `[[My Project]]` |
| `status` | Note lifecycle status | `draft`, `active`, `done`, `archived` |

## Example

```yaml
---
aliases: [Docker Networking]
tags: [type/note, context/work, status/active]
date: 2025-01-15
last_updated: 2025-01-20
source: https://docs.docker.com/network/
---
```

## Guidelines
- Use **lists** for tags and aliases, even if there's only one value.
- Dates use **ISO 8601** format: `YYYY-MM-DD`.
- Keep frontmatter concise — detail belongs in the note body.
