# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

from typing import List, Dict, Any
from esnodepy.engine.boundaries import FunctionBoundary


def print_header(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


def collect_drift_data(boundaries: List[FunctionBoundary]) -> Dict[str, Any]:
    """Collect structured drift data suitable for JSON serialization."""
    issues = [b for b in boundaries if b.has_drift()]

    return {
        "drift_count": len(issues),
        "issues": [
            {
                "name": b.name,
                "file": b.file,
                "lineno": b.lineno,
                "declared_return": b.declared_return,
                "observed_returns": sorted(list(b.observed_returns)),
            }
            for b in issues
        ],
    }


def report_drift(boundaries: List[FunctionBoundary]) -> None:
    """Print a human-readable drift report (keeps behaviour for CLI)."""
    data = collect_drift_data(boundaries)
    print_header("EDGE — Boundary Assumption Report")

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


def collect_imports_data(risks: List[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "risk_count": len(risks),
        "risks": risks,
    }


def report_imports(risks: List[Dict[str, str]]) -> None:
    print_header("EDGE — Import Boundary Report")
    if not risks:
        print("No risky import boundaries detected.")
        return

    for r in risks[:10]:
        print(f"- {r['module']} imported in {r['path']}")

    if len(risks) > 10:
        print(f"... and {len(risks) - 10} others.")
