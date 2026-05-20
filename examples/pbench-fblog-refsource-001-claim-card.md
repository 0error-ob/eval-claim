# Claim Card: fblog reference-source on ProgramBench

A filled claim card for ProgramBench run `fblog-refsource-001`, using [templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

---

## 1. Run identity

**Run ID:** `fblog-refsource-001`.

**Date:** 2026-05-12.

**Author:** `0error`.

## 2. Benchmark

**Benchmark name:** ProgramBench.

**Dataset:** ProgramBench public task set.

**Task:** `brocode__fblog.3b54330` (single task).

**Source field:** Task ID is the canonical reference.

## 3. Agent

**Agent display name:** `reference-source` (ProgramBench claim type).

**Public repo:** N/A. ProgramBench implementations are per-task tarballs.

**What was submitted:** Full upstream fblog 4.17.0 source (`src/*.rs`, `Cargo.toml`, `Cargo.lock`, `default_config.toml`) plus a `compile.sh` that runs `cargo build --release && cp target/release/fblog executable`. No source modifications.

**Claim type lock:** `claim_label: reference-source` (locked in `run_config.yaml` before first package call).

## 4. Model

**Model identifier:** `anthropic/claude-opus-4-7` (coordinator orchestrating the scout and packaging).

**Provider / endpoint:** Anthropic direct (Claude Code).

**Routing notes:** The model did not generate implementation code; it produced the routing decision and packaging commands. The binary is entirely the upstream fblog source compiled by `rust:latest`.

## 5. Harness configuration

**Harness:** ProgramBench eval CLI (`programbench eval`).

**Configuration:**
- Docker image: `rust:latest` (required by Cargo.lock version 4)
- Eval invocation: `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 programbench eval runs/fblog-refsource-001`
- No timeout multiplier override; no resource overrides
- Tarball size: 20 KB (no target/ dir)

**Compliance:**
- [x] `claim_label_locked: true` before first tarball
- [x] No .rs source code read or modified; tarball is bit-exact copy of upstream (confirmed by `diff -r repos/... impl-cleanroom/...`)
- [x] Phase B strict stop: 1 round only (reference-source ceiling policy)
- [x] `--exclude ./target` in tarball command; sanity-checked size (< 5 MB threshold)

## 6. Run type

**Run type:** Per-task ProgramBench evaluation, single round, single tarball.

**Total trials:** 1 tarball × 13 branches × 1127 raw test records (978 scored).

## 7. Evidence surface

**Artifacts produced:**
- `run_config.yaml`: claim type and lock state at `cleanroom/fblog-refsource/run_config.yaml`
- Tarball: `runs/fblog-refsource-001/brocode__fblog.3b54330/submission.tar.gz` (20 KB)
- Eval JSON: `runs/fblog-refsource-001/brocode__fblog.3b54330/brocode__fblog.3b54330.eval.json`
- This claim card

**Artifacts uploaded:** None.

**Inspectability:** A reviewer with ProgramBench installed can reproduce by extracting the impl tarball (which contains the full unmodified fblog 4.17.0 source) and running `programbench eval` against task ID `brocode__fblog.3b54330`.

## 8. Metric distinction

**Leaderboard metric:** ProgramBench task-level score (% of scored test cases passing).

**Other reported metrics:** Raw per-branch test counts (passed/skipped/failed in eval JSON).

**Headline number:** 978/978 = 100% scored tests passing (official programbench eval output, single round).

## 9. Result

**Headline:** 978 / 978 scored tests = 100% ✅, 1 round, 0 repair iterations.

**Disaggregation:**
- 13 branches evaluated; all pass
- Raw JSON: 1121 passed / 6 skipped / 0 failed
- 6 skipped: all in branch `4e219826c927`; `pytest_dependency`-skipped due to pytest-xdist parallel scheduling, NOT due to impl failure (parent test `test_sample_json_log_default_snapshot` status: passed)
- 0 failures across all branches

## 10. Known exceptions

**Infrastructure exceptions:** 6 tests skipped via `pytest_dependency` in branch `4e219826c927` (xdist cross-worker dependency tracking cannot propagate pass state, causing dependent tests to be marked skipped). This is an evaluator scheduling artifact, not an impl bug. Official scoring counts these as skipped (not failed), consistent with ✅ result.

**Failure handling:** ProgramBench counts skipped as not-failed; the ✅ threshold requires zero failures. This run has zero failures.

## 11. Ablations

**Held constant:** fblog 4.17.0 upstream source, rust:latest Docker image, standard ProgramBench eval invocation.

**Varied:** Nothing varied — single round, single tarball, no repair.

**Not ablated:**
- Whether a cleanroom approach could achieve any score on this task (it was not attempted; scout analysis predicted failure based on multi-DSL structure and ANSI constraints)
- Whether a different commit of fblog would achieve the same score
- Whether alternative DSL implementations (independent Lua + Handlebars crates) could reproduce the exact ANSI byte sequences

## 12. Allowed claims

- Under the ProgramBench evaluation harness, submitting unmodified fblog 4.17.0 source (compiled with `rust:latest`) achieves 978/978 (100%) scored tests in the `brocode__fblog.3b54330` task in a single round.
- The reference-source ceiling for `brocode__fblog.3b54330` on this task+branch set is 978/978; no further repair budget was available or needed.
- The scout routing decision (reference-source, not cleanroom) was validated: the multi-DSL structure (Lua 5.4 + Handlebars 6 + Placeholder DSL + TOML config) and ANSI non-suppression are properties of the upstream binary that survive verbatim in the reference-source submission.

## 13. Unsupported claims

- This score does not prove that a cleanroom implementation is impossible or would score below some threshold — it was not attempted.
- This score does not prove that any model can solve `brocode__fblog.3b54330` as a cleanroom task. Reference-source and cleanroom are different claim types; they are not comparable.
- This score does not generalize to other fblog commits or to other log-formatting tools with similar structure.
- The model (claude-opus-4-7) did not write implementation code; its contribution is the routing decision and packaging steps, not code quality.

## 14. Reviewer questions

1. The 6 skipped tests in branch `4e219826c927` — is the root cause pytest-xdist scheduling or an actual impl deficiency? (Answer: root test `test_sample_json_log_default_snapshot` status is `passed` in eval JSON; xdist artifact confirmed.)
2. Was the tarball verified to contain only upstream source without modification? (How to check: `tar -tzf submission.tar.gz` then `diff -r` against `repos/brocode__fblog.3b54330/src/`.)
3. Does the 100% score persist across multiple eval runs, or is it sensitive to xdist scheduling? (The 6 skipped are the only non-passed; on a re-run they might pass if scheduled in the same worker, giving 1127/1127.)
4. What is the routing cost of the scout run? (< 1 hour total: oracle build ~30s, ANSI probes ~5 min, test fetch ~2 min, analysis ~20 min. Reference-source impl: tarball + eval ~3 min.)
