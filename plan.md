# Research Plan: System Prompt Forensics & Agent Governance

## 1. Purpose and Motivation

Modern developer tools (VS Code Copilot, Codex CLI, Copilot CLI, OpenCode CLI, etc.) rely heavily on _system prompts_ to shape model behavior. These prompts are often treated as opaque implementation details, yet they encode critical architectural decisions about agency, authority, safety, and control.

This research project treats system prompts not as instructions, but as **constitutions**: governance documents that define what an AI system _is_, _may do_, _must not do_, and _how it corrects itself_. The goal is to reverse-engineer these constitutions, compare them across tools, and extract reusable design patterns for agent-first systems.

---

## 2. Research Goals

Primary goal:

- To understand how different tools structure system prompts to govern AI behavior.

Secondary goals:

- Identify recurring architectural patterns across tools.
- Make implicit assumptions (authority, scope, feedback) explicit.
- Derive a reusable schema for analyzing and designing system prompts.
- Produce composable prompt primitives that can be used to design new agent systems.

Out of scope:

- Copying or reproducing proprietary prompts verbatim.
- Optimizing for prompt wording or stylistic tricks.
- Evaluating model performance or accuracy.

---

## 3. Core Research Questions

1. How do system prompts define _identity and role_?
2. How is _authority bounded_ (allowed vs forbidden actions)?
3. What _environmental context_ is visible to the model?
4. How are _tools_ exposed, restricted, or abstracted?
5. Are _feedback and correction loops_ explicitly encoded?
6. What are the _termination and stopping conditions_?
7. What failure modes does each prompt appear designed to prevent?

---

## 4. Key Assumptions

- A “system prompt” is a layered construct, not a single block of text.
- Most prompts embed multiple concerns: safety, UX, legal, and architecture.
- Meaningful comparison requires structural normalization, not prose comparison.
- Prohibitions (“must not”) are more informative than permissions.
- Prompt design reflects the tool’s dominant risk model.

---

## 5. Scope of Study

### Tools under analysis

- VS Code Copilot
- VS Code Codex
- Copilot CLI
- Codex CLI
- OpenCode CLI

### Prompt artifacts collected

- Static system prompts
- Session-level scaffolding
- Tool/function declarations
- Safety and refusal clauses
- Output format constraints
- Self-correction or iteration rules

---

## 6. Methodology

### Phase 1: Capture

Collect all available system prompt material via:

- CLI flags / debug modes
- Proxy-based interception
- Logged initialization payloads
- Public documentation and code references (where applicable)

Each capture is stored as a raw artifact with metadata (tool, version, context).

---

### Phase 2: Decomposition

Each captured prompt is decomposed into conceptual layers:

- Identity and role
- Authority and prohibitions
- Scope and visibility
- Tool surface and invocation rules
- Constraints (style, safety, legal)
- Reasoning and explanation policy
- Feedback and correction loops
- Termination and stopping conditions

---

### Phase 3: Normalization

All prompts are mapped into a shared schema to enable comparison.

#### Canonical normalization schema (example)

```yaml
tool: vscode-copilot
layers:
  identity:
    role: AI programming assistant
    persona: helpful, concise
  authority:
    allowed_actions:
      - suggest code
      - explain code
    forbidden_actions:
      - generate unsafe content
  scope:
    inputs_visible:
      - current file
      - surrounding context
    outputs_allowed:
      - text suggestions
      - code snippets
  tools:
    declared_tools: []
    invocation_rules: none
  constraints:
    style:
      - concise
      - code-focused
    safety:
      - content filtering enforced
  reasoning:
    hidden: true
    allowed: false
  correction:
    self_review: implicit
    external_feedback: user edits or rejection
  termination:
    stopping_conditions:
      - suggestion delivered
```
