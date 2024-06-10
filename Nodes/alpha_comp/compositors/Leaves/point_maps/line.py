from Nodes.alpha_comp.Geos import get_centered_vector_map
import torch
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
import math


class Line(PointMap):

    def __init__(self, line):
        self.line = AnimatedProperty(initial_value=line)
        super().__init__("Line", [self.line])

    @staticmethod
    def from_2_points(x_0, x_1, device):
        AB = x_1 - x_0
        a = AB[0]
        b = AB[1]
        c = x_0[1]

        return Line(torch.tensor([a, b, c], device=device))

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)

    def composite(self, index, img):
        position = self.line.get()

        vector_map = get_centered_vector_map(self.width, self.height, self.device)

        vector_map = vector_map * position[:2]

        vector_map = torch.sum(vector_map, dim=2)

        vector_map = vector_map + position[2]

        vector_map = vector_map / math.sqrt(position[0]**2 + position[1]**2)

        vector_map = vector_map / math.sqrt((self.width/2)**2 + (self.height/2)**2)

        vector_map = torch.abs(vector_map)

        return vector_map

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "Line:line": self.line}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
