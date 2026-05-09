---
name: lab-paradigm-distiller
description: |
  Distill a concrete research line from a lab or group into a reusable ChatGPT/Codex research-paradigm skill. Use when Codex is given seed papers, local PDFs, text files, DOI/arXiv/OpenReview/official project links, or a folder of papers and asked to extract how a lab chooses problems, builds methods, validates evidence, frames papers, or generates new research proposals in that group's style. Trigger for requests such as "蒸馏课题组", "科研范式", "课题组范式skill", "lab paradigm", "paper lineage", "research proposal like this group", "study this lab's way of doing research", or "distill this research line".
---

# Lab Paradigm Distiller

You are Codex acting as a research-paradigm distillation engineer and scientific research analyst. Use this skill to distill how a concrete research line does science, not just what its papers concluded.

The output is a self-contained skill folder for one narrow lab/group research line. The generated skill should work as a research advisor that can read new papers, design experiments, frame papers, and generate small proposals in that group's paradigm.

## Required Inputs

Accept any of:

- Seed paper(s)
- Local PDFs or folders of PDFs
- Extracted text files
- DOI, arXiv, OpenReview, Semantic Scholar, publisher, project, code, or official lab links
- A target research line, if the user provides one

If the target line is ambiguous, infer the narrowest plausible research line from the seed paper and state the boundary explicitly. Do not default to the whole lab unless the corpus truly supports it.

## Required Resources

Before building a generated skill, read and follow:

- `SKILL.md`
- `references/extraction-framework.md`
- `references/lab-skill-template.md`
- `scripts/merge_paper_analysis.py`
- `scripts/quality_check.py`

## Core Objective

Generate a self-contained folder:

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

Every source, note, and validation artifact must live inside this folder so the generated skill can be copied or installed independently.

## Source Policy

- Highest weight: user-provided papers, official full texts, appendices, supplementary material, datasets, and code.
- High weight: official project pages, lab pages, talks, slides, and author-maintained repositories.
- Medium weight: conference videos or slides by authors when they clarify methods or motivation.
- Exclude: social-media chatter, comments, ranking posts, blog summaries, Zhihu, WeChat essays, and unverifiable secondhand takes.

## Workflow

### Phase 0: Scope the Target

State:

- Seed paper(s)
- Inferred lab/group and key authors
- Narrow research-line boundary
- What is out of scope
- Source policy and whether web expansion is allowed

If only one seed paper is available, use it to infer the likely line, then expand cautiously. If fewer than four usable papers exist, continue only with strong honest boundaries.

### Phase 1: Build the Corpus

Start from the seed paper and expand to the same research line.

Default split:

- Distillation set: 5-10 papers
- Holdout set: 1-2 same-line or adjacent-frontier papers withheld for validation

For each paper:

- Copy or preserve the PDF/source under `sources/papers/` when available.
- Extract or save readable text under `sources/texts/`.
- Record metadata in `references/corpus-metadata.json`.
- Write one paper card in `references/paper-cards/[year-or-id]-[short-title].md`.

Each paper card must include:

- Bibliographic metadata and source path/URL
- Role: `seed`, `distill`, or `holdout`
- Why it belongs to the research line
- Problem, core hypothesis, method, evidence, contribution, limitations
- Platform/material/system and measurement/simulation stack
- Reusable claims and quotes, with confidence labels
- What it suggests about the lab's paradigm

### Phase 2: Six-Dimension Extraction

Write one research file for each dimension. Use `references/extraction-framework.md` for detailed standards.

| File | Extract |
| --- | --- |
| `01-problem-selection.md` | Repeated problem types, what makes a question worth asking, problem avoidance patterns |
| `02-core-assumptions.md` | Scientific beliefs, modeling assumptions, what variables the group treats as causal or central |
| `03-method-stack.md` | Preferred models, algorithms, datasets, tools, ablations, theoretical moves, code artifacts |
| `04-evidence-standard.md` | Metrics, baselines, controls, user studies, proofs, failure analyses, acceptance thresholds |
| `05-paper-framing.md` | Introduction pattern, contribution claims, naming style, figure/table grammar, limitation style |
| `06-evolution-timeline.md` | Chronology, pivots, scaling of ambition, method migrations, recent direction |

Hard requirements:

- Separate paper fact, author claim, and your inference.
- Preserve contradictions instead of smoothing them over.
- Mark confidence as high, medium, or low.
- Quote sparingly; prefer paraphrase plus precise citation.
- Ground every major synthesis in paper cards or source files.

After extraction, run:

```bash
python scripts/merge_paper_analysis.py <generated-skill-dir>
```

Use the summary to decide whether to add papers, narrow the research line, or continue.

### Phase 3: Synthesize the Paradigm

Read paper cards and all six research files. Extract:

- 3-6 paradigm lenses that pass the lab-paradigm triple test
- 5-10 research heuristics for choosing problems, methods, and evidence
- Method grammar: common pipeline shapes, defaults, and preferred artifacts
- Evidence grammar: what the group tends to count as convincing
- Writing DNA: how the group frames stakes, novelty, results, and limitations
- Anti-patterns: projects this group likely would not do
- Honest boundaries: missing data, mixed lines, low-confidence dimensions, and time cutoff

Use `references/lab-skill-template.md` to assemble `SKILL.md`.

### Phase 4: Validate

Before delivery, create:

- `references/validation/holdout-backtest.md`: withhold 1-2 papers and check whether the skill predicts their problem type, method grammar, and evidence standard.
- `references/validation/new-proposal-test.md`: generate 3 small proposals using the required proposal format.
- `references/validation/revision-log.md`: record major revisions, failed checks, boundary decisions, and why the final version is acceptable.

Then run:

```bash
python scripts/quality_check.py <generated-skill-dir>/SKILL.md
```

If validation fails, revise once and update `revision-log.md`. If it still fails, keep the skill only if the honest-boundary section explains the weakness instead of overfitting.

## Required Proposal Format

When asked to generate new topics, output compact proposals with exactly these fields:

- Problem
- Core hypothesis
- Method
- Experiment
- Expected contribution
- Failure risk
- Why this fits the lab paradigm

## Delivery Standard

Deliver:

- The generated skill folder path
- A short boundary statement for the distilled research line
- Corpus split summary
- Validation summary
- Any low-confidence dimensions or missing source types

Do not present the output as representing the entire lab unless the corpus supports that claim.
