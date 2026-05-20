# Use Task Ontology in 10 Minutes

For a single-claim analysis, use [templates/claim-reading.md](./templates/claim-reading.md).

This file turns the vocabulary in [PRIMITIVES.md](./PRIMITIVES.md) and [DIMENSIONS.md](./DIMENSIONS.md) into three diagnostic templates. Each template applies the same six questions to a different class of agent-evaluation claim.

The questions are deliberately the same across templates. The point of an ontology is that the same lens fits multiple scenarios.

For worked applications, see [examples/](./examples/).

---

## The six questions

Apply in order. Answer each in one sentence. If a question cannot be answered in one sentence, the claim is under-specified.

1. **What task is being constructed?** The actor, the goal, the operating environment, the action space. Not the score — the *task object*.
2. **What is the oracle?** Programmatic test suite, reference-answer match, LLM judge, human evaluator, implicit user satisfaction, or no oracle.
3. **Which task dimensions dominate the result?** From DIMENSIONS.md: time horizon, observability gap, decomposition depth, verification regime, ambiguity load, irreversibility surface, etc. Usually 1–3 dominate.
4. **What does the metric see?** The literal output of the scoring interface.
5. **What does the metric hide?** Components of task structure the metric collapses, ignores, or cannot observe.
6. **What inference is unsafe?** A conclusion a reader might reasonably draw from the metric that the metric does not actually warrant.

---

## Template 1 — Benchmark claim

**Trigger:** *"Model X scored Y on benchmark Z, therefore..."*

1. **Tasks constructed?** What the agent had to do. Not the score, the task.
2. **Oracle?** Test suite (SWE-bench), reference match (GAIA), LLM judge (chat benches), human (rare).
3. **Dominant dimensions?** Look at the typical sample. SWE-bench: oracle-rich, repo-scale, regression-prone. GAIA: research-style, long-horizon, ambiguous oracle. Different benchmarks have different shapes.
4. **Leaderboard sees?** Pass rate, pass@k, or composite — almost always a single scalar.
5. **Leaderboard hides?** Per-task-type variance, failures-of-coverage, harness contribution to the score.
6. **Unsafe inference?** *"Model A > Model B because A scored higher."* Capability ≠ score when harness, prompt, or oracle differ between runs.

**Common error:** Reading the leaderboard number as a property of the model. It is a property of the *(model, harness, prompt, oracle, sample distribution)* joint object.

**Worked example:** [examples/benchmark-leaderboard-claim.md](./examples/benchmark-leaderboard-claim.md)

---

## Template 2 — Agent regression claim

**Trigger:** *"The agent got worse"* / *"This update regressed"* / *"metric X dropped over the last N days"*

1. **Tasks constructed?** Usually a *stream* of related-but-not-identical tasks, varying session by session along several dimensions.
2. **Oracle?** Often the end user (accepts / rejects / abandons / requests rework) — and often *not* visible to the observability tool measuring the regression.
3. **Dominant dimensions?** Time horizon, context locality, verification regime, mutation pattern. Idiosyncratic per user-week.
4. **Metric sees?** A scalar or vector over a time window — typically pre/post means of session-level features.
5. **Metric hides?** Two distinct causes that produce identical metric shifts: model-side behavior change vs user task-mix change.
6. **Unsafe inference?** *"The model regressed"* derived from a metric shift, without controlling for task structure across the before/after windows.

**Common error:** Reading a task-mix shift (user did more debugging this month) as model regression.

**Worked example:** [examples/agent-regression.md](./examples/agent-regression.md)

---

## Template 3 — Model-switching / migration claim

**Trigger:** *"We should move from model A to model B"* / *"Open-source model X is now good enough"* / *"Cheaper model Y can replace stronger model Z"*

1. **Tasks constructed?** What kind of work is the migration target supposed to handle? Single-shot Q&A, oracle-rich coding, long-horizon agent loops, web navigation? Each implies a different bar.
2. **Oracle?** Same question per task class — and worth checking that the oracle is *consistent* across the comparison points (same test suite, same human pool, same LLM judge prompt).
3. **Dominant dimensions?** Compare task profiles between the two regimes. If the migration target's tasks differ in horizon or context locality from the source's, the comparison isn't apples-to-apples.
4. **Metric sees?** Aggregate quality (pass rate, win rate, user satisfaction) and aggregate cost (tokens, latency, dollars).
5. **Metric hides?** Per-task-type performance gaps. A cheaper model may match the stronger one on short oracle-rich tasks while collapsing on long-horizon work.
6. **Unsafe inference?** *"Model B is good enough"* generalized from a sample dominated by easy task profiles.

**Common error:** Treating "good enough on average" as "good enough across the workflow."

**Worked example:** [examples/model-migration-eval.md](./examples/model-migration-eval.md)

---

## Scope

- Not a framework. No API, no SDK, no required workflow.
- Not exhaustive. These three templates cover the high-frequency scenarios; others can be added when external use surfaces them. See [CONTRIBUTING.md](./CONTRIBUTING.md).
- Not a substitute for [PRIMITIVES.md](./PRIMITIVES.md) / [DIMENSIONS.md](./DIMENSIONS.md). The templates use that vocabulary; if a primitive feels missing from a question, follow the question back to the canonical definition.

If a real-world claim doesn't fit any of the three templates, the right response is to ask what new template would, not to force-fit.
