from src.Nodes.node import Node


class NoneProperty(Node):

    def __init__(self, node_id, factory_id, device):
        super().__init__(node_id, factory_id, "Returns the given value.", [], device, [])

    def produce(self):
        return None

    @staticmethod
    def get_node_name():
        return "None Property"
