import random
from src.Nodes.node import Node


class Random(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value=""):
        super().__init__(node_id, factory_id, "Returns the given value.", frame_counter, [], device, [])

    def produce(self):
        return random.random()

    @staticmethod
    def get_node_name():
        return "Random"
