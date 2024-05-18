
from lmao.types import PositionGPS, CameraGPS
from lmao.detection.detector import BoundingBox

from abc import ABC, abstractmethod
from typing import Optional

class BoundingBoxToGpsConverter(ABC):
    """
    Interface for calculating object ground position based on its boudning box on screen.
    """

    @abstractmethod
    def convert_to_ground_position(self, camera: CameraGPS, bbox: BoundingBox) -> Optional[PositionGPS]:
        pass

    
        
