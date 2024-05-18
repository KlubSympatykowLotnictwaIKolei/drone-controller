
from dataclasses import dataclass
from typing import Tuple
from scipy.spatial.transform import Rotation

import math

@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    def get_scaled(self, factor: float) -> 'Vector3D':
        return Vector3D(
            self.x * factor,
            self.y * factor,
            self.z * factor,
        )
    
    def get_rotated(self, rotation: Rotation) -> 'Vector3D':
        rotated_coordinates = rotation.apply([self.x, self.y, self.z])
        return Vector3D(rotated_coordinates[0], rotated_coordinates[1], rotated_coordinates[2])

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D.add(self, other)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D.add(self, other.get_scaled(-1))
    
    def get_magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def three_d_to_ned_vector(self) -> 'Vector3D':
        return Vector3D(self.y, self.x, -self.z)
    
    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]) -> 'Vector3D':
        return Vector3D(tuple[0], tuple[1], tuple[2])

    @classmethod
    def zero(cls) -> 'Vector3D':
        return Vector3D(0, 0, 0)
    
    @classmethod
    def up(cls) -> 'Vector3D':
        return Vector3D(0, 0, 1)
    
    @classmethod
    def down(cls) -> 'Vector3D':
        return Vector3D(0, 0, -1)

    @classmethod
    def add(cls, vec1: 'Vector3D', vec2: 'Vector3D') -> 'Vector3D':
        return Vector3D(
            vec1.x + vec2.x,
            vec1.y + vec2.y,
            vec1.z + vec2.z,
        )
    
    @classmethod
    def multiply(cls, vec1: 'Vector3D', vec2: 'Vector3D') -> 'Vector3D':
        return Vector3D(
            vec1.x * vec2.x,
            vec1.y * vec2.y,
            vec1.z * vec2.z,
        )
    
    @classmethod
    def dot(cls, vec1: 'Vector3D', vec2: 'Vector3D') -> float:
        return vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z

Position3D = Vector3D
