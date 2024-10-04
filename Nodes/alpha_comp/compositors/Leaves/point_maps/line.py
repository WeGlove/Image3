from Nodes.alpha_comp.Geos import get_centered_vector_map
import torch
from Nodes.value_property import ValueProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
from Nodes.node_socket import NodeSocket
import math


class Line(PointMap):

    def __init__(self, node_id, device, frame_counter, line=None):
        """

        :param line: as [ax + by + c]
        :param node_id:
        :param device:
        """
        self.line_noso = NodeSocket(False, "Line",
                                    ValueProperty(line, -1, device, frame_counter))
        self.shift_noso = NodeSocket(False, "Shift",
                                     ValueProperty(line, -1, device, frame_counter))
        super().__init__(device, node_id, frame_counter, [self.line_noso, self.shift_noso])

    def produce(self):
        position = self.line_noso.get().produce()

        vector_map = get_centered_vector_map(self.width, self.height, self.device)

        vector_map = vector_map * position[:2]

        vector_map = torch.sum(vector_map, dim=2)

        vector_map = vector_map + position[2]

        vector_map = vector_map / math.sqrt(position[0]**2 + position[1]**2)

        vector_map = vector_map / math.sqrt((self.width/2)**2 + (self.height/2)**2)

        vector_map = torch.abs(vector_map)

        vector_map += self.shift_noso.get().produce()

        return vector_map

    @staticmethod
    def from_2_points(x_0, x_1, device, node_id, frame_counter):
        AB = x_1 - x_0
        a = AB[0]
        b = AB[1]
        c = x_0[1]

        return Line(node_id, device=device, frame_counter=frame_counter, line=torch.tensor([a, b, c], device=device))

    @staticmethod
    def get_node_name():
        return "Line"
