from Nodes.out import Out
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.value_property import ValueProperty
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.line import Line


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
            return self.animated_poperty(**properties)
        elif name == "Point":
            return self.pointMappingMin(**properties)
        elif name == "Ouuuuuuuuuuuuuut":
            return self.out(**properties)
        elif name == "Line":
            return self.line(**properties)
        else:
            raise ValueError()

    def out(self, node_id=None):
        node = Out(device=self.device, node_id=node_id)
        if node_id is not None:
            self.next_id += 1
        return node

    def pointMappingMin(self, maps, node_id=None):
        node = PointMappingMin(maps, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is not None:
            self.next_id += 1
        return node

    def animated_poperty(self, node_id=None):
        node = AnimatedProperty(initial_value=None, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is not None:
            self.next_id += 1
        return node

    def value_property(self, initial_value=None, node_id=None):
        node = ValueProperty(initial_value=initial_value, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is not None:
            self.next_id += 1
        return node

    def line(self, node_id=None):
        node = Line(line=None, device=self.device, node_id=self.next_id if node_id is None else node_id)
        if node_id is not None:
            self.next_id += 1
        return node

