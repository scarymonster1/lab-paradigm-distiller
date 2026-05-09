# Lab Paradigm Distiller

`lab-paradigm-distiller` is a Codex/ChatGPT skill for distilling a concrete research line from a lab or group into a reusable research-paradigm skill.

It is designed to extract **how a research line does science**, not merely summarize what its papers concluded.

Given seed papers, local PDFs, paper links, DOI/arXiv/OpenReview links, project pages, code repositories, or official lab materials, the skill builds a reusable advisor that can help with:

- choosing new research problems in the target line
- designing methods and experiments
- checking evidence standards
- framing papers and contributions
- generating small research proposals in the distilled paradigm

## What It Produces

The skill generates a self-contained folder for one narrow lab/group research line:

```text
[lab-line]-research-paradigm/
├── SKILL.md
├── sources/
│   ├── papers/
│   └── texts/
├── references/
│   ├── corpus-metadata.json
│   ├── paper-cards/
│   ├── research/
│   │   ├── 01-problem-selection.md
│   │   ├── 02-core-assumptions.md
│   │   ├── 03-method-stack.md
│   │   ├── 04-evidence-standard.md
│   │   ├── 05-paper-framing.md
│   │   └── 06-evolution-timeline.md
│   └── validation/
│       ├── holdout-backtest.md
│       ├── new-proposal-test.md
│       └── revision-log.md
```

The generated `SKILL.md` is the final reusable skill. The surrounding `references/` files preserve the evidence trail, extraction notes, validation results, and revision history.

## Installation

Clone this repository:

```bash
git clone https://github.com/scarymonster1/lab-paradigm-distiller.git
```

Then copy the folder into your Codex skills directory.

On Windows:

```powershell
Copy-Item -Recurse -Force ".\lab-paradigm-distiller" "$env:USERPROFILE\.codex\skills\lab-paradigm-distiller"
```

On macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./lab-paradigm-distiller ~/.codex/skills/lab-paradigm-distiller
```

After installation, start a new Codex/ChatGPT session and ask it to use the `lab-paradigm-distiller` skill.

## Example Use

You can give the skill a folder of papers:

```text
Use lab-paradigm-distiller.

Input folder:
D:\research\papers\my-lab-line

Target research line:
topological acoustic/elastic wave devices based on integrated phononic platforms

Please distill this into a reusable research-paradigm skill.
```

Or start from one seed paper:

```text
Use lab-paradigm-distiller.

Seed paper:
https://arxiv.org/abs/xxxx.xxxxx

Infer the narrowest plausible research line, expand the corpus with official sources, and generate a research-paradigm skill.
```

The skill will define the research-line boundary, build a corpus, create paper cards, extract the paradigm across six dimensions, synthesize a generated skill, and validate it with holdout and proposal tests.

## Distillation Framework

The extraction is organized around six dimensions:

| Dimension | What It Extracts |
| --- | --- |
| Problem selection | What questions the group repeatedly chooses, and what it avoids |
| Core assumptions | The group's scientific beliefs, modeling defaults, and causal variables |
| Method stack | Preferred theories, platforms, algorithms, tools, simulations, measurements, and artifacts |
| Evidence standard | What counts as convincing evidence, including baselines, controls, metrics, and failure analysis |
| Paper framing | How the group motivates, names, figures, claims, and limits its work |
| Evolution timeline | How the research line changes over time, including pivots and frontier shifts |

The goal is to identify the lab's **research grammar**: the recurring pattern that connects problem choice, method design, validation, and writing.

## Source Policy

Highest-priority sources:

- user-provided papers
- official full texts, appendices, and supplementary materials
- datasets and code released by the authors
- official project pages and lab pages
- author-maintained repositories, talks, and slides

Excluded sources:

- social-media chatter
- comment sections
- ranking posts
- unverifiable blog summaries
- Zhihu, WeChat essays, and similar secondhand commentary

The skill should ground claims in papers and official materials. It should mark low-confidence inferences clearly instead of pretending the corpus is stronger than it is.

## Validation

A generated lab-line skill should pass three checks:

1. **Cross-paper recurrence**: the extracted pattern appears across multiple papers, not just one example.
2. **Generative power**: the skill can generate plausible new proposals in the target research line.
3. **Field-level distinction**: the output sounds like this lab/group line, not just a generic field survey.

The workflow creates:

- `holdout-backtest.md`: withholds one or two papers and checks whether the skill predicts their problem, method, and evidence logic.
- `new-proposal-test.md`: generates three compact new proposals.
- `revision-log.md`: records failed checks, boundary decisions, and final caveats.

## Helper Scripts

Merge paper-card analysis:

```bash
python scripts/merge_paper_analysis.py <generated-skill-dir>
```

Run quality checks on a generated skill:

```bash
python scripts/quality_check.py <generated-skill-dir>/SKILL.md
```

The scripts are intentionally lightweight. PDF parsing, citation collection, and web expansion are handled by the active Codex/ChatGPT environment and available tools.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── examples/
│   └── template-lab-line-paradigm/
├── references/
│   ├── extraction-framework.md
│   └── lab-skill-template.md
└── scripts/
    ├── merge_paper_analysis.py
    └── quality_check.py
```

`examples/template-lab-line-paradigm/` is a placeholder structure for generated skills. It does not contain a real lab corpus.

## Privacy And Copyright Notes

Generated research-line skills may contain private notes, copyrighted PDFs, or unpublished research material. Do not publish generated `sources/` folders unless you have the right to share those files.

This repository is meant to publish the **generic distillation workflow**, not any private lab corpus.

## Status

This is an early working skill. It is strongest when the user provides a focused research line and at least 5-10 representative papers, plus 1-2 holdout papers for validation.
