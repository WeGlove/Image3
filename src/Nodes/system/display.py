from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
from src.Nodes.node_socket import NodeSocket


class Display(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.initial_value = NodeEdit("")
        super().__init__(node_id, factory_id, "Returns the given value.",  [self.a], [self.initial_value])

    def produce(self):
        a = self.a.get().produce()
        self.initial_value.set(a)

        return a

    @staticmethod
    def get_node_name():
        return "Display"
