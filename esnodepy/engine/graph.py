class BoundaryGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, src, dst, kind):
        self.edges.append((src, dst, kind))
