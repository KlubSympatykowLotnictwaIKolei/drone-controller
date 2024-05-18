
from ..camera_image_source import CameraImageSource
from .client import VehicleClient
from .types import ImageType

import numpy as np
import cv2

class AirSimCameraImageSource(CameraImageSource):

    def __init__(self, camera_name: str = 'drone_cam'):
        self.__airsim_client = VehicleClient()
        self.__camera_name = camera_name

    def capture_image(self):
        raw_image_buffer = self.__airsim_client.simGetImage(self.__camera_name, ImageType.Scene)
        numpy_image_buffer = np.frombuffer(raw_image_buffer, dtype=np.uint8) 
        image = cv2.imdecode(numpy_image_buffer, cv2.IMREAD_COLOR)

        return image
