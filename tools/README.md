# tools

Small command-line utilities that operate on the artifacts defined elsewhere in this repo (templates, schemas).

---

## claim_lint.py

Minimal linter for evaluation claim cards. Reads a filled card and (optionally) the ledger it cites; reports findings when the claim travels beyond the evidence surface.

### Usage

```bash
python claim_lint.py check path/to/claim.md
python claim_lint.py check path/to/claim.md --ledger path/to/ledger.json
python claim_lint.py check path/to/claim.md --strict
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | OK — no findings |
| 1 | WARN — findings present (not a hard fail) |
| 2 | FAIL — missing required section, malformed input, or `--strict` and any findings |

### What it checks

1. **Required sections.** `Allowed claims` and `Unsupported claims` must exist. Their absence is a `FAIL`.
2. **Overreach in Allowed.** Phrases that require structural evidence the card cannot provide on its own:
   - `model-agnostic` / `generalizes to` / `stronger than other models` / `outperforms all` / `state-of-the-art` / `universally` / `across all benchmarks`
   - Each match is a `WARN` with the matched line as evidence.
3. **Ledger alignment** (if `--ledger` provided). Compares the card's stated benchmark and model against the ledger's `run_identity` fields. If the card claims cross-model evidence but the ledger contains only one model, that is a `WARN`.

### What it does not check

This linter is structural, not semantic. It will catch the common patterns of overreach but cannot judge whether a quoted number is correct, whether an ablation is well-designed, or whether a reviewer would accept the claim. That is the work the linter prepares for, not replaces.

### Dependencies

Standard library only (`json`, `re`, `argparse`, `dataclasses`). No installation step.

### Run the tests

```bash
python test_claim_lint.py
```

Three sets of cases: parse, individual checks, end-to-end lint.

---

## Adding a new check

To add a new finding category:

1. Decide whether it is a structural check (token presence, missing section) or a cross-artifact check (claim vs ledger).
2. Add a `check_*` function returning `list[Finding]`. Use `Finding.severity` `WARN` for findings that block a strict run, `FAIL` for findings that should always halt.
3. Call it from `lint()`.
4. Add a test case in `test_claim_lint.py`.

Keep the linter stdlib-only. If a check requires semantic understanding, it does not belong here — it belongs in a human review pass.
