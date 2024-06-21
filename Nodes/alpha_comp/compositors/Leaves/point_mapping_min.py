import torch
from Nodes.alpha_comp.compositor import Compositor
from Nodes.animated_property import AnimatedProperty
from Nodes.Node import NodeSocket


class PointMappingMin(Compositor):

    def __init__(self, point_maps, device, node_id, shift=0., frequency=1., duty_cycle=None):
        self.duty_cycls_is_none = duty_cycle is None
        self.noso_duty_cycle = NodeSocket(False, "Duty Cycle", AnimatedProperty(-1, duty_cycle, device))
        self.noso_shift = NodeSocket(False, "Shift", AnimatedProperty(-1, shift, device))
        self.noso_frequency = NodeSocket(False, "Frequency", AnimatedProperty(-1, frequency, device))
        super().__init__(device, node_id,"PointMappingMin", [self.noso_duty_cycle, self.noso_shift, self.noso_frequency])
        self.point_maps = point_maps

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        for point_map in self.point_maps:
            point_map.initialize(width, height, limit, device=device)
        if self.duty_cycls_is_none:
            self.noso_duty_cycle.default = AnimatedProperty(torch.tensor([1/limit] * self.limit, device=self.device), device=device, node_id=-1)

    def composite(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        maps = []
        for point_map in self.point_maps:
            maps.append(point_map.composite(index, img))

        maps = torch.stack(maps)
        maps, _ = torch.min(maps, dim=0)

        arr_map = (maps * self.noso_frequency.get().get() + self.noso_shift.get().get()) % 1

        duty_cycle = self.noso_duty_cycle.get().get()
        duty_cycle = duty_cycle / torch.sum(duty_cycle)
        duty_cycle = torch.cumsum(duty_cycle, 0)

        if index == 0:
            out_arr[(0 <= arr_map) & (arr_map < duty_cycle[index])] = 1
        else:
            out_arr[(duty_cycle[index-1] <= arr_map) & (arr_map < duty_cycle[index])] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr

    def get_animated_properties(self):
        animated_properties = [self.noso_duty_cycle.get(), self.noso_shift.get(), self.noso_frequency.get()]
        for animated_property in animated_properties:
            if animated_property.is_constrained():
                animated_properties = animated_properties + animated_property.constraint.get_animated_properties()
        return animated_properties
