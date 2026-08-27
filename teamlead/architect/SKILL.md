---
name: architect
description: "Coordinate competing design sketches before implementation. Use only from an authorized Lead, Teamlead, or Orchestrator after loading the orchestrator skill; never use from a terminal Planner or other worker role."
---

# Architect

Design before implementing. Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across multiple model perspectives, then fill in code against the chosen sketch. If implementation proves the sketch wrong, throw it out and redesign.

This is a coordinator flow. Read the installed `orchestrator` skill first. If the current task does not grant
coordinator authority, stop and use the terminal `plan` skill.

## Start

Open a todolist with one entry per phase before starting. Autonomous mode without checkpoints needs the list to show phase position and keep phases from silently disappearing.

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Delegate bounded terminal `explore` roles over the
relevant subsystems. Use `adversarial-review` when existing structure must be challenged.

Naming a file is not grounding. Produce the traced model `explore` prescribes. When the design changes ownership or
layering, inspect commit, PR, issue, and project-memory history so known reasons become constraints rather than guesses.

Skip Phase A only when the work is genuinely greenfield with no surrounding system to integrate.

## Phase B: Sketch

Run the **arena** skill with the design-sketch task and the Phase A grounding artifacts. Pass `references/runner-prompt.md` as each runner's prompt. Each candidate produces a design package shaped per `references/rationale-template.md`: the caller's usage written first, then the type sketch, function signatures, module map, and prose rationale derived from it.

Use at least two structurally different design views chosen through the current model policy.

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks
sufficient. Compare whole shapes, not small changes inside one shape.

Screen every candidate against [`references/design-red-flags.md`](references/design-red-flags.md) before synthesis. Reject or revise shallow modules, information leakage, temporal decomposition, and pass-through methods.

Compare viable candidates on interface depth. Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

Arena returns one synthesized design package. The synthesis decision populates the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Default in this collection: show the synthesized contract to the user before implementation when the design changes
public APIs, product behavior, ownership, persistence, or another costly choice. For reversible internal structure,
the lead may proceed and report the decision.

Opt in to a checkpoint when the invoker explicitly asks: "/architect with checkpoint," "stop and show me before implementing," or similar. Then surface the synthesized design and pause for sign-off.

The synthesis may ship as its own commit. Subsequent commits then fill bodies against a stable contract. For
adversarial pressure before implementation, run `adversarial-review` on the synthesized sketch.

If the human pushes back on the shape (in a checkpoint or after the fact), treat that as Phase A evidence. Re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

Delegate a terminal `build` role to replace `not implemented` bodies with code and pseudocode with logic. The
synthesized sketch is the contract.

Deviations from the sketch are signal worth surfacing, not friction to absorb silently. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching. Surface it; don't bolt it on.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing the same kind of friction the sketch cannot absorb, throw the sketch out. Do not
keep adding escape hatches to a wrong design.

The signal is a *pattern*, not single instances. Tells:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape across the implementation. Surfacing deviations is Phase D's job; a repeated pattern of them is Phase E's trigger.

Use judgment. A few edge cases don't condemn an architecture. Some problems are legitimately complex; complexity in the data is not complexity in the design. The rewrite signal is repeated friction of the same shape, not single hard cases.

When you scrap:

1. Delegate a fresh terminal `explore` role over what was built. Implementation lessons become inputs to the next design.
2. Redesign as if the new constraints had existed from day one.
3. Remove failed structure before adding more. The new sketch should start smaller than the old one.
4. Return to Phase B and re-run arena.

## Outputs

The caller's usage is written first and the type sketch derived from it. One file with new types and signatures for small changes; module map plus type definitions for larger work. The rationale ships alongside, shaped per `references/rationale-template.md`, including the usage sketch and the synthesis decision.
