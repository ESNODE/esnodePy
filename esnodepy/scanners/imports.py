# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import ast
import os

def run():
    print("\nEDGE — Import Boundary Report")
    print("============================")

    risky = []

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    tree = ast.parse(open(path).read())
                except Exception:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        risky.append((path, node.names[0].name))

    if not risky:
        print("No risky import boundaries detected.")
        return

    for path, name in risky[:5]:
        print(f"- {name} imported in {path}")
