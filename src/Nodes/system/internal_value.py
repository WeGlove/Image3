from src.Nodes.node import Node


class InternalValue(Node):

    def __init__(self, value):
        self.value = value

        super().__init__([
        ], [], "Circles")

    def produce(self):
        return self.value
