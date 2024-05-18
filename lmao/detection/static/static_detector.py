
from ast import List
from typing import List
from lmao.detection.detector import BoundingBox, Detection, Detector

DEFAULT_STATIC_DETECTIONS = [
    Detection(
        bounding_box=BoundingBox(
            center_x=0.5,
            center_y=0.5,
            width=0.1,
            height=0.1,
        ),
        class_id=1,
        confidence=1.0
    )
]

class StaticDetector(Detector):
    def __init__(self, static_detections: List[Detection] = DEFAULT_STATIC_DETECTIONS) -> None:
        self.__detections = static_detections
    
    def detect(self, image) -> List[Detection]:
        return self.__detections