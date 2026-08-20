---
name: session-pickup
description: Resume an in-flight task from a transcript, checkpoint, branch, worktree, agent pane, or prior lead without repeating finished work. Use for "continue", "pick this up", post-compaction recovery, or a teamlead handoff.
---

# Session pickup

1. Read the supplied checkpoint first. If only a transcript exists, read the opening goal and latest relevant region,
   then extract decisions, verified work, open work, and active runtime state. Keep transcript access within the scope
   the user approved.
2. Check the live repository, branch, worktrees, tests, PRs, and agents named in the handoff. History is not current
   truth.
3. Rebuild a compact contract: goal, non-goals, decisions, acceptance, verified results, open gates, and next action.
4. Preserve user changes and existing agent ownership. Do not reuse a pane ID without resolving its current identity.
5. Verify inherited completion claims against source and the real artifact.
6. Continue from the first unfinished step. Do not rerun exploration or implementation that the evidence proves done.

Report any mismatch between the handoff and live state before acting on the stale claim.
