from abc import abstractmethod
import numpy as np
import torch
from Nodes.node import Node


class Compositor(Node):

    def __init__(self, device, node_id, frame_counter, node_name="Compositor", subnode_sockets=None):
        super().__init__(node_id, node_name, "", frame_counter, [] if subnode_sockets is None else subnode_sockets, device, [])
        self.width = None
        self.height = None
        self.limit = None

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.width = width
        self.height = height
        self.limit = limit

    def free(self):
        pass
