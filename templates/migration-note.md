# Model Migration Note

Use this template when recommending a switch from one model to another for a specific workflow. The structure forces the migration into cohort terms — not aggregate terms — so workflow-specific failure modes do not get hidden behind an averaged comparison.

Fill in each field in one to three sentences. If a field cannot be answered, that gap is the finding.

---

**Models compared:** Current model A, candidate model B, and the variables held fixed across the comparison (version, temperature, system prompt, harness). Migration is meaningless without these anchors.

**Target workflow:** The kind of work the candidate must handle in production, described concretely. Not "coding" — "long-running multi-file refactor in a 50k-LOC TypeScript repo with test-suite oracle." Specificity here is what makes the rest of the analysis tractable.

**Comparison artifact:** The eval evidence supporting the switch. A public benchmark, a private A/B run, a vendor-supplied comparison, an internal pilot, or a vibe check. State what concretely exists.

**Task structure:** What the artifact actually measured. Use vocabulary from [PRIMITIVES.md](../PRIMITIVES.md): actor, goal, environment, action space, oracle. Note any gap between the artifact's tasks and the target workflow's tasks.

**Migration-safe cohorts:** Task cohorts within the target workflow where the candidate matches or exceeds the current model, with concrete supporting evidence. Stratified per cohort, not averaged.

**Migration-risky cohorts:** Task cohorts where the candidate underperforms or where evidence is missing. The migration's blast radius is determined here, not in the safe column.

**Rollback condition:** The observable production signal that would trigger reverting. Stated as a measurable threshold, not a feeling.

**Recommendation:** Migrate / migrate with carve-outs / hold / re-eval with stratified data. The decision and the cohort scope it applies to.
