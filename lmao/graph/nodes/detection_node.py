
from typing import Dict
from lmao.detection.detector import Detector
from lmao.detection.utils import opencv_show_detections
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.health.health_manager import GLOBAL_HEALTH_MANAGER, HEALTH_EVENT_DETECTION


class DetectionNode(LmaoGraphNode):
    """
    This node detects objects on an image in a signal.
    """
    
    def __init__(self, 
                 detector: Detector, 
                 input_image_key: str = 'image', 
                 output_detections_key: str = 'detections'):
        self.__detector = detector
        self.__input_image_key = input_image_key
        self.__output_detections_key = output_detections_key

    def process(self, signal: Dict):
        detections = self.__detector.detect(signal[self.__input_image_key])

        for _ in detections:
            GLOBAL_HEALTH_MANAGER.register_event_occurance(HEALTH_EVENT_DETECTION)

        signal[self.__output_detections_key] = detections

        # opencv_show_detections(signal[self.__input_image_key], detections)