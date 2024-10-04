from Nodes.node import NodeSocket
from Nodes.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
from Nodes.value_property import ValueProperty


class PointMapComb(PointMap):

    def __init__(self, node_id, device, frame_counter):
        self.a_el = NodeSocket(False, "Element A", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.b_el = NodeSocket(False, "Element B", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.c_el = NodeSocket(False, "Element C", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.d_el = NodeSocket(False, "Element D", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.e_el = NodeSocket(False, "Element E", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.f_el = NodeSocket(False, "Element F", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.g_el = NodeSocket(False, "Element G", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.h_el = NodeSocket(False, "Element H", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.i_el = NodeSocket(False, "Element I", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.j_el = NodeSocket(False, "Element J", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        super().__init__(device, node_id, frame_counter,
                         [self.a_el, self.b_el, self.c_el, self.d_el, self.e_el, self.f_el, self.g_el,
                          self.h_el, self.i_el, self.j_el])

    def produce(self):
        maps = []

        if self.a_el.is_connected():
            maps.append(self.a_el.get())
        if self.b_el.is_connected():
            maps.append(self.b_el.get())
        if self.c_el.is_connected():
            maps.append(self.c_el.get())
        if self.d_el.is_connected():
            maps.append(self.d_el.get())
        if self.e_el.is_connected():
            maps.append(self.e_el.get())
        if self.f_el.is_connected():
            maps.append(self.f_el.get())
        if self.g_el.is_connected():
            maps.append(self.g_el.get())
        if self.h_el.is_connected():
            maps.append(self.h_el.get())
        if self.i_el.is_connected():
            maps.append(self.i_el.get())
        if self.j_el.is_connected():
            maps.append(self.j_el.get())

        return maps

    @staticmethod
    def get_node_name():
        return "Point Map Comb"
