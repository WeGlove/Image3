from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.math.gemoetry import dist_line, slope_interceptr_to_linear
from src.Nodes.internal.internal_value import InternalValue


class DistAnchorLine(Node):

    def __init__(self):
        self.offset = NodeSocket("Anchor", default=InternalValue(0))
        self.slope = NodeSocket("Slope", default=InternalValue(1))
        super().__init__([self.offset, self.slope], [], "Returns the given value.")

    def produce(self):
        offset = self.offset.get()
        slope = self.slope.get()

        return dist_line(*slope_interceptr_to_linear(offset, slope), self.defaults.width, self.defaults.height, self.defaults.device)
