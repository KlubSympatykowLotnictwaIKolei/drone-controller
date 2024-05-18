
from lmao.types import Vector3D, Camera3D
from .ray_casting import Plane, Ray
from typing import Optional, Tuple
import math

class ScreenToPlanePositionConverter:
    """
    Class for calculating point on a plane based on its screen position from the prespective of a specific camera.
    """
    
    def calculate_plane_point(self, plane: Plane, camera: Camera3D, screen_position: Tuple[float, float]) -> Optional[Vector3D]:
        """
        This function takes screen position of a point and tries to see where this point lands on the plane.
        If there is no such point, it returns None. 
        """

        rescaled_x = screen_position[0] * 2.0 - 1.0
        rescaled_y = screen_position[1] * 2.0 - 1.0
        
        ray_direction = Vector3D(
            math.tan(camera.horizontal_fov / 2.0) * rescaled_x,
            -math.tan(camera.vertical_fov / 2.0) * rescaled_y,
            -1
        )
        ray_direction = ray_direction.get_rotated(camera.rotation)
        
        ray = Ray(camera.position, ray_direction)

        return ray.find_plane_intersection(plane)
    