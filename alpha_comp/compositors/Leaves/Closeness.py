import torch
from alpha_comp.compositor import Compositor
from strips.animated_property import AnimatedProperty


class Closeness(Compositor):

    def __init__(self, comp_img, rev=True, weights=None):
        super().__init__()
        self.block_mask = None
        self.comp_img = AnimatedProperty(comp_img)
        self.rev = rev
        self.weights = AnimatedProperty(weights)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.block_mask = torch.ones((width, height), device=self.device)
        if self.weights.initial_value is None:
            self.weights.initial_value = torch.tensor([1]*self.limit)

    def composite(self, index, img):
        if index == 0:
            self.block_mask = torch.ones((self.width, self.height), device=self.device)
        weights = self.weights.get()
        weights = weights / torch.sum(weights)
        weights *= self.width * self.height
        weights = torch.floor(weights)

        mask = torch.zeros((self.width, self.height), device=self.device)

        a = torch.abs(img / 255 - self.comp_img.get())
        a = torch.tensor(a, dtype=torch.float32)

        brightness = torch.mean(a, dim=2).T
        if self.rev:
            brightness = 1 - brightness
        brightness = brightness * self.block_mask
        size = int(weights[index])
        b = torch.argsort(brightness.flatten())
        brightness_sorted = torch.flip(b, [0])
        highest_indices = brightness_sorted[:size]

        mask = mask.flatten()
        mask[highest_indices] = 1
        mask = torch.reshape(mask, (self.width, self.height))

        self.block_mask = self.block_mask.flatten()
        self.block_mask[highest_indices] = -1
        self.block_mask = torch.reshape(self.block_mask, (self.width, self.height))

        mask = torch.stack([mask, mask, mask])
        mask = torch.transpose(mask, 0, 1).transpose(1, 2)
        return mask

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_" + "Closeness:Weights": self.weights, visitors + "_" + "Closeness:Image": self.comp_img}

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
