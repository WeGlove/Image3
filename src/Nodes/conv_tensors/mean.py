import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Mean(Node):

    def __init__(self,):
        self.size = NodeSocket("Size")
        self.reader = None
        super().__init__([self.size], [], "Mean Tensor")

    def produce(self):
        size = self.size.get().produce()
        mask = torch.ones((int(size), int(size)), device=self.defaults.device)
        mask = mask / size
        return mask
