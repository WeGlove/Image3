import torch
from Nodes.alpha_comp.compositor import Compositor
from Nodes.animated_property import AnimatedProperty
from Nodes.node import NodeSocket
from Nodes.value_property import ValueProperty


class PointMappingMin(Compositor):

    def __init__(self, device, node_id, frame_counter):
        self.noso_duty_cycle = NodeSocket(False, "Duty Cycle", AnimatedProperty(None, -1, frame_counter, device))
        self.noso_shift = NodeSocket(False, "Shift", AnimatedProperty(0., -1, frame_counter, device))
        self.noso_frequency = NodeSocket(False, "Frequency", AnimatedProperty(1., -1, frame_counter, device))
        self.noso_point_maps = NodeSocket(False, "Point Maps", ValueProperty([], -1, frame_counter, device))
        super().__init__(device, node_id, frame_counter, "PointMappingMin",
                         [self.noso_duty_cycle, self.noso_shift, self.noso_frequency, self.noso_point_maps])

    def initialize(self, width, height, limit):
        self.noso_duty_cycle.default = AnimatedProperty(torch.tensor([1/limit] * limit, device=self.device),
                                                        node_id=-1, device=self.device,
                                                        frame_counter=self.frame_counter)
        super().initialize(width, height, limit)

    def produce(self, index, img):
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        maps = []
        for point_map in self.noso_point_maps.get().produce():
            maps.append(point_map.produce())

        maps = torch.stack(maps)
        maps, _ = torch.min(maps, dim=0)

        arr_map = (maps * self.noso_frequency.get().produce() + self.noso_shift.get().produce()) % 1

        duty_cycle = self.noso_duty_cycle.get().produce() / torch.sum(self.noso_duty_cycle.get().produce())
        duty_cycle = torch.cumsum(duty_cycle, 0)

        if index == 0:
            out_arr[(0 <= arr_map) & (arr_map < duty_cycle[index])] = 1
        else:
            out_arr[(duty_cycle[index-1] <= arr_map) & (arr_map < duty_cycle[index])] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr
