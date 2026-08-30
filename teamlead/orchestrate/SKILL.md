---
name: orchestrate
description: Coordinate a multi-day engineering program across tracks, sessions, durable units, human gates, verification, and integration. Use only from an authorized Lead, Teamlead, or Orchestrator after loading the orchestrator skill, and only when work outlives one agent or ticket.
---

# Orchestrate

The lead owns the program, not the code. It authors briefs, drains the queue, keeps integration safe, and decides. Use
this for multi-day work, many PRs or units, and repeated agent handoffs. One ticket routes to `ticket-flow`; one
ambitious run with an unusual phase shape routes to `custom-workflow`. If one agent can finish inside the session's
budget, stop here. This process will make small work slower.

This is a coordinator flow. Read the installed `orchestrator` skill and its shared conventions before starting. If
the current task does not grant coordinator authority, do not launch or manage workers.

Ceremony must scale with the program. Every gate below prices in coordinator minutes; on cheap near-identical units, collapse it as each section directs rather than paying list price.

Four rules carry the rest.

- Completions are queue events, not interrupts.
- Every spawn and every resume carries the standing orders verbatim.
- The brief is the product. A vague brief fails quietly and multiplies drift across workers.
- One declared source owns each fact. Never mirror a tracker or PR host into a competing ledger.

Open a todolist with the steps below copied in verbatim. A step you skip stays listed with `skip: <reason>`.

#### Roles and placement

- **Coordinator.** Frames, authors track briefs, drains the inbox, owns the human report, orders integration, and makes
  program-level judgment calls. It does not write feature code, review diffs, or mutate external systems unless the
  program contract grants that exact authority.
- **Track Orchestrator.** One per large work context or independent track, only when one coordinator cannot drain the
  whole program. It may be a separate full harness session, another task, or an in-process child when the harness
  supports it. Inside a harness whose workflow requires visible task tabs, it must instead be a persistent interactive
  process in its named track tab; a hidden child or headless command is not a full Track Orchestrator session. It owns
  its bounded unit list, worker briefs, verifier flow, and permitted tracker or PR writes, then returns a compact
  rollup.
- **Integrator.** The only role allowed to rebase, retarget, resolve cross-unit conflicts, push integration changes, or
  merge within its declared lane. A Coordinator or Track Orchestrator becomes an Integrator only when the program
  contract says so; coordination authority alone grants no repository mutation.
- **Worker / verifier.** Assign one terminal `explore`, `plan`, `build`, or `review` skill. Prefer fewer, broader
  workers. Give every writer an exclusive worktree, branch, or path set. Run judgment-heavy verification through a
  fresh terminal Reviewer when independence matters.

Depth stays at coordinator, track, worker. Author the track decomposition per project (build, landing, and verification are common cuts, not a required shape); hard-coded swarm trees were tried and parked as too rigid.

#### Authority and state backing

Before the first spawn or external write, record the program's authority matrix: which systems the Coordinator may
read and write, who owns each track, who may change tracker state, who may update PRs, who integrates, and who merges.
Installed tools and credentials do not grant authority.

Choose exactly one state mode:

- **Local-store mode.** The program has no stronger durable tracker, so the `orch` store owns units, decisions,
  verification, gates, and the frontier.
- **Tracker-backed mode.** The project's issue tracker, PR host, and repository rules own their existing facts. Read
  them live. Do not mirror issue status, assignment, decisions, review verdicts, checks, PR revisions, or merge state
  into `units.tsv`, `ledger.tsv`, `overview.md`, or another competing record. Private scratch may hold standing orders,
  completion pointers, resource leases, and a derived status cache; it must name the authoritative source and be safe
  to discard.

In tracker-backed mode, route each durable write to the role that owns it. A read-only Coordinator reports or relays a
needed write; it never performs the write merely to keep the program moving.

#### Local-store layout

