# Worked example: Agent regression claim

**Scenario.** A local agent observability tool scans a user's recent AI-coding-agent session logs and reports that the agent's behavior has degraded over the past 60 days. The tool computes metrics across all sessions in the window — read:edit ratio, reasoning loop count, tool diversity, mean tokens per turn — and outputs a verdict like *CONFIRMED REGRESSION*. The user reads this and asks: *should I update my beliefs about the model?*

This is a real class of claim. The pattern below applies to any tool of this shape.

We apply [Template 2 — Agent regression claim](../QUICKSTART.md#template-2--agent-regression-claim) from QUICKSTART.

---

## 1. What task is being constructed?

Not one task. A *stream* of tasks in the same family (coding-with-an-agent), each varying session by session.

The actor is the agent. The goal in any given session is "the code change the user described." The operating environment is the user's local repo plus whatever tool harness mediates the agent (file read/edit, shell, web). The action space is reading code, editing code, running commands, and (sometimes) asking the user for clarification.

The user is doing different work each session: a bug fix one day, a feature implementation the next, a refactor the day after.

## 2. What is the oracle?

In the actual workflow, the user is the oracle. They accept the agent's diff, request modifications, or abandon the session.

The observability tool does **not** see this oracle. It sees the trace — the sequence of tool calls, message content lengths, file accesses — but not the user's verdict on the work. The tool's metrics (read:edit ratio, reasoning loops, tokens/turn) are *proxies* for what the user actually cared about (did the change land, did the code work, did it require rework).

This proxy gap is the first observation: the tool is reasoning about agent quality from a strict subset of the available signal.

## 3. Which dimensions dominate the result?

From [DIMENSIONS.md](../DIMENSIONS.md), the dimensions most likely to vary across sessions in this scenario:

- **Time horizon** — some sessions are 5 turns, some are 200
- **Context locality** — some touch one file, some touch thirty
- **Verification regime** — some sessions run tests, some don't
- **Mutation pattern** — some are read-heavy investigation, some are write-heavy implementation
- **Greenfield vs brownfield** — creating new files vs editing existing

These dimensions vary **idiosyncratically by what the user is working on this week**. Across a 60-day window, the user's work mix shifts naturally — starting a new project vs maintaining an old one, debugging dense legacy code vs scaffolding a new feature.

## 4. What does the metric see?

A scalar per session, aggregated over the time window.

Concretely, suppose a hypothetical report shows *mean read:edit ratio = 4.2 in the first 30 days and 2.8 in the last 30 days.* The aggregate has shifted. The verdict pipeline reads this as "investigation-per-edit decreased — agent stopped looking before changing — regression."

## 5. What does the metric hide?

The 4.2 → 2.8 shift can have **two structurally different causes** the global aggregate cannot distinguish:

- **Model-side change.** The agent itself, on the same kind of task, now reads less before editing. A genuine behavior shift.
- **Task-mix change.** The user this month is doing more write-heavy implementation work and less debugging-heavy investigation. The same agent on this work mix would naturally produce a lower read:edit ratio.

The verdict cannot distinguish these without **decomposing the metric by task structure first**. A global aggregate collapses every session — debugging, refactoring, greenfield, brownfield, short, long — into one bucket. Any shift in the bucket composition between the before and after windows looks identical to a model behavior shift.

## 6. What inference is unsafe?

> *"The model regressed"* — drawn from a metric shift, when the session corpus has not been controlled for task structure across the before/after windows.

Specifically, the inference fails when:

- The before/after windows have different user-task mixes (which is the normal case across a 60-day work window — user task mix is virtually never stable)
- The tool reports the verdict without per-bucket decomposition
- The tool uses an LLM judge over the trace, compounding a separate concern about self-judging

Without control, the strongest claim the tool can support is: *"a metric shift was observed in this corpus."* Anything stronger — *the model regressed*, *this update is worse*, *capability degraded* — requires task-structure decomposition the global aggregate doesn't provide.

---

## Takeaway

> **Before claiming agent regression, define the task cohort.** A metric shift over uncontrolled task mix reads as model regression but may be workload artifact. The same lens applies to any observability tool that aggregates across heterogeneous sessions.

The structural fix is per-bucket attribution: bucket sessions by task structure first, decompose the metric shift into within-bucket (model-side) and between-bucket (mix-shift) components. The tool then reports *"X% of the shift is mix-driven, Y% is model-driven"* — a falsifiable claim, not a verdict.
