#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
final-comparative-analysis.py

Generate the final comparative analysis report from a curated evidence bundle.

Usage:
  uv run --locked scripts/final-comparative-analysis.py \
    --prompt prompts/final-comparative-analysis.prompt.md \
    --analysis-dir data/analysis \
    --similarities data/similarities.csv \
    --bands data/band-report.csv \
    --families data/prompt-families.csv \
    --family-report data/prompt-families-report.md \
    --methodology methodology.md \
    --goal goal.md \
    --model gpt-5.2 \
    --output final-report.md
"""

import argparse
import logging
import sys
from pathlib import Path

import openai


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def read_analysis_dir(path: Path) -> str:
    if not path.exists() or not path.is_dir():
        sys.exit(f"Analysis directory not found: {path}")

    files = sorted(path.glob("*.analysis.yaml"))
    if not files:
        sys.exit(f"No .analysis.yaml files found in {path}")

    blocks = []
    for f in files:
        blocks.append(f"### {f.name}\n\n```yaml\n{read_text(f)}\n```")
    return "\n\n".join(blocks)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate final comparative analysis report for system prompt governance"
    )
    parser.add_argument(
        "--prompt", required=True, help="Final analysis prompt (Markdown)"
    )
    parser.add_argument(
        "--analysis-dir", required=True, help="Directory with *.analysis.yaml files"
    )
    parser.add_argument("--similarities", required=True, help="similarities.csv")
    parser.add_argument("--bands", required=True, help="band-report.csv")
    parser.add_argument("--families", required=True, help="prompt-families.csv")
    parser.add_argument(
        "--family-report", required=True, help="prompt-families-report.md"
    )
    parser.add_argument("--methodology", required=True, help="methodology.md")
    parser.add_argument("--goal", required=True, help="goal.md")
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2)",
    )
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output",
        help="Output report file (prints to stdout if omitted)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print request payload and exit without calling the API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    prompt_text = read_text(Path(args.prompt))
    analysis_block = read_analysis_dir(Path(args.analysis_dir))
    similarities_csv = read_text(Path(args.similarities))
    bands_csv = read_text(Path(args.bands))
    families_csv = read_text(Path(args.families))
    family_report = read_text(Path(args.family_report))
    methodology_md = read_text(Path(args.methodology))
    goal_md = read_text(Path(args.goal))

    messages = [
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": f"""## Research Goal

{goal_md}""",
        },
        {
            "role": "user",
            "content": f"""## Methodology

{methodology_md}""",
        },
        {
            "role": "user",
            "content": f"""## Normalized System Prompt Analyses

{analysis_block}""",
        },
        {
            "role": "user",
            "content": f"""## Similarities

```csv
{similarities_csv}
```""",
        },
        {
            "role": "user",
            "content": f"""## Band Report

```csv
{bands_csv}
```""",
        },
        {
            "role": "user",
            "content": f"""## Prompt Families

```csv
{families_csv}
```""",
        },
        {
            "role": "user",
            "content": f"""## Prompt Family Interpretation

{family_report}""",
        },
    ]

    if args.dry_run:
        print("Dry run — request payload:")
        print(f"Model: {args.model}")
        if args.seed is not None:
            print(f"Seed: {args.seed}")
        for m in messages:
            print(f"\n[{m['role']}]\n{m['content']}")
        return

    client = openai.OpenAI()

    logging.info(f"Calling model {args.model} for final comparative analysis...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0.1,
            seed=args.seed,
        )
    except Exception:
        logging.exception("API call failed")
        sys.exit(1)

    output = response.choices[0].message.content
    if not output:
        sys.exit("Model returned empty output")

    if args.output:
        out = Path(args.output)
        try:
            out.write_text(output.strip(), encoding="utf-8")
            logging.info(f"Final report written to {out}")
        except Exception:
            logging.exception("Failed to write output file")
            sys.exit(1)
    else:
        print(output.strip())


if __name__ == "__main__":
    main()
