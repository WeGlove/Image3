from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Select(Node):

    def __init__(self):
        self.a = NodeSocket("Tensor")
        self.begin = NodeSocket("Begin")
        self.end = NodeSocket("End")
        super().__init__([self.a, self.begin, self.end], [], "Division")

    def produce(self):
        return self.a.get().produce()[int(self.begin.get().produce()): int(self.end.get().produce())]