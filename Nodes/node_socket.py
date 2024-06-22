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
            raise ValueError("NodeSocket marked as necessary but not connected")
        else:
            return self.default

    def to_dict(self):
        return {"ConnectedID": self.node.node_id if self.connected else None,
                "Connected": self.connected}
