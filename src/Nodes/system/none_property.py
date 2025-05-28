from src.Nodes.node import Node


class NoneProperty(Node):

    def __init__(self):
        super().__init__([], [], "Returns the given value.")

    def produce(self):
        return None
