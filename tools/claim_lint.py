#!/usr/bin/env python3
"""claim_lint: minimal lint for evaluation claim cards.

Reads a filled claim card (markdown) and optionally the ledger it cites.
Reports findings when the claim travels beyond the evidence surface.

This is a stdlib-only linter. It performs keyword and structural checks, not
semantic understanding. It catches the common shapes of overreach; it cannot
catch every problem.

Usage
-----
    python claim_lint.py check claim.md
    python claim_lint.py check claim.md --ledger ledger.json
    python claim_lint.py check claim.md --strict

Exit codes
----------
    0  OK         no findings
    1  WARN       findings present
    2  FAIL       missing required section, malformed input, or --strict + findings
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REQUIRED_SECTIONS = (
    "Allowed claims",
    "Unsupported claims",
)


OVERREACH_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bmodel-?agnostic\b",
     "Model-agnostic claims require evidence across multiple models."),
    (r"\bgeneralizes?\s+to\b",
     "Generalization claims require evidence beyond the cited benchmark."),
    (r"\bstronger\s+than\s+(?:other\s+)?models?\b",
     "Cross-model strength claims require holding the agent constant across models."),
    (r"\bbetter\s+than\s+(?:other\s+)?models?\b",
     "Cross-model superiority claims require a controlled comparison."),
    (r"\boutperforms?\s+(?:all\s+)?(?:other\s+)?(?:models|agents|baselines)\b",
     "Outperform-all claims require a complete baseline set."),
    (r"\bstate[\s-]of[\s-]the[\s-]art\b|\bSOTA\b",
     "SOTA claims should cite the leaderboard view and date."),
    (r"\buniversally\b",
     "Universality claims are unsupportable from one benchmark."),
    (r"\b(?:on|across)\s+all\s+benchmarks\b",
     "Cross-benchmark claims require runs on those benchmarks."),
    (r"\bgeneral(?:ly)?\s+(?:better|stronger|superior)\b",
     "Generality claims require evidence across task families."),
)


@dataclass
class Finding:
    severity: str  # "WARN" or "FAIL"
    section: str
    message: str
    evidence: str = ""

    def format(self) -> str:
        head = f"{self.severity}: [{self.section}] {self.message}"
        if self.evidence:
            head += f"\n        evidence: {self.evidence.strip()[:120]}"
        return head


@dataclass
class ClaimCard:
    raw: str
    sections: dict[str, str] = field(default_factory=dict)

    @classmethod
    def parse(cls, text: str) -> "ClaimCard":
        sections: dict[str, str] = {}
        # Match any markdown header containing the section name.
        # E.g. "## 12. Allowed claims" -> section name "Allowed claims".
        header_re = re.compile(r"^#{1,6}\s+(?:\d+\.\s*)?(.+?)\s*$", re.MULTILINE)
        matches = list(header_re.finditer(text))
        for i, m in enumerate(matches):
            name = m.group(1).strip().rstrip(":")
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections[name] = text[start:end].strip()
        return cls(raw=text, sections=sections)

    def get(self, name: str) -> str | None:
        # Try exact match, then case-insensitive partial match.
        if name in self.sections:
            return self.sections[name]
        lower = name.lower()
        for key, body in self.sections.items():
            if key.lower() == lower or lower in key.lower():
                return body
        return None


def check_required_sections(card: ClaimCard) -> list[Finding]:
    findings: list[Finding] = []
    for name in REQUIRED_SECTIONS:
        if card.get(name) is None:
            findings.append(Finding(
                severity="FAIL",
                section=name,
                message=f"Required section '{name}' not found in claim card.",
            ))
    return findings


def check_overreach(card: ClaimCard) -> list[Finding]:
    findings: list[Finding] = []
    allowed = card.get("Allowed claims") or ""
    for pattern, message in OVERREACH_PATTERNS:
        for match in re.finditer(pattern, allowed, flags=re.IGNORECASE):
            line = _line_for(allowed, match.start())
            findings.append(Finding(
                severity="WARN",
                section="Allowed claims",
                message=message,
                evidence=line,
            ))
    return findings


def check_ledger_alignment(card: ClaimCard, ledger: dict) -> list[Finding]:
    findings: list[Finding] = []
    run = ledger.get("run_identity", {}) if isinstance(ledger, dict) else {}

    # Benchmark mentioned in card must match ledger.
    benchmark_section = card.get("Benchmark") or ""
    if benchmark_section and run.get("benchmark"):
        ledger_benchmark = run["benchmark"]
        if ledger_benchmark.lower() not in benchmark_section.lower() \
           and ledger_benchmark.split("/")[-1].lower() not in benchmark_section.lower():
            findings.append(Finding(
                severity="WARN",
                section="Benchmark",
                message=f"Claim names a benchmark not present in ledger run_identity.benchmark ({ledger_benchmark}).",
            ))

    # Model in card must match ledger.
    model_section = card.get("Model") or ""
    if model_section and run.get("model"):
        ledger_model = run["model"]
        if ledger_model.lower() not in model_section.lower():
            findings.append(Finding(
                severity="WARN",
                section="Model",
                message=f"Claim names a model not present in ledger run_identity.model ({ledger_model}).",
            ))

    # If claim mentions "model-agnostic" or cross-model and ledger has one model, that's overreach.
    allowed = card.get("Allowed claims") or ""
    if run.get("model") and re.search(r"\bmodel-?agnostic\b|\bacross\s+models\b", allowed, re.IGNORECASE):
        findings.append(Finding(
            severity="WARN",
            section="Allowed claims",
            message="Claim suggests cross-model evidence, but ledger contains only one model.",
            evidence=f"ledger.run_identity.model = {run['model']}",
        ))

    return findings


def _line_for(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return text[start:end]


def lint(claim_path: Path, ledger_path: Path | None) -> list[Finding]:
    try:
        text = claim_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [Finding(severity="FAIL", section="input", message=f"Claim file not found: {claim_path}")]

    card = ClaimCard.parse(text)

    findings: list[Finding] = []
    findings.extend(check_required_sections(card))
    findings.extend(check_overreach(card))

    if ledger_path is not None:
        try:
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            findings.append(Finding(severity="FAIL", section="input",
                                    message=f"Ledger file not found: {ledger_path}"))
            return findings
        except json.JSONDecodeError as exc:
            findings.append(Finding(severity="FAIL", section="input",
                                    message=f"Ledger not valid JSON: {exc}"))
            return findings
        findings.extend(check_ledger_alignment(card, ledger))

    return findings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="claim_lint", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    check = sub.add_parser("check", help="Lint a claim card")
    check.add_argument("claim", type=Path, help="Path to the claim card markdown.")
    check.add_argument("--ledger", type=Path, default=None,
                       help="Optional path to a ledger JSON for cross-check.")
    check.add_argument("--strict", action="store_true",
                       help="Treat WARN findings as FAIL.")
    args = parser.parse_args(argv)

    if args.cmd != "check":
        parser.print_help()
        return 2

    findings = lint(args.claim, args.ledger)

    if not findings:
        print("OK: no findings.")
        return 0

    has_fail = any(f.severity == "FAIL" for f in findings)
    has_warn = any(f.severity == "WARN" for f in findings)

    for f in findings:
        print(f.format())

    if has_fail:
        return 2
    if has_warn and args.strict:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
