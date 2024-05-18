
from abc import ABC, abstractmethod

class CameraFov(ABC):
    @abstractmethod
    def get_horizontal_fov(self) -> float:
        pass

    @abstractmethod
    def get_vertical_fov(self) -> float:
        pass