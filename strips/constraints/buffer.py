from Nodes.constraint import Constraint


class Buffer(Constraint):

    def __init__(self, constraint, n):
        super().__init__()
        self.constraint = constraint
        self.buffer = []
        self.n = n

    def constrain(self, interp):
        self.buffer.append(self.constraint.constrain(interp))

        if len(self.buffer) > self.n:
            val = self.buffer[0]
            self.buffer = self.buffer[1:]
            return val

        return self.buffer[0]


class MeanBuffer(Constraint):

    def __init__(self, constraint, n):
        super().__init__()
        self.constraint = constraint
        self.buffer = []
        self.n = n
        self.has_constrained = False

    def constrain(self, interp):
        if not self.has_constrained:
            self.buffer.append(self.constraint.constrain(interp))
            if len(self.buffer) > self.n:
                self.buffer = self.buffer[1:]

            self.has_constrained = True

        return sum(self.buffer) / len(self.buffer)

    def set_frame(self, frame):
        super().set_frame(frame)
        self.constraint.set_frame(frame)
        self.has_constrained = False

    def set_next(self):
        super().set_next()
        self.constraint.set_next()
        self.has_constrained = False

    def set_previous(self):
        super().set_previous()
        self.constraint.set_previous()
        self.has_constrained = False
