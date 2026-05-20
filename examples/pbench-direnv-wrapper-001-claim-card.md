# Claim Card: direnv reference-library wrapper on ProgramBench

A filled claim card for ProgramBench run `direnv-wrapper-001`, using [templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

This is the ProgramBench-side worked example of a claim card. The Terminal-Bench-side example is at [tb21-0error-ledger-claim-card.md](./tb21-0error-ledger-claim-card.md).

---

## 1. Run identity

**Run ID:** `direnv-wrapper-001`.

**Date:** 2026-05.

**Author:** `0error`.

## 2. Benchmark

**Benchmark name:** ProgramBench.

**Dataset:** ProgramBench public task set (200 tools).

**Task:** `direnv__direnv.02040c7` (single task in the set).

**Source field:** Task ID is the canonical reference.

## 3. Agent

**Agent display name:** `reference-library wrapper` (ProgramBench claim type).

**Public repo:** N/A. ProgramBench implementations are per-task tarballs, not a single agent repo. The reproducible artifact is the tarball plus its `run_config.yaml`.

**Claim type lock:** `claim_label: reference-library wrapper` (locked in `run_config.yaml` before first package call).

## 4. Model

**Model identifier:** `anthropic/claude-opus-4-7` (primary working model; see `run_config.yaml` for the actual model recorded for this run).

**Provider / endpoint:** OpenRouter.

**Routing notes:** ProgramBench is prompt-driven — the model is the orchestrator that produces the implementation. Different runs may use different models; this field records what was used for this specific run.

## 5. Harness configuration

**Harness:** ProgramBench eval CLI (`programbench eval`).

**Configuration:**
- Docker image: `golang:1.21` (matching `go.mod`)
- No timeout multiplier override
- No resource overrides
- Eval invocation: `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 programbench eval runs/<run-id>`

**Compliance:**
- [x] `claim_label_locked: true` before first tarball
- [x] No `.go` source files read from `repos/direnv/` during cleanroom probing (wrapper claim permits reading library API; `cmd/main.go` was permissible to read for API understanding)
- [x] All 11 test branches built from the same source tarball (verified identical via md5)

## 6. Run type

**Run type:** Per-task ProgramBench evaluation, single round, single tarball.

**Total trials:** 1 tarball × 11 branches × 849 test cases = single evaluation pass.

## 7. Evidence surface

**Artifacts produced:**
- `run_config.yaml`: claim type and lock state
- Tarball: `submission.tar.gz` containing the wrapper implementation, copied library files, `compile.sh`, `go.mod`, `go.sum`, embedded `stdlib.sh` and `version.txt`
- Eval output: `runs/<run-id>/<task-id>/*.eval.json`

**Artifacts uploaded:** None.

**Inspectability:** A reviewer with ProgramBench installed can reproduce by extracting the impl tarball and running `programbench eval` against the same task ID.

## 8. Metric distinction

**Leaderboard metric:** ProgramBench scores per-task as "resolved" / "not resolved" based on per-task eval pass rate. The aggregate leaderboard metric is the count of resolved tasks across the 200-task set.

**Other reported metrics:** Per-branch raw pass count (849/849 in this run); per-eval-round score history.

**Headline number:** 100% (849 / 849 tests), 1 round — task is resolved.

## 9. Result

**Headline:** 849 / 849 tests passed on first submission. Task `direnv__direnv.02040c7` is resolved.

**Disaggregation:**
- 11 test branches, all with identical source code (same md5 for all `.go` files)
- Tests cover: subcommand dispatch, aliases (`permit`/`grant`/`deny`/`disallow`/`revoke`), help output, hook output for multiple shells, `export` shells, `status --json`, `allow`/`deny`/`exec`, dotenv parsing, `dump`/`show_dump`, watch commands, config gaps, XDG isolation.

## 10. Known exceptions

**Infrastructure exceptions:** None in this run.

**Note:** GOCOVERDIR warnings appeared from tests but are benign (`conftest.py` strips them — confirmed not test failures).

**Failure handling:** N/A — no exceptions.

## 11. Ablations

**Held constant within this run:** Single tarball, single Go version, single Docker image, single wrapper structure.

**Varied:** Nothing varied within this run.

**Not ablated:** Whether a `binary/docs cleanroom` or `test-informed cleanroom` claim could have reached the same score (not tested). The wrapper claim was chosen on first preflight (importable `internal/cmd` package + thin main.go), and the first submission scored 100% — no need to ablate the claim type.

## 12. Allowed claims

- Under ProgramBench's per-task evaluation harness, with claim type `reference-library wrapper` and Docker image `golang:1.21`, this implementation produced 849/849 = 100% on the `direnv__direnv.02040c7` task in 1 round.
- The `reference-library wrapper` approach is feasible for this task: the upstream repo has an importable non-main `internal/cmd` package and a thin `main.go`, which is the structural prerequisite for the wrapper claim.
- All 11 test branches share identical source, so a single tarball suffices.

## 13. Unsupported claims

- This implementation will pass commits or branches not covered by ProgramBench's 11 evaluation branches for this task. (The run only establishes the 11 branches as a fixed sample.)
- The wrapper approach is uniformly better than cleanroom or reference-source approaches for Go CLI tools. (Other tasks in ProgramBench have surfaced cases where wrapper hits a structural ceiling — see, e.g., `kisielk/errcheck` at 97.9%. Wrapper-vs-other ranking is task-specific.)
- The score reflects the model's coding ability in isolation. (The harness produces the score; the model's role is the implementation generation, but the wrapper structure itself is a substantial part of the work product.)

## 14. Reviewer questions

- Are all 11 evaluation branches in ProgramBench really identical for this task? (Run card asserts yes via md5; reviewer can verify.)
- Does the impl exercise the bash-hook integration tests? (`bashPath` was empty — those tests were not exercised. If a future ProgramBench branch adds bash-hook tests, this impl would need to be re-evaluated.)
- What is the test harness's behavior on `//go:embed` mismatches? (Critical for embedded `stdlib.sh` + `version.txt` correctness.)
- Could this task have been solved as `binary/docs cleanroom` without reading the library? (Not tested. Wrapper was chosen because the structure was clearly there; cleanroom feasibility is unknown.)
