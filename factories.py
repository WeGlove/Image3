from node_factory import NodeFactory
from Nodes.system.out import Out
from Nodes.system.number_property import NumberProperty
from Nodes.system.string_property import StringProperty
from Nodes.system.tensor_property import TensorProperty
from Nodes.system.animated_property import AnimatedProperty
from Nodes.system.button import Button
from Nodes.system.wait_manager import WaitManager
from Nodes.system.hold import Hold
from Nodes.system.display import Display


def get_system_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, NumberProperty, StringProperty, TensorProperty, AnimatedProperty, Button, WaitManager, Hold,
                Display]}
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
from Nodes.tensor_math.transposition import Transposition
from Nodes.tensor_math.selection import Selection
from Nodes.tensor_math.shape import Shape
from Nodes.tensor_math.mean import Mean


def get_math_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Matmul, Addition, Subtraction, Multiplication, Division, Modulo, Power, Convolution, Transposition,
                Selection, Shape, Mean]}
    factory = NodeFactory(device, frame_counter, in_dict, "Tensor Math")
    return factory


from Nodes.maps.line import Line
from Nodes.maps.noise import Noise
from Nodes.maps.fill import Fill
from Nodes.maps.spirals import Spirals
from Nodes.maps.circles import Circles


def get_map_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Line, Noise, Fill, Spirals, Circles]}
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
from Nodes.conv_tensors.edge_detection import EdgeDetection
from Nodes.conv_tensors.sharpen import Sharpen


def get_tensor_conv_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Mean, EdgeDetection, Sharpen]}
    factory = NodeFactory(device, frame_counter, in_dict, "Convolution Tensors")
    return factory


from Nodes.maps_2vec.polar import Polar
from Nodes.maps_2vec.positions import Positions


def get_maps_2vec_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Polar, Positions]}
    factory = NodeFactory(device, frame_counter, in_dict, "2Vec Maps")
    return factory


from Nodes.maps_nvec.HSV import HSV


def get_maps_nvec_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [HSV]}
    factory = NodeFactory(device, frame_counter, in_dict, "NVec Maps")
    return factory
