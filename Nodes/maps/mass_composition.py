import torch
from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class MassComposition(Node):

    def __init__(self, node_id, factory_id, frame_counter, device):
        self.frame_counter = frame_counter
        self.device = device
        self.noso_images = NodeSocket(False, "Images", None)
        self.noso_compositor = NodeSocket(False, "Compositor", None)
        self.images = []
        super().__init__(node_id, factory_id, "", frame_counter, [self.noso_images, self.noso_compositor], device, [])

    def produce(self):
        mask = torch.round(self.noso_compositor.get().produce() % 1 * len(self.images))
        mask = torch.stack([mask, mask, mask]).transpose(0, 2)

        stack_img = torch.zeros(mask.shape, device=self.device)
        for i, img in enumerate(self.images):
            stack_img[(mask == i)] = self.images[i][(mask == i)]

        return stack_img

    def initialize(self, width, height, *args):
        self.images = self.noso_images.get().initialize(width, height, *args)
        self.noso_compositor.get().initialize(width, height, *args)

    @staticmethod
    def get_node_name():
        return "Mass Composition"
