---
name: ticket-flow
description: Run a bounded bug fix, feature, refactor, or UI change through terminal explore, plan, build, and review roles. Use only from an authorized Lead, Teamlead, or Orchestrator after loading the orchestrator skill; never use from a terminal worker role.
---

# Ticket flow

The lead plans, decides, verifies, and reports. Workers gather facts, implement the decided change, and review it.
Read the installed `orchestrator` skill and its shared conventions and brief template first. If the current task does
not grant coordinator authority, stop and use the assigned terminal role skill.

## 1. Frame

Confirm the requested outcome, non-goals, acceptance checks, and whether the user wants planning only or a shipped
change. Inspect repository instructions and dirty state. Extract a ticket ID from the branch only when the project
uses one; never invent it.

Before the first delegation, let the authorized harness allocate one task context. Keep exploration, planning,
implementation, review, fixes, and re-review in that context. The active harness skill owns the mechanics.

## 2. Explore

Start one or two terminal `explore` workers when the code path or cause is not already known. Ask for paths and lines,
the runtime mechanism, competing explanations, a minimal fix, and risks. Keep each brief read-only and bounded.

The lead checks the key files and traces the failing path. Explorer agreement is evidence, not proof.

## 3. Plan with the user

Name the root cause or feature shape, the exact change, what stays untouched, and how success will be checked. Point
the implementer at an existing file to mirror when possible. For ambiguous work, settle the contract with the user
before implementation. Delegate a terminal `plan` role for a non-trivial contract. Use `architect` when the change
needs competing designs.

## 4. Implement

Give one terminal `build` worker exclusive write scope. The brief contains the decided approach; the Builder does not
restart discovery unless the source contradicts the plan. Require a diff summary, focused check results, deviations,
and open issues. The Builder does not commit unless the brief says so.

## 5. Verify

Read the full diff. Check edge cases introduced by the change. Run focused type checks, lint, tests, and real-product
checks in proportion to risk. When an agent claims a failure predates the change, prove that with a clean comparison
before accepting the claim. Do not disturb unrelated user changes to create that comparison.

For UI work, let the user provide focused visual feedback when that is faster and more reliable than a broad agent-
driven screenshot loop.

## 6. Review

Use a fresh terminal `review` worker with no stake in the implementation. Give it the contract, cause, diff, and
known risks. Ask for `APPROVE` or `REQUEST CHANGES` with evidence. Use `adversarial-review` when the risk justifies
several independent reviewers.

Judge every finding yourself. Send accepted fixes to the same Builder work context, then return to the same Reviewer
for a new verdict. Do not apply reviewer suggestions just because they exist.

## 7. Ship or hand back

Follow repository instructions for commits and PRs. Never add co-author, generated-with, or AI attribution text.
Lead the final report with the shipped artifact or current result, then cause, change, review rounds, and checks.
