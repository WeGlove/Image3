from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class RowExtension(Node):

    def __init__(self):
        self.row = NodeSocket("Row")
        super().__init__([self.row], [], "Round")

    def produce(self):
        arr = self.row.get().produce()
        arr = arr.repeat((self.defaults.height, 1))

        return arr
