from src.serializable import Serializable


class Defaults(Serializable):

    def __init__(self, width, height, device):
        self.width = width
        self.height = height
        self.device = device

        self.width_dim = -3
        self.height_dim = -2
        self.color_dim = -1

        self.dimensions = [self.width, self.height]
        self.dimensions = tuple(self.dimensions)

    def serialize(self):
        return {
            "width": self.width,
            "height": self.height,
            "device": self.device if type(self.device) == str else self.device.type
        }

    @staticmethod
    def deserialize(obj):
        return Defaults(obj["width"], obj["height"], obj["device"])
