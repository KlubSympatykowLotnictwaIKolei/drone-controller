
import math
from lmao.types import Vector3D
from dataclasses import dataclass
from typing import Optional

@dataclass
class Plane:
    """
    Mathematical concept of a plane, not the flying type! xd
    """
    point_on_the_plane: Vector3D
    normal: Vector3D

    @classmethod
    def ground(cls) -> 'Plane':
        return Plane(
            point_on_the_plane=Vector3D.zero(), 
            normal=Vector3D.up()
        )

@dataclass
class Ray:
    origin: Vector3D
    direction: Vector3D

    def get_point_at(self, t: float) -> Vector3D:
        return self.origin + self.direction.get_scaled(t)

    def find_plane_intersection(self, plane: Plane) -> Optional[Vector3D]:
        """ 
        Algorithm modified from 
        https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection.html
        """
        
        denominator = Vector3D.dot(self.direction, plane.normal)

        if math.fabs(denominator) <= 1e-6:
            return None
        
        ray_origin_to_plane_point_vector = plane.point_on_the_plane - self.origin
        t = Vector3D.dot(ray_origin_to_plane_point_vector, plane.normal) / denominator

        if t < 0:
            return None

        return Vector3D.add(self.origin, self.direction.get_scaled(t))