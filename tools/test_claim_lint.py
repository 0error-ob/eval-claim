#!/usr/bin/env python3
"""Unit tests for claim_lint. Run with: python test_claim_lint.py"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from claim_lint import (
    ClaimCard,
    check_overreach,
    check_required_sections,
    check_ledger_alignment,
    lint,
)


CLEAN_CARD = """# Card
## 1. Run identity
Run ID: r1

## Benchmark
Benchmark name: TB 2.1
Dataset: terminal-bench/terminal-bench-2-1

## Model
Model identifier: anthropic/claude-opus-4-7

## Allowed claims
Under harbor 0.6.4 and claude-opus-4-7, this agent produced 66/89 = 74.2% on the TB 2.1 leaderboard metric.

## Unsupported claims
This agent is model-agnostic.
This agent generalizes to other benchmarks.
"""


OVERREACH_CARD = """# Card
## Benchmark
Benchmark name: TB 2.1

## Model
Model identifier: anthropic/claude-opus-4-7

## Allowed claims
This scaffold is model-agnostic and generalizes to other agentic benchmarks.
It outperforms all other agents and is universally superior.

## Unsupported claims
None.
"""


MISSING_SECTION_CARD = """# Card
## Allowed claims
The agent scored 74.2% under controlled conditions.
"""


LEDGER_ONE_MODEL = {
    "run_identity": {
        "run_id": "tbench-2.1-k5-v01",
        "task_id": "task-1",
        "trial_id": "trial-1",
        "benchmark": "terminal-bench-2-1",
        "model": "anthropic/claude-opus-4-7",
    },
    "task": {"actor": "scaffold agent", "goal": "pass verifier"},
    "phases": [],
}


LEDGER_DIFFERENT_MODEL = {
    "run_identity": {
        "run_id": "tbench-2.1-k5-v01",
        "task_id": "task-1",
        "trial_id": "trial-1",
        "benchmark": "terminal-bench-2-1",
        "model": "openai/gpt-5.5",
    },
    "task": {"actor": "scaffold agent", "goal": "pass verifier"},
    "phases": [],
}


def _write(text: str, suffix: str = ".md") -> Path:
    fd = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8")
    fd.write(text)
    fd.close()
    return Path(fd.name)


def _write_json(obj: dict) -> Path:
    return _write(json.dumps(obj), suffix=".json")


class TestParse(unittest.TestCase):
    def test_extracts_numbered_sections(self):
        card = ClaimCard.parse(CLEAN_CARD)
        self.assertIn("Run identity", card.sections)
        self.assertIn("Allowed claims", card.sections)

    def test_get_is_case_insensitive_and_partial(self):
        card = ClaimCard.parse(CLEAN_CARD)
        self.assertIsNotNone(card.get("allowed claims"))
        self.assertIsNotNone(card.get("Benchmark"))


class TestRequiredSections(unittest.TestCase):
    def test_clean_card_passes(self):
        card = ClaimCard.parse(CLEAN_CARD)
        findings = check_required_sections(card)
        self.assertEqual(findings, [])

    def test_missing_unsupported_section_fails(self):
        card = ClaimCard.parse(MISSING_SECTION_CARD)
        findings = check_required_sections(card)
        self.assertTrue(any(f.severity == "FAIL" for f in findings))


class TestOverreach(unittest.TestCase):
    def test_clean_card_no_overreach(self):
        # Allowed section has no forbidden phrases (model-agnostic is in Unsupported).
        card = ClaimCard.parse(CLEAN_CARD)
        findings = check_overreach(card)
        self.assertEqual(findings, [])

    def test_overreach_card_has_findings(self):
        card = ClaimCard.parse(OVERREACH_CARD)
        findings = check_overreach(card)
        # Expect at least: model-agnostic, generalizes to, outperforms, universally
        self.assertGreaterEqual(len(findings), 4)
        messages = " ".join(f.message for f in findings)
        self.assertIn("Model-agnostic", messages)


class TestLedgerAlignment(unittest.TestCase):
    def test_matching_model_no_finding(self):
        card = ClaimCard.parse(CLEAN_CARD)
        findings = check_ledger_alignment(card, LEDGER_ONE_MODEL)
        # Clean card's Allowed section doesn't claim cross-model, ledger model matches card.
        self.assertEqual(findings, [])

    def test_card_model_not_in_ledger(self):
        card = ClaimCard.parse(CLEAN_CARD)
        findings = check_ledger_alignment(card, LEDGER_DIFFERENT_MODEL)
        self.assertTrue(any("Model" == f.section for f in findings))


class TestIntegration(unittest.TestCase):
    def test_lint_clean(self):
        claim = _write(CLEAN_CARD)
        findings = lint(claim, None)
        self.assertEqual(findings, [])

    def test_lint_overreach(self):
        claim = _write(OVERREACH_CARD)
        findings = lint(claim, None)
        self.assertTrue(any(f.severity == "WARN" for f in findings))

    def test_lint_missing_section(self):
        claim = _write(MISSING_SECTION_CARD)
        findings = lint(claim, None)
        self.assertTrue(any(f.severity == "FAIL" for f in findings))

    def test_lint_with_matching_ledger(self):
        claim = _write(CLEAN_CARD)
        ledger = _write_json(LEDGER_ONE_MODEL)
        findings = lint(claim, ledger)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
