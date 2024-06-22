from Nodes.node import NodeSocket
from Nodes.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap


class PointMapComb(PointMap):

    def __init__(self, node_id, device):
        self.a_el = NodeSocket(False, "Element A", None)
        self.b_el = NodeSocket(False, "Element B", None)
        self.c_el = NodeSocket(False, "Element B", None)
        self.d_el = NodeSocket(False, "Element B", None)
        self.e_el = NodeSocket(False, "Element B", None)
        self.f_el = NodeSocket(False, "Element B", None)
        self.g_el = NodeSocket(False, "Element B", None)
        self.h_el = NodeSocket(False, "Element B", None)
        self.i_el = NodeSocket(False, "Element B", None)
        self.j_el = NodeSocket(False, "Element B", None)
        super().__init__(device, node_id,"Point Map Comb",
                         [self.a_el, self.b_el, self.c_el, self.d_el, self.e_el, self.f_el, self.g_el,
                          self.h_el, self.i_el, self.j_el])

    def get(self):
        maps = []

        if self.a_el.is_connected():
            maps.append(self.a_el.get())
        if self.a_el.is_connected():
            maps.append(self.b_el)
        if self.a_el.is_connected():
            maps.append(self.c_el)
        if self.a_el.is_connected():
            maps.append(self.d_el)
        if self.a_el.is_connected():
            maps.append(self.e_el)
        if self.a_el.is_connected():
            maps.append(self.f_el)
        if self.a_el.is_connected():
            maps.append(self.g_el)
        if self.a_el.is_connected():
            maps.append(self.h_el)
        if self.a_el.is_connected():
            maps.append(self.i_el)
        if self.a_el.is_connected():
            maps.append(self.j_el)

        return maps