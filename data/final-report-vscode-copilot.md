## 1. Assistant Overview

The assistant under analysis is **vscode-copilot** (GitHub/Microsoft), operating as an IDE-integrated AI programming assistant.

**Modes included:**

- `agent`
- `ask`
- `plan`

Across modes, the implied overall purpose is to support programming and repository work inside VS Code, with mode-specific governance determining whether it can merely answer questions, inspect workspace context, produce plans, or take direct action via tools (including filesystem and terminal side effects).

## 2. Methodological Note

This report is derived solely from the provided **normalized system-prompt schemas** and a **structural comparison across modes**, treating each mode as a distinct governance constitution.

## 3. Shared Constitutional Core

Several governance elements remain invariant across all modes:

- **Identity and role anchoring:** The assistant is consistently framed as an _expert AI programming assistant_ in a VS Code context, with a professional, brief, and impersonal persona.
- **Policy supremacy:** In all modes, the **final decision maker is “policy”**, and the assistant claims alignment with Microsoft content policies and copyright avoidance.
- **Fixed refusal mechanism for specific harmful categories:** All modes enforce an **exact, refusal-only** response for harmful/hateful/racist/sexist/lewd/violent content requests.
- **Non-disclosure of internal governance:** All modes prohibit leaking system/developer/tooling instructions, especially via the commentary-channel preambles.
- **Channelized interaction pattern:** All modes recognize a separation between a **commentary channel** (for brief milestone/status preambles) and a **final answer channel** (for user-facing content), with explicit constraints on what preambles may contain.
- **No durable memory:** All modes specify `memory: false` (and where specified, no session persistence), indicating a consistent non-retentive interaction contract.

This invariant core suggests a foundational design role: a policy-governed IDE assistant that prioritizes controlled disclosure, predictable refusal behavior, and a standardized “professional assistant” identity regardless of operational capability.

## 4. Mode-by-Mode Governance Analysis

### Mode: agent

- **Authority and permissions**

  - Broadest operational authority: may **read/search/edit/create files**, run terminal commands, run notebook cells, and manage tasks, subject to detailed tool-routing rules.
  - Introduces a structured autonomy mechanism via **`manage_todo_list`** for non-trivial work, with strict state-transition rules (exactly one in-progress item, immediate completion marking).
  - Enforces operational micro-constraints (e.g., context requirements for `replace_string_in_file`, preference for `multi_replace_string_in_file` for multiple edits).

- **Scope and visibility**

  - Sees system instructions, user messages, environment info, and tool schemas; capture notes indicate **no workspace open**, which becomes a practical boundary for file operations.
  - Allows side effects: filesystem write and terminal execution are explicitly available, with limited network access.

- **Interaction contract**

  - Strongly procedural: milestone preambles before tool batches; tool use is explicit but **tool names must not be announced** to the user.
  - Output is generally markdown-structured except for trivial requests, where brevity overrides formatting and planning.

- **Correction and termination behavior**
  - Self-review is enabled; after edits, validation via diagnostics (`get_errors`) is suggested.
  - Terminates when the request is satisfied or when refusal triggers; aborts if tool constraints prevent completion (e.g., no workspace) or policy risk arises.

### Mode: ask

- **Authority and permissions**

  - Primarily a **question-answering and workspace-inspection** constitution: tools are limited to read/search/list/diff/symbol queries.
  - Explicitly restricts high-impact actions: **no commits unless explicitly requested**, and destructive commands require explicit repeated confirmation (even though terminal execution is not declared in this mode).
  - Includes guidance to read relevant files before editing/running commands, but the toolset itself is read-only, creating a governance posture of “advise and inspect” rather than “act.”

- **Scope and visibility**

  - Receives workspace structure snapshots and an attached operational policy file (`AGENTS.md`), plus repository metadata (branch/name/owner).
  - Filesystem access is described as **read**, and side effects are not clearly enabled; network access is unspecified.

- **Interaction contract**

  - Requires commentary-channel preambles before tool batches and imposes stylistic constraints on preamble variety.
  - Final answers must be professional markdown and, notably, include a rule to **add emojis to highlight key sections**, which sits in tension with the “short and impersonal” persona constraint.

- **Correction and termination behavior**
  - Self-review triggers include running diagnostics/tests and reviewing git status/diff/log before commits, reflecting a governance emphasis on cautious change control even in a mode that cannot directly edit.
  - Terminates on satisfaction or refusal; aborts if required context is missing and the user declines to provide it.

### Mode: plan

- **Authority and permissions**

  - Most restrictive on action: **planning-only**, with explicit prohibition on implementation and editing.
  - Tool mediation is uniquely gated: it **must call `runSubagent` once for research** (step 1), and **after it returns, no further tool calls are allowed**. This is a hard sequencing constraint not present in other modes.
  - Incorporates the same commit/destructive-action prohibitions from repository guidance, but these are largely moot given the no-implementation rule.

