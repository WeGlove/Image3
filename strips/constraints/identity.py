import torch
from strips.constraint import Constraint
from strips.animated_property import AnimatedProperty
from mat_math.homo_kernels import rotation_2D


class Identity(Constraint):

    def get_animated_properties(self, visitors):
        return []

    def constrain(self, interp):
        return interp

