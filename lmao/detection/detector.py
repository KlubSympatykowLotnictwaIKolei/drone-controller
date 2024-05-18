
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class BoundingBox:
    center_x: float
    center_y: float
    width: float
    height: float
    
    def convert_local_to_image_point(self, x: float, y: float) -> Tuple[float, float]:
        x = self.center_x + (x - 0.5) * self.width
        y = self.center_y + (y - 0.5) * self.height
        return (x, y)

@dataclass
class Detection:
    bounding_box: BoundingBox
    class_id: int
    confidence: float

class Detector(ABC):
    """
    Interface for an object that takes an image and returns a list of objects detected on it.
    """

    @abstractmethod
    def detect(self, image) -> List[Detection]:
        pass
