import torch
from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class Mean(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.size = NodeSocket(False, "Size", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Mean Tensor", frame_counter, [self.size], device, [])

    def produce(self):
        size = self.size.get().produce()
        mask = torch.ones((int(size), int(size)), device=self.device)
        mask = mask / size
        return mask

    @staticmethod
    def get_node_name():
        return "Mean"
