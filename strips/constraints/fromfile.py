from Nodes.constraint import Constraint


class FromFile(Constraint):

    def __init__(self, path):
        super().__init__()
        self.f = open(path, "rb")
        self.x = 0

    def constrain(self, interp):
        return self.x

    def set_frame(self, frame):
        super().set_frame(frame)
        self.f.seek(frame) # TODO mod file size

    def set_next(self):
        super().set_next()
        x = self.f.read(1)
        self.x = int(x[0]) / 255

    def set_previous(self):
        super().set_previous()
        self.set_frame(self.frame-1)
        self.set_next()
