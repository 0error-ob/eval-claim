# Run Type Boundary Template

Use this template before reporting a benchmark run. The goal is to label what kind of evidence the run produced before turning it into a public claim.

---

**Run name / ID:** Short stable identifier.

**Benchmark / task set:** Benchmark name, split, task count, and whether this is full-set or subset.

**Actor:** What system was evaluated: model only, CLI agent, scaffold, harness wrapper, human-assisted session, or reference implementation.

**Evidence surface:** What the actor was allowed to inspect. Examples: prompt only, docs, executable behavior, visible tests, source code, public web, traces from previous runs.

**Harness conditions:** Any conditions that affect comparability: timeout, resources, concurrency, retries, tools, hidden-test access, local patches, environment changes.

**Run type:** Choose the tightest label:

- `leaderboard-comparable full run`
- `internal full run under declared modified conditions`
- `targeted retry`
- `subset smoke test`
- `no-probe baseline`
- `probe-ledger scaffold run`
- `black-box cleanroom`
- `test-informed repair`
- `source-reference control`
- `demo only`

**Primary result:** Score, pass count, resolved count, or qualitative outcome.

**Allowed claim:** The strongest statement this run supports.

**Disallowed claim:** The tempting stronger statement this run does not support.

**Comparability:** What this can and cannot be compared against: official leaderboard, previous internal run, targeted subset, ablation, source upper bound, or no direct comparison.

**Ablation needed:** What must be removed or held fixed to attribute the result to a specific model/scaffold/tool/verifier change.

**Publication boundary:** What can be public now, and what should stay private while the benchmark effort is active.

---

## Example Labels

**Reference-source control**

Allowed claim: the evaluator and build path can reach the reference upper bound under these conditions.

Disallowed claim: the agent solved the task.

**Test-informed repair**

Allowed claim: the implementation improved using visible tests plus allowed non-source evidence.

Disallowed claim: pure black-box cleanroom reconstruction.

**Targeted retry**

Allowed claim: a failure class recovered under changed conditions on a selected slice.

Disallowed claim: leaderboard-comparable full-run score.

**Internal full run under modified conditions**

Allowed claim: full task-set result under declared local conditions.

Disallowed claim: direct official leaderboard equivalence if timeout/resources/tools differ.
