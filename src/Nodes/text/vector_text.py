import torch
from src.Nodes.internal.internal_value import InternalValue
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class VectorText(Node):

    def __init__(self):
        self.text = NodeSocket("Text", default=InternalValue("Hello World!"))
        self.fontsize = NodeSocket("Font Size", default=InternalValue(60))
        self.font = NodeSocket("Font", default=InternalValue("arial.ttf"))
        super().__init__([self.text, self.fontsize, self.font])
        self.image = None
        self.draw = None

    def produce(self):
        text = self.text.get().produce()
        font = ImageFont.truetype(self.font.get().produce(), self.fontsize.get().produce())

        return {"text": text, "font": font}