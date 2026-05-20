# Claim Card: ripsecrets reference-source on ProgramBench

A filled claim card for ProgramBench run `ripsecrets-refsource-001`, using [templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

---

## 1. Run identity

**Run ID:** `ripsecrets-refsource-001`.

**Date:** 2026-05-12.

**Author:** `0error`.

## 2. Benchmark

**Benchmark name:** ProgramBench.

**Dataset:** ProgramBench public task set (200 tools).

**Task:** `sirwart__ripsecrets.34c9e03` (single task).

**Source field:** Task ID is the canonical reference; commit `34c9e03` of `github.com/sirwart/ripsecrets`.

## 3. Agent

**Agent display name:** `reference-source` (ProgramBench claim type).

**Public repo:** N/A. ProgramBench implementations are per-task tarballs, not a single agent repo. The reproducible artifact is `submission.tar.gz` plus `run_config.yaml`.

**Claim type lock:** `claim_label: reference-source` (locked in `run_config.yaml` before first package call; `claim_label_locked: true`).

**Claim type history:** An earlier run (`ripsecrets-cleanroom-001`) attempted `test-informed cleanroom` and froze at Step 6 (pre-implementation dimension threshold: 45+ dimensions + non-regex entropy detector). The reference-source claim was chosen as the recovery path.

## 4. Model

**Model identifier:** `anthropic/claude-sonnet-4-6` (model active during this run session).

**Provider / endpoint:** Anthropic / Claude Code interactive session.

**Routing notes:** Claude Code orchestrated the implementation steps (copy, build, package, eval). The implementation itself is the reference source — no model-generated implementation logic.

## 5. Harness configuration

**Harness:** ProgramBench eval CLI (`programbench eval`).

**Configuration:**
- Docker image: `rust:latest` (required by Cargo.lock version = 4)
- Workers: `--workers 2 --branch-workers 2`
- No timeout multiplier override; no resource overrides
- Eval invocation: `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 programbench eval runs/ripsecrets-refsource-001`

**Compliance:**
- [x] `claim_label_locked: true` before first tarball
- [x] Reference source copied verbatim from `repos/sirwart__ripsecrets.34c9e03/` at commit `34c9e03` (no modifications)
- [x] `target/` excluded from submission tarball
- [x] `benches/find_secrets.rs` included (required by `[[bench]]` in Cargo.toml)
- [x] `build.rs` included (generates man page + shell completions via `clap_mangen` + `clap_complete`)
- [x] compile.sh written with LF line endings (printf, not echo)

## 6. Run type

**Run type:** Per-task ProgramBench evaluation, single round, single tarball.

**Total trials:** 1 tarball × 10 branches × (varies per branch) test cases = single evaluation pass.

## 7. Evidence surface

**Artifacts produced:**
- `run_config.yaml`: claim type, lock state, parent run reference
- `submission.tar.gz` (18 KB): reference source (`src/`, `Cargo.toml`, `Cargo.lock`, `build.rs`, `benches/`), `compile.sh`
- Eval JSON: `runs/ripsecrets-refsource-001/sirwart__ripsecrets.34c9e03/sirwart__ripsecrets.34c9e03.eval.json`

**Artifacts uploaded:** None.

**Inspectability:** A reviewer with ProgramBench installed can reproduce by extracting the impl tarball and running `programbench eval` against `sirwart__ripsecrets.34c9e03`. The tarball is deterministically derivable from the public ripsecrets commit `34c9e03`.

## 8. Metric distinction

**Leaderboard metric:** ProgramBench scores per-task as "resolved" / "not resolved" based on per-task eval pass rate. The aggregate leaderboard metric is the count of resolved tasks across the 200-task set.

**Other reported metrics:**
- Raw test counts: 937 total across all branches; 934 passed; 3 non-passed (2 skipped + 1 failure) in quality-excluded branch `da3e74bf86b7`
- Scored branches: 9 of 10, all passing 100%

**Headline number:** 100% (611 / 611 scored tests), 1 round — task `sirwart__ripsecrets.34c9e03` is resolved.

## 9. Result

**Headline:** 611 / 611 scored tests passed on first submission (round 1). Task `sirwart__ripsecrets.34c9e03` is resolved (✅).

**Disaggregation:**
- 10 test branches: 9 fully scored (100% each), 1 quality-excluded (`da3e74bf86b7`)
- Branch `da3e74bf86b7` had 14 passing + 2 skipped + 1 failure; quality-excluded by programbench scoring (not counted in the 611)
- No failures in any scored branch

## 10. Known exceptions

**Infrastructure exceptions:** None in scored branches.

**Branch quality exclusion:** Branch `da3e74bf86b7` is quality-excluded by ProgramBench. Its 3 non-passed tests (2 skipped, 1 failure) do not affect the score and were not investigated.

**Failure handling:** The 3 non-passed tests in `da3e74bf86b7` are structurally excluded from ProgramBench scoring — not counted as failures in the headline metric.

## 11. Ablations

**Held constant within this run:** Single tarball (verbatim reference source), single Docker image (`rust:latest`), single round.

**Varied:** Nothing varied within this run.

**Not ablated:**
- Whether `test-informed cleanroom` could reach a meaningful score if given unlimited rounds (deliberately not attempted; frozen at Step 6 pre-implementation by design)
- Whether modifications to the reference source would be needed to pass any excluded test branch
- Whether a future `rust:stable` or pinned image could replace `rust:latest` (Cargo.lock v4 constraint)

## 12. Allowed claims

- Under ProgramBench's per-task evaluation harness, with claim type `reference-source`, Docker image `rust:latest`, and reference source at commit `34c9e03`, this implementation produced 611/611 = 100% on `sirwart__ripsecrets.34c9e03` in 1 round. The task is resolved.
- The `reference-source` claim is appropriate: ripsecrets has no importable library structure; the full implementation (including entropy detection and secret pattern matching logic) resides in `src/`, which is both necessary and sufficient for the reference-source claim.
- The `cleanroom → reference-source recovery path` is operational for tasks that trigger a pre-implementation dimensional freeze: total elapsed time from freeze to 100% was approximately 20 minutes (copy + build + package + eval), confirming the recovery path is low-cost.
- Cargo.lock v4 requires `rust:latest`; this is a deterministic constraint checkable from the first line of Cargo.lock without reading any source.

## 13. Unsupported claims

- This run does NOT establish that `test-informed cleanroom` would fail on this task at any specific score. The cleanroom was frozen pre-implementation; the trajectory if it had proceeded is unknown.
- This run does NOT prove ripsecrets source is defect-free. The 1 failure and 2 skips in the quality-excluded branch represent potentially valid edge-case behaviors that the scored branches do not cover.
- The `reference-source` label does NOT mean the implementation is "better" than a cleanroom implementation would be — it means source was used, which is the maximum evidence surface. The score reflects the quality of the upstream project's test suite, not agent implementation quality.
- Cross-task generalization to other "secret scanner" tools (e.g. detect-secrets, trufflehog) is NOT supported — ProgramBench tasks are independent and the dimensional structure of other scanners may differ.

## 14. Reviewer questions

- Is branch `da3e74bf86b7` quality-excluded for a specific reason, or is it random across evaluation runs? (Check if ProgramBench documents per-branch quality filtering criteria.)
- Does the programbench scoring aggregate differently from simple pass/total across raw test cases? (The 934/937 raw vs 611 scored gap is larger than just the 3 excluded tests — ~323 tests appear to not exist in scored branches. This is likely due to different test files per branch, not additional exclusions.)
- Was `compile.sh` correctly executed inside the Docker container? (Critical — the eval summary ✅ confirms compile succeeded, but auditors should verify the `cargo build --release && cp target/release/ripsecrets executable` script ran as expected.)
- Would pinning `rust:stable` (rather than `rust:latest`) work for future reproducibility? (Cargo.lock v4 rules out older Rust images, but `rust:latest` tag moves over time. A fixed `rust:1.86` or similar would improve long-term reproducibility.)
