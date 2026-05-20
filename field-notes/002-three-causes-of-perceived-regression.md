# 002 — Three causes of perceived regression

**Type:** Regression claim  
**Question:** What attribution does the observed degradation support?  
**Status:** Claim reading, not regression detection

When users report "it got worse" or a monitoring tool flags a regression, the complaint is real. What it is not yet is an attribution.

At minimum three structurally distinct causes can produce the same phenomenology — a user who experiences degraded output quality over time:

## The three causes

**1. Model-side change**
The underlying model weights or sampling behavior changed. Given identical inputs on identical tasks, outputs differ from a prior window. This is the cause most discussions implicitly assume.

**2. Task-mix shift**
The distribution of what the user asked for changed — longer sessions, more complex repos, less verifiable tasks, different tool configurations. The model may be performing identically on each task type; the aggregate score shifts because the workload shifted.

**3. Harness or scaffolding change**
The evaluation setup, prompt injection, tool surface, default settings, or session persistence behavior changed independently of the model. A harness-side change can degrade effective task quality even when both model and workload are unchanged.

## Why the distinction matters

Each cause implies a different diagnostic and a different fix:

- If **model-side**: the remedy is repeated runs on static frozen tasks, comparing outputs on identical input/context/config across a version boundary.
- If **task-mix shift**: the remedy is cohort stratification — compare within the same task type before aggregating. The apparent regression may disappear once the workload change is controlled for.
- If **harness change**: the remedy is harness versioning — replay prior sessions through the old configuration and compare against the new one.

These interventions are not interchangeable. A harness replay will not detect a model regression. A static benchmark will not catch a task-mix shift. A cohort analysis will not isolate a harness change.

## What "drift" hides

Labeling all three causes "drift" is a pre-attribution move: it treats the symptom as if it were already an explanation. A metric that moves over time — read/edit ratio, reasoning loops per turn, error phrase frequency, tokens per session — does not tell you which of the three caused the move. Calling the move "drift" creates the impression that attribution has occurred when it has not.

The diagnostic question is not *is drift present?* It is: *which cause is active?* Until that is answered, any remediation — changing models, changing harnesses, changing prompts — is untargeted.

## Origin

This note formalizes a decomposition that applies across contexts: monitoring tools detecting session-level change, users reporting perceived quality degradation, and benchmarks claiming model regression.
