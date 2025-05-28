import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
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

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        super().initialize(width, height, excluded_nodes, frame_counter, device)
        path = self.initial_value.get()

        img = np.array(Image.open(os.path.join(path)))
        self.img = torch.tensor(img, device=self.device, dtype=torch.float)

        return img
