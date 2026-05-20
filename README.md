# eval-claim

### Reading AI Evaluation Claims

Templates and worked examples for analyzing what public AI evaluation claims are actually allowed to support.

The core question: **What does this score actually license?**

Vocabulary: [task-ontology v0.1.2](https://github.com/0error-ob/task-ontology) — primitives, dimensions, benchmark maps.

---

## Use this repo when you need to

- turn an eval result into a defensible public claim
- explain what a benchmark score does and does not show
- compare two model results without overclaiming
- write a model migration note for a specific workflow
- review a leaderboard claim before citing it
- prepare a release note, blog post, or README section involving eval results

---

## One-minute example

**Claim:** Model A is better than Model B because it scores 93% vs 90% on Benchmark X.

**Artifact:** Public leaderboard entry.

**Task structure:** Fixed sample of single-shot tasks with frozen ground-truth answers.

**Oracle:** Programmatic match against reference outputs.

**Dominant dimensions:** Verification regime (oracle-rich, single-turn). Decomposition depth, ambiguity load, and irreversibility are absent.

**Allowed inference:** Under this harness and oracle, Model A produced more reference-matching outputs than Model B on this fixed sample.

**Unsupported inference:** Model A is generally better; Model A will outperform B in a multi-turn agent loop, a weak-oracle product workflow, or any setting where success is not reference-match.

---

## Templates

- [templates/claim-reading.md](./templates/claim-reading.md) — analyze a single public eval claim across seven fields.
- [templates/run-type-boundary.md](./templates/run-type-boundary.md) — label a benchmark run before reporting it: evidence surface, harness conditions, comparability, allowed/disallowed claims.
- [templates/migration-note.md](./templates/migration-note.md) — write a defensible model migration recommendation in cohort terms.
- [templates/agent-benchmark-claim-card.md](./templates/agent-benchmark-claim-card.md) — structured card to fill before publishing an agent-benchmark result. Companion to the ledger schema below.
- [QUICKSTART.md](./QUICKSTART.md) — three longer diagnostic templates: benchmark, agent regression, model migration.

---

## Schemas and tools

The reading templates above are for analyzing other people's claims. The pieces below are for producing your own:

- [schemas/agent-run-ledger.schema.json](./schemas/agent-run-ledger.schema.json) — JSON Schema for the per-trial ledger an agent produces during execution. Field names follow [task-ontology primitives](https://github.com/0error-ob/task-ontology/blob/main/PRIMITIVES.md). See [schemas/README.md](./schemas/README.md) for the "eval-grade ledger" position.
- [tools/claim_lint.py](./tools/claim_lint.py) — minimal linter that reads a claim card and (optionally) the ledger it cites, and flags claims that travel beyond their evidence.

---

## Examples

- [examples/](./examples/) — worked applications: benchmark leaderboard claim, agent regression, model migration eval.

---

## Field notes

- [field-notes/](./field-notes/) — public eval claims read through these templates as they surface.

---

## Status

Active. Templates and examples accumulate as claims surface; vocabulary is stable in [task-ontology](https://github.com/0error-ob/task-ontology).
