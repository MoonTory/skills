---
name: linear
description: "Use Linear as the source of truth for engineering work in projects that explicitly expose a `linear` MCP server. Use whenever a task names a Linear issue, asks to plan or track work in Linear, needs a durable planning or review artifact, or needs to create, claim, update, review, or close tracked work. Confirm the authenticated actor before writes, preserve the separation between Orchestrator, Planner, Builder, Reviewer, and Owner, and never introduce Linear into a project that has not opted in."
---

# Linear workflow

Use Linear for durable scope, ownership, dependencies, decisions, evidence, and status. Use the current coding workflow for exploration, implementation, delegation, and review. Do not duplicate Linear's job in a live Markdown task ledger.

Read the focused reference when the task needs it:

- Setup, authentication, tokens, delegation, role profiles, or connection errors: `references/setup.md`.
- Exploration, Plan, or Review documents: `references/artifacts.md`.
- Any issue comment: `references/comments.md`.

When the repository root contains `LINEAR.md`, read it for project identifiers, label mappings, and other local bindings before resolving tracked work. The file supplements repository instructions; it does not replace this workflow or grant Linear access without a configured `linear` MCP server.

## Start with the real context

1. Read the repository instructions, root `LINEAR.md` when present, and the active issue before planning or changing work.
2. Confirm that a configured `linear` MCP server exists. A globally installed skill is not permission to add Linear to an unrelated project.
3. Before the first write in a session, use read calls to identify the authenticated Linear actor, workspace, team, project, and active issue. Recheck after a handoff, reconnect, or profile change.
4. Match the assigned workflow role to the authenticated actor. Reads are safe when they do not match; writes are not. Stop and report the mismatch instead of writing under the wrong name.
5. Resolve issues through Linear search or returned IDs. Never invent an issue ID, project, milestone, relation, status, label, or delegate.

At the first meaningful update, report the execution context in this compact form:

```text
Role: <Orchestrator | Planner | Builder | Reviewer | Owner | Unknown>
Harness: <Pi | Codex | Claude | Zed | other actual client | Unknown>
Shell: <Herdr | Direct | Unknown>
Linear: <authenticated actor name>
Issue: <ID — title | None>
```

The harness is the AI client that runs the agent. Herdr is only a shell and session manager; it is never the harness, role, or Linear identity. Report only what the runtime proves. Use `Unknown` rather than guessing.

## Writer and delegation contract

Use separated authorship. The actor visible in Linear should show which role produced each durable fact.

| Phase | Delegate | Durable author | Metadata and status writer |
| --- | --- | --- | --- |
| Scoping | Planner | Planner | Orchestrator |
| Implementation | Builder | Builder | Orchestrator |
| Review | Reviewer | Reviewer | Orchestrator |
| Owner input | None | Owner, or Orchestrator with clear Owner attribution | Orchestrator |
| Landing | Orchestrator | Orchestrator | Orchestrator |

When the project declares a human Owner, that person remains the assignee from issue creation through completion. The Orchestrator changes the app delegate at phase boundaries. Planner, Builder, and Reviewer publish through their matching app identities, but they never change status, labels, assignee, delegate, project, priority, milestone, or relations.

The Orchestrator is the sole metadata and status writer. It reads the role's published evidence before changing the issue. It does not normally publish a Planner, Builder, or Reviewer artifact on that role's behalf. If the correct role cannot publish, stop the phase and repair the role connection instead of flattening authorship.

A directly authenticated human acts only as themselves. Resolve the human Owner from live assignment plus project policy or explicit user direction; authentication alone does not confer Owner authority. Preserve an existing human assignee, and stop before creating or reassigning an issue when no authoritative Owner can be resolved. Do not call the human session Orchestrator, Planner, Builder, or Reviewer. A role assignment may narrow an actor's authority but cannot widen it.

## Status contract

Only the Orchestrator changes status.

| Status | Meaning |
| --- | --- |
| `Backlog` | Known work that is not being scoped or queued yet |
| `Scoping` | The outcome or execution contract still needs decisions |
| `Needs Input` | One clear Owner action is required before the next truthful stage |
| `Ready` | Scoped, approved, unblocked, and executable |
| `In Progress` | A Builder is actively working on a ticket branch |
| `In Review` | The current implementation round is ready for an independent verdict |
| `Ready To Land` | Review and Owner gates passed; the approved change has not landed through the repository's chosen merge strategy |
| `Done` | The approved work landed in the main branch and passed final verification |
| `Canceled` | Intentionally stopped and not expected to resume |
| `Duplicate` | Replaced by another linked issue |

