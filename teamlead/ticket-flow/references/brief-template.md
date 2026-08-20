# Agent brief

Every worker starts without the lead's conversation. Fill the fields that matter; collapse the template for a tiny
task instead of wrapping a two-line edit in a long document.

```text
GOAL         One outcome a new agent can execute without chat context.
SCOPE        Repository, worktree, allowed paths, forbidden paths, and exclusive ownership.
CONTEXT      The contract, root cause, source pointers, upstream findings, and user decisions.
ACCEPTANCE   Checkable results, one per line.
VERIFY       Exact focused commands or the real-product check.
TIMEBOX      When to return partial findings instead of wandering.
FORBIDDEN    No commits, no broad edits, no agents, no destructive commands, or task-specific limits.
REPORT       Status, files or branch, findings or diff, checks run, failures, deviations, and open questions.
STANDING     The repository and run rules that survive every spawn and resume.
```

A dependency carries context as well as ordering. Relay the useful upstream report into the dependent brief; do not
make a worker guess what a sibling learned.
