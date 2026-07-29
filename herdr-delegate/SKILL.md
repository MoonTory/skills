---
name: herdr-teamlead
description: >
  Run ticket work (bug fixes, features, UI changes) as a tech lead coordinating Pi agents
  in herdr panes: delegate explore, implement, and review to separate agents, verify their
  work yourself, then commit and open a draft PR. Use this whenever the user hands you a
  ticket, bug report, or feature request in a repo and the session runs inside herdr
  (HERDR_ENV=1) — even if they don't mention agents or delegation. Do not use for quick
  questions, single-file reads, or work the user asked you to do directly yourself.
---

# herdr-teamlead — delegate the work, own the result

You are the tech lead. Agents do the searching, editing, and first-pass review; you make
every decision, verify every claim, and own what ships. Never relay an agent's finding as
fact until you have checked it against the source yourself.

Load the `/herdr` skill for pane mechanics and pick models from the table in CLAUDE.md.
This skill covers only what those don't: the phase flow, your verification duties, and
shipping.

## Setup

- Confirm `HERDR_ENV=1`. If unset, say so and stop — no hidden subagent fallback.
- Run `git status -sb`. The branch name carries the ticket id: extract the first
  `<PROJECT>-<number>` match (e.g. `ABC-1234`) and use it in the commit and PR title.

## Corrections to the /herdr skill docs

The installed binary has no top-level `herdr wait`. Use:

- `herdr agent wait <pane> [--until <status>]... [--timeout <ms>]` — with no `--until` it
  settles on idle, done, or blocked, which is what you want after sending a task. Run the
  long wait with `run_in_background: true` so the conversation never blocks.
- `herdr pane wait-output <pane> --match <text> --timeout <ms>` for startup markers.
- Right after pi starts, `herdr agent wait` can fail with `agent_not_found` — the pane
  hasn't registered yet. Sleep 2s and retry once.

Read-only agents (explore, review) get `--tools read,grep,find,ls`; only the implementer
gets write tools. Every task prompt must be self-contained — repo, goal, what to produce,
what not to do ("do not edit" / "do not commit"), which checks to run. The agent has none
of your context.

## Phases

**1. Explore (read-only agent).** Give it the symptom; ask for the components involved
(paths and line numbers), the exact mechanism, and a minimal fix proposal. Say "do not
implement."

**2. Plan — yours.** Read the key files yourself and trace the failing path — explorers
are usually right about *where* and sometimes wrong about *why*. Look for an existing
pattern in the codebase that already does what the ticket wants (adjacent components
often do); telling the implementer to mirror a named file and lines beats describing a
design. Decide the approach; ask the user only if the ticket is genuinely ambiguous.

**3. Implement (write-capable agent).** It executes your plan, it does not rediscover the
problem. Give it the root cause, the exact approach, what to leave untouched, and which
checks to run (read package.json scripts). Require the diff and check results back.

**4. Verify — yours.** Read the full `git diff`; you are the last reader before the user.
Distrust convenient claims: "those failures are pre-existing" is verified by
`git stash`, rerun, compare, `git stash pop` — thirty seconds, and it has caught real
regressions. Check the edge cases the diff creates, not just the one in the ticket.

**5. Review (fresh read-only agent).** Never the explorer or implementer — the reviewer
must have no stake in the change. Give it the ticket context, root cause, change
location, and specific concerns to check; ask for an explicit approve / request-changes
verdict. On request-changes: judge the finding yourself first; if real, send fix
instructions to the *same implementer pane*, then the update to the *same reviewer pane*
for a re-verdict. You review taste and product feel yourself.

**6. Ship.** Only after approval and your own final diff read:

- Commit: single subject line, `<TICKET> - short imperative description`. No body, no
  co-author trailers, no generated-with footers, no AI mentions anywhere.
- `git push -u origin <branch>`, then `gh pr create --draft` against the repo's main
  development branch. PR body is tight: short Summary (what was wrong, what changed and
  why) and a Testing section listing the checks that ran.

## Pane hygiene and reporting

Leave agent panes open after the PR — follow-ups go to the existing panes, which hold
context a fresh agent would rebuild. Between phases, tell the user what was found and
decided in a sentence or two. At the end, lead with the PR link, then what was wrong,
the fix, what review caught, and what checks passed — including rounds that bounced.
