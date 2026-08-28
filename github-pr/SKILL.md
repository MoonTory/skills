---
name: github-pr
description: Create, update, inspect, monitor, and reconcile GitHub pull requests using repository-owned conventions. Use when work must move through a GitHub PR or an existing PR needs CI, review-state, merge, or post-merge follow-up. Do not impose tracker, branch, review, merge, release, or repository-setting policy that the repository has not chosen.
---

# GitHub pull requests

Own the GitHub delivery record, not the implementation, code-review verdict, issue tracker, or release. Read the
repository's policy before acting and keep every mutation within the authority granted by the task.

## Authority boundary

Loading this skill grants no permission to commit, push, open a PR, publish a comment, submit a review, merge, or
change repository settings.

- Reads are safe when they stay within the user's repository and task.
- A request to file, open, or deliver work through a PR normally authorizes pushing the named work branch and
  creating or updating that PR, subject to repository rules.
- Commit, push, PR creation, draft-state changes, review submission, comments, and merge are separate permissions.
  Follow the repository's ownership split rather than assuming one actor owns them all.
- Require fresh explicit authority for force-push, retarget, close or reopen, auto-merge, merge, branch deletion when
  it is not automatic, tags, releases, package publication, and repository settings.
- Never broaden a PR task into a release or deployment.

Before any GitHub write, verify the authenticated account, repository, base, source branch, current head, and whether
a PR already exists. Read the changed object back after every write.

## Discover repository policy

Resolve the repository root and read applicable `AGENTS.md` files, `CONTRIBUTING.md`, and other named contribution
instructions. Search the supported PR-template locations before composing a body:

- `.github/pull_request_template.md`
- `pull_request_template.md`
- `docs/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE/*.md` below `.github`, the root, or `docs`

The repository template owns the body shape. If several templates exist, use the one clearly matched by the change
or user request; ask only when the choice would materially change the PR. If none exists, create a concise factual
body for this PR without adding a permanent template unless asked.

Repository policy also owns branch names, issue references, title format, required evidence, reviewers, merge
strategy, and whether draft PRs are used. Do not import conventions from another project. Do not use
`gh pr create --fill`; commit text is not a safe substitute for the repository's PR contract.

When no template exists, keep the fallback small: a one-sentence purpose or up to three outcome bullets, followed
by the checks that actually ran. Add risk, migration, visual, or compatibility detail only when material. Do not
turn the fallback into a skill-owned template or an exhaustive file summary.

## Compose public-facing content

Treat the branch name, title, body, comments, review text, check annotations, commit text, and release-facing links as
content that may later become public.

- Follow the repository template and keep the explanation proportional to the change.
- State why the change exists, what changed at an outcome level, and checks that actually ran.
- Add compatibility, security, migration, visual, release, or rollback detail only when it helps the review.
- Summarize results; do not paste raw logs or generated file lists.
- Exclude secrets, credentials, private customer data, local absolute paths, temporary URLs, transcripts, and
  unrelated internal context.
- Include tracker references, attribution, or automation disclosure only when repository policy or the user requires
  them. Never invent them.
- Inspect the final title and body before sending them to GitHub.

## PR lifecycle

### Prepare or update

1. Inspect the working tree, branch, remote, base, and current remote head without disturbing unrelated changes.
2. Resolve any existing open or closed PR for the same branch before creating another.
3. Push only the intended branch. Never use broad branch or tag pushes for a PR.
4. Create a draft PR when repository policy or the work state calls for one; otherwise create it ready for review.
5. Read back the PR URL, title, body, base, source branch, draft state, and full head SHA.

### Review and checks

Code-review judgment belongs to the assigned reviewer or review workflow. This skill supplies the exact remote
artifact and current state.

- Bind every review verdict to the PR URL and full head SHA.
- Check the remote head immediately before review and again before accepting the verdict.
- Any new head invalidates evidence for the older head. A rebase or base update that changes the effective diff also
  requires the review promised by repository policy.
- Judge checks only for the current head. Pending, canceled, stale, or unexpectedly skipped checks are not green.
- Do not treat the absence of configured required checks as proof that the repository's expected checks passed.
- Re-read the head after waiting for CI so a concurrent push cannot attach old results to a new revision.

### Ready to merge

Apply the repository's own landing gate. A strict gate normally requires an open non-draft PR, the intended base,
the reviewed head, the expected checks green, a current and mergeable branch, resolved required discussion, and all
human or product gates satisfied. Green CI alone is never a merge decision.

Do not merge unless the current task explicitly grants merge authority. If another person owns the merge, report
that the PR is ready and monitor only when the user asked for follow-up.

### Landed state

After a merge, capture `mergedAt` and the merge commit from live GitHub state. Verify the repository's required
post-merge checks against that exact commit before calling the work complete. A PR closed without merge is not
landed. An unexpected merge strategy or failing base-branch check is a policy or delivery failure, not success.

## Identity and communication

Do not impersonate the authenticated GitHub account. When an agent is using a person's credentials, it may perform
authorized factual mechanics, but it must not present its own judgment as that person's review or approval. Posting
a review, review comment, or conversational reply requires both suitable identity and explicit authority.

Prefer edits to the PR body for factual corrections. Avoid chatty status comments. If a distinct automation identity
exists, stay within its granted permissions and never infer bypass or merge authority from installation access.

## Failure and resume rules

Classify a failed check before acting: change defect, stale or conflicting base, base-branch failure, or infrastructure
failure. Route code and configuration failures back to implementation. Retry a clearly identified infrastructure
failure at most once on the same SHA; if it repeats, stop and report it. Never create an empty commit merely to rerun
CI.

On resume, trust live GitHub state over transcripts or remembered status. Read the current PR, head, checks,
mergeability, discussions required by policy, and merge state. Reconcile these cases explicitly:

- Open with a new head: invalidate earlier head-bound evidence.
- Open with failed or pending checks: route or continue monitoring as authorized.
- Closed without merge: stop; do not reopen automatically.
- Merged: capture the landed commit and verify the base branch.

A request to monitor or babysit persists until the PR merges and required landed checks finish, closes without
merge, needs a human or new authority, or reaches a repeated failure covered by the stop rules. Unchanged pending
state means wait again, not finish. Monitoring grants no comment, retry, ready-state, or merge authority.

For concrete `gh` read-back and mutation patterns, read [references/operations.md](references/operations.md).

## Handoff

Return a compact live-state handoff:

```text
PR: <URL>
State: <draft | review | ready | merged | closed>
Base: <branch>@<full SHA>
Head: <branch>@<full SHA>
Checks: <green | pending | failed | not configured>
Merge: <not merged | merge commit>
Next: <one action and its owner>
```

Report only operations that actually succeeded. A command returning successfully, an idle agent, or green CI does
not by itself prove the PR landed.
