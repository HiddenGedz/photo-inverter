from __future__ import annotations

import argparse
from pathlib import Path

from .components import InvertPipeline


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Invert image colors (component-based example).")
    p.add_argument("input", type=str, help="Path to input image")
    p.add_argument("output", type=str, help="Path to output image")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    pipeline = InvertPipeline()
    res = pipeline.run(Path(args.input), Path(args.output))
    print(f"Saved inverted image: {res.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
