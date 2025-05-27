from src.Nodes.node import Node
from src.Nodes.node import NodeSocket
from src.Nodes.maps.fill import Fill


class Out(Node):

    def __init__(self, node_id, factory_id):
        self.noso_render_input = NodeSocket(False, "RenderInput", default=Fill(-1, "None"))

        super().__init__(node_id, factory_id, "The Output of the Patch",
                         [self.noso_render_input], [])

    def produce(self):
        return self.noso_render_input.get().produce()

    @staticmethod
    def get_node_name():
        return "Output"
