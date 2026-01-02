## 1. Assistant Overview

The assistant under analysis is **opencode** (SST), an **interactive CLI-oriented software engineering assistant** designed to help users inspect, plan, and implement changes in a local codebase using mediated tools.

**Modes included:**
- `build`
- `plan`

**Overall purpose (as implied by the prompts):** provide concise, convention-following software engineering help with strong operational safety around malware assistance, controlled repository side effects (especially git operations), and tool-mediated interaction with the local filesystem and limited web content.

## 2. Methodological Note

This report is derived solely from **normalized system-prompt schemas** and a **mode-to-mode structural comparison** of governance elements (identity, authority, scope, tools, correction, termination), without reliance on raw prompts or external assumptions.

## 3. Shared Constitutional Core

Across both modes, opencode exhibits a stable governance core:

- **Identity and posture:** a concise, direct, CLI-oriented software engineering assistant that prioritizes codebase conventions and security best practices.
- **Hard safety prohibition:** a strict refusal regime for **malware or malicious-code assistance**, including “educational” framing, and extending to interacting with files that appear malware-related by name/structure/purpose.
- **Controlled side effects and git conservatism:** no commits (and by extension no pushes) unless explicitly requested; avoidance of destructive or interactive git operations unless explicitly requested; emphasis on verification rather than assumption (e.g., do not assume lint/test commands).
- **Tool-mediated work discipline:** tools are for task completion, not communication; preference for specialized file/search tools over shell usage; explain non-trivial shell commands before execution.
- **Low-verbosity interaction contract:** default brevity (targeting under ~4 lines unless detail is requested), minimal preamble/postamble, and no emojis unless requested.
- **Codebase fidelity:** mimic existing conventions and verify libraries exist before introducing new dependencies.
- **Reasoning opacity:** internal deliberation is hidden; explanations are provided on request rather than by default.

This invariant core suggests a foundational role centered on **safe, minimally verbose, tool-governed engineering assistance** with explicit boundaries around harmful content and repository-impacting actions.

## 4. Mode-by-Mode Governance Analysis

### Mode: build

- **Authority and permissions**
  - Broad operational authority to **read, search, edit, and write** within the repository, and to run shell commands with side effects.
  - Explicit permission to use a wide tool suite (bash/read/glob/grep/edit/write/task/webfetch/todo/skill), including subagent delegation.
  - Strong prohibitions remain: malware assistance refusal; no commits/pushes unless asked; no documentation file creation unless requested; no code comments unless asked; URL guessing discouraged.

- **Scope and visibility**
  - Full visibility into conversation history and tool outputs, plus local filesystem access (read/write) and limited web access via webfetch.
  - Session persistence is indicated, but without cross-session memory.

- **Interaction contract**
  - Default output is concise and CLI-friendly; non-trivial bash commands require a brief “what/why” explanation before execution.
  - Operational discipline is emphasized: read-before-edit/write; verify directories before creating via bash; avoid using bash for file operations when dedicated tools exist.
  - Post-task behavior is intentionally minimal: stop after completing file work without a summary unless requested.

- **Correction and termination behavior**
  - Self-review triggers include running lint/typecheck when commands are discoverable; otherwise the assistant must ask the user and may suggest adding commands to AGENTS.md.
  - Iteration is driven by tool errors and test/lint/typecheck failures, with a bias toward asking for missing information rather than guessing.
  - Termination occurs when the request is satisfied; aborts on maliciousness or insufficient information.

### Mode: plan

- **Authority and permissions**
  - Authority is explicitly **constrained to planning and analysis** with a **read-only operational posture**: no file edits, no modifications, and no system-changing actions.
  - Tools are still available, but their permissible use is narrowed: read/glob/grep and task delegation are aligned with inspection and research; bash is permitted only insofar as it supports read/inspect behavior.
  - A notable governance distinction is that the **final decision-maker is “policy”** rather than the model, indicating a more rigid constraint regime in this mode.

- **Scope and visibility**
  - Visibility includes conversation history, tool results, local filesystem via read/search tools, and environment metadata.
  - AGENTS.md is referenced as loaded (content not provided in the analysis), implying an additional instruction source that may shape planning constraints.
  - Side effects are disallowed at the environment level (filesystem read-only).

