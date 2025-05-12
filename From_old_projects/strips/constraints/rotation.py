import torch
from src.Nodes import Constraint
from src.Nodes import AnimatedProperty
from src.mat_math.homo_kernels import rotation_2D


class Rotation(Constraint):

    def __init__(self, origin, device):
        super().__init__()
        self.angle = AnimatedProperty(0)
        self.origin = AnimatedProperty(origin)
        self.device = device

    def constrain(self, interp):
        rot_mat = rotation_2D(self.angle.get() / 360 * 2*torch.pi, self.device)
        interp_form_origin = interp - self.origin.get()
        rotated = torch.matmul(interp_form_origin.T, rot_mat)
        out_point = rotated + self.origin.get()
        return out_point

    def get_animated_properties(self, visitor):
        return {visitor + "_Rotation:" + "Angle": self.angle, visitor + "_Rotation:" + "Origin": self.origin}
