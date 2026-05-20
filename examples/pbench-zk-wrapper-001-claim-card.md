# Claim Card: zk reference-library wrapper on ProgramBench

A filled claim card for ProgramBench run `zk-wrapper-001`, using [templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

---

## 1. Run identity

**Run ID:** `zk-wrapper-001`.

**Date:** 2026-05-12.

**Author:** `0error`.

## 2. Benchmark

**Benchmark name:** ProgramBench.

**Dataset:** ProgramBench public task set.

**Task:** `zk-org__zk.10d93d5` (commit `10d93d5`, 8 commits past tag `v0.15.2`).

**Source field:** Task ID is the canonical reference. HuggingFace snapshot of test blobs: `de0ddfb637590c7ecb54fa0b5301f6dc7dfbcee5`.

## 3. Agent

**Agent display name:** `reference-library wrapper` (ProgramBench claim type).

**Public repo:** N/A. ProgramBench implementations are per-task tarballs, not a single agent repo. The reproducible artifact is the tarball plus its `run_config.yaml`.

**Claim type lock:** `claim_label: reference-library wrapper` (locked in `run_config.yaml` before first package call).

## 4. Model

**Model identifier:** `anthropic/claude-opus-4-7` (the model that produced the wrapper implementation).

**Provider / endpoint:** Anthropic direct.

**Routing notes:** ProgramBench is prompt-driven — the model is the orchestrator that produces the implementation. Different runs may use different models; this field records what was used for this specific run.

## 5. Harness configuration

**Harness:** ProgramBench eval CLI (`programbench eval`, installed from PyPI under that name).

**Configuration:**
- Docker image for impl build (during eval): `programbench/zk-org_1776_zk.10d93d5` (task-specific image; supports CGO out of the box, as confirmed by the prior `trdsql-wrapper-001` run that also depends on `mattn/go-sqlite3`).
- Docker image for oracle probing: `golang:1.24` (matching `go.mod: go 1.24.0`), with `gcc` + `libc6-dev` installed for CGO.
- Eval invocation: `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 programbench eval runs/zk-wrapper-001`.

**Compliance:**
- [x] `claim_label_locked: true` set in `run_config.yaml` before first tarball was produced.
- [x] Reading reference `.go` files from `repos/zk-org__zk.10d93d5/` is permitted under the `reference-library wrapper` claim. `main.go` and all of `internal/` were read and copied.
- [x] Probes against the oracle binary only (`--version`, `--help`); no decompilation.
- [x] No internet probing of the upstream project during implementation.
- [x] All 10 test branches built from the same submitted source tarball (single submission).

## 6. Run type

**Run type:** Per-task ProgramBench evaluation, single round, single tarball.

**Total trials:** 1 tarball × 10 branches × ~1108 scored test cases (1471 raw before cross-branch aggregation).

## 7. Evidence surface

**Artifacts produced:**
- `run_config.yaml`: claim type, lock state, and preflight results (TUI / state / cloud / entry-size checks).
- Tarball: `submission.tar.gz` containing the wrapper implementation, copied library files (`internal/`), reference-copied `main.go` (with one-line `Version` literal edit), `compile.sh`, `go.mod`, `go.sum`.
- Eval output: `runs/zk-wrapper-001/zk-org__zk.10d93d5/zk-org__zk.10d93d5.eval.json`.

**Artifacts uploaded:** None.

**Inspectability:** A reviewer with ProgramBench installed and the HuggingFace test snapshot pulled can reproduce by extracting the impl tarball and running `programbench eval` against the same task ID.

## 8. Metric distinction

**Leaderboard metric:** ProgramBench scores per-task as resolved (✅, score 100) / not resolved, based on a cross-branch aggregation that excludes tests whose pass/fail flips across branches (the "branch contradiction" exclusion).

**Other reported metrics:** Per-branch raw pass count (1314 / 1431 = 91.8% raw across 10 branches with 40 skipped).

**Headline number:** **100 / ✅ solved**, 1108 scored tests.

## 9. Result

**Headline:** 1108 / 1108 official scored tests passed on first submission. Task `zk-org__zk.10d93d5` is resolved.

**Disaggregation (raw, 10 test branches):**
- 7 branches: clean (62, 23, 44, 1, 32, 101, 3 tests, all passed).
- 2 branches with 1 isolated failure each:
  - `3bf39808dee9`: 5 / 6 — expects an FTS5-disabled init-error path that contradicts the canonical `Makefile`'s `-tags fts5`.
  - `b7ec3be0bde5`: 13 / 14 — expects a different version-string format than the canonical `Makefile`'s `zk <git-describe>` (leading-`v`-stripped).
- 1 large speculative branch with 115 failures + 40 skipped:
  - `ad0a74fcd352`: 1030 / 1185 — 45 distinct test areas; pattern matches the gomplate / dep-tree / curlie / richgo cross-branch-contradiction family.

All 117 raw failures are filtered out by official cross-branch scoring, yielding 100.

## 10. Known exceptions

**Infrastructure exceptions:** None in this run. `test_branch_errors: {}` and `warnings: []`.

**Failure handling:** All raw failures are counted as failures in the raw breakdown. The 117 → 0 gap is explained by ProgramBench's cross-branch aggregation, not by exclusion policy.

## 11. Ablations

**Held constant within this run:** Single tarball, single Go version (1.24.0), single Docker image, single wrapper structure.

**Varied:** Nothing varied within this run.

**Not ablated:**
- Whether a `test-informed cleanroom` claim could reach the same score (not tested). Wrapper was chosen because `main.go` is pure thin orchestration and `internal/cli/cmd/` + `internal/core/` provide the full library surface; cleanroom would require reconstructing `kong` command registration, alias dispatch, and SQLite notebook discovery from probes (10–20× the effort).
- Whether the FTS5 build tag is what each individual branch expects. The canonical `Makefile` uses `-tags fts5`; the 1 failing FTS5-related test in `3bf39808dee9` is left as a known contradiction.

## 12. Allowed claims

- Under ProgramBench's per-task evaluation harness, with claim type `reference-library wrapper` and the task-specific Docker image, this implementation produced **100 / ✅ solved** (1108 / 1108 scored tests) on the `zk-org__zk.10d93d5` task in 1 round.
- The `reference-library wrapper` approach is feasible for this task. The structural prerequisites are present: the upstream repo's `main.go` is pure thin orchestration (`kong` registration + alias dispatch + path parsing), and all business logic lives in `internal/cli/cmd/` + `internal/core/` as importable packages.
- A note-taking CLI with mutable filesystem and SQLite state can still be wrappered when the ProgramBench test harness pre-skips its interactive and state-mutating tests. The decisive evidence is the harness `SKIP_TESH` set (which excludes `cmd-edit`, `cmd-new`, `cmd-new-template`, `flag-version`, `cmd-index`, `cmd-index-legacy-ignore`), not the source structure alone.
- Across 10 test branches, the same source tarball produces the headline score; the 117 raw failures are concentrated in branches that the framework drops as cross-branch contradictions.

## 13. Unsupported claims

- This implementation will pass commits or branches not covered by ProgramBench's 10 evaluation branches for this task. (The run establishes the 10 branches as a fixed sample.)
- The wrapper approach is uniformly better than cleanroom or reference-source approaches for note-taking CLIs. (Not ablated. Wrapper was chosen because the structural prerequisites were clearly present; cleanroom feasibility is unknown for this task.)
- The score reflects only the model's coding ability. (The harness produces the score; the model's role is to identify the wrapper opportunity and produce the implementation, but the upstream `main.go`'s thin-wrapper shape is a substantial part of why this works.)
- This wrapper would reach 100% with any other ProgramBench-style note-taking CLI. (Cross-task generalization claim; requires evidence on multiple note-taking CLIs.)
- The FTS5-disabled path and version-string format expected by branches `3bf39808dee9` and `b7ec3be0bde5` are bugs in those branches. (Not investigated. They are recorded as contradictions, not adjudicated.)

## 14. Reviewer questions

- Are all 117 raw failures genuinely cross-branch contradictions, or do some reflect real spec gaps that happen to be excluded by aggregation? (Run card lists the 45 distinct failure areas in `ad0a74fcd352`; reviewer can sample-audit against the canonical 9 branches.)
- Was the 329-line `main.go` actually pure orchestration, or did it contain business logic that the wrapper claim should not have copied? (Run card asserts pure orchestration with a function-by-function inventory; reviewer can verify by reading `main.go`.)
- Does the FTS5 build tag in `compile.sh` match the canonical upstream build? (Run card cites the upstream `Makefile`'s `-tags "fts5"`; reviewer can verify.)
- Has the harness `SKIP_TESH` set been audited for completeness — are there interactive paths not skipped? (Run card lists the 6 skip entries; reviewer should check whether anything else in `test_zk.py` exercises `internal/adapter/fzf/`.)
- Could a `test-informed cleanroom` run reach the same score on this task? (Not tested; the wrapper structural prerequisites were strong enough that this was not ablated.)
