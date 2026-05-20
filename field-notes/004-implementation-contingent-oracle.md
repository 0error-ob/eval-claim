# 004 — Implementation-contingent oracle artifacts and cleanroom claims

**Type:** Benchmark construction / cleanroom score interpretation  
**Question:** When a cleanroom agent fails to reproduce oracle behavior, what does the failure evidence support?  
**Status:** Claim reading, not benchmark criticism

Cleanroom benchmark tasks ask an actor to reproduce a target tool's behavior by observing only its inputs and outputs — without access to source code. When a cleanroom agent scores below 100%, the standard reading is: the agent failed to identify some behavioral rule. This note examines a subclass where that reading does not hold.

## Implementation-contingent oracle artifacts

Some benchmark oracles pin to implementation details that are:

1. **Not semantically necessary**: any correct algorithm could use a different choice with equivalent behavioral validity
2. **Not derivable from the public specification or behavioral observation**: no input/output pair distinguishes the correct choice from competing alternatives
3. **Historical accidents**: the artifact reflects how the original developer happened to organize their code, not a principled specification decision

Examples:

- Internal enum or constant ordering in an iota-enumerated AST node type table. Sort output depends on this ordering via hash comparison. No behavioral probe can distinguish 49! possible orderings.
- A traversal choice in a tree algorithm where multiple valid traversals produce identical outputs on any feasible test input.
- A specific nil-deref line number in a legacy code path that tests assert on, where the line number depends on comment and blank-line placement in the original source.

When such artifacts exist, the oracle's scoring condition is:

```
semantic specification + implementation-contingent artifact = oracle pass condition
```

A cleanroom agent that correctly implements the semantic specification but does not replicate the implementation-contingent artifact fails the oracle. This failure does not evidence inability to understand the task.

## Identifiability as the mediating concept

The key distinction is **identifiability**: whether the actor can, under the allowed evidence surface, identify which implementation-contingent choice the oracle uses.

This is relative to evidence surface (task-ontology dimension 14), not absolute:

- At source-visible evidence: every implementation artifact is recoverable by reading the source.
- At behavior-visible evidence only: an artifact is non-discriminable when the hypothesis space (all choices that produce observationally equivalent behavior) is too large to narrow through feasible probing.

Non-discriminable does not mean unknowable in principle. It means unknowable within the allowed evidence surface. Changing the evidence surface changes this dimension — and changes the task.

## What the claim supports

| Scenario | What the cleanroom score supports |
|---|---|
| Task is highly identifiable; agent scores 100% | Agent successfully discovered the behavioral specification |
| Task is highly identifiable; agent scores 85% | Agent missed some behavioral rule identifiable through more careful probing |
| Task has non-discriminable artifact; agent scores 85% | Partially ambiguous — may reflect missed rules AND unrecoverable artifact; requires ceiling analysis |
| Task has non-discriminable artifact; agent scores 100% | Agent successfully guessed the implementation-contingent artifact, OR used non-cleanroom evidence; requires explicit claim investigation |

The third and fourth rows are the problematic claims. A 100% cleanroom score on a non-discriminable task does not, without further investigation, prove that pure spec discovery succeeded.

## Operational implication

Before reporting a cleanroom score, check whether any failing tests (or surprising passes) correspond to implementation-contingent artifacts. If so:

- The ceiling for pure spec discovery may be lower than 100%.
- The gap between spec-discovery ceiling and 100% is a structural artifact gap, not an agent capability gap.
- A 100% result in this gap must state how the artifact was identified (probe, test-informed, or source access).

## Score comparability across evidence surfaces

A corollary: the same numeric score under different evidence surfaces does not support the same claim.

100% under behavior-visible evidence (binary/docs only) and 100% under source-visible evidence are structurally distinct results. Under source-visible evidence, implementation-contingent artifacts — constant ordering, undocumented tie-breaking rules, historically-fixed enum values — are directly readable. Under behavior-visible evidence, those same artifacts may be non-discriminable regardless of how carefully the agent probes.

A score gap relative to the 100% ceiling may therefore reflect an insufficient evidence surface, not an agent capability gap. The ceiling is a property of the interface between task construction and evidence surface, not of the actor.

Safe comparison rule: scores are only directly comparable when produced under the same evidence surface label. A score reported with no evidence surface stated licenses no specific capability claim.

Any score citation should bundle: **score + evidence surface label + claim type**.

## Relation to eval-claim principles

This note extends `run-type-boundary.md`'s principle that the evidence surface must be stated alongside the score. The extension:

> The task structure must also be assessed for non-discriminable artifacts. A score gap that is not closeable by additional probing under the allowed evidence surface is a structural ceiling, not an agent capability gap. These must be labeled separately.

## Origin

Derived from analysis of a binary reimplementation benchmark task where 49 internal AST node type constants, ordered by the original implementation, determine hash ordering and thereby group sort order. Under behavior-visible evidence, no feasible probe sequence can identify the correct ordering among 49! possibilities. An agent that reads source achieves 100%; an agent restricted to behavior-visible evidence is bounded below 100% on any test that exercises group ordering — regardless of algorithmic understanding.
