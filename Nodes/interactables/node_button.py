from Nodes.interactables.interactable import Interactable


class NodeButton(Interactable):

    def __init__(self, default=None):
        super().__init__()
        self.value = default

    def toggle(self):
        self.value = not self.value

    def get(self):
        return self.value

    def to_dict(self):
        return {"ConnectedID": self.node.node_id if self.connected else None, # TODO
                "Connected": self.connected}
