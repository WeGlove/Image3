import torch
from alpha_comp.compositor import Compositor
from strips.animated_property import AnimatedProperty


class PointMapping(Compositor):

    def __init__(self, point_maps, duty_cycle=None):
        super().__init__()
        self.point_maps = point_maps
        self.duty_cycle = AnimatedProperty(duty_cycle)

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        for point_map in self.point_maps:
            point_map.initialize(width, height, limit, device=device)
        if self.duty_cycle.initial_value is None:
            self.duty_cycle.initial_value = torch.tensor([1/limit] * self.limit, device=self.device)

    def composite(self, index, img):
        composite_point_map = torch.zeros(self.width, self.height, device=self.device)
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        for point_map in self.point_maps:
            composite_point_map += point_map.composite(index, img)

        arr_map = composite_point_map / len(self.point_maps)
        arr_map = arr_map % 1
        b= arr_map.cpu().numpy()

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
        animated_properties = {visitors + "_PointMapping:DutyCycle": self.duty_cycle}
        for k, point_map in enumerate(self.point_maps):
            animated_properties.update(point_map.get_animated_properties(visitors + f"_PointMapping:PointMap-{k}"))

        constraint_properties = {}
        for k, animated_property in animated_properties.items():
            constraint_properties.update(animated_property.get_animated_properties(k))

        animated_properties.update(constraint_properties)
        return animated_properties
