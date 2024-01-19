import numpy as np
from scipy.signal import fftconvolve


class TensorComp:

    def __init__(self, compositor, tensor):
        self.compositor = compositor
        self.tensor = tensor
        self.tensor_width = self.tensor.shape[0] // 2
        self.tensor_height = self.tensor.shape[1] // 2

    def composite(self, width, height, index, limit, arg):
        mask, out_arg = self.compositor.composite(width, height, index, limit, arg)
        r = fftconvolve(mask[:, :, 0], self.tensor)
        g = fftconvolve(mask[:, :, 1], self.tensor)
        b = fftconvolve(mask[:, :, 2], self.tensor)
        mask = np.array([r[self.tensor_width:-self.tensor_width, self.tensor_height:-self.tensor_height],
                         g[self.tensor_width:-self.tensor_width, self.tensor_height:-self.tensor_height],
                         b[self.tensor_width:-self.tensor_width, self.tensor_height:-self.tensor_height]])
        mask = np.transpose(mask, (1, 2, 0))

        return mask, arg

    @staticmethod
    def box_blur(size: int = 0):
        size_side = size*2 + 1
        return np.ones((size_side, size_side)) / (size_side**2)

    @staticmethod
    def sharpen():
        return np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])

    @staticmethod
    def emboss():
        return np.array([[-2, -1, 0],[-1, 1, 1],[0, 1, 2]])