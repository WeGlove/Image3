from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Selection(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.dim = NodeSocket("Dim")
        self.select = NodeSocket("Select")
        self.reader = None
        super().__init__([self.a, self.dim, self.select], [], "Division")

    def produce(self):
        dim = int(self.dim.get().produce())
        index = int(self.select.get().produce())
        a = self.a.get().produce()
        return a.select(dim, index)
