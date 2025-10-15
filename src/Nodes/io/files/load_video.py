import torch
from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit
import os
import numpy as np
from PIL import Image
import cv2


class LoadVideo(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.cap = None
        super().__init__([], [self.initial_value], "Load Image")

    def produce(self):
        ret, frame = self.cap.read()
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pil_img_torch = torch.tensor(np.array(pil_img), device=self.defaults.device)
        return pil_img_torch

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.cap = cv2.VideoCapture(self.initial_value.get().produce())
