---
name: swarm
description: "Coordinate parallel workers, drain them, and return one report. Use only from an authorized Lead, Teamlead, or Orchestrator after loading the orchestrator skill; never use from a terminal worker role."
---

# Swarm

Fan out N workers. They may cover separate slices, race the same brief, or mix both. The lead drains them and returns
one report.

This is a coordinator flow. Read the installed `orchestrator` skill first. If the current task does not grant
coordinator authority, do not launch workers.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the work and available concurrency. More workers are not automatically better.
4. Pick the least costly capable model from the current repository or user policy. Name every model in a comparison
   before starting.
5. Give each worker its own writable output when it writes. Use a worktree, branch, or `/tmp/swarm-<slug>/worker-<n>/`.

## Phase B: Fan out

Launch all workers together when the authorized harness permits it. Use read-only tools unless a slice explicitly
owns a writable output. The active harness skill owns work-context placement and lifecycle.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
