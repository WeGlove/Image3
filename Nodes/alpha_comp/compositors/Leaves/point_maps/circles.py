from Nodes.alpha_comp.Geos import get_polar
import torch
from Nodes.animated_property import AnimatedProperty
import math
from Nodes.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap


class Circles(PointMap):

    def __init__(self, points, scale_radius=1, scale=5, shift=0, ratio=0.5, rotation=0, frequency=1, weights_rad=None):
        self.points = AnimatedProperty(initial_value=points)
        self.rotation = AnimatedProperty(initial_value=rotation)
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.weights_rad = AnimatedProperty(initial_value=weights_rad)
        self.scale = AnimatedProperty(initial_value=scale)
        self.shift = AnimatedProperty(initial_value=shift)
        self.ratio = AnimatedProperty(initial_value=ratio)

        self.angle_space = None

        super().__init__("Circles",
                         [self.points, self.rotation, self.frequency, self.weights_rad, self.scale, self.shift, self.ratio,])

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.weights_rad.initial_value is None:
            self.weights_rad.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)

        self.angle_space = 2 * torch.pi / self.limit

    def composite(self, index, img):
        rad_out = None
        points = self.points.get()
        weights_rad = self.weights_rad.get()
        weights_rad = weights_rad / torch.sum(weights_rad)
        for i in range(points.shape[0]):
            rad, _ = get_polar(self.width, self.height, self.device, points[i])
            rad = rad * weights_rad[i]
            if rad_out is None:
                rad_out = rad
            else:
                rad_out += rad

        rad_out = ((rad_out * self.scale.get() + self.shift.get()) % math.sqrt((self.width/2)**2 + (self.height/2)**2)) / math.sqrt((self.width/2)**2 + (self.height/2)**2)

        arr_map = rad_out

        return arr_map

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "PolarDivision:Points": self.points,
                               visitors + "_" + "PolarDivision:Scale": self.scale,
                               visitors + "_" + "PolarDivision:Shift": self.shift,
                               visitors + "_" + "PolarDivision:Ratio": self.ratio,
                               visitors + "_" + "PolarDivision:Rotation": self.rotation,
                               visitors + "_" + "PolarDivision:Frequency": self.frequency,
                               visitors + "_" + "PolarDivision:Weights_rad": self.weights_rad}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
