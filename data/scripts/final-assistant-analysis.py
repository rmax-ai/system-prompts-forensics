#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
final-assistant-analysis.py

Generate per-assistant final governance reports from normalized analysis files.

Each assistant is inferred from filenames of the form:
  assistant.mode.analysis.yaml

Outputs:
  data/final-report-<assistant>.md

Usage:
  python data/scripts/final-assistant-analysis.py \
    --prompt data/prompts/final-assistant-analysis.prompt.md \
    --analysis-dir data/analysis \
    --model gpt-5.2
"""

import argparse
import logging
import sys
from collections import defaultdict
from pathlib import Path

import openai


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def parse_assistant_and_mode(filename: str) -> tuple[str, str]:
    # assistant.mode.analysis.yaml
    parts = filename.split(".")
    if len(parts) < 3:
        sys.exit(f"Unexpected analysis filename format: {filename}")
    assistant = parts[0]
    mode = parts[1]
    return assistant, mode


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate per-assistant final governance analysis reports"
    )
    parser.add_argument("--prompt", required=True, help="Per-assistant analysis prompt")
    parser.add_argument("--analysis-dir", required=True, help="Directory with *.analysis.yaml")
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2)",
    )
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory for final-report-<assistant>.md (default: data/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print request payloads without calling the API",
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
    analysis_dir = Path(args.analysis_dir)

    files = sorted(analysis_dir.glob("*.analysis.yaml"))
    if not files:
        sys.exit(f"No analysis files found in {analysis_dir}")

    grouped: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        assistant, _ = parse_assistant_and_mode(f.name)
        grouped[assistant].append(f)

    client = openai.OpenAI()

    for assistant, paths in grouped.items():
        logging.info(f"Generating final report for assistant: {assistant}")

        blocks = []
        for p in sorted(paths):
            _, mode = parse_assistant_and_mode(p.name)
            blocks.append(
                f"### Mode: {mode}\n\n```yaml\n{read_text(p)}\n```"
            )

        messages = [
            {
                "role": "system",
                "content": prompt_text,
            },
            {
                "role": "user",
                "content": f"""## Normalized Prompt Analyses for Assistant: {assistant}

{'\n\n'.join(blocks)}
""",
            },
        ]

        if args.dry_run:
            print(f"\n--- DRY RUN: {assistant} ---")
            print(f"Model: {args.model}")
            if args.seed is not None:
                print(f"Seed: {args.seed}")
            for m in messages:
                print(f"\n[{m['role']}]\n{m['content']}")
            continue

        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=messages,
                temperature=0.1,
                seed=args.seed,
            )
        except Exception:
            logging.exception(f"API call failed for {assistant}")
            sys.exit(1)

        output = response.choices[0].message.content
        if not output:
            sys.exit(f"Empty output for assistant {assistant}")

        out_path = Path(args.output_dir) / f"final-report-{assistant}.md"
        try:
            out_path.write_text(output.strip(), encoding="utf-8")
            logging.info(f"Wrote {out_path}")
        except Exception:
            logging.exception(f"Failed to write {out_path}")
            sys.exit(1)


if __name__ == "__main__":
    main()
