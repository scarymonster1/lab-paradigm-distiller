#!/usr/bin/env python3
"""Summarize lab-paradigm research notes for a generated skill folder.

Usage:
    python merge_paper_analysis.py <generated-skill-dir>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DIMENSIONS = {
    "01-problem-selection": "problem selection",
    "02-core-assumptions": "core assumptions",
    "03-method-stack": "method stack",
    "04-evidence-standard": "evidence standard",
    "05-paper-framing": "paper framing",
    "06-evolution-timeline": "evolution timeline",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")


def count_paper_mentions(content: str) -> int:
    patterns = [
        r"^\s*(?:-\s*)?(?:Paper|论文)\s*[:：]",
        r"^\|\s*(?:seed|distill|holdout)\s*\|.*$",
        r"^\s*#{2,4}\s+.*\((?:19|20)\d{2}\)",
        r"\barXiv:\s*\d{4}\.\d+",
        r"https?://(?:arxiv\.org|doi\.org|openreview\.net|aclanthology\.org|dl\.acm\.org|ieeexplore\.ieee\.org)[^\s)\]]+",
    ]
    hits: set[str] = set()
    for pattern in patterns:
        hits.update(re.findall(pattern, content, flags=re.IGNORECASE | re.MULTILINE))
    return len(hits)


def count_confidence(content: str) -> dict[str, int]:
    return {
        "high": len(re.findall(r"\bhigh\b|高置信|置信[:：]\s*高", content, flags=re.IGNORECASE)),
        "medium": len(re.findall(r"\bmedium\b|中置信|置信[:：]\s*中", content, flags=re.IGNORECASE)),
        "low": len(re.findall(r"\blow\b|低置信|置信[:：]\s*低", content, flags=re.IGNORECASE)),
    }


def extract_findings(content: str, limit: int = 3) -> list[str]:
    headings = [
        h.strip()
        for h in re.findall(r"^#{2,4}\s+(.+)$", content, flags=re.MULTILINE)
        if not h.lower().startswith(("paper", "论文"))
    ]
    if headings:
        return headings[:limit]

    bolds = [b.strip() for b in re.findall(r"\*\*(.+?)\*\*", content)]
    if bolds:
        return bolds[:limit]

    lines = [
        line.strip("- ").strip()
        for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    return [line[:80] for line in lines[:limit]]


def detect_corpus(skill_dir: Path) -> tuple[int, int]:
    files = list((skill_dir / "references" / "research").glob("*.md"))
    combined = "\n".join(read_text(path) for path in files if path.exists())
    distill = len(re.findall(r"\b(distill|蒸馏)\b", combined, flags=re.IGNORECASE))
    holdout = len(re.findall(r"\b(holdout|留出|回测)\b", combined, flags=re.IGNORECASE))
    return distill, holdout


def count_files(path: Path, suffix: str = "*") -> int:
    if not path.exists():
        return 0
    return len([item for item in path.glob(suffix) if item.is_file()])


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python merge_paper_analysis.py <generated-skill-dir>", file=sys.stderr)
        return 2

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / "references" / "research"
    paper_cards_dir = skill_dir / "references" / "paper-cards"
    texts_dir = skill_dir / "sources" / "texts"
    papers_dir = skill_dir / "sources" / "papers"
    validation_dir = skill_dir / "references" / "validation"
    if not research_dir.exists():
        print(f"Missing research directory: {research_dir}", file=sys.stderr)
        return 1

    rows: list[tuple[str, str, str, str]] = []
    missing: list[str] = []
    low_confidence_total = 0
    paper_total = 0

    for key, label in DIMENSIONS.items():
        path = research_dir / f"{key}.md"
        if not path.exists():
            missing.append(label)
            rows.append((label, "missing", "-", "-"))
            continue

        content = read_text(path)
        paper_count = count_paper_mentions(content)
        confidence = count_confidence(content)
        low_confidence_total += confidence["low"]
        paper_total += paper_count
        findings = "; ".join(extract_findings(content)) or "-"
        if len(findings) > 90:
            findings = findings[:87] + "..."
        conf_summary = f"H{confidence['high']}/M{confidence['medium']}/L{confidence['low']}"
        rows.append((label, str(paper_count), conf_summary, findings))

    distill_count, holdout_count = detect_corpus(skill_dir)
    paper_card_count = count_files(paper_cards_dir, "*.md")
    text_count = count_files(texts_dir, "*")
    paper_source_count = count_files(papers_dir, "*")
    has_revision_log = (validation_dir / "revision-log.md").exists()

    print("| Dimension | Paper signals | Confidence tags | Key findings |")
    print("| --- | ---: | --- | --- |")
    for row in rows:
        print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")

    print()
    print(f"- Total paper signals: {paper_total}")
    print(f"- Distillation role tags: {distill_count}")
    print(f"- Holdout role tags: {holdout_count}")
    print(f"- Paper cards: {paper_card_count}")
    print(f"- Source papers: {paper_source_count}")
    print(f"- Extracted texts: {text_count}")
    print(f"- Revision log: {'present' if has_revision_log else 'missing'}")
    print(f"- Missing dimensions: {', '.join(missing) if missing else 'none'}")
    print(f"- Low-confidence tags: {low_confidence_total}")

    if missing:
        print("\nAction: fill missing dimensions or mark them in Honest Boundaries.")
    if holdout_count == 0:
        print("Action: add at least one holdout paper or explain why validation cannot use holdout backtesting.")
    if paper_card_count == 0:
        print("Action: add paper cards under references/paper-cards/.")
    if text_count == 0:
        print("Action: add extracted paper text under sources/texts/ or explain why extraction failed.")
    if not has_revision_log:
        print("Action: add references/validation/revision-log.md.")
    if paper_total < 12:
        print("Action: corpus may be thin; consider adding papers or narrowing the research line.")

    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
