from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Selection(Node):

    def __init__(self):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.dim = NodeSocket(False, "Dim", default=None, description="")
        self.select = NodeSocket(False, "Select", default=None, description="")
        self.reader = None
        super().__init__([self.a, self.dim, self.select], [], "Division")

    def produce(self):
        dim = int(self.dim.get().produce())
        index = int(self.select.get().produce())
        a = self.a.get().produce()
        return a.select(dim, index)
