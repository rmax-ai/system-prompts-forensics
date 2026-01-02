## 1. Assistant Overview

The assistant under analysis is **vscode-codex**, a GPT‑5.x–family “Codex” coding agent operating in a local CLI/IDE harness on a user’s computer. Across modes, it is positioned as a **concise, collaborative coding teammate** that can run shell commands, inspect and modify project files, and optionally manage a task plan.

**Modes included:**

- `agent-full-access`
- `agent`
- `chat`

Overall purpose implied by the constitutions: provide **tool-mediated software engineering assistance** (implementation, debugging, review) with strong operational guardrails around destructive actions, workspace integrity, and scan-friendly reporting.

## 2. Methodological Note

This report is derived solely from the provided **normalized system-prompt schemas** and a **mode-to-mode structural comparison** of identity, authority, scope, tool mediation, correction, and termination rules.

## 3. Shared Constitutional Core

Across all modes, the assistant maintains a stable governance nucleus:

- **Stable identity and role**: consistently a “coding agent” with a friendly, concise teammate persona; review behavior is explicitly risk- and correctness-oriented.
- **Hard safety boundaries around repository integrity**:
  - destructive git operations are disallowed unless explicitly requested/approved;
  - commit amendment is disallowed unless explicitly requested;
  - reverting unrelated/user changes is disallowed;
  - **unexpected changes trigger a stop-and-ask** behavior (do not proceed without user direction).
- **Tool-mediated operation**: actions are expected to occur through declared tools (shell execution, patch application, MCP reads, plan updates, image attachment), with explicit invocation constraints (e.g., set `workdir`, avoid `cd`).
- **Low-leakage, scan-friendly output contract**: avoid dumping large file contents; reference paths; plain-text/CLI-styled formatting conventions; constrained bulleting and file-reference formats.
- **Non-persistent state**: no memory and no session persistence in all modes.
- **Self-review and validation expectation**: self-review is enabled everywhere, with validation emphasized before yielding when changes are made or when autonomy is higher.

This invariant core suggests a foundational design role: a **local, tool-using coding operator** whose primary governance objective is to prevent accidental damage to the user’s working tree while remaining efficient and auditable through structured, minimal output.

## 4. Mode-by-Mode Governance Analysis

### Mode: agent

- **Authority and permissions**

  - Permits shell execution and file edits **within sandbox permissions**, with an explicit mechanism to **request escalated permissions** when policy allows.
  - Escalation is structurally supported (`allowed: true`) and the **user is the final decision-maker**, indicating a consent-gated authority model.
  - Maintains strict prohibitions on destructive git actions, commit amendment, and reverting unrelated changes; must stop on unexpected changes.

- **Scope and visibility**

  - Inputs include user/environment context, tool outputs, MCP resources (if configured), and optional local images.
  - Environment is local with **write filesystem access** but **limited network access**, implying a default posture of constrained external interaction.

- **Interaction contract**

  - Concise, scan-friendly, plain-text output; strong formatting constraints (no nested bullets, no URIs for file refs, no line ranges).
  - Planning is optional and governed (skip for easy tasks; avoid single-step plans; update after shared sub-tasks).
  - Review mode is formalized: findings-first, severity-ordered, with file/line references (notably, the formatting layer also restricts line ranges, creating a tension between “line refs” and “no line ranges”).

- **Correction and termination behavior**
  - Self-review triggers before yielding after code changes and after plan sub-tasks; rerun with approval if sandbox blocks important commands (when allowed).
  - Termination includes explicit “blocked by required approval” stopping conditions; handoff emphasizes asking for direction/approval or returning control with next steps.

### Mode: agent-full-access

- **Authority and permissions**

  - Broadest operational authority: shell commands, read/write files, MCP reads, image attachment, and plan updates.
  - **Escalation is disabled** (`allowed: false`) and the **final decision-maker is “policy”**, not the user—consistent with a configuration where approvals are not part of the runtime contract.
  - A distinctive constraint: **must not ask for approvals** when `approval_policy=never`, paired with an expectation to “persist and work around constraints” and finish/validate before yielding.
  - Still retains the same hard prohibitions on destructive git actions and commit amendment unless explicitly requested, and the same stop-on-unexpected-changes rule.

- **Scope and visibility**

  - Local execution with **full network access** and **filesystem write access**, increasing operational reach.
  - Inputs explicitly include system/developer instructions in payload and IDE open-tabs metadata, suggesting slightly broader contextual visibility than other modes.

- **Interaction contract**

  - Similar scan-friendly formatting and “reference paths, don’t dump files” discipline.
  - Adds a review-specific ordering rule: findings must precede any overview; and a stronger “do not ask for approvals” constraint that shifts responsibility to internal policy compliance rather than user-mediated consent.

- **Correction and termination behavior**
  - Self-review is emphasized “before yielding in approval_policy=never mode (validate work).”
  - Abort condition is explicit: if approval would be required but is disallowed and no workaround exists, the agent must abort.
  - Handoff returns control with verification guidance rather than seeking approvals.

### Mode: chat

- **Authority and permissions**

  - Similar to `agent` in structure: tool-mediated shell and patch editing, MCP access, and optional planning.
  - Escalation is supported and **user is final decision-maker**, but the captured environment context indicates **`sandbox_mode=read-only`** and **`approval_policy=on-request`**, making write authority conditional on approval.
  - Maintains the same prohibitions: no destructive git actions without explicit request/approval; no commit amendment unless requested; stop on unexpected changes.

- **Scope and visibility**

  - Local execution with **filesystem access effectively read-only** (as derived from environment context) and **restricted network**.
  - Inputs include a “single instructions string” plus environment context, tool schemas, and tool outputs—suggesting a more compact instruction surface than the agent payloads, but still within the same governance family.

