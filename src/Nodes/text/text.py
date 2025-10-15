import torch
from src.Nodes.internal.internal_value import InternalValue
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Text(Node):

    def __init__(self):
        self.text = NodeSocket("Text", default=InternalValue("Hello World!"))
        self.fontsize = NodeSocket("Font Size", default=InternalValue(60))
        self.font = NodeSocket("Font", default=InternalValue("arial.ttf"))
        super().__init__([self.text, self.fontsize, self.font])
        self.image = None
        self.draw = None

    def produce(self):
        text = self.text.get().produce()

        image = Image.new("RGBA", self.defaults.dimensions, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(self.font.get().produce(), self.fontsize.get().produce())

        draw.text((10, 0), text, (0, 0, 0), font=font)
        img = np.array(image)

        return torch.tensor(img, device=self.defaults.device).transpose(0, 1)
