
from lmao.detection.detector import BoundingBox, Detection, Detector
from .utils import blob, det_postprocess, letterbox
from .pycuda_api import TRTEngine
from typing import List

import logging as log
import numpy as np
import cv2

class YoloV8TensorrtDetector(Detector):

    def __init__(self, engine_path: str):
        import pycuda.driver as cuda
        
        cuda.init() 
        device = cuda.Device(0) 
        self.context = device.retain_primary_context()
        
        log.info('Loading YOLOv8 TensorRT model...')
        self.context.push()
        self.__trt_engine = TRTEngine(engine_path)
        self.context.pop()
        log.info('Model loaded')

    def detect(self, image) -> List[BoundingBox]:
        image_width = image.shape[1]
        image_height = image.shape[0]

        self.context.push()
        bboxes, scores, labels = self.__execute_inference(image)
        self.context.pop()

        detections = []
        for (bbox, confidence, class_id) in zip(bboxes, scores, labels):
            x1, y1, x2, y2 = bbox.round().astype(int).tolist()
            x1, x2 = x1/image_width, x2/image_width
            y1, y2 = y1/image_height, y2/image_height

            bounding_box = BoundingBox(
                center_x=(x1 + x2) / 2,
                center_y=(y1 + y2) / 2,
                width=x2 - x1,
                height=y2 - y1,
            )

            detections.append(Detection(bounding_box, class_id, confidence))

        return detections

    def __execute_inference(self, image):
        # This code was copied from https://github.com/triple-Mu/YOLOv8-TensorRT

        H, W = self.__trt_engine.inp_info[0].shape[-2:]
        bgr = image
        bgr, ratio, dwdh = letterbox(bgr, (W, H))
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        tensor = blob(rgb, return_seg=False)
        dwdh = np.array(dwdh * 2, dtype=np.float32)
        tensor = np.ascontiguousarray(tensor)

        data = self.__trt_engine(tensor)
        
        bboxes, scores, labels = det_postprocess(data)
        bboxes -= dwdh
        bboxes /= ratio

        return (bboxes, scores, labels)
