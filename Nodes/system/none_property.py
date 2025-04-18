from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit


class NoneProperty(Node):

    def __init__(self, node_id, factory_id, device, frame_counter):
        super().__init__(node_id, factory_id, "Returns the given value.", frame_counter, [], device, [])

    def produce(self):
        return None

    @staticmethod
    def get_node_name():
        return "None Property"
