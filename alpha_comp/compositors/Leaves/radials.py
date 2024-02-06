from alpha_comp.compositor import Compositor
from alpha_comp.Geos import radial, get_polar


class Radials(Compositor):

    def __init__(self):
        super().__init__()
        self.polar = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.polar = get_polar(width, height, device)

    def composite(self, index, img):
        radius_space = min(self.width, self.height) / self.limit
        radius_start = radius_space * index
        radius_end = radius_space * (index + 1)
        arr = radial(self.width, self.height, radius_start, radius_end)

        return arr

