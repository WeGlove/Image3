class InteractableWidget:

    SOCKET_OFFSET = 20
    LINE_SIZE = 20

    def __init__(self,  parent, node, k, line_offset):
        self.parent = parent
        self.node = node
        self.k = k
        self.line_offset = line_offset

    def cut(self):
        pass

    def move(self, x, y):
        pass

    def update(self):
        pass
