
from typing import List, Set, Union
from lmao.detection.detector import Detection, Detector

class DetectorConfidenceFilter(Detector):
    def __init__(self, filtered_detector: Detector, min_confidence: float) -> None:
        self.__filtered_detector = filtered_detector
        self.__min_confidence = min_confidence
    
    def detect(self, image) -> List[Detection]:
        detection_list = self.__filtered_detector.detect(image)
        return list(filter(
            lambda detection: detection.confidence >= self.__min_confidence,
            detection_list,
        ))

class DetectorClassFilter(Detector):
    def __init__(self, filtered_detector: Detector, allowed_class_ids: Union[List, Set]) -> None:
        self.__filtered_detector = filtered_detector
        self.__allowed_class_ids = allowed_class_ids
    
    def detect(self, image) -> List[Detection]:
        detection_list = self.__filtered_detector.detect(image)
        return list(filter(
            lambda detection: detection.class_id in self.__allowed_class_ids,
            detection_list,
        ))