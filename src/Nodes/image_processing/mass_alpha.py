import time
import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class MassAlpha(Node):

    def __init__(self):
        self.noso_images = NodeSocket("Images")
        self.noso_compositor_a = NodeSocket("Compositor A")
        self.noso_compositor_b = NodeSocket("Compositor B")
        self.noso_compositor_c = NodeSocket("Compositor C")
        super().__init__([self.noso_images, self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c], [],
                         "Mass Alpha")

    def produce(self):
        images = self.noso_images.get().produce()

        masks = [self.noso_compositor_a.get().produce(),
                 self.noso_compositor_b.get().produce(),
                 self.noso_compositor_c.get().produce()]
        mask = torch.stack(masks).transpose(0, 1).transpose(1, 2)
        mask = mask % 1
        mask = mask * len(images)
        mask_floor = torch.floor(mask)

        stack_img = torch.zeros(mask.shape, device=self.defaults.device)
        for i in range(len(images) - 1):
            img_a = images[i]
            img_b = images[i + 1]
            img_a_alpha = img_a * (1-torch.clamp(mask - i, 0, 1))
            img_b_alpha = img_b * torch.clamp(mask - i, 0, 1)
            img_b_alpha[img_b_alpha == 1] = 0
            combined_img = img_a_alpha + img_b_alpha

            stack_img[(mask_floor == i)] = combined_img[(mask_floor == i)]

        return stack_img
