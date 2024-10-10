import torch
from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit


class StringProperty(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value=""):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, factory_id, "Returns the given value.", frame_counter, [], device, [self.initial_value])

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
