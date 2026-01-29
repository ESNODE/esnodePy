# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import argparse
import json
import sys
from typing import Optional, Any, Dict

from esnodepy.scanners import scan as scan_mod, imports as imports_mod, runtime as runtime_mod, diff as diff_mod
from esnodepy.engine import report
from esnodepy.engine.utils import TargetResolver, is_url
from esnodepy.engine.validation import validate_scan_report, ValidationError


def _write_output(data: Dict[str, Any], out_path: Optional[str]) -> None:
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Wrote JSON report to {out_path}")
    else:
        # Human readable fallback
        if data.get("drift_count") is not None:
            # Reconstruct minimal FunctionBoundary-like output via report_drift printing
            # The report functions expect boundaries; to avoid changing signature we re-print from structured data
            report.print_header("EDGE — Boundary Assumption Report")
            if data["drift_count"] == 0:
                print("No assumption drift detected.")
                return
            print(f"\n⚠ {data['drift_count']} boundary issues found:\n")
            for b in data["issues"]:
                print(f"{b['name']}()  [{b['file']}:{b['lineno']}]")
                print(f"  Declared return : {b['declared_return']}")
                print(f"  Observed returns:")
                for r in b["observed_returns"]:
                    print(f"    • {r}")
                print()
        elif data.get("risk_count") is not None:
            report.report_imports(data.get("risks", []))
        else:
            # Generic print
            print(json.dumps(data, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="esnodepy",
        description="Zero-config Python boundary intelligence"
    )

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("target", nargs="?", default=".", help="Target path or git url (http/https)")
    parent.add_argument("-o", "--output", dest="output", help="Write structured JSON output to file")

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("scan", parents=[parent], help="Detect boundary assumption drift")
    sub.add_parser("imports", parents=[parent], help="Analyze import boundaries")
    sub.add_parser("runtime", parents=[parent], help="Observe runtime behavior (opt-in, local only)")
    sub.add_parser("diff", parents=[parent], help="Analyze change impact")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # runtime must be local-only
    if args.command == "runtime" and is_url(args.target):
        print("Runtime observation is local-only and remote URLs are blocked for security.")
        sys.exit(2)

    try:
        with TargetResolver(args.target) as path:
            if args.command == "scan":
                result = scan_mod.run(path)
                # Validate before writing JSON to ensure consumers get well-formed data
                try:
                    validate_scan_report(result)
                except ValidationError as ve:
                    print(f"Report validation failed: {ve}")
                    sys.exit(2)
                _write_output(result, args.output)
            elif args.command == "imports":
                result = imports_mod.run(path)
                _write_output(result, args.output)
            elif args.command == "runtime":
                result = runtime_mod.run(path)
                _write_output(result, args.output)
            elif args.command == "diff":
                result = diff_mod.run(path)
                _write_output(result, args.output)
            else:
                parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
