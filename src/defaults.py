from src.serializable import Serializable


class Defaults(Serializable):

    def __init__(self, width, height, device):
        self.width = width
        self.height = height
        self.device = device

        self.width_dim = 0
        self.height_dim = 1

        self.dimensions = [0, 0]
        self.dimensions[self.width_dim] = self.width
        self.dimensions[self.height_dim] = self.height
        self.dimensions = tuple(self.dimensions)

    def serialize(self):
        return {
            "width": self.width,
            "height": self.height,
            "device": self.device.type
        }

    @staticmethod
    def deserialize(obj):
        return Defaults(obj["width"], obj["height"], obj["device"])
