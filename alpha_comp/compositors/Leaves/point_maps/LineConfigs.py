import torch
from strips.animated_property import AnimatedProperty
from alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
import math
from alpha_comp.compositors.Leaves.point_maps.line import Line


class LineConfigs(PointMap):

    @staticmethod
    def rotation_2D(phi, device):
        return torch.tensor([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], device=device)

    @staticmethod
    def get_NGons(n, position, size, device):
        unit = torch.tensor([[size, 0]], device=device)

        points = []
        for i in range(n):
            point = position + torch.matmul(unit, LineConfigs.rotation_2D(2*math.pi*i/n, device))[0]
            points.append(point)

        lines = []
        for i in range(n):
            if i == n-1:
                line = Line.from_2_points(points[i], points[0], device)
            else:
                line = Line.from_2_points(points[i], points[i+1], device)
            lines.append(line)

        return lines

    @staticmethod
    def get_star(n, position, size, device):
        unit = torch.tensor([[size, 0]], device=device)

        lines = []
        for i in range(n):
            point = position + torch.matmul(unit, LineConfigs.rotation_2D(2*math.pi*i/n, device))[0]
            lines.append(Line.from_2_points(position, point, device))

        return lines

