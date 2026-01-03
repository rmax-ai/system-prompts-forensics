# System Prompt Forensics: Governance Structures in AI Developer Assistants

### What This Is
- A forensic research project analyzing system prompts in AI-assisted developer tools.
- A methodology for normalizing and comparing "invisible constitutions" across different AI agents and modes.
- A catalog of reusable control structures (Prompt Governance Primitives) for agentic systems.
- A repository of normalized prompt artifacts, schemas, and analysis scripts.

### What This Is Not
- A collection of prompt engineering tips or "hacks."
- A guide for bypassing AI safety filters or jailbreaking models.
- A runtime validation of model behavior (focuses on static prompt analysis).
- A product or tool for end-users; it is research-oriented.

### Core Contribution
This project treats system prompts as a distinct governance layer—a "governance constitution"—that defines an agent's identity, authority, and safety boundaries. By decomposing complex prompts into modular **Prompt Governance Primitives (PGPs)**, we surface the architectural trade-offs and control mechanisms that shape modern agentic systems. Our comparative forensics across tools like GitHub Copilot, Codex, and OpenCode reveals how prompts implement tiered autonomy, action gating, and workspace-integrity safeguards.

### Repository Structure
- [paper/](paper/) — Full research paper, executive briefs, and board briefs.
- [data/analysis/](data/analysis/) — Normalized YAML analyses of system prompts.
- [data/payload/](data/payload/) — JSON payloads derived from raw HTTP captures.
- [data/schema/](data/schema/) — Canonical schema for system-prompt normalization.
- [data/scripts/](data/scripts/) — Tooling for redaction, normalization, and analysis.
- [data/prompts/](data/prompts/) — Source prompts used for analysis and synthesis.
- [AGENTS.md](AGENTS.md) — Operational guidance and safety rules for the repository.

### How to Read This Repository
- **First-time reader:** Start with the [Executive Brief](paper/executive-brief.md) and the [Research Paper](paper/paper.md).
- **Technical reader:** Explore the [Normalized Analyses](data/analysis/) and the [Schema](data/schema/system-prompt.v0.yaml).
- **Executive reader:** Review the [Board Brief](paper/board-brief.md) for high-level governance implications.

### Methodology Summary
We treat system prompts as governance artifacts. The methodology involves capturing raw HTTP requests from AI developer tools, redacting sensitive information, and normalizing the prompts into a canonical YAML schema. This allows for structural comparison along dimensions such as authority boundaries, scope/visibility, tool mediation, and termination logic.

### Status and Scope
- **Current completeness:** Core analysis of GitHub Copilot, Codex, and OpenCode is complete.
- **Frozen vs Evolving:** The methodology and schema are stable; new analyses are added as new tools or modes are captured.
- **Known limitations:** Analysis is based on static prompt text and architectural inference, not runtime validation.

### Citation
```text
Espinoza, R. M. (2026). System Prompt Forensics: Governance Structures in AI Developer Assistants (Version 1.0.0). [Research Report]. https://system-prompts-forensics.rmax.ai
```

### License
Licensing status is currently under review.

### Contact / Attribution
- R. Max Espinoza
- [system-prompts-forensics.rmax.ai](https://system-prompts-forensics.rmax.ai)
- Ask the project maintainer before publishing any real (even redacted) artifacts.

## Citation

If you use this research or the provided artifacts in your work, please cite it as follows:

```bibtex
@misc{espinoza2026system,
  author       = {Espinoza, R. Max},
  title        = {System Prompt Forensics: A Governance Framework for AI Developer Tools},
  year         = {2026},
  version      = {v1.0.0},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/rmax-ai/system-prompts-forensics/tree/v1.0.0}}
}
```
