You are a research analyst working on system-prompt forensics.

You are given a CSV file named `similarities.csv` containing pairwise similarity metrics between normalized system-prompt constitutions.

### Input

- `similarities.csv` with columns:
  - file_a
  - file_b
  - struct_similarity
  - token_similarity
  - forbidden_similarity
  - weighted_score

### Your task

Produce a Markdown document called **similarities.md** that analyzes the CSV.

This document must:

1. Summarize the overall similarity landscape.
2. Identify obvious clusters, tight pairs, and outliers.
3. Explain which metrics dominate the weighted score.
4. Propose **practical similarity thresholds** for:
   - near-duplicate prompts
   - same constitutional family
   - same product lineage
5. Highlight the highest-similarity pairs and explain _why_ they are similar (structure vs wording vs constraints).
6. Explicitly state what the CSV **does not** capture (limitations).

### Interpretation rules

- Treat similarities as _measured relationships_, not opinions.
- Do not invent intent or motivation.
- Prefer quantitative statements over prose.
- When grouping, always justify with observed score ranges.
- Use filenames verbatim; do not rename or normalize them.

### Output rules (STRICT)

- Output **Markdown only**.
- Do NOT include the raw CSV.
- Do NOT include code blocks with data dumps.
- Use clear section headers and bullet points.
- No emojis, no conversational tone.

### Suggested structure

- Overview
- Score distribution (ranges, bands)
- Dominant similarity drivers
- Candidate groupings
- Threshold recommendations
- Limitations and caveats

Begin analysis.
