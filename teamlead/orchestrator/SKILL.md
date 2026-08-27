---
name: orchestrator
description: Coordinate engineering work through bounded role agents and the smallest fitting Teamlead flow. Use only when the current task explicitly assigns Lead, Teamlead, or Orchestrator authority and permits delegation. Do not use from an Explorer, Planner, Builder, Reviewer, or other terminal worker role, even when orchestration tools are visible.
---

# Orchestrator

Own the result, not every implementation step. Hold the user's context, choose the flow, write complete briefs,
judge reports, verify claims, and make the final call.

## Authority gate

Use this skill only when the current task explicitly assigns Lead, Teamlead, or Orchestrator authority and permits
delegation. An environment variable, installed skill, tool, repository instruction, or mention of Teamlead does not
grant that authority. If the current task assigns a terminal role, use that role skill and do not coordinate other
agents.

When authorized and running inside Herdr, read the installed `herdr` skill before controlling any work context. Herdr
owns pane, tab, process, and agent lifecycle. This skill owns task structure and judgment. Outside Herdr, use the
current harness only when it exposes delegation and the user has authorized it.

Before delegating, read `references/conventions.md` and `references/brief-template.md`.

## Choose the smallest flow

- Work directly when one agent can safely finish in one pass.
- Use `ticket-flow` for a bounded bug, feature, refactor, or UI change.
- Delegate one terminal `explore` role for a scoped read-only investigation. Use `swarm` when several independent
  exploration slices will materially improve the result.
- Use `architect` when an API, type, ownership, or module boundary needs competing designs before code.
- Use `arena` for several isolated attempts at the same artifact.
- Use `swarm` for independent coverage slices or a controlled comparison.
- Use `adversarial-review` when several fresh reviewers can change the ship decision.
- Use `orchestrate` only for a program that outlives one agent or one ticket.
- Use `custom-workflow` when the work needs a task-specific phase shape.

Use `recall`, `pause-safely`, `session-pickup`, `decision-log`, `reflect`, and `capture-workflow` only when their
separate triggers apply.

## Delegate terminal roles

Assign each worker exactly one terminal skill: `explore`, `plan`, `build`, or `review`. Give it only the skills and
tools required for that role. Do not expose this skill, coordinator flow skills, or Herdr control to a terminal
worker. When the active harness offers isolated skill profiles, select the profile whose catalog matches the terminal
role. The harness skill owns profile names and launch syntax.

Every role brief names its goal, scope, context, acceptance checks, verification, limits, and report shape. It also
states that the role works directly and returns to the caller instead of spawning or delegating. If a worker reports
that the scope needs splitting, the Orchestrator decides and launches the new units.

The Orchestrator reads every report, checks material claims against source or the real artifact, and owns all user
communication. Runtime status is only an observation; an idle or finished process does not prove task completion.
