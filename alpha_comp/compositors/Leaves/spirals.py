from alpha_comp.compositor import Compositor
import torch
from alpha_comp.Geos import get_polar
from strips.animated_property import AnimatedProperty


class Spirals(Compositor):

    def __init__(self, scale=0.001, rotation=0, frequency=1):
        super().__init__()
        self.scale = AnimatedProperty(initial_value=scale)
        self.rotation = AnimatedProperty(initial_value=rotation)
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.angle_space = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.angle_space = 2*torch.pi / self.limit

    def composite(self, index, img):
        arr = torch.zeros((self.width, self.height), device=self.device)
        angle_start = self.angle_space * index
        angle_end = self.angle_space * (index + 1)

        radius, angles = get_polar(self.width, self.height, self.device)
        angles = (angles+torch.pi) + radius * self.scale.get()
        angles = (angles * self.frequency.get() + self.rotation.get()) % (2*torch.pi)

        arr[torch.logical_and(angle_start < angles, angles < angle_end)] = 1

        arr = torch.stack([arr, arr, arr]).transpose(0, 1).transpose(1, 2)

        return arr

    def get_animated_properties(self, visitors):
        return {visitors + "_" + "Spirals:Scale": self.scale, visitors + "_" + "Spirals:Rotation": self.rotation,
                visitors + "_" + "Spirals:Frequency": self.frequency}