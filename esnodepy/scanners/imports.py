# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import ast
import os
import logging
from typing import List, Tuple

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def run(target_dir: str = ".") -> None:
    """
    Scans for external imports in the target directory to identify boundary risks.

    Args:
        target_dir (str): Directory to scan.
    """
    print("\nEDGE — Import Boundary Report")
    print("============================")

    risky: List[Tuple[str, str]] = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                         tree = ast.parse(f.read())
                except (OSError, SyntaxError, UnicodeDecodeError) as e:
                    logger.warning(f"Failed to parse {path}: {e}")
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            risky.append((path, alias.name))
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            risky.append((path, node.module))

    if not risky:
        print("No risky import boundaries detected.")
        return

    # De-duplicate and limit output for CLI readability
    unique_risks = sorted(list(set(risky)), key=lambda x: x[1])
    
    for path, mod_name in unique_risks[:10]:
        print(f"- {mod_name} imported in {path}")
    
    if len(unique_risks) > 10:
        print(f"... and {len(unique_risks) - 10} others.")
