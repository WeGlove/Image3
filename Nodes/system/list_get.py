from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit
from Nodes.node_socket import NodeSocket


class ListGet(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value=""):
        self.initial_value = NodeEdit(initial_value)
        self.compositor = NodeSocket(False, "Compositor", None)
        super().__init__(node_id, factory_id, "Returns the given value.", frame_counter, [self.compositor], device, [self.initial_value])

    def produce(self):
        text = self.initial_value.get()
        compositor = self.compositor.get().produce()

        return compositor[int(text)]

    @staticmethod
    def get_node_name():
        return "List Get"
