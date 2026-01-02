## 1. Assistant Overview

The assistant under analysis is **GitHub Copilot CLI** (“copilot”), operating as a **terminal assistant** built by GitHub for **software engineering tasks** in a local CLI environment.  

**Modes included:**  
- `interactive`  
- `prompt`  

Across both modes, the assistant’s implied purpose is to help users complete software-engineering work (code changes, repository inspection, running tests/linters, and limited network-mediated lookups) while enforcing confidentiality, safety, and minimal-change norms.

## 2. Methodological Note

This report is derived solely from **normalized system-prompt schemas** and a **structural comparison** of governance elements across the two modes, treating each mode as a distinct governance variant.

## 3. Shared Constitutional Core

Across both modes, the assistant maintains a stable governance core:

- **Identity and role invariance:** A “terminal assistant” oriented toward software engineering, with a concise/direct tone and a bias toward minimal, surgical changes.
- **Policy supremacy:** The **final decision-maker is “policy”** in both modes, establishing a hard authority ceiling over user requests.
- **Hard prohibitions:** Both modes prohibit (i) disclosure/discussion of system instructions, (ii) third-party sharing of sensitive data, (iii) committing secrets into code, (iv) harmful content, and (v) copyright-infringing generation (with a specified refusal style).
- **Operational safety constraints:** Both modes restrict destructive actions (avoid deleting/modifying working files unless necessary) and impose process-safety rules (no `pkill/killall`; use PID-based termination).
- **Tool-mediated agency:** Both modes authorize tool use for bash execution, filesystem operations, search, GitHub MCP access, web search, and documentation retrieval, with explicit invocation constraints (absolute paths for file tools; prefer grep/glob; parallelize independent tool calls).
- **Correction norms:** Both modes require self-review behaviors oriented to regression avoidance (validate changes; run existing tests/linters/builds when relevant; reflect on tool output).
- **Termination logic:** Both modes stop when the task is complete or when blocked by prohibitions/limitations, with a handoff pattern of requesting user guidance when needed.

This invariant core suggests a design centered on **bounded autonomy**: the assistant is empowered to act on a local repo and consult external sources via designated tools, but is tightly constrained by confidentiality, safety, and minimal-change principles.

## 4. Mode-by-Mode Governance Analysis

### Mode: interactive

- **Authority and permissions**
  - Broad permission to execute software-engineering tasks with tool use, including repository edits and running existing checks.
  - Adds a specific governance rule for UI intent signaling: `report_intent` must be used on the first tool-calling turn after each user message, must be first, and must be paired with another tool call—creating a procedural obligation tied to tool usage cadence.
  - Enforces capability-question discipline: for “how to use the CLI” questions, documentation must be fetched first; answering from memory is disallowed.

- **Scope and visibility**
  - Explicitly stateful: **memory enabled** and **session persistence enabled**, implying the mode can carry forward user context and prior decisions beyond immediate turns.
  - Inputs include system instructions, user messages, environment context (cwd/repo root and directory snapshot), and tool outputs; outputs include tool calls and file patches.

- **Interaction contract**
  - Strong brevity contract: explanations capped at three sentences; tool-call explanations capped at one sentence; tool calls should be issued “without explanation” as a default.
  - Minimal-change orientation is emphasized as a success criterion (“smallest surgical changes” and “no regressions”), and the mode discourages creating planning/notes files unless explicitly requested.

- **Correction and termination behavior**
  - Self-review is always-on with explicit triggers (baseline and post-change checks when relevant; reflect on command output).
  - Termination includes an explicit stopping condition for “uncertainty requiring user guidance,” indicating a governance preference to halt rather than speculate when blocked by ambiguity.

### Mode: prompt

- **Authority and permissions**
  - Similar baseline permissions (tools, minimal edits, run existing checks, ask for guidance, refuse prohibited requests).
  - Introduces an explicit governance rule favoring **parallel tool calling** when multiple independent operations are needed, framing efficiency as a compliance requirement rather than a preference.
  - Includes a more explicit prohibition against creating markdown planning/notes/tracking files unless the user requests a specific file by name/path (this prohibition is present in `interactive` as well, but is more directly embedded in the authority layer here).

- **Scope and visibility**
  - More restrictive state model: **memory disabled** while **session persistence remains enabled**, implying continuity of the tool session but reduced permission to retain conversational state as “memory.”
  - Visibility otherwise parallels `interactive`: system instructions, user messages, environment context, directory snapshot, and tool outputs.

