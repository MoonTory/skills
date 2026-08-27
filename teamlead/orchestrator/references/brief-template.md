# Agent brief

Every terminal worker starts without the Orchestrator's conversation. Fill the fields that matter; collapse the
template for a tiny task.

```text
ROLE         One terminal skill: explore, plan, build, or review.
GOAL         One outcome a new worker can execute without chat context.
SCOPE        Repository, worktree, allowed paths, forbidden paths, and exclusive ownership.
CONTEXT      Contract, evidence, source pointers, upstream findings, and user decisions.
ACCEPTANCE   Checkable results, one per line.
VERIFY       Exact focused commands or the real-product check.
TIMEBOX      When to return partial findings instead of wandering.
FORBIDDEN    No spawning, delegation, commits, broad edits, destructive actions, or task-specific limits.
REPORT       Status, files or branch, findings or diff, checks, failures, deviations, and open questions.
STANDING     Repository and run rules that survive every resume.
```

A dependency carries context as well as ordering. Relay useful upstream evidence into the dependent brief; do not
make a terminal worker guess what another worker learned.
