import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Split(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.x = NodeSocket("X")
        super().__init__([self.a, self.x], [], "Tiling")

    def produce(self):
        tiles = torch.tensor_split(self.a.get().produce(), self.x.get().produce())

        return tiles
