# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import argparse
from esnodepy.scanners import scan, imports, runtime, diff

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="esnodepy",
        description="Zero-config Python boundary intelligence"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("scan", help="Detect boundary assumption drift")
    sub.add_parser("imports", help="Analyze import boundaries")
    sub.add_parser("runtime", help="Observe runtime behavior (opt-in)")
    sub.add_parser("diff", help="Analyze change impact")

    args = parser.parse_args()

    if args.command == "scan":
        scan.run()
    elif args.command == "imports":
        imports.run()
    elif args.command == "runtime":
        runtime.run()
    elif args.command == "diff":
        diff.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
