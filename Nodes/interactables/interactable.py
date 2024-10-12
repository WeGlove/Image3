class Interactable:

    def __init__(self, default=None):
        self.default = default

    def set(self, value):
        self.default = value

    def get(self):
        return self.default

    def to_dict(self):
        return {"value": self.default}
