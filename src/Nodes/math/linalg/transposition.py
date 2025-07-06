from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Transposition(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.dim_1 = NodeSocket("Dim 1")
        self.dim_2 = NodeSocket("Dim 2")
        super().__init__([self.a, self.dim_1, self.dim_2], [], "Division")

    def produce(self):
        return self.a.get().produce().transpose(self.dim_1.get().produce(), self.dim_2.get().produce())
