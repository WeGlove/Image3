from Nodes.interactables.interactable import Interactable


class NodeEdit(Interactable):

    def __init__(self, default=None):
        super().__init__()
        self.default = default

    def set(self, value):
        self.default = value

    def get(self):
        return self.default

    def to_dict(self):
        return {"ConnectedID": self.node.node_id if self.connected else None, # TODO
                "Connected": self.connected}
