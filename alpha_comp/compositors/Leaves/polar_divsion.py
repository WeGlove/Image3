from alpha_comp.compositor import Compositor
from alpha_comp.Geos import get_polar
import torch
from strips.animated_property import AnimatedProperty
import math


class PolarDivision(Compositor):

    def __init__(self, points, scale_radius=1, scale=5, shift=0, ratio=0.5, rotation=0, frequency=1, weights_rad=None, weights_angles=None):
        super().__init__()
        self.points = AnimatedProperty(initial_value=points)
        self.rotation = AnimatedProperty(initial_value=rotation)
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.weights_rad = AnimatedProperty(initial_value=weights_rad)
        self.weights_angle = AnimatedProperty(initial_value=weights_angles)
        self.scale = AnimatedProperty(initial_value=scale)
        self.shift = AnimatedProperty(initial_value=shift)
        self.ratio = AnimatedProperty(initial_value=ratio)

        self.angle_space = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.weights_rad.initial_value is None:
            self.weights_rad.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)
        if self.weights_angle.initial_value is None:
            self.weights_angle.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)

        self.angle_space = 2 * torch.pi / self.limit

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        rad_out = None
        angles_out = None
        points = self.points.get()
        weights_rad = self.weights_rad.get()
        weights_rad = weights_rad / torch.sum(weights_rad)
        weights_angle = self.weights_angle.get()
        weights_angle = weights_angle / torch.sum(weights_angle)
        for i in range(points.shape[0]):
            rad, angle = get_polar(self.width, self.height, self.device, points[i])
            rad = rad * weights_rad[i]
            angle = angle * weights_angle[i]
            if rad_out is None:
                rad_out = rad
                angles_out = angle
            else:
                rad_out += rad
                angles_out += angle

        print(self.shift.get())
        angles = (((angles_out + torch.pi) * self.frequency.get() + self.rotation.get()) % (2 * torch.pi)) / (2 * torch.pi)
        rad_out = ((rad_out * self.scale.get() + self.shift.get()) % math.sqrt((self.width/2)**2 + (self.height/2)**2)) / math.sqrt((self.width/2)**2 + (self.height/2)**2)

        ratio = self.ratio.get()
        arr_map = (angles * ratio + rad_out * (1-ratio))

        arr = torch.floor(arr_map * self.limit)
        out_arr[arr == index] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "PolarDivision:Points": self.points,
                               visitors + "_" + "PolarDivision:Scale": self.scale,
                               visitors + "_" + "PolarDivision:Shift": self.shift,
                               visitors + "_" + "PolarDivision:Ratio": self.ratio,
                               visitors + "_" + "PolarDivision:Rotation": self.rotation,
                               visitors + "_" + "PolarDivision:Frequency": self.frequency,
                               visitors + "_" + "PolarDivision:Weights_rad": self.weights_rad,
                               visitors + "_" + "PolarDivision:Weights_angle": self.weights_angle}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
