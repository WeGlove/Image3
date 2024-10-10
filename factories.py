from Nodes.system.out import Out
from Nodes.system.value_property import ValueProperty
from Nodes.system.animated_property import AnimatedProperty
from Nodes.maps.pointMapComb import PointMapComb
from From_old_projects.strips.constraints.fromfile import FromFile
from From_old_projects.strips.constraints.buffer import MeanBuffer, WeightBuffer
from From_old_projects.strips.constraints.exciter import Exciter
from Nodes.system.button import Button
from Nodes.misc.mass_composition import MassComposition
from node_factory import NodeFactory


def get_misc_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [ PointMapComb, FromFile, MeanBuffer,
                WeightBuffer, Exciter, MassComposition]}
    factory = NodeFactory(device, frame_counter, in_dict, "Misc")
    return factory


def get_system_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, ValueProperty, AnimatedProperty, Button]}
    factory = NodeFactory(device, frame_counter, in_dict, "System")
    return factory


from Nodes.io.files.images_property import ImagesProperty
from Nodes.io.files.load_image import LoadImage
from Nodes.io.files.byte_reader import ByteReader
from Nodes.io.files.text_reader import TextReader
from Nodes.io.keyboard_reader import KeyboardReader


def get_io_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [ImagesProperty, LoadImage, ByteReader, TextReader, KeyboardReader]}
    factory = NodeFactory(device, frame_counter, in_dict, "IO")
    return factory
