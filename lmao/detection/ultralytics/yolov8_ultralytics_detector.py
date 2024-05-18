
from lmao.detection.detector import BoundingBox, Detection, Detector
from typing import List
import logging as log

class YoloV8UltralyticsDetector(Detector):

    def __init__(self, model_path: str):
        from ultralytics import YOLO

        log.info('Initializing ultralytics YOLO model...')
        self.__yolov8_model = YOLO(model_path)
        log.info('YOLO model initialized')

    def detect(self, image) -> List[Detection]:
        results = self.__yolov8_model(image, verbose=False)[0]
        
        (image_height, image_width) = results.orig_shape
        detection_tensor_list = results.boxes.data

        detections = []
        for detection_tensor in detection_tensor_list:
            normalized_x1 = float(detection_tensor[0] / image_width)
            normalized_y1 = float(detection_tensor[1] / image_height)
            normalized_x2 = float(detection_tensor[2] / image_width)
            normalized_y2 = float(detection_tensor[3] / image_height)

            bounding_box = BoundingBox(
                center_x=(normalized_x1 + normalized_x2) / 2,
                center_y=(normalized_y1 + normalized_y2) / 2,
                width=normalized_x2 - normalized_x1,
                height=normalized_y2 - normalized_y1,
            )

            detections.append(Detection(
                bounding_box=bounding_box,
                class_id=int(detection_tensor[5]),
                confidence=float(detection_tensor[4]),
            ))
        
        return detections
