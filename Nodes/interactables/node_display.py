from Nodes.interactables.interactable import Interactable


class NodeDisplay(Interactable):

    def __init__(self, value=None):
        super().__init__(value)

    def get(self):
        return self.default
