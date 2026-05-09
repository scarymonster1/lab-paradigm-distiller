#!/usr/bin/env python3
"""Check a generated lab-line research-paradigm SKILL.md.

Usage:
    python quality_check.py <path-to-generated-SKILL.md>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Advisor Stance",
    "Corpus",
    "Answer Workflow",
    "Paradigm Lenses",
    "Research Heuristics",
    "Method Grammar",
    "Evidence Standard",
    "Writing DNA",
    "Proposal Generator",
    "Anti-Patterns",
    "Holdout Backtest",
    "Honest Boundaries",
    "Sources",
]

PROPOSAL_FIELDS = [
    "Problem",
    "Core hypothesis",
    "Method",
    "Experiment",
    "Expected contribution",
    "Failure risk",
    "Why this fits the lab paradigm",
]


def section_present(content: str, section: str) -> bool:
    pattern = rf"^##\s+{re.escape(section)}\s*$"
    return bool(re.search(pattern, content, flags=re.MULTILINE | re.IGNORECASE))


def count_lenses(content: str) -> int:
    match = re.search(
        r"^##\s+Paradigm Lenses\s*(.*?)(?=^##\s+)",
        content,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return 0
    return len(re.findall(r"^###\s+", match.group(1), flags=re.MULTILINE))


def count_heuristics(content: str) -> int:
    match = re.search(
        r"^##\s+Research Heuristics\s*(.*?)(?=^##\s+)",
        content,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return 0
    return len(re.findall(r"^\s*\d+\.\s+\*\*", match.group(1), flags=re.MULTILINE))


def has_frontmatter(content: str) -> bool:
    content = content.lstrip("\ufeff")
    return bool(re.match(r"^---\nname:\s*[-a-z0-9]+\ndescription:\s*(?:\||>).+?\n---", content, flags=re.DOTALL))


def list_items_in_section(content: str, section: str) -> int:
    match = re.search(
        rf"^##\s+{re.escape(section)}\s*(.*?)(?=^##\s+|\Z)",
        content,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return 0
    return len(re.findall(r"^\s*[-*]\s+", match.group(1), flags=re.MULTILINE))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python quality_check.py <path-to-generated-SKILL.md>", file=sys.stderr)
        return 2

    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"Missing file: {skill_path}", file=sys.stderr)
        return 1
    skill_dir = skill_path.parent

    content = skill_path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
    checks: list[tuple[str, bool, str]] = []

    checks.append(("frontmatter", has_frontmatter(content), "requires name and description"))

    missing_sections = [section for section in REQUIRED_SECTIONS if not section_present(content, section)]
    checks.append(("required sections", not missing_sections, ", ".join(missing_sections) or "all present"))

    lenses = count_lenses(content)
    checks.append(("paradigm lenses", 3 <= lenses <= 6, f"{lenses} found; expected 3-6"))

    heuristics = count_heuristics(content)
    checks.append(("research heuristics", 5 <= heuristics <= 10, f"{heuristics} found; expected 5-10"))

    missing_fields = [field for field in PROPOSAL_FIELDS if field not in content]
    checks.append(("proposal fields", not missing_fields, ", ".join(missing_fields) or "all present"))

    boundary_items = list_items_in_section(content, "Honest Boundaries")
    checks.append(("honest boundaries", boundary_items >= 4, f"{boundary_items} list items; expected at least 4"))

    anti_patterns = list_items_in_section(content, "Anti-Patterns")
    checks.append(("anti-patterns", anti_patterns >= 3, f"{anti_patterns} list items; expected at least 3"))

    has_holdout = bool(re.search(r"holdout|留出|backtest|回测", content, flags=re.IGNORECASE))
    checks.append(("holdout validation", has_holdout, "must include holdout/backtest evidence or explanation"))

    required_paths = [
        skill_dir / "sources" / "papers",
        skill_dir / "sources" / "texts",
        skill_dir / "references" / "corpus-metadata.json",
        skill_dir / "references" / "paper-cards",
        skill_dir / "references" / "research",
        skill_dir / "references" / "validation" / "holdout-backtest.md",
        skill_dir / "references" / "validation" / "new-proposal-test.md",
        skill_dir / "references" / "validation" / "revision-log.md",
    ]
    missing_paths = [str(path.relative_to(skill_dir)) for path in required_paths if not path.exists()]
    checks.append(("supporting artifacts", not missing_paths, ", ".join(missing_paths) or "all present"))

    passed = 0
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{status:4} {name}: {detail}")
        passed += int(ok)

    print(f"\nResult: {passed}/{len(checks)} checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
