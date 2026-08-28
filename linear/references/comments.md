# Linear comments

Use comments as short event records. The issue contract and role-owned documents hold the detail; a comment states what changed, the evidence that supports it, and what happens next.

## Allowed comment types

Use comments only for:

- Plan ready.
- Builder handoff.
- Review verdict.
- Needs Input.
- Owner decision.
- Landed and verified.

A standard comment has one short heading and at most four bullets. Include only:

- Outcome.
- Evidence summary or canonical artifact link.
- Blocker, Owner action, or next role.
- A deviation only when it changes scope, validation, or the next step.

Omit a bullet when it adds no useful fact. A short event may need only two bullets.

Never copy a multi-round review history into a landing comment. The Review document owns that history; the event comment links it and states the current outcome.

## Author and mutation rules

- Planner posts Plan ready.
- Builder posts Builder handoff.
- Reviewer posts Review verdict.
- Owner may post an Owner decision directly; Orchestrator may record it with clear Owner attribution.
- Orchestrator posts Needs Input and Landed and verified after reading the role evidence.
- The role author never changes status or metadata. Orchestrator reads the comment or linked artifact, then applies the transition and verifies it.

If the authenticated actor does not match the required author, stop instead of posting through another identity.

## Templates

### Plan ready

```markdown
**Plan ready**

- Outcome: <scope is executable or the exact decision still required>.
- Artifact: <canonical Exploration or Plan URL>.
- Labels: <meaningful area and type labels proposed>.
- Next: Orchestrator review and Owner approval.
```

### Builder handoff

```markdown
**Builder handoff**

- Outcome: <implemented result>.
- Evidence: <checks and branch or pull request link>.
- Deviations: <None, blocker, or material scope difference>.
- Next: Independent review.
```

### Review verdict

```markdown
**Review verdict — <Passed | Changes required>**

- Outcome: <one-sentence verdict>.
- Evidence: <Review document URL and reviewed full SHA, or concise finding summary for a simple non-revision review>.
- Blocking findings: <None or short list>.
- Next: <Ready To Land, Owner validation, or Builder fixes>.
```

### Needs Input

```markdown
**Needs Input**

- Owner action: <one exact decision or validation step>.
- Impact: <what cannot proceed or what the answer changes>.
- Evidence: <artifact or stable preview link when available>.
- Resume: <the honest status and delegate after the answer>.
```

Do not put a temporary local URL in the durable comment. Give that URL in the live chat. In Linear, describe what the Owner must validate. A stable pull request or deployed preview URL is allowed.

### Owner decision

```markdown
**Owner decision**

- Decision: <approved choice or validation result>.
- Scope impact: <None or exact contract change>.
- Evidence: <artifact, issue, or stable preview link>.
- Next: <status and role>.
```

When Orchestrator records this comment, name the Owner in the decision bullet rather than implying the app made the product choice.

### Landed and verified

```markdown
**Landed and verified**

- Outcome: <what landed>.
- Landing: <merge commit, pull request, or equivalent durable reference>.
- Validation: <required checks and result on the landed tree>.
- Next: Done.
```

## Keep out of Linear comments

Do not include:

- `localhost`, `127.0.0.1`, or temporary ports.
- Raw test output or a full command transcript.
- Model names.
- Context percentages or token counts.
- Herdr pane, tab, or session names.
- Batch, wave, unit, or worker keys.
- Scratch-file or temporary handoff paths.
- “Catching the log up” histories or late reconstructions of the run.
- Full Exploration, Plan, or Review content.
- Long lists of changed files already represented by a commit or review artifact.

Summarize checks by name and result. Link the canonical artifact, branch, pull request, commit, or stable preview when it exists. Keep temporary execution detail in the live chat or scratch state.

## Read-back check

After posting:

1. Read the comment back.
2. Confirm the author.
3. Confirm the issue.
4. Confirm the rendered content and links.
5. Confirm that no excluded execution detail escaped into Linear.
6. Confirm that intended blocks and links render correctly rather than as literal `\\n`, `\\r`, `\\t`, collapsed lists, or broken link text.

If read-back fails, the same role author corrects the comment before Orchestrator accepts it as transition evidence.

Report the comment URL or ID when the tool returns one. Never claim the comment exists from intent alone.
