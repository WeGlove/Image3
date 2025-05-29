import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.system.number_property import NumberProperty


class Fill(Node):

    def __init__(self):
        self.input_noso = NodeSocket(False, "Input", NumberProperty())
        super().__init__([self.input_noso])

    def produce(self):
        return torch.ones((self.defaults.height, self.defaults.width), device=self.defaults.device) * self.input_noso.get().produce()
