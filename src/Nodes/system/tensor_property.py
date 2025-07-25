import torch
from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit
import json


class TensorProperty(Node):

    def __init__(self):
        self.initial_value = NodeEdit("")
        super().__init__([], [self.initial_value], "Returns the given value.")

    def produce(self):
        text = json.loads(self.initial_value.get())
        return torch.tensor(text, device=self.defaults.device)
