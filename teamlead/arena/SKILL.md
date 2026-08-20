---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open a todolist with one entry per phase before launching anything. The arena runs autonomously and the list keeps phases from silently disappearing.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract. Get it right before spawning anything.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. Concrete: `Adds a --dry-run flag that skips writes`. Vague: `code is correct`. The rubric is the picker's tool in Phase D; candidates only see the task.
3. Pick the runners from the current repository's model policy. Default to two or three structurally different views:
   Sol for exact technical work, Fable or Opus for judgment, and Terra or local Qwen as an independent lane. Spawn
   more only when the design space has more real directions. Same-model repeats fit generation-bound work.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`). N candidates writing to the same path is shared mutable state and fails the the **separate-before-serializing-shared-state** principle skill test.

## Phase B: Fan out

Read `../references/conventions.md`, then launch all candidates together. In Herdr, put them in separate persistent
Pi panes with isolated write locations. Give each the same contract, the shared grounding path, its own output path,
and instructions to produce both the artifact and a short rationale.

The rationale is mandatory. Without it, the parent cannot tell whether a candidate's structure is principled or accidental, which makes Phase E grafting unreliable. Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all candidates complete, spawn one read-only judge from a different model family than the lead when possible.
It sees the rubric and completed candidates by path label, scores each criterion, and recommends a base with reasons.
Run it in parallel with the lead's own reading. Never start the judge while candidates still write.

## Phase D: Pick a base

Read every candidate end to end before picking. Skimming N candidates surfaces only the candidate whose surface looks most familiar.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend without breaking its rules. Prefer the cleaner boundary and smaller
surface when two candidates tie.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each accepted idea into the base deliberately. Do not paste whole sections mechanically. The result must keep
one coherent design.

Record what was grafted, from which candidate, and what was rejected and why. The rejection notes are the highest-signal part of the record. Future readers learn from what you considered and dropped, not just what you kept.

When N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact against the original rubric and the real product. Multiple candidates do not earn a
pass by themselves.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
