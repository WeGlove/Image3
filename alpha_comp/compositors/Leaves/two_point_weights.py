from alpha_comp.compositor import Compositor
from alpha_comp.Geos import get_radius
import torch
from strips.animated_property import AnimatedProperty


class TwoPointWeights(Compositor):

    def __init__(self, point_a=None, point_b=None, size=0.1, shift=0, weight_a=1, weight_b=1):
        super().__init__()
        self.point_a = AnimatedProperty(initial_value=point_a)
        self.point_b = AnimatedProperty(initial_value=point_b)
        self.size = AnimatedProperty(size)
        self.shift = AnimatedProperty(shift)
        self.weight_a = AnimatedProperty(initial_value=weight_a)
        self.weight_b = AnimatedProperty(initial_value=weight_b)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.point_a.initial_value is None:
            self.point_a.initial_value = torch.tensor([0, 0], device=self.device)

        if self.point_b.initial_value is None:
            self.point_b.initial_value = torch.tensor([1920, 1080], device=self.device)

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)
        rad_a = get_radius(self.width, self.height, self.device, self.point_a.get()) + self.shift.get()
        rad_b = get_radius(self.width, self.height, self.device, self.point_b.get()) + self.shift.get()

        arr = rad_a * self.weight_a.get() + rad_b * self.weight_b.get()

        arr = (arr * self.size.get()) % self.limit
        arr = torch.floor(arr)
        out_arr[arr == index] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        return {visitors + "_" + "RadialsWarp:Shift": self.shift, visitors + "_" + "RadialsWarp:Size": self.size,
                visitors + "_" + "RadialsWarp:PointA": self.point_a, visitors + "_" + "RadialsWarp:PointB": self.point_b}
