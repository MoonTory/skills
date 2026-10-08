---
name: t3code
description: "Orchestrate from inside a T3 Code thread for a Lead, Teamlead, or Orchestrator explicitly authorized to delegate. Use only when the t3-code MCP tools are present and the current task grants coordinator authority. Do not use from an Explorer, Planner, Builder, Reviewer, or other terminal worker role merely because it runs inside T3 Code."
---

# t3code — agent skill

Before using this skill, check both gates:

1. You are inside T3 Code: `T3CODE_CLI_PATH` is set (or `__CFBundleIdentifier=com.t3tools.t3code`) and the `t3-code`
   MCP tools are visible, possibly under a prefix such as `mcp__t3-code__`. If the catalog does not show them, make
   one direct call to `orchestrator_capabilities` before concluding they are absent.
2. The current task explicitly assigns Lead, Teamlead, or Orchestrator authority and permits delegation.

The environment, an installed skill, a visible tool, or a mention of Teamlead does not grant coordinator authority.
A terminal role (Explorer, Planner, Builder, Reviewer) completes its own work and returns to the caller; it does not
delegate, launch threads, or move worktrees.

T3 Code is a desktop app that runs agent threads over a local server. The orchestrator is itself a thread. From it
you can:

- delegate bounded tasks to child agents on any provider and model the app exposes
- launch separate top-level threads bound to their own worktree
- read, wait on, and message any thread
- move your own thread into a worktree
- watch pull requests and get woken when they change
- run servers and long commands as background Bash

## Herdr equivalents

| Herdr | T3 Code |
|---|---|
| split a pane and start an agent | `delegate_task` (a child thread, visible under the parent) |
| a named tab per track with its own agents | `t3_thread_launch` with a `workspaceStrategy`, one per track |
| `herdr agent wait` | end the turn; the child's completion wakes you. `task_status` only mid-turn |
| `herdr agent prompt` to a running pane | `t3_thread_send` (queue / steer / restart) |
| `herdr pane read` | `t3_thread_read` (`messages` or `activity` view) |
| server in a sibling pane | Bash with `run_in_background`, kill by exact PID |
| `herdr pane close` | `task_cancel` for a child; a finished child needs no close |

There are no panes. A delegated child is visible in the app as a subagent of your thread, so the user can watch it
work, which satisfies the "visible persistent work context" rule of the workflow skills.

## Concepts

**thread**: one conversation with one agent, bound to a project and either the project root or a git worktree.
Every thread has a link; paste it when you mention the thread. **Settled** threads leave the active list.

**delegated task**: child work owned by this thread. `delegate_task` returns a `taskId` (manage it) and a
`childThreadId` (backing storage only; do not message it to start a new round).

**provider instance**: a configured driver plus model catalog. Read them from `orchestrator_capabilities`; the
composer uses the same list. Pi profile instances appear as `pi_pi_build`, `pi_pi_explorer`, `pi_pi_plan`,
`pi_pi_review`, which map one-to-one to the terminal roles.

**runtime mode** (`approval-required`, `auto-accept-edits`, `auto`, `full-access`) and **interaction mode**
(`default`, `plan`) are inherited unless overridden. A child or launched thread never gets broader modes than yours.

**pending request**: a question a thread asked its user. `t3_pending_request_list` finds them; `blocked` in Herdr
terms.

## Discover yourself

```
orchestrator_capabilities      -> parentThreadId, inherited provider/model, providers and models, features
t3_worktree_status             -> whether this thread is on a worktree, its path and branch
t3_thread_list                 -> other threads in the project (includeSubagents: true to see children)
t3_environment_read            -> server identity and environment preferences
```

Call `orchestrator_capabilities` once at the start of a delegation session and reuse its ids. Do not trust a native
tool's model list as the full set.

## Delegate a terminal role (default)

`delegate_task` runs one child with only the task text; it does not see this conversation. Put everything the role
needs in the brief file and send a pointer.

