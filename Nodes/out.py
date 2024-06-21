import torch

from Nodes.alpha_comp.compositor import Compositor
from Nodes.Node import NodeSocket
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs


class Out(Compositor):

    def __init__(self, device, node_id):
        self.noso_render_input = NodeSocket(False, "RenderInput",
                                            PointMappingMin(LineConfigs.get_random(1, torch.tensor([0., 0.], device=device), 10., -1, device), device, node_id))
        super().__init__(device, node_id,"Ouuuuuuuuuuuuuut", [self.noso_render_input])

    def initialize(self, width, height, limit, device=None):
        super().initialize(width, height, limit, device)
        self.noso_render_input.get().initialize(width, height, limit, device)

    def composite(self, index, img):
        return self.noso_render_input.get().composite(index, img)

    def get_animated_properties(self):
        return self.noso_render_input.get().get_animated_properties()
