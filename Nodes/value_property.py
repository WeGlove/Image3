import torch
from Nodes.node import Node
from Nodes.node_edit import NodeEdit


class ValueProperty(Node):

    def __init__(self, initial_value, node_id, device):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, "Value Property", [], device, [self.initial_value])

    def set_anim_style(self, style):
        pass

    def set_key_frame(self, frame, value):
        pass

    def get(self):
        return self.initial_value.get()

    def set_next(self):
        pass

    def set_previous(self):
        pass

    def set_frame(self, frame):
        pass

    def is_animated(self):
        return False

    def set_constraint(self, constraint):
        ...

    def is_constrained(self):
        return False

    def get_animated_properties(self, _):
        return {}

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    @staticmethod
    def from_dict(properties, device):
        value = properties["value"]
        return ValueProperty(value, device=device)
