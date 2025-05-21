import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
import json


class TensorProperty(Node):

    def __init__(self, node_id, factory_id, device, initial_value=""):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, factory_id, "Returns the given value.", [], device, [self.initial_value])

    def produce(self):
        text = json.loads(self.initial_value.get())
        return torch.tensor(text, device=self.device)

    @staticmethod
    def get_node_name():
        return "Tensor Property"
