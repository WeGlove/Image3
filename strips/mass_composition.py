import torch
from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class MassComposition(Node):

    def __init__(self, frame_counter, device):
        self.frame_counter = frame_counter
        self.device = device
        self.noso_images = NodeSocket(False, "Images", None)
        self.noso_compositor = NodeSocket(False, "Compositor", None)
        super().__init__("MassCompositon", "MassCompositon", "Mass Composition",
                         frame_counter, [self.noso_images, self.noso_compositor], device, [])

    def produce(self):
        stack_img = None

        for i, img in enumerate(self.images):
            if stack_img is None:
                stack_img = torch.zeros(img.shape, device=self.device)

            mask = self.compositor.produce(i, img)

            stack_img = stack_img + torch.multiply(img, mask.transpose(0, 1))

        return stack_img

