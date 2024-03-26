import math
import torch
from alpha_comp.compositor import Compositor
from alpha_comp.Geos import get_centered_vector_map
from strips.animated_property import AnimatedProperty


class Lines(Compositor):

    def __init__(self, frequency=10, shift=0, rotation=0):
        super().__init__()
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.shift = AnimatedProperty(initial_value=shift)
        self.rotation = AnimatedProperty(rotation)
        self.center = AnimatedProperty(None)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.center.initial_value = torch.tensor([1920/2, 1080/2], device=self.device)

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        vector_map = get_centered_vector_map(self.width, self.height, self.device, center=self.center.get())
        vector_map = torch.abs(math.cos(self.rotation.get()) * -vector_map[:, :, 1] -
                               math.sin(self.rotation.get()) * -vector_map[:, :, 0])
        vector_map = (vector_map + self.shift.get()) * self.frequency.get()
        vector_map = vector_map % 1
        vector_map = vector_map * self.limit
        vector_map = torch.floor(vector_map)
        out_arr[vector_map == index] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_Lines:Frequency": self.frequency,
                               visitors + "_Lines:Shift": self.shift,
                               visitors + "_Lines:Rotation": self.rotation,
                               visitors + "_Lines:Center": self.center}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
