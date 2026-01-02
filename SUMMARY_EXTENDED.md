# Extended Summary: System Prompt Forensics

## 1. The Governance Thesis: Prompts as Constitutions
This research moves beyond the view of system prompts as mere "instruction sets" or "persona definitions." Instead, we treat them as **governance artifacts**—the foundational legal framework of an AI agent. These prompts encode the distribution of power, the boundaries of visibility, and the conditions for termination. By analyzing these "constitutions," we can reverse-engineer the implicit assumptions about risk and agency held by the teams that built them.

## 2. Architectural Classes of AI Assistants
Our analysis of GitHub Copilot, Codex, and OpenCode revealed four distinct architectural classes, each with a different governance posture:

- **Suggestion Engines (e.g., Copilot Inline)**: Minimal authority, focused on low-risk text generation with high policy compliance.
- **Command Executors (e.g., Codex Exec, Copilot CLI)**: High authority over the terminal, governed by strict procedural rules and "stop-and-ask" triggers.
- **Workspace Agents (e.g., VS Code Copilot Agent, vscode-codex)**: Broad authority over the filesystem and tools, managed through mode-tiered permissions and sandbox-aware escalation.
- **Constitutional Stewards (e.g., Codex Review, Copilot Plan)**: Specialized modes where the agent's primary role is to enforce a specific schema or workflow, often with tool-use restricted to research or validation.

## 3. The Authority Gradient
Authority is not a binary toggle; it is a gradient managed through three primary arbiters:
- **Policy-Supremacy**: (e.g., VS Code Copilot) Hard-coded refusals and identity disclosures that the model cannot override, even if the user insists.
- **User-Consent**: (e.g., vscode-codex Agent) Authority is expanded conditionally through approval-gated escalation. The user remains the final decision-maker for high-risk actions.
- **Model-Autonomy**: (e.g., vscode-codex Agent-Full-Access) The model is the final decision-maker within its sandbox, trading consent gates for internal termination controls and non-interference rules.

## 4. Tool Mediation as Procedural Governance
Tools in these systems are not just capabilities; they are **enforcement surfaces**. We observed several patterns of procedural governance:
- **Staged Workflows**: (e.g., Copilot Plan) Mandating a research step via `runSubagent` before any other action is allowed.
- **Intent Reporting**: (e.g., Copilot CLI) Requiring the agent to state its intent before invoking a tool.
- **Capability-Permission Separation**: (e.g., Codex Review) Having access to a tool (like `edit_file`) but being constitutionally forbidden from using it to make changes.

## 5. High-Impact Prompt Governance Primitives (PGPs)
The core contribution of this project is the cataloging of PGPs—modular rules that can be reused to build safer agents. Key examples include:
- **PGP-004 (Stop-on-unexpected-change)**: A circuit breaker that triggers a hard stop if the workspace changes in a way the agent didn't initiate.
- **PGP-001 (Approval-gated escalation)**: A mechanism to request higher privileges only when a specific tool call is blocked by a sandbox.
- **PGP-009 (Identity Disclosure)**: Hard-coded rules for how an agent must identify itself and its underlying model.

## 6. Conclusion: From Vibes to Infrastructure
The transition from "Prompt Engineering" to "Agent Architecture" requires moving governance out of hidden strings and into auditable, structured artifacts. This repository provides the forensic tools and the primitive library necessary to build agents that are not just "helpful," but constitutionally bound to be safe, predictable, and transparent.

---
*For the full technical analysis, see the [Research Report](data/final-research-report.revised.md) and the [PGP Appendix](data/appendix-governance-primitives.revised.md).*
