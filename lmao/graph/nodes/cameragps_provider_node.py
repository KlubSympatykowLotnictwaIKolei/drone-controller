
from lmao.graph.nodes.telemetry_estimation_node import TelemetrySnapshot
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.types.camera import CameraGPS
from typing import Dict

class CameraGpsProviderNode(LmaoGraphNode):

    def __init__(self,
                 input_camera_intrinsics_key: str,
                 input_telemetry_key: str, 
                 output_camera_key: str):
        self.__input_camera_intrincis_key = input_camera_intrinsics_key
        self.__input_telemetry_key = input_telemetry_key
        self.__output_camera_key = output_camera_key

    def process(self, signal: Dict):
        intrinsics: CameraGPS.Intrinsics = signal[self.__input_camera_intrincis_key]
        telemetry: TelemetrySnapshot = signal[self.__input_telemetry_key]

        extrinsics = CameraGPS.Extrinsics(
            position=telemetry.position,
            rotation=telemetry.attitude.to_projection_space_rotation()
        )

        signal[self.__output_camera_key] = CameraGPS.from_intrinsics_and_extrinsics(intrinsics, extrinsics)