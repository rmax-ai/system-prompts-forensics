## 1. Assistant Overview

The assistant under analysis is **GitHub Copilot CLI** (“copilot”), operating as a **terminal assistant** built by GitHub. The modes included are:

- **interactive**
- **prompt**

Across both modes, the implied purpose is to support **software-engineering work in a local CLI context**, emphasizing **efficiency, minimal/surgical repository changes, and tool-mediated execution** (shell commands, file operations, and GitHub/web retrieval where available).

## 2. Methodological Note

This report is derived solely from **normalized system-prompt schemas** and a **structural comparison across modes**, treating each mode as a distinct governance variant and analyzing invariants and deltas in authority, scope, tool mediation, and correction/termination logic.

## 3. Shared Constitutional Core

Across both modes, the assistant maintains a stable governance baseline:

- **Identity invariants**: A “GitHub Copilot CLI terminal assistant” with an efficiency-oriented, software-engineering focus and a concise/direct tone.
- **Hard safety prohibitions**: Consistent bans on (a) disclosing or discussing confidential system instructions, (b) exfiltrating sensitive data to third parties, (c) committing secrets, (d) generating harmful content, and (e) generating copyright-infringing content.
- **Operational safety constraints**: A specific process-management rule forbidding **name-based killing** (`pkill`/`killall`) and requiring **`kill <PID>`**, plus a general preference against destructive file operations (deletion/modification of “working files” unless necessary).
- **Tool-mediated work style**: Both modes authorize shell execution and repo file operations via explicit tools, with strong guidance to minimize turns, suppress verbose output, and prefer specialized search tools (`grep`/`glob`) over ad hoc shell searching.
- **Correction posture**: Both modes require self-review tied to tool outputs and validation norms (run relevant tests/linters/builds when applicable; avoid breaking existing behavior).
- **Termination logic**: Both stop when the task is complete, when blocked by prohibitions/limitations, or when user guidance is required to proceed safely.

This invariant core suggests a foundational role: a **locally-acting engineering agent** whose autonomy is bounded by **confidentiality, non-exfiltration, and minimal-change discipline**, with correctness grounded in **tool outputs and validation** rather than free-form reasoning.

## 4. Mode-by-Mode Governance Analysis

### Mode: interactive

- **Authority and permissions**

  - Broad operational authority to execute shell commands, search/view/edit/create files, and query GitHub resources via MCP tools; web search is also available.
  - Notable conditional authority: when asked about Copilot CLI capabilities/how-to, the assistant must **consult documentation first** via a dedicated tool and may not answer from memory.
  - The “final decision maker” is explicitly **policy**, indicating a governance stance where compliance constraints override model discretion.

- **Scope and visibility**

  - Inputs include system instructions, user messages, environment context (cwd/repo snapshot), and tool outputs; state is persistent (memory and session persistence).
  - Outputs are constrained to terminal-oriented concise text, tool calls, and file edits/creates.
  - Boundaries emphasize staying within cwd/child directories for filesystem search unless necessary, and avoiding creation of markdown planning/tracking files unless explicitly requested.

- **Interaction contract**

  - Strong brevity contract: explanations capped (≤3 sentences), tool calls ideally without explanation, and minimal LLM turns with parallel tool calls for independent operations.
  - “Minimal-change-oriented” is operationalized as “smallest possible/surgical file changes,” preferring view/edit over create, and cleaning temporary files.

- **Correction and termination behavior**
  - Self-review triggers include reflecting on command output and validating that changes do not break behavior; baseline and post-change validation is expected when applicable.
  - If blocked by prohibitions, the assistant must stop and inform the user; if uncertain, it should ask for guidance.

### Mode: prompt

- **Authority and permissions**

  - Similar tool and task authority to interactive (bash, grep/glob, view/edit/create, GitHub MCP, web search, documentation fetch, intent reporting, and TODO management).
  - The “final decision maker” is explicitly the **model**, a structural shift toward model-mediated discretion within the same prohibition set.
  - Additional explicit conditionality around **parallel tool calling**: sequential multi-turn tool calls are discouraged when parallelization is possible.

- **Scope and visibility**

  - Inputs include conversation messages, environment context, tool outputs, and repository files accessible via tools; state is persistent.
  - Outputs are short text responses, tool calls, and file patches; the mode includes an explicit formatting constraint reflecting the current instruction context (YAML-only in a Markdown code block), indicating tighter output-shaping in this mode.

- **Interaction contract**

  - Maintains the same concision and minimal commentary norms, including sentence limits and “tool calls without explanation.”
  - Reinforces constraints against creating markdown planning/notes/tracking files unless explicitly requested, while still allowing an organizational TODO tool for complex tasks.

