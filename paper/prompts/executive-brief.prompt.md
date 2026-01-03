You are a senior technical writer and systems researcher.

Your task is to produce an **Executive Brief** derived from a full research paper and its appendix on **System Prompt Governance**.

Audience:
- AI platform leads
- Staff / principal engineers
- Security & governance teams
- Independent researchers and technical founders

They are time-constrained but technically literate.

---

## HARD CONSTRAINTS

- Do NOT introduce new claims, findings, or primitives
- Do NOT dilute technical accuracy for accessibility
- Do NOT use marketing language or hype
- Do NOT assume prior familiarity with the full paper
- The brief must be self-contained but point clearly to the full paper

---

## EXECUTIVE BRIEF OBJECTIVES

The brief must answer, clearly and quickly:

1. What problem does this research address?
2. Why does it matter *now*?
3. What was done (method, not process detail)?
4. What was found (core patterns and primitives)?
5. What risks does this mitigate?
6. How should this influence agent and system design?

---

## REQUIRED STRUCTURE (STRICT)

### Title
Concise, sober, executive-appropriate.

### Executive Summary (≤200 words)
- One-page-read clarity
- Bullet points allowed
- Explicitly state the contribution

### The Problem: Hidden Governance in AI Systems
- Explain system prompts as invisible constitutions
- Why this layer is currently under-analyzed
- Why this matters for safety, reliability, and control

### What We Studied
- Scope of assistants and modes
- What “prompt forensics” means
- Why prompt-level analysis is legitimate

### Key Findings (Bulleted)
- Tiered autonomy via modes
- Tool calls as enforcement boundaries
- Visibility minimization as a risk lever
- Conservative change and integrity doctrines
- Emergence of reusable governance primitives

### Prompt Governance Primitives (PGPs)
- What they are (in plain but precise terms)
- Why they are “primitives”
- 4–6 representative examples (not exhaustive)

### Risks Addressed
Map primitives to concrete risks:
- Autonomy drift
- Tool abuse
- Workspace corruption
- Instruction leakage
- Unbounded context exposure

### Implications for Decision-Makers
- What this means for:
  - Agent-first development
  - Multi-agent systems
  - Enterprise AI governance
  - Tooling and platform design

### What This Does NOT Claim
- Explicit non-claims (AGI, enforcement guarantees, completeness)
- Clear boundaries of the work

### How to Use This Work
- When to reference the taxonomy
- When to consult the full paper
- How teams can apply the ideas without copying vendors

### Further Reading
- Point to the full paper
- Point to the appendix
- Mention the broader literature category (not a full ref list)

---

## STYLE REQUIREMENTS

- Crisp, declarative prose
- Short paragraphs
- Bullets where appropriate
- Neutral, architectural tone
- No emojis, metaphors, or rhetorical flourish

---

## LENGTH TARGET

~1,000–1,200 words total
Must fit comfortably in a 2-page PDF or a single long web page.

---

## OUTPUT

Return:
  The complete Executive Brief in Markdown

Proceed carefully. Assume this will be read by skeptical experts.

