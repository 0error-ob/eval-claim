# Worked example: Benchmark leaderboard claim

**Scenario.** A model provider publishes release notes claiming that Model A achieves 65.4% on SWE-bench-Verified, up from 57.1% for Model A-prev. An engineering team reads this and concludes: "Model A is substantially better at software engineering tasks." A second team reads a competitor's announcement — 68.2% on the same benchmark — and concludes: "Competitor B is the best coding model available."

Both conclusions are common. Both may be wrong for the same structural reason.

This is a recurring class of claim. The pattern applies to any leaderboard-format score.

We apply [Template 1 — Benchmark claim](../QUICKSTART.md#template-1--benchmark-claim) from QUICKSTART.

---

## 1. What task is being constructed?

SWE-bench-Verified is a human-validated subset of 500 SWE-bench instances drawn from popular Python open-source repositories. The agent receives the issue text and the repository at a fixed commit; it must produce a patch that passes the benchmark's designated validation tests while preserving expected behavior checked by the evaluation harness.

The task object is: *given a failing test in a real codebase, locate the defect, understand it, produce a targeted patch, and verify it — within the constraints of the scaffold provided.*

That last phrase matters. The "agent" scored on the leaderboard is not the raw model but a *(model + harness + prompt template + tool interface)* composite. Different teams submit different composites.

## 2. What is the oracle?

A fixed pre-authored test suite, derived from the original issue's resolution. The oracle question is: *does the designated test pass, and do the originally-passing tests still pass?*

This is a strong oracle by agent-eval standards — programmatic, consistent, no judge model involved. That strength is also its sharpness: the oracle answers exactly one question. It does not assess patch quality, surface area, maintainability, or whether invariants outside the test suite still hold.

## 3. Which dimensions dominate the result?

From [DIMENSIONS.md](../DIMENSIONS.md):

- **Oracle availability** — rich. The test suite is unambiguous; this is one of SWE-bench's structural strengths.
- **Context locality** — repo-scale. The defect can be anywhere in a large codebase the agent has not seen before.
- **Decomposition depth** — deep. The nominal workflow is: locate → understand → patch → test → re-verify.
- **Verification regime** — collapses onto the oracle. The only legible feedback signal the agent receives is the test runner.

These dimensions are relatively stable across the 500 instances. That stability is what makes the benchmark a useful calibration surface: the task shape does not drift much within the set.

## 4. What does the metric see?

Binary pass/fail per instance, aggregated into a single pass rate:

> Pass rate = (instances where final patch makes target tests pass) / 500

One scalar. That is the number on the leaderboard.

## 5. What does the metric hide?

**Harness contribution.** The pass rate measures the *(model + harness + prompt)* composite, not the model in isolation. Two teams running the same base model through different scaffolds will report different scores. This is not a measurement error to be corrected; it is a structural feature of the measurement object.

**Patch surface area.** A 300-file change that happens to turn the target tests green counts identically to a surgical 3-line fix. The metric cannot distinguish a model that understands the defect from one that overwrites adjacent code until tests pass.

**Out-of-suite regressions.** The oracle only checks the designated test suite. A patch can break real behavior that no test in that suite covers. This failure mode is structurally invisible to the benchmark — the score offers no evidence on it either way.

**Score portability across time.** A result reported in January on a frozen model version is not the same measurement as one reported in March on an updated endpoint through a different scaffold. Scores are not durable properties of a model; they are dated observations of a configuration.

## 6. What inference is unsafe?

> *"Model A is 8.3 points better at software engineering than Model A-prev."*

This inference is unsafe when:

- The two runs used different harnesses or prompt templates — which is common in version-to-version comparisons, since teams often improve scaffolding alongside model updates
- The comparison crosses two different labs' submissions, which almost never share a matching harness configuration
- The score gap is presented as a capability claim without specifying what held constant between the two measurements

The broader cross-lab version — *"Competitor B is the best coding model because 68.2 > 65.4"* — requires that *(harness, prompt, oracle, sample distribution)* match across both points. They do not, by default.

---

## Takeaway

> **A leaderboard score is a property of the (model, harness, prompt, oracle, sample distribution) joint object, not the model alone.** Before reading a capability gap into a score difference, check whether the four non-model variables in the tuple are held constant across both comparison points. When they are not, the gap is evidence about a configuration comparison, not a capability comparison.

The benchmark is not misleading. The inference is.
