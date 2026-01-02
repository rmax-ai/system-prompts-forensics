## Research Project Summary

**Title:** System Prompt Forensics: Reverse-Engineering Agent Architectures from Tooling Prompts

### 1. Research Goal

The goal of this project is to **systematically study, normalize, and analyze system prompts** used by modern AI-assisted developer tools (e.g. VS Code Copilot, Codex CLI, Copilot CLI, OpenCode CLI) in order to understand:

• How these tools encode **authority, constraints, and behavior** • How system prompts function as **implicit agent constitutions** • What architectural patterns recur across IDE tools, CLIs, and agent-based systems • How these patterns can be reused to design **robust, agent-first systems**

This is not a prompt-copying exercise. The objective is **architectural understanding and synthesis**.

---

### 2. Core Hypothesis

System prompts are **not task instructions**. They are **governance layers** that define:

• Who the agent is • What authority it has • What it can see • What actions it may take • How it reacts to failure • When it must stop

Different tools encode different assumptions about **agency, risk, and control**, and these assumptions are legible in their system prompts.

---

### 3. Scope of Study

The project focuses on **captured system prompts** from:

• IDE assistants (e.g. VS Code Copilot) • CLI-based tools (Codex CLI, Copilot CLI) • Agent-oriented developer tools (OpenCode CLI)

Each captured prompt is treated as a **primary research artifact**.

---

### 4. Methodology

#### 4.1 Prompt Decomposition

Each system prompt is decomposed into conceptual layers, explicitly separating concerns that are often interleaved:

• Identity and role framing • Authority and prohibitions • Context visibility and scope • Tool and command surface • Safety, legal, and style constraints • Feedback and correction mechanisms • Termination and stopping rules

This prevents shallow comparisons based on wording alone.

---

#### 4.2 Normalization into a Common Schema

All prompts are normalized into a **shared structural schema**, enabling meaningful comparison:

```
tool:
identity:
authority:
scope:
tools:
constraints:
reasoning:
correction:
termination:
```

Normalization preserves semantics while removing stylistic noise.

---

#### 4.3 Comparative Analysis via Invariants

Rather than comparing prompts directly, the project analyzes them along **invariant architectural dimensions**, including:

• Role orientation (user-subordinate vs task-subordinate vs environment-subordinate) • Authority boundaries (preventive vs procedural vs constitutional) • Tool exposure (explicit, abstracted, or hidden) • Feedback loops (none, user-driven, self-corrective) • Output contracts (style, format, or side-effect constrained)

This reveals **design intent and risk models** behind each tool.

---

#### 4.4 Diff-Driven Architecture Comparison

Pairwise comparisons are used to surface architectural trade-offs:

• IDE assistant vs CLI executor • CLI executor vs agent workspace • Suggestion engine vs autonomous agent

This explains why some tools minimize agency while others require explicit governance documents (e.g. AGENTS.md).

---

### 5. Expected Findings

The project expects to uncover:

• A small set of **reusable prompt primitives** • Clear architectural classes of system prompts: – Suggestion engines – Command executors – Workspace-bound agents – Constitutional stewards

• Evidence that more powerful agents require **externalized governance**, not longer prompts

---

### 6. Key Outputs

1. **Prompt Forensics Template** A markdown or YAML template for documenting system prompts consistently.

2. **Annotated Prompt Analyses** Deep, line-by-line analysis of selected system prompts.

3. **System Prompt Taxonomy** A classification of prompt architectures by control model and agency level.

4. **Composable Prompt Primitives** Identity, authority, scope, tool, feedback, and termination blocks reusable across systems.

5. **Canonical Agent Constitution Prompt** A synthesized system prompt designed by construction, not prose.

---

### 7. Non-Goals

This project explicitly does **not** aim to:

• Reproduce proprietary prompts verbatim • Bypass safeguards • Optimize jailbreak techniques • Compare model quality or output accuracy

The focus is **architecture, not exploitation**.

---

### 8. Why This Matters

Understanding system prompts at this level enables:

• Designing safer, more predictable agent systems • Moving governance out of hidden prompts into explicit documents • Building self-evolving systems with bounded authority • Treating prompts as **first-class infrastructure**, not magic strings

---

### 9. Immediate Next Steps

1. Select one captured system prompt as the first case study.
2. Normalize it into the shared schema without interpretation.
3. Perform invariant analysis and annotate architectural intent.

From there, the project scales linearly across tools.

---

> “What you permit implicitly will define your system more than what you command explicitly.” — paraphrased from systems engineering doctrine
