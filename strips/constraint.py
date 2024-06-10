from abc import abstractmethod


class Constraint:

    def __init__(self):
        self.frame = 0

    @abstractmethod
    def constrain(self, interp):
        pass

    def set_next(self):
        self.frame += 1

    def set_previous(self):
        self.frame -= 1

    def set_frame(self, frame):
        self.frame = frame

    def to_dict(self):
        return {"Constraint": None}

    @abstractmethod
    def get_animated_properties(self, visitors):
        return {}
