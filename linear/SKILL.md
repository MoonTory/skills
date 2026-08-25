---
name: linear
description: "Use Linear as the source of truth for engineering work in projects that explicitly expose a `linear` MCP server. Use whenever a task names a Linear issue, asks to plan or track work in Linear, needs to create or update a durable planning artifact, or needs to create, claim, update, review, or close tracked work. Confirm the authenticated role before writes, keep issue state and evidence current, and never introduce Linear into a project that has not opted in."
compatibility: "Requires a configured Linear MCP server named `linear`."
---

# Linear workflow

Use Linear for durable scope, ownership, dependencies, and status. Use the current coding workflow for exploration, implementation, delegation, and review. Do not duplicate Linear's job in a hand-maintained Markdown task ledger.

If the user asks about setup, authentication, role profiles, or connection errors, read `references/setup.md`. When creating or updating a plan, design, investigation, or review document, read `references/artifacts.md`.

## Start with the real context

1. Read the repository instructions and the active issue before planning or changing work.
2. Confirm that a configured `linear` MCP server exists. A globally installed skill is not permission to add Linear to an unrelated project.
3. Before the first write in a session, use a read call to identify the authenticated Linear actor, workspace, team, and active issue. Recheck after a handoff or profile change.
4. Match the assigned workflow role to the authenticated actor. Reads are safe when they do not match; writes are not. Stop and report the mismatch instead of writing under the wrong name.
5. Resolve issues through Linear search or returned IDs. Never invent an issue ID, batch code, project, milestone, or dependency.

At the first meaningful update, report the execution context in this compact form:

```text
Role: <Planner | Builder | Reviewer | Owner | Unknown>
Harness: <Pi | Codex | Zed | other actual client | Unknown>
Shell: <Herdr | Direct | Unknown>
Linear: <authenticated actor name>
Issue: <ID — title | None>
```

The harness is the AI client that runs the agent. Herdr is only a shell and session manager; it is never the harness, role, or Linear identity. Report only what the runtime proves. Use `Unknown` rather than guessing.

## Role boundaries

The authenticated app normally determines the role. A workflow assignment may narrow that role but must not silently widen it. A directly authenticated human may act as Owner when the user asks, but should not claim to be an app role.

Not every agent in a workflow has a Linear identity, and that is normal. A lead session that orchestrates delegated agents usually holds the human's own authentication and acts as Owner on their behalf; exploration or implementation agents launched without a role token cannot and should not write to Linear. Those agents report durable facts to the lead, and the lead records them under its own identity, attributing the source in the comment or evidence ("builder run reported…"). Give an agent a role token only when it should speak in Linear as that role.

When the lead takes a decision on the user's behalf — a scope call, an API shape, a terminal transition the user has not seen — record it where the affected work lives (the issue's Decisions or a comment) and mark it as open to veto until the user confirms. A vetoable decision is a durable fact like any other; a decision that only exists in a chat transcript is not recorded.

## Waiting on the owner

Two situations need the owner's attention, and they are not the same. Statuses stay untouched in both — a status describes the work, an issue label describes what is needed from the owner, and clearing the label resumes the work exactly where it stood.

- `Awaiting Ruling` — a decision was taken on the owner's behalf and work continued. The issue's Decisions entry or a comment names the decision "(open to veto)". The owner clears the label by confirming or vetoing; a veto becomes a follow-up, not a rewrite of history.
- `Needs Input` — work is paused on something only the owner can supply (a signed API shape, a product choice, missing information). Add the label, write one comment stating the exact question and what unblocks, assign the issue to the owner, and move to other work instead of guessing. The status keeps telling the truth: `Scoping` if execution never started, unchanged if the block struck mid-flight.

These are issue labels, not project labels; match the team's existing label naming (Linear's defaults are Title Case). A saved view per label gives the owner a standing inbox: what they owe a ruling on, and what is stuck on them. Do not fold either situation into a status — that would overwrite the issue's real position in the pipeline and punch holes in the role transitions above.

### Planner

- Own architecture, scoping, issue breakdown, dependencies, acceptance criteria, and ordering.
- Own the canonical planning document when work needs one. Keep its work breakdown aligned with the issues that were approved and created.
- Turn unclear work into `Scoping`, and move it to `Ready` only when a builder can execute it without filling in a product or architecture decision.
- Preview a new issue set, bulk rewrite, milestone structure, or dependency graph before creating it. After approval, apply that exact batch and report the resulting Linear IDs.
- Do not claim that implementation or review passed. Move `Ready To Land` to `Done` only after landing and validation evidence exists.

### Builder

- Read the whole issue, its dependencies, and repository instructions before changing code.
- Move `Ready` to `In Progress` when work actually starts. Do not claim several issues at once without a reason.
- Stay within the agreed scope. When the ticket is missing a decision or reveals separate work, record the blocker or propose a follow-up instead of quietly expanding the ticket.
- Move to `In Review` only after checking every acceptance criterion and recording the validation that actually ran.
- Do not approve the implementation or mark it `Ready To Land` or `Done`.

### Reviewer

- Review the issue contract, implementation evidence, and current code without inheriting the builder's assumptions.
- Record actionable findings with evidence. Move the issue back to `In Progress` when changes are required.
- Move `In Review` to `Ready To Land` only when the acceptance criteria and proportional checks pass.
- Do not implement fixes while acting as Reviewer. A deliberate role change requires the matching Linear identity.

## Status contract

Use the smallest transition that tells the truth about the work.

