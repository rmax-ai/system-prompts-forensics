# System Prompts as Governance Artifacts in AI Developer Tools — Executive Brief

## Executive Summary (≤200 words)

System prompts in AI developer tools are commonly treated as implementation details, but in practice they function as governance artifacts: they allocate authority between user intent and policy, bound permissible actions, constrain what the assistant may claim about workspace state, and define correction and termination behavior.

This work applies **prompt forensics**: a schema-based, cross-mode comparison of system prompts used by IDE and CLI developer assistants. We treat each interaction mode (e.g., ask/plan/agent, plan vs build, exec vs review) as a distinct constitutional variant that reallocates autonomy and permissible side effects.

Key contributions:

- A normalized, comparative analysis of system prompts across assistants and modes along authority, scope/visibility, tool mediation, and correction/termination dimensions.
- Identification of recurring constitutional patterns: mode-tiered autonomy, tools as enforcement boundaries, separation of capability from permission, state minimization as risk control, and conservative change doctrines.
- A synthesis of these recurring controls into **Prompt Governance Primitives (PGPs)**: reusable, prompt-encoded governance structures that can be composed to build or audit tool-mediated agents.

## The Problem: Hidden Governance in AI Systems

AI developer assistants increasingly act as tool-mediated agents: they can read files, search repositories, run commands, and sometimes modify working directories. In these settings, the governing system prompt does more than set style—it operates as an **invisible constitution**. It implicitly (and sometimes explicitly) answers operational questions that determine safety and controllability:

- Who is the final arbiter when user intent conflicts with policy or operational constraints?
- What is the assistant allowed to assume or claim about the environment?
- Which actions must be mediated through tools, and which side effects are forbidden?
- When must the assistant stop, ask for clarification, or terminate due to contract violations?

This governance layer is often under-analyzed because it is not typically surfaced as a first-class artifact. Yet it is one of the most concrete, text-level specifications of operational boundaries and failure-mode mitigations for agents acting in real repositories.

Treating system prompts as governance matters now because tool-mediated assistants are deployed into environments where failures are not abstract: they manifest as workspace corruption, autonomy drift, instruction leakage, and tool abuse.

## What We Studied

### Scope

We analyze system prompts across multiple developer assistants and interaction modes, including:

- Local software engineering agents with executor and reviewer constitutions.
- Terminal/CLI assistants with interactive versus prompt-oriented variants.
- CLI assistants with explicit plan-versus-build splits.
- IDE assistants with ask/plan/agent tiers and varying sandbox and approval semantics.

### What “prompt forensics” means

Prompt forensics is a structural analysis of system prompts as governance specifications. Rather than judging model outputs alone, we examine how prompt text encodes control structures that allocate authority, bound scope and visibility, mediate tool use, and define correction and termination behavior.

### Why prompt-level analysis is legitimate

Prompt-level analysis does not claim runtime enforcement fidelity. However, system prompts are explicit declarations of intended governance and are often the only observable specification of decision rights, tool constraints, and refusal/termination contracts. As such, they are valid artifacts for identifying architectural patterns, comparing regimes across tools and modes, and extracting reusable control structures—even under partial observability.

## Key Findings (Bulleted)

- **Tiered autonomy via modes:** Authority and permissible side effects are consistently partitioned by mode rather than treated as a single, uniform capability set.
- **Tool calls as enforcement boundaries:** Tools are the dominant action surface; prompts encode procedural obligations for tool use, not only access control.
- **Visibility minimization as a risk lever:** Prompts treat partial observability, memory policies, and bounded context as governance mechanisms to reduce overreach and long-horizon drift.
- **Conservative change and integrity doctrines:** Many regimes encode explicit safeguards against unintended workspace changes, including stop-and-ask triggers and restrictions on destructive operations.
- **Separation of capability from permission:** Tools may exist while specific outcomes remain forbidden; prompts explicitly constrain what the assistant is allowed to do despite apparent capability.
- **Emergence of reusable governance primitives:** Recurrent controls appear across assistants/modes and can be abstracted into modular Prompt Governance Primitives.

## Prompt Governance Primitives (PGPs)

PGPs are recurring, prompt-encoded control structures that allocate authority, bound scope and visibility, mediate tool use, constrain outputs, and/or define correction and termination behavior in tool-mediated assistants.

They qualify as “primitives” because they recur across assistants, compose into larger governance regimes, and can be referenced independently of any single vendor prompt.

Representative examples (not exhaustive):