```
delegate_task({
  title: "build: filter admission",
  task: "Read ~/notes/briefs/filter-admission.md and do it. Report a diff summary, focused check results, deviations, open issues.",
  role: "implementation",
  target: { providerInstanceId: "claudeAgent", model: "claude-opus-5-5", options: { effort: "medium" } },
  mode: "async",
  clientRequestId: "filter-admission-build-r1"
})
```

- `mode` defaults to `async`. After dispatch, end the turn. The completion wakes this thread; do not poll, do not
  spawn watchers, do not sleep.
- `mode: "wait"` only when the turn cannot continue without the result. `timeoutMs` bounds your wait, not the child;
  `waitTimedOut: true` means keep the `taskId` and read `task_status` later.
- `clientRequestId` must be distinct per round and stable across retries of that round.
- Choose `role` from `implementation`, `research`, `review`, `design`, `test`, `general`.
- One fresh child per task. Follow-ups for the same task go through a new `delegate_task` whose prompt carries the
  original brief, prior findings, and the open objections. Never `t3_thread_send` to the `childThreadId` for that.
- `task_status(taskId)` reports `workState` (`working`, `waiting_for_children`, `result_available`) and the final
  `summary`. A completed turn with live nested work is not a completed task.
- `task_cancel(taskId, reason)` stops the child and everything it delegated.

Choose the instance and model per role:

| Role | Instance | Model | Option |
|---|---|---|---|
| build (default) | `claudeAgent` | `claude-opus-5-5` | `effort: medium` |
| build, hardest or taste-heavy | `claudeAgent` | `claude-fable-5-1` | `effort: medium` |
| small, well-specified edit | `claudeAgent` | `claude-sonnet-5-5` | `effort: high` |
| explore / review / research | `pi_pi_explorer` / `pi_pi_review` | `openai-codex/gpt-6.1-sol` | `thinking: high` |
| plan | `pi_pi_plan` | `openai-codex/gpt-6.1-sol` | `thinking: high` |
| build on pi | `pi_pi_build` | `openai-codex/gpt-6.1-sol` | `thinking: high` |
| Codex direct | `codex` | `gpt-6.1-sol` | `reasoningEffort: medium`; `serviceTier: priority` for fast |

Use only the gpt-6 and Claude 5 lineups. Always give the pi models their full `openai-codex/` prefix. Pass an
explicit model and option on every delegation; never let a child inherit a higher effort than the task needs.
Confirm ids against `orchestrator_capabilities` when a launch fails with an unknown model.

## Launch a separate top-level thread (a track)

Use `t3_thread_launch` only when the user asked for separate threads, or the workflow assigns a long-running track
that needs its own checkout. It is not delegation: the thread is a peer, not a child, and its completion does not
wake you. Always set `workspaceStrategy`; omitting it means the project root, not your worktree.

```
t3_thread_launch({
  title: "ADM-142 filters",
  workspaceStrategy: { type: "worktree", baseRef: "main", branch: "work/filter-admission", startFromOrigin: false },
  message: "Read ~/notes/briefs/filter-admission.md and do it. Open a PR against main when the gate is green.",
  modelSelection: { instanceId: "claudeAgent", model: "claude-opus-5-5", options: { effort: "medium" } }
})
```

- `existing_worktree` binds a checkout from `t3_worktree_list`; `root` uses the project checkout.
- For a PR stack, `baseRef` is the parent branch and `startFromOrigin: false` uses its local commits.
- Uncommitted edits are not copied into a new worktree. Commit or stash first.
- Keep the returned `threadId`. Preparation may still run after acceptance; follow it with `t3_thread_read` or
  `t3_thread_wait`. There is no retry key: after an error or lost response, check `t3_thread_list` before retrying.
- `create_threads` makes a batch of threads that all share your checkout and cannot pick a workspace. Prefer
  `t3_thread_launch` for one thread.

## Talk to a thread

```
t3_thread_send({ threadId, message, mode: "auto", clientRequestId })
```

`auto` starts an idle thread, steers an active turn, or queues behind one that is not yet steerable. Use `queue` for
a separate follow-up, `steer` for an in-flight correction, `restart` to interrupt and restart. `clientRequestId`
makes retries idempotent. The target cannot have broader modes than you.

