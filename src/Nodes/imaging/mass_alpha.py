import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class MassAlpha(Node):

    def __init__(self):
        self.noso_images = NodeSocket(False, "Images", None)
        self.noso_compositor_a = NodeSocket(False, "Compositor A", None)
        self.noso_compositor_b = NodeSocket(False, "Compositor B", None)
        self.noso_compositor_c = NodeSocket(False, "Compositor C", None)
        self.images = []
        super().__init__([self.noso_images, self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c], [],
                         "Mass Alpha")

    def produce(self):
        masks = [self.noso_compositor_a.get().produce() % 1 * len(self.images),
                 self.noso_compositor_b.get().produce() % 1 * len(self.images),
                 self.noso_compositor_c.get().produce() % 1 * len(self.images)]
        mask = torch.stack(masks).transpose(0, 2)

        stack_img = torch.zeros(mask.shape, device=self.defaults.device)
        for i in range(len(self.images) - 1):
            img_a = self.images[i]
            img_b = self.images[i+1]

            img_a_alpha = img_a * torch.clamp(mask - i, 0, 1)
            img_b_alpha = img_b * (1-torch.clamp(mask - i, 0, 1))
            img_b_alpha[img_b_alpha == 1] = 0

            stack_img = img_a_alpha + img_b_alpha

        return stack_img
