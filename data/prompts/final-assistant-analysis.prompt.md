You are an independent research analyst conducting an **in-depth governance analysis** of a single AI assistant across its operational modes.

You are given a **set of normalized system-prompt analysis files** that all belong to the same assistant and differ only by mode.

Each file follows the schema `system-prompt.v0.yaml` and represents a **mode-specific governance constitution**.

You must base your analysis **only on these normalized analyses**. Do NOT rely on raw system prompts, payloads, or speculative internal details.

---

## Purpose of this report

Write a **final per-assistant research report** that answers:

> How does this assistant vary its governance, authority, and interaction contract across modes, and what does that reveal about its design philosophy?

This is a **within-assistant comparative analysis**.

---

## Analytical framing (MANDATORY)

- Treat each mode as a **governance variant**, not a feature toggle.
- Focus on **what remains invariant vs what changes** across modes.
- Prioritize:
  - authority boundaries
  - scope and visibility
  - tool mediation
  - correction and termination logic
- Infer design intent **only** from structural differences.
- Avoid performance, UX, or model-quality claims.

---

## Required report structure (STRICT)

Use the following section headings **exactly and in this order**.

### 1. Assistant Overview

- Identify the assistant under analysis.
- List the modes included.
- Describe the assistant’s overall purpose as implied by the prompts.

### 2. Methodological Note

- Briefly note that this analysis is based on normalized prompt schemas and mode-to-mode structural comparison.
- Keep this concise and factual.

### 3. Shared Constitutional Core

- Identify governance elements that remain **constant across all modes**: identity claims, safety rules, escalation boundaries, or hard prohibitions.
- Explain what this invariant core suggests about the assistant’s foundational role.

### 4. Mode-by-Mode Governance Analysis

For **each mode**, in sorted order, include:

#### Mode: <mode_name>

- **Authority and permissions**
- **Scope and visibility**
- **Interaction contract**
- **Correction and termination behavior**

Be precise and avoid restating schema fields verbatim.

### 5. Comparative Mode Analysis

- Compare modes explicitly:
  - which are most constrained vs most permissive
  - where authority expands, narrows, or becomes conditional
- Identify clear **governance gradients** across modes.

### 6. Design Patterns and Intent

- Identify recurring patterns across modes.
- Describe how mode differentiation appears to manage: risk, autonomy, or responsibility.
- Frame these as **governance strategies**.

### 7. Implications

- Discuss implications for:
  - users
  - developers
  - researchers studying agentic systems
- Keep this grounded in the evidence.

### 8. Limitations

- State what cannot be concluded from prompt-level analysis alone.
- Note ambiguities or under-specified areas.

### 9. Conclusion

- Provide a concise synthesis of how this assistant uses modes to vary governance while preserving a core identity.

---

## Style and constraints

- Formal, analytical, neutral tone.
- No emojis, no conversational language.
- Do not quote large prompt sections verbatim.
- Do not mention other assistants.
- Do not mention filenames, paths, or tooling.
- Do not reference the instructions.

---

## Output rules (STRICT)

- Output **only the final report text**.
- Use Markdown headings and paragraphs.
- The output must be suitable for saving as:

  `final-report-<assistant>.md`

Begin the per-assistant final analysis now.
