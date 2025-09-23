from abc import abstractmethod
from typing import Dict


class Serializable:

    @abstractmethod
    def serialize(self, *args, **kwargs) -> Dict:
        return {}

    @staticmethod
    @abstractmethod
    def deserialize(*args, **kwargs):
        pass
