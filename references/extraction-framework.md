# Lab Paradigm Extraction Framework

Use this framework when converting a paper lineage into a reusable research-paradigm skill.

## 1. Unit of Analysis

The target is a research line inside a lab, not a person and not an entire field. A valid line has:

- A seed paper or representative work
- At least several related papers with overlapping authors, assumptions, problems, or method grammar
- A recognizable continuity in questions, tools, or evidence standards

If the papers span unrelated directions, split the corpus or mark the result as low confidence.

## 2. Lab-Paradigm Triple Test

A candidate pattern becomes a "paradigm lens" only if it passes all three tests.

### Test 1: Cross-Paper Recurrence

The pattern appears across at least 3 distillation papers, or appears in 1 seminal paper plus later extensions or variants.

Examples:

- Repeatedly turning messy real-world interaction into benchmarkable tasks
- Repeatedly replacing hand-coded rules with learned latent structure
- Repeatedly validating claims through ablation plus controlled deployment study

### Test 2: Generative Power

The pattern can help generate or evaluate a new project:

- It predicts which problem the group would find interesting
- It suggests the likely method family
- It implies the necessary baselines, metrics, or ablations
- It shapes the introduction or contribution claim

If a pattern only summarizes past results and cannot guide a new project, demote it to an observation.

### Test 3: Relative Distinctiveness

The pattern is more specific than generic good research. Ask:

- Would most competent labs in this field do the same thing?
- Is this a field norm, or does this group emphasize it unusually strongly?
- Does the pattern distinguish this line from nearby labs or methods?

If it is true but generic, demote it to background context.

## 3. Extraction Dimensions

### 3.1 Problem Selection

Extract:

- The recurring problem template
- What counts as a meaningful gap
- The preferred level of abstraction
- Problem constraints the group tends to accept or reject
- Problem types that are adjacent but usually avoided

Paper-level notes should include: problem statement, motivation, gap framing, and why the paper belongs to the line.

### 3.2 Core Assumptions

Extract:

- Scientific or engineering beliefs that recur
- What the group treats as causal, central, measurable, or scalable
- Where the group places complexity: data, model, interaction, environment, objective, or evaluation
- Assumptions that later papers revise

Separate author claims from your inference.

### 3.3 Method Stack

Extract:

- Model families, algorithms, representations, datasets, simulators, hardware, code artifacts
- Common pipeline shape
- Preferred baselines and ablation dimensions
- What is reused, extended, or discarded across papers

Do not list every technical detail. Capture the method grammar.

### 3.4 Evidence Standard

Extract:

- Metrics and thresholds
- Baselines and controls
- Ablation style
- Human studies, field deployment, proofs, qualitative analysis, or failure analysis
- What would make the group believe a result is real

Note evidence gaps and recurring weak spots.

### 3.5 Paper Framing

Extract:

- Intro narrative pattern
- How the paper names the problem and method
- Contribution claim style
- Figure/table grammar
- Related-work positioning
- Limitation and future-work style

This is not roleplay voice. It is paper-writing DNA.

### 3.6 Evolution Timeline

Extract:

- Key papers and pivots
- What became more ambitious, automated, scaled, theoretical, empirical, or applied
- New datasets, tools, benchmarks, or artifacts introduced by the line
- Recent direction and unresolved frontier

## 4. Confidence Rules

Use confidence labels:

- High: supported by multiple papers and explicit author claims
- Medium: supported by multiple papers but mostly inferred
- Low: supported by few papers, mixed evidence, or an ambiguous line boundary

When information is missing, write the limitation directly. Do not fill gaps with field-general assumptions.

## 5. Output Artifacts

The generated skill should contain:

- Corpus table with distillation and holdout split
- 3-6 paradigm lenses
- 5-10 research heuristics
- Method and evidence grammar
- Writing DNA
- Proposal generator format
- Anti-patterns
- Honest boundaries
- Source list and validation summary

## 6. Quality Checklist

Before delivery, verify:

- Each paradigm lens cites evidence from at least 2 papers, preferably 3+
- Each lens has an application and a failure mode
- Heuristics are actionable for new research, not just descriptive
- The holdout backtest is present or the lack of holdout is explained
- The proposal format includes all required fields
- The skill does not claim to represent the entire lab unless the corpus supports that
- The skill avoids comments, social chatter, and unverifiable secondhand analysis
