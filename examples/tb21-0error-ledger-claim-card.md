# Claim Card: 0error Ledger on Terminal-Bench 2.1

A filled claim card for the `tbench-2.1-k5-v01` run, using [templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

All numbers, names, and compliance assertions match the public submission artifacts. Cross-reference:
- HF PR: `harborframework/terminal-bench-2-leaderboard` discussion #184
- Repo: [github.com/0error-ob/terminal-bench-21-scaffold](https://github.com/0error-ob/terminal-bench-21-scaffold) at tag `tb21-submission-v1`
- Submission notes: `SUBMISSION_NOTES.md` in that repo at the same tag

---

## 1. Run identity

**Run ID:** `tbench-2.1-k5-v01`

**Date:** 2026-05

**Author:** `0error` (personal submission). Submission display name: `0error Ledger`.

## 2. Benchmark

**Benchmark name:** Terminal-Bench 2.1.

**Dataset:** `terminal-bench/terminal-bench-2-1` (89 tasks).

**Version:** TB 2.1. Distinct from TB 2.0; the version is determined by the `source` field inside `result.json`, not by the leaderboard submission path (which is shared between TB 2.0 and TB 2.1).

**Source field:** `source` field in each `result.json`.

## 3. Agent

**Agent display name:** `0error Ledger`.

**Public repo:** `github.com/0error-ob/terminal-bench-21-scaffold`.

**Tag:** `tb21-submission-v1`.

**File SHA256(s):**
- `agent/scaffold_agent.py`: `e51752241ea0a0ab9bdb13390c68d25a573ca416457fe30ee1168eb0895f1339`
- `agent/__init__.py`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)

## 4. Model

**Model identifier:** `anthropic/claude-opus-4-7` (Claude Opus 4.7).

**Provider / endpoint:** OpenRouter, `https://openrouter.ai/api/v1`.

**Routing notes:** In `result.json`, the `agent.model_name` field reads `openai/anthropic/claude-opus-4-7`. The `openai/` prefix is a LiteLLM convention indicating an OpenAI-compatible endpoint — it does not indicate the model vendor. The `metadata.yaml` `model_name` and `result.json` `agent_info.model_info.name` fields read `anthropic/claude-opus-4-7`. All three refer to the same model.

## 5. Harness configuration

**Harness:** Harbor 0.6.4.

**Configuration:**
- Concurrency: `-n 4`
- Trials per task: `k = 5` (total trials = 89 × 5 = 445)
- `timeout_multiplier = 1.0`
- No `override_timeout_sec` / `max_timeout_sec`
- No `override_cpus` / `override_memory_mb` / `override_storage_mb`
- VM: Nebius L40S, Ubuntu 24.04

**Compliance:**
- [x] `timeout_multiplier = 1.0`
- [x] No timeout overrides
- [x] No resource overrides
- [x] Agent does not access tbench.ai or the Terminal-Bench GitHub repo
- [x] No per-task pre-recorded trajectories
- [x] No task-name detection
- [x] 5 trials per task, 445 `result.json` total

## 6. Run type

**Run type:** Public leaderboard submission, full k=5 run.

**Total trials:** 445.

## 7. Evidence surface

**Artifacts produced:** Per-trial `result.json`, per-trial verifier outputs, exception logs, trial directories.

**Artifacts uploaded:** All 445 `result.json` files and `metadata.yaml`, under `submissions/terminal-bench/2.0/0error-Ledger__Claude-Opus-4.7/tbench-2.1-k5-v01/` in the HF leaderboard dataset.

**Inspectability:** A reviewer can clone the public agent repo at the tag, verify the SHA256 of `agent/scaffold_agent.py`, and re-run with the documented command.

## 8. Metric distinction

**Leaderboard metric:** Task-level pass@5 — a task passes if at least one of its 5 trials succeeds.

**Other reported metrics:** Trial-level mean reward — 177 / 445 = 39.8%. This metric answers a different question: what fraction of individual trials passed. Exception trials count as failures in this number.

**Headline number:** **66 / 89 = 74.2% pass@5** (the leaderboard-aligned metric).

## 9. Result

**Headline:** 66 / 89 = 74.2% pass@5.

**Disaggregation:**
- 23 tasks failed in pass@5 (none of the 5 trials passed).
- 8 tasks had all 5 trials end in exceptions: `caffe-cifar-10`, `compile-compcert`, `extract-moves-from-video`, `fix-ocaml-gc`, `llm-inference-batching-scheduler`, `mteb-leaderboard`, `qemu-alpine-ssh`, `train-fasttext`. For each: 2/5 Docker Hub rate-limit; 3/5 command timeout or `AgentTimeoutError`.
- Every task had at least 2 trials that successfully pulled the Docker image and entered agent execution.

## 10. Known exceptions

**Infrastructure exceptions:** 215 / 445 trials.

| Exception type | Count |
|----------------|-------|
| Docker Hub anonymous pull rate-limit | 165 |
| Command timeout (300s) | 31 |
| Command timeout (60s) | 4 |
| `AgentTimeoutError` (9 × 900s, 1 × 1800s, 1 × 3600s) | 11 |
| LLM provider `InternalServerError` | 3 |
| LLM provider `BadRequestError` | 1 |
| **Total** | **215** |

**Failure handling:** All 215 exception trials are counted as failures in the 66/89 figure. This is the conservative public posture.

## 11. Ablations

**Held constant:** Within this submission, all variables are held constant — single model (`anthropic/claude-opus-4-7`), single harness (`harbor 0.6.4`), single scaffold version (tag `tb21-submission-v1`), single harness configuration.

**Varied:** Nothing was varied within this submission. The headline number reflects one configuration.

**Not ablated:** Model variation, scaffold variation, harness variation. No baseline run within this submission isolates the scaffold's contribution from the model's.

## 12. Allowed claims

- Under Harbor 0.6.4 with Claude Opus 4.7 via OpenRouter, this submission produced 66 / 89 = 74.2% pass@5 on Terminal-Bench 2.1.
- Under the same model (Claude Opus 4.7), this submission's pass@5 is +4.5pp above the official Claude Code submission (74.2% vs 69.7%). This is a configuration comparison: the same model produced different leaderboard scores under different scaffolds. It is not a capability claim about the model.
- A scaffold that enforces probe → execute → verify → stop discipline can improve Terminal-Bench 2.1 pass@5 by reducing procedural agent failures, under the conditions established by this run.

## 13. Unsupported claims

- Claude Opus 4.7 is stronger than other models. (Requires holding the agent constant across models; this submission ran only one model.)
- This scaffold is model-agnostic. (Requires evidence across multiple models; not established here.)
- This scaffold generalizes to other agentic benchmarks. (Requires evidence on other benchmarks; not established here.)
- The 4.5pp delta is attributable solely to the scaffold's behavioral discipline. (No baseline run within this submission isolates scaffold contribution from other harness-side differences between this submission and the Claude Code submission.)

## 14. Reviewer questions

- Does the harness configuration match Terminal-Bench 2.1's stated rules? (Compliance checklist above — all items satisfied.)
- Are exception trials counted in the headline? (Yes — all 215 are counted as failures in 66/89.)
- How does the trial-level mean reward (39.8%) interact with the leaderboard score? (See section 8 — different metric, different question. pass@5 absorbs one passing trial per task; mean reward does not.)
- What would the most direct next-run lever be? (Authenticated Docker Hub, to reduce the 165 anonymous-pull rate-limit exceptions.)
- Has the agent at this SHA256 been run on any other benchmark? (Not as part of this submission.)
