import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class Fill(Node):

    def __init__(self):
        self.input_noso = NodeSocket("Input", InternalValue(0))
        super().__init__([self.input_noso])

    def produce(self):
        return (torch.ones(self.defaults.dimensions, device=self.defaults.device)
                * self.input_noso.get().produce())
