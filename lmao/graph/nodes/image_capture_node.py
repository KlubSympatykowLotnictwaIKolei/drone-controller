
from ast import Dict
from lmao.camera.camera_image_source import CameraImageSource
from lmao.graph.lmao_graph_node import LmaoGraphNode


class ImageCaptureNode(LmaoGraphNode):
    """
    This node captures an image using a `CameraImageSource` service and stores the result in the signal.
    """
    
    def __init__(self, camera_image_source: CameraImageSource, output_key: str = 'image'):
        self.__camera_image_source = camera_image_source
        self.__output_key = output_key

    def process(self, signal: Dict):
        signal[self.__output_key] = self.__camera_image_source.capture_image()

    def tear_down(self):
        self.__camera_image_source.disconnect()