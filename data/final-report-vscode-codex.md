## 1. Assistant Overview

The assistant under analysis is **vscode-codex**, a local coding agent operating through a Codex CLI/IDE harness and backed by a GPT‑5.x family model. The modes included are:

- **agent-full-access**
- **agent**
- **chat**

Across modes, the assistant’s implied purpose is consistent: provide **concise, tool-mediated coding help** on a user’s machine, including code edits, shell execution, optional planning, and review-oriented feedback when requested.

## 2. Methodological Note

This report is derived solely from **normalized system-prompt schemas** and a **structural comparison across modes**. Conclusions are limited to governance, authority, and interaction-contract differences explicitly represented in those normalized analyses.

## 3. Shared Constitutional Core

Several governance elements remain invariant across all modes:

- **Identity and role stability:** The assistant is consistently framed as a **coding agent / coding teammate** with a concise, factual, scan-friendly communication style and a review posture that emphasizes correctness and risk identification.
- **Non-interference with user work:** All modes prohibit reverting unrelated/user-made changes unless explicitly requested, and prohibit amending git commits unless explicitly requested.
- **Destructive-action restraint:** All modes restrict destructive git/file operations (e.g., `git reset --hard`) unless explicitly requested and/or approved, establishing a stable safety boundary around irreversible actions.
- **Unexpected-change stop rule:** All modes include a hard stop-and-ask behavior when “unexpected changes” are detected that the agent did not make, functioning as a termination/escalation trigger to protect workspace integrity.
- **Tool-mediated operation:** All modes rely on the same general tool family (shell execution, patch editing, MCP resource access, optional planning, image attachment) with explicit invocation constraints (e.g., set `workdir`, avoid unnecessary `cd`, prefer targeted patching).
- **Low persistence:** Memory and session persistence are consistently absent, implying a governance stance that avoids long-lived state accumulation.

This invariant core suggests a foundational role centered on **local, minimally disruptive software change assistance**, with governance designed to prevent accidental damage to a user’s working directory and to keep authority legible through tool calls and explicit constraints.

## 4. Mode-by-Mode Governance Analysis

### Mode: agent

- **Authority and permissions**
  - Operates with **sandbox-mediated authority**: can read/write within configured writable roots and run shell commands, but escalation is explicitly supported and governed by an approval policy.
  - Escalation is **allowed** and the **user is the final decision-maker** for escalated actions, indicating a consent-based authority model.
  - Includes a distinctive rule for on-request approvals: when a command is blocked and escalation is needed, the agent should request escalation via tool parameters with a brief justification, without pre-messaging the user.

- **Scope and visibility**
  - Sees conversation history, environment context (sandbox mode, network access, approval policy, writable roots), tool schemas, and limited IDE context (open tabs list without contents).
  - Network access is described as **limited** (mode-level environment), and filesystem access is **write** within sandbox constraints.

- **Interaction contract**
  - Strong formatting and concision requirements; findings-first review format when asked for “review.”
  - Planning is conditional: skip for trivial tasks; if used, must be multi-step and updated after shared sub-tasks.
  - Frontend-specific stylistic constraints appear (avoid boilerplate, intentional design), indicating domain-specific output governance layered atop general coding assistance.

- **Correction and termination behavior**
  - Self-review is enabled with triggers tied to substantial work and sandbox failures.
  - Termination includes waiting states when blocked by required approval, and a stop-and-ask requirement on unexpected changes.
  - The mode anticipates sandbox failures and channels them into an escalation workflow rather than silent workarounds.

### Mode: agent-full-access

- **Authority and permissions**
  - Authority is maximized: can read and edit files **including outside the workspace** due to full access, run shell commands, and use MCP resources.
  - Escalation is explicitly **disallowed**, and the **model is the final decision-maker**, shifting authority from user-mediated consent to agent autonomy within the mode’s constraints.
  - A key conditional governance inversion appears: when `approval_policy == never`, the agent must not request approvals and must proceed (or work around constraints), including permission to add temporary validation artifacts that must be removed before yielding.

- **Scope and visibility**
  - Similar input visibility to other modes (user messages, open tabs list, tool outputs), but paired with **full network access** and **write filesystem access**.
  - The combination of full filesystem reach and full network access materially expands operational scope and risk surface.

- **Interaction contract**
  - Maintains the same concision and scan-friendly formatting regime, with additional strictness around not dumping large file contents and path-based referencing.
  - Planning remains optional for straightforward tasks, but if used must be multi-step and actively maintained.

- **Correction and termination behavior**
  - Self-review triggers are explicit (validate before yielding; update plan after sub-tasks; respond to tool failures).
  - Termination logic includes a hard abort on unexpected changes (stop and ask user), even though escalation is not available—this functions as a compensating control for high authority.
  - The mode forbids proceeding silently after unexpected changes, emphasizing workspace integrity as a primary termination trigger.

### Mode: chat

- **Authority and permissions**
  - Authority is comparatively constrained by an explicitly inferred active environment: **read-only sandbox mode**, **restricted network**, and **on-request approvals**.
  - Escalation is allowed (to user/tool), and the **user is the final decision-maker** for escalations and destructive actions.
  - Conditional permissions are more granular than in agent mode: separate conditions for read-only sandbox, restricted network, and destructive actions with explicit request/approval.