The normal path is:

```text
Backlog
-> Scoping
-> Needs Input
-> Ready
-> In Progress
-> In Review
-> Needs Input
-> Ready To Land
-> Done
```

Use the second `Needs Input` only when the issue requires Owner validation. If it does not, a passed review can move directly to `Ready To Land`.

The required loops are:

```text
Review rejects:
In Review -> In Progress -> In Review

Material scope change:
Any active status -> Scoping -> Needs Input -> Ready

Owner approves without changing scope:
Needs Input -> previous honest execution stage

Owner changes the contract:
Needs Input -> Scoping
```

A material rescope updates the issue contract and produces newly named planning artifacts before implementation resumes. Every changed implementation returns to `In Review`; never move directly from `In Progress` to `Ready To Land` or `Done`.

`Needs Input` is a status, never a label. Before entering it, write the exact Owner action, its impact, and the stage to resume. Clear the delegate while the issue waits. Do not use `Needs Input` for a question the Planner should resolve during `Scoping`.

Cancellation and duplicate marking are terminal decisions. Require clear authority, record the reason or canonical issue, and verify the result after writing.

## Branch and landing contract

A remote is not required:

1. Work begins on a ticket branch tied to the Linear issue ID.
2. Builders prepare commits on that branch.
3. Review and Owner validation use that branch.
4. `Ready To Land` means no further product or technical work is required before merge.
5. The Orchestrator delegates the issue to itself and lands the branch into the project's main branch.
6. Final verification runs against the landed tree.
7. The Orchestrator records the landing evidence and moves the issue to `Done`.

When a remote exists, the same contract maps to a pull request. Do not treat work already committed to the main branch as `Ready To Land`.

## Role boundaries

### Orchestrator

- Own all issue metadata writes, including status, assignment, delegation, labels, relations, owner decisions, coordination records, and landing evidence. This grants authority to record the resolved Owner, not to choose one.
- Delegate the active phase to Planner, Builder, Reviewer, or itself, while leaving the human assignee unchanged.
- Read the active role's published artifact or comment before applying the next transition.
- Preview broad issue creation, restructuring, or a new dependency graph before writing it.
- Keep the issue contract and area labels current when scope changes.
- Move `Ready To Land` to `Done` only after landing and the promised checks pass on the landed tree.

### Planner

- Own exploration, architecture, scoping, issue proposals, proposed dependencies, acceptance criteria, ordering, and validation strategy. The Orchestrator alone writes relations.
- Publish one canonical Exploration or Plan document per distinct scope when the work needs a durable artifact.
- Make issue proposals executable without filling in a product or architecture decision.
- Publish a concise Plan ready comment, then hand control to the Orchestrator.
- Do not create or update issue metadata, delegate roles, or change status.

### Builder

- Read the whole issue, its dependencies, linked artifacts, and repository instructions before changing code.
- Work on the ticket branch and stay within the agreed scope.
- Report a missing decision, material rescope, or separate follow-up instead of quietly expanding the issue.
- Publish a concise Builder handoff with the outcome, checks that actually ran, deviations, and next role.
- Do not change issue metadata or status, approve the implementation, or land the branch.

### Reviewer

- Review the current issue contract, linked artifacts, implementation evidence, and ticket branch without inheriting the Builder's assumptions.
- Publish actionable findings with evidence and a clear pass or reject verdict.
- Create one Review document whenever a review has a blocking finding, spans more than one implementation round, binds to an exact revision, or otherwise needs durable structure. Update that same document through rejection, fixes, and final approval.
- Recheck every changed implementation round before approving it.
- Do not change issue metadata or status, implement fixes, or land the branch.

## Issue contract

Use Linear's durable issue ID and a plain, descriptive title. Never put agent-made batch, wave, worker, model, pane, tab, or context identifiers in Linear titles, descriptions, comments, documents, relations, or user-facing reports. Temporary orchestration keys remain inside live scratch state.

The issue description always contains the current:

- **Outcome:** what will be true when the issue succeeds.
- **Context:** why the work exists and the evidence behind it.
- **Scope:** what is included and explicitly excluded.
- **Acceptance criteria:** checkable results, not implementation activity.
- **Validation:** checks and real-product evidence required before completion.
- **Dependencies:** true blocking or ordering dependencies only, stated with direction. Put background links in Context or `relatedTo`.
- **Open decisions:** unresolved choices that keep the issue in `Scoping` or move it to `Needs Input`.

