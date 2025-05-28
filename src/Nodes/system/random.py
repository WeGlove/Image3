import random
from src.Nodes.node import Node


class Random(Node):

    def __init__(self):
        super().__init__([], [], "Returns the given value.")

    def produce(self):
        return random.random()
