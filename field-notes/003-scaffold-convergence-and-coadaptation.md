# 003 — Scaffold convergence and benchmark co-adaptation

**Type:** Agent benchmark leaderboard claim  
**Question:** What does a score compare once scaffolds converge?  
**Status:** Claim reading, not benchmark criticism

Agent scaffolds are converging. Across SWE-bench-style coding tasks, Terminal-Bench-style terminal tasks, GAIA-style tool research, and OSWorld-style desktop control, most systems now share the same broad shape:

> observe -> plan/think -> act -> observe -> verify/retry

More industrial systems split this into planner, executor, verifier, memory, and retry policy. More expensive systems may add tree search or branch exploration, but in leaderboard-scale runs full search is often replaced by cheaper heuristics plus a strong verifier.

The result is not that scaffolding no longer matters. It is that scaffolding differences move from obvious topology to smaller but still consequential choices: retry budget, context compression, tool restrictions, verifier strength, checkpointing, rollback, and failure classification.

## The convergence pattern

Most agent submissions now belong to one scaffold family:

- **ReAct loop** — observe, reason, act, observe again.
- **Planner / executor / verifier** — split high-level task decomposition from low-level tool execution and final checking.
- **Cheap search with verifier** — explore a small number of alternatives, prune with tests or other deterministic checks, avoid full tree search unless the task justifies the cost.

This convergence is rational. Single loops wander, repeat mistakes, and exhaust context. Full search is expensive. The stable middle is a workflow that plans just enough, executes bounded steps, verifies aggressively, and retries under budget.

## Benchmarks shape scaffold ecology

Benchmarks do not merely measure agent systems. They reward particular task constructions, and agent systems adapt to that reward surface.

SWE-bench rewards repo navigation, localization, patch generation, and test-driven repair. Scaffold design therefore converges toward:

> read issue -> inspect repo -> localize files -> edit patch -> run tests -> repair

Terminal-Bench rewards terminal-state management, command recovery, and long-horizon execution in a sandbox. Scaffold design therefore converges toward:

> inspect environment -> plan shell actions -> checkpoint state -> run commands -> verify artifacts -> recover from failures

OSWorld rewards screen grounding and GUI-state recovery. GAIA rewards search discipline, tool use, and answer formatting under an exact-answer oracle.

The benchmark is not just a measurement surface. It is a shaping force. Over time, high-scoring systems become co-adapted to the benchmark's oracle, timeouts, tool interface, and sample distribution.

## What the score is measuring

Once scaffolds converge, a leaderboard score is not a clean measurement of raw model capability. It is a dated observation of a joint object:

> model + scaffold + harness + prompt + tools + oracle + sample distribution + budget

The score may still be useful. It may even be highly predictive for that benchmark. But the safe inference narrows.

Unsafe inference:

> System A scores higher, therefore Model A is generally more capable.

Safer inference:

> This model/scaffold/harness configuration is better adapted to this benchmark construction under this budget.

## What convergence hides

When scaffolds look similar at the architecture level, the remaining differences are easy to underreport:

- verifier policy: exact tests, LLM judge, heuristic checks, or no gate
- retry policy: how many attempts, when to change strategy, when to stop
- context policy: what is retained, summarized, dropped, or re-read
- tool policy: shell restrictions, browser access, filesystem visibility, network rules
- failure taxonomy: whether errors are classified or merely retried
- budget policy: token, wallclock, branch count, and parallelism limits

Two submissions can both be "planner-executor-verifier" systems and still differ materially on all of these.

## What would make the claim stronger

Reports should include enough information to distinguish model gain from scaffold fit:

1. **Scaffold topology** — ReAct, planner/executor, verifier-gated, branch/search, multi-agent.
2. **Verifier regime** — tests, exact match, static analysis, screenshots, LLM judge, human review.
3. **Budget and retry policy** — max tool calls, wallclock, branches, repair rounds.
4. **Harness version and tool surface** — what the agent could observe and modify.
5. **Ablations** — same model without the scaffold feature being claimed.
6. **Failure taxonomy** — what kinds of tasks remain unsolved.
7. **Transfer check** — whether the same scaffold improves a structurally different benchmark.

The key question is not only:

> Which system scored higher?

It is:

> Which part of the joint object caused the difference, and does that part transfer outside this benchmark construction?

## Relation to task ontology and work routing

This note does not require a new primitive. Scaffold convergence is a consequence of existing task structure variables: actor boundary, tools, feedback, decomposition, context locality, verification hardness, cost, and oracle shape.

The operational implication belongs in work routing:

> Route by task structure, not by prompt or benchmark name.

Some tasks need decomposition. Some need deterministic verification. Some need search. Some need context reconstruction. Some should stop rather than retry. A converged scaffold family becomes valuable only when it is routed conditionally by the task structure in front of it.

## Origin

This note formalizes an internal reading of current agent benchmark practice across SWE-bench, Terminal-Bench, GAIA, and OSWorld-style evaluations: scaffold topologies are converging, while leaderboard claims still often treat scores as if they were primarily model capability signals.
