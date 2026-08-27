# Orchestrator conventions

Read the repository instructions first. They own project behavior. These rules own Teamlead coordination.

## Roles

- Orchestrator: holds user context, selects the flow, writes briefs, makes decisions, verifies evidence, and reports.
- Explorer: terminal and read-only; traces the assigned question and returns evidence.
- Planner: terminal and read-only; turns known facts into a bounded execution contract.
- Builder: terminal and write-capable only within its assigned scope.
- Reviewer: terminal and read-only; tests the work against the contract and returns a verdict.

Only an explicitly assigned Orchestrator may delegate. Terminal roles never spawn, delegate, manage other work
contexts, or load coordinator skills. A repository mention of Teamlead or an available orchestration tool does not
widen a terminal brief.

## Model choice

Follow the current repository or user model policy. Exact model names, provider IDs, and launch commands belong to
the active harness skill. Choose the least costly model that can handle the work; use stronger reasoning for hard
architecture, security, and technical review, and stronger product judgment for user-facing work. Use different
model families only when independent blind spots justify the cost.

## Harness boundary

When the task grants coordinator authority and `HERDR_ENV=1`, load the installed `herdr` skill and follow it for the
full work-context and agent lifecycle. The environment alone does not grant authority. Outside Herdr, use the current
harness's delegation tools only when they are available and the task permits delegation.

## Ownership and safety

- Use one writer per file set and one writer per worktree or branch.
- Preserve user changes and unrelated dirty files.
- Human approval stays human. Agents may request it but not grant it.
- The Orchestrator decides whether a report proves completion.
- Internal unit keys, worker IDs, batch names, and wave names belong to scratch state. Use stable project identifiers
  and plain work scope in commits and user reports.
- Keep temporary briefs, handoffs, and checkpoints in harness state or a scratch directory outside the repository
  unless the user explicitly asks the project to own them.

## Product and UI work

Product taste stays with the user and Orchestrator. Prefer focused human feedback when it is a better product gate
than a broad automated visual loop. Technical checks do not override a failed product review.
