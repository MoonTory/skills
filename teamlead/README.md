# Teamlead skills

This collection adapts the parts of Cursor's pstack plugin that match Gustavo's working style:

- plan with a lead before agents start;
- give every agent a complete, bounded brief;
- use separate exploration, implementation, and review roles;
- route work by model strength;
- keep one workstream per Herdr tab and one writer per worktree;
- let the lead monitor, steer, stop, or replace workers;
- verify agent claims against the source and the real product;
- keep enough durable state to survive compaction or a new lead session.

The collection is called `teamlead` because that is the existing name for this workflow. It is deliberately smaller
than pstack. It keeps the workflow, review, recall, and coordination skills and leaves out its prose, code-style,
vendor-specific automation, and broad principle catalog.

## Skills

| Skill | Use |
| --- | --- |
| `teamlead-mode` | Routes a task to the smallest fitting workflow. |
| `ticket-flow` | Explore, plan, implement, verify, and review a bug or feature. |
| `explore` | Build a traced model of a subsystem before deciding. |
| `architect` | Compare concrete API and module shapes before implementation. |
| `arena` | Run several isolated attempts, choose a base, and combine the best parts. |
| `swarm` | Split independent coverage across workers and return one report. |
| `adversarial-review` | Run diverse reviewers, then let the lead judge each finding. |
| `orchestrate` | Run a long program with briefs, a durable queue, gates, and a verification ledger. |
| `custom-workflow` | Design a task-specific workflow when the standard flows do not fit. |
| `recall` | Rebuild current context from scoped recent transcripts and live state. |
| `pause-safely` | Write a durable checkpoint before compaction, restart, or a handoff. |
| `session-pickup` | Resume from a transcript, checkpoint, branch, or prior lead. |
| `decision-log` | Keep a small evidence-backed decision trail. |
| `reflect` | Review a completed run for changes worth encoding in skills or tools. |
| `capture-workflow` | Mine recent sessions and create or update a personal workflow skill. |

## Installation

Keep this directory grouped in the source repo. Each direct child with a `SKILL.md` is one self-contained skill, so
the CLI can copy any selected skill without relying on files from a sibling or parent directory.

The Skills CLI does not find this collection when it scans the repository root because it does not recurse through
arbitrary grouping folders. Point it at `teamlead` as the source instead:

```sh
# From the root of the local skills repository
npx skills add ./teamlead --list
npx skills add ./teamlead --skill '*' --agent claude-code --global

# From GitHub, after this collection has been committed and pushed
npx skills add https://github.com/MoonTory/skills/tree/master/teamlead --list
npx skills add https://github.com/MoonTory/skills/tree/master/teamlead --skill '*' --agent claude-code --global
```

The full GitHub URL with `/tree/master/teamlead` is the documented subpath form. Do not use the ambiguous
`MoonTory/skills/teamlead` shorthand.

The skills expect the existing `herdr` skill when `HERDR_ENV=1`. Outside Herdr they may use the current harness's
native subagent tools, but they must never pretend they can control Herdr panes.

## Trial

Use `teamlead-mode` explicitly on a few real tasks first. The prompts in `evals/evals.json` cover the main routing
decisions. Record whether each run saved time, caught a defect, added needless work, or needed human steering. Those
results are more useful to Hob than a synthetic benchmark.

## Upstream

See [UPSTREAM.md](UPSTREAM.md). The adapted source remains under pstack's MIT license in [LICENSE](LICENSE).
