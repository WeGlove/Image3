from Nodes.out import Out
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.value_property import ValueProperty
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.line import Line
from Nodes.pointMapComb import PointMapComb


class NodeFactory:

    def __init__(self, device):
        self.next_id = 0
        self.device = device

    def reset(self):
        self.next_id = 0

    def node_from_dict(self, properties, name):
        if name == "Value Property":
            return self.value_property(**properties)
        elif name == "Animated Property":
            return self.animated_property(**properties)
        elif name == "PointMappingMin":
            return self.pointMappingMin(**properties)
        elif name == "Ouuuuuuuuuuuuuut":
            return self.out(**properties)
        elif name == "Line":
            return self.line(**properties)
        elif name == "Point Map Comb":
            return self.pointMapComb(**properties)
        else:
            raise ValueError(f"Unknown Node {name}")

    def out(self, node_id=None):
        node = Out(device=self.device, node_id=node_id)
        if node_id is None:
            self.next_id += 1
        return node

    def pointMappingMin(self, node_id=None):
        node = PointMappingMin(device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is None:
            self.next_id += 1
        return node

    def animated_property(self, node_id=None):
        node = AnimatedProperty(initial_value=None, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is None:
            self.next_id += 1
        return node

    def value_property(self, initial_value=None, node_id=None):
        node = ValueProperty(initial_value=initial_value, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is None:
            self.next_id += 1
        return node

    def line(self, node_id=None):
        node = Line(line=None, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is None:
            self.next_id += 1
        return node

    def pointMapComb(self, node_id=None):
        node = PointMapComb(device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is None:
            self.next_id += 1
        return node
