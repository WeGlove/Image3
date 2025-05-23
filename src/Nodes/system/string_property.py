import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit


class StringProperty(Node):

    def __init__(self, node_id, factory_id):
        self.initial_value = NodeEdit("")
        super().__init__(node_id, factory_id, "Returns the given value.", [], [self.initial_value])

    def produce(self):
        text = self.initial_value.get()
        return text

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    @staticmethod
    def get_node_name():
        return "String Property"
