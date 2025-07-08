from src.node_factory import NodeFactory
from src.Nodes.system import (Out, NumberProperty, StringProperty, TensorProperty, AnimatedProperty, Button, WaitManager,
                              Hold, Display, Once, ListGet, NoneProperty)
from src.Nodes.io import ImagesProperty, LoadImage, ByteReader, TextReader, KeyboardReader, LivePlayer
from src.Nodes.math import (Abs, Addition, Division, Interpolate, Log, Mean, Modulo, Multiplication, Power, Root, Round,
                            Subtraction, PiProperty, EProperty, Fill, DistPoint, DistGeometryLine, Matmul, Convolution,
                            Transposition, Shape, SVD, QR, ColumnExtension, RowExtension, Cube, Linear,
                            Square, Positions, Selection, Swap, Normal, Uniform, RFFT, iRFFT, Cos, Cosecant, Cotangent,
                            Secant, Sin, Tan, BSpline, Polar, Spirals)
from src.Nodes.image_processing import MassAlpha, MassComposition, RGBToHSV, HSVToRGB, BitPlanes, GreyScale, HueShift


def get_system_factory():
    in_dict = {"Out": Out, "Number": NumberProperty, "String": StringProperty, "Tensor": TensorProperty,
               "Animation": AnimatedProperty,
               "Button": Button, "Display": Display,
               "WaitManager": WaitManager, "Hold": Hold, "Once": Once,
               "ListGet": ListGet, "None": NoneProperty
               }
    factory = NodeFactory(in_dict, "System",
                          hierarchy=["Number", "String", "Tensor",
                                     "Animation",
                                     "Button", "Display",
                                     "WaitManager", "Hold", "Once",
                                     "ListGet", "None"
                                     ])
    return factory


def get_io_factory():
    in_dict = {"ImagesProperty": ImagesProperty, "LoadImage": LoadImage, "ByteReader": ByteReader,
               "TextReader": TextReader, "KeyboardReader": KeyboardReader, "LivePlayer": LivePlayer}
    factory = NodeFactory(in_dict, "IO")
    return factory


def get_math_factory():
    in_dict = {"Abs": Abs, "Addition": Addition, "Division": Division, "Interpolate": Interpolate, "Log": Log,
               "Mean": Mean, "Modulo": Modulo, "Multiplication": Multiplication, "Power": Power, "Root": Root,
               "Round": Round, "Subtraction": Subtraction, "Pi": PiProperty, "E": EProperty, "Fill": Fill,
               "DistPoint": DistPoint, "DistGeometryLine": DistGeometryLine, "Matmul": Matmul,
               "Convolution": Convolution, "Transposition": Transposition, "Shape": Shape, "SVD": SVD, "QR": QR,
               "ColumnExtension": ColumnExtension, "RowExtension": RowExtension, "Cube": Cube, "Linear": Linear,
               "Square": Square, "Positions": Positions, "Selection": Selection, "Swap": Swap, "Normal": Normal,
               "Uniform": Uniform, "RFFT": RFFT, "iRFFT": iRFFT, "Cos": Cos, "Cosecant": Cosecant,
               "Cotangent": Cotangent, "Secant": Secant, "Sin": Sin, "Tan": Tan, "BSpline": BSpline, "Polar": Polar,
               "Spirals": Spirals}
    factory = NodeFactory(in_dict, "Math", hierarchy=[
        ("Arithmetic >", ["Abs", "Addition", "Division", "Interpolate", "Log", "Mean", "Modulo", "Multiplication",
                          "Power", "Root", "Round", "Subtraction"]),
        ("Constants >", ["Fill", "E", "Pi"]),
        ("Distance >", ["DistPoint", "DistGeometryLine"]),
        ("LinAlg >", ["Matmul", "Convolution", "Transposition", "Shape", "SVD", "QR", "ColumnExtension", "RowExtension"]),
        ("Polynomial >", ["Cube", "Linear", "Square"]),
        ("Positions >", ["Positions", "Selection", "Swap"]),
        ("Random >", ["Normal", "Uniform"]),
        ("Spectral >", ["iRFFT", "RFFT"]),
        ("Trigonometry >", ["Cos", "Cosecant", "Cotangent", "Secant", "Sin", "Tan"]),
        "BSpline", "Polar", "Spirals"
    ])
    return factory

def get_imaging_factory():
    in_dict = {"MassAlpha": MassAlpha, "MassComposition": MassComposition, "RGBToHSV": RGBToHSV, "HSVToRGB": HSVToRGB,
               "BitPlanes": BitPlanes, "GreyScale": GreyScale, "HueShift": HueShift}
    factory = NodeFactory(in_dict, "Imaging")
    return factory


from src.conv_tensors.mean import Mean
from src.conv_tensors.edge_detection import EdgeDetection
from src.conv_tensors.sharpen import Sharpen


def get_tensor_conv_factory(): # TODO integrate in Math?
    in_dict = {"Mean": Mean, "EdgeDetection": EdgeDetection, "Sharpen": Sharpen}
    factory = NodeFactory(in_dict, "Convolution Tensors")
    return factory