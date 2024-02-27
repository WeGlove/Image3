from alpha_comp.compositor import Compositor
from alpha_comp.Geos import get_polar
import torch
from strips.animated_property import AnimatedProperty


class PointWeightsSpirals(Compositor):

    def __init__(self, points, scale_radius=0, rotation=0, frequency=1, weights_rad=None, weights_angles=None):
        super().__init__()
        self.points = AnimatedProperty(initial_value=points)
        self.scale_radius = AnimatedProperty(initial_value=scale_radius)
        self.rotation = AnimatedProperty(initial_value=rotation)
        self.frequency = AnimatedProperty(initial_value=frequency)
        self.weights_rad = AnimatedProperty(initial_value=weights_rad)
        self.weights_angle = AnimatedProperty(initial_value=weights_angles)

        self.angle_space = None

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        if self.weights_rad.initial_value is None:
            self.weights_rad.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)
        if self.weights_angle.initial_value is None:
            self.weights_angle.initial_value = torch.tensor([1/self.points.get().shape[0]]*self.points.get().shape[0], device=self.device)

        self.angle_space = 2 * torch.pi / self.limit

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        angle_start = self.angle_space * index
        angle_end = self.angle_space * (index + 1)

        rad_out = None
        angles_out = None
        points = self.points.get()
        weights_rad = self.weights_rad.get()
        weights_angle = self.weights_angle.get()
        for i in range(points.shape[0]):
            rad, angle = get_polar(self.width, self.height, self.device, points[i])
            rad = rad * weights_rad[i] #+ self.shift.get()
            angle = angle * weights_angle[i] #+ self.shift.get()
            if rad_out is None:
                rad_out = rad
                angles_out = angle
            else:
                rad_out += rad
                angles_out += angle

        angles = (angles_out + torch.pi) + rad_out * self.scale_radius.get()
        angles = (angles * self.frequency.get() + self.rotation.get()) % (2 * torch.pi)

        out_arr[torch.logical_and(angle_start < angles, angles < angle_end)] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        return {}
