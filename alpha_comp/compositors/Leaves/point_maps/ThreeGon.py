import torch
from strips.animated_property import AnimatedProperty
from alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
from alpha_comp.compositors.Nodes.TransformationMatrix import TransformationMatrix
import math
from alpha_comp.compositors.Leaves.point_maps.line import Line


class ThreeGon(PointMap):

    @staticmethod
    def rotation_2D(phi, device):
        return torch.tensor([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], device=device)

    @staticmethod
    def get_3Gons(position, size, device):
        unit = torch.tensor([[size, 0]], device=device)

        A = position + torch.matmul(unit, ThreeGon.rotation_2D(0, device))[0]
        B = position + torch.matmul(unit, ThreeGon.rotation_2D(2*math.pi*1/3, device))[0]
        C = position + torch.matmul(unit, ThreeGon.rotation_2D(2*math.pi*2/3, device))[0]

        AB = Line.from_2_points(A, B, device)
        BC = Line.from_2_points(B, C, device)
        CA = Line.from_2_points(C, A, device)

        return AB, BC, CA

