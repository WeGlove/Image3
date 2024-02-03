from alpha_comp.compositor import Compositor
from alpha_comp.Geos import radial


class Radials(Compositor):

    def composite(self, index, img):
        radius_space = min(self.width, self.height) / self.limit
        radius_start = radius_space * index
        radius_end = radius_space * (index + 1)
        arr = radial(self.width, self.height, radius_start, radius_end)

        return arr
