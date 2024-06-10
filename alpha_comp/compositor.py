from abc import abstractmethod
import numpy as np
import torch
from alpha_comp.Node import Node


class Compositor(Node):

    def __init__(self, node_name="Compositor"):
        super().__init__(node_name)
        self.width = None
        self.height = None
        self.limit = None
        self.device = None

    def initialize(self, width, height, limit, device=None):
        self.width = width
        self.height = height
        self.limit = limit
        self.device = torch.device('cpu') if device is None else device

    def free(self):
        pass

    @abstractmethod
    def composite(self, index, img) -> np.ndarray:
        pass

    def get_animated_properties(self, visitors):
        return dict()