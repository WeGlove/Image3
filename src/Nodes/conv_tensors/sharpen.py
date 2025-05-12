import torch
from src.Nodes.node import Node


class Sharpen(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.reader = None
        super().__init__(node_id, factory_id, "Mean Tensor", frame_counter, [], device, [])

    def produce(self):
        mask = torch.tensor([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], device=self.device, dtype=torch.float)
        return mask

    @staticmethod
    def get_node_name():
        return "Sharpen"
