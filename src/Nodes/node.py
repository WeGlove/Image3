from typing import List

import numpy as np

from src.Nodes.node_socket import NodeSocket
from src.Nodes.interactables.interactable import Interactable


class Node:

    def __init__(self, node_id, factory_id, description, subnode_sockets: List[NodeSocket],
                 interactables: List[Interactable], position=None):
        self.subnode_sockets = subnode_sockets
        self.frame_counter = None
        self.description = description
        self.interactables = interactables if interactables is not None else []
        self.device = None
        self.node_id = node_id
        self.is_initialized = False
        self.factory_id = factory_id
        self.position = np.zeros((2, 1)) if position is None else position
        self.width = None
        self.height = None

    def set_position(self, position):
        self.position = np.array(position)

    def get_subnode_count(self):
        return len(self.subnode_sockets)

    def get_description(self):
        return self.description

    def get_interactable_count(self):
        return len(self.interactables)

    def get_subnode(self, k):
        return self.subnode_sockets[k].get()

    def get_interactable(self, k):
        return self.interactables[k]

    def connect_subnode(self, subnode_id, subnode):
        self.subnode_sockets[subnode_id].connect(subnode)

    def to_dict(self):
        return {"properties": {}, "system": {"node_id": self.node_id, "factory_id": self.factory_id, "name": self.get_node_name(),
                                             "interactables": [interactable.to_dict() for interactable in self.interactables],
                                             "position": self.position.tolist()}}

    def produce(self, *args):
        return None

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        for socket in self.subnode_sockets:
            node = socket.get()
            if node in excluded_nodes:
                continue
            else:
                node.initialize(width, height, excluded_nodes + [self], frame_counter, device)

        self.frame_counter = frame_counter
        self.device = device
        self.is_initialized = True
        self.width = width
        self.height = height

    def get_all_subnodes(self):
        subnodes = [self.get_subnode(k).get_all_subnodes() for k in range(self.get_subnode_count()) if self.subnode_sockets[k].is_connected()]
        out_subnodes = []
        for subnodes_list in subnodes:
            out_subnodes.extend(subnodes_list)
        out_subnodes.append(self)
        return out_subnodes

    @staticmethod
    def get_node_name():
        return "Node"
