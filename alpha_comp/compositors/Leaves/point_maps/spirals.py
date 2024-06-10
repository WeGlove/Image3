from alpha_comp.Geos import get_polar
import torch
from strips.animated_property import AnimatedProperty
import math
from alpha_comp.compositors.Leaves.point_maps.point_map import PointMap


class Spirals(PointMap):

    def __init__(self, points, scale_radius=1, scale=5, shift=0, ratio=0.5, rotation=0, frequency=1, weights_angles=None):
        self.points = AnimatedProperty(initial_value=points)
        self.rotation = AnimatedProperty(initial_value=rotation)
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.weights_angle = AnimatedProperty(initial_value=weights_angles)

        self.angle_space = None
        super().__init__("Spirals", [self.points, self.rotation, self.frequency, self.weights_angle])


    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.weights_angle.initial_value is None:
            self.weights_angle.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)

        self.angle_space = 2 * torch.pi / self.limit

    def composite(self, index, img):
        rad_out = None
        angles_out = None
        points = self.points.get()
        weights_angle = self.weights_angle.get()
        weights_angle = weights_angle / torch.sum(weights_angle)
        for i in range(points.shape[0]):
            rad, angle = get_polar(self.width, self.height, self.device, points[i])
            angle = angle * weights_angle[i]
            if rad_out is None:
                rad_out = rad
                angles_out = angle
            else:
                rad_out += rad
                angles_out += angle

        angles = (((angles_out + torch.pi) * self.frequency.get() + self.rotation.get()) % (2 * torch.pi)) / (2 * torch.pi)

        arr_map = angles

        return arr_map

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "PolarDivision:Points": self.points,
                               visitors + "_" + "PolarDivision:Rotation": self.rotation,
                               visitors + "_" + "PolarDivision:Frequency": self.frequency,
                               visitors + "_" + "PolarDivision:Weights_angle": self.weights_angle}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
