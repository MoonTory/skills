---
name: pause-safely
description: Leave a durable, verified checkpoint before context compaction, a harness restart, going offline, or handing a live workflow to another lead. Use only for an explicit pause or handoff; "keep going" and "work while I am away" mean continue with checkpoints.
---

# Pause safely

Leave a checkpoint a cold-start lead can trust.

1. Stop starting new work. Let safe in-flight actions reach a clear boundary; do not interrupt an atomic write or
   merge halfway through.
2. Read live state rather than guessing. Record active worktrees, dirty files, agent panes or task IDs, current
   status, open human gates, and processes that must not be touched.
3. Reconcile claims. Mark what is verified, unverified, blocked, or merely reported by an agent.
4. Write the temporary resume note in a scratch location outside the repository. Include intent, user decisions,
   progress, current state, exact next action, key paths, checks, gotchas, and how to recover each active worker.
5. Point to existing briefs and decision logs instead of copying large reports into the note.
6. Tell the user where the note lives and whether any agents continue running.

Never store secrets or unrelated transcript content in the checkpoint.
