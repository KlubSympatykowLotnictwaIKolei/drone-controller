
import numpy as np
from lmao.detection.detector import Detection
from typing import List
import cv2

def opencv_show_detections(image, detection_list: List[Detection]):
    image = image.copy()

    COLOR = (255, 0, 0)
    IMAGE_WIDTH = image.shape[1]
    IMAGE_HEIGHT = image.shape[0]
    BOUNDING_BOX_THICKNESS = 2
    TEXT_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
    TEXT_SCALE = 0.75
    TEXT_THICKNESS = 2
    TEXT_COLOR = (255, 255, 255)
    TEXT_MARGIN = 5

    for detection in detection_list:
        bounding_box = detection.bounding_box
        x1 = bounding_box.center_x - bounding_box.width/2
        x2 = bounding_box.center_x + bounding_box.width/2
        y1 = bounding_box.center_y - bounding_box.height/2
        y2 = bounding_box.center_y + bounding_box.height/2

        x1, x2 = (np.array([x1, x2]) * IMAGE_WIDTH).astype(int)
        y1, y2 = (np.array([y1, y2]) * IMAGE_HEIGHT).astype(int)

        label = f'{detection.class_id} conf:{detection.confidence:.3f}'

        (w, h), _ = cv2.getTextSize(label, TEXT_FONT_FACE, TEXT_SCALE, TEXT_THICKNESS)
        w, h = w + 2*TEXT_MARGIN, h + 2*TEXT_MARGIN

        cv2.rectangle(
            image, 
            (x1, y1 - h - 2), 
            (x1 + w, y1), 
            COLOR, 
            -1)
        cv2.putText(
            image,
            label, 
            (x1 + TEXT_MARGIN, y1 - TEXT_MARGIN - 2),
            TEXT_FONT_FACE,
            TEXT_SCALE, 
            TEXT_COLOR,
            TEXT_THICKNESS
        )
        cv2.rectangle(
            image, 
            (x1, y1), 
            (x2, y2), 
            COLOR, 
            BOUNDING_BOX_THICKNESS
        )

    cv2.imshow('result', image)
    cv2.waitKey(1)