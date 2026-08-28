# Linear artifacts

Use Linear documents for durable Exploration, Plan, and Review work that does not fit cleanly in an issue description. The issue remains the source of truth for executable scope, assignment, delegation, dependencies, and delivery status.

## Ownership

The durable author must match the authenticated app actor:

- Planner publishes Exploration and Plan documents.
- Reviewer publishes Review documents.
- Builder evidence normally belongs in a short Builder handoff comment.
- Orchestrator links artifacts to issue metadata and uses them as transition evidence; it does not normally publish another role's document.

If the correct role cannot publish, stop the phase and repair the role connection. Do not hide an identity failure by publishing the document through Orchestrator or the human account.

## Naming and scope

Title every artifact:

```text
<descriptive scope> — <artifact type>
```

Examples:

- `Notification delivery — Exploration`
- `Notification delivery — Plan`
- `Notification delivery — Review`
- `Notification retry hardening — Exploration`
- `Notification retry hardening — Plan`
- `Notification retry hardening — Review`

Lead with the scope so several artifact sets remain easy to scan. Use `Exploration`, `Plan`, or `Review` as the artifact type.

Keep one Exploration, one Plan, and one Review document per distinct scope:

- Update the existing document while fixes stay inside the agreed scope.
- A material Owner-approved rescope creates a newly named artifact set.
- Keep the earlier scope's documents intact; they remain the durable record of work already planned, implemented, or reviewed.
- Add a short opening line linking the new scope to the earlier work, such as `Expanded after Owner validation of [the initial scope](<Linear URL>).`
- Update the issue contract before implementation of the new scope resumes.
- Reviewer updates the same Review document through rejection, Builder fixes, recheck, and final verdict.

Never add `v2`, `latest`, `final`, issue-derived suffixes such as `PROJ-7B`, or agent-made batch, wave, or worker keys. Do not repeat the issue ID in the title when the document is already parented to that issue.

## Parent and update rules

The document-save capability supports create and update:

- Create by omitting the document ID and supplying exactly one parent.
- Update by supplying the existing document ID. Use full content for a planned rewrite or a patch for a narrow edit.
- Parent a cross-issue artifact to its project.
- Parent an issue-specific artifact to its issue.
- Do not pass a parent during an update unless the document should move; doing so reparents it.

Search first and keep one canonical document for the role, artifact type, and scope. Rely on Linear's document history rather than creating numbered copies. Store the returned document ID and URL in the related issue or handoff.

After every save, read the document back and verify:

- Authenticated author.
- Title.
- Content.
- Parent.
- Returned URL.

Inspect the rendered Markdown, not only the raw write response. Visible `\\n` or `\\t`, collapsed lists, broken links, or lost block breaks mean the write failed. The same role author repairs the same document and reads it back again before handoff.

## Markdown that renders well

Linear converts Markdown into its rich-text editor. Use this stable subset:

- Keep each prose paragraph and list item on one source line. Use blank lines only between blocks; do not hard-wrap text, because some Linear write paths preserve those line breaks.
- `##` through `####` headings. The Linear document title acts as the page title.
- Bold, italic, strikethrough, inline code, links, and blockquotes.
- Bulleted lists, numbered lists, and task lists using `- [ ]` and `- [x]`.
- Fenced code blocks with a language when known.
- Pipe tables with a header row.
- `---` for a divider.
- Mermaid in a fenced `mermaid` block when a diagram makes a real relationship easier to understand.
- API-created collapsible sections with `+++ Section title`, followed by the content and a closing `+++`.

Use the actual Linear URL for an issue, project, or document when referring to it. Linear renders pasted Linear URLs as mentions. Do not invent mention syntax or type an unlinked identifier when the returned URL is available.

Avoid raw HTML, deeply nested lists, large decorative tables, emoji used as structure, and diagrams that repeat plain text. Do not use a collapsible section for scope, acceptance criteria, risks, findings, or open questions; those must stay visible.

## Exploration template

Title: `<descriptive scope> — Exploration`

Remove empty or irrelevant sections instead of leaving filler text.

```markdown
- **Artifact status:** Draft
- **Authoring role:** Planner
- **Related work:** <project and issue links>
- **Last reviewed:** YYYY-MM-DD

---

## Question

<What must this exploration resolve?>

## Current evidence

<What the code, product, or earlier work proves today.>

## Constraints

- <Constraint that changes the choice>
- <Explicit non-goal>

## Options

### <Option>

- Benefits: <what this option improves>
- Costs: <what this option requires or risks>
- Evidence: <links, code paths, or observed behavior>

## Recommendation

<Preferred direction and why.>

## Open decisions

- [ ] <Decision, Owner, and when it blocks work>
```

