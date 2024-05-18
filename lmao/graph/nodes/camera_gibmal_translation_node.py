
from typing import Dict
from graph.lmao_graph_node import LmaoGraphNode
from graph.nodes.telemetry_estimation_node import TelemetrySnapshot
from types.attitude import Attitude
from types.camera import CameraGPS
from types.vector3d import Position3D, Vector3D
import copy

class CameraGimbalTranslationNode(LmaoGraphNode):
    
    def __init__(self, 
                 gimbal_translation_m: Vector3D, 
                 gimbal_attitude: Attitude, 
                 input_camera_key: str,
                 output_translated_camera_key: str,):
        self.__gimbal_position_m = gimbal_translation_m
        self.__gimbal_attitude = gimbal_attitude
        self.__input_camera_key = input_camera_key
        self.__output_translated_camera_key = output_translated_camera_key

    def process(self, signal: Dict):
        camera: CameraGPS = signal[self.__input_camera_key]
        gimbal_attitude = self.__gimbal_attitude
        gimbal_position = self.__gimbal_position_m

        original_camera_rotation = camera.rotation

        original_camera_rotation = camera.rotation
        gimbal_rotation = gimbal_attitude.to_projection_space_rotation()
        
        position_shift_3d = Vector3D(0, 0, -camera.position.relative_altitude) \
                         + gimbal_position.get_rotated(original_camera_rotation)
        position_shift_ned = position_shift_3d.three_d_to_ned_vector()
        
        final_position = camera.position.get_shifted_by_ned_vector(position_shift_ned)
        final_rotation = original_camera_rotation * gimbal_rotation

        final_camera = copy.copy(camera)
        camera.position = final_position
        camera.rotation = final_rotation

        signal[self.__output_translated_camera_key] = final_camera

