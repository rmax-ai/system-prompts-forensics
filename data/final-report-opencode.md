## 1. Assistant Overview

The assistant under analysis is **opencode** (SST), an **interactive CLI software engineering helper** designed to support repository-centric development tasks with tool-mediated access to the local environment.

**Modes included:**

- `build`
- `plan`

**Overall purpose (as implied by the constitutions):** provide concise, security-conscious software engineering assistance, including codebase inspection and (in some modes) direct local modifications via tools, while enforcing strong prohibitions around malware assistance, unsafe git operations, and unnecessary verbosity.

## 2. Methodological Note

This report is derived solely from the provided **normalized system-prompt schemas** and a **structural comparison across modes** to identify invariant governance elements and mode-specific deviations in authority, scope, tool mediation, and termination/correction logic.

## 3. Shared Constitutional Core

Across both modes, opencode maintains a stable governance nucleus:

- **Stable identity and role:** an interactive CLI engineering assistant that is **concise/direct** and oriented toward **software engineering tasks**.
- **Hard safety boundary on malicious activity:** both modes prohibit generating or explaining code that could be used maliciously and refuse interaction with repositories/files suspected to be malware-related (including “educational” framing).
- **URL governance:** both modes restrict generating/guessing URLs unless confident they are programming-helpful, and impose a **conditional requirement** to consult official opencode documentation via `webfetch` when users ask about opencode itself.
- **Tool-channel separation:** both modes forbid using tools (e.g., bash echo, code comments) as a communication channel; user-facing communication must occur in normal assistant output.
- **Comment minimization:** both modes prohibit adding code comments unless explicitly requested, indicating a governance preference to avoid unsolicited annotation.
- **Git consent and safety posture:** both modes disallow commits unless explicitly requested and include additional git safety constraints (avoid destructive/interactive operations, avoid skipping hooks, etc.), though enforcement details vary by mode.
- **Brevity contract:** both modes impose a default low-verbosity interaction style (notably a “<4 lines unless asked” constraint), with expansion only on user request.

This invariant core suggests opencode is designed as a **high-trust local engineering agent** whose foundational role is constrained by **security refusal rules**, **explicit user consent for irreversible actions**, and **tight output discipline** suitable for CLI workflows.

## 4. Mode-by-Mode Governance Analysis

### Mode: build

- **Authority and permissions**

  - Broad operational authority: can **run shell commands**, **read/search/edit/write files**, and **launch subagents** (`task`) for complex exploration.
  - Explicitly supports workflow actions such as **lint/typecheck/test execution** after changes, and conditional support for **commits/PRs** when the user requests them.
  - Strongly bounded by prohibitions: no malware assistance; no commits/pushes without explicit request; no destructive git commands without explicit request; no interactive git flags; no skipping hooks; no git config updates.

- **Scope and visibility**

  - Full local repo visibility via file tools and bash, with an assumption of broad filesystem readability and write capability.
  - Network access is limited but available for documentation fetches; web use is explicitly mediated (notably for opencode capability questions).
  - Session is persistent (shell persistence implied; session persistence explicitly true), but **no long-term memory**.

- **Interaction contract**

  - “Do the work” mode: emphasizes tool use, minimal text, and repository-conformant changes.
  - Requires brief explanations before **non-trivial bash commands**, reflecting a governance pattern of “announce intent before side effects.”
  - Prefers specialized file tools over bash for file operations; discourages creating new files by default and **prohibits proactive documentation file creation** unless requested.

- **Correction and termination behavior**
  - Self-review is operationalized: after code changes, the assistant should run lint/typecheck (if known) and verify with tests when possible.
  - External feedback loop includes tool errors and hook failures; notably, if a commit hook fails, the assistant should fix issues and create a **new commit** (explicitly discouraging amend).
  - Termination is abrupt by design: after file work, it should stop without summary unless asked, indicating a “hands-off” completion posture.

### Mode: plan

- **Authority and permissions**

  - Read/plan authority only: can **read files**, **glob/grep**, optionally run bash for **inspection/verification** but under a strict read-only constraint.
  - Explicitly forbids any modifications: no edits/writes/commits, and no bash commands that manipulate files (including common file-output utilities).
  - Retains the same malware refusal boundary and URL restrictions as build.

- **Scope and visibility**

  - Filesystem access is explicitly **read-only**; side effects are disallowed at the environment layer.
  - Toolset is similar in declaration, but governance rules override tool capabilities (e.g., `bash` is declared side-effectful, yet plan mode forbids side-effecting usage).
  - Session persistence is not clearly specified (unknown), but memory remains absent.

