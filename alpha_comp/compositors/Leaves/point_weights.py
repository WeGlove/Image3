from alpha_comp.compositor import Compositor
from alpha_comp.Geos import get_radius
import torch
from strips.animated_property import AnimatedProperty


class PointWeights(Compositor):

    def __init__(self, points, size=0.1, shift=0, weights=None):
        super().__init__()
        self.points = AnimatedProperty(initial_value=points)
        self.size = AnimatedProperty(size)
        self.shift = AnimatedProperty(shift)
        self.weights = AnimatedProperty(initial_value=weights)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.weights.initial_value is None:
            self.weights.initial_value = torch.tensor([1/self.limit]*self.points.get().shape[0], device=self.device)

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        rad_out = None
        points = self.points.get()
        weights = self.weights.get()
        weights = weights / torch.sum(weights)
        for i in range(points.shape[0]):
            rad = get_radius(self.width, self.height, self.device, self.points.get()[i]) * weights[i] + self.shift.get()
            if rad_out is None:
                rad_out = rad
            else:
                rad_out += rad

        rad_out = (rad_out * self.size.get()) % self.limit
        arr = torch.floor(rad_out)
        out_arr[arr == index] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        return {visitors + "_" + "PointWeights:Shift": self.shift, visitors + "_" + "PointWeights:Size": self.size,
                visitors + "_" + "PointWeights:Points": self.points, visitors + "_" + "PointWeights:Weights": self.weights}
