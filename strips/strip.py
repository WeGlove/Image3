from abc import abstractmethod
from typing import Dict
from strips.animated_property import AnimatedProperty


class Strip:

    def __init__(self, length):
        self.length = length
        self.fps = None
        self.initial_frame = None
        self.initial_image = None
        self.device = None
        self.width = None
        self.height = None

    def get_length(self):
        return self.length

    def initialize(self, width, height, fps, initial_frame, initial_image, device):
        self.fps = fps
        self.initial_frame = initial_frame
        self.initial_image = initial_image
        self.device = device
        self.width = width
        self.height = height

    @abstractmethod
    def produce_next(self, last_image):
        pass

    @abstractmethod
    def produce_previous(self, last_image):
        pass

    @abstractmethod
    def set_frame(self, frame):
        pass

    @abstractmethod
    def free(self):
        pass

    def get_animated_properties(self) -> Dict[str, AnimatedProperty]:
        pass
