
from lmao.types import PositionGPS, Camera3D, CameraGPS, Vector3D
from ..bounding_box_to_gps_converter import BoundingBoxToGpsConverter
from ..screen_to_plane_position_converter import ScreenToPlanePositionConverter
from ..ray_casting import Plane
from lmao.detection.detector import BoundingBox
from enum import Enum

from dataclasses import dataclass
from typing import Optional
from pyproj import Geod

import numpy as np
import math
    
class BoxPositionEnum(Enum):
    CENTER = (0.5,0.5);
    BOTTOM_CENTER = (0.5,1);
    TOP_CENTER = (0.5,0);
    CENTER_LEFT = (0,0.5);
    CENTER_RIGHT = (1,0.5);

class SimpleBoundingBoxToGpsConverter(BoundingBoxToGpsConverter):
    """
    The simplest implementation of `BoundingBoxToGpsConverter`. It assumes that the center 
    of an object is at the center of the bounding box on screen.
    """

    def __init__(self, box_position_enum: BoxPositionEnum = BoxPositionEnum.CENTER):
        self.__screen_to_plane_position_converter = ScreenToPlanePositionConverter()
        self.__box_position_enum = box_position_enum

    def convert_to_ground_position(self, 
            camera_gps: CameraGPS,
            bbox: BoundingBox,
            ) -> Optional[PositionGPS]:
        
        camera_3d = Camera3D(
            position=Vector3D(0, 0, camera_gps.relative_altitude),
            rotation=camera_gps.rotation,
            horizontal_fov=self.__camera_parameters.physical_parameters.get_horizontal_fov(),
            vertical_fov=self.__camera_parameters.physical_parameters.get_vertical_fov(),
        )
    
        ground_object_relative_3d_position = self.__screen_to_plane_position_converter.calculate_plane_point(
            Plane.ground(), 
            camera_3d, 
            bbox.convert_local_to_image_point(self.__box_position_enum.value[0], self.__box_position_enum.value[1])
        )
        
        if ground_object_relative_3d_position is None:
            return None
        
        ground_object_relative_ned_position = ground_object_relative_3d_position.three_d_to_ned_vector()
        
        ground_object_gps_position =  camera_gps.position.get_shifted_by_ned_vector(ground_object_relative_ned_position)
        ground_object_gps_position.relative_altitude = 0

        return ground_object_gps_position
