# Upstream mapping

- Source: https://github.com/cursor/plugins/tree/main/pstack
- Source commit: `fd6dd6f7276956a532bb78a748a8d2818b6eb5f4`
- pstack plugin version: `0.14.1`
- License: MIT, copyright Lauren Tan
- Port date: 2026-08-20

## Adapted skills

| Teamlead | pstack source |
| --- | --- |
| `teamlead-mode` | `poteto-mode` routing and selected playbooks |
| `ticket-flow` | bug-fix, feature, refactoring, and the prior local `herdr-teamlead` flow |
| `explore` | `how` |
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

- Cursor `Task` and cloud-agent assumptions became harness-neutral delegation rules with a Herdr/Pi path.
- pstack model defaults became the user's lead, implementation, exploration, and review roles.
- pstack names became the terms already used here: teamlead, explore, plan, implement, review, brief, and contract.
- transcript discovery covers Claude, Pi, and Codex and always stays within the user-approved workspace and time range.
- human product and visual review is a first-class gate when taste matters.
- the lead may steer or replace a worker, but does not infer task completion from an idle process.
- the full principle catalog and unrelated playbooks were not copied.
