System Prompt Forensics

A human-friendly guide to the project.

What this is

We treat captured “system prompts” as governance documents. Rather than viewing prompts as task instructions, we study them as constitutions that define what an AI agent is, what it can do, what it must not do, and how it stops. The goal is to reverse‑engineer these constitutions across developer tools (IDE assistants, CLIs, agent frameworks) and surface reproducible design patterns for safer, more predictable agent systems.

What we produce

- A small set of composable prompt primitives (identity, authority, scope, tools, feedback, termination).
- A taxonomy of prompt architectures and their risk models.
- Line-by-line, normalized analyses of captured system prompts (YAML).
- Comprehensive research reports and comparative analyses across major AI assistants.
- A canonical agent constitution prompt designed by construction (not prose).
- Templates and scripts to normalize, analyze, and compare prompts.

Why it matters

System prompts encode a tool’s implicit assumptions about agency, risk, and control. Making those assumptions explicit lets teams design agent-first systems with clear governance and predictable behavior—moving governance out of hidden strings and into auditable infrastructure.

Quick overview of the repository

- data/raw/ — raw HTTP captures (sensitive; MUST be redacted before sharing)
- data/payload/ — parsed JSON payloads derived from captures
- data/analysis/ — normalized YAML analyses (schema v0)
- data/prompts/ — normalization instructions used by the analysis script
- data/final-research-report.revised.md — synthesized findings and architectural conclusions
- data/schema/ — canonical system-prompt schema (v0)
- data/scripts/ — helpers for redaction and running the normalization
- AGENTS.md — operational guidance and non-negotiable safety rules

Quickstart

1. Redact sensitive headers first (always): data/scripts/redact-headers.sh raw/example.request > raw/example.redacted.request

2. Convert redacted captures into payload JSON: make -C data all

3. Validate payload JSON: jq . data/payload/<artifact>.json

4. Run normalization analysis (example): python data/scripts/system-prompt-analysis.py \
   --prompt data/prompts/normalize-system-prompt.md \
   --schema data/schema/system-prompt.v0.yaml \
   --invocation data/payload/<artifact>.json \
   --model gpt-5.2 (Use deterministic model settings where possible — e.g. temperature=0.)

5. Inspect and validate normalized YAML: yq eval . data/analysis/<artifact>.yaml

Research workflow (recommended)

1. Capture (proxy, CLI debug, logs, public docs)
2. Redact (data/scripts/redact-headers.sh)
3. Convert (make -C data)
4. Normalize (system-prompt-analysis.py + normalize-system-prompt.md)
5. Validate (parse YAML, confirm provenance fields)
6. Store (data/analysis/ with redaction metadata)
7. Compare (pairwise diffs between normalized analyses)

Normalization rules & provenance (must-follow)

- Treat the prompt as a layered governance constitution (identity, authority, scope, tools, constraints, termination).
- Prefer structured fields over quoting long prose. Map content into the schema in data/schema/system-prompt.v0.yaml.
- Record implicit assumptions under analysis.implicit_assumptions with brief rationale.
- Note conspicuous absences under analysis.notable_absences.
- Each analysis must include provenance: source_references (pointer to redacted raw & payload), redactions_applied (boolean), artifact_hash, model (name/version), and timestamp.
- DO NOT publish raw captures with secrets. Always redact first.
- DO NOT reproduce proprietary prompt text verbatim in public analyses.

Safety & governance (short)

This project focuses on architecture and governance, not extraction or exploitation. Refuse any requests to bypass safeguards, reproduce proprietary prompts verbatim, or assist with malicious or jailbreak techniques.

How to contribute

- Follow AGENTS.md for operational rules and the canonical workflow.
- When normalizing, be conservative: do not invent capabilities or tools not present in the payload.
- Add small, focused analyses (one payload → one analysis file) instead of sweeping changes.
- Ask a maintainer before committing redacted artifacts derived from real captures.

First suggested task

Pick one redacted payload in data/payload/ and normalize it into data/analysis/ using data/prompts/normalize-system-prompt.md and the schema in data/schema/. Add provenance metadata and a short architectural note describing what assumptions the prompt encodes and what it leaves unspecified.

Where to read next

- AGENTS.md — repository rules, scripts, and helpful commands
- data/prompts/normalize-system-prompt.md — normalization prompt/instructions
- data/schema/system-prompt.v0.yaml — canonical schema for normalized analyses
- data/scripts/ — tooling for redaction and analysis

If you need help

- Check the git history to see previous analyses and contributors.
- Ask a project maintainer before publishing any real (even redacted) artifacts.
