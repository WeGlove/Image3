import torch
from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image


class LoadImage(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, factory_id, "Load Image", frame_counter, [], device, [self.initial_value])

    def produce(self):
        return self.initial_value.get()

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    def initialize(self, width, height, *args):
        path = self.initial_value.get()

        img = np.array(Image.open(os.path.join(path)))
        img = torch.tensor(img, device=self.device, dtype=torch.float)

        return img

    @staticmethod
    def get_node_name():
        return "Load Image"
