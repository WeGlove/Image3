import torch
from Nodes.maps.point_map import PointMap
import math
from Nodes.maps.line import Line
import random


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


    @staticmethod
    def get_random(n, position, size, node_id, device, frame_counter, factory_id):
        unit = torch.tensor([[size, 0]], device=device)

        lines = []
        for i in range(n):
            point = position + torch.matmul(unit, LineConfigs.rotation_2D(2*math.pi*random.random()/n, device))[0]
            lines.append(Line.from_2_points(position, point, device, factory_id=factory_id, node_id=node_id, frame_counter=frame_counter))

        return lines
