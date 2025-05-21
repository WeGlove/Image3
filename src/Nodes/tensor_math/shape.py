from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Shape(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Division",[self.a], [])

    def produce(self):
        a = self.a.get().produce()
        return a.shape

    @staticmethod
    def get_node_name():
        return "Shape"
