from abc import abstractmethod
import numpy as np


class Compositor:

    @abstractmethod
    def composite(self, width, height, index, limit, arg) -> np.ndarray:
        pass
