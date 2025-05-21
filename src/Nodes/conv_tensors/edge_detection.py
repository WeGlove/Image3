import torch
from src.Nodes.node import Node


class EdgeDetection(Node):

    def __init__(self, node_id, factory_id, device, initial_value="."):
        self.reader = None
        super().__init__(node_id, factory_id, "Edge Detection", [], device, [])

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
