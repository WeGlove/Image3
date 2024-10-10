import torch
from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class MassAlpha(Node):

    def __init__(self, node_id, factory_id, frame_counter, device):
        self.frame_counter = frame_counter
        self.device = device
        self.noso_images = NodeSocket(False, "Images", None)
        self.noso_compositor_a = NodeSocket(False, "Compositor A", None)
        self.noso_compositor_b = NodeSocket(False, "Compositor B", None)
        self.noso_compositor_c = NodeSocket(False, "Compositor C", None)
        self.images = []
        super().__init__(node_id, factory_id, "Mass Alpha", frame_counter,
                         [self.noso_images, self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c], device, [])

    def produce(self):
        masks = [self.noso_compositor_a.get().produce() % 1 * len(self.images),
                 self.noso_compositor_b.get().produce() % 1 * len(self.images),
                 self.noso_compositor_c.get().produce() % 1 * len(self.images)]
        mask = torch.stack(masks).transpose(0, 2)

        stack_img = torch.zeros(mask.shape, device=self.device)
        for i in range(len(self.images) - 1):
            img_a = self.images[i]
            img_b = self.images[i+1]

            img_a_alpha = img_a * torch.clamp(mask - i, 0, 1)
            img_b_alpha = img_b * (1-torch.clamp(mask - i, 0, 1))
            img_b_alpha[img_b_alpha == 1] = 0

            stack_img = img_a_alpha + img_b_alpha

        return stack_img

    def initialize(self, width, height, *args):
        self.images = self.noso_images.get().initialize(width, height, *args)
        self.noso_compositor_a.get().initialize(width, height, *args)
        self.noso_compositor_b.get().initialize(width, height, *args)
        self.noso_compositor_c.get().initialize(width, height, *args)

    @staticmethod
    def get_node_name():
        return "Mass Alpha"
