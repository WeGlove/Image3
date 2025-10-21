import torch
from src.Nodes.internal.internal_value import InternalValue
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from PIL import Image, ImageDraw
import numpy as np


class RenderText(Node):

    def __init__(self):
        self.text = NodeSocket("Text", default=InternalValue("Hello World!"))
        super().__init__([self.text])
        self.image = None
        self.draw = None

    def produce(self):
        texts = self.text.get().produce()

        image = Image.new("RGBA", self.defaults.dimensions, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for text in texts:
            draw.text((10, 0), text["text"], (0, 0, 0), font=text["font"])

        img = np.array(image)
        return torch.tensor(img, device=self.defaults.device).transpose(0, 1)
