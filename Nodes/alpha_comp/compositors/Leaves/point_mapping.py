import torch
from Nodes.alpha_comp.compositor import Compositor
from Nodes.animated_property import AnimatedProperty
from Nodes.node import NodeSocket
from Nodes.value_property import ValueProperty


class PointMapping(Compositor):

    def __init__(self, device, node_id, frame_counter):
        self.noso_duty_cycle = NodeSocket(False, "Duty Cycle", AnimatedProperty(None, -1, frame_counter, device))
        self.noso_shift = NodeSocket(False, "Shift", AnimatedProperty(0., -1, frame_counter, device))
        self.noso_frequency = NodeSocket(False, "Frequency", AnimatedProperty(1., -1, frame_counter, device))
        self.noso_point_maps = NodeSocket(False, "Point Maps", ValueProperty([], -1, frame_counter, device))
        self.noso_weights = NodeSocket(False, "Weights", ValueProperty([], -1, frame_counter, device))
        super().__init__(device, node_id, frame_counter, "PointMapping",
                         [self.noso_duty_cycle, self.noso_shift, self.noso_frequency, self.noso_point_maps, self.noso_weights])

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        for point_map in self.noso_point_maps.get().produce():
            point_map.initialize(width, height, limit)
        #if self.noso_duty_cycle.get().initial_value is None:
        #    self.noso_duty_cycle.get().initial_value = torch.tensor([1/limit] * self.limit, device=self.device)
        #if self.noso_weights.get().initial_value is None:
        #    self.noso_weights.get().initial_value = torch.tensor([1/len(self.noso_point_maps.get().produce())] * len(self.noso_point_maps.get().produce()), device=self.device)

    def produce(self, index, img):
        composite_point_map = torch.zeros(self.width, self.height, device=self.device)
        out_arr = torch.zeros(self.width, self.height, device=self.device)

        weights = self.noso_weights.get().produce()
        weights = weights / torch.sum(weights)

        for point_map, weight in zip(self.noso_point_maps.get().produce(), weights):
            composite_point_map += weight * point_map.produce()

        arr_map = (composite_point_map * self.noso_frequency.get().produce() + self.noso_shift.get().produce()) % 1

        duty_cycle = self.noso_duty_cycle.get().produce()
        duty_cycle = duty_cycle / torch.sum(duty_cycle)
        duty_cycle = torch.cumsum(duty_cycle, 0)

        if index == 0:
            out_arr[(0 <= arr_map) & (arr_map < duty_cycle[index])] = 1
        else:
            out_arr[(duty_cycle[index-1] <= arr_map) & (arr_map < duty_cycle[index])] = 1

        out_arr = torch.stack([out_arr, out_arr, out_arr]).transpose(0, 1).transpose(1, 2)
        return out_arr
