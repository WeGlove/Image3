import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Coloring(Node):

    def __init__(self):
        self.noso_compositor_a = NodeSocket("Compositor A")
        self.noso_compositor_b = NodeSocket("Compositor B")
        self.noso_compositor_c = NodeSocket("Compositor C")
        self.images = []
        super().__init__([self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c],
                         [], "Coloring")

    def produce(self):
        mask = torch.stack([self.noso_compositor_a.get().produce(), self.noso_compositor_b.get().produce(),
                            self.noso_compositor_c.get().produce()]).transpose(0, 2) % 1
        return mask * 255
