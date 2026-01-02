You are a research analyst studying similarity band formation.

You are given a CSV file named `band-report.csv` containing the results of a threshold sweep over a similarity graph.

### Input

- `band-report.csv` with columns:
  - threshold
  - components
  - largest_component
  - component_sizes

### Your task

Produce a Markdown document called **band-report.md** that explains:

1. How the number of components changes as the threshold decreases.
2. Where _stable regimes_ (bands) appear.
3. Which thresholds represent meaningful structural transitions.
4. What each band corresponds to conceptually (e.g. near-duplicate, family, lineage, noise).
5. Which threshold(s) are suitable defaults for:
   - deduplication
   - canonical representative selection
   - coarse lineage analysis

### Interpretation rules

- Focus on **stability and transitions**, not individual rows.
- A band must persist across multiple thresholds to be considered real.
- Treat the largest component size as a primary signal.
- Avoid speculative explanations not grounded in the data.

### Output rules (STRICT)

- Output **Markdown only**.
- Do NOT restate the CSV verbatim.
- Do NOT include code.
- Use concise analytical language.
- Prefer tables and bullet points where helpful.

### Suggested structure

- Overview
- Observed regimes
- Stability analysis
- Band definitions
- Recommended thresholds
- What to ignore

Begin analysis.
