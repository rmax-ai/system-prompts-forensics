# Project Summary: System Prompt Forensics

## The Hidden Constitution
In the world of AI-assisted development, system prompts are often treated as mere instructions. However, our research reveals they are something far more significant: **implicit constitutions**. These hidden strings of text define the fundamental laws of an agent—what it is, what it can see, who it must obey, and when it must stop. Until now, these rules have remained opaque, buried in network traffic and proprietary payloads.

## The Forensic Approach
This project applies a forensic methodology to these "constitutions." By capturing raw HTTP traffic from tools like GitHub Copilot and Codex, we extract the underlying system prompts and normalize them into a structured, comparable format. We move beyond the prose to map out the actual governance layers:
- **Authority**: Who has the final say? (User vs. Policy vs. Model)
- **Scope**: What parts of the workspace are visible or writable?
- **Mediation**: How are tools gated and sequenced?
- **Termination**: What triggers a hard stop or a "stop-and-ask"?

## The Discovery of PGPs
Our analysis surfaced a recurring set of **Prompt Governance Primitives (PGPs)**—modular, atomic control structures that appear across different assistants. Whether it's an "Approval-gated execution" rule in Codex or a "Stop-on-unexpected-change" circuit breaker in Copilot, these primitives are the building blocks of predictable agent behavior. By cataloging these PGPs, we provide a library of proven safety patterns for the next generation of agent builders.

## From "Vibes" to Infrastructure
The goal of System Prompt Forensics is to move agent governance out of the realm of "prompt engineering vibes" and into the domain of **auditable infrastructure**. By making the implicit explicit, we enable researchers and developers to design agents with clear authority boundaries and verifiable safety constraints.

---
*For the full technical analysis, see the [Research Report](data/final-research-report.revised.md) and the [PGP Appendix](data/appendix-governance-primitives.revised.md).*
