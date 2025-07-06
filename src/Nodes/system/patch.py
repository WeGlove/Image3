from src.Nodes.node import Node


class Patch(Node):

    def __init__(self):
        self.root = None
        self.nodes = {}
        super().__init__([], [], "Returns the value of the patch.")

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        if self.root is not None:
            self.root.initialize(defaults, excluded_nodes, frame_counter)

    def get_nodes(self):
        return self.nodes.values()

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node(self, node_id):
        return self.nodes[node_id]

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def set_root(self, root): # TODO this should be done via ID
        self.root = root

    def get_root(self):
        return self.root

    def remove_node(self, node_id):
        del self.nodes[node_id]
