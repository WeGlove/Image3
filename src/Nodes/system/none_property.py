from src.Nodes.node import Node


class NoneProperty(Node):

    def __init__(self):
        super().__init__([], [], "Returns None.")

    def produce(self):
        return None
