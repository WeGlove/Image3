import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import math
from src.math.rotation2D import rotation_2D
from src.math.polynomial import two_points_to_linear
from src.math.gemoetry import dist_line


class NGon(Node):

    def __init__(self):
        self.n = NodeSocket("Line")
        self.position = NodeSocket("Position")
        self.shift_noso = NodeSocket("Shift")
        super().__init__([self.n, self.position, self.shift_noso])

    def produce(self):
        unit = torch.tensor([[100, 0]], device=self.defaults.device)

        points = []
        n = self.n.get().produce()
        for i in range(n):
            point = self.position.get().produce() + torch.matmul(unit, rotation_2D(2 * math.pi * i / n, self.defaults.device))[0]
            points.append(point)

        map = torch.zeros((self.defaults.width, self.defaults.height))
        for i in range(n):
            if i == n - 1:
                a, b = two_points_to_linear(points[i], points[0])
            else:
                a, b = two_points_to_linear(points[i], points[i + 1])
            vector_map = dist_line(a, b, self.defaults.width, self.defaults.height, self.defaults.device)
            map += vector_map

        map = map / n

        return map
