# Teamlead skills

This collection separates coordination authority from terminal worker roles. Install skills by role so a focused
worker cannot discover a coordinator workflow and start delegating on its own.

## Coordinator skills

These belong only in a Lead, Teamlead, or Orchestrator profile.

| Skill | Use |
| --- | --- |
| `orchestrator` | Authority gate, shared conventions, brief contract, and flow routing. Required by every coordinator flow. |
| `ticket-flow` | Run a bounded change through exploration, planning, implementation, verification, and review. |
| `architect` | Compare concrete API and module shapes before implementation. |
| `arena` | Run isolated attempts at one artifact, choose a base, and combine the best parts. |
| `swarm` | Split independent coverage across terminal workers and return one report. |
| `adversarial-review` | Run several terminal Reviewers, then let the lead judge each finding. |
| `orchestrate` | Run a long program with briefs, durable state, gates, and a verification ledger. |
| `custom-workflow` | Design a task-specific workflow when the standard flows do not fit. |

The coordinator may also install `recall`, `pause-safely`, `session-pickup`, `decision-log`, `reflect`, and
`capture-workflow` when it needs those utilities.

## Terminal role skills

Install only the role a worker needs. Each role works directly and must return scope problems to its caller instead
of spawning or delegating.

| Skill | Access | Deliverable |
| --- | --- | --- |
| `explore` | Read-only | Traced facts and source evidence. |
| `plan` | Read-only | One bounded implementation contract. |
| `build` | Assigned write scope | Implementation and validation evidence. |
| `review` | Read-only | Findings and a verdict. |

Do not install `orchestrator`, coordinator flow skills, or `herdr` in a terminal worker profile. Running inside a
Herdr pane does not make a worker a coordinator.

## Shared policy

Coordinator skills load the one conventions file and brief template inside `orchestrator`. Terminal roles stay
self-contained and intentionally repeat only the short no-delegation safety gate. There are no copied convention or
brief files to keep in sync.

Herdr owns pane, tab, process, model-ID, and agent lifecycle mechanics. Teamlead owns roles, task structure, briefs,
evidence, and judgment. Exact model names and launch commands do not live in Teamlead.

## Installation

Point the Skills CLI at this directory because the repository scanner does not recurse through arbitrary grouping
folders:

```sh
npx skills add ./teamlead --list
```

For a full coordinator profile, select `orchestrator`, the desired coordinator flows and utilities, and the four
terminal role skills it may assign. Install the separate `herdr` skill only in coordinator profiles that run inside
Herdr.

For a worker profile, select only `explore`, `plan`, `build`, or `review` as required. Add any task-specific
integration skills separately; they do not grant delegation authority.

From GitHub, use the full collection path:

```sh
npx skills add https://github.com/MoonTory/skills/tree/master/teamlead --list
```

## Trial

Test one coordinator ticket flow and one prompt-injection case per terminal role before broad use. The evals verify
that leaked repository mentions and visible orchestration tools do not turn a terminal worker into a coordinator.

## Upstream

See [UPSTREAM.md](UPSTREAM.md). The adapted source remains under pstack's MIT license in [LICENSE](LICENSE).
