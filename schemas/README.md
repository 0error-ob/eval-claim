# Schemas

Structured formats that turn `eval-claim` from a reading practice into a producible artifact set. A claim card is what humans publish. A ledger is what agents produce. The schemas define both surfaces so they can be linted, diffed, and reused across runs.

---

## What's here

- [agent-run-ledger.schema.json](./agent-run-ledger.schema.json) — JSON Schema for the per-trial ledger an agent produces during execution.

The corresponding human-publication template lives at [../templates/agent-benchmark-claim-card.md](../templates/agent-benchmark-claim-card.md).

---

## Eval-grade ledger

The ledger schema names a specific kind of artifact: **structured evidence that an evaluation claim can be cited against**. It is not a transcript, not a cost log, not a memory store.

What makes a ledger eval-grade:

- **Task structure is recorded explicitly.** Goal, constraints, tools, environment — using [task-ontology primitives](https://github.com/0error-ob/task-ontology/blob/main/PRIMITIVES.md). The agent's view of the task is itself a data field, not implicit in conversation context.
- **Phases are first-class.** The ledger records *when* the agent moved from probe to execute to verify to stop. Failure analysis depends on knowing which phase the failure occurred in.
- **Verifier output is reproducible.** Whatever command established success/failure is recorded with its exit code and stderr. A reviewer can re-run it.
- **Stop condition is named.** Every trial ends for a stated reason — `verifier_pass`, `timeout`, `exception`, `budget_exhausted`. "It just stopped" is not a stop condition.

A ledger that has these fields can be cited as evidence in a [claim card](../templates/agent-benchmark-claim-card.md). A ledger missing them cannot — the claim cannot be tied to specific evidence.

---

## What this is not

This schema is unrelated to:

- **Cost-tracking ledgers** (e.g. tooling that records how many tokens a developer's coding sessions consumed). Those are accounting artifacts; this is an evidence artifact.
- **Generic agent transcripts.** A raw transcript records what was said. A ledger records what was *decided* and *verified*.
- **Replay logs for fine-tuning.** This schema does not target training-data formats.

The boundary matters because the field is already overloaded. The word *ledger* gets used for cost tracking, for state management, for memory systems. Here it means one specific thing: **the evidence base of an evaluation claim**.

---

## Versioning

Schema is at `v0`. The `$id` field will receive a versioned URL once a stable v1 ships. Breaking changes between v0 versions are allowed.

Field names that come from task-ontology track that repo's versioning. If a primitive is renamed there, this schema follows.

---

## How to use

A scaffold or harness that produces ledgers conforming to this schema should:

1. Emit one ledger per trial, named by `run_identity.trial_id`.
2. Record `run_identity` at the top level — even if it duplicates the parent run's metadata, the duplication is intentional so a single ledger is self-describing.
3. Populate the `task` block at the end of the probe phase. The act of populating it is the probe.
4. Append phase records as execution proceeds. Do not write phases retroactively; the order matters.
5. Record `stop_condition` before the trial ends. If the trial is killed externally, the harness records the stop condition on the ledger's behalf.

The companion tool [../tools/claim_lint.py](../tools/claim_lint.py) reads claims and (optionally) the ledgers they cite, and flags claims that travel beyond their evidence base.
