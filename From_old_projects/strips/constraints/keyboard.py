from Nodes.constraint import Constraint
import keyboard


class KeyboardConstraint(Constraint):

    def __init__(self, key_dict):
        super().__init__()
        self.key_dict = key_dict

    def constrain(self, interp):
        pressed = [v for k, v in self.key_dict.items() if keyboard.is_pressed(k)]
        print(pressed)

        if len(pressed) == 0:
            return interp
        else:
            return pressed[0]

