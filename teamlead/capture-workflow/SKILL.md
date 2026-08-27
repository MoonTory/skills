---
name: capture-workflow
description: Mine an approved slice of recent Claude, Pi, and Codex sessions to create or update a personal workflow skill. Use for "capture how I work", "update my mode", "learn from my sessions", or turning repeated teamlead corrections and habits into durable instructions.
---

# Capture workflow

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

This skill mines evidence, clusters durable rules, and then uses the available `skill-creator` workflow to draft and
test the result.

## Flow

### 0. Check for an existing skill

Look in the current repository's skill roots and the user's personal skill roots, including `~/code/skills`,
`~/.agents/skills`, `~/.claude/skills`, and `~/.codex/skills`, but only where the user has granted access. If a matching
mode exists, update it by default when the user asked for an update; otherwise confirm before replacing it.

- Update the existing skill (default for repeat runs)
- Start fresh (rare; ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted; revise ones with new evidence; add new sections only for genuinely new rules.

### 1. Mine their history

Lock the workspace, harness roots, topic, and time range before searching. Common roots are `~/.claude/projects`,
`~/.pi/agent/sessions`, and `~/.codex/sessions`. Do not read any of them without user permission. Within approved
roots, identify sessions by current working directory and content rather than UUID names.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Each slice mining subagent reads transcripts from the workspace-scoped path the parent provides, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means; unit tests vs live repro; reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence; lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use the `AskQuestion` tool (structured multi-choice) rather than asking the user to type from scratch. Lower cognitive load, higher hit rate.

Shape: one or two questions with 4-6 options each, `allow_multiple: true` for category questions. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions. Two structured rounds plus one open question is usually enough.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking; MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

Use `orchestrator` as one example of granularity. Do not copy its rules into a personal mode unless the transcripts
and user confirm them.

### 4. Draft the skill

Use the available `skill-creator` workflow to author the skill. Placement:

- Path: preserve an existing mode skill's category. For a new shared source skill, prefer the user's skills repository
  and its grouping conventions. Installation into harness-specific roots is a separate, explicit step.
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name + `/<handle>-mode` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow `skill-creator`'s YAML rules.
- Make heavy personal modes explicit-only when the target harness supports that setting. Enable automatic triggering
  only when the user wants the mode on every matching task.

### 5. Iterate on prose

Apply the repository's communication rules and `skill-creator` writing guidance to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly; a mode skill is not a manual.

### 6. Land it

Follow the target repository's git instructions. Do not commit, push, or open a PR unless the user asked.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name. Others may read or adopt the skill.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely. Sparse is fine; bloated is not.

## Evaluation

A mode skill is subjective. Review the draft with the user first. Run small routing or behavior tests when they can
catch a real error, but do not burn a large benchmark merely to produce a score.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill rather than working conventions: use `skill-creator` without transcript mining.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"): that's a regular skill, not a mode skill.

## Reference files

- `orchestrator`: one example of the output shape.
- `skill-creator`: the authoring, test, and iteration process.
