import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
import keyboard


class KeyboardReader(Node):

    def __init__(self, node_id, factory_id,):
        self.initial_value = NodeEdit(".")
        self.reader = None
        super().__init__(node_id, factory_id, "Keyboard Reader", [], [self.initial_value])

    def produce(self):
        return keyboard.is_pressed(self.initial_value.get())

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    @staticmethod
    def get_node_name():
        return "Keyboard Reader"
