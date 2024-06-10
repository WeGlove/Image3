from typing import List


class Node:

    def __init__(self, node_name):
        self.node_name = node_name
        self.subnodes: List[Node] = []
        self.animated_properties = []

    def set_subnodes(self, subnodes):
        self.subnodes = subnodes

    def set_animated_properties(self, animated_properties):
        self.animated_properties = animated_properties

    def to_dict(self):
        return {self.node_name: {"Subnodes": {k: subnode.to_dict() for k, subnode in enumerate(self.subnodes)},
                                 "AnimatedProperties": [animated_property.to_dict() for animated_property in self.animated_properties]}}
