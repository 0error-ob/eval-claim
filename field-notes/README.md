# Field Notes

Public evaluation claims read through the templates in this repo.

Each note follows [templates/claim-reading.md](../templates/claim-reading.md) and stays concise. Notes anchor to the original public artifact when possible. The recurring question: before drawing a conclusion from this artifact, what task structure did it actually measure?

Notes accumulate as relevant public claims surface. There is no posting schedule.

Field notes are examples of claim readings. They are not verdicts on the artifact, benchmark, model, or project being discussed.

---

## Quality gate

A note must clear both bars before it goes in:

1. **Grounded in the professional domain.** The observation must come from direct contact with a real artifact, benchmark, or result — not from assembling things that are already known. If the note could have been written by someone who has never run an eval, it belongs in a tutorial, not here.

2. **Not field consensus repackaged.** If the core claim is already the default understanding among people who work in this area, the note has no standing. The test: would a practitioner reading the first paragraph think "yes, obviously"? If so, discard or merge into a note that adds something they don't already know.

These are hard stops. Notes that fail either bar will be merged, demoted to callouts, or deleted. A short note that says something true and non-obvious is strictly better than a long note that says something true and obvious.

---

- [001 — Saturation narrows inference](./001-saturation-narrows-inference.md) — How benchmark saturation changes what a leaderboard score can safely support.
- [002 — Three causes of perceived regression](./002-three-causes-of-perceived-regression.md) — Why "the model got worse" is not yet an attribution claim.
- [003 — Scaffold convergence and benchmark co-adaptation](./003-scaffold-convergence-and-coadaptation.md) — Why agent leaderboard scores increasingly measure fit between model, scaffold, harness, oracle, and benchmark construction.
- [004 — Implementation-contingent oracle artifacts and cleanroom claims](./004-implementation-contingent-oracle.md) — When cleanroom failure does not evidence failure to understand the task: oracles that pin to historically-accidental implementation details not recoverable under behavior-visible evidence. Includes: score comparability across evidence surfaces.

---

**Callout — local rehearsal vs official score**

A local run under the benchmark's published eval script is evidence of harness compatibility. If the harness is identical to what the benchmark authority runs, the local score has strong provisional comparability — the main residual risk is environment, not measurement setup. It is still not an official leaderboard result until accepted or published by the benchmark authority. Submission-pending is a distinct state from both "local rehearsal" and "official result," and must be labeled as such in any public claim.
