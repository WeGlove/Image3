from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Selection(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.dim = NodeSocket(False, "Dim", default=None, description="")
        self.select = NodeSocket(False, "Select", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Division",[self.a, self.dim, self.select],[])

    def produce(self):
        dim = int(self.dim.get().produce())
        index = int(self.select.get().produce())
        a = self.a.get().produce()
        return a.select(dim, index)

    @staticmethod
    def get_node_name():
        return "Selection"
