from src.Nodes.node import Node
from scipy.interpolate import BSpline as ScipyBSpine
import numpy as np
import torch


class BSpline(Node):

    def __init__(self):
        super().__init__()

    def produce(self):
        spline = ScipyBSpine((1, 100, 1820, 1920), (0, 1, 1, 0), 1)
        arr = spline(np.array(list(range(1920))))
        arr = torch.tensor(arr, device=self.defaults.device)
        arr = arr.repeat((1080, 1))
        print(arr.shape)

        return arr