import math

from Nodes.constraint import Constraint
from Nodes.system.animated_property import AnimatedProperty


class Jitter(Constraint):

    def __init__(self, device, amplitude=1, frequency=1):
        super().__init__()
        self.amplitude = AnimatedProperty(amplitude)
        self.device = device
        self.frequency = AnimatedProperty(frequency)

    def constrain(self, interp):
        interp = interp + math.sin(self.frame * self.frequency.get()) * self.amplitude.get()
        return interp

    def get_animated_properties(self, visitor):
        return {visitor + "_Jitter:" + "Amplitude": self.amplitude, visitor + "_jitter:" + "Frequency": self.frequency}
