import torch
from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image


class LoadImage(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.img = None
        super().__init__([], [self.initial_value], "Load Image")

    def produce(self):
        return self.img

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        path = self.initial_value.get()

        img = np.array(Image.open(os.path.join(path)))
        self.img = torch.tensor(img, device=self.defaults.device, dtype=torch.float)
        if self.img.shape[-1] > 3:
            self.img = self.img[:, :, :3]
        self.img = torch.transpose(self.img, 0, 1)
        self.img /= 255

        return img
