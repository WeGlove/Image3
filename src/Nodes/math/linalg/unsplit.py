import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Unsplit(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        super().__init__([self.a], [], "DeTiling")

    def produce(self):
        imgs = self.a.get().produce()
        img = torch.concatenate(imgs)
        return img