Use this section only in local-store mode. Create `orchestrate/<project-slug>/` in the current lead's durable
workspace. Every file has exactly one writer; owners publish facts and readers aggregate. Set `ORCH_STORE` to that
directory or pass `--store <dir>` when running
`bun scripts/orch/orch.ts`. The canonical TSV, JSON, and Markdown remain readable without the CLI. In the commands
below, `orch` means that full command with the store configured.

- `preferences.md` is the standing-orders register: numbered lines, one constraint each. Paste it into every spawn
  and resume. When a rule needs repeating, add it to the register before the next spawn.
- `overview.md` is the durable PR and issue DB. Append; never rewrite wholesale per event.
- `units.tsv` has one row per unit: id, track, state, branch, PR, head SHA, brief path. Update rows in place.
- `frontier.json` is the computed merge frontier, per Stack safety.
- `ledger.tsv` is the verification ledger, per Verification.
- `inbox/` holds completion pointers. `gates.md` parks human gates (question, options, default on no answer) so a completion flood cannot wipe AskQuestion state.
- `decisions.tsv` is the trail written with `decision-log`.
- `status.md` is derived from `units.tsv` and `ledger.tsv` at each drain, never hand-maintained; regenerate it from the tables instead of narrating events into it, because hand-churned boards get rewritten on every event and go unreadable.

#### The brief

Your prompts to agents are your only product, and a sloppy brief compounds into slop across the whole tree. Every spawn carries all of it; a field you cannot fill is a unit you have not scoped yet.

```
GOAL         one sentence, the outcome, executable by a stranger with no chat access
SCOPE        paths this unit may write; paths it may not; its exclusive worktree or branch
CONTEXT      pointers to files and PRs; upstream reports pasted in full when this unit
             depends on them, because workers cannot see siblings
ACCEPTANCE   checkable criteria, one per line
VERIFY       exact commands or the control-skill path, plus known gotchas
TIMEBOX      rough cap on runtime; on expiry, return partial findings and stop rather than run on
FORBIDDEN    no gt, no rebase, no force-push, no fixes outside scope, plus unit-specific bans
REPORT       status, branch, head SHA, PRs, verdict, what you actually ran, deviations,
             suggested follow-ups
STANDING     <preferences.md pasted verbatim>
```

Size the brief to the unit. A one-command unit gets a paragraph that still names goal, scope, check, and report. A
long scaffold around a two-line edit costs more to write and obey than the edit. A local agent may read the standing
orders by path; every resume gets them again.

A Track Orchestrator brief adds its session or track boundary, unit list, external-write authority, owned paths and
branches, dependency inputs, shared-resource protocol, spawn budget, drain protocol, and compact rollup format.

A dependency is a context relay, not just ordering: undeclared upstream context makes the worker guess. Missing fields are a refuse-to-spawn condition. Audit one sampled worker brief per sub-coordinator per wave, concurrently with the wave it samples, never as a gate in front of it; a failing brief stops that track and fixes the sub-coordinator's instructions, not just the worker, because brief quality decays late in a run. Never resume-chain a brief; respawn fresh with consolidated scope.

#### Steps

1. **Frame.** State a countable done predicate. Quantify units, effort, tracks, and time. If one agent can finish inside
   that budget, collapse to direct or ticket work with inline verification. Name tracks from the actual project. Use
   `arena` for a contested decomposition. Declare the authority matrix and state mode. Review the program contract
   with the user once before scaling.
2. **Install the runtime.** In local-store mode, run `orch init`, open `decision-log`, write standing orders, and seed
   `frontier.json` from existing PRs with `orch frontier set --repo <repo-dir>` only when the repository uses Graphite.
   In tracker-backed mode, resolve the live tracker, PR, repository, and harness state; keep only the permitted scratch
   state. Do not initialize a duplicate unit or verification ledger.
3. **Pilot.** Push one unit through the whole path: brief, worker, verification, canonical evidence, and landing when the
   program includes it. The pilot exists to falsify the brief template, verify recipe, unit size, and state routing
   while that costs one agent instead of fifty. Fix the contract from pilot evidence before fan-out. On programs of
   near-identical cheap units, the first normal unit is the pilot and fan-out starts when it lands. A separate verifier
   and audit gate are for expensive or novel unit shapes, not clone-units where a serialized pilot proves little.
