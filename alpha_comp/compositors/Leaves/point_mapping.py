import torch
from alpha_comp.compositor import Compositor
from strips.animated_property import AnimatedProperty


class PointMapping(Compositor):

    def __init__(self, point_maps, duty_cycle=None, weights=None):
        super().__init__()
        self.point_maps = point_maps
        self.duty_cycle = AnimatedProperty(duty_cycle)
        self.weights = AnimatedProperty(weights)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        for point_map in self.point_maps:
            point_map.initialize(width, height, limit, device=device)
        if self.duty_cycle.initial_value is None:
            self.duty_cycle.initial_value = torch.tensor([1/limit] * self.limit, device=self.device)
        if self.weights.initial_value is None:
            self.weights.initial_value = torch.tensor([1/len(self.point_maps)] * len(self.point_maps), device=self.device)

    def composite(self, index, img):
        composite_point_map = torch.zeros(self.width, self.height, device=self.device)
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        weights = self.weights.get()
        weights = weights / torch.sum(weights)

        for point_map, weight in zip(self.point_maps, weights):
            composite_point_map += weight * point_map.composite(index, img)

        arr_map = composite_point_map % 1

        duty_cycle = self.duty_cycle.get()
        duty_cycle = duty_cycle / torch.sum(duty_cycle)
        duty_cycle = torch.cumsum(duty_cycle, 0)

        if index == 0:
            out_arr[(0 <= arr_map) & (arr_map < duty_cycle[index])] = 1
        else:
            out_arr[(duty_cycle[index-1] <= arr_map) & (arr_map < duty_cycle[index])] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self, visitors):
        animated_properties = {visitors + "_PointMapping:DutyCycle": self.duty_cycle,
                               visitors + "_PointMapping:Weights": self.weights}
        for k, point_map in enumerate(self.point_maps):
            animated_properties.update(point_map.get_animated_properties(visitors + f"_PointMapping:PointMap-{k}"))

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