- **Scope and visibility**
  - Similar visibility set (system instructions, user messages including environment context, tool schemas, open tabs list, placeholder AGENTS content).
  - Environment is explicitly **filesystem read** (active), with limited network access and an approval mechanism to expand scope.

- **Interaction contract**
  - Strongest emphasis on CLI-oriented formatting discipline: plain text, scannable structure, strict file reference conventions, and findings-first review structure.
  - Explicit refusal/workaround posture: work around constraints where possible; request approval when necessary (unless approvals are disallowed by policy).

- **Correction and termination behavior**
  - Self-review triggers include plan updates and pre-yield validation in never-approval contexts (even if not active here), plus stop-and-ask on unexpected changes.
  - Termination includes being blocked by required approval (and user denial), and aborting when destructive action is required without explicit request/approval.
  - The mode’s correction loop is tightly coupled to sandbox failures and approval gating.

## 5. Comparative Mode Analysis

A clear governance gradient emerges:

- **Most permissive:** **agent-full-access**
  - Full filesystem reach (including outside workspace) and full network access.
  - No escalation pathway; the model holds final authority, constrained primarily by prohibitions on destructive actions and non-interference rules.
  - Designed for autonomous execution under a “no approvals” contract.

- **Intermediate:** **agent**
  - Write access within sandbox constraints and limited network.
  - Escalation is available and user-mediated; authority expands conditionally via approvals.
  - Balances agent initiative with explicit consent gates.

- **Most constrained:** **chat**
  - Active read-only filesystem and restricted network, with on-request escalation.
  - Authority is primarily advisory unless the user grants escalations; destructive actions require explicit request/approval.
  - The interaction contract is the most explicit about conditional permissions and refusal/workaround behavior.

Across modes, authority expands or narrows primarily through (a) **filesystem scope**, (b) **network scope**, and (c) whether escalation is **available and user-governed** versus **disabled and agent-governed**.

## 6. Design Patterns and Intent

Several recurring governance strategies appear:

- **Workspace-integrity primacy:** The consistent prohibition on reverting unrelated changes and the stop-on-unexpected-changes rule indicate a design intent to treat the user’s working directory as a protected asset, regardless of mode.
- **Consent as a configurable control plane:** In agent and chat modes, escalation and approvals operationalize user consent as a first-class governance mechanism; in full-access mode, consent is replaced by strict prohibitions and stop conditions.
- **Tool mediation as accountability:** Explicit tool invocation rules (workdir requirements, patch preference, planning constraints) function as procedural governance—limiting how authority is exercised rather than merely what outcomes are allowed.
- **Conditional governance rather than static rules:** The constitutions encode behavior switches based on approval policy, sandbox mode, network restriction, and user intent (“review”), suggesting a design philosophy that treats context as determinative for authority.
- **Output governance as risk management:** Strict formatting, concision, and “do not dump large files” constraints reduce accidental disclosure and operational confusion, even though explicit privacy rules are notably absent.

Overall, mode differentiation appears to manage **risk and responsibility allocation**: constrained modes allocate decision authority to the user via approvals; full-access mode allocates authority to the agent while strengthening termination triggers and non-destructive constraints.

## 7. Implications

- **For users**
  - Users should expect materially different control dynamics: chat/agent modes preserve user authority through approvals, while full-access mode shifts control to the agent and relies on prohibitions and stop rules for safety.
  - The consistent stop-on-unexpected-changes behavior can interrupt workflows but serves as a predictable safeguard for workspace integrity.

- **For developers**
  - The governance design suggests that safe operation depends heavily on **sandbox configuration and approval policy**; mode selection effectively determines whether consent is enforced procedurally (approvals) or replaced by behavioral constraints.
  - Tooling constraints (patch preference, planning rules, command execution discipline) are central to maintaining predictable behavior across environments.

- **For researchers studying agentic systems**
  - This assistant provides a clear example of **authority partitioning by mode**: autonomy increases with access breadth and decreases with stronger consent gating.
  - The constitutions illustrate how “termination logic” (stop-and-ask on unexpected changes) can serve as a compensating control when escalation is unavailable.

## 8. Limitations

- The analysis cannot determine how reliably “unexpected changes” are detected, as the detection mechanism is not specified.
- No conclusions can be drawn about actual runtime enforcement beyond what the normalized prompt structures describe (e.g., whether network restrictions are technically enforced or merely instructed).
- Privacy, secrets handling, and data minimization are under-specified; absence in the prompt analysis does not prove absence in other system layers.
- Iteration limits, timeouts, and refusal styles are not fully defined, limiting conclusions about boundedness and termination under prolonged failure.

## 9. Conclusion

vscode-codex maintains a stable constitutional core centered on being a concise local coding teammate that protects user workspace integrity and avoids destructive or unsolicited reversions. Modes primarily vary governance by reallocating authority: **chat** and **agent** implement consent-driven escalation under sandbox constraints with the user as final arbiter, while **agent-full-access** removes escalation and expands operational scope (filesystem and network), compensating with stricter non-interference and stop conditions. This reveals a design philosophy that treats “mode” as a governance contract: a deliberate reconfiguration of autonomy, consent, and risk controls rather than a superficial interface change.