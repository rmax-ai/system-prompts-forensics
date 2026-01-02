You are an independent research analyst conducting a **comparative governance analysis** of system prompts used by modern AI developer tools.

You are given a curated evidence bundle consisting of:

- Normalized system-prompt analyses (`analysis/*.analysis.yaml`)
- Quantitative similarity data (`similarities.csv`)
- Band stability analysis (`band-report.csv`)
- Prompt family definitions (`prompt-families.csv`)
- An interpretation memo of prompt families (`prompt-families-report.md`)
- Methodology and research intent documents (`methodology.md`, `goal.md`)

Treat these artifacts as **ground truth evidence**. Do NOT infer internal model details, training data, or business intent beyond what is explicitly encoded in the prompts.

---

## Purpose of the report

Write a **final comparative analysis report** that answers:

> How do modern developer tools differ and converge in the way they encode governance, authority, and interaction contracts through system prompts?

This report should synthesize _all prior artifacts_ into a coherent, defensible analysis.

---

## Analytical framing (MANDATORY)

- Treat system prompts as **constitutions**, not instructions.
- Treat prompt families as **stable governance regimes**, not clusters.
- Use similarity scores and band stability to justify claims about closeness or distance.
- Prefer **structural and authority-level differences** over stylistic ones.
- Make no performance or quality claims.

When in doubt, favor conservative interpretation.

---

## Required report structure (STRICT)

Use the following section headings **exactly and in this order**.

### 1. Introduction

- Briefly state the scope of the analysis.
- Explain why system prompts are analyzed as governance artifacts.
- Summarize the tools and prompt families under study.

### 2. Methodological Summary

- Explain, at a high level:
  - normalization
  - similarity measurement
  - band analysis
  - family extraction
- Justify why this method enables comparison without relying on proprietary internals.
- Keep this concise; details already exist in `methodology.md`.

### 3. The Prompt Family Landscape

- Describe the overall family structure:
  - number of families
  - size distribution
  - confidence distribution
- Explain what the similarity bands reveal about scale (mode-level vs operational vs product-level governance).

### 4. Comparative Analysis of Governance Regimes

For each prompt family (in family_id order):

- Describe its governance characteristics:
  - authority boundaries
  - scope and visibility
  - tool mediation
  - correction and termination behavior
- Explain what kind of interaction contract it encodes.
- Compare it explicitly to _at least one neighboring family_:
  - what is shared
  - what differs
  - why the difference matters

Avoid repetition; focus on contrast.

### 5. Cross-Tool and Cross-Vendor Comparison

- Compare Codex-oriented families vs Copilot-oriented families.
- Identify areas of convergence (shared governance patterns).
- Identify areas of divergence (distinct authority or safety models).
- Discuss whether differences appear mode-driven, product-driven, or lineage-driven.

### 6. Key Findings

Summarize the most important insights as **clear, testable statements**, for example:

- prompts converge on X
- prompts diverge on Y
- governance shifts at Z threshold

Do not exceed 5–7 findings.

### 7. Implications

Discuss implications for:

- tool designers
- researchers studying agentic systems
- future prompt-governance evolution

Keep this grounded in the data.

### 8. Limitations and Future Work

- State what this analysis cannot conclude.
- Identify what additional data would strengthen future comparisons (e.g. temporal versions, more tools, different domains).

### 9. Conclusion

- Provide a concise closing synthesis.
- Reiterate why prompt governance analysis is a useful lens.

---

## Style and constraints

- Tone: formal, analytical, neutral.
- No emojis, no conversational language.
- No quoting raw prompts or payloads.
- No references to “the model” or “this prompt.”
- Do not mention internal OpenAI or Microsoft processes.
- Write as if this were an internal research report or whitepaper draft.

---

## Output rules (STRICT)

- Output **only the final report text**.
- Use Markdown headings and paragraphs.
- Do not include appendices, tables of contents, or raw data dumps.
- Do not mention the instructions or artifacts explicitly by filename inside the prose.

Begin the final comparative analysis now.