| Status | Meaning | Normal owner |
| --- | --- | --- |
| `Backlog` | Known work that is not being scoped or queued yet | Planner or Owner |
| `Scoping` | The outcome or execution contract still needs decisions | Planner |
| `Ready` | Scoped, unblocked, and executable | Planner |
| `In Progress` | A builder is actively working on it | Builder |
| `In Review` | Implementation is ready for an independent verdict | Builder hands to Reviewer |
| `Ready To Land` | Review passed; merge or release remains | Reviewer hands to Planner or Owner |
| `Done` | Landed and validated | Planner or Owner |
| `Canceled` | Intentionally stopped and not expected to resume | Planner or Owner |
| `Duplicate` | Replaced by another linked issue | Planner or Owner |

There is no separate `Parked` state. `Backlog` covers work that is worth retaining but not active.

Normal transitions are:

```text
Backlog -> Scoping -> Ready -> In Progress -> In Review -> Ready To Land -> Done
                                     ^            |
                                     +------------+  changes requested
```

Cancellation and duplicate marking are terminal decisions. Require a clear user instruction or an already-approved plan, link the reason or canonical issue, and verify the result after writing.

## Issue contract

Use Linear's durable issue ID and a plain, descriptive title. Do not replace them with agent-made wave, batch, letter, or number codes. When older planning notes know the work by such a code, keep the title plain and add one line to the description ("Historical planning notes refer to this work as TF4") so both records stay searchable.

When creating or materially rewriting an issue, preserve the project's template and make these facts clear:

- **Goal:** the observable outcome.
- **Context:** why the work exists and the evidence behind it.
- **Scope:** what is included and what is explicitly excluded.
- **Acceptance criteria:** checkable results, not implementation activity.
- **Validation:** the checks or real-product evidence needed before review and completion.
- **Dependencies:** only real ordering or context dependencies.
- **Open questions:** unresolved choices that keep the issue in `Scoping`.

Do not add a permanent repository-location field merely to say where the project lives. Source links, branches, commits, and pull requests carry code location when they exist. A repository without a published remote still produces citable evidence: local commit hashes, tags, the checks that ran with their results, and archive or report paths. Cite what actually exists rather than leaving validation empty or inventing links that will not resolve. Use milestones only for a real release, phase, or checkpoint that groups several issues; one issue does not need milestone ceremony.

## Durable artifacts

Use a Linear document when a plan, design, investigation, or review is too large for one issue, spans several issues, or needs a durable account of decisions and tradeoffs. Do not create a document for a short issue whose contract is already clear.

- Search for an existing canonical document before creating one. Update it by ID rather than creating `v2`, `final`, or duplicate documents; Linear already keeps document history.
- Create a document with exactly one parent. Use the project as parent for cross-issue work and the issue as parent for material that belongs to one issue.
- On update, omit the parent unless intentionally moving the document. Passing a parent reparents it.
- Use the current Linear connection's document-save capability. Creation omits the document ID; updates include it and may replace the full content or apply a narrow patch.
- Prefer titles such as `Plan — <outcome>`, `Design — <topic>`, `Investigation — <topic>`, and `Review — <topic>`. Do not use agent-made batch or wave codes.
- Keep issue descriptions self-contained enough to execute, then link the canonical document for wider context. Do not copy the full document into issue descriptions or comments.
- Use comments only to announce a material decision, handoff, review finding, or artifact update. Link the document instead of pasting it.
- Re-read the document and its parent after saving. Verify title, content, parent, and returned URL before reporting success.

The Planner owns planning artifacts. A Builder reads them but records implementation evidence on the issue. A Reviewer adds concise findings to the issue; use a separate `Review — <topic>` document only when the review itself needs a long-lived, structured report.

## Mutation rules

- Read the current object immediately before changing it. Preserve fields outside the requested scope.
- Show the exact proposal and wait for approval before bulk issue creation, bulk restructuring, or a new dependency graph. Routine updates to the active issue do not need repeated confirmation when the approved workflow already requires them.
- Keep comments sparse and useful: decisions, blockers, handoffs, review findings, and validation evidence. Do not post a running transcript or generic progress noise.
- After each write or coherent batch, read back the affected items and check actor, fields, relations, and status.
- Report created or updated issue IDs and any partial failure. Never state that a write succeeded from intent alone.
- Do not cancel, mark duplicate, delete, or overwrite substantial user-written content without clear authority.

## Working with other workflows

Linear is canonical for the issue's scope, dependencies, assignment, and delivery status. Other skills may keep local scratch plans or execution state, but those records must not compete with or contradict Linear.

A project adopting Linear often has an older ledger — a board file, a plan document, a notes directory. During that transition exactly one record is canonical at a time, and the user decides which. Until they hand authority to Linear, treat the existing ledger as the source of truth and Linear as a deliberate mirror: copy facts in on request, note in each record where the other lives, and never let the two silently diverge. After the handoff, the old ledger stops being updated and says so at the top.

The coding workflow decides how to inspect, delegate, implement, test, and review. This skill decides how those facts enter and move through Linear. The session shell decides where processes run. Keep these concerns separate.

If Linear is unavailable, say which state may now be stale. Do not silently switch to a Markdown ticket system or invent remembered board state. Continue local work only when the user-approved scope remains unambiguous and repository rules permit it.

## Handoff and completion

A useful handoff states:

```text
Issue: <ID — title>
Status: <current Linear status>
Actor: <authenticated Linear actor>
Changed: <durable facts written to Linear>
Evidence: <checks, links, or review verdict>
Blocked by: <issue IDs or None>
Next: <one concrete action and expected role>
```

Completion means the real artifact and Linear agree. `Done` requires landing plus the validation promised by the issue; an agent finishing its response, a passing type check alone, or a runtime becoming idle is not completion.
