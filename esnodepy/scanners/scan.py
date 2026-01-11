# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import ast
import os
import logging
from typing import List, Optional
from esnodepy.engine.boundaries import FunctionBoundary
from esnodepy.engine.report import report_drift

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def infer_return_value(node: Optional[ast.AST]) -> str:
    """
    Infer a human-readable return value shape from an AST node.
    """
    if node is None:
        return "None"

    if isinstance(node, ast.Constant):
        return str(type(node.value).__name__)

    if isinstance(node, ast.Name):
        return f"Unknown({node.id})"

    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return f"CallResult({node.func.id})"
        return "CallResult"

    if isinstance(node, ast.Attribute):
        return "AttributeValue"

    return "Unknown"

def run(target_dir: str = ".") -> None:
    """
    Scans the target directory for Python files and analyzes function return type drift
    using AST-based return value inference.

    Args:
        target_dir (str): The directory to scan. Defaults to current directory.
    """
    boundaries: List[FunctionBoundary] = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source)
            except (OSError, SyntaxError, UnicodeDecodeError) as e:
                logger.warning(f"Failed to parse {path}: {e}")
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    declared = (
                        ast.unparse(node.returns)
                        if node.returns else None
                    )

                    fb = FunctionBoundary(
                        name=node.name,
                        declared_return=declared,
                        file=path,
                        lineno=node.lineno
                    )

                    has_explicit_return = False

                    # Walk the function body to find return statements
                    # Note: simple walk does not handle nested functions correctly (it looks inside them).
                    # For v0.2 this is an acceptable known limitation.
                    
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return):
                            has_explicit_return = True
                            # Use casting or check for None, but inferred signature handles Optional[AST]
                            inferred = infer_return_value(child.value)
                            fb.observe_return(inferred)

                    # Check for implicit None (fall-through)
                    if node.body:
                        last_stmt = node.body[-1]
                        if not isinstance(last_stmt, (ast.Return, ast.Raise)):
                             fb.observe_return("None (implicit)")
                    elif not node.body:
                        fb.observe_return("None (implicit)")

                    boundaries.append(fb)

    report_drift(boundaries)
