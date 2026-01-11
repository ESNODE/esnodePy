# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

from typing import List, Tuple, Any

class BoundaryGraph:
    """
    A graph representation of the code's execution boundaries.
    """
    def __init__(self) -> None:
        self.nodes: List[Any] = []
        self.edges: List[Tuple[Any, Any, str]] = []

    def add_node(self, node: Any) -> None:
        """
        Add a node to the graph.

        Args:
            node (Any): The node object (e.g., FunctionBoundary).
        """
        self.nodes.append(node)

    def add_edge(self, src: Any, dst: Any, kind: str) -> None:
        """
        Add a directed edge between two nodes.

        Args:
            src (Any): Source node.
            dst (Any): Destination node.
            kind (str): The type of relationship (e.g., "CALLS", "IMPORTS").
        """
        self.edges.append((src, dst, kind))
