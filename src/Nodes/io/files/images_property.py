import logging
import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image


class ImagesProperty(Node):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.initial_value = NodeEdit(".")
        super().__init__([], [self.initial_value], "Images Property")

    def produce(self):
        return self.initial_value.get()

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        super().initialize(width, height, excluded_nodes, frame_counter, device)
        path = self.initial_value.get()

        images = []
        for i, file in enumerate(os.listdir(path)):
            self.logger.debug(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=self.device, dtype=torch.float)
            img = img[:, :, :3]
            images.append(img)

        return images
