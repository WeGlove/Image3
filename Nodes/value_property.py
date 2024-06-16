from Nodes.Node import Node


class ValueProperty(Node):

    def __init__(self, initial_value, device):
        super().__init__("Value Property", [], device)
        self.keyframes = []
        self.initial_value = initial_value

    def set_value(self, x):
        self.initial_value = x

    def set_anim_style(self, style):
        pass

    def set_key_frame(self, frame, value):
        pass

    def get(self):
        return self.initial_value

    def set_next(self):
        pass

    def set_previous(self):
        pass

    def set_frame(self, frame):
        pass

    def is_animated(self):
        return False

    def set_constraint(self, constraint):
        ...

    def is_constrained(self):
        return False

    def get_animated_properties(self, _):
        return {}

    def to_dict(self):
        return {"Value": self.initial_value}