4. **Scale.** Spawn a rolling window of workers up to the in-flight cap, refilling as children finish; blocking batches pay the slowest child of every batch. Spawn Track Orchestrators only past the one-drain threshold in Roles. Recompute ready work after each drain; relay upstream reports into downstream briefs; keep sibling communication upward through the Coordinator. Direct sibling communication is for urgent technical context, is copied upward, and never grants one track authority over another. The sampled brief audit runs alongside the wave it samples and stops the next refill on failure, not the current one.
5. **Drain.** Run the queue discipline below at every drain point.
6. **Land.** Landing is continuous, never a terminal phase. The Coordinator orders the landing queue and protects the
   current frontier; the declared Integrator performs repository mutations. A read-only Coordinator hands the slot to
   the owning track or Integrator and observes the result. Keep the frontier green before dependent work; Integration
   safety governs.
7. **Close.** Drain the inbox, reconcile every spawned agent against the canonical state, confirm the predicate on the
   real artifact, confirm every landed PR has a current verdict, audit durable decisions, and encode recurring
   corrections into standing orders, a skill, or a check. Leave the local store intact for review only in local-store
   mode.

#### Queue and drain

- On a completion notification, enqueue the pointer and return to what you were doing. In local-store mode use `orch inbox push <agent> <unit> <status> [--report PATH]`; in tracker-backed mode use the harness queue or permitted scratch. Never deep-review inline; a completion that needs review becomes a verifier unit. Never review a diff inside a drain.
- Drain in batches at the end of a critical section, a track rollup, a harness completion notification, and
  before a human report. In local-store mode begin with `orch inbox drain`; otherwise drain the harness queue and
  re-read changed external facts. Arrivals during a drain wait for the next one.
- Critical sections you finish first: authoring a brief, a stack operation, a conflict decision, writing a gate, updating ledger or frontier.
- Each drain classifies every pointer (landed, needs-verify, failed, zombie, noise), reconciles it with the chosen
  source of truth, then starts the next ready work in one message. Only local-store mode writes `orch` unit and ledger
  rows. Tracker-backed writes stay with their declared role.
- Before a track yields on pending CI, review, human merge, or landed checks, assign a watcher owner and record the
  exact target plus wake condition. Use the active harness's persistent wait mechanism. Do not rely on the human to
  notice that an external gate finished and prompt the program to resume.
- Account for every spawned child at its track's rollup: arrived, respawned, or its scope explicitly absorbed. Silently redoing a missing child's work hides both the wasted spend and the coverage gap its result existed to close.
- A drain turn ends with three facts from the canonical sources: counts against states, what changed, and open human
  gates. In local-store mode derive them with `orch status`; in tracker-backed mode derive them live without copying
  the backing records. The full reply contract applies at checkpoints and close.

#### Integration safety

- The frontier is computed from the chosen source, never narrative. In local-store mode, Graphite projects recompute
  `frontier.json` with `gt` after every stack change. Tracker-backed projects read ordered PRs, base revisions, exact
  head SHAs, checks, and merge state from their normal source of truth.
- Exactly one Integrator per landing lane may rebase, restack, retarget, resolve integration conflicts, or merge.
  Record the role in standing orders and the authority matrix.
- Workers never mutate a shared branch or stack unless their brief explicitly assigns the Integrator role.
- PR closes, retargets, conflict fixes, and merges go through the declared Integrator or human owner. The Coordinator
  chooses order and routes work; it does not acquire mutation authority from the conflict.
- Treat shared check capacity, performance profilers, dev servers, browsers, and mutable main checkouts as named
  resources. The Coordinator grants one lease at a time when concurrent use would corrupt evidence or state.
- Updating a shared local base checkout after merge requires explicit Integrator authority and its resource lease.
  Remote landed evidence or an isolated checkout is the default; merge authority alone does not permit local-base
  mutation.
- One retro watcher follows merged PRs for reverts, post-merge CI breaks, and orphaned follow-ups.

