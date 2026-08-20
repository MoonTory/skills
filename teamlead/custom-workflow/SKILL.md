---
name: custom-workflow
description: Design an auditable, task-specific playbook when ticket-flow and orchestrate do not fit an ambitious migration, unusual prototype, or multi-part change. Use for "figure it out", a risky custom run, or work the user wants to plan jointly before agents start.
---

# Custom workflow

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away. Bias toward more rigor. The cost of building the wrong thing dwarfs the cost of being careful.

Do not reinvent a flow that already fits. A focused bug, feature, refactor, or UI change routes to `ticket-flow`. A
multi-day program with repeated units and tracks routes to `orchestrate`. Use this skill when the work needs its own
phase shape and the user should review that shape before expensive execution.

## Start

Read `references/conventions.md`, then add the phases below to the plan.

## Phase A: Frame

Ground first, then commit. Don't start the run until you can state:

- The definition of done as a checkable predicate. "Done well" is not enough.
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced. Raise them before spending hours, not after fifty doomed commits.
- The rigor level, biased high. One-way doors and high blast radius get more; reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs to the user before committing to a long run. Reversible research may proceed, but
the phase contract and costly product choices need a checkpoint.

## Phase B: Design the workflow

Decompose into small, independently verifiable units. Test the riskiest unknown first. Build the check before the
change when that can prove the result cheaply.

- Build the verification harness before the work, with the baseline captured from the pre-change state, so the check reads as "old value vs new value".
- For costly design decisions, run **architect** or **arena** with isolated candidates and a read-only judge. Skip it
  for mechanical work whose shape is already set.
- Parallelize only across real seams. Give every writer its own paths, worktree, or branch. Do not over-fan.
- Write the designed phase list down. That list is what the human reviews.

Then put the design into motion. Add its steps to the todolist as concrete items, after the Phase C entry and before Phase D. Run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment: state the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it didn't.
Verify each unit before starting a dependent one instead of batching every check at the end.

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system. A blank screenshot passes a lazy gate.
- Pair delegated work with a judge and audit the delegates' artifacts yourself before trusting them. If a worker games the gate, reset and harden the contract. If the gate itself is wrong, fix the gate in its own change rather than routing around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Log the run with **decision-log**, one canonical TSV with a row per important decision and unit. Commit it only when
the reviewer needs the trail to trust a large run. Prefer checks another engineer can rerun.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product. Encode repeated corrections as a gate, lint rule,
check, script, or skill change when text reminders are not enough.

**Reply:** the playbook you designed, the rigor level and why, the decision-trail path, what's verified against the predicate, and what's still open.
