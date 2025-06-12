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


def get_system_factory():
    in_dict = {"Out": Out, "NumberProperty": NumberProperty, "StringProperty": StringProperty,
               "TensorProperty": TensorProperty, "AnimatedProperty": AnimatedProperty, "Button": Button,
               "WaitManager": WaitManager, "Hold": Hold, "Display": Display, "Once": Once, "Random": Random,
               "ListGet": ListGet, "NoneProperty": NoneProperty}
    factory = NodeFactory(in_dict, "System")
    return factory


from src.Nodes.io.files.images_property import ImagesProperty
from src.Nodes.io.files.load_image import LoadImage
from src.Nodes.io.files.byte_reader import ByteReader
from src.Nodes.io.files.text_reader import TextReader
from src.Nodes.io.keyboard_reader import KeyboardReader
from src.Nodes.io.files.live_player import LivePlayer


def get_io_factory():
    in_dict = {"ImagesProperty": ImagesProperty, "LoadImage": LoadImage, "ByteReader": ByteReader,
               "TextReader": TextReader, "KeyboardReader": KeyboardReader, "LivePlayer": LivePlayer}
    factory = NodeFactory(in_dict, "IO",
                          hierarchy= ["ImagesProperty", "LoadImage", "ByteReader", ("Test", ["TextReader", "KeyboardReader", "LivePlayer"])])
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


def get_math_factory():
    in_dict = {"Matmul": Matmul, "Addition": Addition, "Subtraction": Subtraction, "Multiplication": Multiplication,
               "Division": Division, "Modulo": Modulo, "Power": Power, "Convolution": Convolution,
               "Transposition": Transposition, "Selection": Selection, "Shape": Shape, "Mean": Mean, "Round": Round,
               "SVD": SVD, "QR": QR, "Interpolate": Interpolate}
    factory = NodeFactory(in_dict, "Tensor Math")
    return factory


from src.Nodes.maps.line import Line
from src.Nodes.maps.noise import Noise
from src.Nodes.maps.fill import Fill
from src.Nodes.maps.spirals import Spirals
from src.Nodes.maps.circles import Circles
from src.Nodes.maps.swap import Swap
from src.Nodes.maps.iRFFT import iRFFT
from src.Nodes.maps.RFFT import RFFT


def get_map_factory():
    in_dict = {"Line": Line, "Noise": Noise, "Fill": Fill, "Spirals": Spirals, "Circles": Circles, "Swap": Swap,
               "iRFFT": iRFFT, "RFFT": RFFT}
    factory = NodeFactory(in_dict, "Point Maps")
    return factory


from src.Nodes.imaging.mass_composition import MassComposition
from src.Nodes.imaging.coloring import Coloring
from src.Nodes.imaging.mass_alpha import MassAlpha


def get_imaging_factory():
    in_dict = {"MassComposition": MassComposition, "Coloring": Coloring, "MassAlpha": MassAlpha}
    factory = NodeFactory(in_dict, "Imaging")
    return factory


from src.Nodes.conv_tensors.mean import Mean
from src.Nodes.conv_tensors.edge_detection import EdgeDetection
from src.Nodes.conv_tensors.sharpen import Sharpen


def get_tensor_conv_factory():
    in_dict = {"Mean": Mean, "EdgeDetection": EdgeDetection, "Sharpen": Sharpen}
    factory = NodeFactory(in_dict, "Convolution Tensors")
    return factory


from src.Nodes.maps_2vec.polar import Polar
from src.Nodes.maps_2vec.positions import Positions


def get_maps_2vec_factory():
    in_dict = {"Polar": Polar, "Positions": Positions}
    factory = NodeFactory(in_dict, "2Vec Maps")
    return factory


from src.Nodes.maps_nvec.HSV import HSV
from src.Nodes.maps_nvec.bitplanes import BitPlanes


def get_maps_nvec_factory():
    in_dict = {"HSV": HSV, "BitPlanes": BitPlanes}
    factory = NodeFactory(in_dict, "NVec Maps")
    return factory
