import torch
from Nodes.alpha_comp.compositor import Compositor
from Nodes.node import NodeSocket
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs
from Nodes.pointMapComb import PointMapComb


class Out(Compositor):

    def __init__(self, device, node_id, frame_counter):
        mapping = PointMappingMin(device, node_id, frame_counter)
        lines = LineConfigs.get_random(1, torch.tensor([0., 0.], device=device), 10., -1, device, frame_counter)
        comb = PointMapComb(-1, device, frame_counter)
        comb.connect_subnode(0, lines[0])
        mapping.connect_subnode(3, comb)
        self.noso_render_input = NodeSocket(False, "RenderInput", mapping)

        super().__init__(device, node_id, frame_counter, "Ouuuuuuuuuuuuuut", [self.noso_render_input])

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)

    def produce(self, index, img):
        return self.noso_render_input.get().produce(index, img)
