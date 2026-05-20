# 001 — Saturation narrows inference

**Type:** Benchmark score claim  
**Question:** What inference does this score still support?  
**Status:** Claim reading, not benchmark criticism

A leaderboard score does not become useless all at once. As a benchmark approaches its task-distribution ceiling, what changes is not whether the score means something — it is the set of claims the score can still support.

This note records the observation in transferable form.

## The structural shift

At 40% versus 90%, a score gap is probably saying something robust about the systems being compared.

At 93% versus 90%, the gap is dominated by the measurement setup itself: the sample distribution, the harness, the prompt scaffolding, and the oracle's particular shape. The score still moves. What it tracks has shifted — from *capability on the underlying task family* to *fit with the benchmark's particular construction of that task family*.

This is not the same as "the benchmark is broken." Closer to: the benchmark is now answering a different question.

## What a saturated score still supports

- A regression check on the existing system — does this run still pass what previous runs passed?
- Evidence that a system can handle a specific class of construction. For SWE-bench Verified, that means oracle-rich Python repo issues with fixed test verifiers.
- A floor on coverage of the historically-included task types.

## What a saturated score no longer safely supports

- *Higher score = stronger frontier coding capability*, without further decomposition.
- Comparative ranking of frontier systems on dimensions outside the benchmark's task construction.
- Inference about behavior on tasks structurally different from the saturated set: longer horizons, weaker oracles, multi-file edits with no test signal, novel domains.

## What would re-open the inference space

A saturated headline number can be re-opened by reporting alongside it:

1. **Headroom map** — which instances remain unsolved, and what structural property distinguishes them from the solved instances.
2. **Failure-mode taxonomy** — among the unsolved instances, which kinds of failure recur (oracle exploitation, underspecification, test-suite ambiguity, cross-file dependencies).
3. **Joint-object decomposition** — what fraction of the score is attributable to the model itself versus the harness, the prompt scaffolding, and the oracle's shape. A score is always a *(model + harness + prompt + oracle)* measurement; saturation makes the non-model components dominant in any remaining score gap.

The interesting comparison is no longer *did System B pass more tasks than System A?* It is: *did System B pass more of the tasks that System A failed?*

## Why this matters

A saturated benchmark whose report still claims frontier discrimination is making a stronger inference than the data supports. The repair is not necessarily a new benchmark. It is a different report on the same benchmark.

## Origin

This note formalizes a comment posted in the [HN discussion of *SWE-bench Verified no longer measures frontier coding capabilities*](https://news.ycombinator.com/item?id=47910388), under a sub-thread distinguishing 40-vs-90 score gaps from 93-vs-90 score gaps.
