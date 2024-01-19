from abc import abstractmethod


class Compositor:

    @abstractmethod
    def composite(self, width, height, index, limit, arg):
        pass
