#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
final-research-report.py

Generate the final cross-assistant comparative research report from:
- per-assistant final reports (final-report-*.md)
- research goal document (goal.md)

Output:
  final-research-report.md

Usage:
  uv run --locked data/scripts/final-research-report.py \
    --prompt data/prompts/final-research-report.prompt.md \
    --assistants data/final-report-*.md \
    --goal goal.md \
    --model gpt-5.2

Options:
  --dry-run   Print the assembled request and exit without calling the API
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

import openai


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        sys.exit(f"Failed to read {path}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate final comparative research report"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Final research report prompt (Markdown)",
    )
    parser.add_argument(
        "--assistants",
        required=True,
        nargs="+",
        help="Per-assistant final reports (final-report-*.md)",
    )
    parser.add_argument(
        "--goal",
        required=True,
        help="Research goal document (goal.md)",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2)",
    )
    parser.add_argument(
        "--output",
        default="final-research-report.md",
        help="Output path (default: final-research-report.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling the API",
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
    goal_text = read_text(Path(args.goal))

    assistant_paths = [Path(p) for p in args.assistants]
    assistant_blocks: List[str] = []

    for path in sorted(assistant_paths):
        assistant_blocks.append(
            f"## Assistant Report: {path.stem}\n\n{read_text(path)}"
        )

    messages = [
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": f"""## Research Goals

{goal_text}
""",
        },
        {
            "role": "user",
            "content": f"""## Per-Assistant Final Reports

{'\n\n'.join(assistant_blocks)}
""",
        },
    ]

    if args.dry_run:
        print("=== DRY RUN MODE ===\n")
        print(f"Model: {args.model}\n")
        for msg in messages:
            print(f"[{msg['role']}]\n{msg['content']}\n")
        return

    client = openai.OpenAI()

    logging.info("Calling model to generate final research report...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0,
        )
    except Exception as e:
        sys.exit(f"API call failed: {e}")

    output = response.choices[0].message.content
    if not output:
        sys.exit("Model returned empty output")

    out_path = Path(args.output)
    try:
        out_path.write_text(output.strip(), encoding="utf-8")
        logging.info(f"Wrote final report to {out_path}")
    except Exception as e:
        sys.exit(f"Failed to write output file: {e}")


if __name__ == "__main__":
    main()
