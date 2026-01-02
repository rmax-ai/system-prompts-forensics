# System Prompt Forensics

A human-friendly guide to the project.

## What this is

We treat captured “system prompts” as governance documents. Rather than viewing prompts as task instructions, we study them as constitutions that define what an AI agent is, what it can do, what it must not do, and how it stops. The goal is to reverse‑engineer these constitutions across developer tools (IDE assistants, CLIs, agent frameworks) and surface reproducible design patterns for safer, more predictable agent systems.

## What we produce

- A small set of composable prompt primitives (identity, authority, scope, tools, feedback, termination).
- A taxonomy of prompt architectures and their risk models.
- Line-by-line, normalized analyses of captured system prompts (YAML).
- Comprehensive research reports and comparative analyses across major AI assistants.
- A canonical agent constitution prompt designed by construction (not prose).
- Templates and scripts to normalize, analyze, and compare prompts.

## Why it matters

System prompts encode a tool’s implicit assumptions about agency, risk, and control. Making those assumptions explicit lets teams design agent-first systems with clear governance and predictable behavior—moving governance out of hidden strings and into auditable infrastructure.

## Quick overview of the repository

- data/raw/ — raw HTTP captures (sensitive; MUST be redacted before sharing)
- data/payload/ — parsed JSON payloads derived from captures
- data/analysis/ — normalized YAML analyses (schema v0)
- data/prompts/ — normalization instructions used by the analysis script
- data/final-research-report.revised.md — synthesized findings and architectural conclusions
- data/schema/ — canonical system-prompt schema (v0)
- data/scripts/ — helpers for redaction and running the normalization
- AGENTS.md — operational guidance and non-negotiable safety rules

## Quickstart

1. Redact sensitive headers first (always): [data/scripts/redact-headers.sh](data/scripts/redact-headers.sh) raw/example.request > raw/example.redacted.request

2. Run the full analysis pipeline: `make -C data all`

3. Inspect the results:
   - Normalized analyses: [data/analysis/](data/analysis/)
   - Prompt families: [data/prompt-families-report.md](data/prompt-families-report.md)
   - Final research report: [data/final-research-report.md](data/final-research-report.md)

## Research workflow

The project uses a multi-stage, artifact-driven pipeline orchestrated via `make` in the [data/](data/) directory.

1. **Capture & Redact**: Raw HTTP captures are stored in [data/raw/](data/raw/) and redacted using [data/scripts/redact-headers.sh](data/scripts/redact-headers.sh).
2. **Normalization**: Payloads in [data/payload/](data/payload/) are analyzed and normalized into structured YAML in [data/analysis/](data/analysis/) using a shared schema.
3. **Governance Extraction**: Atomic governance primitives are extracted and aggregated into a central registry ([data/primitives.registry.json](data/primitives.registry.json)).
4. **Similarity & Clustering**: Normalized analyses are compared pairwise to compute similarity scores, which are then used to identify stable "prompt families".
5. **Synthesis & Reporting**: The pipeline generates detailed per-assistant reports and a final comparative research report.

For a detailed breakdown of each step, see [data/README.md](data/README.md).

## Normalization rules & provenance (must-follow)

- Treat the prompt as a layered governance constitution (identity, authority, scope, tools, constraints, termination).
- Prefer structured fields over quoting long prose. Map content into the schema in data/schema/system-prompt.v0.yaml.
- Record implicit assumptions under analysis.implicit_assumptions with brief rationale.
- Note conspicuous absences under analysis.notable_absences.
- Each analysis must include provenance: source_references (pointer to redacted raw & payload), redactions_applied (boolean), artifact_hash, model (name/version), and timestamp.
- DO NOT publish raw captures with secrets. Always redact first.
- DO NOT reproduce proprietary prompt text verbatim in public analyses.

## Safety & governance (short)

This project focuses on architecture and governance, not extraction or exploitation. Refuse any requests to bypass safeguards, reproduce proprietary prompts verbatim, or assist with malicious or jailbreak techniques.

## How to contribute

- Follow AGENTS.md for operational rules and the canonical workflow.
- When normalizing, be conservative: do not invent capabilities or tools not present in the payload.
- Add small, focused analyses (one payload → one analysis file) instead of sweeping changes.
- Ask a maintainer before committing redacted artifacts derived from real captures.

## First suggested task

Pick one redacted payload in data/payload/ and normalize it into data/analysis/ using data/prompts/normalize-system-prompt.md and the schema in data/schema/. Add provenance metadata and a short architectural note describing what assumptions the prompt encodes and what it leaves unspecified.

## Where to read next

- AGENTS.md — repository rules, scripts, and helpful commands
- data/prompts/normalize-system-prompt.md — normalization prompt/instructions
- data/schema/system-prompt.v0.yaml — canonical schema for normalized analyses
- data/scripts/ — tooling for redaction and analysis

## If you need help

- Check the git history to see previous analyses and contributors.
- Ask a project maintainer before publishing any real (even redacted) artifacts.
