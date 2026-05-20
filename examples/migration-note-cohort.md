# Example: Cohort-Stratified Migration Note

A worked application of [migration-note.md](../templates/migration-note.md). Models, cohorts, and numbers are generic — the point is to demonstrate cohort-stratified reasoning, not to evaluate any specific model.

The teaching point sits in the **Recommendation** field: the aggregate pass rate would have authorized a full migration; the cohort breakdown reveals that doing so would ship a 16pp regression on the cohort that drives the most downstream damage.

---

**Models compared:** Current model A → candidate model B (cheaper, faster). Same harness, system prompt, and tool surface. Temperature held at 0.

**Target workflow:** Internal coding-agent loop, three cohorts:
- C1 — test-backed bug fixes (single-file, passing test suite as oracle)
- C2 — multi-file refactors (medium repo, partial test coverage)
- C3 — weak-oracle product judgment (release notes, customer summaries; no automated oracle)

**Comparison artifact:** Internal A/B over 30 days, n=240 sessions, sampled across the three cohorts roughly proportionally to production traffic.

**Task structure:** All three cohorts share actor (the agent), environment (repo + tool surface), and action space (file edit + shell). They differ in oracle: C1 has a strong programmatic oracle; C2 has a partial one; C3 has an implicit oracle (the downstream human reviewer).

**Migration-safe cohorts:** C1 — Model B within ±1pp of Model A (B: 78%, A: 79%). Strong oracle pins behavior; no observable degradation.

**Migration-risky cohorts:** C2 — Model B drops to 51% vs A's 67%. Failures cluster on cross-file consistency: B writes locally correct edits that break call sites it did not read. C3 — no automated oracle, but human reviewers flag B's outputs as "off" 22% of the time vs 9% for A; the failure mode is invisible at session end.

**Rollback condition:** If rolling 7-day pass rate on C1 drops below 75%, or if C3 reviewer flag rate exceeds 15%, revert affected cohort traffic to Model A within 24 hours.

**Recommendation:** Migrate with carve-outs. Route C1 traffic to Model B now. Hold C2 and C3 on Model A; re-eval B on C2 once a stronger cohort-level oracle (e.g., regression test on call-site consistency) is available. The aggregate pass rate (B: 64%, A: 71%) would have authorized full migration; the cohort breakdown reveals that doing so would ship a 16pp regression on C2.
