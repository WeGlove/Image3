
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.math.polynomial import linear_dist


class DistLinear(Node):

    def __init__(self):
        """

        :param line: as [ax + by + c]
        :param node_id:
        :param device:
        """
        self.line_noso = NodeSocket("Line")
        self.shift_noso = NodeSocket("Shift")
        super().__init__([self.line_noso, self.shift_noso])

    def produce(self):
        vector_map = linear_dist(self.line_noso.get().produce(), self.shift_noso.get().prodcue(), self.defaults.width,
                                 self.defaults.height, self.defaults.device)

        return vector_map
