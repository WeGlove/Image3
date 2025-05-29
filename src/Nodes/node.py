from typing import List
import numpy as np
from src.Nodes.node_socket import NodeSocket
from src.Nodes.interactables.interactable import Interactable
from abc import abstractmethod


class Node:

    def __init__(self, subnode_sockets: List[NodeSocket] = None, interactables: List[Interactable] = None,
                 description=""):
        # Subnodes and interactables
        self.subnode_sockets = [] if subnode_sockets is None else subnode_sockets
        self.interactables = [] if interactables is None else interactables

        # Identifiers and descriptors

        self.description = description
        self.node_id = None
        self.is_initialized = False
        self.factory_id = None
        self.position = np.array([0, 0])
        self.node_name = None

        # Initialization variables

        self.frame_counter = None
        self.defaults = None

    def set_factory_id(self, factory_id):
        self.factory_id = factory_id

    def set_node_id(self, node_id):
        self.node_id = node_id

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

    def set_node_name(self, name):
        self.node_name = name

    def get_node_name(self):
        return self.node_name

    def to_dict(self):
        return {"node_id": self.node_id, "factory_id": self.factory_id, "name": self.get_node_name(),
                "interactables": [interactable.to_dict() for interactable in self.interactables],
                "position": self.position.tolist()}

    def initialize(self, defaults, excluded_nodes, frame_counter):
        for socket in self.subnode_sockets:
            node = socket.get()
            if node in excluded_nodes:
                continue
            else:
                node.initialize(defaults, excluded_nodes + [self], frame_counter)

        self.defaults = defaults
        self.frame_counter = frame_counter
        self.is_initialized = True

    def get_all_subnodes(self):
        subnodes = [self.get_subnode(k).get_all_subnodes() for k in range(self.get_subnode_count()) if self.subnode_sockets[k].is_connected()]
        out_subnodes = []
        for subnodes_list in subnodes:
            out_subnodes.extend(subnodes_list)
        out_subnodes.append(self)
        return out_subnodes

    @abstractmethod
    def produce(self):
        return None
