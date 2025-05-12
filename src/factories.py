from src.node_factory import NodeFactory
from src.Nodes.system.out import Out
from src.Nodes.system.number_property import NumberProperty
from src.Nodes.system.string_property import StringProperty
from src.Nodes.system.tensor_property import TensorProperty
from src.Nodes.system.animated_property import AnimatedProperty
from src.Nodes.system.button import Button
from src.Nodes.system.wait_manager import WaitManager
from src.Nodes.system.hold import Hold
from src.Nodes.system.display import Display
from src.Nodes.system.once import Once
from src.Nodes.system.random import Random
from src.Nodes.system.list_get import ListGet
from src.Nodes.system.none_property import NoneProperty


def get_system_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Out, NumberProperty, StringProperty, TensorProperty, AnimatedProperty, Button, WaitManager, Hold,
                Display, Once, Random, ListGet, NoneProperty]}
    factory = NodeFactory(device, frame_counter, in_dict, "System")
    return factory


from src.Nodes.io.files.images_property import ImagesProperty
from src.Nodes.io.files.load_image import LoadImage
from src.Nodes.io.files.byte_reader import ByteReader
from src.Nodes.io.files.text_reader import TextReader
from src.Nodes.io.keyboard_reader import KeyboardReader
from src.Nodes.io.files.live_player import LivePlayer


def get_io_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [ImagesProperty, LoadImage, ByteReader, TextReader, KeyboardReader, LivePlayer]}
    factory = NodeFactory(device, frame_counter, in_dict, "IO")
    return factory


from src.Nodes.tensor_math.matmul import Matmul
from src.Nodes.tensor_math.addition import Addition
from src.Nodes.tensor_math.subtraction import Subtraction
from src.Nodes.tensor_math.multiplication import Multiplication
from src.Nodes.tensor_math.division import Division
from src.Nodes.tensor_math.modulo import Modulo
from src.Nodes.tensor_math.power import Power
from src.Nodes.tensor_math.convolution import Convolution
from src.Nodes.tensor_math.transposition import Transposition
from src.Nodes.tensor_math.selection import Selection
from src.Nodes.tensor_math.shape import Shape
from src.Nodes.tensor_math.mean import Mean
from src.Nodes.tensor_math.round import Round
from src.Nodes.tensor_math.svd import SVD
from src.Nodes.tensor_math.qr import QR
from src.Nodes.tensor_math.interpolate import Interpolate


def get_math_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Matmul, Addition, Subtraction, Multiplication, Division, Modulo, Power, Convolution, Transposition,
                Selection, Shape, Mean, Round, SVD, QR, Interpolate]}
    factory = NodeFactory(device, frame_counter, in_dict, "Tensor Math")
    return factory


from src.Nodes.maps.line import Line
from src.Nodes.maps.noise import Noise
from src.Nodes.maps.fill import Fill
from src.Nodes.maps.spirals import Spirals
from src.Nodes.maps.circles import Circles
from src.Nodes.maps.swap import Swap
from src.Nodes.maps.iRFFT import iRFFT
from src.Nodes.maps.RFFT import RFFT


def get_map_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Line, Noise, Fill, Spirals, Circles, Swap, iRFFT, RFFT]}
    factory = NodeFactory(device, frame_counter, in_dict, "Point Maps")
    return factory


from src.Nodes.imaging.mass_composition import MassComposition
from src.Nodes.imaging.coloring import Coloring
from src.Nodes.imaging.mass_alpha import MassAlpha


def get_imaging_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [MassComposition, Coloring, MassAlpha]}
    factory = NodeFactory(device, frame_counter, in_dict, "Imaging")
    return factory


from src.Nodes.conv_tensors.mean import Mean
from src.Nodes.conv_tensors.edge_detection import EdgeDetection
from src.Nodes.conv_tensors.sharpen import Sharpen


def get_tensor_conv_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Mean, EdgeDetection, Sharpen]}
    factory = NodeFactory(device, frame_counter, in_dict, "Convolution Tensors")
    return factory


from src.Nodes.maps_2vec.polar import Polar
from src.Nodes.maps_2vec.positions import Positions


def get_maps_2vec_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [Polar, Positions]}
    factory = NodeFactory(device, frame_counter, in_dict, "2Vec Maps")
    return factory


from src.Nodes.maps_nvec.HSV import HSV
from src.Nodes.maps_nvec.bitplanes import BitPlanes


def get_maps_nvec_factory(device, frame_counter):
    in_dict = {node.get_node_name(): node for node in
               [HSV, BitPlanes]}
    factory = NodeFactory(device, frame_counter, in_dict, "NVec Maps")
    return factory
