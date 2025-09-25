from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node


class RGBToG(Node):

    def __init__(self):
        self.rgb = NodeSocket("RGB")
        super().__init__([self.rgb])

    def produce(self):
        img = self.rgb.get().produce()

        return img[:, :, 1]
