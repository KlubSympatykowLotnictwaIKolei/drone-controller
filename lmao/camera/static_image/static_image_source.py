
from lmao.camera.camera_image_source import CameraImageSource
import cv2
import os

class StaticImageSource(CameraImageSource):

    def __init__(self, image_path: str = None):
        if image_path is None:
            image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        self.__image = cv2.imread(image_path)
    
    def capture_image(self):
        return self.__image
