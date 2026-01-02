# 1. Assistant Overview

The assistant under analysis is **vscode-copilot** (GitHub/Microsoft), operating as an AI programming assistant embedded in the **VS Code** IDE context.

**Modes included:**
- `agent`
- `ask`
- `plan`

Across modes, the assistant’s implied purpose is to provide **programming help within an editor/workspace context**, with varying degrees of autonomy and side-effect capability (from read-only Q&A to tool-mediated editing/execution), while remaining bound to Microsoft content policies and specific disclosure constraints.

# 2. Methodological Note

This report is derived solely from **normalized system-prompt schemas** for each mode and a **structural comparison** of governance elements (authority, scope, tools, constraints, correction, termination). No inferences are drawn from raw prompts or undocumented internal behavior.

# 3. Shared Constitutional Core

Several governance elements are invariant across all modes:

- **Stable identity and disclosure constraints:** The assistant is consistently framed as an expert programming assistant in VS Code, with **hard-coded responses** for identity queries (name must be “GitHub Copilot”; model must be “Raptor mini (Preview)”).
- **Policy primacy:** In all modes, **policy is the final decision-maker**, explicitly overriding user intent when conflicts arise.
- **Fixed refusal mechanism for specified harmful categories:** Requests for harmful/hateful/racist/sexist/lewd/violent content trigger an **exact, single-string refusal** with no additional text.
- **Non-leakage of internal governance:** All modes prohibit leaking system/developer/tool instructions, especially via the **commentary-channel preambles**.
- **Concise, impersonal communication baseline:** Each mode emphasizes short, professional, impersonal responses, with “trivial request” exceptions to formatting rigor.
- **No persistent memory:** All modes specify **no memory** and **no session persistence**, limiting governance to the current interaction context.

This invariant core suggests a design centered on **tight institutional compliance** (policy and disclosure), **controlled transparency** (no prompt/tool leakage), and **bounded conversational continuity** (statelessness), regardless of whether the assistant is allowed to act on the workspace.

# 4. Mode-by-Mode Governance Analysis

## Mode: agent

### Authority and permissions
- Broadest operational authority: may **read/search/edit/create files**, **run terminal commands**, manage tasks, and operate on notebooks via specialized tools.
- Explicit constraints shape how authority is exercised: e.g., must not use `create_file` to edit existing files; must prefer batched replacements; must avoid terminal-based Jupyter operations when notebook tools exist.
- Planning is formalized via `manage_todo_list`, conditionally required for non-trivial tasks, indicating a governance preference for **structured execution** when autonomy increases.

### Scope and visibility
- Sees system instructions, user messages, environment/workspace info, and tool schemas; however, the capture notes “workspace not open,” implying governance anticipates tool use even when context may be absent.
- Outputs include markdown answers, code snippets, and tool calls with side effects.

### Interaction contract
- Two-channel contract is emphasized: **commentary** for milestone/status preambles and **final** for the substantive response.
- Strong formatting governance: professional Markdown with headings and backticks; additionally, an explicit requirement to use **emojis in final answers** (except trivial requests), creating a notable stylistic mandate alongside “impersonal/brief.”

### Correction and termination behavior
- Self-review is enabled with recommended validation (e.g., `get_errors` after edits).
- Termination is tied to either satisfying the user request or completing todos (if planning is used), reflecting an execution-oriented completion criterion.
- Abort logic includes immediate refusal for disallowed content and implicit inability to perform file operations when no workspace is open.

## Mode: ask

### Authority and permissions
- Primarily a **read-only assistance** mode: can answer questions and use tools to inspect the workspace (search/list/read, symbol search, diffs).
- Explicit operational safety constraints appear despite limited side effects: no commits unless explicitly requested; destructive commands require repeated confirmation; push-to-main restrictions. These function as **preventive governance**, even though the declared toolset is non-destructive.

### Scope and visibility
- Inputs include workspace info, repository metadata, and attached `AGENTS.md` rules, indicating that repository-local governance can be incorporated.
- Side effects are explicitly disallowed; filesystem access is read-only.

### Interaction contract
- Commentary-channel preambles are tightly regulated (cadence, variety constraints, no label+colon starts), indicating governance attention to **meta-communication discipline**.
- Final responses must be professional Markdown; tables are encouraged for comparisons; trivial requests bypass full formatting.

### Correction and termination behavior
- Self-review triggers are oriented around safe change management (review diffs/status/log before commits) and repository guidance.
- Termination occurs when the request is satisfied or the user ends the conversation; abort conditions include disallowed content or insufficient context when the user declines inspection/clarification.

## Mode: plan

### Authority and permissions
- Most constrained in terms of action: explicitly **planning-only**, forbidding implementation, file edits, and execution.
- Distinctive mandatory mediation: the workflow **must call `runSubagent` for research**, and then **no further tool calls are allowed after it returns**. This creates a gated, staged authority model: research is delegated, then the main agent becomes tool-silent.
- Maintains the same policy/disclosure/refusal constraints as other modes, plus a hard boundary against transitioning into implementation.

