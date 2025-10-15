from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from torch.nn.functional import pad


class ZeroPad(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.x = NodeSocket("X")
        self.y = NodeSocket("Y")
        super().__init__([self.a, self.x, self.y], [], "Tiling")

    def produce(self):
        x = self.x.get().produce()
        y = self.y.get().produce()

        img = self.a.get().produce()
        img = pad(img, (2, x, 3, y), "constant", 0)
        
        return img
