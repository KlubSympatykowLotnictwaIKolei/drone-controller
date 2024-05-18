
from typing import Dict
from lmao.coordinate_calculation.bounding_box_to_gps_converter import BoundingBoxToGpsConverter
from lmao.graph.lmao_graph_node import LmaoGraphNode

class DetectionPositionCalculatorNode(LmaoGraphNode):
    """
    This node uses the information in the signal to calulcate 
    the positions of detected objects on the ground.
    """
    
    def __init__(self, 
                 bounding_box_to_position_converter: BoundingBoxToGpsConverter,
                 input_detections_key: str,
                 input_telemetry_key: str,
                 output_positions_key: str):
        self.__bounding_box_to_position_converter = bounding_box_to_position_converter
        self.__input_bounding_boxes_key = input_detections_key
        self.__input_telemetry_key = input_telemetry_key
        self.__output_positions_key = output_positions_key

    def process(self, signal: Dict):
        detections = signal[self.__input_bounding_boxes_key]
        telemetry = signal[self.__input_telemetry_key]

        positions = [
            self.__bounding_box_to_position_converter.convert_to_ground_position(
                telemetry.position,
                telemetry.attitude,
                detection.bounding_box
            )
            for detection in detections
        ]

        signal[self.__output_positions_key] = positions
        