- **Interaction contract**

  - Plain-text, scan-friendly output with strict formatting prohibitions (no nested bullets, no URIs, no line ranges).
  - For code changes, the contract specifies a “quick explanation” first, then context; review mode remains findings-first and severity-ordered.
  - Refusal style is under-specified (“unknown”), indicating less explicit guidance for handling disallowed requests compared to the agent variants.

- **Correction and termination behavior**
  - Self-review includes plan updates and validation guidance; if commands/tests cannot be run, provide verification steps.
  - Termination includes waiting for user response when approvals are required; handoff behavior is explicitly to ask the user.

## 5. Comparative Mode Analysis

- **Most permissive vs most constrained**

  - **Most permissive operationally**: `agent-full-access` (full network, write access, no escalation workflow, policy-driven autonomy).
  - **Most constrained**: `chat` in the captured configuration (read-only sandbox + restricted network + approvals required for non-read actions).
  - `agent` sits between: write access is available, network is limited, and escalation is available with user consent.

- **Authority expansion and conditionality**

  - The key governance gradient is **consent-gated authority**:
    - `agent-full-access` removes user-mediated escalation and instead enforces “do not ask for approvals,” shifting control to policy constraints and stop conditions.
    - `agent` and `chat` preserve a **user-as-final-authority** model via approval-based escalation.
  - A second gradient is **environmental reach**:
    - network: restricted/limited (`agent`, `chat`) → full (`agent-full-access`)
    - filesystem: read-only (`chat` as captured) → write (`agent`, `agent-full-access`)

- **Visibility and instruction surface**

  - `agent-full-access` explicitly includes system/developer instructions and IDE open-tabs metadata in visible inputs, implying a slightly broader operational context.
  - `chat` appears to have a more compact instruction representation, though tool schemas and environment context remain visible.

- **Correction/termination differences**
  - All modes share stop-on-unexpected-changes, but the **reason for stopping** differs:
    - `chat`/`agent`: often stop to obtain approval or direction.
    - `agent-full-access`: stop primarily when unexpected changes appear or when blocked by a constraint that cannot be worked around (since approvals cannot be requested).

## 6. Design Patterns and Intent

Several recurring governance strategies emerge:

- **Workspace-integrity primacy**: prohibitions against destructive git actions, commit amendment, and reverting unrelated changes are invariant, indicating a design intent to protect the user’s working state as the top operational safety objective.
- **Tool mediation with explicit invocation discipline**: requiring explicit tool calls, `workdir` specification, and discouraging `cd` suggests an intent to make actions **auditable and reproducible** within the harness.
- **Consent as a mode-dependent control plane**:
  - In `agent`/`chat`, risk is managed through **user-mediated escalation** (approvals with justification).
  - In `agent-full-access`, risk is managed through **policy-only constraints plus validation**, reflecting a design that supports autonomous execution when approvals are structurally unavailable.
- **Structured minimalism in outputs**: strict formatting and “no large dumps” rules function as governance to reduce accidental disclosure and improve operator oversight, even though explicit privacy rules are largely absent.
- **Termination as governance**: “stop and ask” on unexpected changes is a consistent circuit breaker; in full-access mode, abort conditions replace approval requests as the primary fail-safe.

Overall, mode differentiation appears to manage **risk and responsibility allocation**: either to the user (approval-gated modes) or to the policy harness (no-approval full-access mode), while keeping the same core safety invariants.

## 7. Implications

- **For users**

  - Users should expect consistent protection against destructive repository operations across modes, but different expectations about consent: `agent`/`chat` will seek approvals (when allowed), while `agent-full-access` will not and instead may proceed autonomously within policy limits or abort when blocked.
  - In read-only chat configurations, users should anticipate more “verification steps” and approval prompts for writes.

- **For developers**

  - The constitutions suggest a deliberate separation between **capability** (tools available) and **governance** (sandbox, approvals, escalation rules). Mode selection effectively chooses a responsibility model: user-in-the-loop vs policy-autonomous.
  - Strict formatting and file-reference rules indicate an emphasis on downstream rendering/consumption constraints (CLI/IDE), which developers must preserve to maintain governance guarantees.

- **For researchers studying agentic systems**
  - This assistant exemplifies a governance pattern where **agent autonomy is not merely tool access**, but a combination of (a) escalation availability, (b) approval policy, and (c) termination triggers.
  - The “stop on unexpected changes” rule functions as a robust, mode-invariant interrupt mechanism—an important design element for local agents operating in mutable workspaces.

## 8. Limitations

- Prompt-level analysis cannot confirm actual enforcement by the harness (e.g., whether sandboxing truly prevents writes or network calls).
- Several areas are under-specified across modes: explicit privacy/secret handling, data exfiltration constraints, and concrete definitions of “read” commands in sandbox contexts.
- Some internal tensions exist in the normalized rules (e.g., “file/line references” vs “no line ranges”), but the schemas do not resolve how conflicts are adjudicated at runtime.
- No conclusions can be drawn about real-world behavior, reliability, or compliance beyond what the constitutions specify.

## 9. Conclusion

vscode-codex uses modes as distinct governance variants that preserve a stable core identity—local coding agent, tool-mediated operation, and strong workspace-integrity safeguards—while varying **who authorizes risky actions** and **how far the agent can reach** (network/filesystem). The design philosophy is consistent: protect the user’s repository state through invariant prohibitions and a universal “stop-and-ask” circuit breaker, then modulate autonomy via sandbox/approval mechanics—either user-consent–driven (`agent`, `chat`) or policy-autonomous with validation and abort logic (`agent-full-access`).
