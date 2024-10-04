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
            "Value Property": self.value_property,
            "Animated Property": self.animated_property,
            "PointMappingMin": self.pointMappingMin,
            "Ouuuuuuuuuuuuuut": self.out,
            "Line": self.line,
            "Point Map Comb": self.pointMapComb,
            "FromFile": self.fromfile,
            "MeanBuffer": self.meanBuffer,
            "Exciter": self.exciter,
            "WeightBuffer": self.weightbuffer,
            "PointMapping": self.pointMapping,
            "Circles": self.circles,
            "Spirals": self.spirals,
            "MassComposition": self.mass_composition
        }

    def reset(self):
        self.next_id = 0

    def set_next(self, x):
        self.next_id = x

    def node_from_dict(self, properties, name):
        if name in self.in_dict:
            self.in_dict[name](**properties)
            return self.value_property(**properties)
        else:
            raise ValueError(f"Unknown Node {name}")

    def out(self, node_id=None):
        node = Out(device=self.device, node_id=self.next_id if node_id is None else node_id,
                   frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def pointMappingMin(self, node_id=None):
        node = PointMappingMin(device=self.device, node_id=self.next_id if node_id is None else node_id,
                               frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def animated_property(self, node_id=None, keyframes=None):
        if keyframes is not None:
            keyframes = [(frame, torch.tensor(value, device=self.device) if type(value) == list else value)
                         for (frame, value) in keyframes]
        node = AnimatedProperty(keyframes=keyframes, initial_value=None, device=self.device,
                                node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def value_property(self, initial_value=None, node_id=None):
        if type(initial_value) == list:
            initial_value = torch.tensor(initial_value, device=self.device)
        node = ValueProperty(initial_value=initial_value, device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def line(self, node_id=None):
        node = Line(line=None, device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def pointMapComb(self, node_id=None):
        node = PointMapComb(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def fromfile(self, node_id=None):
        node = FromFile(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def meanBuffer(self, node_id=None):
        node = MeanBuffer(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def exciter(self, node_id=None):
        node = Exciter(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def weightbuffer(self, node_id=None):
        node = WeightBuffer(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def pointMapping(self, node_id=None):
        node = PointMapping(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def circles(self, node_id=None):
        node = Circles(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def spirals(self, node_id=None):
        node = Spirals(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

    def mass_composition(self, node_id=None):
        node = MassComposition(device=self.device, node_id=self.next_id if node_id is None else node_id, frame_counter=self.frame_counter)
        if node_id is None:
            self.next_id += 1
        return node

