from Nodes.system.out import Out
from Nodes.misc.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.system.value_property import ValueProperty
from Nodes.system.animated_property import AnimatedProperty
from Nodes.misc.alpha_comp.compositors.Leaves.point_maps.line import Line
from Nodes.misc.pointMapComb import PointMapComb
from From_old_projects.strips.constraints.fromfile import FromFile
from From_old_projects.strips.constraints.buffer import MeanBuffer, WeightBuffer
from From_old_projects.strips.constraints.exciter import Exciter
from Nodes.misc.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.misc.alpha_comp.compositors.Leaves.point_maps.circles import Circles
from Nodes.misc.alpha_comp.compositors.Leaves.point_maps.spirals import Spirals
from Nodes.misc.mass_composition import MassComposition
from node_factory import NodeFactory


def get_misc_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [PointMappingMin, Line, PointMapComb, FromFile, MeanBuffer,
                WeightBuffer, Exciter, PointMapping, Circles, Spirals, MassComposition]}
    factory = NodeFactory(device, frame_counter, in_dict, "Misc")
    return factory


def get_system_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, ValueProperty, AnimatedProperty]}
    factory = NodeFactory(device, frame_counter, in_dict, "System")
    return factory