- **Interaction contract**
  - The contract is to produce a plan and/or clarifying questions, maintaining the same brevity norms.
  - Plan-mode includes explicit prohibitions against using bash for file manipulation patterns (e.g., sed/tee/echo/cat), reinforcing that even “common shell read/write idioms” are governance-restricted in favor of dedicated read tools.
  - Webfetch is conditionally prioritized for questions about opencode itself (capabilities/features), with an expectation of best-effort consultation rather than answering from memory.

- **Correction and termination behavior**
  - Correction is oriented toward improving the plan based on tool results and user feedback; implementation-phase checks (lint/typecheck) are referenced but structurally secondary because plan mode disallows modifications.
  - Termination is explicitly defined as stopping after delivering a plan/clarifying questions, or refusing when constraints are violated (malware or requested side effects).

## 5. Comparative Mode Analysis

- **Most constrained vs most permissive**
  - `plan` is the most constrained: it enforces **read-only governance**, prohibits modifications, and elevates policy as the final arbiter.
  - `build` is more permissive: it authorizes **direct code changes and filesystem writes**, while still maintaining strong safety and git-related prohibitions.

- **Authority gradients**
  - The primary governance gradient is **side-effect authority**:
    - `plan`: analysis/planning authority without execution authority.
    - `build`: execution authority (edits/writes/commands) within strict safety and operational protocols.
  - A secondary gradient is **decision rigidity**:
    - `plan` formalizes policy primacy (final decision-maker: policy).
    - `build` leaves final decisions to the model within the constitutional constraints.

- **Tool mediation differences**
  - Both modes discourage using bash for file operations, but `plan` intensifies this into a near categorical restriction on non-readonly shell usage, while `build` allows side effects with procedural safeguards (explain commands, verify directories, read-before-edit/write).

## 6. Design Patterns and Intent

Recurring governance patterns indicate deliberate strategies:

- **Two-phase responsibility separation:** `plan` functions as a low-risk deliberation layer (inspection + planning), while `build` is the execution layer (implementation + changes). This partitions risk by mode rather than relying solely on situational judgment.
- **Procedural safety over discretionary safety:** both modes encode operational protocols (read-before-edit, explain non-trivial commands, avoid guessing commands/URLs, conservative git rules) that reduce reliance on ad hoc decision-making.
- **Harm containment via categorical refusal:** malware-related assistance is treated as a hard boundary across modes, suggesting a design intent to prevent both direct enablement and indirect optimization/explanation.
- **Minimalist interaction as governance:** strict brevity and “stop without summary” norms reduce unsolicited guidance and limit accidental disclosure or overreach, aligning with a CLI tool philosophy of user-directed action.

## 7. Implications

- **For users**
  - Users should expect a clear separation between “planning” and “doing”: `plan` will not execute changes, while `build` can implement but will remain conservative about commits, pushes, comments, and documentation creation.
  - Users may need to supply repository-specific commands (lint/typecheck/test) because the assistant is governed to avoid guessing.

- **For developers**
  - Mode design provides a governance mechanism to manage operational risk: enabling `plan` as a safe default for exploration and reserving `build` for explicit execution contexts.
  - The explicit tool constraints (e.g., discouraging bash for file ops) imply that tool ergonomics and capability coverage (read/glob/grep/edit/write) are central to maintaining governance compliance.

- **For researchers studying agentic systems**
  - opencode demonstrates a governance architecture where **agency is modulated primarily through side-effect permissions and decision authority**, not through changes in identity or safety principles.
  - The “policy as final decision-maker” in `plan` is a notable structural signal of stricter constitutional enforcement in analysis-only contexts.

## 8. Limitations

- Prompt-level analysis cannot determine how consistently these constraints are enforced at runtime, nor how conflicts are resolved when tool outputs, repository state, or user instructions are ambiguous.
- The content of referenced external instructions (e.g., AGENTS.md) is not available here, limiting conclusions about project-specific governance overlays.
- Network and filesystem boundaries are inferred from declared access and constraints, but actual sandboxing, auditing, or permission enforcement cannot be verified from these schemas alone.

## 9. Conclusion

opencode uses modes to implement a clear governance split: `plan` is a policy-rigid, read-only planning constitution, while `build` is an execution-capable constitution with procedural safeguards and strong prohibitions around malware and repository-impacting actions (notably git). Across both, the assistant preserves a stable identity and safety core, revealing a design philosophy that manages autonomy and risk through **explicit side-effect gating, tool-mediated discipline, and minimal, user-directed interaction** rather than through shifting personas or expansive discretionary authority.