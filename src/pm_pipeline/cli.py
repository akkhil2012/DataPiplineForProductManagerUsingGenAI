"""Command line interface for the product insights pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import Pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the product insights pipeline")
    parser.add_argument("--input", required=True, type=Path, help="Path to the feedback CSV file")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Directory where generated artifacts will be stored",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = Pipeline()
    result = pipeline.run_from_csv(args.input)
    Pipeline.write_outputs(result, args.output)
    print(f"Generated artifacts in {args.output.resolve()}")


if __name__ == "__main__":
    main()
