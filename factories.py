from Nodes.out import Out
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.value_property import ValueProperty
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.line import Line
from Nodes.pointMapComb import PointMapComb
from From_old_projects.strips.constraints.fromfile import FromFile
from From_old_projects.strips.constraints.buffer import MeanBuffer, WeightBuffer
from From_old_projects.strips.constraints.exciter import Exciter
from Nodes.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.alpha_comp.compositors.Leaves.point_maps.circles import Circles
from Nodes.alpha_comp.compositors.Leaves.point_maps.spirals import Spirals
from Nodes.mass_composition import MassComposition
from node_factory import NodeFactory


def get_misc_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, PointMappingMin, ValueProperty, AnimatedProperty, Line, PointMapComb, FromFile, MeanBuffer,
                WeightBuffer, Exciter, PointMapping, Circles, Spirals, MassComposition]}
    factory = NodeFactory(device, frame_counter, in_dict, "Misc")
    return factory
