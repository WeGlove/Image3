import torch
from Nodes.node import Node
from Nodes.node import NodeSocket
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs
from Nodes.pointMapComb import PointMapComb


class Out(Node):

    def __init__(self, device, node_id, frame_counter):
        lines = LineConfigs.get_random(1, torch.tensor([0., 0.], device=device), 10., -1, device, frame_counter)
        comb = PointMapComb(-1, device, frame_counter)
        comb.connect_subnode(0, lines[0])
        self.noso_render_input = NodeSocket(False, "RenderInput", None)

        super().__init__(node_id, "The Output of the Patch",
                         frame_counter, [self.noso_render_input], device, [])

    def produce(self):
        return self.noso_render_input.get().produce()

    def initialize(self, width, height, *args):
        for socket in self.subnode_sockets:
            socket.get().initialize(width, height)

    @staticmethod
    def get_node_name():
        return "Output"
