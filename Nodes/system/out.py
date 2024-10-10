from Nodes.node import Node
from Nodes.node import NodeSocket


class Out(Node):

    def __init__(self, device, node_id, frame_counter, factory_id):
        self.noso_render_input = NodeSocket(False, "RenderInput", None)

        super().__init__(node_id, factory_id, "The Output of the Patch",
                         frame_counter, [self.noso_render_input], device, [])

    def produce(self):
        return self.noso_render_input.get().produce()

    def initialize(self, width, height, *args):
        for socket in self.subnode_sockets:
            socket.get().initialize(width, height)

    @staticmethod
    def get_node_name():
        return "Output"
