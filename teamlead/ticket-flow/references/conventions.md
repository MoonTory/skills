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
- Explorer/planner: read-only. Always add a local Qwen lane beside every explorer and planner fan-out
  (`pi --model local5080/qwen/qwen3.8-27b --thinking low --tools read,grep,find,ls`; free; never let it
  run at its default xhigh thinking — it is slow and verbose). Qwen rules: a hyper-specific
  brief (exact files, exact question, findings-only output), read-only tools only, never paste a diff into its
  prompt or ask it to echo files, at most two Qwen panes live, read its report from the pane.
- Implementer: one writer with exclusive scope.
- Reviewer: fresh and read-only, with no stake in the implementation.

Rankings are defaults, not benchmarks; higher is better. Cost measures affordability and value. Intelligence is how
hard a problem the model can handle without help. Taste covers UI, code quality, API design, and copy.

| Model | Cost | Intelligence | Taste |
| --- | ---: | ---: | ---: |
| `gpt-5.6-luna` | 9 | 5 | 6 |
| `gpt-5.6-terra` | 7 | 7 | 7 |
| `gpt-5.6-sol` | 5 | 9 | 8 |
| `opus-4.8` | 4 | 7 | 8 |
| `fable-5` | 1.5 | 9 | 9 |

- Start with the cheapest model that comfortably fits the task. If its output misses the bar, rerun or continue
  with the next tier. Judge the output, not the price tag.
- Cost breaks ties. For work that ships, intelligence matters more than taste, and taste more than cost.
- Use Luna for clear bulk or mechanical work: small edits, migrations, cleanup, docs, test scaffolding, and first-pass
  investigation.
- Use Terra as the default Pi model for everyday implementation, debugging, research, and data analysis.
- Use Sol for complex or ambiguous work, architecture, cross-cutting changes, difficult debugging, and technical
  review.
- Use Fable or Opus when product taste is the main risk. Anything user-facing needs taste of at least 7.
- Every review fan-out includes a local Qwen reviewer beside the primary reviewers; Luna or Terra can join as
  a further cheap view. On security reviews Qwen joins but never replaces Opus.
- Never use Haiku.

The exact Pi command and provider-qualified model ID belong to the installed `herdr` skill. Do not rely on Pi's
global default when a brief assigns a model. If the current harness cannot resolve a listed model, use the current
`AGENTS.md` model table rather than guessing another ID.

## Herdr

When `HERDR_ENV=1`, load the `herdr` skill and follow it for every delegated agent's full lifecycle.

- Before the first delegated agent in a Teamlead workflow, create one new named tab for the task. Do this even for a
  small ticket when the lead delegates implementation or review. Skip the tab only when the lead delegates nothing,
  or when the user explicitly says to reuse an existing task tab.
- Derive a short, stable label from the work: a ticket ID plus subject when available, otherwise a two-to-five-word
  task name such as `settings form` or `auth refresh`. Do not name tabs after phases or roles such as `explore`,
  `review`, or `agent 1`.
- Parse and retain the tab ID and root-pane ID from the create response. Start the first agent in that root pane.
- Split every later explorer, implementer, and reviewer from a pane in the task tab. Reuse the same tab through
  exploration, implementation, fixes, review, and re-review. Do not create one tab per phase or agent, and do not put
  workflow workers in the lead's original tab.
- For `orchestrate`, a real independent track may receive its own named tab. Keep its teamlead and workers there.
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
