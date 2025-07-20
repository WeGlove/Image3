import logging
import torch
from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image


class ImagesProperty(Node):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.initial_value = NodeEdit(".")
        self.images = []
        super().__init__([], [self.initial_value], "Images Property")

    def produce(self):
        return self.images

    def initialize(self, defaults,  excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        path = self.initial_value.get()

        images = []
        for i, file in enumerate(os.listdir(path)):
            self.logger.debug(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=self.defaults.device, dtype=torch.float)
            img = img[:, :, :3]
            img = img / 255
            images.append(img)

        self.images = images
