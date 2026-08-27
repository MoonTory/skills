# Upstream mapping

- Source: https://github.com/cursor/plugins/tree/main/pstack
- Source commit: `fd6dd6f7276956a532bb78a748a8d2818b6eb5f4`
- pstack plugin version: `0.14.1`
- License: MIT, copyright Lauren Tan
- Port date: 2026-08-20

## Adapted skills

| Teamlead | pstack source |
| --- | --- |
| `orchestrator` | `poteto-mode` routing and selected playbooks, plus the local coordinator authority boundary |
| `ticket-flow` | bug-fix, feature, refactoring, and the prior local `herdr-teamlead` flow |
| `explore` | terminal read-only role adapted from `how` |
| `plan` | local terminal planning role extracted from the architecture and ticket flows |
| `build` | local terminal implementation role extracted from the ticket flow |
| `review` | local terminal review role extracted from `interrogate` |
| `architect` | `architect` |
| `arena` | `arena` |
| `swarm` | `swarm` |
| `adversarial-review` | `interrogate` |
| `orchestrate` | `poteto-mode/playbooks/orchestrate` and its `orch` store |
| `custom-workflow` | `figure-it-out` |
| `recall` | `recall` |
| `pause-safely` | `poteto-mode/playbooks/pause-safely` |
| `session-pickup` | `poteto-mode/playbooks/session-pickup` |
| `decision-log` | `show-me-your-work` |
| `reflect` | `reflect` |
| `capture-workflow` | `automate-me` |

## Main adaptations

- Cursor `Task` and cloud-agent assumptions became coordinator-only, harness-neutral delegation rules.
- Terminal Explorer, Planner, Builder, and Reviewer skills cannot spawn or delegate; coordinator skills are installed
  separately as a capability boundary.
- Exact model IDs and process lifecycle rules live in the active harness skill rather than Teamlead.
- pstack names became the terms already used here: teamlead, explore, plan, implement, review, brief, and contract.
- transcript discovery covers Claude, Pi, and Codex and always stays within the user-approved workspace and time range.
- human product and visual review is a first-class gate when taste matters.
- the lead may steer or replace a worker, but does not infer task completion from an idle process.
- the full principle catalog and unrelated playbooks were not copied.
