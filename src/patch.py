class Patch:

    def __init__(self):
        self.root = None
        self.nodes = {}

    def get_nodes(self):
        return self.nodes.values()

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node(self, node_id):
        return self.nodes[node_id]

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root
