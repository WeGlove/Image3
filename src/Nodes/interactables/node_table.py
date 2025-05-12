from src.Nodes.interactables.interactable import Interactable


class NodeTable(Interactable):

    def __init__(self, value=None):
        super().__init__(value)
        self.values = []

    def set(self, value):
        super().set(value)
        self.parse()

    def parse(self):
        try:
            values = self.get()
            self.values = eval(values)
        except Exception:
            self.values = []

    def get_values(self):
        return self.values
