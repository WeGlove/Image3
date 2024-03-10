from abc import abstractmethod


class Constraint:

    def __init__(self):
        self.frame = 0

    @abstractmethod
    def constrain(self, interp):
        pass

    def set_frame(self, frame):
        self.frame = frame

    @abstractmethod
    def get_animated_properties(self, visitors):
        return {}