The prose and live relation graph must agree:

- If issue A depends on issue B, A is `blockedBy` B and B `blocks` A.
- `relatedTo` records useful context only. It never satisfies a written ordering dependency.
- Parent, duplicate, and release relations do not stand in for blocking direction.
- Keep a satisfied blocker for history unless the contract itself changed; a completed blocker is satisfied, not absent.

Planner proposes dependency changes in the Plan or issue proposal. Orchestrator writes them, reads both sides back, and checks parity before moving an issue to `Ready` or starting implementation.

Before writing a blocking relation, read both issues and their current relations. Reject self-links, duplicate edges, and dependency cycles. After writing, read both ends back. An unresolved blocker prevents `Ready`; a context link never does.

The Orchestrator updates this contract before implementation resumes after a material rescope. Do not add a permanent repository-location field merely to say where the project lives. Cite source links, commits, pull requests, checks, stable previews, or report paths that actually exist. Never use a local-only URL as durable evidence.

## Area and type labels

Use the project's defined area labels to show meaningful implementation ownership at a glance:

- Apply the union of meaningful areas across the whole issue.
- Set the expected areas during `Scoping`.
- Add newly affected areas when scope grows.
- Keep area labels after completion so they remain useful for filtering and analysis.
- Do not add a label for every incidental fixture, generated file, or formatting-only change.
- Use flat labels when one issue may touch several areas; do not place mutually compatible areas in a one-choice label group.
- Apply one durable work-type label, such as `Bug`, `Feature`, or `Improvement`, when the project defines them.

Repository instructions own the exact label-to-path mapping. Do not invent a mapping in the generic skill.

## Durable artifacts and comments

Use a Linear document when an Exploration, Plan, or Review needs more structure than the issue or a short comment can hold. Before creating or changing one, read `references/artifacts.md`.

Use comments only for Plan ready, Builder handoff, Review verdict, Needs Input, Owner decision, and Landed and verified events. Before posting one, read `references/comments.md`.

Do not copy full plans, reviews, raw test output, temporary URLs, or internal execution details into comments. Link the canonical artifact and summarize only the event that changes what happens next.

## Mutation rules

- Read the current object immediately before changing it and preserve fields outside the actor's responsibility.
- When the project declares a human Owner, verify that assignee before every status or delegate transition and repair a missing assignment before continuing.
- Verify the actor again before the first write after any reconnect, profile change, or long pause.
- Stop if the authenticated actor does not match the assigned role.
- Show the exact proposal and wait for approval before broad issue creation, bulk restructuring, or a new dependency graph.
- After every write, read back the affected object and verify actor, fields, relations, delegate, labels, parent, or status as applicable.
- Report created or updated issue IDs and any partial failure. Never state that a write succeeded from intent alone.
- Do not cancel, mark duplicate, delete, reparent, or overwrite substantial user-written content without clear authority.

## Working with other workflows

Linear is canonical for durable issue scope, dependencies, assignment, delegation, decisions, evidence, and delivery status. Other skills may keep temporary execution state, but those records must not compete with Linear or appear in durable comments and artifacts.

Do not create or maintain a live Markdown board, local ticket mirror, or durable research ledger as a fallback. If an older ledger exists, follow the project's cutover state: preserve it as history once Linear becomes canonical, but never append new status.

The coding workflow decides how to inspect, delegate, implement, test, and review. This skill decides how those facts enter and move through Linear. The session shell decides where processes run. Keep these concerns separate.

If Linear is unavailable, state which durable facts may now be stale and stop Linear-dependent transitions. Do not switch to a Markdown board or reconstruct the issue from memory. Continue local work only when the approved issue contract remains available and repository rules permit it.

## Handoff and completion

A useful handoff states:

```text
Issue: <ID — title>
Status: <current Linear status>
Actor: <authenticated Linear actor>
Delegate: <current app delegate or None>
Changed: <durable facts written by this actor>
Evidence: <checks, branch, artifact, or verdict>
Next: <one concrete action and expected role>
```

Completion means the landed work and Linear agree. `Done` requires the approved change to have landed through the repository's chosen merge strategy, the exact landed commit to be recorded, and the promised validation to pass on that landed tree. A role finishing its response, one passing check, or an idle runtime is not completion.
