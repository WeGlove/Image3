from typing import List
from Nodes.node_socket import NodeSocket
from Nodes.node_edit import NodeEdit


class Node:

    def __init__(self, node_id, node_name, frame_counter, subnode_sockets: List[NodeSocket], device, node_edits: List[NodeEdit]):
        self.node_name = node_name
        self.subnode_sockets = subnode_sockets
        self.frame_counter = frame_counter
        self.nodes_edits = node_edits if node_edits is not None else []
        self.animated_properties = []
        self.device = device
        self.node_id = node_id

    def get_subnode_count(self):
        return len(self.subnode_sockets)

    def get_edit_count(self):
        return len(self.nodes_edits)

    def get_subnode(self, k):
        return self.subnode_sockets[k].get()

    def get_node_edit(self, k):
        return self.nodes_edits[k].get()

    def set_node_edit(self, k, value):
        return self.nodes_edits[k].set(value)

    def connect_subnode(self, subnode_id, subnode):
        self.subnode_sockets[subnode_id].connect(subnode)

    def to_dict(self):
        return {"properties": {"node_id": self.node_id}, "name": self.node_name}

    def produce(self, *args):
        return None

    def initialize(self, width, height, limit):
        for socket in self.subnode_sockets:
            socket.get().initialize(width, height, limit)

    def get_all_subnodes(self):
        subnodes = [self.get_subnode(k).get_all_subnodes() for k in range(self.get_subnode_count()) if self.subnode_sockets[k].is_connected()]
        out_subnodes = []
        for subnodes_list in subnodes:
            out_subnodes.extend(subnodes_list)
        out_subnodes.append(self)
        return out_subnodes
