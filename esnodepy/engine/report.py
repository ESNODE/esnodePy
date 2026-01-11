# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

def print_header(title):
    print(f"\n{title}")
    print("=" * len(title))

def report_drift(boundaries):
    print_header("EDGE — Boundary Assumption Report")

    issues = [b for b in boundaries if b.has_drift()]

    if not issues:
        print("No assumption drift detected.")
        return

    print(f"\n⚠ {len(issues)} boundary issues found:\n")

    for b in issues:
        print(f"- {b.name}")
        print(f"  Declared return: {b.declared_return}")
        print(f"  Observed returns: {', '.join(b.observed_returns)}\n")