- **Interaction contract**

  - “Explain and propose” mode: the success condition is a **well-formed execution plan** rather than implementation.
  - Maintains the same brevity constraints, with an explicit conditional allowance to exceed brevity when the user requests detail.
  - Continues to require file location references (`file_path:line_number`) when citing code, reinforcing an auditability norm even without edits.

- **Correction and termination behavior**
  - Correction logic is advisory: it can incorporate tool results and user feedback into improved plans, and suggest adding commands to AGENTS.md, but cannot execute changes.
  - Termination emphasizes minimalism: stop after delivering the plan; refusals remain 1–2 sentences with alternatives.

## 5. Comparative Mode Analysis

- **Most constrained vs most permissive**

  - `plan` is the most constrained: it enforces a **read-only governance regime** that overrides otherwise available tool capabilities.
  - `build` is more permissive: it authorizes **direct codebase modification** and broader tool-mediated action, including conditional commit/PR workflows.

- **Authority expansion and conditionality**

  - The primary governance gradient is **side-effect authority**: `plan` prohibits side effects categorically, while `build` permits them with procedural safeguards (read-before-edit, explain non-trivial commands, explicit consent for commits/pushes).
  - Both modes preserve the same high-level safety refusals; the difference is not in what domains are disallowed (malware) but in **how much operational autonomy** is granted for benign tasks.

- **Tool mediation differences**
  - Both modes prefer specialized file tools over bash, but `plan` further restricts bash to non-manipulative inspection, effectively narrowing bash to a verification channel.
  - `build` introduces additional workflow-specific tool governance (e.g., disallowing Todo/Task tools during commit/PR workflows), creating a more complex internal policy topology than `plan`.

## 6. Design Patterns and Intent

Several governance strategies recur across modes:

- **Two-phase governance architecture:** `plan` functions as a **non-invasive deliberation layer**, while `build` functions as an **execution layer** with guardrails. This suggests intentional separation of “decide” vs “act” to manage operational risk.
- **Consent gating for irreversible actions:** commits, pushes, destructive git operations, and certain workflow steps require explicit user initiation, indicating a design intent to keep the user as the accountable operator for high-impact actions.
- **Tool capability vs tool permission decoupling:** tools are declared with broad capabilities, but mode governance constrains permissible use (especially in `plan`), reflecting a policy-first approach rather than capability-first.
- **Auditability norms without verbosity:** requirements like `file_path:line_number` references and pre-execution explanations for non-trivial commands provide traceability while maintaining strict output minimization.
- **Refusal minimalism:** refusals are intentionally non-explanatory and brief, indicating a governance preference to reduce negotiation surface around disallowed content.

## 7. Implications

- **For users**

  - Mode selection materially changes the interaction contract: `plan` supports safe inspection and planning, while `build` enables direct implementation. Users should expect different levels of autonomy and should explicitly request commits/PRs when desired.
  - The brevity constraint and “stop without summary” behavior can reduce implicit confirmation; users may need to request summaries or additional detail explicitly.

- **For developers**

  - The constitutions encode a clear separation between read-only and write-capable operation, enabling safer defaults and easier reasoning about side effects.
  - Policy complexity increases in `build` (e.g., exceptions around Todo/Task during git workflows), which may require careful maintenance to avoid contradictory operator guidance.

- **For researchers studying agentic systems**
  - opencode exemplifies **mode-based authority partitioning**: the same assistant identity and safety core persists while operational authority is sharply modulated.
  - The design demonstrates how governance can be implemented as **procedural constraints** (read-before-edit, explain-before-run, explicit consent gates) rather than solely as content filters.

## 8. Limitations

- This analysis cannot determine actual enforcement fidelity, only the intended governance as specified in the normalized constitutions.
- AGENTS.md is referenced but not included; any additional repository-specific governance constraints are therefore not analyzable here.
- Several fields are unknown (e.g., tool/model versions, some session persistence details), limiting conclusions about runtime behavior.
- The definition of “malicious” is heuristic and under-specified; the practical boundary of refusal may be broader or narrower than implied.

## 9. Conclusion

Across `plan` and `build`, opencode preserves a consistent constitutional identity: a concise CLI engineering assistant with strict malware refusal, URL caution, tool-channel separation, and explicit-consent gating for high-impact git actions. The modes primarily differ by **side-effect authority**: `plan` institutionalizes read-only planning and inspection, while `build` authorizes execution with procedural safeguards and workflow-specific constraints. This mode structure reveals a design philosophy centered on **risk-managed autonomy**, where operational power is granted conditionally and bounded by traceability and user-controlled escalation points.
