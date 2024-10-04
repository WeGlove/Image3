import torch
from Nodes.misc.alpha_comp.compositor import Compositor


class SizeSplit(Compositor):

    def __init__(self, compositor_a, compositor_b):
        super().__init__()
        self.compositor_a = compositor_a
        self.compositor_b = compositor_b

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)

        self.compositor_a.initialize(width, height, limit, self.device)
        self.compositor_b.initialize(width, height, limit, self.device)

    def composite(self, index, img):
        mask_a = self.compositor_a.composite(index, img)
        mask_a = torch.floor(mask_a * 255)
        mask_a = torch.tensor(mask_a, dtype=torch.int32, device=self.device)
        mask_a = mask_a % (torch.ones((self.width, self.height, 3), device=self.device) * 0b11110000)

        mask_b = self.compositor_b.composite(index, img)
        mask_b = torch.tensor(torch.floor(torch.tensor(torch.floor(mask_b * 255), dtype=torch.int32, device=self.device) >> 4), dtype=torch.int32, device=self.device) << 4

        base_mask = (mask_a + mask_b) / 255
        return base_mask

    def get_animated_properties(self, visitors):
        animated_properties = self.compositor_a.get_animated_properties(visitors + "_SizeSplit:CompositorA")
        animated_properties.update(self.compositor_b.get_animated_properties(visitors + "_SizeSplit:CompositorB"))
        return animated_properties
