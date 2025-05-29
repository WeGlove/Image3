from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Shape(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.reader = None
        super().__init__([self.a], [], "Division")

    def produce(self):
        a = self.a.get().produce()
        return a.shape
