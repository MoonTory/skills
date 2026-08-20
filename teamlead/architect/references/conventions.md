# Teamlead conventions

Read the repository's `AGENTS.md` and the installed `herdr` skill first. They are authoritative when they disagree
with this collection.

## Choose the smallest useful flow

- Direct work: one agent can finish safely in one pass. Do not add team ceremony.
- Ticket flow: a bounded bug, feature, or refactor benefits from exploration, a plan, implementation, and review.
- Custom workflow: the work is unusual, risky, or ambiguous enough that its phases must be designed first.
- Orchestrate: a multi-day program outlives one agent and needs durable queue state, tracks, and repeated handoffs.

## Roles and models

- Lead: holds user context, writes contracts and briefs, makes decisions, verifies claims, and reports to the user.
- Teamlead: owns one large workstream or Herdr tab. Use only when the parent lead cannot drain that track itself.
- Explorer/planner: read-only. Prefer the cheapest capable model; include a local Qwen lane when useful and available.
- Implementer: one writer. Prefer Sol for complex or exact implementation. Use a cheaper model for small mechanical edits.
- Reviewer: fresh and read-only. Use Sol for technical correctness and Fable or Opus when product taste is the main risk.

Do not hard-code a model slug that the current harness cannot resolve. Follow the current `AGENTS.md` model table.

## Herdr

When `HERDR_ENV=1`, load the `herdr` skill and follow it for every delegated agent's full lifecycle.

- Give each workstream its own named tab when the work is large enough to need a teamlead.
- Keep all agents for that workstream inside that tab.
- Start Pi as a persistent interactive process. Never use one-shot `pi -p` delegation.
- Parse pane IDs from create or split responses. Never guess or reuse a stale ID.
- Confirm startup, then confirm the agent moved to working before waiting for completion.
- Use Herdr's event-driven status tools and inspect blocked agents promptly.
- Keep the same implementer and reviewer panes for fix and re-review loops.
- Do not close panes until follow-ups are unlikely.

When `HERDR_ENV` is absent, do not inspect or control Herdr. Use the current harness's native subagent tools only when
they are available and the user authorized delegation.

## Ownership and safety

- One writer per file set and one writer per worktree or branch.
- Preserve user changes and unrelated dirty files.
- Do not let workers spawn their own agents unless their brief grants that role.
- Runtime state is observation, not semantic task state. `idle` never means complete.
- The lead decides whether a report proves completion.
- Human approval stays human. Agents may request it but not grant it.

## Product and UI work

Product taste stays with the user and lead. Use human screenshots and focused feedback when that costs less than a
large automated visual loop. Agents may build narrow repro tools, but they should not spend tokens running broad UI
suites when a short human check is the better test.
