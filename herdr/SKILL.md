---
name: herdr
description: "Control herdr from inside it. Manage workspaces and tabs, split panes, spawn agents, read output, and wait for state changes — all via CLI commands that talk to the running herdr instance over a local unix socket. Use when running inside herdr (HERDR_ENV=1)."
---

# herdr — agent skill

before using this skill, check that `HERDR_ENV=1`. if it is not set to `1`, say you are not running inside a herdr-managed pane and stop. do not inspect or control the focused herdr pane from outside herdr.

you are running inside herdr, a terminal-native agent multiplexer. herdr gives you workspaces, tabs, and panes — each pane is a real terminal with its own shell, agent, server, or log stream — and you can control all of it from the cli.

this means you can:

- see what other panes and agents are doing
- create tabs for separate subcontexts inside one workspace
- split panes and run commands in them
- start servers, watch logs, and run tests in sibling panes
- wait for specific output before continuing
- wait for another agent to finish
- spawn more agent instances

the `herdr` binary is available in your PATH. its workspace, tab, pane, and wait commands talk to the running herdr instance over a local unix socket.

if you need the raw protocol or full api reference, read the [socket api docs](https://herdr.dev/docs/socket-api/).

## concepts

**workspaces** are project contexts. each workspace has one or more tabs. unless manually renamed, a workspace's label follows the first tab's root pane — usually the repo name, otherwise the root pane's current folder name.

**tabs** are subcontexts inside a workspace. each tab has one or more panes.

**panes** are terminal splits inside a tab. each pane runs its own process — a shell, an agent, a server, anything.

**agent status** is detected automatically by herdr. the api exposes one public field for it:

- `agent_status` — `idle`, `working`, `blocked`, `done`, `unknown`

`done` means the agent finished, but you have not looked at that finished pane yet.

plain shells still exist as panes, but herdr's sidebar agent section intentionally focuses on detected agents rather than listing every shell.

**ids** — workspace ids look like `1`, `2`. tab ids look like `1:1`, `1:2`, `2:1`. pane ids look like `1-1`, `1-2`, `2-1`. these are compact public ids for the current live session.

important: ids can compact when tabs, panes, or workspaces are closed. do not treat them as durable ids. re-read ids from `workspace list`, `tab list`, `pane list`, or create/split responses when you need a current id. do not guess that an older `1-3` is still the same pane later.

## discover yourself

see what panes exist and which one is focused:

```bash
herdr pane list
```

the focused pane is yours. other panes are your neighbors.

list workspaces:

```bash
herdr workspace list
```

## tab management

list tabs in the current workspace:

```bash
herdr tab list --workspace 1
```

create a new tab:

```bash
herdr tab create --workspace 1
```

without `--label`, the new tab keeps the default numbered tab name.

create and name it in one step:

```bash
herdr tab create --workspace 1 --label "logs"
```

rename it:

```bash
herdr tab rename 1:2 "logs"
```

focus it:

```bash
herdr tab focus 1:2
```

close it:

```bash
herdr tab close 1:2
```

## read another pane

see what is on another pane's screen:

```bash
herdr pane read 1-1 --source recent --lines 50
```

- `--source visible` = current viewport
- `--source recent` = recent scrollback as rendered in the pane
- `--source recent-unwrapped` = recent terminal text with soft wraps joined back together

## create a pane or tab for new work

first decide whether the request calls for a **pane** or a **tab**:

- if the user explicitly asks for a new tab, create a tab; do not substitute a split pane. give it a short, descriptive `--label` based on the requested work (for example, `api tests` or `review auth`).
- a requested tab is the work context for that task: start every new agent for that task in its root pane or in panes split from it. do not place those agents in another tab unless the user requests a separate tab.
- otherwise, create a pane in the current tab when the work should remain visible alongside the current task (for example, a server, tests, or an agent to coordinate with).
- choose the split direction deliberately. use `down` for a short-lived command or log stream so the main pane retains width; use `right` only when a side-by-side layout is useful or the user requests it. do not default every split to `right`.

create a downward pane while retaining focus, parse its id, then run a command:

```bash
NEW_PANE=$(herdr pane split 1-2 --direction down --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "npm run dev"
```

for a requested new tab, create it in the current workspace with a short task-derived label, parse its root pane, and use that pane. add `--no-focus` unless the user asked to switch to the new tab (omit it when they did):

```bash
NEW_PANE=$(herdr tab create --workspace 1 --label "api tests" --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "npm run dev"
```

when that task needs additional agents, split `NEW_PANE` (or another pane in that same tab) and start `pi` in the resulting pane. keep all agents for the task in that tab.

## spawn a pi agent (always interactive)

always start pi as a persistent interactive process in its pane — run `pi` (optionally with `--model` and `--tools`) with no prompt argument, then send tasks to the pane. never use `pi -p "<prompt>"` or pass the task on the command line: one-shot mode exits after one response and may remove the pane, preventing follow-ups.

```bash
NEW_PANE=$(herdr pane split 1-2 --direction right --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')

# Omit --model unless you have verified that the model is configured and authenticated.
herdr pane run "$NEW_PANE" "pi --tools read,grep,find,ls"

# agent_status can become idle before the TUI is ready to accept submitted input.
# Wait for a startup marker as well as idle before sending the task.
herdr wait output "$NEW_PANE" --match "Pi can explain its own features" --timeout 15000
herdr wait agent-status "$NEW_PANE" --status idle --timeout 10000

herdr pane run "$NEW_PANE" "review the test coverage in src/api/ and report gaps"
herdr wait agent-status "$NEW_PANE" --status working --timeout 10000
```

`pane run` already sends Enter. do not send an extra Enter during the normal flow; it can submit an empty prompt or open a menu after an error. if the `working` confirmation times out, inspect `pane get` and `pane read` immediately. the prompt may still be in the editor because startup raced, or pi may be showing an authentication/configuration error. only send Enter after confirming that the intended prompt is visibly waiting in the editor.

then detect completion with the settle loop in "waiting for an agent to finish". after the agent responds, send every clarification or follow-up to the **same pane**. leave the interactive process open until likely follow-ups are complete.

## wait for output

block until specific text appears in a pane. useful for waiting on servers, builds, and tests.

for `--source recent`, matching uses unwrapped recent terminal text, so pane width and soft wrapping do not break matches. `pane read --source recent` still shows the pane as rendered. if you want to inspect the same transcript that the waiter matches, use `pane read --source recent-unwrapped`.

```bash
herdr wait output 1-3 --match "ready on port 3000" --timeout 30000
```

with regex:

```bash
herdr wait output 1-3 --match "server.*ready" --regex --timeout 30000
```

if it times out, exit code is `1`.

## wait for an agent status

block until another agent reaches a specific status:

```bash
herdr wait agent-status 1-1 --status done --timeout 60000
```

`wait agent-status` is event-driven: it returns the moment the pane hits the target status. the timeout is a ceiling for how long to keep listening, not a delay — a matching status change comes back instantly. it also returns instantly if the pane is *already* at the target status.

use this when you want the same `done` / `idle` distinction the UI shows.

### waiting for an agent to finish

do not pin a single long wait on `--status done`. `done` is transient — it means "finished and not yet viewed", and it flips to `idle` once the pane is looked at — and a `blocked` agent (asking you a question) never reaches `done` at all. a lone `wait --status done --timeout 600000` can therefore sit for the full timeout while the agent finished or blocked long ago.

instead, detect that the agent has **left `working`**. combine short chunked waits on `done` (instant when it fires) with `pane get` polls that also catch `idle` and `blocked`:

```bash
# after confirming the agent is working
DEADLINE=$(( $(date +%s) + 1800 ))
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  st=$(herdr pane get "$PANE" | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["pane"]["agent_status"])')
  [ "$st" != "working" ] && { echo "settled: $st"; exit 0; }
  herdr wait agent-status "$PANE" --status done --timeout 15000 >/dev/null 2>&1 && { echo "settled: done"; exit 0; }
done
echo timeout; exit 1
```

a `done` transition settles instantly via the wait; `idle` and `blocked` are caught within one 15s chunk. run this loop in the background when the current harness supports background commands. otherwise use short chunks and return to other work between checks; do not issue one long blocking wait.

interpret the settled status:

- `done` / `idle` → read the pane and continue the conversation
- `blocked` → the agent is asking for input: read the pane, answer with `pane run`, confirm it is `working` again, and restart the loop

## send text or keys to a pane

send text without pressing Enter:

```bash
herdr pane send-text 1-1 "hello from pi"
```

press Enter or other keys:

```bash
herdr pane send-keys 1-1 Enter
```

`pane run` sends the text and then a real `Enter` key in one request:

```bash
herdr pane run 1-1 "echo hello"
```

## workspace management

create a new workspace:

```bash
herdr workspace create --cwd /path/to/project
```

without `--label`, the new workspace keeps the default cwd-based name.

create and name one in one step:

```bash
herdr workspace create --cwd /path/to/project --label "api server"
```

create one without focusing it:

```bash
herdr workspace create --no-focus
```

focus a workspace:

```bash
herdr workspace focus 2
```

rename:

```bash
herdr workspace rename 1 "api server"
```

close:

```bash
herdr workspace close 2
```

## close a pane

```bash
herdr pane close 1-3
```

## recipes

### run a server and wait until it is ready

```bash
NEW_PANE=$(herdr pane split 1-2 --direction down --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "npm run dev"
herdr wait output "$NEW_PANE" --match "ready" --timeout 30000
herdr pane read "$NEW_PANE" --source recent --lines 20
```

### run tests in a separate pane and inspect the result

```bash
NEW_PANE=$(herdr pane split 1-2 --direction down --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "cargo test"
herdr wait output "$NEW_PANE" --match "test result" --timeout 60000
herdr pane read "$NEW_PANE" --source recent --lines 30
```

### check what another agent is working on

```bash
herdr pane list
herdr pane read 1-1 --source recent --lines 80
```

### watch another pane robustly

use this pattern when you need to coordinate with a sibling pane:

```bash
# inspect what is already there
herdr pane read 1-3 --source recent --lines 40

# wait only for the next output you expect
herdr wait output 1-3 --match "ready" --timeout 30000

# if you need to inspect the same transcript the waiter matched,
# read the unwrapped recent text directly
herdr pane read 1-3 --source recent-unwrapped --lines 40
```

### spawn a new agent and give it a task

start pi interactively (never `pi -p`) so the agent stays alive for follow-ups:

```bash
NEW_PANE=$(herdr pane split 1-2 --direction down --no-focus | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "pi --tools read,grep,find,ls"
herdr wait output "$NEW_PANE" --match "Pi can explain its own features" --timeout 15000
herdr wait agent-status "$NEW_PANE" --status idle --timeout 10000
herdr pane run "$NEW_PANE" "review the test coverage in src/api/"
herdr wait agent-status "$NEW_PANE" --status working --timeout 10000
```

### follow up with the same agent

wait for the agent to settle using the background loop from "waiting for an agent to finish" (never a single long `wait --status done`), then keep the conversation in the same pane instead of spawning a new agent:

```bash
# (settle loop from "waiting for an agent to finish" has exited)
herdr pane read "$NEW_PANE" --source recent-unwrapped --lines 100
herdr pane run "$NEW_PANE" "also check the integration tests in tests/api/"
herdr wait agent-status "$NEW_PANE" --status working --timeout 10000
# then start the settle loop again in the background
```

### coordinate with another agent

run the settle loop from "waiting for an agent to finish" in the background, then read the pane once it exits:

```bash
# settle loop exited with "settled: done" (or idle/blocked)
herdr pane read 1-1 --source recent --lines 100
```

## notes

- `workspace list`, `workspace create`, `tab list`, `tab create`, `tab get`, `tab focus`, `tab rename`, `tab close`, `pane list`, `pane get`, `pane split`, `wait output`, and `wait agent-status` print json on success.
- `pane read` prints text, not json.
- `pane read --format ansi` or `pane read --ansi` returns a rendered ANSI snapshot for TUI feedback loops.
- `pane read --source recent-unwrapped` is useful when you want to inspect the same unwrapped transcript that `wait output --source recent` matches against.
- `pane send-text`, `pane send-keys`, and `pane run` print nothing on success.
- parse ids from `workspace create`, `tab create`, and `pane split` responses when you need new ids. `workspace create` returns `result.workspace`, `result.tab`, and `result.root_pane`. `tab create` returns `result.tab` and `result.root_pane`. for `pane split`, the new pane id is at `result.pane.pane_id`.
- a pane may disappear when its foreground process exits, especially after accidental one-shot `pi -p` usage. re-run `pane list` instead of reusing an old id after any exit or close.
- use `pane read` for current output that already exists. use `wait output` for future output you expect next.
- `--no-focus` on split, tab create, and workspace create keeps your current terminal context focused.
- without `--label`, workspace create keeps cwd-based naming and tab create keeps numbered naming.
- `--label` on tab create and workspace create applies the custom name immediately.
- if you are running inside herdr, the `HERDR_ENV` environment variable is set to `1`.
