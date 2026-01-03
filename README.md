![Header](images/header.png)

# System Prompt Forensics

System prompts in AI-assisted developer tools are more than just task instructions; they function as implicit "constitutions" that define an agent's identity, authority, and safety boundaries. This repository provides a forensic framework for treating these prompts as governance artifacts, offering a methodology to normalize, analyze, and compare them across major assistants like GitHub Copilot and Codex. By decomposing complex prompts into modular **Prompt Governance Primitives (PGPs)**, we surface the architectural trade-offs and control mechanisms that shape modern agentic systems, moving governance from hidden strings into auditable infrastructure.

## What we analyzed

We performed a structural analysis of system prompts from leading AI developer tools, including **GitHub Copilot (CLI and VS Code)**, **Codex (Execution and Review modes)**, and **OpenCode**. Our method involves capturing raw HTTP payloads, redacting sensitive data, and normalizing the prompts into a canonical YAML schema. This allows for line-by-line comparison of how different tools handle authority boundaries, workspace visibility, tool mediation, and termination logic.

## What’s new

This project introduces the concept of **System Prompts as Governance Artifacts**, shifting the focus from prompt engineering to prompt governance. We identify and catalog **Prompt Governance Primitives (PGPs)**—recurring, modular control structures (e.g., "Approval-gated execution", "Stop-on-unexpected-change") that can be reused to design safer agents. This architectural approach treats the prompt as a layered contract between the user, the policy, and the model.

## How to navigate the repo

- **[Research Report](data/final-research-report.revised.md)**: The primary synthesis of our findings, architectural conclusions, and comparative analysis.
- **[PGP Appendix](data/appendix-governance-primitives.revised.md)**: A detailed registry of Prompt Governance Primitives, categorized by governance axis and risk mitigation.
- **[Normalized Analyses](data/analysis/)**: Structured YAML files for each assistant mode, providing a granular view of their internal constitutions.
- **[Schema & Tooling](data/schema/)**: The canonical schema and scripts used to drive the normalization process.

## Who this is for

- **Researchers**: Studying AI safety, alignment, and the governance of autonomous agents.
- **Agent Builders**: Looking for reproducible design patterns and modular controls for predictable agent behavior.
- **Tool Designers**: Seeking to implement clear authority boundaries and auditable safety constraints in developer tools.

## Status and limitations

This is a research-oriented project. All findings are derived from **static analysis of prompt text and architectural inference**. These analyses are **not runtime-validated**; they describe the *intended* governance as encoded in the prompt, which may differ from the model's actual behavior or the tool's underlying implementation.

## Quick overview of the repository

- [data/payload/](data/payload/) — parsed JSON payloads derived from captures
- [data/analysis/](data/analysis/) — normalized YAML analyses (schema v0)
- [data/prompts/](data/prompts/) — normalization instructions used by the analysis script
- [data/schema/](data/schema/) — canonical system-prompt schema (v0)
- [data/scripts/](data/scripts/) — helpers for redaction and running the normalization
- [AGENTS.md](AGENTS.md) — operational guidance and non-negotiable safety rules

## Quickstart

1. Make sure you have installed `make`, `uv` and set `OPENAI_API_KEY`.

2. Run the full analysis pipeline: `make -C data`

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
- Ask the project maintainer before publishing any real (even redacted) artifacts.

## Citation

If you use this research or the provided artifacts in your work, please cite it as follows:

```bibtex
@misc{espinoza2026system,
  author       = {Espinoza, R. Max},
  title        = {System Prompt Forensics: A Governance Framework for AI Developer Tools},
  year         = {2026},
  version      = {v0.9.0},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/rmax-ai/system-prompts-forensics/releases/tag/v0.9.0}}
}
```
