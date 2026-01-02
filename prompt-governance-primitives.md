# Prompt Governance Primitives

_A reference schema for agent-first system design_

## Purpose

This document extracts **reusable governance primitives** from comparative analysis of IDE and CLI AI developer assistants. These primitives describe how system prompts allocate authority, constrain action, manage risk, and enforce accountability. They are intended to be **composable**, **mode-aware**, and **implementation-agnostic**, suitable for designing robust agentic systems beyond developer tooling.

This is not a safety policy or prompt-writing guide. It is a **governance layer reference**.

---

## 1. Authority Allocation Primitive

**Definition** The authority allocation primitive specifies **who is allowed to authorize actions** and **where final adjudication resides**.

**Canonical loci**

- **User-sovereign**: user approval required for escalation or irreversible actions.
- **Policy-sovereign**: external policy adjudicates and overrides model or user discretion.
- **Model-sovereign**: the model is the final arbiter, constrained by output contracts and epistemic rules.

**Design guidance**

- Treat authority as **distributed**, not binary.
- Allocate authority based on expected externalities (e.g. workspace mutation vs analysis).
- Make escalation paths explicit (“stop-and-ask”, refusal, abort).

**Common failure mode**

- Implicit authority: allowing actions without stating who authorizes them.

---

## 2. Mode-Based Partitioning Primitive

**Definition** Modes are **constitutional variants** that reallocate authority, scope, and risk without changing core capabilities.

**Typical partitions**

- **Plan**: read-only, deliberative, no side effects.
- **Ask / Review**: inspection, explanation, or judgment without mutation.
- **Act / Build / Exec**: tool-mediated execution with governance constraints.

**Design guidance**

- Use modes to bound risk, not to signal UX intent.
- Ensure each mode has explicit prohibitions (not just permissions).
- Avoid “soft” mode boundaries; enforce via tool gating and termination rules.

**Common failure mode**

- Planning modes that silently drift into execution.

---

## 3. Scope and Visibility Primitive

**Definition** This primitive governs **what the agent can see, claim, infer, and act upon**.

**Key dimensions**

- **Context visibility**: current session only vs persistent memory.
- **Read vs write scope**: inspection-only vs mutation-capable.
- **Disclosure boundaries**: what may be quoted, summarized, or referenced.

**Design guidance**

- Use visibility limits as epistemic constraints (“do not assume unseen state”).
- Prefer references (paths, symbols) over verbatim dumps.
- Allow repository- or project-injected governance to override defaults.

**Common failure mode**

- Allowing broad claims without visibility guarantees.

---

## 4. Tool Mediation Primitive

**Definition** All environment interaction occurs **through tools**, which act as auditable control surfaces.

**Typical controls**

- Mandatory tool use for side effects.
- Explicit working directory requirements.
- Prohibitions on implicit state changes (e.g. `cd`, interactive flags).
- Parallelization or sequencing constraints.

**Design guidance**

- Separate **capability declaration** from **permission to use**.
- Encode workflow norms (tests, hooks, validation) as tool rules.
- Treat tool invocation as a contractual act, not a convenience.

**Common failure mode**

- Granting tools without procedural constraints.

---

## 5. Sequencing and Autonomy Throttling Primitive

**Definition** This primitive constrains **the order and number of actions**, limiting autonomy without reducing intelligence.

**Examples**

- Single research call, then no tools.
- Plan → explicit user confirmation → execute.
- Validation required before yielding output.

**Design guidance**

- Use sequencing to prevent drift from intent to side effects.
- Hard limits are often more reliable than advisory language.
- Particularly effective in planning and high-risk contexts.

**Common failure mode**

- Allowing iterative tool loops in deliberative modes.

---

## 6. Consent Gate Primitive

**Definition** Explicit user authorization is required for **irreversible or high-impact transitions**.

**Typical gated actions**

- Git commits, pushes, rebases.
- Destructive file operations.
- Network access or external publication.

**Design guidance**

- Make consent a structural requirement, not a suggestion.
- Where consent cannot be requested, substitute abort logic and validation.
- Clearly define what counts as “irreversible”.

**Common failure mode**

- Bundling gated and non-gated actions together.

---

## 7. Output Contract Primitive

**Definition** Strict constraints on output format and content act as **governance surfaces**.

**Common forms**

- JSON-only schemas.
- Plan-only prose with no code blocks.
- Scan-friendly or machine-ingestable formats.

**Design guidance**

- Use output contracts to enforce epistemic discipline.
- Prefer contracts that downstream systems can validate.
- Terminate rather than speculate when contracts cannot be satisfied.

**Common failure mode**

- Overloading outputs with explanation that violates contracts.

---

## 8. Correction and Validation Primitive

**Definition** Defines how the agent detects, corrects, and validates errors.

**Typical mechanisms**

- Test/build execution before yielding results.
- Tool-output–grounded corrections.
- Self-validation when approvals are unavailable.

**Design guidance**

- Prefer external validation (tools) over self-assertion.
- Make correction loops explicit and bounded.
- Tie validation requirements to authority level.

**Common failure mode**

- Silent correction without evidence.

---

## 9. Termination and Circuit Breaker Primitive

**Definition** Specifies **when the agent must stop, pause, or return control**.

**Common triggers**

- Unexpected workspace changes.
- Insufficient evidence to make claims.
- Policy or tool blockage.
- Mode boundary violations.

**Design guidance**

- Treat termination as a first-class behavior.
- Encode “stop-and-ask” paths clearly.
- Abstention is a valid and often correct outcome.

**Common failure mode**

- Forcing completion despite uncertainty or blockage.

---

## 10. Risk Alignment Matrix (Summary)

| Risk Type            | Primary Primitives                            |
| -------------------- | --------------------------------------------- |
| Workspace corruption | Consent gates, termination, tool mediation    |
| Malicious misuse     | Policy-sovereign authority, refusal templates |
| Epistemic error      | Output contracts, visibility limits           |
| Autonomy drift       | Mode partitioning, sequencing constraints     |
| Governance leakage   | Disclosure boundaries, output minimalism      |

---

## Closing Note

Effective agent governance emerges from **composition**, not verbosity. Increasing agent capability reliably requires _more explicit structure_, not longer instructions. These primitives provide a vocabulary and design surface for building agent constitutions that scale in power while remaining auditable, predictable, and aligned.

---

_“Power reveals itself most clearly in procedure.”_