- **PGP-001 — Approval-gated execution outside sandbox / escalated permissions:** Requires explicit user approval before actions that exceed sandbox/network/filesystem constraints or require escalated privileges.
- **PGP-004 — Stop-on-unexpected-workspace-changes circuit breaker:** If unexpected changes are detected that the assistant did not make, it must stop immediately and ask how to proceed.
- **PGP-008 — Commit/push requires explicit user request/confirmation:** Disallows committing or pushing to remote without explicit user request/confirmation.
- **PGP-009 — Read-only planning phase forbids implementation and modifications:** Plan/read-only modes allow observation and planning but prohibit edits or other side effects.
- **PGP-012 — Read-before-edit enforcement:** Requires reading a file before editing/writing it to reduce integrity and epistemic errors.
- **PGP-014 — Instruction confidentiality / no system prompt leakage:** Prohibits revealing internal instructions; treats the system prompt as confidential.

## Risks Addressed

This work maps prompt-encoded governance controls to concrete operational risks for tool-mediated agents.

- **Autonomy drift**
  - Addressed by: mode-tiered autonomy (plan vs build; ask/plan/agent), approval gates (PGP-001), and explicit stop conditions (PGP-004).
- **Tool abuse and prompt injection**
  - Addressed (indirectly) by: tool mediation and procedural constraints that keep side effects routed through declared tools and bounded by mode contracts.
- **Workspace corruption and unintended side effects**
  - Addressed by: conservative change doctrines; restrictions on destructive operations; read-before-edit rules (PGP-012); and stop-on-unexpected-change circuit breakers (PGP-004).
- **Instruction leakage**
  - Addressed by: explicit confidentiality constraints (PGP-014) that treat internal instructions as non-disclosable.
- **Unbounded context exposure / ungrounded claims**
  - Addressed by: bounded visibility disclosures, state minimization, and requirements for tool-grounded inspection (including, in some regimes, consulting authoritative documentation tools for capability questions).

These mitigations should be interpreted as intended controls expressed at the prompt layer, not as enforcement guarantees.

## Implications for Decision-Makers

### Agent-first development

Treat governance as an explicit architecture layer. System prompts already encode operational boundaries; making those boundaries first-class (and versioned) improves clarity about decision rights, side effects, and stop conditions.

### Multi-agent systems

The observed role partitioning (planner/reviewer/executor; ask/plan/agent) provides a template for separating capabilities and permissions across constitutions. Mode boundaries can act as explicit contracts that prevent role bleed-through.

### Enterprise AI governance

Schema-based normalization and comparison support auditing and change control. Treating prompts as governance artifacts makes it feasible to reason about drift across versions and to align internal expectations with declared constraints.

---
**Use of AI Assistance**: This research was produced with AI assistance: GPT-5.2 for data analysis and synthesis, ChatGPT for ideation and prompt refinement, ChatGPT Deep Research for citations, and Gemini 3 Flash for final edits. The author's primary contribution is the development of the AI-driven research methodology and data capture; the author does not claim analytical judgments or conclusions.

### Tooling and platform design

Tools function as the enforceable action surface. Designing tool APIs and agent platforms with explicit mediation points (side-effect gating, approval semantics, and stop-and-ask triggers) aligns runtime architecture with prompt-level governance declarations.

## What This Does NOT Claim

- This work does not claim that prompt-level governance is necessarily enforced at runtime.
- It does not claim completeness of coverage across all assistants, vendors, or modes.
- It does not claim that identifying primitives alone prevents failures; effectiveness depends on implementation, monitoring, and operational practice.
- It does not make claims about broader intelligence thresholds; it focuses on tool-mediated developer assistants operating in real repositories and terminals.

## How to Use This Work

- Use the comparative dimensions (authority, scope/visibility, tool mediation, correction/termination) to audit an assistant’s operating regime without relying on output-only evaluation.
- Use the PGP catalog as a vocabulary for specifying, reviewing, or negotiating governance requirements (e.g., “plan mode must enforce PGP-009”).
- Use the primitives as building blocks for internal constitutions without copying vendor prompts verbatim; treat the primitives as structural patterns.
- Consult the full paper for the detailed argumentation, framing, and limitations, and consult the appendix when you need the concrete primitive definitions and cross-references.

## Further Reading

- Full paper: System Prompts as Governance Artifacts in AI Developer Tools: A Forensic Comparative Study
- Appendix: Prompt Governance Primitives (PGP catalog and cross-reference table)
- Broader category: work on constitutional approaches to alignment, prompt-injection and tool-calling vulnerabilities, and agent security design patterns
