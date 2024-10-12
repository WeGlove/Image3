from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit


class NumberProperty(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value=""):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, factory_id, "Returns the given value.", frame_counter, [], device, [self.initial_value])

    def produce(self):
        text = self.initial_value.get()
        return float(text)

    @staticmethod
    def get_node_name():
        return "Number Property"
