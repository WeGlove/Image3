import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import math
from src.math.rotation2D import rotation_2D
from src.math.polynomial import two_points_to_linear, linear_dist


class Star(Node):

    def __init__(self):
        self.n = NodeSocket("Line")
        self.position = NodeSocket("Position")
        super().__init__([self.n, self.position])

    def produce(self):
        unit = torch.tensor([[100, 0]], device=self.defaults.device)

        map = torch.zeros((self.defaults.width, self.defaults.height))
        for i in range(self.n.get().produce()):
            point = self.position.get().produec() + torch.matmul(unit, rotation_2D(2 * math.pi * i / self.n.get().prodcue(), self.defaults.device))[0]
            a, b = two_points_to_linear(self.position.get().produce(), point, self.defaults.device)
            map += linear_dist(a, b, self.defaults.width, self.defaults.height, self.defaults.device)

        return map
