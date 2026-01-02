#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai", "PyYAML"]
# ///

"""
system-prompt-analysis.py

Generate a normalized system-prompt analysis from:
- a normalization prompt (Markdown)
- a schema YAML
- an invocation payload JSON

Usage:
  uv run --locked system-prompt-analysis.py \
    --prompt prompt.md \
    --schema schema/system-prompt.v0.yaml \
    --invocation request.json \
    --model gpt-5.2
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
import yaml
from openai.types.chat import ChatCompletionMessageParam


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def clean_output(text: str) -> str:
    """Remove markdown code blocks if present."""
    # Match ```yaml ... ``` or ``` ... ```
    # We use a non-greedy match for the content and handle multiple blocks by taking the first one
    pattern = r"```(?:yaml)?\s*\n(.*?)\n\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
        logging.debug("Removed markdown code block markers from output")
        return cleaned
    return text.strip()


def validate_yaml(text: str, schema_yaml: str) -> None:
    """Validate that the text is valid YAML and matches the basic schema structure."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        logging.exception("Output is not valid YAML")
        sys.exit(1)

    if not isinstance(data, dict):
        sys.exit("Output YAML must be a dictionary at the top level")

    try:
        schema = yaml.safe_load(schema_yaml)
    except yaml.YAMLError:
        logging.exception("Failed to parse schema for validation")
        return

    # Basic structural check: ensure major sections from schema exist in data
    # We skip 'schema' as it's metadata about the schema itself
    expected_sections = [k for k in schema.keys() if k != "schema"]
    missing_sections = [s for s in expected_sections if s not in data]

    if missing_sections:
        logging.warning(
            f"Output is missing expected schema sections: {', '.join(missing_sections)}"
        )
    else:
        logging.debug("Output passed basic structural validation against schema")


def main() -> None:
    parser = argparse.ArgumentParser(description="System prompt normalization runner")
    parser.add_argument(
        "--prompt", required=True, help="Normalization prompt (Markdown)"
    )
    parser.add_argument("--schema", required=True, help="Normalization schema (YAML)")
    parser.add_argument("--invocation", required=True, help="Invocation payload (JSON)")
    parser.add_argument("--model", required=True, help="Model name (e.g. gpt-5.2)")
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output", help="Output file path (optional, prints to stdout if omitted)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request that would be sent and exit without calling the API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for debugging",
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    prompt_path = Path(args.prompt)
    schema_path = Path(args.schema)
    invocation_path = Path(args.invocation)

    normalization_prompt = read_text(prompt_path)
    schema_yaml = read_text(schema_path)
    invocation_json = read_text(invocation_path)

    logging.debug(f"Read prompt from {prompt_path} ({len(normalization_prompt)} chars)")
    logging.debug(f"Read schema from {schema_path} ({len(schema_yaml)} chars)")
    logging.debug(
        f"Read invocation from {invocation_path} ({len(invocation_json)} chars)"
    )

    # Validate JSON early
    try:
        json.loads(invocation_json)
    except json.JSONDecodeError:
        logging.exception("Invalid JSON in invocation payload")
        sys.exit(1)

    # Calculate capture metadata
    file_stat = invocation_path.stat()
    timestamp = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    artifact_hash = hashlib.sha256(invocation_json.encode("utf-8")).hexdigest()

    capture_metadata: dict[str, str | dict[str, str]] = {
        "method": "mitmproxy",
        "timestamp": timestamp,
        "environment": {
            "os": platform.system(),
            "arch": platform.machine(),
            "runtime": f"Python {platform.python_version()}",
        },
        "artifact_hash": artifact_hash,
    }

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": normalization_prompt,
        },
        {
            "role": "user",
            "content": f"""## Normalization Schema ({schema_path.name})

    ```yaml
    {schema_yaml}
    ```
    """,
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
            "content": f"""## Invocation Payload ({invocation_path.name})

    ```json
    {invocation_json}
    ```
    """,
        },
    ]

    # If dry-run, print the prepared request and exit without calling the API.
    if args.dry_run:
        print("Dry run mode enabled. The following request would be sent to the model:")
        print(f"Model: {args.model}")
        if args.seed is not None:
            print(f"Seed: {args.seed}")
        print("Messages:")
        print(json.dumps(messages, indent=2, ensure_ascii=False))
        # Also print invocation and schema for convenience
        print("\n--- Normalization prompt ---")
        print(normalization_prompt)
        print("\n--- Schema YAML ---")
        print(schema_yaml)
        print("\n--- Capture Metadata ---")
        print(json.dumps(capture_metadata, indent=2))
        print("\n--- Invocation JSON ---")
        print(invocation_json)
        return

    # Instantiate client only when making a real API call (avoids requiring OPENAI_API_KEY in --dry-run)
    client = openai.OpenAI()

    logging.info(f"Calling model {args.model}...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            # Temperature 0 is supported by all GPT-4 and GPT-5 models (except mini variants)
            temperature=0,
            seed=args.seed,
        )
    except Exception:
        logging.exception("API call failed")
        sys.exit(1)

    # Print ONLY the model output
    output = response.choices[0].message.content
    if not output:
        sys.exit("Model returned empty output")

    logging.debug(f"Received response ({len(output)} chars)")

    # Clean and validate output
    output = clean_output(output)
    validate_yaml(output, schema_yaml)

    if args.output:
        output_path = Path(args.output)
        try:
            logging.debug(f"Writing output to {output_path}")
            output_path.write_text(output, encoding="utf-8")
            print(f"Analysis saved to {output_path}")
        except Exception:
            logging.exception(f"Failed to write output to {output_path}")
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
