# Agent Benchmark Claim Card

A structured card to fill in before publishing a benchmark result. Each field anchors a specific kind of claim to a specific kind of evidence. If a field cannot be filled, the gap is part of the claim — leave it blank and acknowledge it.

This is a publication-time artifact. The companion runtime artifact is [agent-run-ledger.schema.json](../schemas/agent-run-ledger.schema.json) — the structured ledger an agent produces during execution. The claim card cites the ledger as its evidence base.

Vocabulary: [task-ontology](https://github.com/0error-ob/task-ontology) — primitives and dimensions.

---

## 1. Run identity

**Run ID:** A stable identifier for this run (e.g. `tbench-2.1-k5-v01`). Should appear inside any uploaded `result.json` / `metadata.yaml` for cross-reference.

**Date:** When the run completed (ISO date).

**Author:** The person or team responsible. Submission name (not company), if anonymity matters.

## 2. Benchmark

**Benchmark name:** Public identifier of the benchmark.

**Dataset:** The dataset string as recorded in result artifacts (e.g. `terminal-bench/terminal-bench-2-1`).

**Version:** Benchmark version. State explicitly — TB 2.0 and TB 2.1 are different task sets.

**Source field:** Where the version is determined inside the artifact (e.g. `source` field in result.json). Required when path-based version is ambiguous.

## 3. Agent

**Agent display name:** As it should appear on a leaderboard.

**Public repo:** URL to the agent's source code at the exact commit/tag submitted.

**Tag / commit:** The immutable reference. A `tag` is preferred over a branch.

**File SHA256(s):** SHA256 hashes of the load-bearing files in the submitted agent. At minimum, the main agent entrypoint.

## 4. Model

**Model identifier:** Provider-namespaced model ID (e.g. `anthropic/claude-opus-4-7`).

**Provider / endpoint:** Where the model was actually called (e.g. `openrouter`, `openai`, `anthropic`). Distinct from the model identifier — the same model accessed through different endpoints may differ in throughput, rate limits, and sometimes routing.

**Routing notes:** Any prefix conventions (e.g. LiteLLM `openai/` prefix indicates an OpenAI-compatible endpoint, not the model vendor).

## 5. Harness configuration

**Harness:** Name and version (e.g. `harbor 0.6.4`).

**Configuration:** Concurrency (`-n`), trials per task (`k`), timeout multiplier, resource overrides. State explicitly that defaults were unchanged where this matters for compliance.

**Compliance:** A checklist mapping to the benchmark's stated rules. For each, mark satisfied / not satisfied / not applicable.

## 6. Run type

**Run type:** What kind of submission this is — public submission, internal calibration, ablation, smoke test, partial run. Each licenses different inferences.

**Total trials:** Tasks × trials-per-task. Verifiable count of result artifacts.

## 7. Evidence surface

**Artifacts produced:** Per-trial `result.json`, per-trial ledger, raw agent transcripts, verifier outputs, exception logs. List what exists and what was retained.

**Artifacts uploaded:** A subset of the above. Different submissions upload different surfaces — state what this submission uploaded, and what was kept private.

**Inspectability:** How a reviewer can verify the claim — reproduce the run, inspect the artifacts, audit the agent code at the tag.

## 8. Metric distinction

**Leaderboard metric:** The specific metric the leaderboard scores by (e.g. task-level pass@k). Cite the benchmark's documentation.

**Other reported metrics:** Any other metrics the run produces (e.g. trial-level mean reward). These answer different questions; state which question each answers.

**Headline number:** Which metric is being reported as the headline. The number must come from the leaderboard metric, not a derived or alternative metric.

## 9. Result

**Headline:** The leaderboard-aligned score, with denominator. Not just a percentage.

**Disaggregation:** Per-task-family or per-trial-level breakdown when relevant. Avoid claiming aggregate when the disaggregation tells a different story.

## 10. Known exceptions

**Infrastructure exceptions:** Counts and categories of trials that ended outside the agent's control (Docker rate limits, command timeouts, provider errors). State explicitly whether these were counted as failures or excluded.

**Failure handling:** The policy used — strictly counted-as-failure is the conservative default for public claims.

## 11. Ablations

**Held constant:** What did not change in this run that might have in another version of the same agent (model, scaffold version, harness flags).

**Varied:** What is different from any reference comparison point (e.g. comparison against an earlier submission with the same model). State the controlled difference.

**Not ablated:** Variables not held constant or systematically varied. The headline number cannot speak to these.

## 12. Allowed claims

State, in plain sentences, what conclusions the evidence licenses. Each sentence should be defensible by pointing to a field above.

Common allowed claim shapes:
- *Under {harness, model, dataset}, this agent produced {score} on {leaderboard metric}.*
- *Holding {variables} constant, this configuration differs from {reference} by {delta}.*

Do not state more than the evidence surface and ablation structure support.

## 13. Unsupported claims

State, in plain sentences, what conclusions a reader might reasonably draw but the evidence does not support.

Common unsupported claim shapes:
- *This model is stronger than other models.* (Cross-model claim; requires holding the agent constant across models.)
- *This agent is model-agnostic.* (Generalization claim; requires evidence across models.)
- *This agent generalizes to other benchmarks.* (Cross-benchmark claim; requires evidence across benchmarks.)
- *The score reflects only the agent's contribution.* (Attribution claim; requires a baseline holding the agent variable.)

If the run does support one of these claim shapes, move it to section 12 with the supporting evidence cited.

## 14. Reviewer questions

A list of three to five questions a careful reviewer should ask. These are not weaknesses — they are the most productive entry points for someone deciding whether to use, cite, or extend this work.

Examples:
- Does the harness configuration match the benchmark's stated rules?
- Are exception trials counted in the headline?
- What does the leaderboard metric *not* see in this run?
- Has the agent at this SHA256 been run on any other benchmark?

---

## Worked example

See `examples/` for filled-in cards on specific submissions. A claim card without a worked example is a form; with a worked example, it becomes a pattern.
