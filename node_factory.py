from Nodes.out import Out
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.value_property import ValueProperty
from Nodes.animated_property import AnimatedProperty


class NodeFactory:

    def __init__(self, device):
        self.next_id = 0
        self.device = device

    def out(self):
        node = Out(device=self.device, node_id=self.next_id)
        self.next_id += 1
        return node

    def pointMappingMin(self, maps):
        node = PointMappingMin(maps, device=self.device, node_id=self.next_id)
        self.next_id += 1
        return node

    def animated_poperty(self):
        node = AnimatedProperty(initial_value=None, device=self.device, node_id=self.next_id)
        self.next_id += 1
        return node

    def value_property(self):
        node = ValueProperty(initial_value=None, device=self.device, node_id=self.next_id)
        self.next_id += 1
        return node
