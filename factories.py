from Nodes.system.out import Out
from Nodes.maps.alpha_comp import PointMappingMin
from Nodes.system.value_property import ValueProperty
from Nodes.system.animated_property import AnimatedProperty
from Nodes.maps.alpha_comp import Line
from Nodes.maps.pointMapComb import PointMapComb
from From_old_projects.strips.constraints.fromfile import FromFile
from From_old_projects.strips.constraints.buffer import MeanBuffer, WeightBuffer
from From_old_projects.strips.constraints.exciter import Exciter
from Nodes.maps.alpha_comp import PointMapping
from Nodes.maps.alpha_comp import Circles
from Nodes.maps.alpha_comp import Spirals
from Nodes.system.images_property import ImagesProperty
from Nodes.system.button import Button
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
               [Out, ValueProperty, AnimatedProperty, Button, ImagesProperty]}
    factory = NodeFactory(device, frame_counter, in_dict, "System")
    return factory

