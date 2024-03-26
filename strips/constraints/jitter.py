import math

import torch
from strips.constraint import Constraint
from strips.animated_property import AnimatedProperty
from mat_math.homo_kernels import rotation_2D


class Jitter(Constraint):

    def __init__(self, device, amplitude=1, frequency=1):
        super().__init__()
        self.amplitude = AnimatedProperty(amplitude)
        self.device = device
        self.frequency = AnimatedProperty(frequency)

    def constrain(self, interp):
        interp = interp + math.sin(self.frame * self.frequency.get()) * self.amplitude.get()
        return interp

    def set_frame(self, frame):
        super().set_frame(frame)

    def get_animated_properties(self, visitor):
        return {visitor + "_Jitter:" + "Amplitude": self.amplitude, visitor + "_jitter:" + "Frequency": self.frequency}
