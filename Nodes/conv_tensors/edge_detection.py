import torch
from Nodes.node import Node


class EdgeDetection(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.reader = None
        super().__init__(node_id, factory_id, "Edge Detection", frame_counter, [], device, [])

    def produce(self):
        mask = torch.tensor([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ], device=self.device, dtype=torch.float)
        return mask

    @staticmethod
    def get_node_name():
        return "Edge Detection"
