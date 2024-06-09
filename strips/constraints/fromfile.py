from strips.constraint import Constraint


class FromFile(Constraint):

    def __init__(self, path):
        super().__init__()
        self.f = open(path, "rb")
        self.x = 0

    def constrain(self, interp):
        return self.x

    def set_frame(self, frame):
        super().set_frame(frame)
        x = self.f.read(1)
        self.x = int(x[0]) / 255
