
from abc import ABC, abstractmethod

class CameraImageSource(ABC):
    """
    Interface serving as a layer of abstraction between LMAO and a physical camera.
    The only thing an implementation has to is be able to capture a single image.
    """

    @abstractmethod
    def capture_image(self):
        pass

    def disconnect(self):
        pass