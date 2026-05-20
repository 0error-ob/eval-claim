# Claim Reading Template

Use this template to analyze a public AI evaluation claim before drawing conclusions from it. Fill in each field in one to three sentences. If a field cannot be answered, that gap is the finding.

---

**Claim:** The exact statement being made. Quote or paraphrase in one sentence.

**Artifact:** The concrete evidence offered: a benchmark leaderboard entry, a regression alert, an A/B comparison, a user study result, a monitoring metric. What physically exists that the claim points to?

**Task structure:** What kind of work the artifact actually measured. Use vocabulary from [PRIMITIVES.md](../PRIMITIVES.md): actor, goal, environment, action space, oracle. Not the score — the task object.

**Oracle:** How success was determined — programmatic test suite, reference-answer match, LLM judge, human evaluator, implicit user satisfaction signal, or no explicit oracle. Note any mismatch between what the oracle can observe and what the claim asserts.

**Dominant dimensions:** Which 1–3 task dimensions from [DIMENSIONS.md](../DIMENSIONS.md) most shape the result. Common candidates: time horizon, observability gap, decomposition depth, verification regime, ambiguity load, irreversibility surface.

**Allowed inference:** What conclusion the artifact actually supports, stated as tightly as the evidence warrants. Usually narrower than the headline claim.

**Unsupported inference:** What conclusion a reader might reasonably draw that the artifact does not support. This is where the claim travels beyond its license.
