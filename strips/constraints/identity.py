import torch
from strips.constraint import Constraint
from strips.animated_property import AnimatedProperty
from mat_math.kernels import rotation_2D


class Identity(Constraint):

    def constrain(self, interp):
        return interp

