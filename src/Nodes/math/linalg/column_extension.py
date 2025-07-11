from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class ColumnExtension(Node):

    def __init__(self):
        self.column = NodeSocket("Column")
        super().__init__([self.column], [], "Round")

    def produce(self):
        arr = self.column.get().produce()
        arr = arr.repeat((1, self.defaults.width))

        return arr