- **Scope and visibility**

  - Read-only workspace and limited network via `fetch_webpage`; side effects are explicitly **false**.
  - Visibility includes attachments and tool availability lists; the mode is designed to produce a plan informed by limited, controlled research.

- **Interaction contract**

  - Output must follow a **plan style guide**: “ONLY write the plan,” no code blocks, describe changes and reference files/symbols, and avoid manual testing sections unless requested.
  - Maintains commentary preambles for tool batches, but the tool-batch structure is intentionally minimized by the “single subagent call” rule.

- **Correction and termination behavior**
  - Termination logic is mode-protective: stop if drifting toward implementation; stop tool usage immediately after the subagent returns and present the plan.
  - Iteration is framed as plan refinement via user feedback, with re-research allowed only through the prescribed workflow (implying repeated cycles would re-enter the “subagent first” gate).

## 5. Comparative Mode Analysis

- **Most permissive vs most constrained**

  - **Most permissive:** `agent`—it can directly change the environment (write files, run terminal commands, execute notebook cells) and manage multi-step work with a formal todo mechanism.
  - **Intermediate:** `ask`—it can inspect and advise with read-only tools, while embedding strong guardrails around commits and destructive actions (despite lacking execution tools).
  - **Most constrained:** `plan`—it forbids implementation entirely and imposes a strict research-then-stop tool sequence.

- **Authority expansion and conditionality**

  - Authority expands from `plan` → `ask` → `agent` along two axes:
    1. **Side effects** (none → unclear/limited → explicit write/execute).
    2. **Autonomy structure** (plan template and single research call → ad hoc inspection → todo-governed multi-phase execution).
  - Conditional authority is most formalized in `agent` (todo gating, replacement-context rules, notebook routing) and most absolute in `plan` (no implementation; no tools after subagent).

- **Governance gradients**
  - A clear gradient emerges: **deliberation and containment** in `plan`, **interpretation and inspection** in `ask`, and **execution under procedural constraints** in `agent`.

## 6. Design Patterns and Intent

Recurring governance strategies across modes indicate a deliberate design philosophy:

- **Risk-tiered operational constitutions:** Modes appear to correspond to escalating operational risk. As side effects become possible (`agent`), governance becomes more procedural (todo discipline, edit-context requirements, notebook routing constraints).
- **Tool mediation as governance, not convenience:** Tool availability and sequencing rules (especially `plan`’s “single subagent then no more tools”) function as hard controls on autonomy and information gathering.
- **Channel separation to manage disclosure:** Commentary preambles are consistently constrained to prevent leakage and to standardize user-visible “status” without exposing internal reasoning or tool selection.
- **Policy-first identity with controlled self-representation:** All modes enforce fixed identity/model claims when asked, indicating a governance choice to standardize outward identity independent of underlying runtime metadata.
- **Repository governance injection:** In `ask` and `plan`, attached repository rules (e.g., commit/destructive command confirmations) are elevated into the assistant’s authority boundaries, suggesting a design intent to let local project governance shape assistant behavior.

## 7. Implications

- **For users**

  - Mode choice materially changes what the assistant is authorized to do: `plan` will not implement, `ask` will primarily inspect and advise, and `agent` can execute changes with side effects.
  - Users should expect consistent refusal behavior and limited transparency about internal instructions/tools, especially in preambles.

- **For developers**

  - The assistant’s governance is modular: toolsets, sequencing constraints, and side-effect permissions can be composed into distinct operational constitutions.
  - Embedding repository-specific operational rules (e.g., via attachments) is a practical mechanism for aligning assistant authority with project governance.

- **For researchers studying agentic systems**
  - This assistant provides a clear example of **mode-based authority partitioning**: autonomy is not merely reduced by removing tools, but also by adding workflow gates (todo discipline; single research call; post-research tool prohibition).
  - The constitutions illustrate how **interaction surfaces (commentary vs final)** can be used to enforce disclosure boundaries and standardize user-facing process signals.

## 8. Limitations

- Prompt-level analysis cannot determine actual runtime enforcement, tool availability in practice, or whether side-effect permissions are technically constrained beyond the declared schemas.
- The content of “Microsoft content policies” is referenced but not specified, limiting precision about the full safety boundary.
- Network access and data handling/privacy expectations are under-specified in all modes; conclusions about confidentiality or exfiltration risk cannot be made from these schemas alone.
- Iteration limits (timeouts, max cycles) are not defined, so persistence and termination behavior beyond stated stopping conditions remain ambiguous.

## 9. Conclusion

vscode-copilot uses modes as distinct governance constitutions that preserve a shared policy-first, non-disclosing, professional programming-assistant identity while varying authority through tool access, side-effect permissions, and workflow gating. `plan` enforces deliberation without action via strict research sequencing and planning-only output; `ask` supports inspection and advice with conservative change-control norms; `agent` enables execution with procedural constraints that structure autonomy and reduce operational risk. This mode differentiation reflects a design philosophy of **graduated authority with increasing procedural governance as capability and side effects increase**, while maintaining a stable interaction identity and refusal contract.
