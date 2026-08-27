---
name: linear-teamlead
description: Connect a Teamlead engineering workflow to Linear when a project uses both and the run is tied to a Linear issue. Use for Teamlead ticket flows, planning, implementation, review, pause, resume, or long orchestration that must publish role evidence through separate Linear profiles. Do not use for Teamlead work without Linear or ordinary Linear updates without a Teamlead workflow.
---

# Linear with Teamlead

Compose the two workflows without copying either one. Read the installed `linear` skill and the selected Teamlead
skill before starting. The Linear skill owns identity, issue contracts, artifacts, comments, metadata, and status.
The Teamlead skill owns execution, delegation, synthesis, verification, and review mechanics.

This bridge never grants coordination or delegation authority. An Orchestrator may load the `orchestrator` skill and
coordinator flows. A terminal Explorer, Planner, Builder, or Reviewer loads only its matching terminal role skill and
must not load Herdr or coordinator skills.

Use this bridge only when repository instructions opt into Linear and the work is tied to a real Linear issue. If
either required skill is unavailable, name the missing dependency and stop the integrated workflow rather than
guessing its contract.

## Add tracker context at the boundary

Do not add Linear fields to generic Teamlead brief templates. When a role brief belongs to a Linear-backed phase,
append only the integration context that role needs:

```text
LINEAR ISSUE   Resolved issue ID and title.
LINEAR ROLE    Planner, Builder, Reviewer, or Orchestrator.
PROFILE        Matching configured Linear profile; never include credentials.
PUBLISH        Evidence the role must publish before returning its handoff.
```

Before any write, the role verifies the authenticated Linear actor through its matching profile. A mismatch blocks
publication. Planner, Builder, and Reviewer publish only their own evidence; they do not change issue metadata or
status. Orchestrator does not republish another role's work under its own identity.

## Complete each phase at its boundary

| Role | Before returning its handoff |
| --- | --- |
| Planner | Publish the planning artifact required by the Linear skill and the Plan ready comment. |
| Builder | Publish the concise Builder handoff with validation that actually ran, deviations, and next role. |
| Reviewer | Publish the Review artifact when required and the current pass or reject verdict. |
| Orchestrator | Read the role's publication back, then apply the allowed delegation, metadata, and status changes. |

Publish during each phase transition. Never defer all Linear updates until the workflow ends. A Teamlead worker or
panel may produce internal findings, but the assigned workflow role publishes the consolidated phase evidence.

## Keep internal state internal

Unit keys, worker IDs, model names, pane or tab IDs, batch names, wave names, and context telemetry may exist in
scratch state. Do not put them in Linear, issue or artifact titles, commits, or user reports. Use the real issue ID
and describe work by scope and outcome.

Keep temporary briefs, handoffs, checkpoints, and unpublished evidence in harness state or a scratch directory
outside the repository. When Linear is unavailable, preserve that temporary evidence and report the blocked
publication. Do not advance a Linear-dependent transition or create, revive, or update a Markdown ticket ledger as
a fallback.
