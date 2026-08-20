---
name: teamlead-mode
description: Route non-trivial engineering work through the smallest fitting lead workflow. Use for teamlead work, tickets, bugs, features, ambiguous research, multi-agent implementation, adversarial review, or long autonomous programs, especially when the session runs in Herdr. Do not use for a quick answer or a change one agent can safely finish in one pass.
---

# Teamlead mode

Own the result. Agents search, implement, and challenge. The lead holds the user's context, writes the contract,
makes decisions, reads the resulting work, and verifies every claim that matters.

Read `../references/conventions.md` before choosing a flow.

## Route the task

1. Use direct work when one agent can safely finish it in one pass. Do not add delegation for its own sake.
2. Use `ticket-flow` for a bounded bug, feature, refactor, or UI change.
3. Use `explore` for a read-only question or before planning an unfamiliar subsystem.
4. Use `architect` when an API, type, ownership, or module boundary must be settled before code.
5. Use `arena` for competing designs or prototypes of the same artifact.
6. Use `swarm` for independent coverage slices or a controlled model comparison.
7. Use `adversarial-review` when a fresh multi-model challenge can change the ship decision.
8. Use `custom-workflow` when the standard phases do not fit an ambitious or unusual task.
9. Use `orchestrate` only when the work outlives one agent and needs durable queue state.
10. Use `pause-safely`, `session-pickup`, `recall`, `decision-log`, or `reflect` when the run needs continuity or learning.

## Contract before fan-out

Agree with the user on the goal, non-goals, decisions, acceptance checks, autonomy limits, and workflow shape before
starting expensive work. Reversible research may proceed while the contract is taking shape. A product choice that
changes the outcome remains a human decision.

Use `../references/brief-template.md` for delegated work. Every brief stands alone and names its write scope.

## Lead loop

- Keep useful work moving while agents run.
- Treat completions as queue events. Finish the current decision before draining reports.
- Read blocked workers and answer or stop them quickly.
- Steer the same worker when its context is still useful. Replace it when it has the wrong task model, has drifted,
  or would need a full re-brief.
- Verify reports against source, diff, checks, and the real product in proportion to risk.
- Tell the user when the plan changes, a real blocker appears, or human taste is needed.

## Handoff

Lead with the outcome. Then state the cause or decision, what changed, what reviewers found, which checks actually
ran, and anything still open. Do not forward raw agent reports.
