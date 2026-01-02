# System Prompt Forensics — Data Workflow

This directory documents the **data-generation and analysis workflow** used to extract, normalize, compare, cluster, and interpret system prompts from AI tools.

The pipeline treats system prompts as **governance constitutions** and produces auditable artifacts at each stage, from raw payloads to a final comparative report.

---

## Overview of the Pipeline

The workflow is a **multi-stage, artifact-driven pipeline** orchestrated via `make`:

```
payload/*.json
├── analysis/*.analysis.yaml
│   ├── similarities.csv
│   │   └── band-report.csv
│   │       └── prompt-families.csv
│   │           └── prompt-families-report.md
│   │               └── final-comparative-report.md
│   └── assistant-reports (final-report-*.md)
│       └── final-research-report.md
│           └── appendix-governance-primitives.md
└── governance/*.json
    └── primitives.registry.json
```

Each step has:

- a single responsibility
- a well-defined input/output contract
- a stable, versionable artifact

No step mutates earlier outputs.

---

## Step 0 — Raw Payload Collection (`payload/`)

**Input:**

- `payload/*.json`

These files are **captured invocation payloads** from tools such as:

- VS Code Copilot
- Codex CLI
- OpenCode CLI

They typically include:

- system instructions
- developer instructions
- tool declarations
- runtime metadata

**Important properties:**

- Treated as immutable evidence
- Never edited manually
- Represent the closest observable approximation of a tool’s real system prompt

---

## Step 1 — Normalization (`analysis/*.analysis.yaml`)

**Make target:**

```make
analysis/%.analysis.yaml: payload/%.json
```

**Script:**

- `scripts/system-prompt-analysis.py`

**Purpose:** Convert opaque system prompts into a **normalized, structured representation** using a shared schema (`schema/system-prompt.v0.yaml`).

**What happens:**

- The model is given:

  - a normalization prompt
  - the schema
  - the raw invocation payload

- It outputs a YAML document describing:

  - identity
  - authority
  - scope
  - tools
  - constraints
  - correction loops
  - termination conditions
  - risk model

**Output:**

- One `.analysis.yaml` file per payload
- All files conform to the same structural schema

**Why this matters:** This step removes stylistic and textual noise and makes prompts **comparable as governance systems**, not prose.

---

## Step 1b — Governance Extraction (`governance/*.json`)

**Make target:**

```make
governance/%.json: payload/%.json
```

**Script:**

- `scripts/governance-primitive-extract.py`

**Purpose:** Extract atomic governance primitives (rules, permissions, prohibitions) from raw payloads.

**Output:**

- One `.json` file per payload containing a list of extracted primitives.

---

## Step 1c — Primitives Registry (`primitives.registry.json`)

**Make target:**

```make
primitives.registry.json: $(GOVERNANCE)
```

**Script:**

- `scripts/governance-primitives-reduce.py`

**Purpose:** De-duplicate and normalize primitives across all tools into a canonical registry.

**Output:**

- `primitives.registry.json` — a unified catalog of governance primitives found across the corpus.

---

## Step 2 — Pairwise Similarity (`similarities.csv`)

**Make target:**

```make
similarities.csv: analysis/*.analysis.yaml
```

**Script:**

- `scripts/prompt-similarity.py`

**Purpose:** Quantify how similar each pair of normalized prompts is.

**Metrics computed:**

- `struct_similarity` — schema-level structural overlap
- `token_similarity` — textual similarity of key fields
- `forbidden_similarity` — overlap in prohibitions / “must not” rules
- `weighted_score` — composite similarity score

**Output:**

- `similarities.csv`
- One row per unordered pair of prompts

**Why this matters:** This provides a **measurement layer** that is explicit, reproducible, and auditable, rather than relying on intuitive or model-only judgments.

---

## Step 3 — Band Analysis (`band-report.csv`)

**Make target:**

```make
band-report.csv: similarities.csv
```

**Script:**

- `scripts/band-report-from-csv.py`

**Purpose:** Analyze similarity **across thresholds** to identify stable regimes (“bands”).

**What happens:**

- The similarity graph is thresholded repeatedly (e.g. 0.74 → 0.51)
- For each threshold:

  - connected components are computed
  - component sizes are recorded

**Output:**

- `band-report.csv`
- Columns include:

  - threshold
  - number of components
  - largest component size
  - component size distribution

**Why this matters:** This step reveals **scale**:

- high thresholds → near-duplicates
- mid thresholds → operational families
- low thresholds → product lineage
- very low thresholds → structural collapse (noise)

It replaces arbitrary clustering thresholds with **empirical stability analysis**.

---

## Step 4 — Prompt Family Extraction (`prompt-families.csv`)

**Make target:**

```make
prompt-families.csv: similarities.csv band-report.csv
```

**Script:**

- `scripts/prompt-family-analysis.py`

**Purpose:** Convert similarity data + band stability into **discrete prompt families**.

**What happens:**

