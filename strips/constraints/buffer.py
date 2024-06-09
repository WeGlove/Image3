from strips.constraint import Constraint


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

    def constrain(self, interp):
        self.buffer.append(self.constraint.constrain(interp))

        if len(self.buffer) > self.n:
            self.buffer = self.buffer[1:]

        return sum(self.buffer) / len(self.buffer)
