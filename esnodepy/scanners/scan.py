import ast
import os
from esnodepy.engine.boundaries import FunctionBoundary
from esnodepy.engine.report import report_drift

def run():
    boundaries = []

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                except Exception:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        declared = (
                            ast.unparse(node.returns)
                            if node.returns else None
                        )
                        fb = FunctionBoundary(node.name, declared)
                        fb.observe_return("None")  # placeholder
                        boundaries.append(fb)

    report_drift(boundaries)
