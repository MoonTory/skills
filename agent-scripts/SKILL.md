---
name: agent-scripts
description: Provides checked command-line helpers for waiting on and working with agent panes.
---

# Agent scripts

Run these scripts through their installed absolute paths, such as
`~/.agents/skills/agent-scripts/scripts/wait-agent`. They find `waitlib.py` through the real path of the script,
so symlinked installs work from any worktree.

## Shared contract

Every script writes a final stdout line with one JSON object. It always has `script`, `event`, `target`,
`elapsed_s`, `at`, and `detail`. Poll progress goes to stderr, starts with the script name, and is hidden by
`--quiet`. `--pretty` replaces the JSON object with one short line for use at a terminal; agents must not use it.

Exit `0` means the event happened. Exit `2` means the target is gone or cannot be used. Exit `3` means timeout.
Exit `4` means a tool failed after its allowed retries. Scripts use no other exit codes for run results.

Every script accepts `--timeout <seconds>`, `--interval <seconds>`, `--fixture <path>`, `--quiet`, `--pretty`,
`--brief <path>`, and `--help`. A timeout of `0` checks once. Polling tool failures back off for
`min(interval * 2 ** (failures - 1), 300)` seconds and fail after five in a row; a good poll clears the count.

Fixture files hold ordered `responses`. Each response records `cmd`, `stdout`, `stderr`, and `exit`. The fixture
runner checks that the recorded command starts with the command the script built. Its clock advances without
sleeping. Production commands run only through `waitlib.Runner`, and sleeps run only through `waitlib.Clock`.

Each completed run appends a tab-separated row with timestamp, script, target, event, elapsed seconds, and the
exact command. With `--brief`, it writes `<brief>.launch`; otherwise it writes
`${TMPDIR:-/tmp}/agent-scripts/waits.log`.

These scripts do not resume agents, send keys, or prompt them while checking state. Only `agent-task` sends a
prompt, and it sends the given line once, apart from its one retry when Herdr has not registered the agent yet.

## Environment

- `HERDR_SOCKET_PATH` selects the Herdr socket and defaults to `~/.config/herdr/herdr.sock`.
- `LINEAR_API_KEY` supplies the Linear token to scripts that query Linear.
- `AGENT_SCRIPTS` lets private scripts select this scripts directory.
- `GH_REPO` passes repository selection to `gh`.
- No script reads or writes other settings.

## Script index

Warning: output waits ignore matching lines that were present before the wait began, including echoed commands.
Choose markers that do not appear in the command sent to the pane so the intended output stays clear.

- `wait-output` waits for pane text; exits 0 matched, 2 pane gone, 3 timeout, or 4 tool failure.
- `wait-agent` waits for an agent to leave working; exits 0 settled, 2 pane gone, 3 timeout, or 4 tool failure.
- `wait-any` waits for the first of several agents; exits 0 settled, 2 all panes gone, 3 timeout, or 4 tool failure.
- `agent-probe` reports state and session activity without prompting; exits 0 probe, 2 pane gone, or 4 tool failure.
- `agent-answer` prints the last assistant reply; exits 0 answer or truncated, 2 no reply or pane, or 4 tool failure.
- `agent-task` waits for startup (pi banner, or for `--claude` the `❯` prompt line or the `auto mode on` / `accept edits on` footer; ceiling `--timeout` capped at 60 s, 30 s when `--timeout 0`), prompts once, and waits for settle; `--timeout 0` returns after the prompt with the current status; exits 0 settled, 2 gone or blocked, 3 timeout, or 4 prompt/tool failure.
- `close-track` closes all safe panes in a tab; exits 0 closed, 2 busy or gone, or 4 tool failure.
- `brief-check` checks required brief fields; exits 0 valid, 2 missing fields or file, or 4 tool failure.
- `wait-ci` waits for PR or commit checks; exits 0 green or red, 2 closed or head changed, 3 timeout or no run, or 4 tool failure.
- `wait-merged` waits for a PR merge; exits 0 merged, 2 closed, 3 timeout, or 4 tool failure.
- `wait-branch-gone` waits for remote branch deletion; exits 0 gone, 2 absent, 3 timeout, or 4 tool failure.
- `wait-review` waits for PR review activity; exits 0 threads, changes_requested, approved, or baseline, 2 merged or closed, 3 timeout, or 4 tool failure.
- `wait-linear` waits for a Linear comment or state change; exits 0 changed or baseline, 2 not found, 3 timeout, or 4 API failure.
- `wake-on` queues a wait command for the Claude hook; exits 0 queued.
- `wake-run` runs queued waits; exits 0 for an empty queue or 2 when a wait finishes.

## Tests

From the repository root run:

```sh
python3 -m unittest discover -s agent-scripts/tests -t agent-scripts
```
