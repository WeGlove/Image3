from src.interactables.interactable import Interactable


class NodeButton(Interactable):

    def __init__(self, default=None):
        super().__init__(default)

    def toggle(self):
        self.default = not self.default