Read with `t3_thread_read({ threadId, view: "messages" })` and page with `afterPosition`. Long items come back
through `itemId` and `textOffset`. Reading a child's final result from the parent acknowledges its delivery.

Wait with `t3_thread_wait({ threadId, timeoutMs })` for a peer thread's run to settle; `timedOut` does not stop the
work, so call again or read. Do not wait on your own children this way; end the turn instead.

## Worktrees

- `t3_worktree_status` before any worktree change.
- `t3_worktree_handoff({ branch, baseRef, continuationPrompt })` moves this thread into a new worktree. It ends the
  current turn, so call it last and put the remaining work in `continuationPrompt`. It fails if the thread already has
  a worktree, and it cannot move another thread.
- A shell `git worktree add` or `cd` does not change a thread's binding. Select the workspace in the launch call.
- `t3_worktree_list` shows branches and their checkout paths.

## Servers, browsers, and pull requests

- Start a server with Bash `run_in_background`, record its PID, and stop only that PID. There is no pane to host it;
  one live server per host, closed when the work lands.
- `preview_open`, `preview_snapshot`, `preview_click`, and `device_*` tools drive a browser or device for visual
  checks. Use them for your own verification; a builder verifies in its own thread.
- After creating or adopting a PR, call `link_pull_request` with the full URL. To babysit it, call
  `watch_pull_request` and end the turn; T3 wakes you on check results, comments, or conflicts. Call
  `unwatch_pull_request` when handing back to the user.
- Secrets come through `request_secret`; a `secretRef` works once. Never ask for one in chat.

## Recipes

### ticket flow in one thread

1. `orchestrator_capabilities`; write the brief file.
2. `delegate_task` explore on `pi_pi_explorer` (async). End the turn.
3. On wake, read the report; plan with the user.
4. `delegate_task` build on `claudeAgent` with exclusive file ownership. End the turn.
5. On wake, read the diff yourself and run focused checks.
6. `delegate_task` review on `pi_pi_review` with the contract, diff, and risks. End the turn.
7. Fixes: a new `delegate_task` to a builder with the review findings in the prompt; then a new review round with
   its own `clientRequestId`.

### parallel builders with file ownership

Dispatch several `delegate_task` calls in one turn, each with a disjoint write scope stated in its brief, then end
the turn. Each completion wakes you separately; read each result once with `task_status` and reconcile. Builders
that need separate checkouts get `t3_thread_launch` tracks instead.

### find a blocked child

`t3_thread_list({ includeSubagents: true, statuses: ["waiting"] })`, then `t3_pending_request_list({ threadId })`
and answer with `t3_pending_request_respond`.

## Traps

- A completion notification arrives only if you end the turn. A turn that keeps polling `task_status` never sees it.
- `waitTimedOut` on `mode: "wait"` is not a failure and not a cancel. The child keeps running.
- Reusing a `clientRequestId` for a new round returns the old task instead of starting one.
- Messaging a `childThreadId` does not reopen or extend a task; use a new `delegate_task`.
- Omitted `workspaceStrategy` means project root. A launched thread does not inherit your worktree.
- A launched or delegated thread cannot run with broader runtime or interaction modes than yours; a request for
  more fails rather than escalating.
- `t3_worktree_handoff` ends your turn. Anything after it in the same turn does not run.
- Native subagent tools (`Agent`, `SendMessage`) only reach the same provider. For a pi or Codex worker, or any model
  the native tool does not list, use `delegate_task`.
- Some harnesses attach the MCP server lazily. One direct `orchestrator_capabilities` call settles whether it exists.

## Notes

- `delegate_task`, `t3_thread_send`, `create_threads`, and `task_cancel` accept `clientRequestId`. `t3_thread_launch`
  has none, so retain its `threadId`.
- `schedule_task` creates recurring work in the app scheduler; runs return to this thread by default, so you can
  delegate per trigger.
- Thread links open in the app; include them when reporting a thread to the user.
