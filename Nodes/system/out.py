from Nodes.node import Node
from Nodes.node import NodeSocket


class Out(Node):

    def __init__(self, device, node_id, frame_counter, factory_id):
        self.noso_render_input = NodeSocket(False, "RenderInput", None)

        super().__init__(node_id, factory_id, "The Output of the Patch",
                         frame_counter, [self.noso_render_input], device, [])

    def produce(self):
        return self.noso_render_input.get().produce()

    @staticmethod
    def get_node_name():
        return "Output"