## Plan template

Title: `<descriptive scope> — Plan`

The artifact status describes the plan, not implementation progress. Linear issue statuses remain canonical for execution.

```markdown
- **Artifact status:** Draft
- **Authoring role:** Planner
- **Related work:** <project and issue links>
- **Last reviewed:** YYYY-MM-DD

---

## Outcome

<What will be true when this work succeeds.>

## Context

<Why this work exists and the evidence that shaped it.>

## Scope

### Included

- <Included result>

### Excluded

- <Explicit non-goal>

## Proposed approach

<The chosen approach and the key reasons for it.>

## Work breakdown

| Work item | Outcome | Blocked by | State |
| --- | --- | --- | --- |
| <issue link or proposed title> | <checkable result> | <issue link or None> | Proposed |

Every accepted `Blocked by` value maps to the issue's live `blockedBy` relation; `Proposed` rows remain previews until Orchestrator writes and reads back the relation. Put context-only links in Related work, not this column.

## Acceptance criteria

- [ ] <Checkable product or code result>

## Validation

- [ ] <Check that proves the outcome>
- [ ] <Owner or real-product validation when needed>

## Risks and tradeoffs

| Risk or tradeoff | Impact              | Response                      |
| ---------------- | ------------------- | ----------------------------- |
| <risk>           | <what could happen> | <mitigation or accepted cost> |

## Open decisions

- [ ] <Decision, Owner, and when it blocks work>
```

## Review template

Title: `<descriptive scope> — Review`

Keep one Review document for the scope. Update its current verdict and append a review-cycle row when the Builder returns with fixes.

```markdown
- **Artifact status:** Active
- **Authoring role:** Reviewer
- **Related work:** <issue, branch, and Plan links>
- **Review target:** <pull request, branch, diff, or other stable target>
- **Head revision:** <full SHA or immutable revision; N/A with reason>
- **Base revision:** <full SHA or immutable base; N/A with reason>
- **Last reviewed:** YYYY-MM-DD

---

## Verdict

<Pending re-review | Pass | Changes required>

## Scope reviewed

<Issue contract, branch or pull request, and implementation round.>

## Findings

### <Finding title>

- Severity: <blocking | non-blocking>
- Evidence: <specific code, behavior, or check>
- Required change: <what must change>

## Acceptance and validation

| Requirement | Result      | Evidence                   |
| ----------- | ----------- | -------------------------- |
| <criterion> | Pass / Fail | <link or concise evidence> |

## Review cycles

| Date       | Implementation round | Revision | Verdict          | Notes           |
| ---------- | -------------------- | -------- | ---------------- | --------------- |
| YYYY-MM-DD | Initial              | <full SHA or immutable revision> | Changes required | <short summary> |

## Final approval

<Complete only after the current implementation round passes.>
```

## Keeping artifacts current

- Planner updates the Exploration or Plan when evidence or decisions change inside the current scope.
- Planner changes a Plan from `Draft` to `Ready` before publishing Plan ready, updates `Last reviewed`, and clears or records every resolved Owner decision. A document that still says Draft or awaiting approval cannot support execution.
- A material scope change returns the issue to `Scoping`, updates the issue contract, and starts a new named artifact set.
- Builder reads the current set before work and reports contradictions instead of silently rewriting Planner or Reviewer documents.
- Reviewer records every rejected and approved implementation round and its exact revision in the same Review document for that scope. It marks the current verdict `Changes required` or `Pass`; a new revision retains earlier cycles but resets the current verdict to `Pending re-review` until the Reviewer checks and records the new target.
- Orchestrator reads the role-authored artifact before changing status or delegation.
- Orchestrator does not advance a phase when the canonical artifact still claims Draft, pending approval, an unresolved blocking decision, an older review revision, or another state that contradicts the proposed transition. It returns the artifact to its authoring role rather than editing another role's evidence.
- When the review target is mutable, Orchestrator compares its live revision and base with the Reviewer-recorded values before `Ready To Land`. It never edits Reviewer-owned target or verdict evidence to make them match.

Link the canonical artifact from the issue and short event comment. Do not copy its full content into the issue description or comments.
