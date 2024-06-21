from abc import abstractmethod
from Nodes.Node import Node


class Constraint(Node):

    def __init__(self, device, node_id):
        super().__init__(node_id, "Constraint", [], device)
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

    def get_animated_properties(self):
        return []
