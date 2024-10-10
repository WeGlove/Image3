import math
import torch
from Nodes.maps.alpha_comp.Geos import get_centered_vector_map
from Nodes.system.animated_property import AnimatedProperty
from Nodes.maps.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap


class Lines(PointMap):

    def __init__(self, frequency=1, shift=0, rotation=0):
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.shift = AnimatedProperty(initial_value=shift)
        self.rotation = AnimatedProperty(rotation)
        self.center = AnimatedProperty(None)
        super().__init__("Lines", [self.frequency, self.shift, self.rotation, self.center])

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.center.initial_value = torch.tensor([1920/2, 1080/2], device=self.device)

    def composite(self, index, img):
        vector_map = get_centered_vector_map(self.width, self.height, self.device, center=self.center.get())

        vector_map = torch.abs(math.cos(self.rotation.get()/360 * 2*math.pi) * -vector_map[:, :, 1] -
                               math.sin(self.rotation.get()/360 * 2*math.pi) * -vector_map[:, :, 0])

        vector_map = (vector_map * self.frequency.get() + self.shift.get())
        border = min(self.width, self.height) / 2
        vector_map = vector_map % border
        vector_map = torch.abs(vector_map)
        vector_map = vector_map / border

        return vector_map

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_Lines:Frequency": self.frequency,
                               visitors + "_Lines:Shift": self.shift,
                               visitors + "_Lines:Rotation": self.rotation,
                               visitors + "_Lines:Center": self.center
                               }

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
