import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
import keyboard


class KeyboardReader(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.reader = None
        super().__init__([], [self.initial_value], "Keyboard Reader")

    def produce(self):
        return keyboard.is_pressed(self.initial_value.get())