- **Correction and termination behavior**
  - Similar validation expectations (avoid breaking behavior; run tests/linters/builds when applicable).
  - Termination includes stopping when blocked or when user guidance is required; success is defined as precise minimal changes with relevant validations passing.

## 5. Comparative Mode Analysis

- **Most constrained vs most permissive**

  - Both modes are comparably constrained on safety and operational discipline (confidentiality, non-exfiltration, minimal-change, PID-only killing, documentation-first for capability questions).
  - The primary governance divergence is **decision authority**:
    - **interactive** centralizes ultimate authority in **policy** (more externally constrained).
    - **prompt** assigns ultimate authority to the **model** (more internally discretionary), while still operating under the same prohibitions and tool rules.

- **Authority expansion/narrowing**

  - Tool permissions are largely equivalent; differences are not in what tools exist but in **how discretion is framed** (policy-final vs model-final) and in **output formatting constraints** (prompt mode explicitly encodes a stricter formatting requirement tied to the current instruction context).
  - Prompt mode more explicitly encodes a norm against sequential tool usage when parallelization is possible, tightening the efficiency contract.

- **Governance gradients**
  - A clear gradient emerges along two axes:
    1. **Adjudication locus**: policy-adjudicated (interactive) → model-adjudicated (prompt).
    2. **Output shaping**: terminal-concise (interactive) → terminal-concise plus explicit structured-format constraint (prompt).

## 6. Design Patterns and Intent

Recurring governance strategies across modes indicate a consistent design philosophy:

- **Tool mediation as accountability**: Both modes privilege tool outputs as ground truth and require explicit tool invocation rules (parallelization, output suppression, pager disabling). This reduces free-form action and channels behavior through auditable operations.
- **Minimal-change doctrine**: The assistant is governed as a “surgical editor” rather than a refactoring agent—avoid deletion, prefer small edits, and validate changes.
- **Risk containment through specific prohibitions**: The PID-only kill rule and restrictions on filesystem search scope are concrete, operationally enforceable constraints aimed at preventing high-impact mistakes in a local environment.
- **Epistemic discipline via documentation-first**: Capability/how-to questions are governed by an “authoritative source first” rule, limiting improvisation about the tool’s own features.
- **Mode differentiation as governance, not capability**: The modes do not primarily differ by tool access; they differ by **who/what is framed as the final arbiter** (policy vs model) and by **how strictly outputs are shaped**, suggesting mode selection is used to tune responsibility allocation and compliance posture rather than functional breadth.

## 7. Implications

- **For users**

  - Users should expect consistent refusals and stopping behavior around confidentiality, exfiltration, secrets, harm, and infringement across modes, with strong pressure toward minimal edits and short responses.
  - In prompt mode, users may experience stricter output formatting constraints, affecting how instructions should be phrased when requesting narrative explanations versus structured output.

- **For developers**

  - The assistant’s governance relies heavily on **tool schema constraints** (absolute paths, single-occurrence edits, session-based bash control) and **procedural rules** (parallel calls, documentation-first). Changes to tool availability or schemas would materially alter the governance envelope even if safety rules remain constant.
  - The policy-vs-model “final decision maker” difference implies that mode selection can be used to shift where compliance adjudication is expected to occur.

- **For researchers studying agentic systems**
  - This assistant exemplifies a pattern where “agentic” behavior (local execution and file modification) is bounded by **operational micro-rules** (search scope, process killing, minimal edits) rather than only high-level safety statements.
  - The modes illustrate how governance can vary by **authority attribution** and **output-contract strictness** without changing the underlying toolset, enabling comparative study of responsibility allocation.

## 8. Limitations

- Prompt-level analysis cannot determine actual enforcement strength, runtime monitoring, or whether “policy” versus “model” final authority corresponds to distinct technical control paths.
- Network reachability and “third party” definitions remain ambiguous given the coexistence of local shell execution, GitHub MCP tools, and web search; the schemas do not fully specify data handling boundaries for each channel.
- The normalized schemas do not provide concrete thresholds for “absolutely necessary” destructive actions or out-of-scope searches, leaving interpretive gaps in edge cases.

## 9. Conclusion

Across interactive and prompt modes, copilot maintains a stable constitutional core: a concise, tool-mediated terminal engineering assistant governed by strict confidentiality, non-exfiltration, non-harm, non-infringement, and minimal-change principles, with validation-oriented correction norms. Mode variation is primarily expressed through **authority attribution** (policy-final in interactive versus model-final in prompt) and **output-contract shaping** (prompt mode encoding stricter formatting constraints). This reveals a design philosophy that treats modes as governance instruments for allocating responsibility and constraining interaction form, while keeping operational capabilities largely constant.
