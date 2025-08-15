from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Normal(Node):

    def __init__(self):
        self.noso_mean = NodeSocket("Mean")
        self.noso_std = NodeSocket("Std")
        super().__init__([self.noso_mean, self.noso_std], [], "Returns the given value.")

    def produce(self):
        return torch.normal(torch.ones((self.defaults.width, self.defaults.height), device=self.defaults.device) * self.noso_mean.get().produce(),
                            torch.ones((self.defaults.width, self.defaults.height), device=self.defaults.device) * self.noso_std.get().produce())
