---
name: codex-consult
description: Ask Codex CLI (gpt-5.5) for independent read-only analysis, codebase exploration, architecture advice, debugging insight, implementation guidance, or a second opinion. Use when the user asks Claude to consult Codex or gpt-5.5 without delegating edits, or when another model's perspective would improve a technical decision. Do not use when Codex should modify code or perform a formal code review; use codex-implement or codex-review instead.
---

# Codex Consult

Use Codex as an independent technical consultant for questions that benefit from another agent's analysis but do not require Codex to edit files.

Suitable tasks include:

- understanding unfamiliar code
- tracing behavior through a repository
- investigating likely causes of a bug
- comparing implementation approaches
- evaluating architecture or migration options
- identifying relevant files and dependencies
- answering repository-specific technical questions

Prefer answering directly for simple questions that Claude can resolve confidently without delegation.

Treat Codex's response as evidence and analysis, not authority.

## Workflow

1. Define the question or decision Codex should analyze.
2. Gather relevant requirements, symptoms, logs, files, and prior investigation.
3. Create a temporary artifact directory for the prompt and report.
4. Run `codex exec` in a read-only sandbox.
5. Read the report and verify important repository-specific claims.
6. Synthesize the useful findings into Claude's own response.

Use this command shape:

```bash
ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-consult.XXXXXX")"
REPORT="$ARTIFACT_DIR/report.md"
PROMPT="$ARTIFACT_DIR/prompt.md"

codex -C "$PWD" exec \
  --ephemeral \
  --sandbox read-only \
  - < "$PROMPT" > "$REPORT"
```

## Consultation Prompt

Ask a focused question and specify the desired evidence:

```text
Act as an independent senior software engineer and analyze the following question.

Question:
[State the question or decision clearly.]

Context:
[Provide requirements, symptoms, relevant files, logs, prior findings, and constraints.]

Instructions:
- Inspect the relevant repository code and documentation.
- Do not edit any files.
- Base repository-specific claims on concrete evidence.
- Distinguish confirmed behavior from assumptions or speculation.
- Cite relevant files, symbols, and line ranges when possible.
- Consider edge cases, risks, compatibility, and operational impact.
- Prefer a clear recommendation over an unranked list of possibilities.
- State what additional information would be needed where the evidence is insufficient.

Return:
1. direct answer or recommendation
2. supporting evidence
3. important trade-offs or risks
4. unresolved questions
5. suggested next steps
```

Tailor the requested output to the task. For example, ask for a call-flow trace, root-cause hypothesis, migration comparison, dependency map, or architectural recommendation.

## Verifying the Analysis

Before relaying repository-specific conclusions:

- inspect the most important cited files or symbols
- confirm that Codex interpreted the current code rather than an outdated pattern
- verify commands, configuration names, and API behavior when consequential
- separate confirmed findings from plausible hypotheses
- resolve disagreements between Codex and Claude using the available evidence

Do not present an unverified hypothesis as a confirmed root cause.

## Reporting Back

Answer the user's actual question rather than reproducing the entire Codex report.

Lead with the conclusion, then include the strongest evidence and relevant trade-offs. Mention that Codex was consulted only when that context is useful to the user.

If Codex cannot determine the answer, explain what was inspected, what remains unknown, and the most useful next investigation step.

If `codex` is not installed or the command fails, report the error and perform the analysis directly instead.
