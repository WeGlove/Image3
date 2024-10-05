import torch
from Nodes.node import Node
from Nodes.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image


class ImagesProperty(Node):

    def __init__(self, initial_value, node_id, device, frame_counter):
        self.initial_value = NodeEdit(initial_value)
        super().__init__(node_id, "Images Property", "", frame_counter, [], device, [self.initial_value])

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

        images = []
        for i, file in enumerate(os.listdir(path)):
            print(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=self.device)
            images.append(img)

        return images
