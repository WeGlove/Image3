from abc import abstractmethod
import numpy as np


class Compositor:

    def __init__(self):
        self.width = None
        self.height = None
        self.limit = None

    def initialize(self, width, height, limit):
        self.width = width
        self.height = height
        self.limit = limit

    @abstractmethod
    def composite(self, index, img) -> np.ndarray:
        pass
