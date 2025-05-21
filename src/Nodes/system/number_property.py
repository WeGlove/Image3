from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit


class NumberProperty(Node):

    def __init__(self, node_id, factory_id):
        self.initial_value = NodeEdit(0)
        super().__init__(node_id, factory_id, "Returns the given value.", [], [self.initial_value])

    def produce(self):
        text = self.initial_value.get()
        return float(text)

    @staticmethod
    def get_node_name():
        return "Number Property"
