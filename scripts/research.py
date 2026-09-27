"""Optional offline JSON adapter; no network, wallet or schema-validation gate."""

import argparse
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys

# Isolated Python (-I) omits the script directory from its import path.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from calculations import (estimate_workload, gap_to_floor_scenario,
                          pending_delta_pace, summarize_rounds, weighted_price)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def _json_value(value):
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Fraction):
        return {"numerator": str(value.numerator), "denominator": str(value.denominator)}
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    raise TypeError(f"unsupported output value: {type(value).__name__}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Optional offline calculations on supplied JSON; no live reads or wallet actions.",
        epilog="Exit 0 means arithmetic completed, not verified or complete evidence. "
               "Exit 2 means invalid arguments/input or an input read failure.")
    commands = parser.add_subparsers(dest="command", required=True)
    descriptions = {
        "weighted-price": "Exact weighted accounting: {rows: [[quantity, raw_price], ...]}",
        "rounds": "Partial observed-round summary: an optional evidence-v1 document",
        "pace": "Signed ledger-change pace: explicit endpoints, timestamps, assets, scales and period",
        "workload": "Inclusive-range request estimate: ranges, max_blocks_per_request, optional overlaps",
        "curve": "Mathematical scenario only: opening, floor, half_life, elapsed, precision (16..200)",
    }
    for name, description in descriptions.items():
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("--input", type=Path, metavar="PATH",
                             help="Read UTF-8 JSON from this file instead of stdin")
    args = parser.parse_args(argv)
    try:
        text = args.input.read_text(encoding="utf-8") if args.input is not None else sys.stdin.read()
        document = json.loads(text, parse_float=str, parse_constant=_nonfinite,
                              object_pairs_hook=_object)
        if not isinstance(document, dict):
            raise ValueError("input must be one JSON object")
        if args.command == "rounds":
            result = summarize_rounds(document)
        else:
            function = {"weighted-price": weighted_price, "pace": pending_delta_pace,
                        "workload": estimate_workload, "curve": gap_to_floor_scenario}[args.command]
            result = function(**document)
        encoded = json.dumps(_json_value(result), ensure_ascii=True, allow_nan=False, indent=2)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError,
            ArithmeticError, RecursionError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
