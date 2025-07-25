from src.Nodes.node import Node
from src.Nodes.node import NodeSocket
from src.Nodes.math.constants.fill import Fill


class Out(Node):

    def __init__(self):
        self.noso_render_input = NodeSocket("RenderInput", default=Fill())
        super().__init__([self.noso_render_input], [], "The Output of the Patch")

    def produce(self):
        return self.noso_render_input.get().produce()
