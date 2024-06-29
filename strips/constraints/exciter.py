from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class Exciter(Node):

    def __init__(self, device, node_id, frame_counter):
        self.noso_limit = NodeSocket(False, "Limit", None)
        self.noso_input = NodeSocket(False, "Input", None)
        self.noso_default = NodeSocket(False, "Default", None)
        self.accumulator = 0
        self.impulse = NodeSocket(False, "Impulse", None)
        super().__init__(node_id, "Exciter", frame_counter,
                         [self.noso_limit, self.noso_input, self.impulse, self.noso_default], device, [])

    def produce(self, *args):
        acc_in = self.noso_input.get().produce()
        self.accumulator += acc_in

        limit = self.noso_limit.get().produce()

        if self.accumulator > limit:
            self.accumulator %= limit

            return self.impulse.get().produce(*args)
        else:
            return self.noso_default.get().produce(*args)

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.accumulator = 0
