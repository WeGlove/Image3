from typing import List


class NodeSocket:

    def __init__(self, is_necesseary, socket_name, default=None):
        self.is_necessary = is_necesseary
        self.connected = False
        self.node = None
        self.default = default
        self.socket_name = socket_name

    def is_connected(self):
        return self.connected

    def get_socket_name(self):
        return self.socket_name

    def connect(self, node):
        self.node = node
        self.connected = True

    def disconnect(self):
        self.node = None
        self.connected = False

    def get(self):
        if self.is_connected():
            return self.node
        elif self.is_necessary:
            raise ValueError("Tried to get Value from a Node marked as necessary that was not connected.")
        else:
            return self.default

    def to_dict(self):
        return {"IsNecessary": self.is_necessary,
                "Node": self.node.to_dict() if self.node is not None else self.node,
                "Default": self.default.to_dict() if self.default is not None else self.default,
                "Connected": self.connected}


class Node:

    def __init__(self, node_name, subnode_sockets: List[NodeSocket], device):
        self.node_name = node_name
        self.subnode_sockets = subnode_sockets
        self.animated_properties = []
        self.device = device

    def get_subnode_count(self):
        return len(self.subnode_sockets)

    def get_subnode(self, k):
        return self.subnode_sockets[k].get()

    def connect_subnode(self, subnode_id, subnode):
        self.subnode_sockets[subnode_id].connect(subnode)

    def to_dict(self):
        return {"Name": self.node_name, "SubnodeSocekts": [subnode_socket.to_dict() for subnode_socket in self.subnode_sockets]}

    def get_all_subnodes(self):
        subnodes = [self.get_subnode(k).get_all_subnodes() for k in range(self.get_subnode_count())]
        out_subnodes = []
        for subnodes_list in subnodes:
            out_subnodes.extend(subnodes_list)
        out_subnodes.append(self)
        return out_subnodes