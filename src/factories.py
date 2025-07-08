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
from src.Nodes.system.list_get import ListGet
from src.Nodes.system.none_property import NoneProperty


def get_system_factory():
    in_dict = {"Number": NumberProperty, "String": StringProperty, "Tensor": TensorProperty,
               "Animation": AnimatedProperty,
               "Button": Button, "Display": Display,
               "WaitManager": WaitManager, "Hold": Hold, "Once": Once,
               "ListGet": ListGet,
               "Out": Out}
    factory = NodeFactory(in_dict, "System",
                          hierarchy=[("Inputs", ["Number", "String", "Tensor"]),
                                     "Animation",
                                     ("Widgets", ["Button", "Display"]),
                                     ("Delays", ["WaitManager", "Hold", "Once"]),
                                     "ListGet"
                                     ])
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
    factory = NodeFactory(in_dict, "IO")
    return factory


from src.Nodes.math.linalg.matmul import Matmul
from src.Nodes.math.airthmetic.addition import Addition
from src.Nodes.math.airthmetic.subtraction import Subtraction
from src.Nodes.math.airthmetic.multiplication import Multiplication
from src.Nodes.math.airthmetic.division import Division
from src.Nodes.math.airthmetic.modulo import Modulo
from src.Nodes.math.airthmetic.power import Power
from src.Nodes.math.linalg.convolution import Convolution
from src.Nodes.math.linalg.transposition import Transposition
from src.Nodes.math.positions.selection import Selection
from src.Nodes.math.linalg.shape import Shape
from src.Nodes.math.airthmetic.mean import Mean
from src.Nodes.math.airthmetic.round import Round
from src.Nodes.math.linalg.svd import SVD
from src.Nodes.math.linalg.qr import QR
from src.Nodes.math.airthmetic.interpolate import Interpolate
from src.Nodes.math.constants.pi_property import PiProperty
from src.Nodes.math.constants.e_property import EProperty
from src.Nodes.math.random import Normal
from src.Nodes.math.random.normal import Gauss
from src.Nodes.math.constants.constant import Constant


def get_math_factory():
    in_dict = {"None": NoneProperty, "Pi": PiProperty, "E": EProperty,
               "Addition": Addition, "Subtraction": Subtraction, "Multiplication": Multiplication, "Division": Division, "Modulo": Modulo, "Power": Power,
               "Convolution": Convolution, "Matmul": Matmul, "SVD": SVD, "QR": QR, "Shape": Shape, "Transposition": Transposition,
               "Uniform": Normal, "Normal": Gauss,
               "Selection": Selection, "Mean": Mean, "Round": Round, # TODO order these
               "Interpolate": Interpolate, "Constant": Constant}
    factory = NodeFactory(in_dict, "Math", hierarchy=[
        ("Constants", ["None", "E", "Pi"]),
        ("Arithmetic", ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Power"]),
        ("LinAlg", ["Convolution", "Matmul", "SVD", "QR", "Shape", "Transposition"]),
        ("Random", ["Normal", "Gauss"]),
        "FunctionValueMap", "Constant"
    ])
    return factory


from src.Nodes.math.distance.dist_polynom_linear import Line
from src.Nodes.maps.noise import Noise
from src.Nodes.math.constants.fill import Fill
from src.Nodes.math.spirals import Spirals
from src.Nodes.math.distance.dist_point import Circles
from src.Nodes.math.positions.swap import Swap
from src.Nodes.math.spectral.iRFFT import iRFFT
from src.Nodes.math.spectral.RFFT import RFFT
from src.Nodes.math.bspline import BSpline


def get_map_factory():
    in_dict = {"Line": Line, "Noise": Noise, "Fill": Fill, "Spirals": Spirals, "Circles": Circles, "Swap": Swap,
               "iRFFT": iRFFT, "RFFT": RFFT, "BSpline": BSpline}
    factory = NodeFactory(in_dict, "Point Maps")
    return factory


from src.Nodes.image_processing.mass_composition import MassComposition
from src.Nodes.image_processing.color.tensors_to_rgb import Coloring
from src.Nodes.image_processing.mass_alpha import MassAlpha


def get_imaging_factory():
    in_dict = {"MassComposition": MassComposition, "Coloring": Coloring, "MassAlpha": MassAlpha}
    factory = NodeFactory(in_dict, "Imaging")
    return factory


from src.conv_tensors.mean import Mean
from src.conv_tensors.edge_detection import EdgeDetection
from src.conv_tensors.sharpen import Sharpen


def get_tensor_conv_factory(): # TODO integrate in Math?
    in_dict = {"Mean": Mean, "EdgeDetection": EdgeDetection, "Sharpen": Sharpen}
    factory = NodeFactory(in_dict, "Convolution Tensors")
    return factory


from src.Nodes.math.polar import Polar
from src.Nodes.math.positions import Positions


def get_maps_2vec_factory():
    in_dict = {"Polar": Polar, "Positions": Positions}
    factory = NodeFactory(in_dict, "2Vec Maps")
    return factory


from src.Nodes.image_processing.color.rgb_to_hsv import HSV
from src.Nodes.image_processing.color.tensor_to_bitplanes import BitPlanes


def get_maps_nvec_factory():
    in_dict = {"HSV": HSV, "BitPlanes": BitPlanes}
    factory = NodeFactory(in_dict, "NVec Maps")
    return factory
