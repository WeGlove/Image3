class Interactable:

    def __init__(self, default=None):
        self.default = default
        self.set_callback = lambda x : ...

    def set(self, value):
        self.default = value
        self.set_callback(value)

    def set_set_callback(self, callback):
        print("Setting callback")
        self.set_callback = callback

    def get(self):
        return self.default

    def to_dict(self):
        return {"value": self.default}
