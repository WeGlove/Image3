from abc import abstractmethod


class PointMap:

    def __init__(self):
        self.device = None
        self.limit = None
        self.width = None
        self.height = None

    def initialize(self, width, height, limit, device=None):
        self.device = device
        self.limit = limit
        self.width = width
        self.height = height

    @abstractmethod
    def composite(self, index, img):
        pass

    def get_animated_properties(self, visitors):
        pass
