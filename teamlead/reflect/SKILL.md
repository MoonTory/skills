---
name: reflect
description: Coordinate a review of a completed or troubled run for durable workflow lessons. Use in a coordinator profile when the user explicitly asks to reflect or improve the workflow. Never use from a terminal worker role, and do not edit shared skills until the user approves the proposed changes.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

This is a coordinator utility. Read the installed `orchestrator` skill before launching reviewers. If the current
task assigns a terminal role, return to the caller instead of starting this workflow.

## When to invoke

- The user said "reflect" or "/reflect".
- A complex task (5+ tool calls) just landed cleanly and the recipe is worth keeping.
- The agent hit dead ends, found the working path, and the path generalizes.
- The user corrected the agent's approach mid-task.
- A non-trivial workflow emerged that isn't captured anywhere.

Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Start from the active conversation. If a file transcript is needed, locate only this workspace's session under the
harness-specific roots the user approved: Claude, Pi, or Codex. Check opening goal, current working directory, and
latest messages before accepting a match. If no path resolves, write a tight digest and use that instead.

### 2. Spawn three reviewers in parallel

Launch three reviewers together when available. They are read-only on files and external systems; the parent applies
approved edits. Give each the same transcript or digest and one lens.

| Lens | Selection | Prompt template |
|---|---|---|
| Judgment | Strong product and engineering judgment | `references/judgment-reviewer.md` |
| Tooling | Strong technical reasoning | `references/tooling-reviewer.md` |
| Divergent | Different model family from the first two | `references/divergent-reviewer.md` |

Choose the concrete models through the current repository or user policy and active harness skill.

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Task` response body.

### 3. Synthesize

Use the lead or one strong judgment agent to synthesize. It spot-checks evidence and returns Accepted, Rejected, and
Backlog candidates. Use `references/synthesizer.md` with the full reviewer outputs.

### 4. Structural enforcement check

Sanity-check the Accepted list. When a lint rule, script, metadata flag, runtime check, or Hob feature would enforce
the lesson better than prose, route it there instead of adding another instruction.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org; do not auto-apply.

Do not file backlog items or edit skills automatically. Present every proposed external write and wait for the user's
approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit: use the available `skill-creator` workflow and its draft, test, and review loop.
- `tune description: <skill path>`: use `skill-creator` description optimization.
- `new skill via skill-creator: <kebab-name>`: create it only after user approval.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
