import torch
from Nodes.node import Node
from Nodes.node_edit import NodeEdit


class ValueProperty(Node):

    def __init__(self, initial_value, node_id, device, frame_counter):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, "", frame_counter, [], device, [self.initial_value])

    def produce(self):
        return self.initial_value.get()

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    @staticmethod
    def get_node_name():
        return "Value Property"
