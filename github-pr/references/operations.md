# GitHub PR operations

Use these patterns only after the task and repository rules authorize the corresponding action. Prefer structured
output and read live state again after every mutation.

## Preflight

Resolve local and GitHub identity before writing:

```sh
git rev-parse --show-toplevel
git status --short --branch
git remote get-url origin
git branch --show-current
git rev-parse HEAD
gh auth status
gh repo view --json nameWithOwner,url,visibility,defaultBranchRef
```

Check whether the branch already has a PR instead of creating a duplicate:

```sh
gh pr list --head <branch> --state all --json number,url,state,isDraft,headRefName,headRefOid
```

Do not switch branches, clean the tree, stage files, or rewrite commits as part of this preflight.

## Template discovery

Search the repository rather than using a skill-owned template:

```sh
rg --files -g 'pull_request_template.md' -g 'PULL_REQUEST_TEMPLATE.md' -g '**/PULL_REQUEST_TEMPLATE/*.md'
```

Read contribution instructions and the selected template in full. Prepare the populated body in a temporary file
outside the repository so the working tree does not gain scratch content. Preserve useful headings and hidden
instructions, but remove unused placeholders and empty optional sections from the submitted body when the template
permits it.

## Create or update

Push only the intended branch and set its upstream explicitly when needed:

```sh
git push -u origin <branch>
```

Create from an inspected title and body file. Omit `--draft` only when the work is already ready and repository policy
allows a ready PR at creation:

```sh
gh pr create --draft --base <base> --head <branch> --title <title> --body-file <body-file>
```

Never use `--fill`. Update an existing PR rather than opening another for the same branch:

```sh
gh pr edit <number-or-url> --title <title> --body-file <body-file>
```

Mark a draft ready only when the owning workflow authorizes review:

```sh
gh pr ready <number-or-url>
```

After each action, read the exact object back.

## Canonical snapshot

Use one structured snapshot for decisions and resume:

```sh
gh pr view <number-or-url> --json number,url,state,isDraft,title,body,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,mergedAt,mergeCommit
```

Record the full `headRefOid`; a short SHA is display text, not a review key. Re-read this snapshot after waiting for
checks or a human action.

## Checks

Watch required checks when the repository configures them:

```sh
gh pr checks <number-or-url> --watch --required
```

If no required checks are configured, this command cannot prove readiness. Compare `statusCheckRollup` with the
checks named by repository policy. Do not count missing, pending, canceled, stale, or unexpectedly skipped checks as
passing.

Retry only a clearly identified infrastructure failure, once, on the same head SHA. Prefer rerunning failed jobs in
the existing run. Re-read both the run and PR head after the retry. Never use an empty commit as a retry mechanism.

## Review identity

Inspecting a PR is read-only. These are representational writes and require suitable identity plus explicit authority:

- `gh pr review`
- PR or review comments
- approval or change-request decisions
- resolving another person's discussion

When authenticated as a human whose judgment the agent does not own, keep review evidence in the task's approved
review system and do not publish it as that human.

## Merge observation

If another person owns the merge, wait through the harness's supported monitor rather than polling aggressively.
Notify on state changes, failures, or a required human action, not unchanged status.

After GitHub reports the PR merged, capture the returned merge commit and inspect the base-branch run for that exact
commit. Do not infer completion from the source branch disappearing. If the PR closed without `mergedAt`, stop and
report that it was not merged.

Do not invoke `gh pr merge`, enable auto-merge, delete branches, create tags or releases, or publish packages unless
the current task separately authorizes that action.
