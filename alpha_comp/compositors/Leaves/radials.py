import numpy as np
import torch
from alpha_comp.compositor import Compositor
from alpha_comp.Geos import radial, get_polar, radial_map


class Radials(Compositor):

    def __init__(self):
        super().__init__()
        self.polar = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.polar = get_polar(width, height, device)

    def composite(self, index, img):
        highest_radius = np.sqrt((self.width/2) ** 2 + (self.height/2) ** 2)
        radius_space = highest_radius / self.limit
        radius_start = radius_space * index
        radius_end = radius_space * (index + 1)

        arr = radial(self.width, self.height, self.polar, radius_start,
                     radius_end, self.device)

        return arr


class RadialsWrap(Compositor):

    def __init__(self, shift=0):
        super().__init__()
        self.polar = None
        self.r_map = None
        self.shift = shift

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.polar = get_polar(width, height, device)
        self.r_map = radial_map(self.polar + self.shift, limit, 1/100)

    def composite(self, index, img):
        arr = torch.zeros(self.width, self.height, 3, device=self.device)
        arr[self.r_map == index] = 1

        return arr