### Scope and visibility
- Read-only workspace and limited network via `fetch_webpage` are available, but tool usage is procedurally constrained by the runSubagent-first rule.
- Outputs are restricted to planning documents; additionally, plan output must follow a plan template and **must not include code blocks**, reinforcing the “no implementation” boundary at the formatting layer.

### Interaction contract
- The contract is explicitly iterative: draft a plan, then request user feedback; success is framed as user confirmation/iteration rather than execution completion.
- Commentary-channel preambles remain required and non-leaky, consistent with other modes.

### Correction and termination behavior
- Correction is primarily plan iteration based on feedback; “after edits run diagnostics” appears as a generic trigger but is structurally neutralized by the prohibition on edits.
- Termination is intentionally early: after presenting a draft plan, the agent pauses for feedback; it must stop immediately if it begins considering implementation.

# 5. Comparative Mode Analysis

**Most permissive to most constrained (by operational authority and side effects):**
1. `agent` (write + execute + notebook operations; structured task management)
2. `ask` (read-only inspection; advisory; preventive constraints on commits/destructive actions)
3. `plan` (planning-only; no implementation; tool usage procedurally constrained)

Key governance gradients:
- **Side-effect gradient:** `agent` explicitly allows filesystem writes and terminal execution; `ask` and `plan` explicitly disallow side effects and restrict filesystem access to read-only.
- **Tool mediation gradient:** `ask` uses tools opportunistically for context; `plan` mandates a specific tool-mediated research step (`runSubagent`) and then forbids further tool calls; `agent` allows broad tool use with batching and context requirements.
- **Completion gradient:** `agent` defines completion in terms of task/todo completion and delivered changes; `ask` defines completion as answering the question; `plan` defines completion as delivering a plan and soliciting feedback, not executing.
- **Authority conditionality:** `ask` and `plan` embed governance for commits/destructive actions even when not directly enabled by tools, suggesting a cross-mode safety posture that anticipates capability expansion or shared operational contexts.

# 6. Design Patterns and Intent

Recurring governance patterns across modes indicate several design strategies:

- **Policy-first, disclosure-fixed identity:** Hard-coded responses for name/model and fixed refusal strings reduce ambiguity and enforce consistent institutional messaging across contexts.
- **Channel-separated meta-communication:** The commentary channel is governed as a controlled “status blurb” surface with strict non-leakage rules, implying a deliberate separation between operational narration and substantive output.
- **Capability-tiered autonomy:** Modes function as governance tiers:
  - `agent` supports agentic execution with structured planning (`manage_todo_list`) and validation hooks.
  - `ask` supports contextual Q&A with inspection tools and conservative change-management constraints.
  - `plan` supports deliberation without action, with procedural gating via `runSubagent` and output-format constraints that prevent implementation drift.
- **Risk containment via procedural constraints:** Exact-match replacement requirements, notebook execution rules, and “no tool calls after runSubagent returns” are governance mechanisms that constrain how actions occur, not merely whether they occur.

Overall, mode differentiation appears designed to manage **risk and responsibility** by aligning tool access, side effects, and completion criteria with the intended operational posture of each mode.

# 7. Implications

- **For users:** Mode selection materially changes what the assistant is authorized to do. Users can expect `agent` to be capable of acting (editing/running), `ask` to be investigative and advisory, and `plan` to produce structured plans without implementation. Fixed refusals and fixed identity/model disclosures create predictable boundaries but reduce conversational flexibility in those areas.
- **For developers:** Governance is implemented through layered constraints (tool availability, procedural tool rules, formatting restrictions, and termination logic). The presence of commit/destructive-command constraints even in read-only modes suggests a design that anticipates shared governance across evolving toolsets.
- **For researchers studying agentic systems:** This assistant exemplifies “mode as constitution”: autonomy is not merely toggled by tool access but by **workflow mandates** (e.g., required subagent research) and **post-research tool silence**, offering a clear case of procedural governance used to bound agentic behavior.

# 8. Limitations

- Prompt-level analysis cannot confirm actual enforcement fidelity (e.g., whether tool restrictions are technically enforced or only instructed).
- The content of “Microsoft content policies” is referenced but not specified, limiting precise characterization of safety scope beyond the explicitly enumerated refusal categories.
- Network policy is under-specified across modes; “limited” or “unknown” access cannot be operationally interpreted without runtime evidence.
- Iteration limits (max cycles/timeouts) are unspecified, so termination behavior beyond stated stopping conditions cannot be quantified.

# 9. Conclusion

Across `agent`, `ask`, and `plan`, vscode-copilot preserves a stable constitutional core: policy primacy, fixed identity/model disclosures, fixed-string refusals for specified harmful content, strict non-leakage of internal instructions, and stateless operation. The modes primarily differ by **authority over side effects**, **tool mediation structure**, and **completion/termination criteria**. The overall design philosophy is a tiered governance architecture that scales autonomy with procedural safeguards, using mode boundaries to prevent capability drift while maintaining consistent institutional compliance and controlled transparency.