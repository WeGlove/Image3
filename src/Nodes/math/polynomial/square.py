from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Square(Node):

    def __init__(self):
        self.a0 = NodeSocket("a0")
        self.a1 = NodeSocket("a1")
        self.b = NodeSocket("b")
        self.X0 = NodeSocket("X0")
        self.X1 = NodeSocket("X1")
        self.reader = None
        super().__init__([self.a0, self.a1, self.b, self.X0 , self.X1], [], "Keyboard Reader")

    def produce(self):
        return (self.a1.get().produce() * self.X1.get().produce() + self.a0.get().produce() * self.X0.get().produce() +
                self.b.get().produce())
