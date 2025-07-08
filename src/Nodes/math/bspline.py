from src.Nodes.node import Node
from scipy.interpolate import BSpline as ScipyBSpine
import numpy as np
import torch
from src.Nodes.node_socket import NodeSocket


class BSpline(Node):

    def __init__(self):
        self.joint_a = NodeSocket("Joint A")
        self.joint_b = NodeSocket("Joint B")
        self.joint_c = NodeSocket("Joint C")
        self.joint_d = NodeSocket("Joint D")
        super().__init__(subnode_sockets=[self.joint_a, self.joint_b, self.joint_c, self.joint_d])

    def produce(self):
        spline = ScipyBSpine((1, 100, self.defaults.height, self.defaults.width),
                             (self.joint_a.get().produce(), self.joint_b.get().produce(),
                              self.joint_c.get().produce(), self.joint_d.get().produce()),
                             1)
        arr = spline(np.array(list(range(self.defaults.width))))
        arr = torch.tensor(arr, device=self.defaults.device)

        return arr
