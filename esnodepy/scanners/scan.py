# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import ast
import os
import logging
from typing import List
from esnodepy.engine.boundaries import FunctionBoundary
from esnodepy.engine.report import report_drift

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def run(target_dir: str = ".") -> None:
    """
    Scans the target directory for Python files and analyzes function return type drift.

    Args:
        target_dir (str): The directory to scan. Defaults to current directory.
    """
    boundaries: List[FunctionBoundary] = []

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
                    if isinstance(node, ast.FunctionDef):
                        declared = (
                            ast.unparse(node.returns)
                            if node.returns else None
                        )
                        fb = FunctionBoundary(node.name, declared)
                        
                        # In v0.1, static analysis inference is a placeholder.
                        # Real implementation would infer distinct return paths.
                        # For now, we simulate an untyped observation (None).
                        fb.observe_return("None") 
                        
                        boundaries.append(fb)

    report_drift(boundaries)
