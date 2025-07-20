import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class MassComposition(Node):

    def __init__(self):
        self.noso_images = NodeSocket("Images")
        self.noso_compositor_a = NodeSocket("Compositor A")
        self.noso_compositor_b = NodeSocket("Compositor B")
        self.noso_compositor_c = NodeSocket("Compositor C")
        super().__init__([self.noso_images, self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c], [],
                         "")

    def produce(self):
        images = self.noso_images.get().produce()

        masks = [torch.round(self.noso_compositor_a.get().produce() % 1 * (len(images)-1)),
                 torch.round(self.noso_compositor_b.get().produce() % 1 * (len(images)-1)),
                 torch.round(self.noso_compositor_c.get().produce() % 1 * (len(images)-1))]
        mask = torch.stack(masks).transpose(0, 1).transpose(1, 2)

        stack_img = torch.zeros(mask.shape, device=self.defaults.device)
        for i, img in enumerate(images):
            stack_img[(mask == i)] = images[i][(mask == i)]

        return stack_img