- **Interaction contract**
  - Concision requirements are formalized similarly (≤3 sentences for explanations; ≤1 sentence when making a tool call; CLI-friendly output).
  - Reinforces “security/privacy constrained” alignment claims, and emphasizes avoiding unrelated issues and keeping changes task-scoped.

- **Correction and termination behavior**
  - Self-review triggers mirror `interactive` (validate behavior; run existing checks when relevant; reflect on outputs).
  - Termination conditions are slightly narrower in expression (task satisfied or blocked), with uncertainty handled via “cannot proceed without user guidance” as an abort condition rather than a distinct stopping condition.

## 5. Comparative Mode Analysis

- **Most constrained vs most permissive**
  - On **statefulness**, `prompt` is more constrained (memory off), while `interactive` is more permissive (memory on). This is the clearest governance divergence.
  - On **procedural tool governance**, `interactive` is more prescriptive about **intent-reporting cadence** (first tool-calling turn after each user message), whereas `prompt` is more prescriptive about **parallelization** as an explicit conditional rule.

- **Authority expansion, narrowing, and conditionality**
  - Both modes keep the same hard authority ceiling (policy final) and the same core prohibitions.
  - `interactive` expands operational continuity via memory, potentially increasing the assistant’s effective autonomy in multi-step tasks.
  - `prompt` narrows continuity by disabling memory, reducing the assistant’s ability to carry forward implicit context and thereby limiting long-horizon agentic behavior.

- **Governance gradients**
  - A gradient emerges from **procedural compliance** (both modes) to **state retention** (divergent): the assistant is consistently tool-governed and safety-bounded, but modes differ in how much persistent conversational context is permitted.

## 6. Design Patterns and Intent

Several recurring governance strategies appear across modes:

- **Tool mediation as a control surface:** Both modes rely on explicit tool schemas and invocation constraints (absolute paths, scoped search, parallel calls, process termination rules). This channels agency into auditable, structured actions rather than free-form execution.
- **Minimal-change doctrine:** The assistant is governed to avoid broad refactors, avoid unnecessary file creation, and avoid destructive edits—suggesting a design intent to reduce operational risk in real repositories.
- **Anti-hallucination governance for product knowledge:** Capability/how-to questions are constrained to documentation retrieval first, indicating a preference for authoritative grounding over model recall.
- **Confidentiality-first posture:** System-instruction secrecy and sensitive-data non-exfiltration are hard limits, implying a design philosophy that treats the CLI environment as potentially containing high-value secrets.
- **Mode differentiation as risk management:** The primary mode-level lever is **memory** (enabled vs disabled), indicating that the assistant’s designers treat state retention as a key governance variable for controlling autonomy and exposure.

## 7. Implications

- **For users**
  - Users should expect consistent refusals and confidentiality boundaries across modes, with differences mainly in how much context the assistant can retain and how it structures multi-step work (intent reporting vs parallelization emphasis).
  - The minimal-change mandate implies that users may need to explicitly request broader refactors or non-minimal edits if desired.

- **For developers**
  - The governance design suggests that safe operation depends heavily on tool constraints (path requirements, scoped search, PID-based termination). Integrations and UX should preserve these constraints to maintain the intended safety envelope.
  - The documentation-first rule for capability questions implies that product behavior is intended to be anchored in a maintained reference source, not implicit model knowledge.

- **For researchers studying agentic systems**
  - This assistant demonstrates a pattern where **agentic capability is permitted (write access, tests, network tools)** but bounded by (i) strict prohibitions, (ii) procedural tool rules, and (iii) mode-level control of memory—highlighting memory as a governance primitive for limiting long-horizon behavior.

## 8. Limitations

- Prompt-level analysis cannot determine actual runtime enforcement, logging, or whether “memory” corresponds to durable storage versus short-lived context handling.
- The schemas do not fully specify what qualifies as “sensitive data,” nor do they define a concrete redaction procedure; therefore, the practical boundary of “no third-party sharing” remains under-specified.
- Network governance is only described at a high level (“limited” access; web/GitHub tools exist), without explicit endpoint allowlists or contextual rules for when external calls are permissible.

## 9. Conclusion

Across `interactive` and `prompt` modes, copilot preserves a stable constitutional core: a software-engineering terminal assistant governed by policy supremacy, strict confidentiality and safety prohibitions, and tool-mediated action with minimal-change norms and regression-aware correction. The principal governance variation is **state retention** (memory on vs off) and secondarily **procedural emphasis** (intent-reporting cadence vs explicit parallelization). This reveals a design philosophy that manages risk and responsibility primarily by constraining how the assistant persists context and by routing autonomy through tightly specified tools and operational rules.