from node_factory import NodeFactory

from Nodes.system.out import Out
from Nodes.system.number_property import NumberProperty
from Nodes.system.string_property import StringProperty
from Nodes.system.tensor_property import TensorProperty
from Nodes.system.animated_property import AnimatedProperty
from Nodes.system.button import Button
from Nodes.system.wait_manager import WaitManager


def get_system_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, NumberProperty, StringProperty, TensorProperty, AnimatedProperty, Button, WaitManager]}
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


from Nodes.tensor_math.matmul import Matmul
from Nodes.tensor_math.addition import Addition
from Nodes.tensor_math.subtraction import Subtraction
from Nodes.tensor_math.multiplication import Multiplication
from Nodes.tensor_math.division import Division
from Nodes.tensor_math.modulo import Modulo
from Nodes.tensor_math.power import Power
from Nodes.tensor_math.convolution import Convolution


def get_math_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Matmul, Addition, Subtraction, Multiplication, Division, Modulo, Power, Convolution]}
    factory = NodeFactory(device, frame_counter, in_dict, "Tensor Math")
    return factory


from Nodes.maps.line import Line
from Nodes.maps.noise import Noise


def get_map_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Line, Noise]}
    factory = NodeFactory(device, frame_counter, in_dict, "Point Maps")
    return factory


from Nodes.imaging.mass_composition import MassComposition
from Nodes.imaging.coloring import Coloring
from Nodes.imaging.mass_alpha import MassAlpha


def get_imaging_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [MassComposition, Coloring, MassAlpha]}
    factory = NodeFactory(device, frame_counter, in_dict, "Imaging")
    return factory


from Nodes.conv_tensors.mean import Mean


def get_tensor_conv_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Mean]}
    factory = NodeFactory(device, frame_counter, in_dict, "Convolution Tensors")
    return factory

