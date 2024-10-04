import torch
from Nodes.out import Out
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.value_property import ValueProperty
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.line import Line
from Nodes.pointMapComb import PointMapComb
from strips.constraints.fromfile import FromFile
from strips.constraints.buffer import MeanBuffer, WeightBuffer
from strips.constraints.exciter import Exciter
from Nodes.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.alpha_comp.compositors.Leaves.point_maps.circles import Circles
from Nodes.alpha_comp.compositors.Leaves.point_maps.spirals import Spirals
from strips.mass_composition import MassComposition


class NodeFactory:

    def __init__(self, device, frame_counter):
        self.next_id = 0
        self.device = device
        self.frame_counter = frame_counter

        self.in_dict = {
            node.get_node_name(): node
                for node in
            [Out, PointMappingMin, ValueProperty, AnimatedProperty, Line, PointMapComb,FromFile,MeanBuffer, WeightBuffer,
             Exciter, PointMapping, Circles, Spirals, MassComposition]
        }

    def reset(self):
        self.next_id = 0

    def set_next(self, x):
        self.next_id = x

    def node_from_dict(self, properties, name):
        if name in self.in_dict:
            return self.instantiate(name, node_id, properties)
        else:
            raise ValueError(f"Unknown Node {name}")

    def instantiate(self, node_name, node_id=None, **properties):
        node = self.in_dict[node_name](device=self.device, node_id=self.next_id if node_id is None else node_id,
                                       frame_counter=self.frame_counter, **properties)
        if node_id is None:
            self.next_id += 1
        return node
