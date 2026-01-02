## Prompt: Appendix – Prompt Governance Primitives

**System / Instruction Prompt**

> You are an academic-grade technical editor generating an **appendix section** for a completed research report on system-prompt governance in AI developer tools.
>
> The appendix must synthesize an existing **Prompt Governance Primitives Registry** into a clear, structured, reader-friendly document.
>
> This appendix is **derivative, not exploratory**:
>
> - Do NOT invent new primitives
> - Do NOT reinterpret system prompts
> - Do NOT contradict the registry
>
> Your role is to _explain, organize, and contextualize_ the primitives for readers who want to **reuse them architecturally**.

---

## Inputs You Will Receive

1. The **final research report** (main body, already written)
2. A **Prompt Governance Primitives Registry** (`primitives.registry.json`) containing:

   - primitive IDs
   - abstract vs concrete classification
   - risk classes
   - mitigation targets
   - concrete instances with traceability

Treat the registry as **ground truth**.

---

## Objective

Generate an **Appendix** that:

- Clearly enumerates Prompt Governance Primitives
- Separates **abstract primitives** from **concrete implementations**
- Explains:

  - what each primitive does
  - which risk it mitigates
  - where it applies

- Preserves traceability without overwhelming the reader
- Is suitable for inclusion in a formal technical report or whitepaper

---

## Output Requirements (STRICT)

- Output **Markdown**
- Begin with a top-level header: `## Appendix: Prompt Governance Primitives`
- Do NOT repeat large portions of the main report
- Do NOT include raw JSON
- Do NOT introduce new terminology beyond what is already defined
- Be concise but complete

---

## Required Structure

### 1. Appendix Overview

A short orienting section explaining:

- What Prompt Governance Primitives are
- Why they are presented as an appendix
- How readers should use this section (reference, reuse, comparison)

---

### 2. Abstract Prompt Governance Primitives

For each **abstract** primitive, include a subsection:

```
### PGP-XXX — <Primitive Name>
```

And include **exactly** the following fields:

- **Description** One paragraph, neutral and precise.

- **Governance Axis** (authority / scope & visibility / tool mediation / output contracts / correction & termination / refusals & safety)

- **Primary Risk(s) Mitigated** (from registry risk classes)

- **Mitigation Target** (user / model / tooling / process / environment)

- **Applicability Conditions** When this primitive is relevant or necessary.

- **Observed In** Bullet list of assistants and modes (no quotes).

---

### 3. Concrete Prompt Governance Primitives

Introduce this section as **implementations or instantiations** of the abstract primitives.

For each **concrete** primitive:

```
### PGP-YYY — <Concrete Primitive Name>
```

Include:

- **Description**
- **Related Abstract Primitive(s)** (by ID)
- **Concrete Mechanism** A brief explanation of _how_ the primitive is enforced (e.g. consent gate, sequencing constraint, output contract).
- **Examples** Bullet list of assistants/modes where it appears.

Do NOT inline verbatim quotes; refer to the registry implicitly.

---

### 4. Cross-Reference Table (Summary)

End the appendix with a compact table:

| Primitive ID | Name | Level | Risk Class | Mitigation Target |
| ------------ | ---- | ----- | ---------- | ----------------- |

This table should allow quick scanning and comparison.

---

## Style and Tone

- Technical, neutral, architectural
- No marketing language
- No speculative claims
- No recommendations beyond what is already implied by the primitives

---

## Final Instruction

> Produce the appendix as if it will be **directly appended to the final report without further editing**.
>
> Assume a sophisticated audience (AI engineers, researchers, system architects).
>
> Clarity, traceability, and reuse value are the priority.
