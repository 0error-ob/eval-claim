# Worked example: Model migration eval

**Scenario.** A team is considering moving from Model A on Harness H1 to Model B on Harness H2. Their internal eval, run over a 200-session bag assembled from recent production traffic, reports that aggregate quality is comparable — Model B lands within 2 points of Model A on the bag's headline metric — and aggregate cost is roughly 70% lower per session. The proposal lands as: *"Model B is good enough; let's migrate."*

This is a recurring class of decision. The pattern below applies whenever migration is justified by aggregate metrics over a heterogeneous task mix.

We apply [Template 3 — Model-switching / migration claim](../QUICKSTART.md#template-3--model-switching--migration-claim) from QUICKSTART.

---

## 1. What task is being constructed?

Not one task. The eval is a *bag* of session traces drawn from recent production work. That bag is heterogeneous: short single-shot lookups, multi-turn coding loops, long-horizon investigations, occasional high-irreversibility operations.

The actor is the *(model + harness + prompt template)* composite — and the migration changes two of these three. *Model A on H1* and *Model B on H2* are two different composites. The eval compares two composites, not two models.

If H1 and H2 were identical, the comparison would isolate a model effect. They are not. So the eval surfaces a composite gap, and any inference that names "the model" must account for the harness shift carrying part of the gap.

## 2. What is the oracle?

It depends on the task class inside the bag. Programmatic tasks: a test runner or assertion. Chat-style tasks: a reference answer or LLM judge. Long-horizon agent work: typically the user (accept / reject / rework) — and the user is rarely captured in an offline bag.

The migration question requires the oracle to be the *same* across both comparison points. If sessions in the bag were originally judged by the user during live operation, an offline re-scoring is a different oracle than the one those sessions ran under. A "comparable" aggregate under offline judgment can hide a sizable gap under live user verdict.

## 3. Which dimensions dominate the result?

From [DIMENSIONS.md](../DIMENSIONS.md), the dimensions where migration risk concentrates:

- **Time horizon** — short sessions are easier; long sessions accumulate failure
- **Context locality** — local-file work compresses; repo-scale or cross-system work amplifies the gap
- **Decomposition depth** — shallow tasks compress; deep tasks expose planning weakness
- **Verification regime** — oracle-rich tasks self-correct; oracle-light tasks degrade silently
- **Irreversibility surface** — low-risk tasks tolerate noise; high-risk tasks do not

Recent production bags are typically dominated by short, local, oracle-rich sessions, because routine work is the most common kind of work. Aggregate quality on such a bag is structurally insensitive to the long-horizon, repo-scale, oracle-light tail where Model B is most likely to break.

## 4. What does the metric see?

Two scalars per session, aggregated:

> Aggregate quality (pass rate, win rate, or judge score) and aggregate cost (tokens, latency, dollars).

Plotted side by side, the migration story emerges: similar quality at substantially lower cost.

## 5. What does the metric hide?

**Per-task-cohort gaps.** A 2-point aggregate gap can decompose into a near-zero gap on the routine majority and a 15-point gap on the long-horizon minority. The aggregate compresses these into a single number that reads as safe.

**Sample-distribution effects.** If the bag overweights easy work — and recent production traffic typically does — the aggregate is dominated by tasks where most reasonable models pass. The gap on hard work, where the migration decision should turn, is structurally underrepresented.

**Harness contribution.** Part of the apparent quality match comes from H2 doing more work — better retries, better tool routing, more aggressive prompting. That work is real, but it is a property of H2, not of Model B. If H2 is brittle in the unmeasured tail, the aggregate quality is borrowed from the harness, not earned by the model.

**Failure-mode cost.** Cost is averaged per session. The cost of a session that *fails on a high-irreversibility task* — and triggers human cleanup, downstream rework, or worse — is not captured by per-session token cost. Aggregate cost savings can be erased by a small number of bad outcomes the metric does not see.

## 6. What inference is unsafe?

> *"Model B is good enough; let's migrate."*

This inference is unsafe when:

- The eval bag is not stratified by task structure, so the per-cohort gap is invisible
- The harness shift is folded into the model comparison, so the apparent "model" gap is actually a *(model + harness)* gap
- The oracle used in the eval differs from the oracle that will judge work after migration
- High-irreversibility task classes are present in the workflow but underweight in the bag

The strongest claim the metric supports is: *"on this particular bag, under offline scoring, the (Model B + H2) composite produced comparable aggregate quality to (Model A + H1) at lower cost."* Anything stronger — *Model B is good enough for our workflow* — requires per-cohort decomposition the aggregate does not provide.

---

## Takeaway

> **A migration eval should not ask whether Model B is globally good enough. It should ask where Model B is good enough — under the same kind of work, with the harness held constant, and the oracle held constant.** "Good enough on average" is not "safe to replace across the workflow." A task-cohort-aware eval reports per-bucket gaps; a global eval reports a number that looks safe and quietly externalizes the risk to the long-horizon, high-irreversibility tail.

The structural fix is the same one that surfaces in the [agent-regression example](./agent-regression.md): bucket sessions by task structure first, decompose the gap into within-bucket composite differences and between-bucket mix-shift effects, and report the per-bucket numbers. Migration becomes a decision about workflow coverage, not about an aggregate.
