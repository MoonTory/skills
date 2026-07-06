---
name: codex-implement
description: Ask Codex CLI (gpt-5.5) to implement a scoped coding task directly in the current repository. Use when the user asks Claude to have Codex or gpt-5.5 build, fix, refactor, migrate, or modify code, or when the model-selection rubric delegates implementation to gpt-5.5. Codex may edit files and run validation. Do not use for review-only tasks or general advice; use codex-review or codex-consult instead.
---

# Codex Implement

Use Codex as an implementation agent when the user explicitly wants Codex to make changes or when another implementation perspective would be useful.

Claude remains responsible for the final result. Inspect Codex's changes, verify important claims, and do not treat a successful Codex response as proof that the implementation is correct.

## Workflow

1. Identify the requested behavior, constraints, and acceptance criteria.
2. Inspect the repository enough to provide relevant context and identify existing uncommitted changes.
3. Create a temporary artifact directory for the prompt and Codex report.
4. Run `codex exec` with workspace write access and a focused implementation prompt.
5. Read Codex's report and inspect the actual working-tree diff.
6. Run or verify the relevant tests, type checks, lint checks, or builds.
7. Fix minor issues directly when appropriate, or report unresolved problems clearly.

Use this command shape:

```bash
ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-implement.XXXXXX")"
REPORT="$ARTIFACT_DIR/report.md"
PROMPT="$ARTIFACT_DIR/prompt.md"
STATUS_BEFORE="$ARTIFACT_DIR/status-before.txt"

git status --short > "$STATUS_BEFORE"

codex -C "$PWD" exec \
  --ephemeral \
  --sandbox workspace-write \
  - < "$PROMPT" > "$REPORT"
```

## Implementation Prompt

Give Codex a concrete task with requirements and repository context:

```text
Implement the requested change in the current repository.

Requirements:
- [Describe the required behavior.]
- [Describe important constraints.]
- [Include acceptance criteria when available.]

Instructions:
- Read the repository instructions and relevant existing code before editing.
- Follow established architecture, naming, formatting, and testing patterns.
- Make the smallest coherent change that fully implements the requirements.
- Preserve existing behavior unless the requirements explicitly change it.
- Do not overwrite or revert unrelated uncommitted changes.
- Do not commit, push, create branches, or open pull requests.
- Add or update focused tests where appropriate.
- Run the most relevant available validation commands.
- Do not hide failing tests or weaken existing assertions.
- Stop and explain the blocker if the requirements cannot be implemented safely.

In the final response include:
- a concise implementation summary
- files changed
- validation performed and its results
- assumptions or unresolved risks
```

Add task-specific context when useful: ticket requirements, relevant files, existing implementation patterns, expected API behavior, screenshots, failing tests, or areas Claude has already investigated.

## Verifying the Implementation

After Codex finishes:

1. Read `$REPORT`.
2. Inspect `git status --short` and the complete diff.
3. Confirm that unrelated pre-existing changes were not modified.
4. Check the implementation against every stated requirement.
5. Run the relevant validation independently when practical.
6. Look for incomplete error handling, missing tests, debug code, broad refactors, or requirement mismatches.

Do not claim that tests passed unless their successful execution was observed.

## Reporting Back

Summarize what was actually changed, not merely what Codex claimed to change.

Include:

- implemented behavior
- important files changed
- validation results
- assumptions, limitations, or remaining work

Separate verified results from anything Codex reported that Claude could not independently confirm.

If Codex made incorrect or incomplete changes, either correct them or explain the remaining issue clearly.

If `codex` is not installed or the command fails, report the error and continue the implementation directly when possible.
