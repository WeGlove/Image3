from src.Nodes.node import Node
from src.Nodes import NodeSocket


class WeightBuffer(Node):

    def __init__(self, device, node_id, frame_counter):
        self.acc = 0
        self.acc_in = NodeSocket(False, "Input", None)
        self.reduce = NodeSocket(False, "Reduce", None)
        super().__init__(node_id, "WeightBuffer", frame_counter, [self.acc_in, self.reduce], device, [])

    def produce(self, *args):
        self.acc = self.acc * self.reduce.get().produce() + self.acc_in.get().produce() * (1-self.reduce.get().produce())
        return self.acc

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.acc = 0


class MeanBuffer(Node):

    def __init__(self, device, node_id, frame_counter):
        self.noso_in = NodeSocket(False, "In", None)
        self.buffer = []
        self.n = NodeSocket(False, "n", None)
        super().__init__(node_id, "MeanBuffer", frame_counter, [self.noso_in, self.n], device, [])

    def produce(self, *args):
        self.buffer.append(self.noso_in.get().produce(*args))
        if len(self.buffer) > self.n.get().produce():
            self.buffer = self.buffer[-self.n.get().produce():]

        print(self.buffer)

        return sum(self.buffer) / len(self.buffer)

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.buffer = []
