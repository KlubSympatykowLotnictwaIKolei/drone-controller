import math

from analysis.config.camera_parameters import CameraFov


from .validators.distance import distance_validator
from .validators.angle import angle_validator

from pydantic import BaseModel, validator, ValidationError
from typing import Optional, Union

import logging as log
import yaml


class AngleCameraFov(BaseModel, CameraFov):
    horizontal_fov: float
    vertical_fov: float

    __horizontal_fov_validator = validator(
        'horizontal_fov', allow_reuse=True, pre=True
    )(angle_validator)

    __vertical_fov_validator = validator(
        'vertical_fov', allow_reuse=True, pre=True
    )(angle_validator)

    def get_horizontal_fov(self) -> float:
        return self.horizontal_fov

    def get_vertical_fov(self) -> float:
        return self.vertical_fov


class CalculatedCameraFov(BaseModel, CameraFov):
    sensor_width: float
    sensor_height: float
    focal_length: float

    __sensor_width_validator = validator(
        'sensor_width', allow_reuse=True, pre=True
        )(distance_validator)
    
    __sensor_height_validator = validator(
        'sensor_height', allow_reuse=True, pre=True
        )(distance_validator)
    
    __focal_length_validator = validator(
        'focal_length', allow_reuse=True, pre=True
        )(distance_validator)
        

    def get_horizontal_fov(self) -> float:
        return 2*math.atan(self.sensor_width/(2*self.focal_length))

    def get_vertical_fov(self) -> float:
        return 2*math.atan(self.sensor_height/(2*self.focal_length))


class CameraParameters(BaseModel):
    type: str  # Literal["airsim", "pylon", "static"]
    physical_parameters: Union[AngleCameraFov, CalculatedCameraFov]


class ConfigFileGimbalPosition(BaseModel):
    forward: float
    right: float
    up: float

    __forward_validator = validator(
        'forward', allow_reuse=True, pre=True
        )(distance_validator)
    
    __right_validator = validator(
        'right', allow_reuse=True, pre=True
        )(distance_validator)
    __up_validator = validator(
        'up', allow_reuse=True, pre=True
        )(distance_validator)

class ConfigFileGimbalAttitude(BaseModel):
    roll: float
    pitch: float
    yaw: float

    __roll_validator = validator(
        'roll', allow_reuse=True, pre=True
        )(angle_validator)
    
    __pitch_validator = validator(
        'pitch', allow_reuse=True, pre=True
        )(angle_validator)
    
    __yaw_validator = validator(
        'yaw', allow_reuse=True, pre=True
        )(angle_validator)

class GimbalParameters(BaseModel):
    position: ConfigFileGimbalPosition
    rotation: ConfigFileGimbalAttitude


class DetectorParameters(BaseModel):
    type: str  # Literal["ultralytics", "tensorrt", "static", "none"]
    path: Optional[str] = None


class LiveViewParameters(BaseModel):
    type: str  # Literal["gstreamer", "opencv", "none"]


class CommunicationChannelParameters(BaseModel):
    type: str
    address: Optional[str] = None


class CommunicationParameters(BaseModel):
    telemetry: CommunicationChannelParameters  # "mavlink" | "redis" | "none"
    mission: CommunicationChannelParameters  # "mavlink" | "redis"


class LmaoConfig(BaseModel):
    detector: DetectorParameters
    gimbal: GimbalParameters
    camera: CameraParameters
    live_view: LiveViewParameters
    communication: CommunicationParameters


class LmaoConfigLoader:
    def load_from_file(self, path: str, fancy_errors: bool = True) -> LmaoConfig:
        """
        Load a LmaoConfig from a file
        Args:
            path (str): Path to the file
            fancy_errors (bool): If True, will print a more human readable error message, if you can't comprehend curret error message, change this
        """
        with open(path) as file:
            file = file.read()
            config_dict = yaml.safe_load(file)
            try:
                return LmaoConfig(**config_dict)
            except ValidationError as e:
                # ErrorDisplay()(e, file.split('\n'), fancy_errors)
                raise ValueError("Invalid config file")
