import torch
from strips.animated_property import AnimatedProperty
from alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
from alpha_comp.compositors.Nodes.TransformationMatrix import TransformationMatrix
import math
from alpha_comp.compositors.Leaves.point_maps.line import Line


class ThreeGon(PointMap):

    def __init__(self, position, size):
        super().__init__()
        self.position = AnimatedProperty(initial_value=position)
        self.size = AnimatedProperty(initial_value=size)

        self.AB = Line(torch.tensor([1,0,0], device=self.device))
        self.BC = Line(torch.tensor([1,0,0], device=self.device))
        self.CA = Line(torch.tensor([1,0,0], device=self.device))

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.AB.initialize(width, height, limit, device)
        self.BC.initialize(width, height, limit, device)
        self.CA.initialize(width, height, limit, device)

    def _rotation_matrix(self, phi, device):
        return torch.tensor([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], device=device)

    def composite(self, index, img):
        unit = torch.tensor([[1., 0.]], device=self.device)

        A = self.position.get() + unit.flatten() * self.size.get()
        B = self.position.get() + torch.matmul(self._rotation_matrix(2*math.pi/3, self.device), unit.T).flatten() * self.size.get()
        C = self.position.get() + torch.matmul(self._rotation_matrix(2*math.pi*2/3, self.device), unit.T).flatten() * self.size.get()

        AB = B - A
        BC = C - B
        CA = A - C

        self.AB.line.initial_value = torch.tensor([AB[0], AB[1], A[0]], device=self.device)
        self.BC.line.initial_value = torch.tensor([BC[0], BC[1], B[0]], device=self.device)
        self.CA.line.initial_value = torch.tensor([CA[0], CA[1], C[0]], device=self.device)

        map = self.AB.composite(index, img) + self.BC.composite(index, img) + self.CA.composite(index, img)
        map = map/3

        return map

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "ThreeGon:size": self.size}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
