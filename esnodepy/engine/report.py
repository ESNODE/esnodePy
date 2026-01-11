# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

from typing import List
from esnodepy.engine.boundaries import FunctionBoundary

def print_header(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))

def report_drift(boundaries: List[FunctionBoundary]) -> None:
    print_header("EDGE — Boundary Assumption Report")

    # Drift definition for report: 
    # Declared return exists, is not None, but we see a None based return.
    issues = [
        b for b in boundaries
        if b.has_drift()
    ]

    if not issues:
        print("No assumption drift detected.")
        return

    print(f"\n⚠ {len(issues)} boundary issues found:\n")

    for b in issues:
        print(f"{b.name}()  [{b.file}:{b.lineno}]")
        print(f"  Declared return : {b.declared_return}")
        print(f"  Observed returns:")
        for r in sorted(list(b.observed_returns)):
            print(f"    • {r}")
        print()