- Stable bands are identified from `band-report.csv`
- A representative threshold is chosen per band
- Connected components at that threshold become **prompt families**

**Each family includes:**

- band range
- chosen threshold
- family size
- average internal similarity
- member prompts
- confidence level

**Output:**

- `prompt-families.csv`
- One row per prompt family

**Why this matters:** This step compresses many prompts into a small set of **governance regimes** that can be meaningfully compared and discussed.

---

## Step 5 — Human Interpretation (`prompt-families-report.md`)

**Make target:**

```make
prompt-families-report.md: prompt-families.csv
```

**Script:**

- `scripts/prompt-families-interpretation.py`

**Purpose:** Produce a **human-readable interpretation report** explaining what the prompt families mean and how they relate.

**What happens:**

- The model is given:

  - a strict interpretation prompt
  - `prompt-families.csv`

- It outputs a structured report covering:

  - family descriptions
  - governance characteristics
  - cross-family relationships
  - implications and limitations

**Output:**

- `prompt-families-report.md`

**Why this matters:** This is the **only narrative step** in the pipeline. All prior steps are structural and quantitative.

---

## Step 5b — Assistant Reports (`final-report-*.md`)

**Make target:**

```make
assistant-reports: $(ANALYSIS)
```

**Script:**

- `scripts/final-assistant-analysis.py`

**Purpose:** Generate detailed, per-assistant governance reports by synthesizing all normalized analyses for a specific tool (e.g., all `vscode-copilot` variants).

**Output:**

- `final-report-<assistant>.md` for each unique assistant identified in the corpus.

---

## Step 6 — Final Comparative Analysis (`final-comparative-report.md`)

**Make target:**

```make
final-comparative-report.md: prompt-families-report.md ../methodology.md ../goal.md
```

**Script:**

- `scripts/final-comparative-analysis.py`

**Purpose:** Synthesize all findings into a **comprehensive comparative report** focusing on cross-tool patterns and family relationships.

**What happens:**

- The model is given:

  - the final comparative analysis prompt
  - all normalized analyses
  - similarity data
  - band reports
  - prompt families
  - the human-readable interpretation report
  - project methodology and goals

- It outputs a final report that:

  - synthesizes the entire research effort
  - maps findings back to the original goals
  - provides a high-level executive summary

**Output:**

- `final-comparative-report.md`

**Why this matters:** This step provides the **structural synthesis**, connecting the low-level forensic data to the high-level research objectives.

---

## Step 7 — Final Research Report (`final-research-report.md`)

**Make target:**

```make
final-research-report.md: assistant-reports ../goal.md
```

**Script:**

- `scripts/final-research-report.py`

**Purpose:** Produce the **ultimate research artifact** by synthesizing the per-assistant reports into a final narrative.

**Output:**

- `final-research-report.md`

**Why this matters:** This is the final deliverable, providing a cohesive narrative across all assistants and research goals.

---

## Step 8 — Governance Primitives Appendix (`appendix-governance-primitives.md`)

**Make target:**

```make
appendix-governance-primitives.md: final-research-report.md primitives.registry.json
```

**Script:**

- `scripts/governance-primitives-appendix.py`

**Purpose:** Generate a detailed appendix of all prompt governance primitives, cross-referenced with the final research report.

**Output:**

- `appendix-governance-primitives.md`

**Why this matters:** It provides a technical deep-dive into the specific governance mechanisms identified, serving as a reference for the findings in the main report.

---

## Reproducibility and Control

Key controls in the Makefile:

- `ANALYSIS_MODEL`

  - Default: `gpt-5.2`
  - Can be overridden for testing

- `DRY_RUN`

  - When `true`, normalization does not call the API
  - Useful for debugging and inspection

- Deterministic settings

  - Model calls use `temperature=0` for record-producing scripts and `temperature=0.1` for structured analysis/interpretation scripts.
  - All intermediate artifacts are persisted

---

## What This Workflow Enables

- Comparative analysis across tools and vendors
- Detection of governance convergence/divergence
- Stable prompt family definitions
- Longitudinal tracking of prompt evolution
- Audit-friendly research artifacts

This workflow is intentionally **not** designed for:

- performance evaluation
- output quality ranking
- model benchmarking

It is a **governance-forensics pipeline**.

---

## Cleaning the Workspace

To remove all generated artifacts:

```bash
make clean
```

This deletes:

- `analysis/*.analysis.yaml`
- `governance/*.json`
- `primitives.registry.json`
- `similarities.csv`
- `band-report.csv`
- `prompt-families.csv`
- `prompt-families-report.md`
- `final-comparative-report.md`
- `final-research-report.md`
- `final-report-*.md`

Raw payloads are preserved.

---

## Summary

This directory implements a **closed-loop, evidence-based workflow** for understanding system prompts as constitutions.

Each artifact builds on the previous one, and no step depends on hidden state or manual intervention.

The result is a reproducible foundation for comparative prompt governance research.