#### Verification

Scale verification to the unit. When VERIFY is a single cheap command, the worker runs it and reports the output, and the coordinator spot-checks receipts; a dedicated verifier agent (on a different model family than the worker) is for units whose verification is expensive, judgment-laden, or high-blast-radius. A verifier agent whose entire product would be rerunning one command is ceremony, not verification.

Keep flaky-check diagnosis bounded: start with one focused reproduction and at most one controlled comparison. Do not
grow the run into a repeat matrix across worktrees, orderings, or timing modes unless the approved brief calls for
statistical evidence or the first comparison leaves more than one plausible cause. Reuse current canonical evidence
when neither the tested logic nor the exact revision changed.

In local-store mode, write ledger rows with `orch ledger record` and check the current PR and head SHA with `orch ledger check`. In tracker-backed mode, use the project's canonical review and verification records and do not copy them into `ledger.tsv`. In either mode, bind each verdict to the exact revision. CI green is an input to a verdict, not a verdict. Behavioral work needs more than a type check. A blocked or failed verifier is not a pass, and a new head or changed effective diff voids the earlier verdict.

A unit is not done until its role report has returned and its output and verification are recorded in the chosen
durable source. Durable evidence does not replace a missing terminal handoff, and a handoff does not replace required
durable evidence. Work that exists only in one session or checkout when it dies was never done.

#### Liveness and failure

- Never send a follow-up merely to check liveness; that can restart an idle harness. Probe read-only through the
  active harness and the chosen tracker, PR, branch, or local-store evidence. Transcript mtime is not liveness.
- A silent death gets a synthetic postmortem row in the inbox (unit, failure mode, last evidence, options). Replan on evidence as it arrives; never wait for full quiescence.
- Retry by mode: cap-hit or oom, respawn with smaller scope; network-drop, retry as-is; tool-error, retry on a different model; unknown, retry once. Two retries, then abandon the unit and replan around it.
- A zombie that returns hours late reconciles against the current frontier and canonical verification record before anything is accepted; the world moved while it slept. Salvage unique findings through a fresh unit, never a blind merge.
- When continued spawning would produce garbage tree-wide (bad upstream output, broken acceptance, dead infra), write a stop line at the top of the standing orders, let in-flight work finish, fix the cause, clear it.
- Bound your own infra retries the same way you bound a child's. After a few consecutive tool aborts, stop retrying: write a terminal handoff to durable state (what is done, where it lives, the exact command to resume) and end the run. Hours of retry loops against a dead executor produce nothing a handoff would not.
- After a harness restart, assume nothing about agent liveness. Re-read standing orders and the chosen source of
  truth, resolve current sessions or tasks, recompute the frontier, and reattach work by branch, PR, issue, and
  artifact rather than stale agent IDs. In local-store mode, `orch` replaces a lock whose holder process is gone.

#### Escalation

Reaches the human, batched into the status page rather than per item: irreversible actions (force-push to shared branches, deploys, deletions, closing someone else's PR), genuine product or preference calls no experiment settles, a standing order that contradicts observed reality, a program-level dead end that survived a replan. In local-store mode park each as a `gates.md` entry. In tracker-backed mode use the project's declared Owner-gate path through the role allowed to write it; a read-only Coordinator keeps only a derived open-gate index and routes work around it.

Never reaches the human: frontier nudges, restack mechanics, retries, CI flake triage, review-thread triage, format fixes, scope the brief already forbids (refuse and continue), and "should I keep going". When in doubt, act and log; deferring is the measured failure mode.

Mid-run discoveries fix only what blocks the frontier. Everything else parks in follow-ups; at this fan-out a small scope leak multiplies into PRs nobody asked for.

**Reply:** at checkpoints and close: the predicate and count from the canonical sources, tracks and what each landed,
the frontier (PR list plus exact SHAs), verdict summary, abandoned work and reason, and gates awaiting the human. Name
the state mode and sources. Include the store and decision-trail paths only in local-store mode. Include PR links.
