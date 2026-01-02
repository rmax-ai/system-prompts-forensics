#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""
band-report-from-csv.py

Generate a band report from a similarities CSV by sweeping thresholds and
recording connected components.

Expected CSV columns:
  - file_a
  - file_b
  - weighted_score

Usage:
  uv run --locked band-report-from-csv.py similarities.csv
  uv run --locked band-report-from-csv.py similarities.csv --step 0.01 --csv band-report.csv
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

# -------------------------
# Graph utilities
# -------------------------


def build_components(
    files: Set[str],
    edges: Dict[Tuple[str, str], float],
    threshold: float,
) -> List[Set[str]]:
    graph: Dict[str, Set[str]] = {f: set() for f in files}

    for (a, b), score in edges.items():
        if score >= threshold:
            graph[a].add(b)
            graph[b].add(a)

    visited: Set[str] = set()
    components: List[Set[str]] = []

    for node in graph:
        if node in visited:
            continue
        stack = [node]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            comp.add(cur)
            stack.extend(graph[cur] - visited)
        components.append(comp)

    return components


# -------------------------
# Main
# -------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Produce a band report (threshold → components) from similarities CSV"
    )
    parser.add_argument("csv", help="similarities.csv input file")
    parser.add_argument(
        "--step",
        type=float,
        default=0.01,
        help="Threshold step size (default: 0.01)",
    )
    parser.add_argument(
        "--csv-out",
        help="Optional CSV output path for band report",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"CSV file not found: {csv_path}")

    if args.dry_run:
        print(f"Dry run: Would process {csv_path} with step {args.step}")
        if args.csv_out:
            print(f"Dry run: Would write output to {args.csv_out}")
        return

    edges: Dict[Tuple[str, str], float] = {}
    files: Set[str] = set()
    scores: List[float] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"file_a", "file_b", "weighted_score"}
        if not required.issubset(reader.fieldnames or []):
            sys.exit(f"CSV must contain columns: {', '.join(required)}")

        for row in reader:
            a = row["file_a"]
            b = row["file_b"]
            s = float(row["weighted_score"])
            files.update([a, b])
            edges[(a, b)] = s
            scores.append(s)

    lo, hi = min(scores), max(scores)
    thresholds = np.arange(round(lo, 2), round(hi + args.step, 2), args.step)

    report_rows: List[dict] = []

    print("\nBand report (threshold → components):\n")
    for t in thresholds[::-1]:  # high → low
        comps = build_components(files, edges, float(t))
        sizes = sorted((len(c) for c in comps), reverse=True)
        row = {
            "threshold": round(float(t), 2),
            "components": len(comps),
            "largest_component": sizes[0] if sizes else 0,
            "component_sizes": " ".join(map(str, sizes)),
        }
        report_rows.append(row)

        print(
            f"t≥{row['threshold']:.2f} | "
            f"components={row['components']} | "
            f"largest={row['largest_component']} | "
            f"sizes=[{row['component_sizes']}]"
        )

    if args.csv_out:
        out = Path(args.csv_out)
        with out.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "threshold",
                    "components",
                    "largest_component",
                    "component_sizes",
                ],
            )
            writer.writeheader()
            writer.writerows(report_rows)
        logging.info(f"Band report CSV written to {out}")


if __name__ == "__main__":
    main()
