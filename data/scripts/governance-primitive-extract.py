#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
governance-primitive-extract.py

Extract verbatim prompt governance primitives from a system prompt payload
using a strict extraction prompt.

Usage:
  uv run --locked governance-primitive-extract.py \
    --prompt prompts/governance-primitive-extraction.prompt.md \
    --payload payload/vscode-copilot.agent.json \
    --model gpt-5.2 \
    --output governance/vscode-copilot.agent.json
"""

import argparse
import hashlib
import json
import logging
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from openai.types.chat import ChatCompletionMessageParam


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def clean_output(text: str) -> str:
    """
    Remove markdown code fences if the model accidentally emits them.
    Only the first fenced block is extracted.
    """
    pattern = r"```(?:json)?\s*\n(.*?)\n\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        logging.debug("Removed markdown code block markers from output")
        return match.group(1).strip()
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prompt governance primitive extraction runner"
    )
    parser.add_argument("--prompt", required=True, help="Extraction prompt (Markdown)")
    parser.add_argument("--payload", required=True, help="System prompt payload (JSON)")
    parser.add_argument("--model", required=True, help="Model name (e.g. gpt-5.2)")
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON file path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request that would be sent and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    # Logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    prompt_path = Path(args.prompt)
    payload_path = Path(args.payload)
    output_path = Path(args.output)

    extraction_prompt = read_text(prompt_path)
    payload_json = read_text(payload_path)

    logging.debug(f"Read prompt from {prompt_path}")
    logging.debug(f"Read payload from {payload_path}")

    # Validate payload JSON early
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError:
        logging.exception("Invalid JSON in payload")
        sys.exit(1)

    # Capture metadata (deterministic + audit-friendly)
    stat = payload_path.stat()
    artifact_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
    captured_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    # Extract assistant and mode from filename
    # Expected format: assistant.mode.suffix
    parts = payload_path.name.split(".")
    assistant_name = parts[0] if len(parts) > 0 else "unknown"
    mode_name = parts[1] if len(parts) > 1 else "unknown"

    capture_metadata = {
        "assistant_name": assistant_name,
        "mode_name": mode_name,
        "source_file": payload_path.name,
        "source_hash": artifact_hash,
        "timestamp": captured_at,
        "environment": {
            "os": platform.system(),
            "arch": platform.machine(),
            "runtime": f"Python {platform.python_version()}",
        },
    }

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": extraction_prompt,
        },
        {
            "role": "user",
            "content": f"""## Capture Metadata

```json
{json.dumps(capture_metadata, indent=2)}
```
""",
        },
        {
            "role": "user",
            "content": f"""## Prompt Payload ({payload_path.name})

```json
{json.dumps(payload, indent=2)}
```

""",
        },
    ]

    if args.dry_run:
        print("Dry run mode enabled. The following request would be sent:\n")
        print(f"Model: {args.model}")
        if args.seed is not None:
            print(f"Seed: {args.seed}")
        print(json.dumps(messages, indent=2, ensure_ascii=False))
        return

    client = openai.OpenAI()

    logging.info(f"Calling model {args.model}...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0,
            seed=args.seed,
        )
    except Exception:
        logging.exception("API call failed")
        sys.exit(1)

    content = response.choices[0].message.content
    if not content:
        sys.exit("Model returned empty output")

    content = clean_output(content)

    # Validate output JSON strictly
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        logging.exception("Model output is not valid JSON")
        sys.exit(1)

    # Write output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(parsed, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Governance primitives saved to {output_path}")
    except Exception:
        logging.exception("Failed to write output")
        sys.exit(1)


if __name__ == "__main__":
    main()
